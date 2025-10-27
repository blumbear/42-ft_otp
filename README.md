# ft_otp

A simple HOTP (HMAC-based One-Time Password) and TOTP (Time-based One-Time Password) implementation in Python.

## Description

This program implements the HOTP algorithm to generate time-based one-time passwords. It can store hexadecimal keys securely and generate temporary passwords based on those keys.

## Initialisation
### Create virtual environment
python3 -m venv venv

### Activate virtual environment
### On Linux/Mac:
source venv/bin/activate
### On Windows:
venv\Scripts\activate

### Install required packages
pip install qrcode[pil] PyPNG

## Usage

### Store a key
```bash
python3 ft_otp.py -g key_file.txt
```
This reads a 64-character hexadecimal key from `key_file.txt` and stores it in `ft_otp.key`.

### Generate a password
```bash
python3 ft_otp.py -k ft_otp.key
```
This generates a temporary password using the stored key.

## Requirements

- Python 3.x
- Key must be exactly 64 hexadecimal characters
- Key file should contain only the hexadecimal string

## Example

```bash
# Generate a random key
openssl rand -hex 32 > my_key.txt

# Store the key
python3 ft_otp.py -g my_key.txt

# Generate password
python3 ft_otp.py -k ft_otp.key
```

## Arguments

- `-g, --gen`: Store a hexadecimal key from file
- `-k, --key`: Generate password from key file (default: ft_otp.key)
