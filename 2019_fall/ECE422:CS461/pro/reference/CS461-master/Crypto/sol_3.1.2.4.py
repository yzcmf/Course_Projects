#!/usr/bin/python
import math
import sys
with open(sys.argv[1]) as f:
    file_content = f.read().strip()
    c = int(file_content,16)

with open(sys.argv[2]) as f:
    file_content = f.read().strip()
    d = int(file_content,16)

with open(sys.argv[3]) as f:
    file_content = f.read().strip()
    n = int(file_content,16)


answer = hex((c**d) % n).rstrip("L").lstrip("0x")
f = open(sys.argv[4],'w')
f.write(answer)
f.close()
