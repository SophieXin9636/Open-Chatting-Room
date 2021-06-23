import socket
import threading
import time
from os import listdir, remove
from tkinter import Tk, Frame, Label, Button, Text, Entry, Scrollbar, PhotoImage, Listbox, StringVar
from tkinter import BOTTOM, TOP, LEFT, RIGHT, END, Y, BOTH, WORD, INSERT
from tkinter.font import Font as tkfont
from tkinter.font import BOLD, ITALIC
from tkinter.filedialog import askdirectory, askopenfilename
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk, ImageFile
from functools import partial
from playsound import playsound
ImageFile.LOAD_TRUNCATED_IMAGES = True

# tk window basic setting: title and size###############################################
loginoutsize = "400x160"
chatroomsize = "800x650"
window = Tk()
window.title("Chatroom")
window.geometry(loginoutsize)
#######################################################################################

# functions#############################################################################
##global var
clientName = StringVar()
input_msg = StringVar()
msg_buf = []
listitemcounter = 0
currenttime = None
# UDP, TCP socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverIp = "127.0.0.1"
udpServerPort = 10002
tcpServerPort = 10001
saddr = (serverIp, udpServerPort)
taddr = (serverIp, tcpServerPort)
# login flag
loginFlag = 0

def client_online(event=None):
    global saddr
    global clientName
    global txt_getName, entry_getName, button_getName

    '''unpack login widgets'''
    txt_getName.pack_forget()
    entry_getName.pack_forget()
    button_getName.pack_forget()
    window.unbind_all('<Return>')

    '''pack chatting room widgets & bind <enter> to <sendMsg>'''
    window.geometry(chatroomsize)
    chat = ChatRoom(window)
    window.bind("<Return>", chat.getMsgInput)

    '''thread creation'''
    tread = threading.Thread(target=chat.recvMsg, args=(clientSocket, saddr), daemon=True)
    treadFile = threading.Thread(target=chat.recvFile, daemon=True)
    tread.start()
    treadFile.start()


def gettime():
    curtime = str(time.ctime(time.time()+25200)).split(" ")
    return " [" + curtime[1] + " " + curtime[2] + " " + curtime[3][:-3] + "] "


def seticon(iconpath):
    iconsize = (40, 40)
    return PhotoImage(Image.open(iconpath).resize(iconsize, Image.NEAREST).convert("RGBA"))


class ChatRoom():
    def __init__(self, parent):
        global font_btn, font_content
        global clientName, msg_buf
        # window = top + middle(2 parts) + bottom
        self.top_frame = Frame(parent)
        self.middle_frame = Frame(parent, height=10)
        self.middle_p1 = Frame(self.middle_frame)
        self.middle_p2 = Frame(self.middle_frame)
        self.bottom_frame = Frame(parent)

        # icon
        iconsize = (40, 40)
        icon_slfile = PhotoImage(file="img/selectfile.png").subsample(30, 30)

        # emoji
        self.emj_file = listdir("emoji")
        emj_list = []
        for emj in self.emj_file:
            emj_list.append(PhotoImage(file=r"emoji/"+emj).subsample(3, 3))

        # top: 顯示聊天訊息(listbox & scrollbar)
        '''
        self.scrollbar = Scrollbar(self.top_frame)
        self.listbox = Listbox(self.top_frame, yscrollcommand=self.scrollbar.set,
                               height=20, width=90, font=font_content, bg="#FFFFFF")
        self.scrollbar.config(command=self.listbox.yview)
        '''
        self.chatbox=ScrolledText(self.top_frame,wrap=WORD,
                                  height=25, width=90, font=font_content, bg="#FFFFFF")
        self.chatbox.tag_config("time", foreground="#AAAAAA")
        self.chatbox.tag_config("usr_sp_act", foreground="#B833FF")
        self.chatbox.tag_config("system_noti", foreground="#0000CC")
        self.chatbox.tag_config("bot_wait", foreground="#AAAAAA")
        self.chatbox.tag_config('bot_respond', foreground="#FF338A")
        self.chatbox.tag_config('error', foreground="#FF0000")
        self.chatbox.images = []

        # middle: 選擇檔案/emoji
        self.button_slfile = Button(self.middle_p1, image=icon_slfile, borderwidth=0,
                                    command=self.browsefile)
        self.button_slfile.image = icon_slfile
        self.button_list_emoji = []

        for index, img in enumerate(emj_list):
            btn = Button(self.middle_p2, image=img, borderwidth=0,
                         command=partial(self.sendEmj, index))
            btn.image = img
            self.button_list_emoji.append(btn)

        # bottom: 傳送聊天訊息或登出
        cN = clientName.get()
        cNlen = len(cN)
        if (cNlen > 8):
            cN = cN[:8] + "..."
        self.txt_sendbox = Label(self.bottom_frame, text=cN + ":", font=font_content)
        self.entry_sendbox = Entry(self.bottom_frame, width=60, font=font_content, textvariable=input_msg)
        self.button_sendbox = Button(self.bottom_frame, text="Send", width=8, fg="#FFFFFF", bg="#5555CC", font=font_btn,
                                     command=self.getMsgInput)
        self.button_logout = Button(self.bottom_frame, text="Logout", width=8, fg="#FFFFFF", bg="#AAAAAA",
                                    font=font_btn,
                                    command=self.logout)

        # connect TCP Server
        self.file_srv_skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcpConnect()

        # pack widgets
        self.packUI()

    def tcpConnect(self):
        global taddr, loginFlag
        try:
            self.file_srv_skt.connect(taddr)
            self.file_srv_skt.send(clientName.get().encode('utf-8'))
        except ConnectionRefusedError:
            print("Connection failed! Please try again!(Error code: 2)")
            exit(1)
        loginFlag = 1

    def packUI(self):
        # frame
        self.top_frame.pack(side=TOP, pady=10)
        self.middle_frame.pack(side=TOP, pady=2)
        self.middle_p1.pack(side=TOP, pady=4)
        self.middle_p2.pack(side=BOTTOM, pady=2)
        self.bottom_frame.pack(side=BOTTOM, pady=10)

        # top
        '''
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.listbox.pack(side=LEFT, fill=BOTH, pady=5)
        '''
        self.chatbox.pack(side=TOP,pady=5)

        # middle
        self.button_slfile.pack(side=TOP, padx=2)
        for btn in self.button_list_emoji:
            btn.pack(side=LEFT,padx=2)

        # bottom
        self.txt_sendbox.pack(side=LEFT)
        self.entry_sendbox.pack(side=LEFT, padx=2)
        self.button_sendbox.pack(side=LEFT, padx=2)
        self.button_logout.pack(side=RIGHT, padx=2)

    def getMsgInput(self, event=None):
        global saddr
        global clientSocket
        global msg_buf, input_msg

        text = input_msg.get()
        bot_keyword = ["天氣", "熱門搜尋", "熱搜", "熱門搜索"]

        if (text != ""):
            clientSocket.sendto(text.encode('utf-8'), saddr)
            self.entry_sendbox.delete(0, "end")
            if (text in bot_keyword):
                self.chatbox.insert(END, "Please wait for a while for ["+text+"]...\n", "bot_wait")
        else:
            pass

    def recvMsg(self, sock, addr):
        global clientName, loginFlag
        global msg_buf, listitemcounter, currenttime
        # 一個UDP連線在接收訊息前必須要讓系統知道所佔埠->需要先send一次
        sock.sendto(clientName.get().encode("utf-8"), addr)

        while (1):
            try:
                msg = sock.recv(1024)
            except:
                if (loginFlag != 1):
                    print("Connection failed! Please try again!(Error code: 1)")
                    self.chatbox.insert(END, "Connection failed! Please exit and try again! (Error code: 1)\n", "error")
                exit(1)

            if (msg != ""):
                if (not currenttime or currenttime != gettime()):
                    currenttime = gettime()
                    '''
                    self.listbox.insert(END, currenttime)
                    self.listbox.itemconfig(END, {"fg": "#AAAAAA"})
                    listitemcounter += 1
                    '''
                    self.chatbox.insert(END,currenttime+"\n","time")
                msg = msg.decode("utf-8")
                msg_buf.append(msg)
                # bot respond
                if (msg.count('\n') > 1):
                    tmp = msg.split("\n")
                    for i, s in enumerate(tmp):
                        '''
                        self.listbox.insert(END, s)
                        if i == 0:
                            self.listbox.itemconfig(END, {"fg": "#B833FF"})
                        elif i == 1:
                            self.listbox.itemconfig(END, {"fg": "#0000CC"})
                        else:
                            self.listbox.itemconfig(END, {"fg": "#FF338A"})
                        listitemcounter += 1
                        '''
                        if i == 0:
                            self.chatbox.insert(END, s+"\n", "usr_sp_act")
                        elif i == 1:
                            self.chatbox.insert(END, s+"\n", "system_noti")
                        else:
                            self.chatbox.insert(END, s+"\n", "bot_respond")
                else:
                    '''
                    self.listbox.insert(END, msg)
                    if (msg[:21] == "<System notification>"):
                        self.listbox.itemconfig(END, {"fg": "#0000CC"})
                    listitemcounter += 1
                    self.listbox.see(END)
                    '''
                    # system boardcast(login/logout)
                    if (msg[:21] == "<System notification>"):
                        self.chatbox.insert(END, msg+"\n", "system_noti")
                    # normal msg
                    else:
                        self.chatbox.insert(END, msg+ "\n", "normal_talk")
                self.chatbox.see(END)

    def recvFile(self):
        global listitemcounter, currenttime
        while True:
            name = self.file_srv_skt.recv(10)
            if (name != ""):
                # [!!!]
                # this causes problem due to unexpected cut in unicode(if clientName is in Chinese, same problem with filename)
                name = name.decode("utf-8").split('\0')[0]
                try:
                    filename_msg = self.file_srv_skt.recv(100).decode("utf-8")
                except OSError:
                    print("Connection closed.")
                    exit(0)
                if (filename_msg != ""):
                    filename = filename_msg.split('\0')[0]
                    print("File:", filename)
                    f = open(filename, 'wb')

                    filesize_msg = self.file_srv_skt.recv(10).decode("utf-8")
                    if (filesize_msg != ""):
                        filesize = int(filesize_msg)
                        print("Size:", filesize)

                    while (filesize > 1024):
                        # print(filesize)
                        indata = self.file_srv_skt.recv(1024)
                        filesize -= 1024
                        f.write(indata)
                    else:
                        # print(filesize)
                        indata = self.file_srv_skt.recv(filesize)
                        f.write(indata)
                        f.close()
                    print("File received!")

                    emjFlag = int(self.file_srv_skt.recv(1).decode())

                    if (not currenttime or currenttime != gettime()):
                        currenttime = gettime()
                        '''
                        self.listbox.insert(END, currenttime)
                        self.listbox.itemconfig(END, {"fg": "#AAAAAA"})
                        listitemcounter += 1
                        '''
                        self.chatbox.insert(END, currenttime + "\n", "time")
                        self.chatbox.tag_config("time", foreground="#AAAAAA")

                    filetype = filename.split('.')[-1]
                    pictype = ["png", "jpg", "tiff", "gif", "bmp"]
                    soundtype = ["mp3", "wav", "m4a"]
                    if (filetype.lower() in pictype):
                        '''display if it's a picture'''
                        msg = name + ": shared a picture <" + filename + ">"
                        '''
                        try:
                            self.txt_picfilename.pack_forget()
                            self.pic_fromfile.pack_forget()
                        except:
                            pass
                        rd_fromfile = ImageTk.PhotoImage(Image.open(filename).resize((120, 120), Image.BILINEAR))
                        self.txt_picfilename = Label(self.middle_frame, text=filename, font=font_content, fg="#BBBBBB")
                        self.pic_fromfile = Label(self.middle_frame, image=rd_fromfile, width=116, height=116)
                        self.txt_picfilename.pack(side=LEFT)
                        self.pic_fromfile.pack(side=LEFT,pady=15)
                        '''
                        if (not emjFlag):
                            self.chatbox.insert(END, msg + "\n", "usr_sp_act")
                        else:
                            self.chatbox.insert(END, name + ": ")
                        rd_fromfile = ImageTk.PhotoImage(Image.open(filename).resize((120, 120), Image.BILINEAR))
                        self.chatbox.image_create(END, padx=5, pady=5, image=rd_fromfile)
                        self.chatbox.images.append(rd_fromfile)
                        self.chatbox.insert(END, "\n", "usr_sp_act")
                        self.chatbox.see(END)
                        if (emjFlag):
                            remove(filename)


                    elif (filetype.lower() in soundtype):
                        ''' play music if it's a sound file '''
                        msg = name + ": is playing music <" + filename + ">"
                        self.chatbox.insert(END, msg + "\n", "usr_sp_act")
                        self.chatbox.see(END)
                        playsound(filename)
                    else:
                        msg = name + ": shared a file <" + filename + ">"
                        self.chatbox.insert(END, msg + "\n", "usr_sp_act")
                        self.chatbox.see(END)
                    '''
                    self.listbox.insert(END, msg)
                    self.listbox.itemconfig(END, {"fg": "#B833FF"})
                    listitemcounter += 1
                    self.listbox.see(END)
                    if (filetype.lower() in soundtype):
                        playsound(filename)
                    '''
    def browsefile(self):
        # get file path and name (return empty tuple if not select)
        filename = askopenfilename()
        window.update()
        if (filename != () and filename != ""):
            self.sendFile(filename)

    def sendFile(self, filepath, emjFlag=0):
        # filename (max string size is 100)
        filename = filepath[::-1].split("/")[0][::-1]  # complete path -> only filename

        if (len(filename) > 99):
            filename_msg = filename[:100]
        else:
            filename_msg = filename + (100 - len(filename)) * '\0'  # padding
        self.file_srv_skt.send(filename_msg.encode('utf-8')[:100])
        print("File: " + filename_msg)

        # filesize (max string size is 10)
        f = open(filepath, "rb")
        buf = f.read()  # data type: bytes
        file_size = len(buf)
        file_size_msg = "0" * (10 - len(str(file_size))) + str(file_size)
        self.file_srv_skt.send(file_size_msg.encode('utf-8'))
        print("Size:",file_size)

        # file data
        self.file_srv_skt.send(buf)
        print("File sent!")
        f.close()

        # emoji flag
        self.file_srv_skt.send(str(emjFlag).encode())

    def sendEmj(self, i):
        target_path=r"emoji/"+self.emj_file[i]
        self.sendFile(target_path, 1)

    def logout(self):
        global window
        global clientName, clientSocket
        '''send termination signal'''
        clientSocket.sendto("LOGOUTSIGNAL".encode('utf-8'), saddr)
        self.file_srv_skt.send("LOGOUTSIGNAL".encode('utf-8'))

        '''unpack chatting room widgets'''
        self.top_frame.pack_forget()
        self.middle_frame.pack_forget()
        self.bottom_frame.pack_forget()
        clientSocket.close()
        self.file_srv_skt.close()

        '''pack logout widgets'''
        txt_logout.config(text="Logout successfully.\n\nGoodbye, " + clientName.get() + "!")
        txt_logout.pack(side=TOP, pady=15)
        window.geometry(loginoutsize)


#######################################################################################

# label / button########################################################################
##font
font_btn = tkfont(family="微軟正黑體", size=10, weight=BOLD)
font_content = tkfont(family="微軟正黑體", size=10)
font_cr = tkfont(family="Times", size=8, slant=ITALIC)
##login/logout phase
txt_getName = Label(window, text="Please enter your name", font=font_content)
entry_getName = Entry(window, width=30, font=font_content, textvariable=clientName)
button_getName = Button(window, text="Login!", width=8, fg="#FFFFFF", bg="#5555CC", font=font_btn,
                        command=client_online)
txt_logout = Label(window, text="", font=font_content)
##copyright
txt_copyright = Label(window, text="® SophieXin & KaielHsu 2021", font=font_cr)
#######################################################################################

# pack / place##########################################################################
##login
txt_getName.pack(side=TOP, pady=15)
entry_getName.pack(side=TOP, pady=5)
button_getName.pack(side=TOP, pady=10)
window.bind("<Return>", client_online)
##copyright
txt_copyright.pack(side=BOTTOM)
#######################################################################################

# window looping########################################################################
if __name__ == '__main__':
    window.mainloop()
