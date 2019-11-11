#!/usr/bin/python
import sys

#def class WHA:
#    def __init__(self, MASK):


def WHA(inStr):
    new_inStr = []
    MASK = 0x3fffffff
    outhash = 0

    for Byte in inStr:
        byte = ord(Byte)
        intermediate_value = ((byte ^ 0xcc) << 24) | ((byte ^ 0x33) << 16) | ((byte ^ 0xaa) << 8) | ((byte ^ 0x55))
        outhash = (outhash & MASK) + (intermediate_value & MASK)

    return outhash


output = hex(WHA(open(sys.argv[1],'r').read().strip()))
with open(sys.argv[2], 'a+') as f:
    f.write(output)
