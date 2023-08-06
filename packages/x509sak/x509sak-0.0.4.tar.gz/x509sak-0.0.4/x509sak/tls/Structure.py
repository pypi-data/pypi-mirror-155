#	x509sak - The X.509 Swiss Army Knife white-hat certificate toolkit
#	Copyright (C) 2019-2020 Johannes Bauer
#
#	This file is part of x509sak.
#
#	x509sak is free software; you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation; this program is ONLY licensed under
#	version 3 of the License, later versions are explicitly excluded.
#
#	x509sak is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with x509sak; if not, write to the Free Software
#	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#	Johannes Bauer <JohannesBauer@gmx.de>

import re
from x509sak.tls.DataBuffer import DataBuffer, DataBufferException
from x509sak.Exceptions import ProgrammerErrorException, InvalidInputException

class StructureException(Exception): pass

class SerializationException(StructureException): pass
class DeserializationException(StructureException): pass

class InvalidInputTypeException(SerializationException): pass
class NoPossibleSerializationException(SerializationException): pass

class NoMoreDataToUnpackException(DeserializationException): pass
class InfiniteUnpackingException(DeserializationException): pass
class IncompleteUnpackingException(DeserializationException): pass
class UnexpectedFixedValueException(DeserializationException): pass
class NoPossibleDeserializationException(DeserializationException): pass

class BaseStructureMember():
	def __init__(self, name = None):
		self._name = name

	@property
	def name(self):
		return self._name

	def pack(self, values):
		raise NotImplementedError(self.__class__.__name__)

	def _unpack(self, databuffer):
		raise NotImplementedError(self.__class__.__name__)

	def unpack(self, databuffer):
		try:
			return self._unpack(databuffer)
		except DataBufferException as e:
			raise NoMoreDataToUnpackException(e)

class StructureMemberFactory():
	_REGISTERED = [ ]

	def __init__(self):
		pass

	@classmethod
	def register(cls, element_class):
		regex = re.compile(element_class._REGEX)
		cls._REGISTERED.append((regex, element_class))
		return element_class

	@classmethod
	def instantiate(cls, name, typename, **kwargs):
		for (regex, element_class) in cls._REGISTERED:
			match = regex.fullmatch(typename)
			if match:
				match = match.groupdict()
				return element_class.from_match(name, match, **kwargs)
		raise ProgrammerErrorException("No handler for type '%s' found." % (typename))

class StructureMemberFactoryElement(BaseStructureMember):
	_REGEX = None

	@classmethod
	def from_match(cls, name, match, **kwargs):
		raise NotImplementedError(cls.__name__)

	@property
	def typename(self):
		return None

	@property
	def implicit_value(self):
		return False

	def __repr__(self):
		cname = self.typename if (self.typename is not None) else self.__class__.__name__
		return "%s %s" % (cname, self.name)

@StructureMemberFactory.register
class StructureElementFixed(StructureMemberFactoryElement):
	_REGEX = r"fixed\[(?P<hexdata>[0-9a-fA-F\s]+)\]"

	def __init__(self, name, fixed_data):
		StructureMemberFactoryElement.__init__(self, name)
		self._fixed_data = fixed_data

	@classmethod
	def from_match(cls, name, match, **kwargs):
		fixed_data = bytes.fromhex(match["hexdata"])
		return cls(name = name, fixed_data = fixed_data, **kwargs)

	@property
	def typename(self):
		return "fixed[%s]" % (self._fixed_data.hex())

	@property
	def implicit_value(self):
		return True

	def _unpack(self, databuffer):
		data = databuffer.get(len(self._fixed_data))
		if data != self._fixed_data:
			raise UnexpectedFixedValueException("%s unpacking expected %s but got %s." % (str(self), self._fixed_data.hex(), data.hex()))
		return data

	def pack(self):
		return self._fixed_data

@StructureMemberFactory.register
class StructureElementInteger(StructureMemberFactoryElement):
	_REGEX = r"uint(?P<bit>\d+)"

	def __init__(self, name, length_bytes, enum_class = None, strict_enum = False, fixed_value = None):
		StructureMemberFactoryElement.__init__(self, name)
		self._length_bytes = length_bytes
		self._enum_class = enum_class
		self._strict_enum = strict_enum
		self._fixed_value = fixed_value
		self._minval = 0
		self._maxval = (1 << (8 * self._length_bytes)) - 1

	@classmethod
	def from_match(cls, name, match, **kwargs):
		length_bits = int(match["bit"])
		assert((length_bits % 8) == 0)
		length_bytes = length_bits // 8
		return cls(name = name, length_bytes = length_bytes, **kwargs)

	@property
	def typename(self):
		return "uint%d" % (self._length_bytes * 8)

	@property
	def implicit_value(self):
		return self._fixed_value is not None

	def _unpack(self, databuffer):
		data = databuffer.get(self._length_bytes)
		value = int.from_bytes(data, byteorder = "big")
		if self._enum_class is not None:
			try:
				value = self._enum_class(value)
			except ValueError:
				if self._strict_enum:
					raise
		if self._fixed_value and (value != self._fixed_value):
			raise UnexpectedFixedValueException("Deserialization requires fixed value 0x%x but encountered 0x%x." % (self._fixed_value, value))
		return value

	def pack(self, value = None):
		if (value is None) and (self._fixed_value is not None):
			value = self._fixed_value
		if not isinstance(value, int):
			raise InvalidInputTypeException("%s requires int to be supplied for packing, got %s: %s" % (self.typename, type(value).__name__, str(value)))
		if self._enum_class is not None:
			if self._strict_enum:
				if not isinstance(value, self._enum_class):
					raise InvalidInputException("%s packing input must be of type %s." % (str(self), self._enum_class))
			value = int(value)
		if (value < self._minval) or (value > self._maxval):
			raise InvalidInputException("%s must be between %d and %d (given value was %d)." % (str(self), self._minval, self._maxval, value))
		data = int.to_bytes(value, byteorder = "big", length = self._length_bytes)
		return data

@StructureMemberFactory.register
class StructureElementOpaque(StructureMemberFactoryElement):
	_REGEX = r"opaque(?P<bit>\d+)"

	def __init__(self, name, length_field, inner = None, contains_array = None, string_encoding = None, fixed_value = None, allow_trailing_data = False):
		StructureMemberFactoryElement.__init__(self, name)
		self._length_field = length_field
		self._inner = inner
		self._contains_array = contains_array
		self._string_encoding = string_encoding
		self._fixed_value = fixed_value
		self._allow_trailing_data = allow_trailing_data
		if (self._string_encoding is not None) and (self._inner is not None):
			raise ProgrammerErrorException("Opaque object can either encode strings or have an inner object, but not both.")

	@classmethod
	def from_match(cls, name, match, **kwargs):
		length_field = StructureMemberFactory.instantiate(name = "length", typename = "uint" + match["bit"])
		return cls(name, length_field = length_field, **kwargs)

	@property
	def typename(self):
		return "opaque<%s>" % (self._length_field)

	@property
	def implicit_value(self):
		return self._fixed_value is not None

	def _unpack(self, databuffer):
		length = self._length_field.unpack(databuffer)
		data = databuffer.get(length)
		if (self._string_encoding is not None):
			data = data.decode(self._string_encoding)
		elif self._inner is not None:
			db = DataBuffer(data)
			if not self._contains_array:
				data = self._inner.unpack(db)
			else:
				result_array = [ ]
				while db.remaining > 0:
					pre_unpack = db.remaining
					result_array.append(self._inner.unpack(db))
					if pre_unpack == db.remaining:
						raise InfiniteUnpackingException("Inner unpacking of %s consumed no data, still %d bytes remaining. Breaking infinite loop." % (str(self._inner), db.remaining))
				data = result_array
			if (db.remaining > 0) and (not self._allow_trailing_data):
				raise IncompleteUnpackingException("%s unpacking still has %d bytes of trailing, non-consumed data left." % (self.typename, db.remaining))
		return data

	def pack(self, data = None):
		if (data is None) and (self._fixed_value is not None):
			data = self._fixed_value

		if (self._string_encoding is not None):
			data = data.encode(self._string_encoding)
		elif self._inner is not None:
			if not self._contains_array:
				data = self._inner.pack(data)
			else:
				packed_data = bytearray()
				for element in data:
					packed_data += self._inner.pack(element)
				data = packed_data

		if not isinstance(data, (bytes, bytearray)):
			raise InvalidInputTypeException("%s requires bytes/bytearray to be supplied for packing, got %s: %s" % (self.typename, type(data).__name__, str(data)))
		return self._length_field.pack(len(data)) + data

@StructureMemberFactory.register
class StructureElementArray(StructureMemberFactoryElement):
	_REGEX = r"array\[(?P<length>\d+)(,\s+(?P<padbyte>[0-9a-fA-F]{2}))?\]"

	def __init__(self, name, length, padbyte = None):
		StructureMemberFactoryElement.__init__(self, name)
		self._length = length
		self._padbyte = padbyte

	@classmethod
	def from_match(cls, name, match, **kwargs):
		length = int(match["length"])
		if match["padbyte"] is not None:
			padbyte = int(match["padbyte"], 16)
		else:
			padbyte = None
		return cls(name, length = length, padbyte = padbyte, **kwargs)

	@property
	def typename(self):
		if self._padbyte is None:
			return "array[%d]" % (self._length)
		else:
			return "array[%d, %02x]" % (self._length, self._padbyte)

	def _unpack(self, databuffer):
		return databuffer.get(self._length)

	def pack(self, data):
		if self._padbyte is None:
			# Size must exactly match up
			if len(data) == self._length:
				return data
			else:
				raise InvalidInputException("For packing of array of length %d without padding, %d bytes must be provided. Got %d bytes." % (self._length, self._length, len(data)))
		else:
			# Can pad
			if len(data) <= self._length:
				pad_len = self._length - len(data)
				padding = bytes([ self._padbyte ]) * pad_len
				return data + padding
			else:
				raise InvalidInputException("For packing of array of length %d with padding, at most %d bytes must be provided. Got %d bytes." % (self._length, self._length, len(data)))

class Structure(BaseStructureMember):
	def __init__(self, members, name = None):
		BaseStructureMember.__init__(self, name = name)
		self._members = members
		self._required_keys = set(member.name for member in members if (not member.implicit_value))
		explicit_member_count = sum(1 for member in members if (not member.implicit_value))
		if len(self._required_keys) != explicit_member_count:
			raise ProgrammerErrorException("Structure definition amgiguous, duplicate member names used.")

	@property
	def typename(self):
		return "Structure"

	@property
	def implicit_value(self):
		return False

	@property
	def members(self):
		return iter(self._members)

	def pack(self, values):
		if not isinstance(values, dict):
			raise InvalidInputTypeException("%s requires a dict to be supplied for packing, got %s: %s" % (self.typename, type(values).__name__, str(values)))

		# First check if all members are present
		present_keys = set(values.keys())
		missing_keys = self._required_keys - present_keys
		if len(missing_keys) > 0:
			raise ProgrammerErrorException("Missing keys in %s: %s" % (self.__class__.__name__, ", ".join(sorted(missing_keys))))

		result_data = bytearray()
		for member in self.members:
			if not member.implicit_value:
				value = values[member.name]
				result_data += member.pack(value)
			else:
				# Data is implicit
				result_data += member.pack()
		return bytes(result_data)

	def _unpack(self, databuffer):
		result = { }
		with databuffer.rewind_on_exception():
			for member in self.members:
				value = member.unpack(databuffer)
				if not member.implicit_value:
					result[member.name] = value
			return result

	def __repr__(self):
		if self.name is None:
			return "%s" % (self.typename)
		else:
			return "%s(%s)" % (self.typename, self.name)

	def __str__(self):
		return "%s<%s>" % (self.name, ", ".join(("%s %s" % (member.name, member.typename) for member in self.members)))

class VariableType(BaseStructureMember):
	def __init__(self, possible_inner_classes, name = None):
		BaseStructureMember.__init__(self, name = name)
		self._possible_inner_classes = possible_inner_classes

	@property
	def typename(self):
		return "Variable"

	def pack(self, type_value_tuple):
		if not isinstance(type_value_tuple, tuple):
			raise InvalidInputTypeException("%s requires a tuple to be supplied for packing, got %s: %s" % (self.typename, type(type_value_tuple).__name__, str(type_value_tuple)))
		if len(type_value_tuple) != 2:
			raise InvalidInputTypeException("%s requires a 2-tuple to be supplied for packing, got %d-tuple: %s" % (self.typename, len(type_value_tuple), str(type_value_tuple)))
		(inner_class, values) = type_value_tuple
		return inner_class.pack(values)

	def _unpack(self, databuffer):
		for possible_inner_class in self._possible_inner_classes:
			try:
				unpacking = possible_inner_class.unpack(databuffer)
			except (DeserializationException, DataBufferException):
				continue
			return (possible_inner_class, unpacking)
		raise NoPossibleDeserializationException("Attempts to deserialize all possible %d inner classes were unsuccessful." % (len(self._possible_inner_classes)))

def instantiate_member(name, typename, **kwargs):
	return StructureMemberFactory.instantiate(name, typename, **kwargs)
