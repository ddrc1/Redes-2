import threading
from time import sleep
from observer import Subject

class ChatClient(Subject, threading.Thread):

    def __init__(self, conn, addr):
        super(ChatClient, self).__init__()
        self.conn = conn
        self.addr = addr

    def attach(self, hanlder):
        self.handler = hanlder

    def detach(self, hanlder):
        self.handler = None

    def notify(self, addr, data):
        self.handler.notifyAll(addr, data)

    def run(self):
        while True:
            data = self.conn.recv(1024)
            if "\close".encode("utf8") in data:
                nick = data.lstrip("\close")
                self.notify(self.addr, f"{nick} disconnected".encode("utf8"))
                self.conn.close()
                break
            else:
                print(str(data, 'utf8'))
                self.notify(self.addr, data)
