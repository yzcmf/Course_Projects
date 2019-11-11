#!/usr/bin/python

import dpkt
import os
import sys
import socket

#import pathlib
# pathlib to glob certain pattern in all file names under certain directory defined by the pathlib.glob()
# for string in pathlib.Path(".").glob(currentPattern)


if len(sys.argv)!=2:
	print "input should be 'python 4.2.2.py <filename>'"
	sys.exit(0)

# PATH  = '.'
# file_list = os.listdir(PATH)

# pattern  = ".pcap"
# files = []
# for string in file_list:
# 	if string.find(pattern) != -1:
# 		files.append(string)

# def find_srclist(srclist, param):
# 	src_idx = -1
# 	found = 0
# 	for i,j in enumerate(srclist):
# 		if j[0] == param:
# 			src_idx = i
# 			found = 1
# 	return found,src_idx

def find_srclistdata(srclist, param):
	src_idx = -1
	found = 0
	for i,j in enumerate(srclist):
		if j == param:
			src_idx = i
			found = 1
	return found,src_idx



file_name_pcap = sys.argv[1]
#fiel_name = os.path.join(PATH, files[0])
# file_name_txt = file_name_pcap[:file_name_pcap.find('.pcap')]


# cand_ip_addr = set()
# with open(file_name_txt, 'rb') as f:
# 	tmp = f.readline().strip()
# 	cand_ip_addr.add(tmp)

f = open(file_name_pcap, 'rb');

pkt_types = ["UDP", "TCP"]
pcap = dpkt.pcap.Reader(f)
list_src = []
list_srcdata = []
list_dst = []
list_dstdata = []
for timestamp, buf in pcap:
	try:
		eth = dpkt.ethernet.Ethernet(buf)
	except:
		continue
	try:
		ip = eth.data
		dst_ip_addr = socket.inet_ntoa(ip.dst)
		src_ip_addr = socket.inet_ntoa(ip.src)
	except:
		continue


	try:
		tcp = ip.data
	except:
		continue

#	print (type(tcp))

	if(type(tcp) is dpkt.tcp.TCP):
		syn_flag = ( tcp.flags & dpkt.tcp.TH_SYN ) != 0
		ack_flag = ( tcp.flags & dpkt.tcp.TH_ACK ) != 0
		fin_flag = ( tcp.flags & dpkt.tcp.TH_FIN ) != 0
		rst_flag = ( tcp.flags & dpkt.tcp.TH_RST ) != 0
		psh_flag = ( tcp.flags & dpkt.tcp.TH_PUSH) != 0
		urg_flag = ( tcp.flags & dpkt.tcp.TH_URG ) != 0
		ece_flag = ( tcp.flags & dpkt.tcp.TH_ECE ) != 0
		cwr_flag = ( tcp.flags & dpkt.tcp.TH_CWR ) != 0
		if(syn_flag == 1 and ack_flag == 0 and cwr_flag == 0 and ece_flag == 0 and urg_flag == 0 and rst_flag == 0 and fin_flag == 0):
			# found,idx = find_srclist(list_src,src_ip_addr)
			found,idx = find_srclistdata(list_src,src_ip_addr)
			if(found == 0):
				list_src.append(src_ip_addr)
				list_srcdata.append(1)
				list_dstdata.append(0)
				# list_src.append([src_ip_addr,dst_ip_addr])
				# list_dstdata.append([0,0])
				# list_srcdata.append([0,1])
			else:
				list_srcdata[idx] += 1
				# dfound,i = find_srclistdata(list_src[idx],dst_ip_addr)
				# if(dfound == 0):
					# list_src[idx].append(dst_ip_addr)
					# list_srcdata[idx].append(1)
					# list_dstdata[idx].append(0)
				# else:
					# list_srcdata[idx][i]+=1

		elif(syn_flag == 1 and ack_flag == 1 and cwr_flag == 0 and ece_flag == 0 and urg_flag == 0 and rst_flag == 0 and fin_flag == 0):
			# print(src_ip_addr)
			# found,idx = find_srclist(list_src,dst_ip_addr)
			found,idx = find_srclistdata(list_src,dst_ip_addr)
			if(found == 0):
				# print("error")
				list_src.append(dst_ip_addr)
				list_dstdata.append(1)
				list_srcdata.append(0)
			else:
				list_dstdata[idx] += 1
				# dfound,i = find_srclistdata(list_src[idx],src_ip_addr)
				# if(dfound == 0):
				# 	list_src[idx].append(dst_ip_addr)
				# 	list_dstdata[idx].append(1)
				# 	list_srcdata[idx].append(0)
				# else:
				# 	list_dstdata[idx][i]+=1

# list_result = []
# len_srclist = len(list_src)
# for i in range(len_srclist):
# 	len_dst = len(list_src[i])
# 	srcIp = list_src[i][0]
# 	for j in range(1,len_dst):
# 		dstIp = list_src[i][j]
# 		if(list_srcdata[i][j] > 3*list_dstdata[i][j]):
# 			list_result.append(srcIp)

list_result = []
len_srclist = len(list_src)
for i in range(len_srclist):
	if(list_srcdata[i] > 3*list_dstdata[i]):
		list_result.append(list_src[i])

for i,j in enumerate(list_result):
	print(j)


#print(len(list_result))
#print(list_result)
# print(list_srcdata)
# print(list_src)




f.close()
