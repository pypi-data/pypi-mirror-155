# pwnedpasswords tool

This code enables efficient querying of the [Pwned Passwords](https://haveibeenpwned.com/Passwords) database,
*without* connecting to an external web service. This is primarily a python port of [pwnedpass](https://github.com/tylerchr/pwnedpass).
This version uses the full 32 bit integer for each pwned count, and the searching code is written in python instead
of Go since I need to use it in a Flask web application.

This includes both a tool to convert the pwned passwords data dump txt file to a binary database format, and a library/CLI
program to query that database. You can install it using pip:

```
pip install pwnedpass
```

## Binary file conversion tool

*If you'd rather not go to the hassle of running this, you can download a copy of the .bin file
[off my site](https://watch.lambda.dance/~lambda/pwned-passwords-v8.bin).*

First download the latest Pwned Passwords SHA-1 file from here: <https://haveibeenpwned.com/Passwords>.
Pick the one that's ordered by hash.

```
$ 7z e -so pwned-passwords-sha1-ordered-by-hash-v8.7z pwned-passwords-sha1-ordered-by-hash-v8.txt | python -m pwnedpass.rewrite - pwned-passwords-v8.bin
Reserving space for the index segment...
Writing data segment...
Writing index segment...
OK
```

(If necessary, this procedure can be done from within python, using `pwnedpass.rewrite(in_file, out_file)`.)

The SHA-256 hash of the outputted file should be **0a6c80edf2b542bfa7a2d650c10228b5abc8aead69b6985e145ed3c7f30b1b63**.

## Testing the binary file

Assuming you did use v8 of the pwned passwords file, you can test the output file was generated correctly by
running `./test.py <path to the binary file>`.

## Search tool

The querying can be done via a CLI script or from within python code.

### CLI

```
$ pwnedpass pwned-passwords-v8.bin 9e7c97801cb4cce87b6c02f98291a6420e6400ad
10664
$ echo $?
2
$ pwnedpass pwned-passwords-v8.bin 4e0ff63499ff9931ec2980c6a71d63cab4f94f99
0
$ echo $?
0
$ pwnedpass pwned-passwords-v8.bin
Password: 
6753
```

Where `pwned-passwords-v8.bin` is the output of the rewrite tool.

* For compromised password hashes, output the number of times the password was compromised, and return an unsuccessful error code != 1.
* For non-compromised password hashes, output 0, and exit successfully.

### As a library

```
import hashlib
import pwnedpass

user_password = read_password_from_web_form()

with open('pwned-passwords-v8.bin', 'rb') as f:
	if count := pwnedpass.search(f, hashlib.sha1(user_password.encode()).digest()):
		return f'Please use a different password. This one has been compromised {count} times.'
	else:
		# DO NOT USE the sha1 digest in your user database. SHA1 should *only* be used for checking if it's compromised.
		hash = salt_and_hash_password(user_password)
		save_to_database(hash)
```

## License

BSD 3-clause, per the original. See LICENSE for details.
