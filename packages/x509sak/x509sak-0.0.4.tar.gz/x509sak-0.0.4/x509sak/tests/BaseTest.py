#	x509sak - The X.509 Swiss Army Knife white-hat certificate toolkit
#	Copyright (C) 2018-2019 Johannes Bauer
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
import unittest
import pkgutil
import gzip
import tempfile
import json
from x509sak import X509Certificate
from x509sak.PublicKey import PublicKey
from x509sak.RSAPrivateKey import RSAPrivateKey
from x509sak.SubprocessExecutor import SubprocessExecutor

class ResourceFileLoader():
	def __init__(self, *resource_names):
		self._resource_names = resource_names
		self._tempfiles = None

	@classmethod
	def load_data(cls, filename, auto_decompress = True):
		if filename is None:
			return None
		data = pkgutil.get_data("x509sak.tests.data", filename)
		if auto_decompress and filename.endswith(".gz"):
			data = gzip.decompress(data)
		return data

	def __enter__(self):
		filenames = [ ]
		self._tempfiles = [ ]

		for resource_name in self._resource_names:
			if isinstance(resource_name, str):
				# Load a single file
				data = self.load_data(resource_name)
				tmpfile = tempfile.NamedTemporaryFile(mode = "wb")
				tmpfile.write(data)
				tmpfile.flush()
			elif isinstance(resource_name, (tuple, list)):
				# Load multiple files
				tmpfile = tempfile.TemporaryDirectory()
				for resource in resource_name:
					data = self.load_data(resource)
					with open(tmpfile.name + "/" + os.path.basename(resource), "wb") as f:
						f.write(data)
			elif resource_name is None:
				# Allow this to avoid having multiple nested cases (e.g.,
				# loading cert + CA cert vs. only cert)
				return None
			else:
				raise NotImplementedError(type(resource_name))
			self._tempfiles.append(tmpfile)
			filenames.append(tmpfile.name)

		if len(filenames) == 1:
			return filenames[0]
		else:
			return filenames

	def __exit__(self, *args):
		for tmpfile in self._tempfiles:
			if getattr(tmpfile, "close", None) is not None:
				tmpfile.close()
			else:
				tmpfile.cleanup()

class BaseTest(unittest.TestCase):
	def __init__(self, *args, **kwargs):
		unittest.TestCase.__init__(self, *args, **kwargs)
		self._x509sak_binary = os.path.realpath("x509sak.py")
		self._produce_statistics = "X509SAK_TEST_STATISTICS" in os.environ
		if "X509SAK_COVERAGE" not in os.environ:
			self._coverage = None
		else:
			self._coverage = json.loads(os.environ["X509SAK_COVERAGE"])

	def _run_x509sak(self, cmdline, env = None, success_return_codes = None, on_failure = "exception"):
		if self._coverage is None:
			cmd = [ self._x509sak_binary ] + cmdline
		else:
			if env is None:
				env = { }
			env["COVERAGE_FILE"] = self._coverage["coverage_path"] + ".coverage." + os.urandom(8).hex()
			cmd = [ "coverage", "run", "--parallel-mode", "--rcfile", self._coverage["coverage_path"] + ".coveragerc", "--omit", self._coverage["omit"], self._x509sak_binary ] + cmdline
			cmdx = [ self._x509sak_binary ] + cmdline
			print(cmdx)
		return SubprocessExecutor(cmd, env = env, success_return_codes = success_return_codes, on_failure = on_failure).run()

	def assertOcurrences(self, haystack, needle, expected_count):
		count = haystack.count(needle)
		self.assertEqual(count, expected_count)

	@staticmethod
	def _load_data(filename):
		return ResourceFileLoader.load_data(filename, auto_decompress = True)

	def _load_text(self, filename):
		return self._load_data(filename).decode("ascii")

	def _load_crt(self, crtname):
		x509_text = self._load_text("certs/" + crtname + ".pem")
		cert = X509Certificate.from_pem_data(x509_text)[0]
		return cert

	def _load_crt_pubkey(self, crtname):
		return self._load_crt(crtname).pubkey

	def _load_raw_pubkey(self, keyname):
		return PublicKey.from_pem_data(self._load_data(keyname))[0]

	def _load_privkey(self, keyname):
		privkey_text = self._load_text("privkey/" + keyname + ".pem")
		return RSAPrivateKey.from_pem_data(privkey_text)[0]

	def _load_json(self, filename):
		return json.loads(self._load_text(filename))
