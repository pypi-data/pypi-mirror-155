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

class CmdLineTestsGraphPool(BaseTest):
	def test_create_dot(self):
		with tempfile.NamedTemporaryFile(prefix = "graph_", suffix = ".dot") as f, ResourceFileLoader("certs/ok/johannes-bauer.com.pem") as certfile:
			self._run_x509sak([ "graph", "--outfile", f.name, certfile ])
			with open(f.name) as f:
				dotfile = f.read()
			self.assertIn("digraph", dotfile)
			self.assertIn("bcade7ce", dotfile)

	def test_render_dot_png(self):
		with tempfile.NamedTemporaryFile(prefix = "graph_", suffix = ".png") as f, ResourceFileLoader("certs/ok/johannes-bauer.com.pem") as certfile:
			self._run_x509sak([ "graph", "--outfile", f.name, certfile ])
			with open(f.name, "rb") as f:
				dotfile = f.read()
			self.assertTrue(dotfile.startswith(b"\x89PNG\r\n"))

	def test_render_dot_ps(self):
		with tempfile.NamedTemporaryFile(prefix = "graph_", suffix = ".ps") as f, ResourceFileLoader("certs/ok/johannes-bauer.com.pem") as certfile:
			self._run_x509sak([ "graph", "--outfile", f.name, certfile ])
			with open(f.name, "rb") as f:
				dotfile = f.read()
			self.assertTrue(dotfile.startswith(b"%!PS-Adobe-3.0"))

	def test_render_dot_pdf(self):
		with tempfile.NamedTemporaryFile(prefix = "graph_", suffix = ".pdf") as f, ResourceFileLoader("certs/ok/johannes-bauer.com.pem") as certfile:
			self._run_x509sak([ "graph", "--outfile", f.name, certfile ])
			with open(f.name, "rb") as f:
				dotfile = f.read()
			self.assertTrue(dotfile.startswith(b"%PDF"))

	def test_render_unknown_ext(self):
		with tempfile.NamedTemporaryFile(prefix = "graph_", suffix = ".xyz") as f, ResourceFileLoader("certs/ok/johannes-bauer.com.pem") as certfile:
			self._run_x509sak([ "graph", "--outfile", f.name, certfile ], success_return_codes = [ 1 ])
			self._run_x509sak([ "graph", "--outfile", f.name, "--format", "pdf", certfile ])
			with open(f.name, "rb") as f:
				dotfile = f.read()
			self.assertTrue(dotfile.startswith(b"%PDF"))

	def test_render_multiple(self):
		with tempfile.NamedTemporaryFile(prefix = "graph_", suffix = ".dot") as f, ResourceFileLoader("certs/ok/johannes-bauer.com.pem", "certs/ok/johannes-bauer-intermediate.pem", "certs/ok/johannes-bauer-root.pem") as certfiles:
			self._run_x509sak([ "graph", "--outfile", f.name ] + list(certfiles))
