import socket
import threading
import curses
import ASCII_art as ascii

SERVER_ADDRESS = (socket.gethostname(), 15662)
ENCODING = "utf-8"

print_lock = threading.Lock()
curses_lock = threading.Lock()


def center_text(scr, text, start_y = 0):
    height, width = scr.getmaxyx()
    lines = text.strip().split("\n")
    for i, line in enumerate(lines):
        x = max(0, (width - len(line)) // 2)
        y = i + start_y
        if 0 <= y < height:
            scr.addstr(y, x, line)

def handle_input(scr, max_len, prefix=""):
    input = ""

    while True:
        char = scr.get_wch()  # Get one character at a time
        if char == "\n":  # This means the user has pressed enter
            break
        elif char in (curses.KEY_BACKSPACE, "\b", "\x7f"):
            input = input[:-1]
        elif isinstance(char, str) and (len(input) + len(prefix)) < max_len:
            input += char

        with curses_lock:
            scr.clear()
            scr.addstr(prefix + input)
            scr.refresh()

    return input


def prep_client(stdscr):
    curses.curs_set(1)

    height, width = stdscr.getmaxyx()

    ascii_win = curses.newwin(int(height/2)-1, width, 0, 0)
    input_prompt_win = curses.newwin(int(height/2), width, int(height/2), 0)

    max_username_len = 30
    username_input_pos = [int(height / 2) + 2, int(width / 2) - 6]
    username_input_win = curses.newwin(1, max_username_len + 1, username_input_pos[0], username_input_pos[1])

    lines = ascii.title.strip().split("\n")

    center_text(ascii_win, ascii.title, 1)
    center_text(input_prompt_win, ascii.username_prompt, 0)
    input_prompt_win.refresh()
    ascii_win.refresh()

    username = handle_input(username_input_win, max_username_len)

    return username

def run_client(stdscr, username):
    curses.curs_set(1)
    stdscr.nodelay(False)

    height, width = stdscr.getmaxyx()

    # Message window (all lines except the last)
    msg_win = curses.newwin(height - 1, width, 0, 0)
    msg_win.scrollok(True)  # auto-scroll when full
    
    # Input window (bottom line)
    max_input_len = 90
    prompt = f"{username}: "
    # input_win = curses.newwin(1, len(prompt) + max_input_len , height - 1, 0)
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

        msg = handle_input(input_win, max_input_len, prompt)

        with curses_lock:
            input_win.clear()  # wipe whatever is left in the buffer. I can't get shit to work without this here for some reason.
            input_win.refresh()

        if msg == "/leave":
            break

        client.send(msg.encode(ENCODING))

    client.close()
    print("Connection to server closed")

def main(stdscr):
    username = prep_client(stdscr)
    run_client(stdscr, username)

curses.wrapper(main)