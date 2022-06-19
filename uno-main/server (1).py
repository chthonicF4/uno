import threading
import socket 
Host = socket.gethostname()
print("Host :",Host)
Port = 65432
max_clients = 1
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((Host,Port))

clients = []
nicknames = []

def brodcast(msg):
    msg = msg.encode("utf-8")
    for client in clients :
        client.send(msg)

def handle(name) :
    index = clients.index(name)
    brodcast(nicknames[index]+" joined")
    print("handle start for :",nicknames[index])
    data = ''
    while True :
        try :
            data = name.recv(1024)
        except :
            break
        if data == False :
            pass
        else :
            index = clients.index(name)
            data = data.decode("utf-8")
            msg = (nicknames[index],data)
            msg = ":".join(msg)
            print(msg)
            brodcast(msg)
            data = ''
    leave = nicknames[index] + " left"
    clients.remove(name)
    nicknames.pop(index)
    print(leave)
    brodcast(leave)

while True :
    server.listen(2)
    conn , addr = server.accept()
    print("connected by", addr)
    nick = conn.recv(1024)
    nick = nick.decode("utf-8")
    nicknames.append(nick)
    clients.append(conn)
    thread = threading.Thread(target=handle, args=(conn,))
    thread.start()
