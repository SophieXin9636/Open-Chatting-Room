# NAP Final project

Python - GUI Programming (Tkinter)
* [教學文件](https://www.tutorialspoint.com/python/python_gui_programming.htm)
* [參考](https://www.itbook5.com/2019/02/10638/#ttk-widgets)

## 目前問題
> [time=6.22 14:43]
傳送圖片之後，圖片會將對話輸入框給覆蓋掉

## 待完成
* 傳送圖片之後顯示在聊天室上 (貼圖)
* 貼圖素材


## chatroom
https://shengyu7697.github.io/python-chatroom/
https://shengyu7697.github.io/python-tcp-socket/
https://iter01.com/562533.html

## tkinter widget
Button, Checkbutton, Entry, Frame,Label, LabelFrame, Menubutton, PanedWindow,Radiobutton, Scale, Scrollbar, Spinbox, Combobox, Notebook,Progressbar, Separator, Sizegrip, Treeview
* Tk(): 建立主視窗
* Frame(): 建立 Frame
* Text(): 新增文字輸入框
	* https://www.delftstack.com/zh-tw/howto/python-tkinter/how-to-get-the-input-from-tkinter-text-box/
* Button(): 新建按鈕
* Label(): 訊息框
	* https://www.tutorialspoint.com/python/tk_label.htm
* Scrollbar(): 滾輪
* Listbox(): 列表，若超出邊界會搭配滾輪
	* https://www.tutorialspoint.com/python/tk_listbox.htm
* PanedWindow():
	* https://www.twblogs.net/a/5ca0b67dbd9eee5b1a069ea6

## 架構 (Architecture)
本專案使用的是 Client-Server 架構，有多個 client 端與兩個 Server 端，兩個 Server 各司其職，一個為 TCP Server，一個為 UDP Server。

### Client
* interaction flow, window is cleared before entering next phase
	* login
	* chatting
	* logout
		client's logout action: click logout button, input of "exit" is no longer used
* message
	* message time: display only once whenever receiving time is different from last message's different font color of different kind of messages
	* time: gray
	* normal message: black
	* system message: blue
	* input message class: Entry (used to be Text)

### TCP Server: File System
* 負責傳收檔案 (Undone)
* 傳送貼圖 (TODO)
* 傳送音訊 (TODO)


### UDP Server
* 負責傳收、廣播訊息
* 天氣現況
* 熱門搜尋 (排名前十)

