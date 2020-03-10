import socket
import threading
import protocol

from protocol import *

HOST = 'localhost'
PORT = 4006

def handle_connection(socket):
    nick = "###"
    while True:
        header = socket.recv(4)
    
        version = header[0]

        if version != protocol.PROTOCOL_VERSION:
            pass

        length = 0
        length = (length | header[1]) << 8
        length = (length | header[2]) << 0

        type = header[3]

        if type == protocol.NICKNAME_MESSAGE_TYPE:
            msg = socket.recv(length - protocol.PROTOCOL_HEADER_LENGTH)
            nm = protocol.NicknameMessage(str(msg, 'utf8'))
            nick = nm.nickname
        elif type == protocol.CHAT_MESSAGE_TYPE:
            
            msg = socket.recv(length - protocol.PROTOCOL_HEADER_LENGTH)
            cm = protocol.ChatMessage(str(msg, 'utf8'))
            print(f'{nick} {cm.msg}')

        else:
            pass


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print(f'Connected on server {s.getpeername}')
    t = threading.Thread(target=handle_connection, args=(s,))
    t.start()

    while True:
        print('> ', end='')
        data = input()

        m = protocol.getMessageClass(data)
        s.sendall(m.get_bytes())
        # cm = ChatMessage(data)
        # s.sendall(cm.get_bytes())
