import threading
import socket

# ANSI escape codes:
# \033[2J - clear the entire screen
# \033[H - move cursor to top left
# \033[A - Move cursor up one line
# \033[K - Clear from cursor to end of line

ENCODING = 'utf-8'
SERVER_ADDRESS = (socket.gethostname(), 15662)

participants = []

class User:
    def __init__(self, username, client_socket):
        self.username = username
        self.client_socket = client_socket

def receive_from_user(user: User):
    print(f"Receiving message from {user.username}")
    return user.client_socket.recv(1024).decode(ENCODING)

def send_to_user(user: User, message):
    print(f"Sent {message} to {user.username}")
    return user.client_socket.send(message.encode(ENCODING))

def broadcast(message):
    print(f"Broadcasting {message}")
    for user in participants:
        user.client_socket.send(message.encode(ENCODING))

def handle_new_connection(user: User):
    while True:
        try:
            message = receive_from_user(user)
            broadcast(f"{user.username}: {message}")
        except Exception as e:
            print(e)
            try:
                participants.remove(user)
                user.client_socket.close()
                broadcast(f"{user.username} has left the chatroom")
            finally:
                break

def receive():
    while True:
        client_socket, address = server.accept()
        print(f"Connected from {str(address)}", end="")

        username = client_socket.recv(1024).decode(ENCODING)

        print(f" with username {username}")

        new_user = User(username, client_socket)
        participants.append(new_user)

        broadcast(f"{new_user.username} has joined the chat")
        send_to_user(new_user, f"\nWelcome {username}!")

        thread = threading.Thread(target=handle_new_connection, args=(new_user,))
        thread.start()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(SERVER_ADDRESS)
server.listen()

print('Server is listening... ')

receive()