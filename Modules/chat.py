from easygui import enterbox
from config import rat_name

def chat(msg):
    client_Message = enterbox(msg, title="You have been hacked by " + rat_name)
    return client_Message
