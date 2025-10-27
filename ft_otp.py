import argparse
from hashlib import sha1
import hmac
import os
import struct

def initCounterFile(filePath: str):
	if not os.path.exists(filePath):
		with open('.count', "wt") as countFile:
			countFile.write("-1")

def storeKey(filePath: str):
	with open(filePath, "rt") as file:
		key = file.read()
		key = key.lower()
		if key.endswith('\n'):
			key = key[:-1]
		if (not key.isalnum() or len(key) != 64):
			print(f"error: key must be 64 hexadecimal characters.")
			return False
		with open("ft_otp.key", "w") as keyfile:
			keyfile.write(key)
			return True

def dt(mac):
	hdig = mac.hexdigest()
	offset = int(hdig[-1], 16)
	p = hdig[offset * 2 : offset * 2 + 8]
	return int(p, 16) & 0x7fffffff

def genkey(file):
	initCounterFile('.count')
	with open('.count', "r") as countFile:
		tmp: int = int(countFile.read().strip())
		tmp += 1
		countFile.seek(0)
	with open('.count', "w") as countFile:
		countFile.write(str(tmp))
	s = dt(hmac.new(file.read(), struct.pack(">Q", tmp), sha1))
	print(f"{"{:06}".format(s % 10 ** 6)}")
	


def main():
	parser = argparse.ArgumentParser(description='ft_otp - HOTP alghorithm')

	parser.add_argument('-g', '--gen',
						type=str,
						default=None,
						help='Receives as argument a hexadecimal key of at least 64 char-acters. The program stores this key safely in a file called ft_otp.key, which is encrypted'
					)

	parser.add_argument('-t', '--totp',
						type=str,
						default=None,
						help='Generates a new temporary password based on the key given as argument and the TOTP algorithm. Prints it on the standard output'
					)

	parser.add_argument('-k', '--key',
						type=str,
						default=None,
						help='Generates a new temporary password based on the key given as argument and the HOTP algorithm. Prints it on the standard output'
					)

	args=parser.parse_args()

	if args.gen:
		storeKey(args.gen)
	elif (args.key):
		with open(args.key, "rb") as file:
			genkey(file)

if __name__ == "__main__":
	main()