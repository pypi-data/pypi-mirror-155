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

import pyasn1.type.univ
from x509sak.BijectiveDict import BijectiveDict
from x509sak.Exceptions import InvalidInputException

class OID():
	def __init__(self, oid_value):
		self._oid_value = tuple(oid_value)

	def __eq__(self, other):
		return (type(self) == type(other)) and (self._oid_value == other._oid_value)

	def __neq__(self, other):
		return not (self == other)

	def __lt__(self, other):
		return (type(self) == type(other)) and (self._oid_value < other._oid_value)

	def __hash__(self):
		return hash(self._oid_value)

	def to_asn1(self):
		return pyasn1.type.univ.ObjectIdentifier(self._oid_value)

	@classmethod
	def from_str(cls, oid_string):
		assert(isinstance(oid_string, str))
		split_string = oid_string.split(".")
		try:
			int_string = [ int(value) for value in split_string ]
		except ValueError:
			raise InvalidInputException("Cannot parse \"%s\" as a string OID." % (oid_string))
		return cls(int_string)

	@classmethod
	def from_asn1(cls, oid_asn1):
		if not isinstance(oid_asn1, pyasn1.type.univ.ObjectIdentifier):
			raise InvalidInputException("Tried to construct an OID from ASN.1 of type %s." % (oid_asn1.__class__.__name__))
		return cls.from_str(str(oid_asn1))

	def __repr__(self):
		return ".".join(str(value) for value in self._oid_value)

class OIDDB():
	"""KeySpecification algorithm OIDs."""
	KeySpecificationAlgorithms = BijectiveDict({
		OID.from_str("1.2.840.113549.1.1.1"):	"rsaEncryption",
		OID.from_str("1.2.840.10045.2.1"):		"ecPublicKey",
		OID.from_str("1.2.840.10040.4.1"):		"id-dsa",
		OID.from_str("1.3.101.110"):			"id-X25519",
		OID.from_str("1.3.101.111"):			"id-X448",
		OID.from_str("1.3.101.112"):			"id-Ed25519",
		OID.from_str("1.3.101.113"):			"id-Ed448",
	})

	"""Signature algorithm OIDs."""
	SignatureAlgorithms = BijectiveDict({
		OID.from_str("1.2.840.113549.1.1.2"):	"md2WithRsaEncryption",
		OID.from_str("1.2.840.113549.1.1.3"):	"md4WithRsaEncryption",
		OID.from_str("1.2.840.113549.1.1.4"):	"md5WithRsaEncryption",
		OID.from_str("1.2.840.113549.1.1.5"):	"sha1WithRsaEncryption",
		OID.from_str("1.2.840.113549.1.1.10"):	"RSASSA-PSS",
		OID.from_str("1.2.840.113549.1.1.11"):	"sha256WithRsaEncryption",
		OID.from_str("1.2.840.113549.1.1.12"):	"sha384WithRsaEncryption",
		OID.from_str("1.2.840.113549.1.1.13"):	"sha512WithRsaEncryption",

		OID.from_str("1.2.840.10040.4.3"):		"dsa-with-sha1",
		OID.from_str("2.16.840.1.101.3.4.3.1"):	"dsa-with-sha224",
		OID.from_str("2.16.840.1.101.3.4.3.2"):	"dsa-with-sha256",
		OID.from_str("2.16.840.1.101.3.4.3.3"):	"dsa-with-sha384",
		OID.from_str("2.16.840.1.101.3.4.3.4"):	"dsa-with-sha512",

		OID.from_str("1.2.840.10045.4.1"):		"ecdsa-with-SHA1",
		OID.from_str("1.2.840.10045.4.3.1"):	"ecdsa-with-SHA224",
		OID.from_str("1.2.840.10045.4.3.2"):	"ecdsa-with-SHA256",
		OID.from_str("1.2.840.10045.4.3.3"):	"ecdsa-with-SHA384",
		OID.from_str("1.2.840.10045.4.3.4"):	"ecdsa-with-SHA512",

		OID.from_str("1.3.14.3.2.2"):			"md4WithRsaEncryption-alt1",
		OID.from_str("1.3.14.3.2.3"):			"md5WithRsaEncryption-alt1",
		OID.from_str("1.3.14.3.2.4"):			"md5WithRsaEncryption-alt2",
		OID.from_str("1.3.14.3.2.13"):			"dsa-with-sha",
		OID.from_str("1.3.14.3.2.15"):			"shaWithRsaEncryption",
		OID.from_str("1.3.14.3.2.27"):			"sha1DSA-alt1",
		OID.from_str("1.3.14.3.2.29"):			"sha1WithRsaEncryption-alt1",

		OID.from_str("1.3.14.7.2.3.1"):			"md2WithRsaEncryption-alt1",
	})

	"""Relative Distinguished Name type component OIDs."""
	RDNTypes = BijectiveDict(value_predicate = lambda name: name.lower(), values = {
		OID.from_str("2.5.4.0"):					"objectClass",
		OID.from_str("2.5.4.1"):					"aliasedEntryName",
		OID.from_str("2.5.4.2"):					"knowledgeinformation",
		OID.from_str("2.5.4.3"):					"CN",				# common name
		OID.from_str("2.5.4.4"):					"SN",				# surname
		OID.from_str("2.5.4.5"):					"serialNumber",
		OID.from_str("2.5.4.6"):					"C",				# country
		OID.from_str("2.5.4.7"):					"L",				# locality
		OID.from_str("2.5.4.8"):					"ST",				# stateOrProvinceName
		OID.from_str("2.5.4.9"):					"street",			# streetAddress
		OID.from_str("2.5.4.10"):					"O",				# organizationName
		OID.from_str("2.5.4.11"):					"OU",				# organizationalUnitName
		OID.from_str("2.5.4.12"):					"title",
		OID.from_str("2.5.4.13"):					"description",
		OID.from_str("2.5.4.14"):					"searchGuide",
		OID.from_str("2.5.4.15"):					"businessCategory",
		OID.from_str("2.5.4.16"):					"postalAddress",
		OID.from_str("2.5.4.17"):					"postalCode",
		OID.from_str("2.5.4.18"):					"postOfficeBox",
		OID.from_str("2.5.4.19"):					"physicalDeliveryOfficeName",
		OID.from_str("2.5.4.20"):					"telephoneNumber",
		OID.from_str("2.5.4.21"):					"telexNumber",
		OID.from_str("2.5.4.22"):					"teletexTerminalIdentifier",
		OID.from_str("2.5.4.23"):					"facsimileTelephoneNumber",
		OID.from_str("2.5.4.24"):					"x121Address",
		OID.from_str("2.5.4.25"):					"internationaliSDNNumber",
		OID.from_str("2.5.4.26"):					"registeredAddress",
		OID.from_str("2.5.4.27"):					"destinationIndicator",
		OID.from_str("2.5.4.28"):					"preferredDeliveryMethod",
		OID.from_str("2.5.4.29"):					"presentationAddress",
		OID.from_str("2.5.4.30"):					"supportedApplicationContext",
		OID.from_str("2.5.4.31"):					"member",
		OID.from_str("2.5.4.32"):					"owner",
		OID.from_str("2.5.4.33"):					"roleOccupant",
		OID.from_str("2.5.4.34"):					"seeAlso",
		OID.from_str("2.5.4.35"):					"userPassword",
		OID.from_str("2.5.4.36"):					"userCertificate",
		OID.from_str("2.5.4.37"):					"cACertificate",
		OID.from_str("2.5.4.38"):					"authorityRevocationList",
		OID.from_str("2.5.4.39"):					"certificateRevocationList",
		OID.from_str("2.5.4.40"):					"crossCertificatePair",
		OID.from_str("2.5.4.41"):					"name",
		OID.from_str("2.5.4.42"):					"GN",				# givenName
		OID.from_str("2.5.4.43"):					"initials",
		OID.from_str("1.2.840.113549.1.9.1"):		"emailAddress",
		OID.from_str("0.9.2342.19200300.100.1.1"):	"UID",
		OID.from_str("0.9.2342.19200300.100.1.25"):	"DC",
	})

	"""X.509 Extension OIDs."""
	X509Extensions = BijectiveDict({
		OID.from_str("2.5.29.1"):					"oldAuthorityKeyIdentifier",
		OID.from_str("2.5.29.2"):					"oldPrimaryKeyAttributes",
		OID.from_str("2.5.29.3"):					"oldCertificatePolicies",
		OID.from_str("2.5.29.4"):					"PrimaryKeyUsageRestriction",
		OID.from_str("2.5.29.9"):					"SubjectDirectoryAttributes",
		OID.from_str("2.5.29.14"):					"SubjectKeyIdentifier",
		OID.from_str("2.5.29.15"):					"KeyUsage",
		OID.from_str("2.5.29.16"):					"PrivateKeyUsagePeriod",
		OID.from_str("2.5.29.17"):					"SubjectAlternativeName",
		OID.from_str("2.5.29.18"):					"IssuerAlternativeName",
		OID.from_str("2.5.29.19"):					"BasicConstraints",
		OID.from_str("2.5.29.20"):					"CRLNumber",
		OID.from_str("2.5.29.21"):					"ReasonCode",
		OID.from_str("2.5.29.23"):					"HoldInstructionCode",
		OID.from_str("2.5.29.24"):					"InvalidityDate",
		OID.from_str("2.5.29.27"):					"DeltaCRLIndicator",
		OID.from_str("2.5.29.28"):					"IssuingDistributionPoint",
		OID.from_str("2.5.29.29"):					"CertificateIssuer",
		OID.from_str("2.5.29.30"):					"NameConstraints",
		OID.from_str("2.5.29.31"):					"CRLDistributionPoints",
		OID.from_str("2.5.29.32"):					"CertificatePolicies",
		OID.from_str("2.5.29.33"):					"PolicyMappings",
		OID.from_str("2.5.29.35"):					"AuthorityKeyIdentifier",
		OID.from_str("2.5.29.36"):					"PolicyConstraints",
		OID.from_str("2.5.29.37"):					"ExtendedKeyUsage",
		OID.from_str("2.5.29.46"):					"FreshestCRL",
		OID.from_str("2.5.29.54"):					"X509Version3CertificateExtensionInhibitAnyPolicy",

		OID.from_str("1.3.6.1.5.5.7.1.11"):			"SubjectInformationAccess",

		OID.from_str("1.2.840.113533.7.65.0"):		"EntrustVersionExtension",

		OID.from_str("1.2.840.113549.1.9.15"):		"SMIMECapabilities",

		OID.from_str("1.3.6.1.4.1.311.20.2"):		"CertificateTemplateNameDomainController",
		OID.from_str("1.3.6.1.4.1.311.21.1"):		"CertSRVCAVersion",

		OID.from_str("1.3.6.1.4.1.11129.2.4.2"):	"CertificateTransparency",
		OID.from_str("1.3.6.1.4.1.11129.2.4.3"):	"CertificateTransparencyPrecertificatePoison",

		OID.from_str("2.23.42.7.0"):				"hashedRootKey",

		OID.from_str("1.3.6.1.5.5.7.1.1"):			"id-pe-authorityInfoAccess",
		OID.from_str("1.3.6.1.5.5.7.1.2"):			"id-pe-biometricInfo",
		OID.from_str("1.3.6.1.5.5.7.1.3"):			"id-pe-qcStatements",
		OID.from_str("1.3.6.1.5.5.7.1.12"):			"id-pe-logotype",
		OID.from_str("1.3.6.1.5.5.7.1.23"):			"NSACertificateExtension",
		OID.from_str("1.3.6.1.5.5.7.1.24"):			"TLSFeature",
		OID.from_str("1.3.6.1.5.5.7.48.1.5"):		"id-pkix-ocsp-nocheck",

		# Microsoft-specific extensions
		OID.from_str("1.3.6.1.4.1.311.21.7"):		"szOID_CERTIFICATE_TEMPLATE",
		OID.from_str("1.3.6.1.4.1.311.21.10"):		"szOID_APPLICATION_CERT_POLICIES",

		# Netscape-specific extensions
		OID.from_str("2.16.840.1.113730.1.1"):		"NetscapeCertificateType",
		OID.from_str("2.16.840.1.113730.1.2"):		"NetscapeBaseUrl",
		OID.from_str("2.16.840.1.113730.1.3"):		"NetscapeRevocationUrl",
		OID.from_str("2.16.840.1.113730.1.4"):		"NetscapeCARevocationUrl",
		OID.from_str("2.16.840.1.113730.1.5"):		"NetscapeCACRLUrl",
		OID.from_str("2.16.840.1.113730.1.6"):		"NetscapeCACertUrl",
		OID.from_str("2.16.840.1.113730.1.7"):		"NetscapeRenewalUrl",
		OID.from_str("2.16.840.1.113730.1.8"):		"NetscapeCAPolicyUrl",
		OID.from_str("2.16.840.1.113730.1.9"):		"NetscapeHomepageUrl",
		OID.from_str("2.16.840.1.113730.1.10"):		"NetscapeEntityLogo",
		OID.from_str("2.16.840.1.113730.1.11"):		"NetscapeUserPicture",
		OID.from_str("2.16.840.1.113730.1.12"):		"NetscapeSSLServerName",
		OID.from_str("2.16.840.1.113730.1.13"):		"NetscapeComment",
		OID.from_str("2.16.840.1.113730.1.14"):		"NetscapeLostPasswordUrl",
		OID.from_str("2.16.840.1.113730.1.15"):		"NetscapeCertRenewalTime",
		OID.from_str("2.16.840.1.113730.1.16"):		"NetscapeAuthorityInformationAccess",
		OID.from_str("2.16.840.1.113730.1.17"):		"NetscapeCertScopeOfUse",

		OID.from_str("2.16.840.1.113719.1.9.4.1"):	"NovellSecurityAttributes",
	})

	"""X.509 Certificate Policy OIDs."""
	X509ExtensionCertificatePolicy = BijectiveDict({
		OID.from_str("2.5.29.32.0"):				"anyPolicy",
	})

	"""X.509 Certificate Policy Qualifier OIDs."""
	X509ExtensionCertificatePolicyQualifierOIDs = BijectiveDict({
		OID.from_str("1.3.6.1.5.5.7.2.1"):			"id-qt-cps",
		OID.from_str("1.3.6.1.5.5.7.2.2"):			"id-qt-unotice",
	})

	"""Hash functions."""
	HashFunctions = BijectiveDict({
		OID.from_str("1.3.14.3.2.26"):				"sha1",
		OID.from_str("2.16.840.1.101.3.4.2.1"):		"sha256",
		OID.from_str("2.16.840.1.101.3.4.2.2"):		"sha384",
		OID.from_str("2.16.840.1.101.3.4.2.3"):		"sha512",
		OID.from_str("2.16.840.1.101.3.4.2.4"):		"sha224",
		OID.from_str("2.16.840.1.101.3.4.2.5"):		"sha512-224",
		OID.from_str("2.16.840.1.101.3.4.2.6"):		"sha512-256",
		OID.from_str("2.16.840.1.101.3.4.2.7"):		"sha3-224",
		OID.from_str("2.16.840.1.101.3.4.2.8"):		"sha3-256",
		OID.from_str("2.16.840.1.101.3.4.2.9"):		"sha3-384",
		OID.from_str("2.16.840.1.101.3.4.2.10"):	"sha3-512",
		OID.from_str("2.16.840.1.101.3.4.2.11"):	"shake128",
		OID.from_str("2.16.840.1.101.3.4.2.12"):	"shake256",
	})

	"""X.509 Extension Extended Key Usage."""
	X509ExtendedKeyUsage = BijectiveDict({
		OID.from_str("2.5.29.37.0"):				"anyExtendedKeyUsage",
		OID.from_str("1.3.6.1.5.5.7.3.1"):			"id_kp_serverAuth",
		OID.from_str("1.3.6.1.5.5.7.3.2"):			"id_kp_clientAuth",
		OID.from_str("1.3.6.1.5.5.7.3.3"):			"id_kp_codeSigning",
		OID.from_str("1.3.6.1.5.5.7.3.4"):			"id_kp_emailProtection",
		OID.from_str("1.3.6.1.5.5.7.3.5"):			"id_kp-ipsecEndSystem",
		OID.from_str("1.3.6.1.5.5.7.3.6"):			"id_kp-ipsecTunnel",
		OID.from_str("1.3.6.1.5.5.7.3.7"):			"id_kp-ipsecUser",
		OID.from_str("1.3.6.1.5.5.7.3.8"):			"id_kp_timeStamping",
		OID.from_str("1.3.6.1.5.5.7.3.9"):			"OCSPSigning",
		OID.from_str("1.3.6.1.5.5.7.3.10"):			"dvcs",
		OID.from_str("1.3.6.1.5.5.7.3.11"):			"id-kp-sbgpCertAAServerAuth",
		OID.from_str("1.3.6.1.5.5.7.3.12"):			"id-kp-scvp-responder",
		OID.from_str("1.3.6.1.5.5.7.3.13"):			"id-kp-eapOverPPP",
		OID.from_str("1.3.6.1.5.5.7.3.14"):			"id-kp-eapOverLAN",
		OID.from_str("1.3.6.1.5.5.7.3.15"):			"id-kp-scvpServer",
		OID.from_str("1.3.6.1.5.5.7.3.16"):			"id-kp-scvpClient",
		OID.from_str("1.3.6.1.5.5.7.3.17"):			"id-kp-ipsecIKE",
		OID.from_str("1.3.6.1.5.5.7.3.18"):			"id-kp-capwapAC",
		OID.from_str("1.3.6.1.5.5.7.3.19"):			"id-kp-capwapWTP",
		OID.from_str("1.3.6.1.5.5.7.3.20"):			"id-kp-sipDomain",
		OID.from_str("1.3.6.1.5.5.7.3.21"):			"secureShellClient",
		OID.from_str("1.3.6.1.5.5.7.3.22"):			"secureShellServer",
		OID.from_str("1.3.6.1.5.5.7.3.27"):			"id-kp-cmcCA",
		OID.from_str("1.3.6.1.5.5.7.3.28"):			"id-kp-cmcRA",
		OID.from_str("1.3.6.1.5.5.7.3.29"):			"id-kp-cmcArchive",
		OID.from_str("1.3.6.1.5.5.7.3.30"):			"id-kp-bgpsec-router",
		OID.from_str("1.2.203.7064.1.1.369791.1"):	"CSN369791-TLS-CLIENT",
		OID.from_str("1.2.203.7064.1.1.369791.2"):	"CSN369791-TLS-SERVER",
	})

	"""ECC field type."""
	ECFieldType = BijectiveDict({
		OID.from_str("1.2.840.10045.1.1"):			"prime-field",
		OID.from_str("1.2.840.10045.1.2"):			"characteristic-two-field",
	})

	"""ECC twofield basisType."""
	ECTwoFieldBasistype = BijectiveDict({
		OID.from_str("1.2.840.10045.1.2.3.1"):		"gnBasis",		# Gaussian basis
		OID.from_str("1.2.840.10045.1.2.3.2"):		"tpBasis",		# Trinomial basis
		OID.from_str("1.2.840.10045.1.2.3.3"):		"ppBasis",		# Pentanomial basis
	})

	"""RSAPSS Mask Generation Functions."""
	RSAPSSMaskGenerationAlgorithm = BijectiveDict({
		OID.from_str("1.2.840.113549.1.1.8"):		"mgf1",
	})

	"""Subject Information Access Method OIDs."""
	SubjectInformationAccessMethod = BijectiveDict({
		OID.from_str("1.3.6.1.5.5.7.48.1"):		"ocsp",
		OID.from_str("1.3.6.1.5.5.7.48.2"):		"caIssuers",
		OID.from_str("1.3.6.1.5.5.7.48.3"):		"timestamping",
		OID.from_str("1.3.6.1.5.5.7.48.4"):		"DVCS",							# Data Validation and Certification Server
		OID.from_str("1.3.6.1.5.5.7.48.5"):		"caRepository",
		OID.from_str("1.3.6.1.5.5.7.48.6"):		"httpCerts",
		OID.from_str("1.3.6.1.5.5.7.48.7"):		"httpCRLs",
		OID.from_str("1.3.6.1.5.5.7.48.8"):		"XKMS",							# XML Key Management Specification
		OID.from_str("1.3.6.1.5.5.7.48.9"):		"signedObjectRepository",
		OID.from_str("1.3.6.1.5.5.7.48.10"):	"rpkiManifest",					# Resource Public Key Infrastructure
		OID.from_str("1.3.6.1.5.5.7.48.11"):	"signedObject",
		OID.from_str("1.3.6.1.5.5.7.48.12"):	"CMC",							# Certificate Management over CMS
		OID.from_str("1.3.6.1.5.5.7.48.13"):	"rpkiNotify",					# Resource Public Key Infrastructure
		OID.from_str("1.3.6.1.5.5.7.48.14"):	"stirTNList",					# Secure Telephone Identity Revisited Telephony Numbers
	})
