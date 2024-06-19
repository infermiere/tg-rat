import random
import pyautogui


def move_mouse():
    pyautogui.moveTo(random.randrange(1, 500), random.randrange(1, 500))
