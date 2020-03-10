import socket
import threading

HOST = 'localhost'
PORT = 4006

def handle_connection(socket):
    while True:
        data = socket.recv(1024)
        print('### ', str(data, 'utf8'))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print(f'Connected on server {s.getpeername}')
    t = threading.Thread(target=handle_connection, args=(s,))
    t.start()

    while True:
        print('> ', end='')
        data = input()
        s.send(data.encode())
