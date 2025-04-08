import nextcord
from nextcord.ext import commands
import os
import logging
from pystyle import Colors,Colorate

from server import server_on

intents = nextcord.Intents.all()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
allowed_users = set()
logger = logging.getLogger('discord_bot')

commands_path = "./commands"
for filename in os.listdir(commands_path):
    if filename.endswith(".py"):
        bot.load_extension(f"commands.{filename[:-3]}")

class LinkControl(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="Allow_Link", description="เพิ่มคนที่สามารถส่งลิงก์ได้")
    async def allow_link(self, interaction: nextcord.Interaction, user: nextcord.Member):
        allowed_users.add(user.id)
        await interaction.response.send_message(f'{user.mention} สามารถส่งลิงก์ได้แล้ว!', ephemeral=True)

    @nextcord.slash_command(name="Disallow_Link", description="นำสิทธิ์ส่งลิงก์ออก")
    async def disallow_link(self, interaction: nextcord.Interaction, user: nextcord.Member):
        allowed_users.discard(user.id)
        await interaction.response.send_message(f'{user.mention} ถูกนำสิทธิ์ออกจากการส่งลิงก์!', ephemeral=True)

bot.add_cog(LinkControl(bot))

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if "http" in message.content or "www." in message.content:
        if message.author.id not in allowed_users:
            await message.delete()
            await message.channel.send(f'{message.author.mention} 🚫 คุณไม่มีสิทธิ์ส่งลิงก์!', delete_after=5)
    if len(message.content) > 8 and message.content.count(message.content[0]) > 8:
        await message.delete()
        await message.channel.send(f'{message.author.mention} หยุดสแปม😡! คุณถูกแบน 20 วินาที', delete_after=5)
        try:
            await message.author.timeout(duration=20, reason="สแปมข้อความ")
        except Exception as e:
            print(f'ไม่สามารถแบน {message.author}: {e}')
    await bot.process_commands(message)

@bot.event
async def on_ready():
    await bot.change_presence(activity=nextcord.Streaming(name="เป็นบอทแอดมินคับ😙"))
    print('Bot Run!')

server_on()
bot.run(os.getenv('TOKEN'))
