import socket
import sys
import struct
import numpy as np

def read_data():
    txt = ''
    with open('dataset1.csv','r') as f:
        txt += f.read()

    return txt

def read_test_data():
    flag = 1
    with open('testset1.csv','r') as f:
        x = []
        y = []
        for i in f:
            if flag == 1:
                flag = 0
                continue
            else:
                tmp1 = []
                tmp = i.split(',')
                tmp1 += [float(tmp[0])]
                tmp1 += [float(tmp[1])]
                tmp1 += [float(tmp[2])]
                tmp1 += [float(tmp[3])]
                y += [float(tmp[4])]
                x.append(tmp1)

        return x,y



def connection(datasheet):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('seclab-enclave-3.cs.illinois.edu', 10055)
    sock.connect(server_address)
    sock.sendall(datasheet)

    data = []

    while True:
        tmp = sock.recv(64)
        return struct.unpack('<dddd',tmp)



if __name__ == "__main__":
    datasheet = read_data()
    weights = connection(datasheet)
    x,y = read_test_data()
    x = np.array(x)
    y = np.array(y)
    weights = np.array([weights[0],weights[1],weights[2],weights[3]])

    predicts = 1.0 / (1.0+np.exp(-x.dot(weights)))

    for i in range(len(predicts)):
        if predicts[i] > 0.5:
            predicts[i] = 1.0
        else:
            predicts[i] = 0.0

    acc = np.count_nonzero(predicts == y)
    print acc
    print acc*100/len(y)
