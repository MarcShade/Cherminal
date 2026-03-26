import threading
import socket

ENCODING = 'utf-8'
SERVER_ADDRESS = ("10.147.139.11", 15662)

def receive():
    client_socket, address = server.accept()
    print(f"Connected from {address}")
    while True:

        request = client_socket.recv(1024).decode(ENCODING)
        if request.lower() == 'close':
            client_socket.send("close".encode(ENCODING))
            break

        print(f"Recieved {request}")



server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(SERVER_ADDRESS)
server.listen()

print('Server is listening... ')
receive()