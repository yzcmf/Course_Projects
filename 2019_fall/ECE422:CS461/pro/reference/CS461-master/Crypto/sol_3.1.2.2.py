#!/usr/bin/python

from Crypto.Cipher import AES
import sys

with open(sys.argv[2]) as f:
    key = f.read().strip()

with open(sys.argv[3]) as f:
    iv = f.read().strip()

with open(sys.argv[1]) as f:
    input_text = f.read().strip()

key = key.decode('hex')
iv = iv.decode('hex')
input_text = input_text.decode('hex')

aes = AES.new(key, AES.MODE_CBC, iv)

#output_msg = iv + aes.encrypt(input_text)
output_msg = aes.decrypt(input_text)

with open(sys.argv[4], 'a+') as f:
    f.write(output_msg)
