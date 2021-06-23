import socket
import logging
import threading

"""
TCP File serverSocket
"""

HOST = "127.0.0.1"
PORT = 10001
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
        filename_msg = sock.recv(100).decode("utf-8")
        if(filename_msg == "LOGOUTSIGNAL"):
            print("<System notification> " + name + " has left the chatting room.")
            clientState[caddr] = 0
            sock.close()
            break
        elif (filename_msg != ""):
            try:
                filename = filename_msg.split('\0')[0]
                print("File: " + filename)

                filesize_msg = sock.recv(10).decode("utf-8")
                if(filesize_msg != ""):
                    filesize = int(filesize_msg)
                    print("Size: " , filesize)

                while(filesize > 1024):
                    indata = bytearray(sock.recv(1024))
                    filesize -= 1024
                    buf += indata
                else:
                    indata = bytearray(sock.recv(filesize))
                    buf += indata
                print("File is received successfully!")
                fileInfo = [filename_msg, filesize_msg]
                boardcastFile(sock, name, fileInfo, buf)
            except ValueError:
                print("Unicode convert problem.")

def boardcastFile(sock, name, fileInfo, buf):
    global  skt_list
    if (len(name) > 9):
        name = name[:10]
    else:
        name = name + '\0'*(10-len(name)) #padding
    for c in skt_list:
        try:
            # User name (size 10)
            c.send(name.encode('utf-8')[:10])
            # filename (size 100)
            c.send(fileInfo[0].encode('utf-8'))
            # filesize (size 10)
            c.send(fileInfo[1].encode('utf-8'))
            # file data
            c.send(buf)
        except OSError:
            continue
    print("File has been boradcast!")

def checkZombie():
    global clientState
    for caddr, state in clientState.items():
        if(state == 0):
            skt_tread_map[caddr].join()
            # remove
            del clientState[caddr]
            del skt_tread_map[caddr]
            print("One thread has closed")
            break

def clientAccept():
    global clientState
    while True:
        cli_skt, caddr = serverSocket.accept()
        print('connected by ' + str(caddr))
        skt_list.append(cli_skt)
        tread = threading.Thread(target=recv_file, args=(cli_skt, caddr), daemon=True)
        skt_tread_map[caddr] = tread
        tread.start()
        checkZombie()

if __name__ == '__main__':
    tAccept = threading.Thread(target=clientAccept, daemon=True)
    tAccept.start()
    tAccept.join()
    serverSocket.close()
