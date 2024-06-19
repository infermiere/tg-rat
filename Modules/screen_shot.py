# Program to take a screenshot of the screen
import pyautogui, os, getpass


def screen_shot():
    user_folder = os.path.join("C:\\Users", getpass.getuser())
    screenshot_path = os.path.join(user_folder, "screenshot.png")

    myScreenshot = pyautogui.screenshot()
    myScreenshot.save(screenshot_path)

    return screenshot_path
