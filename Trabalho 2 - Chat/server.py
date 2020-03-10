import socket
from chat_client import ChatClient

HOST = ''
PORT = 4006

clients = []

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(5)

    stop = False
    while not stop:
        print('Waiting connections...')
        conn, addr = s.accept()
        print(f'Connected by: {addr}.')
        client = ChatClient(conn, addr, clients)
        client.start()
        clients.append(client)
