import socket
import threading
import tkinter as tk

name = "Sophie"
msg_buf = []
msg = ""

"""
# 建立主視窗和 Frame
window = tk.Tk()
window.title('Chatroom')
window.geometry('800x600')
window.configure(background='white')

# 將元件分為 top/bottom 兩群並加入主視窗
top_frame = tk.Frame(window)
top_frame.pack()
bottom_frame = tk.Frame(window)
bottom_frame.pack(side=tk.BOTTOM)
"""
# 顯示聊天訊息 (using label)
"""
var = tk.StringVar()
chat_label = tk.Label(top_frame, textvariable=var, height=27, width=90, 
				 font=('Arial', 10), anchor=tk.NW, justify=tk.LEFT) # height: num of lines, width:字數
var.set(msg_buf)
chat_label.pack(side=tk.BOTTOM)
"""

# 顯示聊天訊息 (using listbox + scrollbar)
"""
scrollbar = tk.Scrollbar(top_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
 
listbox = tk.Listbox(top_frame, font=('Arial', 10), height=27, width=90, yscrollcommand=scrollbar.set)
listbox.insert(tk.END, msg_buf[0])
listbox.pack(side=tk.LEFT, fill=tk.BOTH)

scrollbar.config(command=listbox.yview)

btn_read = tk.Button(bottom_frame, height=1, width=10, text="送出", command=getMsgInput)
btn_read.pack(side=tk.BOTTOM)
msg_input_field = tk.Text(bottom_frame, height=5)
msg_input_field.pack(side=tk.BOTTOM)

window.bind('<Return>', getMsgInput)
window.mainloop()
"""

def recv(sock, addr):
	sock.sendto(name.encode('utf-8'), addr)
	while True:
		data = sock.recv(1024)
		print(data.decode('utf-8'))


def send(sock, addr):
	while True:
		string = btn_read.invoke()
		message = name + ' : ' + string
		print(message)
		sock.sendto(message.encode('utf-8'), addr)
		if string.lower() == 'exit':
			break

def main():
	skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	server = ('127.0.0.1', 9999)
	tread = threading.Thread(target=recv, args=(skt, server), daemon=True)
	#tsend = threading.Thread(target=send, args=(skt, server))
	tread.start()
	#tsend.start()
	#tsend.join()
	skt.close()

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

		self.btn_read = tk.Button(self.bottom_frame, height=1, width=10, text="送出", command=self.getMsgInput)
		self.msg_input_field = tk.Text(self.bottom_frame, height=5)
		self.setupUI()

	def setupUI(self):
		self.top_frame.pack()
		self.bottom_frame.pack(side=tk.BOTTOM)
		self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
		self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)
		self.btn_read.pack(side=tk.BOTTOM)
		self.msg_input_field.pack(side=tk.BOTTOM)

	# 建立 "送出" 訊息的按鈕 或按下 enter 即傳送
	def getMsgInput(self, event=None):
		global msg_buf, line_cnt
		text = self.msg_input_field.get(1.0, tk.END+"-1c")
		msg = name + ' : ' + text
		msg_buf.append(msg)
		self.listbox.see(tk.END) # auto scroll to the latest msg
		self.listbox.insert(tk.END, msg)
		self.msg_input_field.delete("1.0","end") # clear
		print(msg)
		return msg

if __name__ == '__main__':
	name = input('Enter Your name: ')
	msg_buf.append("---------- 哈囉！%s～歡迎來到聊天室！退出聊天室請輸入'EXIT'(不分大小寫) ----------" % name)
	main()
	window = tk.Tk()
	window.title('Chatroom')
	window.geometry('800x600')
	window.configure(background='white')
	chat = ChatRoom(window)
	window.bind('<Return>', chat.getMsgInput)
	window.mainloop()