#	x509sak - The X.509 Swiss Army Knife white-hat certificate toolkit
#	Copyright (C) 2019-2019 Johannes Bauer
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

from x509sak.HexDump import HexDump

class DataBufferException(Exception): pass
class NotEnoughDataException(DataBufferException): pass

class _RewindObject():
	def __init__(self, data_buffer):
		self._data_buffer = data_buffer
		self._pos = None

	def __enter__(self):
		assert(self._pos is None)
		self._pos = self._data_buffer.offset

	def __exit__(self, exception_class, exception, traceback):
		if exception_class is not None:
			# Exception was thrown, rewind.
			self._data_buffer.offset = self._pos

class DataBuffer():
	def __init__(self, initial_value = None):
		if initial_value is None:
			self._data = bytearray()
		else:
			self._data = bytearray(initial_value)
		self._offset = 0

	@classmethod
	def fromhex(cls, hex_str):
		return cls(bytes.fromhex(hex_str))

	@property
	def offset(self):
		return self._offset

	@offset.setter
	def offset(self, value):
		assert(0 <= value <= self.length)
		self._offset = value

	@property
	def length(self):
		return len(self._data)

	@property
	def remaining(self):
		return self.length - self.offset

	def rewind_on_exception(self):
		return _RewindObject(self)

	def get(self, length):
		if length > self.remaining:
			raise NotEnoughDataException("%d bytes requested from data buffer, but only %d bytes remaining." % (length, self.remaining))
		returned_data = self._data[self.offset : self.offset + length]
		self._offset += length
		return returned_data

	def append(self, data):
		self += data

	def hexdump(self):
		print("%s" % (self))
		HexDump().dump(self._data)

	def __iadd__(self, other):
		self._data += other
		return self

	def __iter__(self):
		return iter(self._data)

	def __str__(self):
		return "DataBuffer<%d (0x%x) bytes, offset %d (0x%x), remaining %d (0x%x)>" % (self.length, self.length, self.offset, self.offset, self.remaining, self.remaining)
