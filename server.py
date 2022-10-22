import socket
from threading import Thread

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #sockstream is for tcp, INET is for ipv4
ip_Address = "127.0.0.1"
port = 8000
server.bind((ip_Address, port))
server.listen()
clients = []
nicknames = []

print("Server has started and is ready to connect....")

def remove(connection, nickname):
    if connection in clients:
        clients.remove(connection) 
    if nickname in nicknames:
        nicknames.remove(nickname)
def broadcast(msgToSend, connection):
    for client in clients:
        if client != connection:
            try:
                client.send(msgToSend.encode("utf-8"))
            except:
                remove(client)
    
def clientThread(connection, nickname):
    connection.send("Welcome to the chat room".encode("utf-8"))
    while(True):
        try:
            msg = connection.recv(2048).decode("utf-8")#to recieve
            if msg:
                print(msg)
                broadcast(msg, connection)
            else:
                remove(connection, nickname)
        except:
            continue


while(True):
    connection, address = server.accept()
    connection.send("NICKNAME".encode("utf-8"))
    nickname = connection.recv(2048).decode("utf-8")
    nicknames.append(nickname)
    clients.append(connection)
    print(address)
    print("{} Joined with ip address {}".format(nickname, address[0]))
    newThread = Thread(target = clientThread, args=(connection, nickname))
    newThread.start()

