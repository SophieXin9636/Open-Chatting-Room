import socket
import logging

# functions#############################################################################
##global var
serverIp = "127.0.0.1"
serverPort = 9999
saddr = (serverIp, serverPort)
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverOnline = 0
clientInfo = {}  # dict{address:name}

def server_online():
    global saddr
    global serverOnline
    global serverSocket
    '''UDP socket'''
    try:
        serverSocket.bind(saddr)
    except:
        logging.warning("UDP Server(%s:%s) online failed.", saddr[0], saddr[1])

    logging.info("UDP Server(%s:%s) online succeeded.", saddr[0], saddr[1])
    print("UDP Server(%s:%s) online succeeded." % (saddr[0], saddr[1]))

    serverOnline = 1
    while (serverOnline):
        try:
            boardcast_message=server_running()
            print(boardcast_message)
        except:
            logging.info("UDP Server(%s:%s) runtime failed.",saddr[0],saddr[1])

def server_running():
    global serverSocket
    global serverOnline
    global clientInfo

    data, caddr = serverSocket.recvfrom(1024)
    data = data.decode("utf-8")

    if (caddr not in clientInfo):
        '''login phase: data->name'''
        name = data
        clientInfo[caddr] = name
        bm = "<System notification> " + name + " has entered the chatting room."
    else:
        '''chatting phase: data->msg'''
        name = clientInfo[caddr]
        # logout: exit
        if (data == "LOGOUTSIGNAL"):
            clientInfo.pop(caddr)
            bm = "<System notification> " + name + " has left the chatting room."
        # normal case
        else:
            bm = name + ": " + data
    boardcasting(bm, caddr)
    return bm

def boardcasting(msg, source):
    global serverSocket
    global saddr
    global clientInfo
    for address in clientInfo:
        serverSocket.sendto(msg.encode("utf-8"), address)

#######################################################################################

if __name__ == '__main__':
    server_online()