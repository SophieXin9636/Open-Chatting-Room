import socket
import logging
import threading

"""
TCP File serverSocket
"""

HOST = "127.0.0.1"
PORT = 10000
NUM_OF_CLIENT = 10

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind((HOST, PORT))
serverSocket.listen(NUM_OF_CLIENT)
skt_list = []
skt_tread_map = {} # {address: thread info}
clientState = {}  # dict{address: login state}

print('TCP File Server ip: %s:%s' % (HOST, PORT))

def recv_file(sock, caddr):
    # recv name
    name = sock.recv(100).decode("utf-8")
    clientState[caddr] = 1
    print("<System notification> " + name + " has connected the file server.")

    # recv file
    while True:
        buf = bytearray()
        filename_msg = sock.recv(100).decode()
        if(filename_msg == "LOGOUTSIGNAL"):
            print("<System notification> " + name + " has left the chatting room.")
            clientState[caddr] = 0
            sock.close()
            break
        elif (filename_msg != ""):
            filename = filename_msg.split()[0]
            print("File: " + filename)

            filesize_msg = sock.recv(10).decode()
            if(filesize_msg != ""):
                filesize = int(filesize_msg)
                print("Size: " , filesize)

            if(filesize > 1024):
                indata = bytearray(sock.recv(1024))
                filesize -= 1024
                while filesize > 0:
                    buf += indata
                    indata = bytearray(sock.recv(1024))
                    filesize -= 1024
            else:
                indata = bytearray(sock.recv(1024))
                buf += indata
            fileInfo = [filename_msg, filesize_msg]
            boardcastFile(sock, name, fileInfo, buf)
            print("File Transfer Success!")

def boardcastFile(sock, name, fileInfo, buf):
    name = name + '\0'*(10-len(name))

    for c in skt_list:
        print(c)
        # User name (size 10)
        c.send(name.encode('utf-8'))
        # filename (size 100)
        c.send(fileInfo[0].encode('utf-8'))
        # filesize (size 10)
        c.send(fileInfo[1].encode('utf-8'))
        # file data
        c.send(bytes(buf))

def checkZombie():
    global clientState
    for caddr, state in clientState.items():
        if(state == 0):
            skt_tread_map[caddr].join()
            print("One thread hss closed")

def clientAccept():
    global clientState
    while True:
        cli_skt, caddr = serverSocket.accept()
        print('connected by ' + str(caddr))
        skt_list.append(cli_skt)
        tread = threading.Thread(target=recv_file, args=(cli_skt, caddr), daemon=True)
        skt_tread_map[caddr] = tread
        #tread_list.append(tread)
        tread.start()
        checkZombie()

if __name__ == '__main__':
    tAccept = threading.Thread(target=clientAccept, daemon=True)
    tAccept.start()
    # close thread
    #for t in tread_list:
    #    t.join()
    tAccept.join()
    serverSocket.close()