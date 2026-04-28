title = """
   :####:  ##    ##  ########  ######:   ###  ###   ######   ###   ##    :##:    ##       
  ######  ##    ##  ########  #######   ###  ###   ######   ###   ##     ##     ##       
:##:  .#  ##    ##  ##        ##   :##  ###::###     ##     ###:  ##    ####    ##       
##        ##    ##  ##        ##    ##  ###  ###     ##     ####  ##    ####    ##       
##.       ##    ##  ##        ##   :##  ## ## ##     ##     ##:#: ##   :#  #:   ##       
##        ########  #######   #######:  ##:##:##     ##     ## ## ##    #::#    ##       
##        ########  #######   ######    ##.##.##     ##     ## ## ##   ##  ##   ##       
##.       ##    ##  ##        ##   ##.  ## ## ##     ##     ## :#:##   ######   ##       
##        ##    ##  ##        ##   ##   ##    ##     ##     ##  ####  .######.  ##       
:##:  .#  ##    ##  ##        ##   :##  ##    ##     ##     ##  :###  :##  ##:  ##       
  ######  ##    ##  ########  ##    ##: ##    ##   ######   ##   ###  ###  ###  ######## 
  :####:  ##    ##  ########  ##    ### ##    ##   ######   ##   ###  ##:  :##  ########
"""

username_prompt = """
╔══════════════════════════════════════════════════════╗
║                                                      ║
║   Enter a username:                                  ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
"""

def get_private_message_invitation(username: str):
    return f"""
══════════════════════════════════════════════════════

   {username} has invited you to privately message.

   Type /accept to accept
   Type /decline to decline

══════════════════════════════════════════════════════
    """

def get_private_message_receipt(username: str):
    return f"""
══════════════════════════════════════════════════════

   You invited {username} to privately message.
   Waiting for their response...

══════════════════════════════════════════════════════
"""

user_not_found = """
══════════════════════════════════════════════════════

   Could not find anyone with that username.

══════════════════════════════════════════════════════
"""

invalid_command = """
══════════════════════════════════════════════════════

   Not a valid command.

══════════════════════════════════════════════════════
"""

help_message = """
══════════════════════════════════════════════════════

   Available commands:

   /pm [username]   Send a private message invite
   /ttt [username]  Send a tic tac tor invite
   /accept          Accept a pending invitation
   /decline         Decline a pending invitation
   /leave           Leave a session
   /quit            Quit the program
   /help            Show this message

══════════════════════════════════════════════════════
"""

def get_outgoing_pm_request_declined(username: str):
    return f"""
══════════════════════════════════════════════════════

   {username} has declined your private message request.

══════════════════════════════════════════════════════
"""

def get_incoming_pm_request_declined(username: str):
    return f"""
══════════════════════════════════════════════════════

   You have declined the private message request
   from {username}.

══════════════════════════════════════════════════════
"""

def get_pm_conversation_started(username: str):
    return f"""
══════════════════════════════════════════════════════

   You are now in a private conversation with {username}.
   Type /leave to return to the public chat.

══════════════════════════════════════════════════════
"""

no_invitation_to_accept = f"""
══════════════════════════════════════════════════════

   You have no pending invitations to accept.

══════════════════════════════════════════════════════
"""

no_invitation_to_decline = f"""
══════════════════════════════════════════════════════

   You have no pending invitations to decline.

══════════════════════════════════════════════════════
"""

no_session_to_leave = f"""
══════════════════════════════════════════════════════

   You are not currently in a session to leave.

══════════════════════════════════════════════════════
"""

def get_tictactoe_invitation(username: str):
    return f"""
══════════════════════════════════════════════════════

   {username} has invited you to play TicTacToe!

   Type /accept to accept
   Type /decline to decline

══════════════════════════════════════════════════════
"""

def get_tictactoe_receipt(username: str):
    return f"""
══════════════════════════════════════════════════════

   You have invited {username} to play TicTacToe!

   Waiting for them to accept or decline...

══════════════════════════════════════════════════════
"""

def get_tictactoe_invitation_declined_outgoing(username: str):
    return f"""
══════════════════════════════════════════════════════

   {username} has declined your invitation
   to play TicTacToe.

══════════════════════════════════════════════════════
"""

def get_tictactoe_invitation_declined_incoming(username: str):
    return f"""
══════════════════════════════════════════════════════

   You have declined {username}'s invitation
   to play TicTacToe.

══════════════════════════════════════════════════════
"""

cannot_invite_self_pm = f"""
══════════════════════════════════════════════════════

   You cannot invite yourself to a private message.

══════════════════════════════════════════════════════
"""

cannot_invite_self_ttt = f"""
══════════════════════════════════════════════════════

   You cannot invite yourself to a TicTacToe game.

══════════════════════════════════════════════════════
"""

def get_tictactoe_board(board: list[int], username: str, winner: str = ""):
    X = [
        "X   X",
        " X X ",
        "  X  ",
        " X X ",
        "X   X",
    ]

    O = [
        " OOO ",
        "O   O",
        "O   O",
        "O   O",
        " OOO ",
    ]

    EMPTY = [
        "     ",
        "     ",
        "     ",
        "     ",
        "     ",
    ]

    symbols = {1: X, 2: O, 0: EMPTY}

    def render_row(row_index):
        cells = [symbols[board[row_index * 3 + col]] for col in range(3)]
        lines = [f" {cells[0][i]} │ {cells[1][i]} │ {cells[2][i]} " for i in range(5)]
        return "\n".join(lines)

    divider = "───────┼───────┼───────"

    status = f"  It is {username}'s turn" if winner == "" else f"  {winner} has won!"

    return f"""
════════════════════════

  TicTacToe
{status}

{render_row(0)}
{divider}
{render_row(1)}
{divider}
{render_row(2)}

════════════════════════
"""

def get_chat_users(participants: list):
    user_lines = "\n".join(f"   > {user.username}" for user in participants)

    return f"""
  ═════════════════════

  Users in chat ({len(participants)})

{user_lines}

  ═════════════════════
"""