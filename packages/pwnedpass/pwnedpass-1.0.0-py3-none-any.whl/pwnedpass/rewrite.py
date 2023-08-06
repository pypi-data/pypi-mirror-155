#!/usr/bin/env python3

# SPDX-License-Identifier: BSD-3-Clause

import io
import sys
import shutil
import typing

from .constants import *

def rewrite(in_file: typing.TextIO, out_file: typing.BinaryIO):
	header = io.BytesIO()
	data_pointer = 0
	current_header = bytearray(INDEX_PREFIX_SIZE)

	# "zero out" the index segment
	out_file.seek(INDEX_SEGMENT_SIZE)

	print('Writing data segment...')

	for line in in_file:
		# hex requires double the bytes
		hash = bytes.fromhex(line[:HASH_SIZE * 2])
		# skip the ':' after the hash
		count = int(line[HASH_SIZE * 2 + 1:])

		if data_pointer == 0 or current_header != hash[:INDEX_PREFIX_SIZE]:
			current_header[:] = hash[:INDEX_PREFIX_SIZE]
			header.write(data_pointer.to_bytes(INDEX_POINTER_SIZE, byteorder='big'))

		data_pointer += out_file.write(hash[INDEX_PREFIX_SIZE:])
		data_pointer += out_file.write(count.to_bytes(COUNT_SIZE, byteorder='big'))

	out_file.flush()

	header_len = len(header.getbuffer())
	if header_len != INDEX_SEGMENT_SIZE:
		raise RuntimeError(f'Header not of the expected size: {header_len:,}')

	out_file.seek(0)
	header.seek(0)

	print('Writing index segment...')

	shutil.copyfileobj(header, out_file)

	print('OK')

def main():
	out_file = 'pwned-passwords.bin'

	if len(sys.argv) == 1:
		in_file = sys.stdin
	else:
		if sys.argv[1] == '-':
			in_file = sys.stdin
		else:
			in_file = open(sys.argv[1])

		if len(sys.argv) == 3:
			out_file = sys.argv[2]

	with in_file, open(out_file, 'wb') as out_file:
		rewrite(in_file, out_file)

if __name__ == '__main__':
	main()
