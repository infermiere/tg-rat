title github.com/infermiere
pyinstaller --onefile --add-data "config.py;." --add-data "Modules;Modules" --icon=icon.ico main.py
echo done