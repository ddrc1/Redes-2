import socket
import time

HOST = 'localhost'
PORT = 10000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    data = s.recv(1024)
    texto = str(data, "utf8")
    print(texto)