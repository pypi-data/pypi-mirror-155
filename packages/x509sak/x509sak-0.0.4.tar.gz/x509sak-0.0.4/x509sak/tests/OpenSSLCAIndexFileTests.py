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

import tempfile
from x509sak.tests import BaseTest, ResourceFileLoader
from x509sak.OpenSSLCAIndexFile import OpenSSLCAIndexFile

class OpenSSLCAIndexFileTests(BaseTest):
	def test_index_file(self):
		with ResourceFileLoader("misc/index.txt") as infile, tempfile.NamedTemporaryFile(prefix = "new_index_", suffix = ".txt") as outfile:
			index_file = OpenSSLCAIndexFile(infile)

			# Write index file to outfile
			index_file.write(outfile.name)

			# Assert files are identical
			with open(infile, "rb") as f:
				in_data = f.read()
			with open(outfile.name, "rb") as f:
				out_data = f.read()
			self.assertEqual(in_data, out_data)
