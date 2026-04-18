import threading
import socket
from enum import Enum
import ASCII_art as ascii

ENCODING = 'utf-8'
SERVER_ADDRESS = (socket.gethostname(), 15662)

participants = []

outgoing_requests = []

messages = []

class MessageStates(Enum):
    PUBLIC_STATE = 0
    PRIVATE_STATE = 1
    MINIGAME_STATE = 2

class PendingStates(Enum):
    NONE = 0
    PRIVATE_PENDING = 1
    MINIGAME_PENDING = 2


class User:
    def __init__(self, username, client_socket):
        self.username = username
        self.client_socket = client_socket
        self.state = MessageStates.PUBLIC_STATE
        self.pm_partner = None

class PendingRequest:
    def __init__(self, request_type: PendingStates, sender: User, recipient: User):
        self.request_type = request_type
        self.sender = sender
        self.recipient = recipient

def receive_from_user(user: User):
    print(f"Receiving message from {user.username}")
    return user.client_socket.recv(1024).decode(ENCODING)

def send_to_user_raw(user: User, message: str):
    print(f"Sent raw message {message} to {user.username}")
    return user.client_socket.send(message.encode(ENCODING))

def send_to_user(user: User, message: str):
    print(f"Sent {message} to {user.username}")
    return user.client_socket.send(f"@{message}".encode(ENCODING))

def broadcast(message: str):
    print(f"Broadcasting {message}")
    messages.append(message + "\n")
    for user in participants:
        if user.state == MessageStates.PUBLIC_STATE:
            send_to_user(user, message)

def load_previous_messages(user: User):
    all_messages = ""
    for msg in messages:
        all_messages += msg

    all_messages = all_messages[:-1] #Remove the last character of the string, which will always be a '\n'. Looks can easily deceive, because this is one single character, even though it looks like two!
    send_to_user(user, all_messages)

def handle_server_commands(user: User, message: str):
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

                send_to_user_raw(request.recipient, "clear")
                send_to_user_raw(request.sender, "clear")

                send_to_user(request.recipient, ascii.get_pm_conversation_started(request.sender.username))
                send_to_user(request.sender, ascii.get_pm_conversation_started(request.sender.username))

                outgoing_requests.remove(request)

    elif message_tokens[0] == "decline":
        for request in outgoing_requests:
            if request.recipient == user:
                # TODO: Is it necessary to do anything with the states if nothing happens? Don't think so. Will check up on this.
                request.sender.pm_partner, request.recipient.pm_partner = (request.recipient, request.sender)

                send_to_user(request.recipient, ascii.get_incoming_pm_request_declined(user.username))
                send_to_user(request.sender, ascii.get_outgoing_pm_request_declined(user.username))

                outgoing_requests.remove(request)


    elif message_tokens[0] == "quit":
        send_to_user_raw(user, "quit")

    elif message_tokens[0] == "ttt":
        for i in range(0, len(participants)):
            if message_tokens[1] == participants[i].username:
                pass # ascii stuff and state management stuff goes here

    elif message_tokens[0] == "help":
        send_to_user(user, ascii.help_message)

    elif message_tokens[0] == "leave":
        if user.state == MessageStates.PRIVATE_STATE:
            send_to_user_raw(user, "clear")
            send_to_user_raw(user.pm_partner, "clear")

            user.state = MessageStates.PUBLIC_STATE
            user.pm_partner.state = MessageStates.PUBLIC_STATE

            load_previous_messages(user)
            load_previous_messages(user.pm_partner)

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

        broadcast(f"{new_user.username} has joined the chat")
        load_previous_messages(new_user)
        participants.append(new_user)

        thread = threading.Thread(target=handle_new_connection, args=(new_user,))
        thread.start()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(SERVER_ADDRESS)
server.listen()

print('Server is listening... ')

receive()