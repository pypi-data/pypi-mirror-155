#	x509sak - The X.509 Swiss Army Knife white-hat certificate toolkit
#	Copyright (C) 2018-2018 Johannes Bauer
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

import os
from x509sak import CAManager
from x509sak.BaseAction import BaseAction

class ActionSignCSR(BaseAction):
	def __init__(self, cmdname, args):
		BaseAction.__init__(self, cmdname, args)

		if os.path.exists(self._args.crt_filename) and (not self._args.force):
			raise Exception("File/directory %s already exists. Remove it first or use --force." % (self._args.crt_filename))

		camgr = CAManager(self._args.capath)
		custom_x509_extensions = { custom_x509_extension.key: custom_x509_extension.value for custom_x509_extension in self._args.extension }
		camgr.sign_csr(self._args.csr_filename, self._args.crt_filename, extension_template = self._args.template, custom_x509_extensions = custom_x509_extensions, subject_dn = self._args.subject_dn, validity_days = self._args.validity_days, signing_hash = self._args.hashfnc, subject_alternative_dns_names = self._args.san_dns, subject_alternative_ip_addresses = self._args.san_ip)
