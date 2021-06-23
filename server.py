import socket
import logging
import requests
import demjson
from bs4 import BeautifulSoup

# functions#############################################################################
##global var
serverIp = "127.0.0.1"
serverPort = 10002
saddr = (serverIp, serverPort)
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverOnline = 0
clientInfo = {}  # dict{address:name}
msg = [None, None]

def server_online():
    global saddr
    global serverOnline
    global serverSocket
    '''UDP socket'''
    try:
        serverSocket.bind(saddr)
    except:
        logging.warning("UDP Server(%s:%s) online failed.", saddr[0], saddr[1])
        exit(1)

    logging.info("UDP Server(%s:%s) is online.", saddr[0], saddr[1])
    print("UDP Server(%s:%s) is online." % (saddr[0], saddr[1]))

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
    weather_key = ["天氣"]
    hotissue_key = ["熱門搜尋", "熱搜", "熱門搜索"]

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
        # chat bot
        elif (data in weather_key):
            bot_respond(1)
            bm = name + ": " + data + "\n" + "<System notification> " + msg[0]
        elif (data in hotissue_key):
            bot_respond(2)
            bm = name + ": " + data + "\n" + "<System notification> " + msg[1]
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

def bot_respond(cate):
    global msg
    print("Updating...",end='')
    if (cate == 1):
        # Today's weather
        r = requests.get('https://www.cwb.gov.tw/Data/js/Observe/Observe_Home.js?')
        time = r.text.split(" = '")[1].split("';")[0]
        whether_data = r.text.split(" = '")[1].split("';")[1].split("OBS = ")[1].split(";\n")[0]
        t = demjson.decode(whether_data)

        data = "更新時間: " + time
        for i in range(1, 14):
            if (i != 3 and i != 6 and i != 7):
                data += "\n" + t[i]['CountyName']['C'] + ": " + t[i]['Temperature']['C'] + "°C, " + t[i]['Weather'][
                    'C'] + ", 累積雨量: " + t[i]['Rain']['C']
        msg[0] = data
    elif (cate == 2):
        # Trending Searches
        g = requests.get("https://trends.google.com/trends/trendingsearches/daily/rss?geo=TW")
        soup = BeautifulSoup(g.text, 'html.parser')
        trend_list = soup.find_all("title")

        data = "熱門搜尋榜單"
        for i in range(1, 11):
            data += str.format("\nNo.%-2d %s" % (i, trend_list[i].string))
        msg[1] = data
    print("finish.")
#######################################################################################

if __name__ == '__main__':
    server_online()
