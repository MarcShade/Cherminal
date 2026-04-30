import threading
import socket
from enum import Enum
import ASCII_art as ascii
from collections import deque
from TIcTacToe import TicTacToe as ttt

ENCODING = 'utf-8'
SERVER_ADDRESS = (socket.gethostname(), 15662)

messages = deque(maxlen=1000)  # Caps the amount of messages being saved on the server.

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

participants: list[User] = []

outgoing_requests: list[PendingRequest] = []

ongoing_games: list[ttt] = []

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

    if len(message_tokens) == 1:
        if message_tokens[0] == "accept":
            for request in outgoing_requests:
                if request.recipient == user:
                    if request.request_type == PendingStates.PRIVATE_PENDING:
                        request.recipient.state = MessageStates(request.request_type.value)
                        request.sender.state = MessageStates(request.request_type.value)
                        request.sender.pm_partner, request.recipient.pm_partner = (request.recipient, request.sender)

                        send_to_user_raw(request.recipient, "clear")
                        send_to_user_raw(request.sender, "clear")

                        send_to_user(request.recipient, ascii.get_pm_conversation_started(request.sender.username))
                        send_to_user(request.sender, ascii.get_pm_conversation_started(request.sender.username))

                        outgoing_requests.remove(request)
                        break
                    elif request.request_type == PendingStates.MINIGAME_PENDING:
                        request.recipient.state = MessageStates(request.request_type.value)
                        request.sender.state = MessageStates(request.request_type.value)

                        send_to_user_raw(request.recipient, "clear")
                        send_to_user_raw(request.sender, "clear")

                        outgoing_requests.remove(request)

                        ongoing_games.append(ttt(request.sender, request.recipient, len(ongoing_games)))
                        send_to_user(request.recipient, ascii.get_tictactoe_board(ongoing_games[len(ongoing_games) - 1].board, ongoing_games[len(ongoing_games) - 1].player_1.username))
                        send_to_user(request.sender, ascii.get_tictactoe_board(ongoing_games[len(ongoing_games) - 1].board, ongoing_games[len(ongoing_games) - 1].player_1.username))
                        break

            else:
                send_to_user(user, ascii.no_invitation_to_accept)

        elif message_tokens[0] == "decline":
            for request in outgoing_requests:
                if request.recipient == user:
                    if request.request_type == PendingStates.PRIVATE_PENDING:
                        send_to_user(request.recipient, ascii.get_incoming_pm_request_declined(request.sender.username))
                        send_to_user(request.sender, ascii.get_outgoing_pm_request_declined(request.recipient.username))

                        outgoing_requests.remove(request)
                        break

                    elif request.request_type == PendingStates.MINIGAME_PENDING:
                        send_to_user(request.recipient, ascii.get_tictactoe_invitation_declined_incoming(request.sender.username))
                        send_to_user(request.sender, ascii.get_tictactoe_invitation_declined_outgoing(request.recipient.username))

                        outgoing_requests.remove(request)
                        break
            else:
                send_to_user(user, ascii.no_invitation_to_decline)

        elif message_tokens[0] == "quit":
            send_to_user_raw(user, "quit") # does absolutely nothing for now

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
            elif user.state == MessageStates.MINIGAME_STATE: #This handles everything for me inside handle_game_message
                for game in ongoing_games:
                    if game.player_1 == user or game.player_2 == user: # This method is very slow and very stupid. Why are we checking every single game?
                        handle_game_message(user, "leave")
            else:
                send_to_user(user, ascii.no_session_to_leave)
        else:
            send_to_user(user, ascii.invalid_command)

    elif len(message_tokens) == 2:
        if message_tokens[0] == "pm":
            if message_tokens[1] == user.username:
                send_to_user(user, ascii.cannot_invite_self_pm)
                return
            for i in range(0, len(participants)):
                if message_tokens[1] == participants[i].username:
                    send_to_user(participants[i], ascii.get_private_message_invitation(user.username))
                    send_to_user(user, ascii.get_private_message_receipt(participants[i].username))

                    outgoing_requests.append(PendingRequest(PendingStates.PRIVATE_PENDING, user, participants[i]))
                    break
            else:
                send_to_user(user, ascii.user_not_found)

        elif message_tokens[0] == "ttt":
            if message_tokens[1] == user.username:
                send_to_user(user, ascii.cannot_invite_self_ttt)
                return
            for i in range(0, len(participants)):
                if message_tokens[1] == participants[i].username:
                    send_to_user(participants[i], ascii.get_tictactoe_invitation(user.username))
                    send_to_user(user, ascii.get_tictactoe_receipt(participants[i].username))

                    outgoing_requests.append(PendingRequest(PendingStates.MINIGAME_PENDING, user, participants[i]))
                    break
            else:
                send_to_user(user, ascii.user_not_found)
        else:
            send_to_user(user, ascii.invalid_command)
    else:
        send_to_user(user, ascii.invalid_command)

def handle_game_message(user: User, message: str):
    for game in ongoing_games:
        if user in game.players:
            if message == "leave":
                loser = user
                winner = game.player_2 if user == game.player_1 else game.player_1

                broadcast(f"*** {winner.username} has won a game of TicTacToe against {loser.username} by resignation! ***")

                for player in [winner, loser]:
                    print(f"Handling for {player.username}")
                    send_to_user_raw(player, "clear")
                    player.state = MessageStates.PUBLIC_STATE
                    load_previous_messages(player)

                ongoing_games.remove(game)
                break

            if game.players[game.turn] == user:
                try:
                    msg = int(message)
                except ValueError:
                    return

                if msg >= 1 or msg <= 9:
                    if game.move(msg-1) == 0:
                        return
                    send_to_user_raw(game.player_1, "clear")
                    send_to_user_raw(game.player_2, "clear")

                    winner_username = game.players[game.winner % 2].username if game.winner != 0 else ""
                    send_to_user(game.player_1, str(game.winner))
                    send_to_user(game.player_1, ascii.get_tictactoe_board(game.board, game.players[game.turn].username, winner_username))
                    send_to_user(game.player_2, ascii.get_tictactoe_board(game.board, game.players[game.turn].username, winner_username))

                    if game.moves_played == 9 and winner_username == "":
                        broadcast(f"*** {game.player_1.username} and {game.player_1.username} drew their game of TicTacToe ***")


                    if winner_username != "":
                        broadcast(f"*** {winner_username} has won a game of TicTacToe against {game.players[game.winner - 1].username}! ***")

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
            elif user.state == MessageStates.MINIGAME_STATE:
                handle_game_message(user, message)
        except Exception as e:
            print(e)
            try:
                participants.remove(user)
                for participant in participants:
                    send_to_user_raw(participant, f"connections {ascii.get_chat_users(participants)}")
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

        from time import sleep # Haha we don't have a breakpoint for incoming messages in a row
        sleep(0.5)



        for participant in participants:
            send_to_user_raw(participant, f"connections {ascii.get_chat_users(participants)}")


        thread = threading.Thread(target=handle_new_connection, args=(new_user,))
        thread.start()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(SERVER_ADDRESS)
server.listen()

print('Server is listening... ')

receive()