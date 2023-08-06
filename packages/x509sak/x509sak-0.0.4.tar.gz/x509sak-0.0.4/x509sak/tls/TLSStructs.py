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

from x509sak.tls.Enums import TLSVersionRecordLayer, TLSVersionHandshake, ContentType, HandshakeType, CipherSuite, CompressionMethod, ExtensionType, ServerNameType, ECPointFormats, SupportedGroups, TLSAlertLevel, TLSAlertDescription
from x509sak.tls.Structure import Structure, VariableType, instantiate_member as IM

RecordLayerPkt = Structure(name = "RecordLayerPkt", members = [
	IM("content_type",			"uint8", enum_class = ContentType),
	IM("record_layer_version",	"uint16", enum_class = TLSVersionRecordLayer),
	IM("payload",				"opaque16"),
])

TLSExtension = Structure(name = "TLSExtension", members = [
	IM("extension_id",					"uint16", enum_class = ExtensionType),
	IM("content",						"opaque16"),
])

TLSExtensionFlag = Structure(name = "TLSExtensionFlag", members = [
	IM("extension_id",					"uint16", enum_class = ExtensionType),
	IM("content",						"opaque16", fixed_value = bytes()),
])

TLSExtensionServerNameIndication = Structure(name = "TLSExtensionServerNameIndication", members = [
	IM("extension_id",					"uint16", enum_class = ExtensionType, fixed_value = ExtensionType.server_name),
	IM("content",						"opaque16", inner = Structure([
		IM("server_name_list",				"opaque16", contains_array = True, inner = Structure([
			IM("server_name_type",				"uint8", enum_class = ServerNameType, fixed_value = ServerNameType.Hostname),
			IM("server_name",					"opaque16", string_encoding = "ascii"),
		])),
	])),
])
TLSExtensionServerNameIndication.create = lambda hostname: { "content": { "server_name_list": [ { "server_name": hostname } ] } }

TLSExtensionECPointFormats = Structure(name = "TLSExtensionECPointFormats", members = [
	IM("extension_id",					"uint16", enum_class = ExtensionType, fixed_value = ExtensionType.ec_point_formats),
	IM("content",						"opaque16", inner = Structure([
		IM("point_formats",					"opaque8", contains_array = True, inner =
			IM("point_format",					"uint8", enum_class = ECPointFormats),
		),
	])),
])

TLSExtensionSupportedGroups = Structure(name = "TLSExtensionSupportedGroups", members = [
	IM("extension_id",					"uint16", enum_class = ExtensionType, fixed_value = ExtensionType.supported_groups),
	IM("content",						"opaque16", inner = Structure([
		IM("groups",						"opaque16", contains_array = True, inner =
			IM("group",							"uint16", enum_class = SupportedGroups),
		),
	])),
])

AnyExtension = VariableType(name = "AnyExtension", possible_inner_classes = [
	TLSExtensionServerNameIndication,
	TLSExtensionECPointFormats,
	TLSExtensionSupportedGroups,
	TLSExtensionFlag,
	TLSExtension,
])

AlertPkt = Structure(name = "AlertPkt", members = [
	IM("alert_level",		"uint8", enum_class = TLSAlertLevel),
	IM("alert_description",	"uint8", enum_class = TLSAlertDescription),
])

ClientHelloPkt = Structure(name = "ClientHelloPkt", members = [
	IM("handshake_type",				"uint8", enum_class = HandshakeType, fixed_value = HandshakeType.ClientHello),
	IM("payload",						"opaque24", inner = Structure([
		IM("handshake_protocol_version",	"uint16", enum_class = TLSVersionHandshake),
		IM("client_random",					"array[32]"),
		IM("session_id",					"opaque8"),
		IM("cipher_suites",					"opaque16", contains_array = True, inner =
			IM("cipher_suite",					"uint16", enum_class = CipherSuite),
		),
		IM("compression_methods",			"opaque8", contains_array = True, inner =
			IM("compression_method",			"uint8", enum_class = CompressionMethod),
		),
		IM("extensions",					"opaque16", contains_array = True, inner = AnyExtension),
	])),
])

ServerHelloPkt = Structure(name = "ServerHelloPkt", members = [
	IM("handshake_type",				"uint8", enum_class = HandshakeType, fixed_value = HandshakeType.ServerHello),
	IM("payload",						"opaque24", inner = Structure([
		IM("handshake_protocol_version",	"uint16", enum_class = TLSVersionHandshake),
		IM("server_random",					"array[32]"),
		IM("session_id",					"opaque8"),
		IM("cipher_suite",					"uint16", enum_class = CipherSuite),
		IM("compression_method",			"uint8", enum_class = CompressionMethod),
		IM("extensions",					"opaque16", contains_array = True, inner = AnyExtension),
	])),
])

CertificatePkt = Structure(name = "Certificate", members = [
	IM("handshake_type",				"uint8", enum_class = HandshakeType, fixed_value = HandshakeType.Certificate),
	IM("payload",						"opaque24", inner = Structure([
		IM("certificates",					"opaque24", contains_array = True, inner =
			IM("certificate", "opaque24"),
		),
	])),
])

ClientHandshakeMessage = VariableType(name = "ClientHandshakeMessage", possible_inner_classes = [
	ClientHelloPkt,
	CertificatePkt,
])

ServerHandshakeMessage = VariableType(name = "ServerHandshakeMessage", possible_inner_classes = [
	ServerHelloPkt,
	CertificatePkt,
])
