import urllib2

url_base  =  "http://72.36.89.198:9999/mp3/xchen138/?"
url_base = "http://72.36.89.198:9999/mp3/xy21/?"

zz ="http://72.36.89.198:9999/mp3/xchen138/?eee5ccb829f7e1487dab2bf01b3596963f5fda48fa90a961e899c284c227f15be77107c76693f4e9fe7a0bb94d018249a1815d61013b39f3587e00fc58b3c9a0c94542e710e46ed81c8dc81965d773f4834895c1fabf3fe27770216ba224863894449d91e3a23169ed326028c4c14f50"

cipher_original_hex = "eee5ccb829f7e1487dab2bf01b3596963f5fda48fa90a961e899c284c227f15be77107c76693f4e9fe7a0bb94d018249a1815d61013b39f3587e00fc58b3c9a0c94542e710e46ed81c8dc81965d773f4834895c1fabf3fe27770216ba224862494449d91e3a23169ed326028c4c14f50";
cipher_original =  cipher_original_hex.decode('hex')


PAD_ERROR = 500
PAD_SUCCESS = 404

with open('3.2.3_ciphertext.hex', 'rb') as f:
    cipher_original_hex = f.read()


WORDS_IN_BLOCK = 16
BLOCK_TOTAL = (len(cipher_original_hex)/2) / WORDS_IN_BLOCK
# 112/16 = 7


pad_end_char = '\x10'
pad_end_int = 16

iv = cipher_original_hex[0: 1 * WORDS_IN_BLOCK * 2]
iv = iv.decode('hex')

def getStatus(u):
    req = urllib2.Request(u)
    try:
        f = urllib2.urlopen(req)
        return f.code
    except urllib2.HTTPError,e:
        return e.code

# Pad the message to a multiple of 16 bytes
def pad(msg):
    n = len(msg)%16
    return msg + ''.join(chr(i) for i in range(16,n,-1))

def helper(input, id, current_pos_int_set):
    # current_index = 12; lastbyte + \x151413
    rst = []
    # print "current index starts from: " + str(id + 1)
    # print "helper input id: " + str(id)

    if id == WORDS_IN_BLOCK - 1:
        return ""
    for index  in range(id + 1, WORDS_IN_BLOCK):
            # if id == 15:
            #     rst.append(bin((WORDS_IN_BLOCK - (index - id)) ^ current_pos_int_set[index])[2:])
            # index = 15, id = 14, 16 - (15-14)
            # 15 ^
            tmp_hex = hex((WORDS_IN_BLOCK - (index - id)) ^ current_pos_int_set[index]^ input[index])[2:]
            if(len(tmp_hex) % 2 != 0):
                tmp_hex = '0' + tmp_hex
            rst.append(tmp_hex)


    return "".join(rst)

def block_hack(block_index):

    # block index = 5 - > 0
    url_prefix_hex = cipher_original_hex[0: block_index * WORDS_IN_BLOCK * 2]
    current_cipher_block_hex = cipher_original_hex[block_index * WORDS_IN_BLOCK * 2:(block_index+1) * WORDS_IN_BLOCK * 2]
    next_cipher_block_hex = cipher_original_hex[(block_index+1) * WORDS_IN_BLOCK * 2:(block_index+2) * WORDS_IN_BLOCK * 2]
    current_cipher_block_char = current_cipher_block_hex.decode('hex')
    recovered_message = [""] *  WORDS_IN_BLOCK # in hex
    recovered_message_int = [""] * WORDS_IN_BLOCK # in int
    current_pos_int_set = [ord(current_cipher_block_char[i]) for i in range(WORDS_IN_BLOCK)]

    for current_index in range(WORDS_IN_BLOCK-1, -1, -1):
        # current_index 15 -- > 0
        # current_index = 15


        # // pad_end_int = /x10 when current_index = 15

        for guess_end in range(256):
            # // g --> match the real byte
            help_result = helper(recovered_message_int, current_index, current_pos_int_set)
            last_byte_xor = hex(current_pos_int_set[current_index]^guess_end^16)[2:]
            if len(last_byte_xor) < 2:
                last_byte_xor = "0" + last_byte_xor
            if guess_end < 16:
                guess_end_char = "0" + hex(guess_end)[2:]
            else:
                guess_end_char = hex(guess_end)[2:]
            guess_com_hex = last_byte_xor + help_result

            # print str(len(guess_com_hex)) + "   " +  str(len(next_cipher_block_hex))
            # print "helper: " + str(help_result) + "    index:  " + str(current_index) + "  guess com hex:" + str(guess_com_hex) + "     len of guess_com_hex: " + str(len(guess_com_hex)) + "   block  num:  " + str(block_index)
            current_rst = getStatus(url_base + url_prefix_hex + current_cipher_block_hex[:-(WORDS_IN_BLOCK - current_index) * 2] +guess_com_hex + next_cipher_block_hex)
            # print str(len(url_prefix_hex[:-2*(16-current_index)] + guess_com_hex + next_cipher_block_hex))
            # str

            # print str(current_rst) + "    " + str(guess_end)
            # string

            if current_rst != PAD_ERROR:

                recovered_message_int[current_index] = guess_end
                print str(recovered_message_int[current_index]) + "   index = " + str(current_index)
                recovered_message[current_index] = guess_end_char
                print str(guess_com_hex)
                print "last byte should be: " + str(guess_end) + "and the hex number of this is" + guess_end_char
                print "for block_number: " + str(block_index) + "  for index in current block: " + str(current_index)
                break
    print str(block_index) + "th block finished"
    return recovered_message, recovered_message_int;


block_number = BLOCK_TOTAL - 2

# [] of [], which contains block of decrypted msg
result = []
result_int = []

for n in range(block_number, -1, -1):
    # //use 0 - 5 to get rst
    ls, ls_int  = block_hack(n)
    result.insert(0, ("".join(ls)).decode('hex'))
    result_int.insert(0, ls_int)
    print "this is the " + str(n) +  "th decrypted message: " + result[0]
    print str(len(result[0])) + "--> len"
    print result_int

rst = "".join(result)

# ls = block_hack(5)
# result.insert(0, ("".join(ls)).decode('hex'))
# print "this is the " + str(5) +  "th decrypted message: " + result[0]


with open('vv', 'wb') as f:
    # for n in rae(block_number, -1, -1):
    #     f.write(result[block_number])
    f.write(rst)
# with open('output_int.txt', 'a+') as f:
#     for n in range(block_number, -1, -1):
#         f.write(result_int[block_number])
print "finished"
