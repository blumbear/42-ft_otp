import argparse
from hashlib import sha1
import hmac
import os
import struct
import time
import qrcode
from PIL import Image

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

def hotpSeedHandler(file):
	with open('.count', "r") as countFile:
		tmp: int = int(countFile.read().strip())
		tmp += 1
		countFile.seek(0)
	with open('.count', "w") as countFile:
		countFile.write(str(tmp))
	return (genkey(file, tmp))

def totpSeedHandler(file):
	tmp = time.time()
	return (genkey(file, int(tmp)))

def genkey(file, seed):
	s = dt(hmac.new(file.read(), struct.pack(">Q", seed), sha1))
	res = "{:06}".format(s % 10 ** 6)
	print(f"{res}")
	return (res)
	

def genQrCode(otp):
	img = qrcode.make(str(otp))
	type(img)
	img.show()

def main():
	parser = argparse.ArgumentParser(description='ft_otp - HOTP and TOTP alghorithm')

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

	parser.add_argument('-q', '--qr-code',
						action="store_true",
						help='Generates a QR code with the otp code in it.'
					)

	args=parser.parse_args()
	if args.gen:
		storeKey(args.gen)
	elif (args.key):
		with open(args.key, "rb") as file:
			initCounterFile('.count')
			res = hotpSeedHandler(file)
	elif (args.totp):
		with open(args.totp, "rb") as file:
			initCounterFile('.count')
			res = totpSeedHandler(file)
	if (args.qr_code == True and (args.key or args.totp)):
		genQrCode(res)

if __name__ == "__main__":
	main()