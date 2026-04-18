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
   /accept          Accept a pending invitation
   /decline         Decline a pending invitation
   /leave           Leave the private message session
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