import psutil, os, getpass

def ktask(task):
        try:
            pid = int(task)
            process = psutil.Process(pid)
            process_name = process.name()
            process.terminate()
            return f"The '{process_name}' task with PID {pid} has been stopped."
        except (psutil.NoSuchProcess, ValueError) as e:
            return f"Errore: {str(e)}"
        
def ltask():
    user_folder = os.path.join("C:\\Users", getpass.getuser())
    fl_path = os.path.join(user_folder, "task.txt")
    processes = [proc.info for proc in psutil.process_iter(['pid', 'name'])]
    process_list = "\n".join([f"PID {proc['pid']}: {proc['name']}" for proc in processes])
    with open(fl_path, "w") as e:
        e.write(process_list)
    return fl_path