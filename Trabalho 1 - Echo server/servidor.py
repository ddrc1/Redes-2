import socket

HOST = "localhost"
PORT = 10000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    message = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    while True:
        conn, addr = s.accept()
        with conn:
            conn.sendall(message.encode())
            letra = message[0]
            message = message[1:]
            message += letra