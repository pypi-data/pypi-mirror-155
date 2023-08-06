#	x509sak - The X.509 Swiss Army Knife white-hat certificate toolkit
#	Copyright (C) 2018-2020 Johannes Bauer
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

import contextlib
import collections
import pyasn1.error
import pyasn1.type.univ
from pyasn1.type import tag
from pyasn1_modules import rfc2459, rfc5280
from x509sak.OID import OID, OIDDB
from x509sak import ASN1Models
from x509sak.ASN1Wrapper import ASN1GeneralNameWrapper, ASN1GeneralNamesWrapper
from x509sak.Tools import ASN1Tools
from x509sak.OtherModels import SignedCertificateTimestampList
from x509sak.tls.DataBuffer import DataBuffer
from x509sak.tls.Structure import DeserializationException
from x509sak.Exceptions import InvalidInputException
from x509sak.DistinguishedName import RelativeDistinguishedName

class X509Extensions():
	def __init__(self, extensions):
		self._exts = extensions

	def get_all(self, oid):
		assert(isinstance(oid, OID))
		return [ extension for extension in self._exts if extension.oid == oid ]

	def get_first(self, oid):
		assert(isinstance(oid, OID))
		exts = self.get_all(oid)
		if len(exts) == 0:
			return None
		else:
			return exts[0]

	def remove_all(self, oid):
		assert(isinstance(oid, OID))
		self._exts = [ extension for extension in self._exts if extension.oid != oid ]
		return self

	def filter(self, oid, replacement_extension):
		assert(isinstance(oid, OID))
		self._exts = [ extension if (extension.oid != oid) else replacement_extension for extension in self._exts ]
		return self

	def has(self, oid):
		assert(isinstance(oid, OID))
		return any(extension.oid == oid for extension in self._exts)

	def dump(self, indent = ""):
		print("%sTotal of %d X.509 extensions present:" % (indent, len(self)))
		for (eid, ext) in enumerate(self, 1):
			print("%sExtension %d: %s%s" % (indent + "    ", eid, ext.__class__.__name__, " [critical]" if ext.critical else ""))
			ext.dump(indent = indent + "        ")

	def to_asn1(self):
		extension_list = [ extension.to_asn1() for extension in self ]
		extensions_asn1 = rfc2459.TBSCertificate()["extensions"]
		extensions_asn1.setComponents(*extension_list)
		return extensions_asn1

	def __getitem__(self, index):
		return self._exts[index]

	def __iter__(self):
		return iter(self._exts)

	def __len__(self):
		return len(self._exts)

	def __str__(self):
		return "X509Extensions<%d>" % (len(self))

class X509ExtensionRegistry():
	_KNOWN_EXTENSIONS = { }
	_DEFAULT_CLASS = None

	@classmethod
	def set_default_class(cls, handler):
		cls._DEFAULT_HANDLER = handler

	@classmethod
	def install_handler_class(cls, handler):
		oid = handler.get_handler_oid()
		cls._KNOWN_EXTENSIONS[oid] = handler
		return handler

	@classmethod
	def create(cls, oid, critical, data):
		if oid in cls._KNOWN_EXTENSIONS:
			return cls._KNOWN_EXTENSIONS[oid](oid, critical, data)
		else:
			return cls._DEFAULT_HANDLER(oid, critical, data)

class X509Extension():
	_HANDLER_OID = None
	_ASN1_MODEL = None

	def __init__(self, oid, critical, data):
		assert(isinstance(oid, OID))
		assert(isinstance(critical, bool))
		assert(isinstance(data, bytes))
		self._oid = oid
		self._critical = critical
		self._data = data
		self._detailed_asn1 = None
		spec = self._ASN1_MODEL() if (self._ASN1_MODEL is not None) else None
		self._detailed_asn1 = ASN1Tools.safe_decode(self.data, asn1_spec = spec)
		self._decode_hook()

	def to_asn1(self):
		extension = rfc2459.Extension()
		extension["extnID"] = self.oid.to_asn1()
		extension["critical"] = self.critical
		extension["extnValue"] = self.data
		return extension

	@classmethod
	def construct_from_asn1(cls, asn1, critical = False):
		data = pyasn1.codec.der.encoder.encode(asn1)
		return cls(oid = cls._HANDLER_OID, data = data, critical = critical)

	@classmethod
	def get_handler_oid(cls):
		return cls._HANDLER_OID

	@property
	def asn1_model(self):
		return self._ASN1_MODEL

	@property
	def oid(self):
		return self._oid

	@property
	def critical(self):
		return self._critical

	@property
	def data(self):
		return self._data

	@property
	def detailed_asn1(self):
		return self._detailed_asn1

	@property
	def asn1(self):
		return self._detailed_asn1.asn1

	def _decode_hook(self):
		pass

	@property
	def format_value(self):
		return self.data.hex()

	@property
	def known(self):
		return self.oid in OIDDB.X509Extensions

	@property
	def name(self):
		if self.known:
			name = OIDDB.X509Extensions[self.oid]
		else:
			name = str(self.oid)
		return name

	def dump(self, indent = ""):
		print("%s%s" % (indent, str(self)))

	def __repr__(self):
		return "%s<%s = %s>" % (self.__class__.__name__, self.name, self.format_value)
X509ExtensionRegistry.set_default_class(X509Extension)


@X509ExtensionRegistry.install_handler_class
class X509SubjectKeyIdentifierExtension(X509Extension):
	_HANDLER_OID = OIDDB.X509Extensions.inverse("SubjectKeyIdentifier")
	_ASN1_MODEL = rfc2459.SubjectKeyIdentifier

	@classmethod
	def construct(cls, keyid):
		assert(isinstance(keyid, bytes))
		assert(len(keyid) == 20)
		return cls.construct_from_asn1(cls._ASN1_MODEL(keyid), critical = False)

	@property
	def keyid(self):
		return self._keyid

	@property
	def format_value(self):
		if self.keyid is not None:
			return "KeyID %s" % (self.keyid.hex())
		else:
			return "Invalid KeyID"

	def __eq__(self, other):
		return self.keyid == other.keyid

	def _decode_hook(self):
		if self.asn1 is not None:
			self._keyid = bytes(self.asn1)
		else:
			self._keyid = None


@X509ExtensionRegistry.install_handler_class
class X509AuthorityKeyIdentifierExtension(X509Extension):
	_HANDLER_OID = OIDDB.X509Extensions.inverse("AuthorityKeyIdentifier")
	_ASN1_MODEL = rfc2459.AuthorityKeyIdentifier

	@classmethod
	def construct(cls, keyid):
		assert(isinstance(keyid, bytes))
		assert(len(keyid) > 0)
		asn1 = cls._ASN1_MODEL()
		asn1["keyIdentifier"] = keyid
		return cls.construct_from_asn1(asn1, critical = False)

	@property
	def keyid(self):
		return self._keyid

	@property
	def ca_names(self):
		return self._ca_names

	@property
	def serial(self):
		return self._serial

	@property
	def format_value(self):
		values = [ ]
		if self.keyid is not None:
			values.append("KeyID %s" % (self.keyid.hex()))
		if self.ca_names is not None:
			values.append("CAName {%s}" % (", ".join(str(name) for name in self.ca_names)))
		if self.serial is not None:
			values.append("Serial %x" % (self.serial))
		return ", ".join(values)

	def _decode_hook(self):
		if self.asn1 is not None:
			if self.asn1.getComponentByName("keyIdentifier", None, instantiate = False) is not None:
				self._keyid = bytes(self.asn1["keyIdentifier"])
			else:
				self._keyid = None
			if self.asn1.getComponentByName("authorityCertIssuer", None, instantiate = False) is not None:
				self._ca_names = [ ASN1GeneralNameWrapper.from_asn1(generalname) for generalname in self.asn1["authorityCertIssuer"] ]
			else:
				self._ca_names = None
			if self.asn1.getComponentByName("authorityCertSerialNumber", None, instantiate = False) is not None:
				self._serial = int(self.asn1["authorityCertSerialNumber"])
			else:
				self._serial = None
		else:
			self._keyid = None
			self._ca_names = None
			self._serial = None


@X509ExtensionRegistry.install_handler_class
class X509BasicConstraintsExtension(X509Extension):
	_HANDLER_OID = OIDDB.X509Extensions.inverse("BasicConstraints")
	_ASN1_MODEL = rfc2459.BasicConstraints

	@property
	def pathlen(self):
		if self.asn1 is None:
			return None
		if self.asn1["pathLenConstraint"].hasValue():
			return int(self.asn1["pathLenConstraint"])
		else:
			return None

	@property
	def is_ca(self):
		if self.asn1 is not None:
			return bool(self.asn1["cA"])
		else:
			return False

	def __repr__(self):
		return "%s<CA = %s>" % (self.__class__.__name__, self.is_ca)


@X509ExtensionRegistry.install_handler_class
class X509ExtendedKeyUsageExtension(X509Extension):
	_HANDLER_OID = OIDDB.X509Extensions.inverse("ExtendedKeyUsage")
	_ASN1_MODEL = rfc2459.ExtKeyUsageSyntax

	def _decode_hook(self):
		if self.asn1 is not None:
			self._oids = [ OID.from_str(str(oid)) for oid in self.asn1 ]
		else:
			self._oids = [ ]

	@property
	def key_usage_oids(self):
		return iter(self._oids)

	@property
	def any_key_usage(self):
		return OIDDB.X509ExtendedKeyUsage.inverse("anyExtendedKeyUsage") in self._oids

	@property
	def client_auth(self):
		return OIDDB.X509ExtendedKeyUsage.inverse("id_kp_clientAuth") in self._oids

	@property
	def server_auth(self):
		return OIDDB.X509ExtendedKeyUsage.inverse("id_kp_serverAuth") in self._oids

	def __repr__(self):
		return "%s<%s>" % (self.__class__.__name__, ", ".join(OIDDB.X509ExtendedKeyUsage.get(oid, str(oid)) for oid in sorted(self._oids)))


@X509ExtensionRegistry.install_handler_class
class X509SubjectAlternativeNameExtension(X509Extension):
	_HANDLER_OID = OIDDB.X509Extensions.inverse("SubjectAlternativeName")
	_ASN1_MODEL = rfc5280.SubjectAltName

	def _decode_hook(self):
		self._known_names = [ ]
		if self.asn1 is None:
			return
		for altname in self.asn1:
			self._known_names.append(ASN1GeneralNameWrapper.from_asn1(altname))

	@property
	def name_count(self):
		return len(self._known_names)

	def get_all(self, name_type):
		return [ asn1name for asn1name in self._known_names if asn1name.name == name_type ]

	def __iter__(self):
		return iter(self._known_names)

	def __repr__(self):
		return "%s<%s>" % (self.__class__.__name__, ", ".join(str(asn1name) for asn1name in self._known_names))


@X509ExtensionRegistry.install_handler_class
class X509IssuerAlternativeNameExtension(X509SubjectAlternativeNameExtension):
	_HANDLER_OID = OIDDB.X509Extensions.inverse("IssuerAlternativeName")
	_ASN1_MODEL = rfc5280.IssuerAltName


@X509ExtensionRegistry.install_handler_class
class X509KeyUsageExtension(X509Extension):
	_HANDLER_OID = OIDDB.X509Extensions.inverse("KeyUsage")
	_ASN1_MODEL = rfc5280.KeyUsage

	@property
	def flags(self):
		"""Known flags (defined in the bitset) only."""
		return self._flags

	@property
	def all_flags(self):
		"""All set flags (also those not defined in bitset) only."""
		return self._all_flags

	@property
	def has_trailing_zero(self):
		return ASN1Tools.bitstring_has_trailing_zeros(self.asn1) if (self.asn1 is not None) else None

	@property
	def highest_set_bit_value(self):
		return ASN1Tools.bitstring_highbit(self.asn1) if (self.asn1 is not None) else None

	@property
	def highest_permissible_bit_value(self):
		return max(self._ASN1_MODEL.namedValues.values())

	@property
	def all_bits_zero(self):
		return ASN1Tools.bitstring_is_empty(self.asn1) if (self.asn1 is not None) else None

	@property
	def unknown_flags_set(self):
		return (self.highest_set_bit_value or 0) > len(self._ASN1_MODEL.namedValues)

	def _decode_hook(self):
		if self.asn1 is None:
			self._flags = None
			self._all_flags = None
		else:
			self._flags = set()
			self._all_flags = set()
			known_bits = { bit : name for (name, bit) in self._ASN1_MODEL.namedValues.items() }
			for (bit, value) in enumerate(self.asn1):
				if value == 1:
					if bit in known_bits:
						flag_name =  known_bits[bit]
						self._flags.add(flag_name)
						self._all_flags.add(flag_name)
					else:
						flag_name = "bit-%d" % (bit)
						self._all_flags.add(flag_name)

	def __repr__(self):
		if self.flags is not None:
			return "%s<%s>" % (self.__class__.__name__, ", ".join(sorted(self._flags)))
		else:
			return "%s<flags unparsable>" % (self.__class__.__name__)


@X509ExtensionRegistry.install_handler_class
class X509NetscapeCertificateTypeExtension(X509Extension):
	_HANDLER_OID = OIDDB.X509Extensions.inverse("NetscapeCertificateType")
	_ASN1_MODEL = ASN1Models.NetscapeCertificateType

	@property
	def ssl_server(self):
		return "server" in self.flags

	@property
	def ssl_client(self):
		return "client" in self.flags

	@property
	def flags(self):
		return self._flags

	def _decode_hook(self):
		self._flags = set()
		if self.asn1 is None:
			return
		for (name, bit) in self._ASN1_MODEL.namedValues.items():
			if (len(self.asn1) > bit) and self.asn1[bit]:
				self._flags.add(name)

	def __repr__(self):
		return "%s<%s>" % (self.__class__.__name__, ", ".join(sorted(self._flags)))


@X509ExtensionRegistry.install_handler_class
class X509AuthorityInformationAccessExtension(X509Extension):
	_HANDLER_OID = OIDDB.X509Extensions.inverse("id-pe-authorityInfoAccess")
	_ASN1_MODEL = rfc5280.AuthorityInfoAccessSyntax

	@property
	def method_count(self):
		return len(self._methods)

	def _decode_hook(self):
		self._methods = [ ]
		if self.asn1 is not None:
			for item in self.asn1:
				oid = OID.from_asn1(item["accessMethod"])
				location = item["accessLocation"]
				self._methods.append((oid, location))

	def __repr__(self):
		return "%s<%s>" % (self.__class__.__name__, ", ".join(str(oid) for (oid, location) in self._methods))


@X509ExtensionRegistry.install_handler_class
class X509CertificatePoliciesExtension(X509Extension):
	_HANDLER_OID = OIDDB.X509Extensions.inverse("CertificatePolicies")
	_ASN1_MODEL = rfc5280.CertificatePolicies

	_CertificatePolicy = collections.namedtuple("CertificatePolicy", [ "oid", "qualifiers" ])
	_CertificatePolicyQualifier = collections.namedtuple("CertificatePolicyQualifier", [ "oid", "qualifier_data", "decoded_qualifier" ])
	_DecodedQualifier = collections.namedtuple("DecodedQualifier", [ "asn1", "trailing_data", "constraint_violation" ])

	@property
	def policies(self):
		return iter(self._policies)

	@property
	def policy_count(self):
		return len(self._policies)

	@property
	def policy_oids(self):
		return [ policy.oid for policy in self.policies ]

	@classmethod
	def decode_qualifier(cls, oid, qualifier_data):
		decoded_qualifier = None
		if oid == OIDDB.X509ExtensionCertificatePolicyQualifierOIDs.inverse("id-qt-cps"):
			decoded_qualifier = ASN1Tools.safe_decode(qualifier_data, asn1_spec = (rfc5280.CPSuri(), ASN1Models.RelaxedCPSuri()))
		elif oid == OIDDB.X509ExtensionCertificatePolicyQualifierOIDs.inverse("id-qt-unotice"):
			decoded_qualifier = ASN1Tools.safe_decode(qualifier_data, asn1_spec = (rfc5280.UserNotice(), ASN1Models.RelaxedUserNotice()))
		return decoded_qualifier

	def get_policy(self, policy_oid):
		for policy in self._policies:
			if policy.oid == policy_oid:
				return policy
		return None

	def _decode_hook(self):
		self._policies = [ ]
		if self.asn1 is None:
			return
		for item in self.asn1:
			policy_oid = OID.from_asn1(item["policyIdentifier"])
			qualifiers = [ ]
			for qualifier in item["policyQualifiers"]:
				qualifier_oid = OID.from_asn1(qualifier["policyQualifierId"])
				qualifier_data = bytes(qualifier["qualifier"])
				qualifier = self._CertificatePolicyQualifier(oid = qualifier_oid, qualifier_data = qualifier_data, decoded_qualifier = self.decode_qualifier(qualifier_oid, qualifier_data))
				qualifiers.append(qualifier)
			policy = self._CertificatePolicy(oid = policy_oid, qualifiers = tuple(qualifiers))
			self._policies.append(policy)

	def __repr__(self):
		return "%s<%s>" % (self.__class__.__name__, ", ".join(str(oid) for (oid, qualifiers) in self._policies))


@X509ExtensionRegistry.install_handler_class
class X509CRLDistributionPointsExtension(X509Extension):
	_HANDLER_OID = OIDDB.X509Extensions.inverse("CRLDistributionPoints")
	_ASN1_MODEL = rfc5280.CRLDistributionPoints
	_KNOWN_REASON_BITS = {
		0:		"unused",
		1:		"keyCompromise",
		2:		"cACompromise",
		3:		"affiliationChanged",
		4:		"superseded",
		5:		"cessationOfOperation",
		6:		"certificateHold",
		7:		"privilegeWithdrawn",
		8:		"aACompromise",
	}
	_ALL_USED_REASONS = set(name for name in _KNOWN_REASON_BITS.values() if (name != "unused"))
	_DistributionPoint = collections.namedtuple("DistributionPoint", [ "point_name", "point_name_rdn_malformed", "reasons", "reasons_trailing_zero", "crl_issuer" ])

	@classmethod
	def all_used_reasons(cls):
		return iter(cls._ALL_USED_REASONS)

	@property
	def points(self):
		return iter(self._distribution_points)

	def _decode_hook(self):
		if self.asn1 is None:
			self._distribution_points = None
			return

		self._distribution_points = [ ]
		for asn1_point in self.asn1:
			point_name_rdn_malformed = False
			if asn1_point["distributionPoint"].hasValue():
				point_name_asn1 = asn1_point["distributionPoint"].getComponent()
				if asn1_point["distributionPoint"]["fullName"].hasValue():
					# GeneralNames
					point_name = ASN1GeneralNamesWrapper.from_asn1(point_name_asn1)
				else:
					# RelativeDistinguishedName
					try:
						point_name = RelativeDistinguishedName.from_asn1(point_name_asn1)
					except InvalidInputException:
						point_name = None
						point_name_rdn_malformed = True
			else:
				point_name = None

			if asn1_point["reasons"].hasValue():
				reasons = set()
				for (bitno, value) in enumerate(asn1_point["reasons"]):
					if value == 1:
						value = self._KNOWN_REASON_BITS.get(bitno, bitno)
						reasons.add(value)
				reasons_trailing_zero = ASN1Tools.bitstring_has_trailing_zeros(asn1_point["reasons"])
			else:
				reasons = None
				reasons_trailing_zero = False

			if asn1_point["cRLIssuer"].hasValue():
				crl_issuer = ASN1GeneralNamesWrapper.from_asn1(asn1_point["cRLIssuer"])
			else:
				crl_issuer = None

			cdp = self._DistributionPoint(point_name = point_name, point_name_rdn_malformed = point_name_rdn_malformed, reasons = reasons, reasons_trailing_zero = reasons_trailing_zero, crl_issuer = crl_issuer)
			self._distribution_points.append(cdp)

	def __repr__(self):
		if self.asn1 is not None:
			return "%s<%s>" % (self.__class__.__name__, ", ".join(str(point) for point in self.points))
		else:
			return "%s<malformed>" % (self.__class__.__name__)


@X509ExtensionRegistry.install_handler_class
class X509FreshestCRLExtension(X509CRLDistributionPointsExtension):
	_HANDLER_OID = OIDDB.X509Extensions.inverse("FreshestCRL")


@X509ExtensionRegistry.install_handler_class
class X509CertificateTransparencySCTsExtension(X509Extension):
	_HANDLER_OID = OIDDB.X509Extensions.inverse("CertificateTransparency")
	_ASN1_MODEL = pyasn1.type.univ.OctetString

	@property
	def payload(self):
		return self._payload

	@property
	def malformed_payload(self):
		return self.payload is None

	def _decode_hook(self):
		self._payload = None
		if self.asn1 is None:
			return
		raw_data = bytes(self.asn1)
		try:
			self._payload = SignedCertificateTimestampList.unpack(DataBuffer(raw_data))
		except DeserializationException:
			pass

	def __repr__(self):
		return "%s<%s>" % (self.__class__.__name__, str(self.payload))


@X509ExtensionRegistry.install_handler_class
class X509CertificateTransparencyPrecertificatePoisonExtension(X509Extension):
	_HANDLER_OID = OIDDB.X509Extensions.inverse("CertificateTransparencyPrecertificatePoison")
	_ASN1_MODEL = pyasn1.type.univ.Null

	def __repr__(self):
		return "%s<%s>" % (self.__class__.__name__, "malformed" if (self.asn1 is None) else "OK")


@X509ExtensionRegistry.install_handler_class
class X509NameConstraintsExtension(X509Extension):
	_HANDLER_OID = OIDDB.X509Extensions.inverse("NameConstraints")
	_ASN1_MODEL = rfc5280.NameConstraints
	_NameConstraintsSubtree = collections.namedtuple("NameConstraintSubtree", [ "minimum", "maximum", "base" ])

	@property
	def permitted_subtrees(self):
		return self._permitted_subtrees

	@property
	def excluded_subtrees(self):
		return self._excluded_subtrees

	def _parse_subtree(self, subtree):
		minimum = int(subtree["minimum"])
		maximum = int(subtree["maximum"]) if (subtree["maximum"].isValue) else None
		base = ASN1GeneralNameWrapper.from_asn1(subtree["base"])
		return self._NameConstraintsSubtree(minimum = minimum, maximum = maximum, base = base)

	def _parse_subtrees(self, subtrees):
		parsed_subtrees = [ ]
		for subtree in subtrees:
			parsed_subtree = self._parse_subtree(subtree)
			parsed_subtrees.append(parsed_subtree)
		return parsed_subtrees


	def _decode_hook(self):
		if self.asn1 is None:
			self._permitted_subtrees = None
			self._excluded_subtrees = None
			return
		self._permitted_subtrees = self._parse_subtrees(self.asn1["permittedSubtrees"])
		self._excluded_subtrees = self._parse_subtrees(self.asn1["excludedSubtrees"])

	def __repr__(self):
		return "%s<permitted = %s, excluded = %s>" % (self.__class__.__name__, self.permitted_subtrees, self.excluded_subtrees)


@X509ExtensionRegistry.install_handler_class
class X509SubjectDirectoryAttributesExtension(X509Extension):
	_HANDLER_OID = OIDDB.X509Extensions.inverse("SubjectDirectoryAttributes")
	_ASN1_MODEL = rfc5280.SubjectDirectoryAttributes
	_Attribute = collections.namedtuple("Attribute", [ "attribute_type", "values" ])

	@property
	def attributes(self):
		return self._attributes

	def _decode_hook(self):
		self._attributes = [ ]
		if self.asn1 is not None:
			for attribute in self.asn1:
				self._attributes.append(self._Attribute(attribute_type = OID.from_asn1(attribute["type"]), values = [ ASN1Tools.safe_decode(value) for value in attribute["values"] ]))

	def __repr__(self):
		return "%s<%s>" % (self.__class__.__name__, self.attributes)


@X509ExtensionRegistry.install_handler_class
class X509SubjectInformationAccessExtension(X509Extension):
	_HANDLER_OID = OIDDB.X509Extensions.inverse("SubjectInformationAccess")
	_ASN1_MODEL = rfc5280.SubjectInfoAccessSyntax
	_AccessDescription = collections.namedtuple("AccessDescription", [ "method", "location" ])

	@property
	def description(self):
		return self._description

	def _decode_hook(self):
		self._description = [ ]
		if self.asn1 is not None:
			for access_description in self.asn1:
				self._description.append(self._AccessDescription(method = OID.from_asn1(access_description["accessMethod"]), location = ASN1GeneralNameWrapper.from_asn1(access_description["accessLocation"])))

	def __repr__(self):
		return "%s<%s>" % (self.__class__.__name__, self.description)


@X509ExtensionRegistry.install_handler_class
class X509InhibitAnyPolicyExtension(X509Extension):
	_HANDLER_OID = OIDDB.X509Extensions.inverse("X509Version3CertificateExtensionInhibitAnyPolicy")
	_ASN1_MODEL = rfc5280.InhibitAnyPolicy

	@property
	def skipcerts(self):
		return None if (self.asn1 is None) else (int(self.asn1))

	def __repr__(self):
		return "%s<%s>" % (self.__class__.__name__, self.skipcerts)


@X509ExtensionRegistry.install_handler_class
class X509PolicyConstraintsExtension(X509Extension):
	_HANDLER_OID = OIDDB.X509Extensions.inverse("PolicyConstraints")
	_ASN1_MODEL = rfc5280.PolicyConstraints

	@property
	def require_explicit_policy(self):
		return self._require_explicit_policy

	@property
	def inhibit_policy_mapping(self):
		return self._inhibit_policy_mapping

	def _decode_hook(self):
		self._require_explicit_policy = None
		self._inhibit_policy_mapping = None
		if self.asn1 is not None:
			self._require_explicit_policy = int(self.asn1["requireExplicitPolicy"]) if self.asn1["requireExplicitPolicy"].hasValue() else None
			self._inhibit_policy_mapping = int(self.asn1["inhibitPolicyMapping"]) if self.asn1["inhibitPolicyMapping"].hasValue() else None

	def __repr__(self):
		return "%s<require explicit = %s; inhibit policy mapping = %s>" % (self.__class__.__name__, self.require_explicit_policy, self.inhibit_policy_mapping)


@X509ExtensionRegistry.install_handler_class
class X509PolicyMappingsExtension(X509Extension):
	_HANDLER_OID = OIDDB.X509Extensions.inverse("PolicyMappings")
	_ASN1_MODEL = rfc5280.PolicyMappings
	_PolicyMapping = collections.namedtuple("PolicyMapping", [ "issuer_policy", "subject_policy" ])

	@property
	def mappings(self):
		return self._mappings

	def _decode_hook(self):
		self._mappings = [ ]
		if self.asn1 is not None:
			for mapping in self.asn1:
				self._mappings.append(self._PolicyMapping(issuer_policy = OID.from_asn1(mapping["issuerDomainPolicy"]), subject_policy = OID.from_asn1(mapping["subjectDomainPolicy"])))

	def __repr__(self):
		return "%s<%s>" % (self.__class__.__name__, self.mappings)
