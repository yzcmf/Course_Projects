#!/usr/bin/python

import sys
from Crypto.Hash import SHA256

input_text1 = open(sys.argv[1]).read()
input_text2 = open(sys.argv[2]).read()

hs = SHA256.new()
hs.update(input_text1)
output_text1 = hs.digest()

hs = SHA256.new()
hs.update(input_text2)
output_text2 = hs.digest()

hamming_dist = 0
for i in range(len(output_text1)):

    if output_text1[i] != output_text2[i]:
        hamming_dist+= 1

with open(sys.argv[3], 'a+') as f:
    f.write(hex(hamming_dist))
# print hex(hamming_dist)
