#!/home/anaconda2/bin/python

from fractions import gcd
import numpy as np
import math
import Crypto.Util.number as number
from Crypto.PublicKey import RSA
from pbp import decrypt
import Crypto

def product(X):
    if len(X) == 0: return 1
    while len(X) > 1:
        temp = []
        l = len(X)
        for i in range((l+1)/2):
            sum = 1
            for j in range(i*2,(i+1)*2):
                if(l > j):
                    sum = sum*X[j]
            temp.append(sum)
        X = temp
    return X[0]

def producttree(X):
       result = [X]
       while len(X) > 1:
           temp = []
           l = len(X)
           for i in range((l+1)/2):
               sum = 1
               for j in range(i*2,(i+1)*2):
                   if(l > j):
                       sum = sum*X[j]
               temp.append(sum)
           X = temp
           result.append(X)
       return result

def remaindersusingproducttree(n,T):
       result = [n]
       for t in reversed(T):
         result = [result[(int)(math.floor(i/2))] % t[i] for i in range(len(t))]
       return result

def remainders(n,X):
       return remaindersusingproducttree(n,producttree(X))

def batchgcd_simple(X):
       R = remainders(product(X),[n**2 for n in X])
       return [gcd(r/n,n) for r,n in zip(R,X)]

def batchgcd_faster(X):
       prods = producttree(X)
       R = prods.pop()
       while prods:
         X = prods.pop()
         R = [R[(int)(math.floor(i/2))] % X[i]**2 for i in range(len(X))]
       return [gcd(r/n,n) for r,n in zip(R,X)]

def extended_gcd(aa, bb):
    lastremainder, remainder = abs(aa), abs(bb)
    x, lastx, y, lasty = 0, 1, 1, 0
    while remainder:
        lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
        x, lastx = lastx - quotient*x, x
        y, lasty = lasty - quotient*y, y
    return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)

def modinv(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
            raise ValueError
    return x % m


#print batchgcd_simple([1909,2923,291,205,989,62,451,1943,1079,2419])
filename = "3.2.4_ciphertext.enc.asc"
with open(filename) as f:
    ciphertext = f.read()

# strip_list = [x.strip() for x in cipher_list]

# text_list = strip_list[1:-1]

# ciphertext = ''.join(x for x in text_list)

e = 65537L
hexfile = "moduli.hex"
with open(hexfile) as f:
    content = f.readlines()

mod_list = []
hex_list = [x.strip() for x in content]
temp_list = [x.decode('hex') for x in hex_list]
for i in range(len(temp_list)):
    list = [ord(x) for x in temp_list[i]]
    sum = list[0]
    for j in range(1,len(list)):
        sum = sum * 256 + list[j]
    mod_list.append(sum)

# gcd_list = []
gcdSelf_list = []
modulus_list = []
remainder_list = batchgcd_simple(mod_list)


for i in range(len(remainder_list)):
    p = remainder_list[i]
    if p == 1:
            continue
    q = mod_list[i] / p
    try:
            d = modinv(e, (p-1)*(q-1))
    except ValueError:
            continue
    tup = (mod_list[i],e,d)
    key = RSA.construct(tup)
    try:
        plaintext = decrypt(key,ciphertext)
        print "Correct Key"
        print(plaintext)
        break
    except ValueError:
        print("exception")
        continue
#

# d_list = []
# for i in range(len(gcd_list)):
#     p = gcd_list[i]
#     q = modulus_list[i]/gcd_list[i]
#     m1 = (p-1)*(q-1)
#     temp = number.inverse(e,m1)
#     d_list.append(temp)
#
#

# while(len(gcdSelf_list) >0):
#     copy_list = []
#     for i in range(len(gcdSelf_list)):
#         for j in range(len(gcd_list)):
#             p = gcd_list[j]
#             q = gcdSelf_list[i]
#             if(not isinstance(q,float)):
#                 if(not gcd_list.contains(q)):
#                     gcd_list.append(q)
#                 m1 = (p-1)*(q-1)
#                 temp = number.inverse(e,m1)
#                 d_list.append(temp)
#                 modulus_list.append(p*q)
#                 break
#             else:
#                 if(j == len(gcd_list)):
#                     copy_list.append(gcdSelf_list[i])
#     gcdSelf_list = copy_list





# print(modulus_list)
#
# print("===============")
# print(d_list)
# print("===============")

# for i in range(len(d_list)):
#     try:
#         key = RSA.construct((modulus_list[i],e,d_list[i]))
#         print("========================================")
#         plaintext = decrypt(key,ciphertext)
#         print(plaintext)
#         print("========================================")
#         pass
#     except ValueError:
#         print("exception")
#         continue
