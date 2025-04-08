import nextcord
from nextcord.ext import commands
import re
from datetime import timedelta

allowed_users = set()

class LinkControl(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: nextcord.Message):
        if message.author.bot:
            return

        # เช็กลิงก์
        if re.search(r"(http[s]?://|www\.|discord\.gg)", message.content):
            if message.author.id not in allowed_users:
                await message.delete()
                await message.channel.send(
                    f'{message.author.mention} 🚫 คุณไม่มีสิทธิ์ส่งลิงก์!',
                    delete_after=5
                )
                return

        # ตรวจจับสแปมข้อความเดิมรัว ๆ
        if len(message.content) > 5 and message.content.count(message.content[0]) > 5:
            await message.delete()
            await message.channel.send(
                f'{message.author.mention} หยุดสแปม 😡! ถูกแบน 20 วินาที',
                delete_after=5
            )
            try:
                # ใช้ timeout 
                await message.guild.timeout(
                    member=message.author,
                    duration=timedelta(seconds=20),
                    reason="สแปมข้อความ"
                )
            except Exception as e:
                print(f'ไม่สามารถ timeout {message.author}: {e}')

    @nextcord.slash_command(name="allow_link", description="เพิ่มคนที่สามารถส่งลิงก์ได้")
    async def allow_link(self, interaction: nextcord.Interaction, user: nextcord.Member):
        allowed_users.add(user.id)
        await interaction.response.send_message(
            f'{user.mention} สามารถส่งลิงก์ได้แล้ว!', ephemeral=True
        )

    @nextcord.slash_command(name="disallow_link", description="นำสิทธิ์ส่งลิงก์ออก")
    async def disallow_link(self, interaction: nextcord.Interaction, user: nextcord.Member):
        allowed_users.discard(user.id)
        await interaction.response.send_message(
            f'{user.mention} ถูกนำสิทธิ์ออกจากการส่งลิงก์!', ephemeral=True
        )

def setup(bot):
    bot.add_cog(LinkControl(bot))
