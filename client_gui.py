import socket
import threading
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

size = "800x800"
chat = None
window = None
clientSocket = None
clientName = "Sophie"
msg_buf = []
msg = ""
loginFlag = 0
saddr = ("127.0.0.1", 9999)

def main():
	global window, size, chat
	window = tk.Tk()
	window.title('Chatroom')
	window.geometry(size)
	window.configure(background='white')
	chat = ChatRoom(window)
	window.bind('<Return>', chat.getMsgInput)
	client_online()

def client_online():
	global saddr, window, chat, clientSocket
	'''UDP socket'''
	clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	'''thread creation'''
	tread = threading.Thread(target=chat.recv, args=(clientSocket, saddr), daemon=True)
	#twrite = threading.Thread(target=chat.send, args=(clientSocket, saddr))
	tread.start()
	#twrite.start()
	window.mainloop()
	#twrite.join()
	clientSocket.close()

class ChatRoom():
	def __init__(self, parent):
		# 將元件分為 top/bottom 兩群並加入主視窗
		self.top_frame = tk.Frame(parent)
		self.bottom_frame = tk.Frame(parent)

		# 顯示聊天訊息 (using listbox + scrollbar)
		self.scrollbar = tk.Scrollbar(self.top_frame)
		self.listbox = tk.Listbox(self.top_frame, font=('Arial', 10), height=27, width=90, yscrollcommand=self.scrollbar.set)
		self.listbox.insert(tk.END, msg_buf[0])
		self.scrollbar.config(command=self.listbox.yview)

		# button
		self.btn_read = tk.Button(self.bottom_frame, height=1, width=10, text="送出", command=self.getMsgInput)
		
		### ToDo: it doesn't work ###
		file_icon = tk.PhotoImage(file='img/files.png')#.subsample(4, 4)
		#img = Image.open("img/files.png")
		#file_icon = ImageTk.PhotoImage(img)
		#self.btn_select_file = tk.Button(self.bottom_frame, image=file_icon, command=self.clickSelectFile)
		self.btn_select_file = tk.Button(self.bottom_frame, height=1, width=10, text="選擇檔案", command=self.clickSelectFile)

		self.msg_input_field = tk.Text(self.bottom_frame, height=5)
		self.setupUI()

	def setupUI(self):
		self.top_frame.pack()
		self.bottom_frame.pack(side=tk.BOTTOM)
		self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
		self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)
		self.btn_read.pack(side=tk.BOTTOM)
		self.msg_input_field.pack(side=tk.BOTTOM)
		self.btn_select_file.pack(side=tk.BOTTOM)

	# 建立 "送出" 訊息的按鈕 或按下 enter 即傳送
	def getMsgInput(self, event=None):
		global msg_buf, clientName, clientSocket, saddr

		if(event == None):
			text = self.msg_input_field.get(1.0, tk.END+"-1c")
		else:
			text = self.msg_input_field.get(1.0, tk.END+"-2c")
		
		if(text != ""):
			msg = clientName + ' : ' + text
			msg_buf.append(msg)
			self.listbox.see(tk.END) # auto scroll to the latest msg
			#self.listbox.insert(tk.END, msg)
			self.msg_input_field.delete("1.0","end") # clear
			clientSocket.sendto(text.encode('utf-8'), saddr)
			return msg
		else:
			return ""


	def recv(self, sock, addr):
		global clientName
		sock.sendto(clientName.encode('utf-8'), addr)
		while True:
			msg = sock.recv(1024)
			if(msg != ""):
				msg_buf.append(msg)
				self.listbox.see(tk.END) # auto scroll to the latest msg
				self.listbox.insert(tk.END, msg.decode('utf-8'))
				pass
				#print(data.decode('utf-8'))

	def clickSelectFile(self):
		filename = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(("jpeg files","*.jpg"),("all files","*.*")))
		print(filename)

	"""
	def send(self, sock, addr):
		global loginFlag, clientName
		while True:
			string = self.btn_read.invoke()
			#print(len(string), string, sep=".")
			if(string != ""):
				message = clientName + ' : ' + string
				print(message)
				sock.sendto(message.encode('utf-8'), addr)
				'''logout phase'''
				if string.lower() == 'exit':
					break
	"""

if __name__ == '__main__':
	clientName = input("Welcome to the chatroom, please enter your name first: ")
	msg_buf.append("---------- 哈囉！%s～歡迎來到聊天室！退出聊天室請輸入'EXIT'(不分大小寫) ----------" % clientName)
	main()