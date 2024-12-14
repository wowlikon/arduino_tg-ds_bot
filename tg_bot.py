import os
import serial
import telebot
import threading
import serial.tools.list_ports
from dotenv import load_dotenv

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# Dict of colors & emojis
colors = {
    "white":   (0b111, '⬜'),
    "red":     (0b100, '🟥'),
    "yellow":  (0b110, '🟨'),
    "green":   (0b010, '🟩'),
    "cylan":   (0b011, '🏞️'),
    "blue":    (0b001, '🟦'),
    "magenta": (0b101, '🟪'),
    "black":   (0b000, '⬛')
}

# Print list of ports (DEBUG)
ports = list(serial.tools.list_ports.comports())
print(list(map(lambda x: x.name, ports)))

cmds = []

# Create port object
ard = serial.Serial('/dev/ttyACM0', 9600)
if not ard.is_open: ard.open()

# Create bot
bot=telebot.TeleBot(
    token=os.environ.get('tg_token')
    )

# Parse command args
def extract_arg(arg):
    return arg.split()[1:]

# Thread function
def t(port):
    global cmds
    while True: # Send command if possible
        if cmds: port.write(bytes([cmds.pop(0)]))

# /start - command
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет ✌️\nВыбери цвет светодиода:\n\t\t"+"\n\t\t".join([f"{t} {e}" for t, (c, e) in colors.items()]))

# /set [color] - command
@bot.message_handler(commands=['set'])
def set_color(message):
    global cmds
    c = extract_arg(message.text)[0].lower()
    if c not in  colors.keys():
        bot.send_message(message.chat.id, "Неверный цвет ❌\nВыбери цвет светодиода:\n"+"\n".join(colors.keys()))
    else:
        print("Color set to "+c); cmds.append(colors[c][0])
        bot.send_message(message.chat.id, f"Цвет установлен на {c}{colors[c][1]}")

# /off - command
@bot.message_handler(commands=['off'])
def turn_off(message):
    global cmds
    print("Turned off"); cmds.append(colors["black"][0])
    bot.send_message(message.chat.id, f"Выключено💡")

# Start thread & bot
threading.Thread(target=t, args=(ard,)).start()
bot.infinity_polling()
