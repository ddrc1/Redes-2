import socket
from chat_client import ChatClient
from observer import Observer

class ChatHandler(Observer):

    def __init__(self, address='localhost', port=4006):
        self.address = address
        self.port = port
        self.clients = []

    def notifyAll(self, addr, data):
        for client in self.clients:
            if client.addr != addr:
                client.conn.send(data)

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.address, self.port))
            s.listen(5)

            stop = False
            while not stop:
                print('Waiting connections...')
                conn, addr = s.accept()
                print(f'Connected by: {addr}.')
                client = ChatClient(conn, addr)
                client.start()
                client.attach(self)

                self.clients.append(client)