import socket
import logging
import threading

"""
TCP File Server
"""

HOST = "127.0.0.1"
PORT = 10000
NUM_OF_CLIENT = 10

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(NUM_OF_CLIENT)
tread_list = []

print('TCP file server ip: %s:%s' % (HOST, PORT))

def recv_file(sock, addr):
	while True:
		buf = ""
		filename = sock.recv(100).decode().split()[0]
		if(filename.lower() == "exit"):
			break
		filesize = int(sock.recv(10).decode())

		indata = sock.recv(1024)
		while indata:
			buf += indata.decode()
			indata = sock.recv(1024)
		sock.send(buf)

while True:
    cli_skt, addr = server.accept()
    print('connected by ' + str(addr))
    tread = threading.Thread(target=recv_file, args=(cli_skt, addr), daemon=True)
    tread_list.append(tread)
    tread.start()
    tread.join()