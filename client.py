import socket
import threading

def recv(sock, addr):
    '''
    一個UDP連線在接收訊息前必須要讓系統知道所佔埠
    也就是需要send一次，否則win下會報錯
    '''
    sock.sendto(name.encode('utf-8'), addr)
    while True:
        data = sock.recv(1024)
        print(data.decode('utf-8'))


def send(sock, addr):
    '''
        傳送資料的方法
        引數：
            sock：定義一個例項化socket物件
            server：傳遞的伺服器IP和埠
    '''
    while True:
        string = input('')
        message = name + ' : ' + string
        sock.sendto(message.encode('utf-8'), addr)
        if string.lower() == 'exit':
            break

def main():
    skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = ('127.0.0.1', 9999)
    tread = threading.Thread(target=recv, args=(skt, server), daemon=True)
    tsend = threading.Thread(target=send, args=(skt, server))
    tread.start()
    tsend.start()
    tsend.join()
    skt.close()

if __name__ == '__main__':
    print("-----歡迎來到聊天室,退出聊天室請輸入'EXIT(不分大小寫)'-----")
    name = input('Enter Your name: ')
    print('-----------------%s------------------' % name)
    main()