#	x509sak - The X.509 Swiss Army Knife white-hat certificate toolkit
#	Copyright (C) 2018-2021 Johannes Bauer
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
import sys
import logging
import traceback
import x509sak
from x509sak.actions.ActionBuildChain import ActionBuildChain
from x509sak.actions.ActionGraphPool import ActionGraphPool
from x509sak.actions.ActionFindCert import ActionFindCert
from x509sak.actions.ActionCreateCA import ActionCreateCA
from x509sak.actions.ActionCreateCSR import ActionCreateCSR
from x509sak.actions.ActionSignCSR import ActionSignCSR
from x509sak.actions.ActionRevokeCRT import ActionRevokeCRT
from x509sak.actions.ActionCreateCRL import ActionCreateCRL
from x509sak.actions.ActionGenerateBrokenDSA import ActionGenerateBrokenDSA
from x509sak.actions.ActionGenerateBrokenRSA import ActionGenerateBrokenRSA
from x509sak.actions.ActionDumpKey import ActionDumpKey
from x509sak.actions.ActionExamineCert import ActionExamineCert
from x509sak.actions.ActionForgeCert import ActionForgeCert
from x509sak.actions.ActionScrape import ActionScrape
from x509sak.actions.ActionHashPart import ActionHashPart
from x509sak.actions.ActionTLSClient import ActionTLSClient
from x509sak.actions.ActionTLSParse import ActionTLSParse
from x509sak.actions.ActionDebug import ActionDebug
from x509sak.actions.ActionJudgementCode import ActionJudgementCode
try:
	from x509sak.actions.ActionTestcaseGen import ActionTestcaseGen
except ImportError:
	ActionTestcaseGen = None
from x509sak.CmdLineArgs import KeyValue
from x509sak.KeySpecification import KeySpecification
from x509sak.Exceptions import UserErrorException, InvisibleUserErrorException, CmdExecutionFailedException
from x509sak.SubprocessExecutor import SubprocessExecutor
from .FriendlyArgumentParser import baseint, baseint_unit
from .MultiCommand import MultiCommand

def main():

	_default_so_search_path = "/usr/local/lib:/usr/lib:/usr/lib/x86_64-linux-gnu:/usr/lib/x86_64-linux-gnu/openssl-1.0.2/engines:/usr/lib/x86_64-linux-gnu/engines-1.1"

	if "X509SAK_VERBOSE_EXECUTION" in os.environ:
		SubprocessExecutor.set_all_verbose()
	if "X509SAK_PAUSE_FAILED_EXECUTION" in os.environ:
		SubprocessExecutor.pause_after_failed_execution()
	if "X509SAK_PAUSE_BEFORE_EXECUTION" in os.environ:
		SubprocessExecutor.pause_before_execution()

	mc = MultiCommand(trailing_text = "version: x509sak v%s" % (x509sak.VERSION))

	def genparser(parser):
		parser.add_argument("-s", "--ca-source", metavar = "path", action = "append", default = [ ], help = "CA file (PEM format) or directory (containing .pem/.crt files) to include when building the chain. Can be specified multiple times to include multiple locations.")
		parser.add_argument("--inform", choices = [ "pem", "der" ], default = "pem", help = "Specifies input file format for certificate. Possible options are %(choices)s. Default is %(default)s.")
		parser.add_argument("--order-leaf-to-root", action = "store_true", help = "By default, certificates are ordered with the root CA first and intermediate certificates following up to the leaf. When this option is specified, the order is inverted and go from leaf certificate to root.")
		parser.add_argument("--allow-partial-chain", action = "store_true", help = "When building the certificate chain, a full chain must be found or the chain building fails. When this option is specified, also partial chain matches are permitted, i.e., not going up to a root CA. Note that this can have undesired side effects when no root certificates are found at all (the partial chain will then consist of only the leaf certificate itself).")
		parser.add_argument("--dont-trust-crtfile", action = "store_true", help = "When there's multiple certificates in the given crtfile in PEM format, they're by default all added to the truststore. With this option, only the leaf cert is taken from the crtfile and they're not added to the trusted pool.")
		parser.add_argument("--outform", choices = [ "rootonly", "intermediates", "fullchain", "all-except-root", "multifile", "pkcs12" ], default = "fullchain", help = "Specifies what to write into the output file. Possible options are %(choices)s. Default is %(default)s. When specifying multifile, a %%d format must be included in the filename to serve as a template; typical printf-style formatting can be used of course (e.g., %%02d).")
		parser.add_argument("--private-key", metavar = "filename", type = str, help = "When creating a PKCS#12 output file, this private key can also be included. By default, only the certificates are exported.")
		parser.add_argument("--pkcs12-legacy-crypto", action = "store_true", help = "Use crappy crypto to encrypt a PKCS#12 exported private key.")
		group = parser.add_mutually_exclusive_group()
		group.add_argument("--pkcs12-no-passphrase", action = "store_true", help = "Do not use any passphrase to protect the PKCS#12 private key.")
		group.add_argument("--pkcs12-passphrase-file", metavar = "filename", type = str, help = "Read the PKCS#12 passphrase from the first line of the given file. If omitted, by default a random passphrase will be generated and printed on stderr.")
		parser.add_argument("-o", "--outfile", metavar = "file", help = "Specifies the output filename. Defaults to stdout.")
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increase verbosity level. Can be specified multiple times.")
		parser.add_argument("crtfile", metavar = "crtfile", type = str, help = "Certificate that a chain shall be build for, in PEM format.")
	mc.register("buildchain", "Build a certificate chain", genparser, action = ActionBuildChain, aliases = [ "bc" ])

	def genparser(parser):
		parser.add_argument("-c", "--color-scheme", choices = sorted(list(ActionGraphPool.get_supported_colorschemes())), default = "expiration", help = "Color scheme to use when coloring the certificates. Can either color by expiration date, by certificate type (client/server/CA/...), key type (RSA/ECC/etc), signature type (used hash function) or overall security level. Defaults to %(default)s.")
		parser.add_argument("--abbreviate-to", metavar = "charcnt", type = int, default = 30, help = "Abbreviate each line to this amount of characters. Defaults to %(default)d characters.")
		parser.add_argument("-l", "--label", metavar = "text", default = [ ], action = "append", help = "Label that is printed in the certificate nodes. Can be given multiple times to specify multiple lines. Substitutions that are supported are %s. Defaults to %s." % (", ".join(sorted(ActionGraphPool.get_supported_substitutions())), [ line.replace("%", "%%") for line in ActionGraphPool.get_default_label() ]))
		parser.add_argument("-f", "--format", choices = [ "dot", "png", "ps", "pdf" ], default = None, help = "Specifies the output file format. Can be one of %(choices)s. When unspecified, the file extension out the output file is used to determine the file type.")
		parser.add_argument("-o", "--outfile", metavar = "file", required = True, help = "Specifies the output filename. Mandatory argument.")
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increase verbosity level. Can be specified multiple times.")
		parser.add_argument("crtsource", metavar = "crtsource", nargs = "+", type = str, help = "Certificate file (in PEM format) or directory (containting PEM-formatted .pem or .crt files) which should be included in the graph.")
	mc.register("graph", "Graph a certificate pool", genparser, action = ActionGraphPool)

	def genparser(parser):
		parser.add_argument("-h", "--hashval", metavar = "hash", type = str, help = "Find only certificates with a particular hash prefix.")
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increase verbosity level. Can be specified multiple times.")
		parser.add_argument("crtsource", metavar = "crtsource", nargs = "+", type = str, help = "Certificate file (in PEM format) or directory (containting PEM-formatted .pem or .crt files) which should be included in the search.")
	mc.register("findcrt", "Find a specific certificate", genparser, action = ActionFindCert)

	def genparser(parser):
		group = parser.add_mutually_exclusive_group()
		group.add_argument("-g", "--gen-keyspec", metavar = "keyspec", type = KeySpecification.from_cmdline_str, help = "Private key specification to generate. Examples are rsa:1024 or ecc:secp256r1. Defaults to ecc:secp384r1.")
		group.add_argument("-w", "--hardware-key", metavar = "pkcs11uri", type = str, help = "Use a hardware token which stores the private key. The parameter gives the pkcs11 URI, e.g., 'pkcs11:object=mykey;type=private'")
		parser.add_argument("--pkcs11-so-search", metavar = "path", type = str, default = _default_so_search_path, help = "Gives the path that will be searched for the \"dynamic\" and \"module\" shared objects. The \"dynamic\" shared object is libpkcs11.so, the \"module\" shared object can be changed by the --pkcs11-module option. The search path defaults to %(default)s.")
		parser.add_argument("--pkcs11-module", metavar = "sofile", type = str, default = "opensc-pkcs11.so", help = "Name of the \"module\" shared object when using PKCS#11 keys. Defaults to %(default)s.")
		parser.add_argument("-p", "--parent-ca", metavar = "capath", type = str, help = "Parent CA directory. If omitted, CA certificate will be self-signed.")
		parser.add_argument("-s", "--subject-dn", metavar = "subject", type = str, default = "/CN=Root CA", help = "CA subject distinguished name. Defaults to %(default)s.")
		parser.add_argument("-d", "--validity-days", metavar = "days", type = int, default = 365, help = "Number of days that the newly created CA will be valid for. Defaults to %(default)s days.")
		parser.add_argument("-h", "--hashfnc", metavar = "alg", type = str, default = "sha384", help = "Hash function to use for signing the CA certificate. Defaults to %(default)s.")
		parser.add_argument("--serial", metavar = "serial", type = baseint, help = "Serial number to use for root CA certificate. Randomized by default.")
		parser.add_argument("--allow-duplicate-subjects", action = "store_true", help = "By default, subject distinguished names of all valid certificates below one CA must be unique. This option allows the CA to have duplicate distinguished names for certificate subjects.")
		parser.add_argument("--extension", metavar = "key=value", type = KeyValue, action = "append", default = [ ], help = "Additional certificate X.509 extension to include on top of the default CA extensions. Can be specified multiple times.")
		parser.add_argument("-f", "--force", action = "store_true", help = "By default, the capath will not be overwritten if it already exists. When this option is specified the complete directory will be erased before creating the new CA.")
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increase verbosity level. Can be specified multiple times.")
		parser.add_argument("capath", metavar = "capath", type = str, help = "Directory to create the new CA in.")
	mc.register("createca", "Create a new certificate authority (CA)", genparser, aliases = [ "genca" ], action = ActionCreateCA)

	def genparser(parser):
		parser.add_argument("-g", "--gen-keyspec", metavar = "keyspec", type = KeySpecification.from_cmdline_str, help = "Private key specification to generate for the certificate or CSR when it doesn't exist. Examples are rsa:1024 or ecc:secp256r1.")
		parser.add_argument("-k", "--keytype", choices = [ "pem", "der", "hw" ], default = "pem", help = "Private key type. Can be any of %(choices)s. Defaults to %(default)s.")
		parser.add_argument("-s", "--subject-dn", metavar = "subject", type = str, default = "/CN=New Cert", help = "Certificate/CSR subject distinguished name. Defaults to %(default)s.")
		parser.add_argument("-d", "--validity-days", metavar = "days", type = int, default = 365, help = "When creating a certificate, number of days that the certificate will be valid for. Defaults to %(default)s days.")
		parser.add_argument("-h", "--hashfnc", metavar = "alg", type = str, default = None, help = "Hash function to use for signing when creating a certificate. Defaults to the default hash function specified in the CA config.")
		parser.add_argument("-t", "--template", choices = [ "rootca", "ca", "tls-server", "tls-client" ], help = "Template to use for determining X.509 certificate extensions. Can be one of %(choices)s. By default, no extensions are included except for SAN.")
		parser.add_argument("--san-dns", metavar = "FQDN", type = str, action = "append", default = [ ], help = "Subject Alternative DNS name to include in the certificate or CSR. Can be specified multiple times.")
		parser.add_argument("--san-ip", metavar = "IP", type = str, action = "append", default = [ ], help = "Subject Alternative IP address to include in the certificate or CSR. Can be specified multiple times.")
		parser.add_argument("--extension", metavar = "key=value", type = KeyValue, action = "append", default = [ ], help = "Additional certificate X.509 extension to include on top of the extensions in the template and by the SAN parameters. Can be specified multiple times.")
		parser.add_argument("-f", "--force", action = "store_true", help = "Overwrite the output file if it already exists.")
		parser.add_argument("-c", "--create-crt", metavar = "capath", help = "Instead of creating a certificate signing request, directly create a certificate instead. Needs to supply the CA path that should issue the certificate.")
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increase verbosity level. Can be specified multiple times.")
		parser.add_argument("key_filename", metavar = "in_key_filename", type = str, help = "Filename of the input private key or PKCS#11 URI (as specified in RFC7512 in case of a hardware key type.")
		parser.add_argument("out_filename", metavar = "out_filename", type = str, help = "Filename of the output certificate signing request or certificate.")
	mc.register("createcsr", "Create a new certificate signing request (CSR) or certificate", genparser, aliases = [ "gencsr", "createcrt", "gencrt" ], action = ActionCreateCSR)

	def genparser(parser):
		parser.add_argument("-s", "--subject-dn", metavar = "subject", type = str, help = "Certificate's subject distinguished name. Defaults to the subject given in the CSR.")
		parser.add_argument("-d", "--validity-days", metavar = "days", type = int, default = 365, help = "Number of days that the newly created certificate will be valid for. Defaults to %(default)s days.")
		parser.add_argument("-h", "--hashfnc", metavar = "alg", type = str, default = None, help = "Hash function to use for signing. Defaults to the default hash function specified in the CA config.")
		parser.add_argument("-t", "--template", choices = [ "rootca", "ca", "tls-server", "tls-client" ], help = "Template to use for determining X.509 certificate extensions. Can be one of %(choices)s. By default, no extensions are included except for SAN.")
		parser.add_argument("--san-dns", metavar = "FQDN", type = str, action = "append", default = [ ], help = "Subject Alternative DNS name to include in the certificate. Can be specified multiple times.")
		parser.add_argument("--san-ip", metavar = "IP", type = str, action = "append", default = [ ], help = "Subject Alternative IP address to include in the CRT. Can be specified multiple times.")
		parser.add_argument("--extension", metavar = "key=value", type = KeyValue, action = "append", default = [ ], help = "Additional certificate X.509 extension to include on top of the extensions in the template and by the SAN parameters. Can be specified multiple times.")
		parser.add_argument("-f", "--force", action = "store_true", help = "Overwrite the output certificate file if it already exists.")
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increase verbosity level. Can be specified multiple times.")
		parser.add_argument("capath", metavar = "capath", type = str, help = "Directory of the signing CA.")
		parser.add_argument("csr_filename", metavar = "in_csr_filename", type = str, help = "Filename of the input certificate signing request.")
		parser.add_argument("crt_filename", metavar = "out_crt_filename", type = str, help = "Filename of the output certificate.")
	mc.register("signcsr", "Make a certificate authority (CA) sign a certificate signing request (CSR) and output the certificate", genparser, action = ActionSignCSR)

	def genparser(parser):
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increase verbosity level. Can be specified multiple times.")
		parser.add_argument("capath", metavar = "capath", type = str, help = "CA which created the certificate.")
		parser.add_argument("crt_filename", metavar = "crt_filename", type = str, help = "Filename of the output certificate.")
	mc.register("revokecrt", "Revoke a specific certificate", genparser, action = ActionRevokeCRT)

	def genparser(parser):
		parser.add_argument("-d", "--validity-days", metavar = "days", type = int, default = 30, help = "Number of days until the CRLs 'nextUpdate' field will expire. Defaults to %(default)s days.")
		parser.add_argument("-h", "--hashfnc", metavar = "alg", type = str, default = "sha256", help = "Hash function to use for signing the CRL. Defaults to %(default)s.")
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increase verbosity level. Can be specified multiple times.")
		parser.add_argument("capath", metavar = "capath", type = str, help = "CA which should generate the CRL.")
		parser.add_argument("crl_filename", metavar = "crl_filename", type = str, help = "Filename of the output CRL.")
	mc.register("createcrl", "Generate a certificate revocation list (CRL)", genparser, action = ActionCreateCRL, aliases = [ "gencrl" ])

	def genparser(parser):
		parser.add_argument("-d", "--prime-db", metavar = "path", type = str, default = ".", help = "Prime database directory. Defaults to %(default)s and searches for files called primes_{bitlen}.txt in this directory.")
		parser.add_argument("-b", "--bitlen", metavar = "bits", type = int, default = 2048, help = "Bitlength of modulus. Defaults to %(default)d bits.")
		parser.add_argument("-e", "--public-exponent", metavar = "exp", type = baseint, default = 0x10001, help = "Public exponent e (or d in case --switch-e-d is specified) to use. Defaults to 0x%(default)x. Will be randomly chosen from 2..n-1 if set to -1.")
		parser.add_argument("--switch-e-d", action = "store_true", help = "Switch e with d when generating keypair.")
		parser.add_argument("--accept-unusable-key", action = "store_true", help = "Disregard integral checks, such as if gcd(e, phi(n)) == 1 before inverting e. Might lead to an unusable key or might fail altogether.")
		parser.add_argument("--carmichael-totient", action = "store_true", help = "By default, d is computed as the modular inverse of e to phi(n), the Euler Totient function. This computes d as the modular inverse of e to lambda(n), the Carmichael Totient function, instead.")
		parser.add_argument("--generator", metavar = "file", help = "When prime database is exhausted, will call the prime generator program as a subprocess to generate new primes. Otherwise, and the default behavior, is to fail.")
		group = parser.add_mutually_exclusive_group()
		group.add_argument("--gcd-n-phi-n", action = "store_true", help = "Generate a keypair in which gcd(n, phi(n)) != 1 by specially constructing the prime q. This will lead to a size disparity of p and q and requires 3-msb primes as input.")
		group.add_argument("--close-q", action = "store_true", help = "Use a value for q that is very close to the value of p so that search starting from sqrt(n) is computationally feasible to factor the modulus. Note that for this, the bitlength of the modulus must be evenly divisible by two.")
		parser.add_argument("--q-stepping", metavar = "int", type = baseint, default = 1, help = "When creating a close-q RSA keypair, q is chosen by taking p and incrementing it repeatedly by a random int from 2 to (2 * q-stepping). The larger q-stepping is therefore chosen, the further apart p and q will be. By default, q-stepping is the minimum value of %(default)d.")
		parser.add_argument("-o", "--outfile", metavar = "file", type = str, default = "broken_rsa.key", help = "Output filename. Defaults to %(default)s.")
		parser.add_argument("-f", "--force", action = "store_true", help = "Overwrite output file if it already exists instead of bailing out.")
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increase verbosity level. Can be specified multiple times.")
	mc.register("genbrokenrsa", "Generate broken RSA keys for use in penetration testing", genparser, action = ActionGenerateBrokenRSA)

	def genparser(parser):
		parser.add_argument("-d", "--prime-db", metavar = "path", type = str, default = ".", help = "Prime database directory. Defaults to %(default)s and searches for files called primes_{bitlen}.txt in this directory.")
		parser.add_argument("--generator", metavar = "file", help = "When prime database is exhausted, will call the prime generator program as a subprocess to generate new primes. Otherwise, and the default behavior, is to fail.")
		parser.add_argument("-o", "--outfile", metavar = "file", type = str, default = "broken_dsa.key", help = "Output filename. Defaults to %(default)s.")
		parser.add_argument("-f", "--force", action = "store_true", help = "Overwrite output file if it already exists instead of bailing out.")
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increase verbosity level. Can be specified multiple times.")
		parser.add_argument("L_bits", metavar = "L_bits", type = int, help = "Bitlength of the modulus p, also known as L.")
		parser.add_argument("N_bits", metavar = "N_bits", type = int, help = "Bitlength of q, also known as N.")
	mc.register("genbrokendsa", "Generate broken DSA parameters for use in penetration testing", genparser, action = ActionGenerateBrokenDSA)

	def genparser(parser):
		parser.add_argument("-t", "--key-type", choices = [ "rsa", "ecc", "eddsa" ], default = "rsa", help = "Type of private key to import. Can be one of %(choices)s, defaults to %(default)s. Disregarded for public keys and determined automatically.")
		parser.add_argument("-p", "--public-key", action = "store_true", help = "Input is a public key, not a private key.")
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increase verbosity level. Can be specified multiple times.")
		parser.add_argument("key_filename", metavar = "key_filename", type = str, help = "Filename of the input key file in PEM format.")
	mc.register("dumpkey", "Dump a key in text form", genparser, action = ActionDumpKey)

	def genparser(parser):
		parser.add_argument("-p", "--purpose", choices = [ "ca", "tls-server", "tls-client" ], action = "append", default = [ ], help = "Check if the certificate is fit for the given purpose. Can be any of %(choices)s, can be specified multiple times.")
		parser.add_argument("-n", "--server-name", metavar = "fqdn", type = str, help = "Check if the certificate is valid for the given hostname.")
		parser.add_argument("-f", "--out-format", choices = [ "ansitext", "text", "json" ], default = "ansitext", help = "Determine the output format. Can be one of %(choices)s, defaults to %(default)s.")
		parser.add_argument("-i", "--in-format", choices = [ "pemcrt", "dercrt", "json", "host" ], default = "pemcrt", help = "Specifies the type of file that is read in. Can be either certificate files in PEM or DER format, a pre-processed JSON output from a previous run or a hostname[:port] combination to query a TLS server directly (port defaults to 443 if omitted). Valid choices are %(choices)s, defaults to %(default)s.")
		parser.add_argument("-r", "--parent-certificate", metavar = "pemfile", type = str, help = "Specifies a parent CA certificate that is used to run additional checks against the certificate.")
		parser.add_argument("--no-automatic-host-check", action = "store_true", help = "By default, when the input format is a given hostname, the server name is assumed as well and the purpose is assumed to be a TLS server. When this option is specified, these automatic checks are omitted.")
		parser.add_argument("--fast-rsa", action = "store_true", help = "Skip some time-intensive number theoretical tests for RSA moduli in order to speed up checking. Less thorough, but much faster.")
		parser.add_argument("--include-raw-data", action = "store_true", help = "Add the raw data such as base64-encoded certificate and signatures into the result as well.")
		parser.add_argument("--pretty-json", action = "store_true", help = "Prettyfy any generated JSON output.")
		parser.add_argument("-o", "--output", metavar = "filename", help = "Specify the output file. Defaults to stdout.")
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increase verbosity level. Can be specified multiple times.")
		parser.add_argument("infiles", metavar = "filename/uri", type = str, nargs = "+", help = "Filename of the input certificate or certificates in PEM format.")
	mc.register("examinecert", "Examine an X.509 certificate", genparser, action = ActionExamineCert, aliases = [ "analyze" ])

	def genparser(parser):
		parser.add_argument("--key_template", metavar = "path", default = "forged_%02d.key", help = "Output template for key files. Should contain '%%d' to indicate element in chain. Defaults to '%(default)s'.")
		parser.add_argument("--cert_template", metavar = "path", default = "forged_%02d.crt", help = "Output template for certificate files. Should contain '%%d' to indicate element in chain. Defaults to '%(default)s'.")
		parser.add_argument("-r", "--recalculate-keyids", action = "store_true", help = "By default, Subject Key Identifier and Authority Key Identifier X.509 extensions are kept as-is in the forged certificates. Specifying this will recalculate the IDs to fit the forged keys.")
		parser.add_argument("-f", "--force", action = "store_true", help = "Overwrite key/certificate files.")
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increase verbosity level. Can be specified multiple times.")
		parser.add_argument("crt_filename", metavar = "crt_filename", type = str, help = "Filename of the input certificate or certificates PEM format.")
	mc.register("forgecert", "Forge an X.509 certificate", genparser, action = ActionForgeCert)

	def genparser(parser):
		parser.add_argument("--no-pem", action = "store_true", help = "Do not search for any PEM encoded blobs.")
		parser.add_argument("--no-der", action = "store_true", help = "Do not search for any DER encoded blobs.")
		parser.add_argument("-i", "--include-dertype", metavar = "class", action = "append", default = [ ], help = "Include the specified DER handler class in the search. Defaults to all known classes if omitted. Can be specified multiple times and must be one of %s." % (", ".join(sorted(ActionScrape.handler_classes))))
		parser.add_argument("-e", "--exclude-dertype", metavar = "class", action = "append", default = [ ], help = "Exclude the specified DER handler class in the search. Can be specified multiple times and must be one of %s." % (", ".join(sorted(ActionScrape.handler_classes))))
		parser.add_argument("--extract-nested", action = "store_true", help = "By default, fully overlapping blobs will not be extracted. For example, every X.509 certificate also contains a public key inside that would otherwise be found as well. When this option is given, any blobs are extracted regardless if they're fully contained in another blob or not.")
		parser.add_argument("--keep-original-der", action = "store_true", help = "When finding DER blobs, do not convert them to PEM format, but leave them as-is.")
		parser.add_argument("--allow-non-unique-blobs", action = "store_true", help = "For all matches, the SHA256 hash is used to determine if the data is unique and findings are by default only written to disk once. With this option, blobs that very likely are duplicates are written to disk for every occurrence.")
		parser.add_argument("--disable-der-sanity-checks", action = "store_true", help = "For DER serialization, not only is it checked that deserialization is possible, but additional checks are performed for some data types to ensure a low false-positive rate. For example, DSA signatures with short r/s pairs are discarded by default or implausible version numbers for EC keys. With this option, these sanity checks will be disabled and therefore structurally correct (but implausible) false-positives are also written.")
		parser.add_argument("--outmask", metavar = "mask", default = "scrape_%(offset)07x_%(type)s.%(ext)s", help = "Filename mask that's used for output. Defaults to %(default)s and can use printf-style substitutions offset, type and ext.")
		parser.add_argument("-w", "--write-json", metavar = "filename", type = str, help = "Write the stats with detailed information about matches into the given filename.")
		parser.add_argument("-o", "--outdir", metavar = "path", type = str, default = "scrape", help = "Output directory. Defaults to %(default)s.")
		parser.add_argument("-f", "--force", action = "store_true", help = "Overwrite key/certificate files and proceed even if outdir already exists.")
		parser.add_argument("-s", "--seek-offset", metavar = "offset", type = baseint_unit, default = "0", help = "Offset to seek into file. Supports hex/octal/binary prefixes and SI/binary SI (k, ki, M, Mi, etc.) suffixes. Defaults to %(default)s.")
		parser.add_argument("-l", "--analysis-length", metavar = "length", type = baseint_unit, default = None, help = "Amount of data to inspect at max. Supports hex/octal/binary prefixes and SI/binary SI (k, ki, M, Mi, etc.) suffixes. Defaults to everything until EOF is hit.")
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increase verbosity level. Can be specified multiple times.")
		parser.add_argument("filename", metavar = "filename", type = str, help = "File that should be scraped for certificates or keys.")
	mc.register("scrape", "Scrape input file for certificates, keys or signatures", genparser, action = ActionScrape)

	def genparser(parser):
		parser.add_argument("-h", "--hash-alg", metavar = "alg", choices = ActionHashPart.get_supported_hash_fncs() + [ "all" ], action = "append", default = [ ], help = "Hash function(s) that should be tried. Can be specified multiple times and defaults to all available hash functions. Can be any of %%(choices)s, but defaults to %s. Special value 'all' means all supported functions." % (", ".join(ActionHashPart.get_default_hash_fncs())))
		parser.add_argument("-o", "--seek-offset", metavar = "offset", type = baseint_unit, default = "0", help = "Offset to seek into file. Supports hex/octal/binary prefixes and SI/binary SI (k, ki, M, Mi, etc.) suffixes. Defaults to %(default)s.")
		parser.add_argument("--max-offset", metavar = "offset", type = baseint_unit, help = "Largest offset to consider. By default, this is end-of-file. Supports hex/octal/binary prefixes and SI/binary SI (k, ki, M, Mi, etc.) suffixes.")
		parser.add_argument("-a", "--variable-hash-length", metavar = "length", type = int, action = "append", default = [ ], help = "For hash functions which have a variable output length, try all of these hash lenghts. Length is given in bits and must be a multiple of 8. Can be supplied multiple times. Defaults to %s." % ((", ".join("%d" % (length) for length in ActionHashPart.get_default_variable_hash_lengths_bits()))))
		parser.add_argument("-l", "--analysis-length", metavar = "length", type = baseint_unit, default = None, help = "Amount of data to inspect at max. Supports hex/octal/binary prefixes and SI/binary SI (k, ki, M, Mi, etc.) suffixes. Defaults to everything until EOF is hit.")
		parser.add_argument("-s", "--search", metavar = "hexpattern", type = str, help = "Hexadecimal pattern that is expected in the hashing.")
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increase verbosity level. Can be specified multiple times.")
		parser.add_argument("filename", metavar = "filename", type = str, help = "File that should be hashed.")
	mc.register("hashpart", "Hash all substrings of a file and search for a particular hash value", genparser, action = ActionHashPart)

	def genparser(parser):
		parser.add_argument("-p", "--port", metavar = "port", default = 443, help = "Port to connect to. Defaults to %(default)d.")
		parser.add_argument("-s", "--starttls", choices = [ "smtp" ], help = "Perform a STARTTLS cleartext negotiation before sending TLS messages. Can be any of %(choices)s.")
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increase verbosity level. Can be specified multiple times.")
		parser.add_argument("servername", metavar = "filename", type = str, help = "Server name to connect to.")
	mc.register("tlsclient", "Act as a TLS client", genparser, action = ActionTLSClient, visible = False)

	def genparser(parser):
		parser.add_argument("-s", "--side", choices = [ "client", "server" ], default = "client", help = "Which side the messages are from, can be one of %(choices)s. Defaults to %(default)s.")
		parser.add_argument("-e", "--encoding", choices = [ "bin", "hex" ], default = "bin", help = "Encoding of the given file. Can be one of %(choices)s, defaults to %(default)s.")
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increase verbosity level. Can be specified multiple times.")
		parser.add_argument("filename", metavar = "filename", type = str, help = "Binary file that contains the data stream.")
	mc.register("tlsparse", "Parse previously sniffed TLS messages and dump them", genparser, action = ActionTLSParse, visible = False)

	def genparser(parser):
		parser.add_argument("--der", action = "store_true", help = "Read in certificate in DER format instead of PEM.")
		parser.add_argument("-n", "--no-interact", action = "store_true", help = "Do not enter interactive console mode. Useful if you only want to execute specific commands and immediately quit.")
		parser.add_argument("-e", "--execute", metavar = "command", action = "append", default = [ ], help = "Execute the given command on the console. Can be specified multiple times.")
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increase verbosity level. Can be specified multiple times.")
		parser.add_argument("crtfile", metavar = "filename", type = str, nargs = "*", help = "Certificate file that should be loaded in the console.")
	mc.register("debug", "Open an interactive Python console", genparser, aliases = [ "dbg" ], action = ActionDebug, visible = False)

	def genparser(parser):
		parser.add_argument("-a", "--action", choices = [ "list", "dump", "inherit" ], default = "list", help = "Specifies what information to print out, can be one of %(choices)s. Defaults to %(default)s.")
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increase verbosity level. Can be specified multiple times.")
	mc.register("judgementcode", "Show information about judgement codes", genparser, aliases = [ "jc" ], action = ActionJudgementCode, visible = False)

	if ActionTestcaseGen is not None:
		def genparser(parser):
			parser.add_argument("-l", "--list-parameters", action = "store_true", help = "List possible parameters and values from the template.")
			parser.add_argument("-n", "--no-pem", action = "store_true", help = "Do not generate PEM data, just print the asciider")
			parser.add_argument("-o", "--output-dir", metavar = "path", type = str, default = "gen_tcs", help = "Output directory to store testcases in. Defaults to %(default)s.")
			parser.add_argument("-p", "--parameter", metavar = "key=value", type = str, action = "append", default = [ ], help = "Give a key/value parameter.")
			parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increase verbosity level. Can be specified multiple times.")
			parser.add_argument("tcname", metavar = "basename", type = str, help = "Testcase name to render.")
		mc.register("testcasegen", "Generate testcase certificates", genparser, aliases = [ "gentc", "tcgen" ], action = ActionTestcaseGen, visible = False)

	try:
		mc.run(sys.argv[1:])
	except (UserErrorException, InvisibleUserErrorException) as e:
		if logging.root.level == logging.DEBUG:
			traceback.print_exc()
			print(file = sys.stderr)
		if isinstance(e, UserErrorException) or (logging.root.level == logging.DEBUG):
			print("%s: %s" % (e.__class__.__name__, str(e)), file = sys.stderr)
		else:
			print("Failure while processing this request: %s" % (e.__class__.__name__), file = sys.stderr)

		if isinstance(e, CmdExecutionFailedException):
			if len(e.execution_result.stderr) > 0:
				print("~" * 120)
				e.execution_result.dump()
		sys.exit(1)

if __name__ == "__main__":
	main()
