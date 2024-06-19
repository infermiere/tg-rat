import ctypes
from config import rat_name

def show_popup(message):
    ctypes.windll.user32.MessageBoxW(0, message, rat_name, 0x30)
