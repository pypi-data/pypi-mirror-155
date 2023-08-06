#!/usr/bin/env python3

# SPDX-License-Identifier: BSD-3-Clause

import io
import typing

from .rewrite import rewrite
from .constants import *

def search(f: typing.BinaryIO, target_hash: bytes) -> int:
	if len(target_hash) != HASH_SIZE:
		raise ValueError(f'target_hash must be a valid sha1 hash, got {target_hash!r}')

	index_prefix = target_hash[:INDEX_PREFIX_SIZE]
	hash_rest = target_hash[INDEX_PREFIX_SIZE:]
	entries_loc, entries_size = _entries_location(f, index_prefix)

	f.seek(entries_loc)
	entries = memoryview(f.read(entries_size))

	for i in range(0, len(entries), ENTRY_SIZE):
		if hash_rest == entries[i:i+ENTRY_HASH_SIZE]:
			return int.from_bytes(entries[i+ENTRY_HASH_SIZE:i+ENTRY_HASH_SIZE+COUNT_SIZE], byteorder='big')
	return 0

def _entries_location(f, index_prefix: bytes) -> typing.Tuple[int, int]:
	"""returns the location and size of a block of entries, given a hash prefix"""
	index_loc = int.from_bytes(index_prefix, byteorder='big') * INDEX_POINTER_SIZE
	f.seek(index_loc)

	if index_prefix == b'\xff\xff\xff':
		# this is the last prefix, so the entries go until EOF
		first_loc = int.from_bytes(f.read(INDEX_POINTER_SIZE), byteorder='big') + INDEX_SEGMENT_SIZE
		size = -1  # when passed to read(), reads until EOF
	else:
		buf = f.read(INDEX_POINTER_SIZE * 2)
		first_loc = int.from_bytes(buf[:INDEX_POINTER_SIZE], byteorder='big') + INDEX_SEGMENT_SIZE
		second_loc = int.from_bytes(buf[INDEX_POINTER_SIZE:], byteorder='big') + INDEX_SEGMENT_SIZE
		size = second_loc - first_loc

	return first_loc, size
