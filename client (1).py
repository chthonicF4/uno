import socket
import threading
import time

Host = str(input("ip: "))
Port = 65432
conection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
nick = str(input("nickname: "))
#connect to server or crash trying
def connect():
    try :
        conection.connect((Host,Port))
    except:
        print("cant connect, retrying..")
        time.sleep(1)
        connect()
    print("connected")
connect()

msg = nick.encode("utf-8")
conection.sendall(msg)

#send data to server
def msg_send() :
    time.sleep(0.2)
    while True :
        msg = str(input(""))
        msg = msg.encode("utf-8")
        conection.sendall(msg)

#revive mesages from server
def msg_recv():
    while True:
        data = conection.recv(1024)
        msg = data.decode("utf-8")

        print(msg)

send = threading.Thread(target=msg_send, args=())
recive = threading.Thread(target=msg_recv, args=())
send.start()
recive.start()

