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

import datetime
import calendar
from pyasn1.type.useful import GeneralizedTime
from x509sak.Tools import DateTimeTools
from x509sak.estimate.BaseEstimator import BaseEstimator
from x509sak.estimate import JudgementCode, Verdict, Commonness, Compatibility
from x509sak.estimate.Judgement import SecurityJudgement, SecurityJudgements, RFCReference

@BaseEstimator.register
class CrtValiditySecurityEstimator(BaseEstimator):
	_ALG_NAME = "crt_validity"

	def _format_datetime(self, dt):
		return {
			"iso":		DateTimeTools.strfmt_iso(dt),
			"timet":	calendar.timegm(dt.utctimetuple()),
		}

	def analyze(self, certificate):
		not_before = certificate.valid_not_before
		not_after = certificate.valid_not_after
		is_ca = certificate.is_ca_certificate
		judgements = SecurityJudgements()

		if not_before is None:
			judgements += SecurityJudgement(JudgementCode.X509Cert_Body_Validity_NotBefore_Malformed, "'Not Before' timestamp is malformed. Certificate is always invalid.", bits = 0, compatibility = Compatibility.STANDARDS_DEVIATION)
			validity_days = 0
		elif not_after is None:
			judgements += SecurityJudgement(JudgementCode.X509Cert_Body_Validity_NotAfter_Malformed, "'Not After' timestamp is malformed. Certificate is always invalid.", bits = 0, compatibility = Compatibility.STANDARDS_DEVIATION)
			validity_days = 0
		else:
			now = datetime.datetime.utcnow()
			if not_before > not_after:
				judgements += SecurityJudgement(JudgementCode.X509Cert_Body_Validity_Status_NeverValid, "'Not Before' timestamp is greater than 'not after' timestamp. Certificate is always invalid.", bits = 0)
			elif now < not_before:
				judgements += SecurityJudgement(JudgementCode.X509Cert_Body_Validity_Status_NotYetValid, "Certificate is not yet valid, becomes valid in the future.", bits = 0, commonness = Commonness.UNUSUAL)
			elif now > not_after:
				judgements += SecurityJudgement(JudgementCode.X509Cert_Body_Validity_Status_Expired, "Certificate has expired.", bits = 0, commonness = Commonness.COMMON)
			else:
				judgements += SecurityJudgement(JudgementCode.X509Cert_Body_Validity_Status_CurrentlyValid, "Certificate is currently valid.", commonness = Commonness.COMMON)

			validity_days = ((not_after - not_before).total_seconds()) / 86400

			if not is_ca:
				margins = [ 2 * 365.25, 5 * 365.25, 7 * 365.25 ]
			else:
				margins = [ 12.5 * 365.25, 25 * 365.25, 30 * 365.25 ]

			# Add some error margin
			margins = [ margin + 14 for margin in margins ]

			crt_type = "CA" if is_ca else "non-CA"
			if validity_days < margins[0]:
				judgements += SecurityJudgement(JudgementCode.X509Cert_Body_Validity_Length_Conservative, "Lifetime is conservative for %s certificate." % (crt_type), commonness = Commonness.COMMON, verdict = Verdict.BEST_IN_CLASS)
			elif validity_days < margins[1]:
				judgements += SecurityJudgement(JudgementCode.X509Cert_Body_Validity_Length_Long, "Lifetime is long, but still acceptable for %s certificate." % (crt_type), commonness = Commonness.COMMON, verdict = Verdict.HIGH)
			elif validity_days < margins[2]:
				judgements += SecurityJudgement(JudgementCode.X509Cert_Body_Validity_Length_VeryLong, "Lifetime is very long for %s certificate." % (crt_type), commonness = Commonness.UNUSUAL, verdict = Verdict.MEDIUM)
			else:
				judgements += SecurityJudgement(JudgementCode.X509Cert_Body_Validity_Length_ExceptionallyLong, "Lifetime is exceptionally long for %s certificate." % (crt_type), commonness = Commonness.HIGHLY_UNUSUAL, verdict = Verdict.WEAK)

			if (not_before < datetime.datetime(2050, 1, 1, 0, 0, 0)) and isinstance(certificate.asn1["tbsCertificate"]["validity"]["notBefore"].getComponent(), GeneralizedTime):
				standard = RFCReference(rfcno = 5280, sect = "4.1.2.5", verb = "MUST", text = "CAs conforming to this profile MUST always encode certificate validity dates through the year 2049 as UTCTime; certificate validity dates in 2050 or later MUST be encoded as GeneralizedTime.")
				judgements += SecurityJudgement(JudgementCode.X509Cert_Body_Validity_NotBefore_InvalidType, "GeneralizedTime used for 'not before' validity timestamp although earlier than year 2050.", compatibility = Compatibility.STANDARDS_DEVIATION, standard = standard)
			if (not_after < datetime.datetime(2050, 1, 1, 0, 0, 0)) and isinstance(certificate.asn1["tbsCertificate"]["validity"]["notAfter"].getComponent(), GeneralizedTime):
				standard = RFCReference(rfcno = 5280, sect = "4.1.2.5", verb = "MUST", text = "CAs conforming to this profile MUST always encode certificate validity dates through the year 2049 as UTCTime; certificate validity dates in 2050 or later MUST be encoded as GeneralizedTime.")
				judgements += SecurityJudgement(JudgementCode.X509Cert_Body_Validity_NotAfter_InvalidType, "GeneralizedTime used for 'not after' validity timestamp although earlier than year 2050.", compatibility = Compatibility.STANDARDS_DEVIATION, standard = standard)

		return {
			"not_before":		self._format_datetime(not_before) if not_before is not None else None,
			"not_after":		self._format_datetime(not_after) if not_after is not None else None,
			"validity_days":	validity_days,
			"security":			judgements,
		}
