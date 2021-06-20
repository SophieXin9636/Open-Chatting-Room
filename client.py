import socket
import threading

# functions#############################################################################
##global var
clientName = ""
loginFlag = 0
serverIp = "127.0.0.1"
serverPort = 9999
saddr = (serverIp, serverPort)

def client_online():
    global saddr
    '''UDP socket'''
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    '''thread creation'''
    tread = threading.Thread(target=recv, args=(clientSocket, saddr), daemon=True)
    twrite = threading.Thread(target=send, args=(clientSocket, saddr))

    tread.start()
    twrite.start()
    twrite.join()

    clientSocket.close()

def recv(sock, source):
    #一個UDP連線在接收訊息前必須要讓系統知道所佔埠->需要先send一次
    data = clientName.encode("utf-8")
    sock.sendto(data, source)
    while (1):
        data = sock.recv(1024)
        data = data.decode("utf-8")
        print(data)

def send(sock, dest):
    global loginFlag
    global clientName
    while (1):
        if (not loginFlag):
            loginFlag = 1
            print("Have a nice day, %s~" % clientName)
            continue
        else:
            instr = input("")
        data = instr.encode("utf-8")
        sock.sendto(data, dest)
        '''logout phase'''
        if (instr.lower() == "exit"):
            return 0

if __name__ == '__main__':
    clientName = input("Welcome to the chatroom, please enter your name first: ")
    client_online()