import socket
import logging
import requests
import demjson
from bs4 import BeautifulSoup

# functions#############################################################################
##global var
serverIp = "127.0.0.1"
serverPort = 9999
saddr = (serverIp, serverPort)
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverOnline = 0
clientInfo = {}  # dict{address:name}
msg = {"天氣":"", "熱門搜尋":""}

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
    global msg

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
        elif data == "天氣" or data == "熱門搜尋":
            bm = name + ": " + data + "\n" + msg[data]
            print(bm)
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

def init():
    global msg

    # Today's weather
    r = requests.get('https://www.cwb.gov.tw/Data/js/Observe/Observe_Home.js?')
    time = r.text.split(" = '")[1].split("';")[0]
    whether_data = r.text.split(" = '")[1].split("';")[1].split("OBS = ")[1].split(";\n")[0]
    t = demjson.decode(whether_data)

    data = "更新時間: " + time
    for i in range(1, 14):
        if(i != 3 and i != 6 and i != 7):
            data += "\n地區: " + t[i]['CountyName']['C'] +", 溫度: " + t[i]['Temperature']['C'] +", 天氣: " + t[i]['Weather']['C'] +", 累積雨量: " + t[i]['Rain']['C']
    msg["天氣"] = data

    # Trending Searches
    g = requests.get("https://trends.google.com/trends/trendingsearches/daily/rss?geo=TW")
    soup = BeautifulSoup(g.text, 'html.parser')
    trend_list = soup.find_all("title")

    data = "熱門搜尋: "
    for i in range(1, 11):
        data += "\nNo." + str(i) + " " + trend_list[i].string
    msg["熱門搜尋"] = data
#######################################################################################

if __name__ == '__main__':
    init()
    server_online()
