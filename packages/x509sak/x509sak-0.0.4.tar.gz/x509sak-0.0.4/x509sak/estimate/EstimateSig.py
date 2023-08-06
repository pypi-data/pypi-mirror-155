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

from pyasn1_modules import rfc3279
from x509sak.AlgorithmDB import SignatureAlgorithms, SignatureFunctions, Cryptosystems
from x509sak.estimate.BaseEstimator import BaseEstimator
from x509sak.estimate.Validator import ValidationJudgement
from x509sak.estimate import JudgementCode, Commonness, Compatibility
from x509sak.estimate.Judgement import SecurityJudgement, SecurityJudgements, RFCReference
from x509sak.estimate.Validator import ValidationIssue
from x509sak.NumberTheory import NumberTheory
from x509sak.RSAPSSParameters import RSAPSSParameters
from x509sak.estimate.DERValidator import DERValidator
from x509sak.Tools import ASN1Tools
from x509sak import ASN1Models

@BaseEstimator.register
class SignatureSecurityEstimator(BaseEstimator):
	_ALG_NAME = "sig"
	_DER_VALIDATOR_ECDSA_SIGNATURE = DERValidator.create_inherited("X509Cert_Signature_ECDSA", validation_subject = "ECDSA signature", specific_judgements = {
		("Enc_DER_EncodingIssues_Malformed_NonDEREncoding", "Enc_DER_EncodingIssues_Malformed_Undecodable", "Enc_DER_EncodingIssues_Malformed_UnexpectedType"): ValidationJudgement(standard = RFCReference(rfcno = 3279, sect = "2.2.3", verb = "SHALL", text = "To easily transfer these two values as one signature, they MUST be ASN.1 encoded using the following ASN.1 structure:")),
	})
	_DER_VALIDATOR_DSA_SIGNATURE = DERValidator.create_inherited("X509Cert_Signature_DSA", validation_subject = "DSA signature", specific_judgements = {
		("Enc_DER_EncodingIssues_Malformed_NonDEREncoding", "Enc_DER_EncodingIssues_Malformed_Undecodable", "Enc_DER_EncodingIssues_Malformed_UnexpectedType"): ValidationJudgement(standard = RFCReference(rfcno = 3279, sect = "2.2.2", verb = "SHALL", text = "To easily transfer these two values as one signature, they SHALL be ASN.1 encoded using the following ASN.1 structure:")),
	})

	_DER_VALIDATOR_RSAPSS_PARAMETERS = DERValidator(validation_subject = "RSA/PSS parameters", recognized_issues = {
		"Enc_DER_EncodingIssues_Malformed_NonDEREncoding":		ValidationIssue(code = JudgementCode.X509Cert_PublicKey_RSA_RSAPSS_Parameters_Malformed_NonDEREncoding),
		"Enc_DER_EncodingIssues_Malformed_UnexpectedType":		ValidationIssue(code = JudgementCode.X509Cert_PublicKey_RSA_RSAPSS_Parameters_Malformed_UnexpectedType),
	})

	def _analyze_rsa_pss_signature_params(self, signature_alg_params):
		judgements = SecurityJudgements()
		asn1_details = ASN1Tools.safe_decode(signature_alg_params, asn1_spec = ASN1Models.RSASSA_PSS_Params())
		judgements += self._DER_VALIDATOR_RSAPSS_PARAMETERS.validate(asn1_details)
		if asn1_details.asn1 is not None:
			rsapss = RSAPSSParameters.from_asn1(asn1_details.asn1)
			if rsapss.hash_algorithm is None:
				judgements += SecurityJudgement(JudgementCode.X509Cert_Signature_HashFunction_Unknown, "Certificate has unknown hash function for use in RSA-PSS, OID %s. Cannot make security determination for that part." % (rsapss.hash_algorithm_oid), commonness = Commonness.HIGHLY_UNUSUAL, compatibility = Compatibility.LIMITED_SUPPORT)

			if rsapss.mask_algorithm is None:
				judgements += SecurityJudgement(JudgementCode.X509Cert_PublicKey_RSA_RSA_PSS_UnknownMaskFunction, "Certificate has unknown mask function for use in RSA-PSS, OID %s." % (rsapss.mask_algorithm_oid), commonness = Commonness.HIGHLY_UNUSUAL, compatibility = Compatibility.LIMITED_SUPPORT)

			if rsapss.mask_hash_algorithm is None:
				judgements += SecurityJudgement(JudgementCode.X509Cert_Signature_HashFunction_Unknown, "Certificate has unknown mask hash function for use in RSA-PSS, OID %s." % (rsapss.mask_hash_algorithm_oid), commonness = Commonness.HIGHLY_UNUSUAL, compatibility = Compatibility.LIMITED_SUPPORT)

			if rsapss.trailer_field_value is None:
				judgements += SecurityJudgement(JudgementCode.X509Cert_PublicKey_RSA_RSA_PSS_UnknownTrailerField, "Certificate has unknown trailer field for use in RSA-PSS, trailer field ID %d." % (rsapss.trailer_field), commonness = Commonness.HIGHLY_UNUSUAL, compatibility = Compatibility.LIMITED_SUPPORT)

			if (rsapss.hash_algorithm is not None) and (rsapss.mask_hash_algorithm is not None) and (rsapss.hash_algorithm != rsapss.mask_hash_algorithm):
				standard = RFCReference(rfcno = 3447, sect = "8.1", verb = "RECOMMEND", text = "Therefore, it is recommended that the EMSA-PSS mask generation function be based on the same hash function.")
				judgements += SecurityJudgement(JudgementCode.X509Cert_PublicKey_RSA_RSA_PSS_MultipleHashFunctions, "RSA-PSS uses hash function %s for hashing, but %s for masking. This is discouraged." % (rsapss.hash_algorithm.name, rsapss.mask_hash_algorithm.name), commonness = Commonness.HIGHLY_UNUSUAL, compatibility = Compatibility.LIMITED_SUPPORT, standard = standard)

			if rsapss.salt_length < 0:
				judgements += SecurityJudgement(JudgementCode.X509Cert_PublicKey_RSA_RSAPSS_InvalidSaltLength, "Certificate has negative salt length for use in RSA-PSS, %d bytes specified." % (rsapss.salt_length), commonness = Commonness.HIGHLY_UNUSUAL, compatibility = Compatibility.STANDARDS_DEVIATION, bits = 0)
			elif rsapss.salt_length == 0:
				judgements += SecurityJudgement(JudgementCode.X509Cert_PublicKey_RSA_RSA_PSS_NoSaltUsed, "RSA-PSS does not use any salt.", commonness = Commonness.HIGHLY_UNUSUAL)
			elif rsapss.salt_length < 16:
				judgements += SecurityJudgement(JudgementCode.X509Cert_PublicKey_RSA_RSA_PSS_ShortSaltUsed, "RSA-PSS uses a comparatively short salt value of %d bits." % (rsapss.salt_length * 8), commonness = Commonness.UNUSUAL)
			else:
				judgements += SecurityJudgement(JudgementCode.X509Cert_PublicKey_RSA_RSA_PSS_SaltLengthInBytes, "RSA-PSS uses a salt of %d bits." % (rsapss.salt_length * 8))
			return (rsapss.hash_algorithm, judgements)
		else:
			return (None, judgements)

	def _determine_hash_function(self, signature_alg, signature_alg_params):
		hash_fnc = None
		judgements = SecurityJudgements()
		if signature_alg == SignatureAlgorithms.RSASSA_PSS:
			(hash_fnc, new_judgements) = self._analyze_rsa_pss_signature_params(signature_alg_params)
			judgements += new_judgements
		else:
			judgements += SecurityJudgement(JudgementCode.X509sakIssues_AnalysisNotImplemented, "Cannot determine hash function for signature algorithm %s. This might be a shortcoming of x509sak; please report the certificate in question to the developers." % (signature_alg.name))

		return (hash_fnc, judgements)

	def analyze(self, signature_alg_oid, signature_alg_params, signature, root_cert = None):
		judgements = SecurityJudgements()
		signature_alg = SignatureAlgorithms.lookup("oid", signature_alg_oid)
		if signature_alg is None:
			judgements += SecurityJudgement(JudgementCode.X509Cert_Signature_Function_Unknown, "Certificate has unknown signature algorithm with OID %s. Cannot make security determination." % (signature_alg_oid), commonness = Commonness.HIGHLY_UNUSUAL, compatibility = Compatibility.LIMITED_SUPPORT)
			result = {
				"name":			str(signature_alg_oid),
				"pretty":		str(signature_alg_oid),
				"security":		judgements,
			}
			return result

		if isinstance(signature_alg.value.oid, (tuple, list)):
			# Have more than one OID for this
			if signature_alg.value.oid[0] != signature_alg_oid:
				judgements += SecurityJudgement(JudgementCode.X509Cert_Signature_Function_DeprecatedOID, "Signature algorithm uses alternate OID %s for algorithm %s. Preferred OID would be %s." % (signature_alg_oid, signature_alg.name, signature_alg.value.oid[0]), commonness = Commonness.HIGHLY_UNUSUAL, compatibility = Compatibility.LIMITED_SUPPORT)

		if signature_alg.value.hash_fnc is not None:
			# Signature algorithm already implies a concrete hash function, already done.
			hash_fnc = signature_alg.value.hash_fnc
		else:
			# Signature algorithms depends and is not implied.
			(hash_fnc, new_judgements) = self._determine_hash_function(signature_alg, signature_alg_params)
			judgements += new_judgements

		if signature_alg.value.sig_fnc == SignatureFunctions.ecdsa:
			# Decode ECDSA signature
			asn1_details = ASN1Tools.safe_decode(signature, asn1_spec = rfc3279.ECDSA_Sig_Value())
			judgements += self._DER_VALIDATOR_ECDSA_SIGNATURE.validate(asn1_details)
			if (asn1_details.asn1 is not None) and (root_cert is not None):
				if root_cert.pubkey.pk_alg.value.cryptosystem == Cryptosystems.ECC_ECDSA:
					# Check that this is really a potential parent CA certificate
					ca_curve = root_cert.pubkey.curve
					hweight_analysis = NumberTheory.hamming_weight_analysis(int(asn1_details.asn1["r"]), min_bit_length = ca_curve.field_bits)
					if not hweight_analysis.plausibly_random:
						judgements += SecurityJudgement(JudgementCode.X509Cert_Signature_ECDSA_R_BitBiasPresent, "Hamming weight of ECDSA signature R parameter is %d at bitlength %d, but expected a weight between %d and %d when randomly chosen; this is likely not coincidential." % (hweight_analysis.hweight, hweight_analysis.bitlen, hweight_analysis.rnd_min_hweight, hweight_analysis.rnd_max_hweight), commonness = Commonness.HIGHLY_UNUSUAL)
					hweight_analysis = NumberTheory.hamming_weight_analysis(int(asn1_details.asn1["s"]), min_bit_length = ca_curve.field_bits)
					if not hweight_analysis.plausibly_random:
						judgements += SecurityJudgement(JudgementCode.X509Cert_Signature_ECDSA_S_BitBiasPresent, "Hamming weight of ECDSA signature S parameter is %d at bitlength %d, but expected a weight between %d and %d when randomly chosen; this is likely not coincidential." % (hweight_analysis.hweight, hweight_analysis.bitlen, hweight_analysis.rnd_min_hweight, hweight_analysis.rnd_max_hweight), commonness = Commonness.HIGHLY_UNUSUAL)

		elif signature_alg.value.sig_fnc == SignatureFunctions.dsa:
			# Decode DSA signature
			asn1_details = ASN1Tools.safe_decode(signature, asn1_spec = rfc3279.Dss_Sig_Value())
			judgements += self._DER_VALIDATOR_DSA_SIGNATURE.validate(asn1_details)
			if (asn1_details.asn1 is not None) and (root_cert is not None):
				if root_cert is not None:
					if root_cert.pubkey.pk_alg.value.cryptosystem == Cryptosystems.DSA:
						field_width = root_cert.pubkey.q.bit_length()

						hweight_analysis = NumberTheory.hamming_weight_analysis(int(asn1_details.asn1["r"]), min_bit_length = field_width)
						if not hweight_analysis.plausibly_random:
							judgements += SecurityJudgement(JudgementCode.X509Cert_Signature_DSA_R_BitBiasPresent, "Hamming weight of DSA signature R parameter is %d at bitlength %d, but expected a weight between %d and %d when randomly chosen; this is likely not coincidential." % (hweight_analysis.hweight, hweight_analysis.bitlen, hweight_analysis.rnd_min_hweight, hweight_analysis.rnd_max_hweight), commonness = Commonness.HIGHLY_UNUSUAL)

						hweight_analysis = NumberTheory.hamming_weight_analysis(int(asn1_details.asn1["s"]), min_bit_length = field_width)
						if not hweight_analysis.plausibly_random:
							judgements += SecurityJudgement(JudgementCode.X509Cert_Signature_DSA_S_BitBiasPresent, "Hamming weight of DSA signature S parameter is %d at bitlength %d, but expected a weight between %d and %d when randomly chosen; this is likely not coincidential." % (hweight_analysis.hweight, hweight_analysis.bitlen, hweight_analysis.rnd_min_hweight, hweight_analysis.rnd_max_hweight), commonness = Commonness.HIGHLY_UNUSUAL)

		result = {
			"name":				signature_alg.name,
			"sig_fnc":			self.algorithm("sig_fnc").analyze(signature_alg.value.sig_fnc),
			"security":			judgements,
		}
		if hash_fnc is not None:
			result.update({
				"pretty":		signature_alg.value.sig_fnc.value.pretty_name + " with " + hash_fnc.value.pretty_name,
				"hash_fnc":		self.algorithm("hash_fnc").analyze(hash_fnc),
			})
		else:
			result.update({
				"pretty":		 "%s with undetermined hash function" % (signature_alg.value.sig_fnc.value.pretty_name)
			})
		return result
