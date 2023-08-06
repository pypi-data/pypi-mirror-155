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

from x509sak.OID import OIDDB
from x509sak.estimate.BaseEstimator import BaseEstimator
from x509sak.estimate import JudgementCode, AnalysisOptions, Verdict, Commonness
from x509sak.estimate.Judgement import SecurityJudgement, SecurityJudgements
from x509sak.Tools import ValidationTools
from x509sak.FlagChecker import FlagChecker

@BaseEstimator.register
class PurposeEstimator(BaseEstimator):
	_ALG_NAME = "purpose"

	def _judge_name(self, certificate, name):
		judgements = SecurityJudgements()
		rdns = certificate.subject.get_all(OIDDB.RDNTypes.inverse("CN"))
		have_valid_cn = False
		if len(rdns) > 0:
			found_rdn = None
			for rdn in rdns:
				value = rdn.get_value(OIDDB.RDNTypes.inverse("CN"))
				if ValidationTools.validate_domainname_template_match(value.printable_value, name):
					found_rdn = rdn
					break
			if found_rdn is not None:
				if found_rdn.component_cnt == 1:
					judgements += SecurityJudgement(JudgementCode.CertUsage_Purpose_ServerCert_CN_Match, "Common name (CN) matches '%s'." % (name), commonness = Commonness.COMMON)
				else:
					judgements += SecurityJudgement(JudgementCode.CertUsage_Purpose_ServerCert_CN_MatchMultivalueRDN, "Common name (CN) matches '%s', but is part of a multi-valued RDN: %s" % (name, found_rdn.pretty_str), commonness = Commonness.HIGHLY_UNUSUAL)
			else:
				judgements += SecurityJudgement(JudgementCode.CertUsage_Purpose_ServerCert_CN_Mismatch, "No common name (CN) matches '%s'." % (name), commonness = Commonness.UNUSUAL)

		have_valid_san = False
		extension = certificate.extensions.get_first(OIDDB.X509Extensions.inverse("SubjectAlternativeName"))
		if extension is not None:
			for san_name in extension.get_all("dNSName"):
				if ValidationTools.validate_domainname_template_match(san_name.str_value, name):
					have_valid_san = True
					judgements += SecurityJudgement(JudgementCode.CertUsage_Purpose_ServerCert_SAN_Match, "Subject Alternative Name matches '%s'." % (name), commonness = Commonness.COMMON)
					break
			else:
				judgements += SecurityJudgement(JudgementCode.CertUsage_Purpose_ServerCert_SAN_Mismatch, "No Subject Alternative Name X.509 extension matches '%s'." % (name), commonness = Commonness.UNUSUAL)

		if (not have_valid_cn) and (not have_valid_san):
			judgements += SecurityJudgement(JudgementCode.CertUsage_Purpose_ServerCert_NameVerificationFailed, "Found neither valid common name (CN) nor valid subject alternative name (SAN).", commonness = Commonness.HIGHLY_UNUSUAL, verdict = Verdict.NO_SECURITY)

		return judgements

	def _judge_purpose(self, certificate, purpose):
		judgements = SecurityJudgements()
		ku_ext = certificate.extensions.get_first(OIDDB.X509Extensions.inverse("KeyUsage"))
		eku_ext = certificate.extensions.get_first(OIDDB.X509Extensions.inverse("ExtendedKeyUsage"))
		ns_ext = certificate.extensions.get_first(OIDDB.X509Extensions.inverse("NetscapeCertificateType"))

		if certificate.is_ca_certificate:
			if purpose == AnalysisOptions.CertificatePurpose.TLSServerCertificate:
				judgements += SecurityJudgement(JudgementCode.CertUsage_Purpose_ServerCert_IsCACert, "Certificate is a valid CA certificate even though it's supposed to be a TLS server.", commonness = Commonness.HIGHLY_UNUSUAL, verdict = Verdict.NO_SECURITY)
			elif purpose == AnalysisOptions.CertificatePurpose.TLSClientCertificate:
				judgements += SecurityJudgement(JudgementCode.CertUsage_Purpose_ClientCert_IsCACert, "Certificate is a valid CA certificate even though it's supposed to be a TLS client.", commonness = Commonness.HIGHLY_UNUSUAL, verdict = Verdict.NO_SECURITY)

		if ku_ext is not None:
			# ('digitalSignature', 0),	The digitalSignature bit is asserted when the subject public key is used for verifying digital signatures, other than signatures on certificates (bit 5) and CRLs (bit 6), such as those used in an entity authentication service, a data origin authentication service, and/or an integrity service.
			# ('nonRepudiation', 1),	The nonRepudiation bit is asserted when the subject public key is used to verify digital signatures, other than signatures on certificates (bit 5) and CRLs (bit 6), used to provide a non-repudiation service that protects against the signing entity falsely denying some action.
			# ('keyEncipherment', 2),	The keyEncipherment bit is asserted when the subject public key is used for enciphering private or secret keys, i.e., for key transport.
			# ('dataEncipherment', 3),	The dataEncipherment bit is asserted when the subject public key is used for directly enciphering raw user data without the use of an intermediate symmetric cipher.  Note that the use of this bit is extremely uncommon
			# ('keyAgreement', 4),		The keyAgreement bit is asserted when the subject public key is used for key agreement.
			# ('keyCertSign', 5),
			# ('cRLSign', 6),
			# ('encipherOnly', 7),		The meaning of the encipherOnly bit is undefined in the absence of the keyAgreement bit. When the encipherOnly bit is asserted and the keyAgreement bit is also set, the subject public key may be used only for enciphering data while performing key agreement.
			# ('decipherOnly', 8)		The meaning of the decipherOnly bit is undefined in the absence of the keyAgreement bit. When the decipherOnly bit is asserted and the keyAgreement bit is also set, the subject public key may be used only for deciphering data while performing key agreement.

			flag_checker = FlagChecker()
			if purpose == AnalysisOptions.CertificatePurpose.CACertificate:
				flag_checker.may_not_have("nonRepudiation", "keyEncipherment", "dataEncipherment", "keyAgreement", "encipherOnly", "decipherOnly")
				flag_checker.must_have("keyCertSign")
				flag_checker.may_have("digitalSignature", "cRLSign")
			elif purpose in [ AnalysisOptions.CertificatePurpose.TLSClientCertificate, AnalysisOptions.CertificatePurpose.TLSServerCertificate ]:
				flag_checker.may_not_have("nonRepudiation", "dataEncipherment", "keyCertSign", "cRLSign", "encipherOnly", "decipherOnly")
				flag_checker.complex_check([ "digitalSignature", "keyEncipherment", "keyAgreement" ], min_count = 1)
			else:
				raise NotImplementedError(purpose)

			jcode = {
				"missing": {
					AnalysisOptions.CertificatePurpose.CACertificate: JudgementCode.CertUsage_Purpose_CACert_KU_MissingBits,
					AnalysisOptions.CertificatePurpose.TLSClientCertificate: JudgementCode.CertUsage_Purpose_ClientCert_KU_MissingBits,
					AnalysisOptions.CertificatePurpose.TLSServerCertificate: JudgementCode.CertUsage_Purpose_ServerCert_KU_MissingBits,
				}[purpose],
				"unusual": {
					AnalysisOptions.CertificatePurpose.CACertificate: JudgementCode.CertUsage_Purpose_CACert_KU_UnusualBits,
					AnalysisOptions.CertificatePurpose.TLSClientCertificate: JudgementCode.CertUsage_Purpose_ClientCert_KU_UnusualBits,
					AnalysisOptions.CertificatePurpose.TLSServerCertificate: JudgementCode.CertUsage_Purpose_ServerCert_KU_UnusualBits,
				}[purpose],
				"excess": {
					AnalysisOptions.CertificatePurpose.CACertificate: JudgementCode.CertUsage_Purpose_CACert_KU_ExcessBits,
					AnalysisOptions.CertificatePurpose.TLSClientCertificate: JudgementCode.CertUsage_Purpose_ClientCert_KU_ExcessBits,
					AnalysisOptions.CertificatePurpose.TLSServerCertificate: JudgementCode.CertUsage_Purpose_ServerCert_KU_ExcessBits,
				}[purpose],
			}

			for violation in flag_checker.check(ku_ext.all_flags):
				if violation.check_type == "missing":
					judgements += SecurityJudgement(jcode["missing"], "Certificate with purpose %s should have at least key usage flags %s, but %s is missing." % (purpose.name, ", ".join(sorted(violation.reference)), ", ".join(sorted(violation.flags))), commonness = Commonness.HIGHLY_UNUSUAL)
				elif violation.check_type == "excess":
					judgements += SecurityJudgement(jcode["excess"], "Certificate with purpose %s has excessive key usage bits set: %s" % (purpose.name, ", ".join(sorted(violation.flags))), commonness = Commonness.HIGHLY_UNUSUAL)
				elif violation.check_type == "unusual":
					judgements += SecurityJudgement(jcode["unusual"], "For certificate with purpose %s it is uncommon to have KeyUsage %s." % (purpose.name, ", ".join(sorted(violation.flags))), commonness = Commonness.UNUSUAL)
				elif violation.check_type == "complex_too_few":
					if len(violation.flags) == 0:
						judgements += SecurityJudgement(jcode["missing"], "Certificate with purpose %s should have at least %d flag(s) out of %s, but none were present." % (purpose.name, violation.reference_count, ", ".join(sorted(violation.reference))), commonness = Commonness.HIGHLY_UNUSUAL)
					else:
						judgements += SecurityJudgement(jcode["missing"], "Certificate with purpose %s should have at least %d flag(s) out of %s, but only %s were present." % (purpose.name, violation.reference_count, ", ".join(sorted(violation.reference)), ", ".join(sorted(violation.flags))), commonness = Commonness.HIGHLY_UNUSUAL)
				else:
					raise Exception(NotImplemented)

		if eku_ext is not None:
			if (purpose == AnalysisOptions.CertificatePurpose.TLSClientCertificate) and (not eku_ext.client_auth):
				judgements += SecurityJudgement(JudgementCode.CertUsage_Purpose_ClientCert_EKUMismatch, "Certificate is supposed to be a client certificate and has an Extended Key Usage extension, but no clientAuth flag set within that extension.", commonness = Commonness.UNUSUAL)

			if (purpose == AnalysisOptions.CertificatePurpose.TLSServerCertificate) and (not eku_ext.server_auth):
				judgements += SecurityJudgement(JudgementCode.CertUsage_Purpose_ServerCert_EKUMismatch, "Certificate is supposed to be a server certificate and has an Extended Key Usage extension, but no serverAuth flag set within that extension.", commonness = Commonness.UNUSUAL)

		if ns_ext is not None:
			if (purpose == AnalysisOptions.CertificatePurpose.TLSClientCertificate) and (not ns_ext.ssl_client):
				judgements += SecurityJudgement(JudgementCode.CertUsage_Purpose_ClientCert_NSCT_NoSSLClient, "Certificate is supposed to be a client certificate and has an Netscape Certificate Type extension, but no sslClient flag set within that extension.", commonness = Commonness.UNUSUAL)

			if (purpose == AnalysisOptions.CertificatePurpose.TLSServerCertificate) and (not ns_ext.ssl_server):
				judgements += SecurityJudgement(JudgementCode.CertUsage_Purpose_ServerCert_NSCT_NoSSLServer, "Certificate is supposed to be a server certificate and has an Netscape Certificate Type extension, but no sslServer flag set within that extension.", commonness = Commonness.UNUSUAL)

			if (purpose == AnalysisOptions.CertificatePurpose.CACertificate):
				if not any(flag in ns_ext.flags for flag in [ "sslCA", "emailCA", "objCA" ]):
					# No CA bit is set
					judgements += SecurityJudgement(JudgementCode.CertUsage_Purpose_CACert_NSCT_NoCA, "Certificate is supposed to be a CA certificate and has an Netscape Certificate Type extension, but neither sslCA/emailCA/objCA flag set within that extension.", commonness = Commonness.UNUSUAL)
				else:
					# At least it's some type of CA. But is it a SSL CA?
					if "sslCA" not in ns_ext.flags:
						judgements += SecurityJudgement(JudgementCode.CertUsage_Purpose_CACert_NSCT_NoSSLCA, "Certificate is supposed to be a CA certificate and has an Netscape Certificate Type extension, but it is not marked as an SSL CA. It can only be used for S/MIME or object signing.", commonness = Commonness.UNUSUAL)

		if purpose == AnalysisOptions.CertificatePurpose.CACertificate:
			if not certificate.is_ca_certificate:
				judgements += SecurityJudgement(JudgementCode.CertUsage_Purpose_CACert_NoCACert, "Certificate is not a valid CA certificate even though it's supposed to be.", commonness = Commonness.HIGHLY_UNUSUAL, verdict = Verdict.NO_SECURITY)

		return judgements

	def analyze(self, certificate):
		result = [ ]

		if self._analysis_options.fqdn is not None:
			analysis = {
				"type":			"name_match",
				"name":			self._analysis_options.fqdn,
				"security":		self._judge_name(certificate, self._analysis_options.fqdn),
			}
			result.append(analysis)

		for purpose in self._analysis_options.purposes:
			analysis = {
				"type":			"purpose_match",
				"purpose":		purpose,
				"security":		self._judge_purpose(certificate, purpose),
			}
			result.append(analysis)

		return result
