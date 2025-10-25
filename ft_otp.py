import argparse
from hashlib import sha1
import hmac

def storeKey(filePath):
	with open(filePath, "r") as file:
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

def main():
	parser = argparse.ArgumentParser(description='ft_otp - HOTP alghorithm')

	parser.add_argument('-g', '--gen',
						type=str,
						default=None,
						help='Receives as argument a hexadecimal key of at least 64 char-acters. The program stores this key safely in a file called ft_otp.key, which is encrypted'
					)

	parser.add_argument('-k', '--key',
						type=str,
						default='ft_otp.key',
						help='Generates a new temporary password based on the key given as argument and prints it on the standard output'
					)

	args=parser.parse_args()

	if args.gen:
		storeKey(args.gen)

if __name__ == "__main__":
	main()