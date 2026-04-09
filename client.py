import socket
import threading
import curses

SERVER_ADDRESS = (socket.gethostname(), 15662)
ENCODING = "utf-8"

username = input("Username: ")
print_lock = threading.Lock()

def run_client(stdscr):
    curses.curs_set(1)
    stdscr.nodelay(False)

    height, width = stdscr.getmaxyx()

    # Message window (all lines except the last)
    msg_win = curses.newwin(height - 1, width, 0, 0)
    msg_win.scrollok(True)  # auto-scroll when full
    
    # Input window (bottom line)
    input_win = curses.newwin(1, width, height - 1, 0)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(SERVER_ADDRESS)

    client.send(username.encode(ENCODING))

    curses_lock = threading.Lock()

    messages = []

    def display_message(msg):
        with curses_lock:
            msg_win.addstr(msg + "\n")
            msg_win.refresh()

    def receive_message(client):
        while True:
            try:
                msg = client.recv(1024).decode(ENCODING)
                display_message(msg)
            except:
                break

    thread = threading.Thread(target=receive_message, args=(client,), daemon=True)
    thread.start()

    while True:
        with curses_lock:
            input_win.clear()
            prompt = f"{username}: "
            input_win.addstr(prompt)
            input_win.refresh()

        current_input = ""

        while True:
            char = input_win.get_wch() # Get one character at a time
            if char == "\n": # This means the user has pressed enter
                break
            elif char in (curses.KEY_BACKSPACE, "\b", "\x7f"):
                current_input = current_input[:-1]
            elif isinstance(char, str):
                current_input += char
            
            with curses_lock:
                input_win.clear()
                input_win.addstr(prompt + current_input)
                input_win.refresh()

        msg = current_input

        with curses_lock:
            input_win.clear()  # wipe whatever is left in the buffer. I can't get shit to work without this here for some reason.
            input_win.refresh()

        if msg == "/leave":
            break

        client.send(msg.encode(ENCODING))

    client.close()
    print("Connection to server closed")

curses.wrapper(run_client)