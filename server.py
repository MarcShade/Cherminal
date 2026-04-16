import threading
import socket
from enum import Enum
import ASCII_art as ascii

ENCODING = 'utf-8'
SERVER_ADDRESS = (socket.gethostname(), 15662)

participants = []

class MessageStates(Enum):
    PUBLIC_MESSAGE = 1
    PRIVATE_MESSAGE = 2

class User:
    def __init__(self, username, client_socket):
        self.username = username
        self.client_socket = client_socket
        self.state = MessageStates.PUBLIC_MESSAGE
        self.pending = None

def receive_from_user(user: User):
    print(f"Receiving message from {user.username}")
    return user.client_socket.recv(1024).decode(ENCODING)

def send_to_user(user: User, message):
    print(f"Sent {message} to {user.username}")
    return user.client_socket.send(message.encode(ENCODING))

def broadcast(message):
    print(f"Broadcasting {message}")
    for user in participants:
        if user.state == MessageStates.PUBLIC_MESSAGE:
            user.client_socket.send(message.encode(ENCODING))

def handle_server_commands(user: User, message):
    message = message[1:] # remove the slash ('/') from the message
    message_tokens = message.split(" ")

    if message_tokens[0] == "pm":
        for i in range(0, len(participants)):
            if message_tokens[1] == participants[i].username:
                send_to_user(participants[i], ascii.get_private_message_invitation(user.username))
                send_to_user(user, ascii.get_private_message_receipt(participants[i].username))
    else:
        send_to_user(user, ascii.invalid_command)



def handle_new_connection(user: User):
    while True:
        try:
            message = receive_from_user(user)
            if message.startswith("/"):
                handle_server_commands(user, message)
            else:
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