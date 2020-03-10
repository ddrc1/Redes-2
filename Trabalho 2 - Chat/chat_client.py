import threading
from time import sleep

class ChatClient():

    def __init__(self, conn, addr, clients):
        self.conn = conn
        self.addr = addr
        self.clients = clients
        self.thread = threading.Thread(target=self.handler_connection)
    
    def handler_connection(self):
        while True:
            data = self.conn.recv(1024)
            print(str(data, 'utf8'))
            for client in self.clients:
                if client.addr != self.addr:
                    print("enviou!!", data)
                    client.conn.send(data)

    def start(self):
        self.thread.start()