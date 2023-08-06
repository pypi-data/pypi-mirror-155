from . import search

def main():
	import sys

	if len(sys.argv) == 1:
		print('Usage:', sys.argv[0], '<pwned passwords database file>', '[sha1 hash as hex]', file=sys.stderr)
		print('If the hash is omitted, read a password from stdin.', file=sys.stderr)
		sys.exit(1)

	if len(sys.argv) < 3:
		from hashlib import sha1
		from getpass import getpass

		target_hash = sha1(getpass().encode()).digest()
	else:
		target_hash = bytes.fromhex(sys.argv[2])

	with open(sys.argv[1], 'rb') as f:
		count = search(f, target_hash)
		print(count)
		if count:
			sys.exit(2)
		else:
			sys.exit(0)

if __name__ == '__main__':
	main()
