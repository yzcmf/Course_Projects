#!/usr/bin/python
import sys

with open(sys.argv[2],'r') as f:
    key = f.read().strip()

key = list(key)
table = {}
for i in range(26):

    table[key[i]] = chr(65+i)
#print table

with open(sys.argv[1], 'r') as f:
    input_text = f.read().strip()

output = []
for i in input_text:
    if ord(i) > 90 or ord(i) < 65:
        output += i
        continue
    output += table[i]



with open(sys.argv[3], 'a+') as f:
    f.write("".join(output))
