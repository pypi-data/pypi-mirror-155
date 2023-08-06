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
import random
from x509sak.BaseAction import BaseAction
from x509sak.PrimeDB import PrimeDB
from x509sak.RSAPrivateKey import RSAPrivateKey
from x509sak.NumberTheory import NumberTheory
from x509sak.Exceptions import UnfulfilledPrerequisitesException, InvalidInputException

class ActionGenerateBrokenRSA(BaseAction):
	def __init__(self, cmdname, args):
		BaseAction.__init__(self, cmdname, args)

		if (not self._args.force) and os.path.exists(self._args.outfile):
			raise UnfulfilledPrerequisitesException("File/directory %s already exists. Remove it first or use --force." % (self._args.outfile))

		if not self._args.gcd_n_phi_n:
			self._primetype = "2msb"
			self._p_bitlen = self._args.bitlen // 2
			self._q_bitlen = self._args.bitlen - self._p_bitlen
		else:
			self._primetype = "3msb"
			self._p_bitlen = self._args.bitlen // 3
			self._q_bitlen = self._args.bitlen - (2 * self._p_bitlen) - 1

		if (self._args.close_q) and (self._p_bitlen != self._q_bitlen):
			raise UnfulfilledPrerequisitesException("Generating a close-q keypair with a %d modulus does't work, because p would have to be %d bit and q %d bit. Choose an even modulus bitlength." % (self._args.bitlen, self._p_bitlen, self._q_bitlen))

		if self._args.q_stepping < 1:
			raise InvalidInputException("q-stepping value must be greater or equal to 1, was %d." % (self._args.q_stepping))

		self._log.debug("Selecting %s primes with p = %d bit and q = %d bit.", self._primetype, self._p_bitlen, self._q_bitlen)

		self._prime_db = PrimeDB(self._args.prime_db, generator_program = self._args.generator)
		p = None
		q = None
		while True:
			if p is None:
				p = self._prime_db.get(bitlen = self._p_bitlen, primetype = self._primetype)
				q_generator = self._select_q(p)
			if q is None:
				q = next(q_generator)
			if self._args.gcd_n_phi_n:
				# q = (2 * r * p) + 1
				r = q
				q = 2 * r * p + 1
				if not NumberTheory.is_probable_prime(q):
					q = None
					continue

			# Always make p the smaller factor
			if p > q:
				(p, q) = (q, p)

			n = p * q
			if self._args.public_exponent == -1:
				e = random.randint(2, n - 1)
			else:
				e = self._args.public_exponent

			if self._args.carmichael_totient:
				totient = NumberTheory.lcm(p - 1, q - 1)
			else:
				totient = (p - 1) * (q - 1)
			gcd = NumberTheory.gcd(totient, e)
			if self._args.accept_unusable_key or (gcd == 1):
				break
			else:
				# Pair (phi(n), e) wasn't acceptable.
				self._log.debug("gcd(totient, e) was %d, retrying.", gcd)
				if self._args.public_exponent != -1:
					# Public exponent e is fixed, need to choose another q.
					if p.bit_length() == q.bit_length():
						# Can re-use q as next p
						(p, q) = (q, None)
						q_generator = self._select_q(p)
					else:
						# When they differ in length, need to re-choose both values
						(p, q) = (None, None)

		rsa_keypair = RSAPrivateKey.create(p = p, q = q, e = e, swap_e_d = self._args.switch_e_d, valid_only = not self._args.accept_unusable_key, carmichael_totient = self._args.carmichael_totient)
		rsa_keypair.write_pemfile(self._args.outfile)
		if self._args.verbose >= 1:
			diff = q - p
			print("Generated %d bit RSA key:" % (rsa_keypair.n.bit_length()))
			print("p = 0x%x" % (rsa_keypair.p))
			if not self._args.gcd_n_phi_n:
				print("q = 0x%x" % (rsa_keypair.q))
			else:
				print("q = 2 * r * p + 1 = 0x%x" % (rsa_keypair.q))
				print("r = 0x%x" % (r))

			print("phi(n) = 0x%x" % (rsa_keypair.phi_n))
			print("lambda(n) = 0x%x" % (rsa_keypair.lambda_n))
			print("phi(n) / lambda(n) = gcd(p - 1, q - 1) = %d" % (rsa_keypair.phi_n // rsa_keypair.lambda_n))
			gcd_n_phin = NumberTheory.gcd(rsa_keypair.n, rsa_keypair.phi_n)
			if gcd_n_phin == rsa_keypair.p:
				print("gcd(n, phi(n)) = p")
			else:
				print("gcd(n, phi(n)) = 0x%x" % (gcd_n_phin))
			if self._args.close_q:
				print("q - p = %d (%d bit)" % (diff, diff.bit_length()))
			print("n = 0x%x" % (rsa_keypair.n))
			print("d = 0x%x" % (rsa_keypair.d))
			print("e = 0x%x" % (rsa_keypair.e))

	def _select_q(self, p):
		if not self._args.close_q:
			while True:
				yield self._prime_db.get(bitlen = self._q_bitlen, primetype = self._primetype)
		else:
			q = p
			while True:
				q += 2 * random.randint(1, self._args.q_stepping)
				if NumberTheory.is_probable_prime(q):
					yield q
