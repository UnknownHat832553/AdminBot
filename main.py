import nextcord
from nextcord.ext import commands
import os
import logging

from server import server_on

intents = nextcord.Intents.all()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
logger = logging.getLogger('discord_bot')

commands_path = "./commands"
for filename in os.listdir(commands_path):
    if filename.endswith(".py"):
        bot.load_extension(f"commands.{filename[:-3]}")

@bot.event
async def on_ready():
    await bot.change_presence(activity=nextcord.Game(name="เป็นผู้ดูสถานะเซิร์ฟเวอร์ค่ะ"))
    print('Bot Run!')

server_on()
bot.run(os.getenv('TOKEN'))
