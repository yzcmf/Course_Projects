# encoding= utf-8
import functools
import operator
import re
import csv
import emoji
def is_emoji(s): return s in UNICODE_EMOJI

filename = "Query Results.csv" # testing: [0] + [4766:7149]; training: [:4765]
fields = []
rows = []
with open(filename, 'r') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile)
    # extracting field names through first row
    fields = csvreader.next()
    # extracting each data row one by one
    for row in csvreader:
        rows.append(row)
    print("Total no. of rows: %d" % (csvreader.line_num))
print('Field names are: ' + ', '.join(field for field in fields))

new_data = set()
for row in rows:
    # emojis_str = unicode(row[0], 'utf-8')
    emojis_str = row[0].decode('utf-8')

    emojis_list = [emojis_str[i:i + 4] for i in range(0, len(emojis_str), 4)]
    # print 'emojis_list=%s' % emojis_list
    for em in emojis_list:
        # print 'emoji: %s' % em
        # print(em)
        if is_emoji(em) and len(em) == 2:
            new_data.add(tuple([em.encode('utf-8')] + row[1:]))

    em_split_emoji = emoji.get_emoji_regexp().split(emojis_str)
    em_split_whitespace = [substr.split() for substr in em_split_emoji]
    em_split = functools.reduce(operator.concat, em_split_whitespace)
    for separated in em_split:
        # print(separated)
        if is_emoji(separated) and len(separated) == 2:
            # print len(separated)
            new_data.add(tuple([separated.encode('utf-8')] + row[1:]))


# print len(new_data)
new_data = [fields] + list(new_data)
# for row in new_data[1::]:
    # print row[0]
print(len(new_data))

# f = open('Query_Normalized_Results.csv', 'w')
# for r in new_data:
#         f.writelines(str(r) + '\n')
# f.close()

f = open('Query_Normalized_Results_With_emoji_out.csv', 'w')
for r in new_data:
        # print r[0]
        # f.writelines(r[0] + str(r[1:]) + '\n')
        line = ""
        for c in r:
            line += c
            if c != r[-1]:
                line += ","
        f.writelines(line + '\n')
f.close()