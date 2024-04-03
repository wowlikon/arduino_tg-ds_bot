import asyncio
import os
import serial
import threading
import serial.tools.list_ports
from dotenv import load_dotenv

from discord import *
from discord.ext import commands
from functools import wraps, partial

load_dotenv()

intents = Intents.all()
intents.message_content = True
intents.members = True

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

ports = list(serial.tools.list_ports.comports())
print(list(map(lambda x: x.name, ports)))

cmds = []
ard = serial.Serial('COM3', 9600)
if not ard.is_open:
    ard.open()

bot = commands.Bot(command_prefix='!', case_insensitive=True, intents=intents)

def t(port):
    global cmds
    while True:  # Send command if possible
        if cmds:
            port.write(bytes([cmds.pop(0)]))

def async_run(func):
    @wraps(func)
    async def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_running_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)
    return run

@bot.event
async def on_ready():
    print('Working...')
    print(f"{bot.user} is ready and online!")

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

async def get_colors(ctx: AutocompleteContext):
    return [f'{t} {e}' for t, (_, e) in colors.items()]

@bot.slash_command(name="set", description="Устаноить цвет светодиода")
async def set_color(ctx, c: Option(str, "Введите цвет", required=True, autocomplete=utils.basic_autocomplete(get_colors))):  # type: ignore
    if c := c.split()[0]:
        await ctx.send(f"Color {c} {colors[c][1]} turned on")
        cmds.append(colors[c][0])
    else:
        await ctx.send("Error")

    try:
        await ctx.message.delete()
    except:
        print("Delete failed")

event_loop = asyncio.get_event_loop()
threading.Thread(target=t, args=(ard,)).start()
event_loop.run_until_complete(bot.start(token=os.environ.get('ds_token')))