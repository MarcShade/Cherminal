import threading
import socket
from enum import Enum
import ASCII_art as ascii

ENCODING = 'utf-8'
SERVER_ADDRESS = (socket.gethostname(), 15662)

participants = []

outgoing_requests = []

class MessageStates(Enum):
    PUBLIC_STATE = 0
    PRIVATE_STATE = 1
    MINIGAME_STATE = 2

class PendingStates(Enum):
    NONE = 0
    PRIVATE_PENDING = 1
    MINIGAME_PENDING = 2

class PendingRequest:
    def __init__(self, request_type, sender, recipient):
        self.request_type = request_type
        self.sender = sender
        self.recipient = recipient

class User:
    def __init__(self, username, client_socket):
        self.username = username
        self.client_socket = client_socket
        self.state = MessageStates.PUBLIC_STATE
        self.pm_partner = None

def receive_from_user(user: User):
    print(f"Receiving message from {user.username}")
    return user.client_socket.recv(1024).decode(ENCODING)

def send_to_user(user: User, message):
    print(f"Sent {message} to {user.username}")
    return user.client_socket.send(f"@{message}".encode(ENCODING))

def broadcast(message):
    print(f"Broadcasting {message}")
    for user in participants:
        if user.state == MessageStates.PUBLIC_STATE:
            send_to_user(user, message)

def handle_server_commands(user: User, message):
    message = message[1:] # remove the slash ('/') from the message
    message_tokens = message.split(" ")

    if message_tokens[0] == "pm":
        for i in range(0, len(participants)):
            if message_tokens[1] == participants[i].username:
                send_to_user(participants[i], ascii.get_private_message_invitation(user.username))
                send_to_user(user, ascii.get_private_message_receipt(participants[i].username))

                outgoing_requests.append(PendingRequest(PendingStates.PRIVATE_PENDING, user, participants[i]))
                break
        else:
            send_to_user(user, ascii.user_not_found)

    elif message_tokens[0] == "accept":
        for request in outgoing_requests:
            if request.recipient == user:
                request.recipient.state = MessageStates(request.request_type.value)
                request.sender.state = MessageStates(request.request_type.value)
                request.sender.pm_partner, request.recipient.pm_partner = (request.recipient, request.sender)
                send_to_user(request.recipient, "clear")
                send_to_user(request.sender, "clear")
                outgoing_requests.remove(request)

    elif message_tokens[0] == "ttt":
        for i in range(0, len(participants)):
            if message_tokens[1] == participants[i].username:
                pass # ascii stuff and state management stuff goes here

    elif message_tokens[0] == "help":
        send_to_user(user, ascii.help_message)

    else:
        send_to_user(user, ascii.invalid_command)

def handle_new_connection(user: User):
    while True:
        try:
            message = receive_from_user(user)
            if message.startswith("/"):
                handle_server_commands(user, message)
            elif user.state == MessageStates.PUBLIC_STATE:
                broadcast(f"{user.username}: {message}")
            elif user.state == MessageStates.PRIVATE_STATE:
                send_to_user(user.pm_partner, f"{user.username}: {message}")
                send_to_user(user, f"{user.username}: {message}")
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

        broadcast(f"{new_user.username} has joined the chat\n")
        send_to_user(new_user, f"Welcome {username}!")

        thread = threading.Thread(target=handle_new_connection, args=(new_user,))
        thread.start()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(SERVER_ADDRESS)
server.listen()

print('Server is listening... ')

receive()