#!/usr/bin/env python3

# SPDX-License-Identifier: BSD-3-Clause

import sys
from pathlib import Path

from pwnedpass import search

if not __debug__:
	print('This program requires assertions enabled.', file=sys.stderr)
	sys.exit(1)

def assert_eq(x, y):
	assert x == y, (x, y)

if len(sys.argv) != 2:
	print('Usage:', sys.argv[0], '<path to pwned passwords binary file>', file=sys.stderr)
	sys.exit(1)

here = Path(__file__).parent

with open(sys.argv[1], 'rb') as db_file:
	with open(here / 'test-cases.txt', 'r') as test_cases:
		next(test_cases)  # skip header line
		for line in test_cases:
			hash, _, count = line.partition(':')
			hash = bytes.fromhex(hash)
			count = int(count)
			assert_eq(search(db_file, hash), count)

	import hashlib

	h = hashlib.sha1(b'this is a really long string that is hopefully not in the pwned passwords file').digest()
	assert search(db_file, h) == 0, 'expected string to not appear in the file'

	try:
		search(db_file, b'f')
	except ValueError:
		pass
	else:
		raise AssertionError('searching for an invalid hash did not raise ValueError')
