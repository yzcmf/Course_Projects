import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 6666)
sock.bind(server_address)
sock.listen(1)

while True:
    connection, client_address = sock.accept()
    data = connection.recv(4096)
    print data
    connection.sendall(data)
