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
import tempfile
from x509sak.tests import BaseTest
from x509sak.WorkDir import WorkDir
from x509sak.SubprocessExecutor import SubprocessExecutor

class CmdLineTestsCreateCA(BaseTest):
	def test_create_simple_ca(self):
		with tempfile.TemporaryDirectory() as tempdir, WorkDir(tempdir):
			self._run_x509sak([ "createca", "root_ca" ])
			output = SubprocessExecutor([ "openssl", "x509", "-text", "-in", "root_ca/CA.crt" ]).run().stdout
			self.assertIn(b"--BEGIN CERTIFICATE--", output)
			self.assertIn(b"--END CERTIFICATE--", output)
			self.assertIn(b"id-ecPublicKey", output)
			SubprocessExecutor([ "openssl", "ec", "-in", "root_ca/CA.key" ]).run()

	def test_create_simple_ca_2(self):
		with tempfile.TemporaryDirectory() as tempdir, WorkDir(tempdir):
			self._run_x509sak([ "createca", "-g", "ecc:secp256r1", "-s", "/CN=YepThatsTheCN", "-h", "sha512", "root_ca" ])
			output = SubprocessExecutor([ "openssl", "x509", "-text", "-in", "root_ca/CA.crt" ]).run().stdout
			self.assertIn(b"--BEGIN CERTIFICATE--", output)
			self.assertIn(b"--END CERTIFICATE--", output)
			self.assertIn(b"id-ecPublicKey", output)
			self.assertIn(b"ecdsa-with-SHA512", output)
			self.assertIn(b"prime256v1", output)
			self.assertTrue((b"CN=YepThatsTheCN" in output) or (b"CN = YepThatsTheCN" in output))
			self.assertIn(b"X509v3 extensions", output)
			self.assertIn(b"CA:TRUE", output)
			self.assertIn(b"X509v3 Subject Key Identifier", output)
			SubprocessExecutor([ "openssl", "ec", "-in", "root_ca/CA.key" ]).run()

	def test_create_simple_ca_3(self):
		with tempfile.TemporaryDirectory() as tempdir, WorkDir(tempdir):
			self._run_x509sak([ "createca", "-g", "rsa:1024", "-s", "/CN=YepThats!TheCN", "-h", "sha1", "root_ca" ])
			output = SubprocessExecutor([ "openssl", "x509", "-text", "-in", "root_ca/CA.crt" ]).run().stdout
			self.assertIn(b"--BEGIN CERTIFICATE--", output)
			self.assertIn(b"--END CERTIFICATE--", output)
			self.assertIn(b"rsaEncryption", output)
			self.assertIn(b"sha1WithRSAEncryption", output)
			self.assertIn(b"Public-Key: (1024 bit)", output)
			self.assertTrue((b"CN=YepThats!TheCN" in output) or (b"CN = YepThats!TheCN" in output))
			self.assertIn(b"X509v3 extensions", output)
			self.assertIn(b"CA:TRUE", output)
			self.assertIn(b"X509v3 Subject Key Identifier", output)
			SubprocessExecutor([ "openssl", "rsa", "-in", "root_ca/CA.key" ]).run()

	def test_create_nested_ca(self):
		with tempfile.TemporaryDirectory() as tempdir, WorkDir(tempdir):
			self._run_x509sak([ "createca", "this/is/a/root_ca" ])
			output = SubprocessExecutor([ "openssl", "x509", "-text", "-in", "this/is/a/root_ca/CA.crt" ]).run().stdout
			self.assertIn(b"--BEGIN CERTIFICATE--", output)
			self.assertIn(b"--END CERTIFICATE--", output)
			self.assertIn(b"id-ecPublicKey", output)
			SubprocessExecutor([ "openssl", "ec", "-in", "this/is/a/root_ca/CA.key" ]).run()

	def test_create_intermediate_ca(self):
		with tempfile.TemporaryDirectory() as tempdir, WorkDir(tempdir):
			self._run_x509sak([ "createca", "-s", "/CN=PARENT", "root_ca" ])
			output = SubprocessExecutor([ "openssl", "x509", "-text", "-in", "root_ca/CA.crt" ]).run().stdout
			self.assertIn(b"--BEGIN CERTIFICATE--", output)
			self.assertIn(b"--END CERTIFICATE--", output)
			self.assertTrue((b"Issuer: CN=PARENT" in output) or (b"Issuer: CN = PARENT" in output))
			self.assertTrue((b"Subject: CN=PARENT" in output) or (b"Subject: CN = PARENT" in output))
			self.assertIn(b"id-ecPublicKey", output)
			SubprocessExecutor([ "openssl", "ec", "-in", "root_ca/CA.key" ]).run()

			self._run_x509sak([ "createca", "-p", "root_ca", "-s", "/CN=INTERMEDIATE", "intermediate_ca" ])
			output = SubprocessExecutor([ "openssl", "x509", "-text", "-in", "intermediate_ca/CA.crt" ]).run().stdout
			self.assertIn(b"--BEGIN CERTIFICATE--", output)
			self.assertIn(b"--END CERTIFICATE--", output)
			self.assertTrue((b"Issuer: CN=PARENT" in output) or (b"Issuer: CN = PARENT" in output))
			self.assertTrue((b"Subject: CN=INTERMEDIATE" in output) or (b"Subject: CN = INTERMEDIATE" in output))
			self.assertIn(b"id-ecPublicKey", output)
			SubprocessExecutor([ "openssl", "ec", "-in", "intermediate_ca/CA.key" ]).run()

	def test_subject_info(self):
		with tempfile.TemporaryDirectory() as tempdir, WorkDir(tempdir):
			self._run_x509sak([ "createca", "-s", "/CN=Elem00/OU=Elem01/C=DE/SN=Elem02/GN=Elem03/emailAddress=Elem04/title=Elem05/L=Elem06/stateOrProvinceName=Elem07/pseudonym=Elem08", "root_ca" ])
			output = SubprocessExecutor([ "openssl", "x509", "-subject", "-noout", "-in", "root_ca/CA.crt" ]).run().stdout
			self.assertIn(b"DE", output)
			for eid in range(9):
				element = ("Elem%02d" % (eid)).encode("ascii")
				self.assertIn(element, output)

	def test_x509_extension(self):
		with tempfile.TemporaryDirectory() as tempdir, WorkDir(tempdir):
			self._run_x509sak([ "createca", "--extension", "nameConstraints=critical,permitted;DNS:foo.bar.com", "root_ca" ])
			output = SubprocessExecutor([ "openssl", "x509", "-text", "-noout", "-in", "root_ca/CA.crt" ]).run().stdout
			self.assertIn(b"DNS:foo.bar.com", output)
			self.assertNotIn(b"pathlen", output)

			self._run_x509sak([ "createca", "--extension", "nameConstraints=critical,permitted;DNS:foo.bar.com", "--extension", "basicConstraints=critical,CA:TRUE,pathlen:123", "root_ca2" ])
			output = SubprocessExecutor([ "openssl", "x509", "-text", "-noout", "-in", "root_ca2/CA.crt" ]).run().stdout
			self.assertIn(b"DNS:foo.bar.com", output)
			self.assertIn(b"pathlen:123", output)

	def test_dont_overwrite_dir_except_force(self):
		with tempfile.TemporaryDirectory() as tempdir, WorkDir(tempdir):
			os.makedirs("root_ca")
			with open("root_ca/foobar", "wb"):
				pass
			self._run_x509sak([ "createca", "root_ca" ], success_return_codes = [ 1 ])
			self.assertTrue(os.path.isfile("root_ca/foobar"))
			self._run_x509sak([ "createca", "--force", "root_ca" ])
			self.assertFalse(os.path.isfile("root_ca/foobar"))

	def test_serial_spec(self):
		with tempfile.TemporaryDirectory() as tempdir, WorkDir(tempdir):
			self._run_x509sak([ "createca", "-s", "/CN=PARENT", "--serial", "1234567", "root_ca" ])
			output = SubprocessExecutor([ "openssl", "x509", "-text", "-in", "root_ca/CA.crt" ]).run().stdout
			self.assertIn(b"Serial Number: 1234567", output)

			self._run_x509sak([ "createca", "-s", "/CN=PARENT", "-f", "--serial", "0x1234567", "root_ca" ])
			output = SubprocessExecutor([ "openssl", "x509", "-text", "-in", "root_ca/CA.crt" ]).run().stdout
			self.assertIn(b"Serial Number: 19088743", output)

			# Catch error message
			output = self._run_x509sak([ "createca", "-p", "root_ca", "-s", "/CN=INTERMEDIATE", "--serial", "9876", "intermediate_ca" ], success_return_codes = [ 1 ]).stderr
			self.assertIn(b"specify certificate serial number", output)
