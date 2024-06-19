import os

def dir_dot():
    os.chdir('..')
    return os.getcwd()

def dir_path(path):
    try:
        os.chdir(path)
        message = "Directory Changed To: " + os.getcwd()
    except Exception as e:
        message = "❌ Error: " + str(e) 

    return message

def dir_ls(path):
    try:
        if len(path) == 0:
            files_and_folders = os.listdir('.')
        else:
            files_and_folders = os.listdir(path)
        message = "Files and directories in the current folder:\n" + "\n".join(files_and_folders)
    except Exception as e:
        message = "❌ Error: " + str(e)

    return message 