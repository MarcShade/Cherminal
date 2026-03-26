import socket
#KILDE: https://www.datacamp.com/tutorial/a-complete-guide-to-socket-programming-in-python

SERVER_ADDRESS = ("10.147.139.11", 15662)
ENCODING = "utf-8"

username = input("username: ")

def run_client():
    # create a socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP
    # establish connection with server
    client.connect(SERVER_ADDRESS)

    while True:
        # input message and send it to the server
        msg = input(f"{username}: ")
        client.send(msg.encode("utf-8")[:1024])
        if msg.lower() == "close":
            break

    # close client socket (connection to the server)
    client.close()
    print("Connection to server closed")

run_client()