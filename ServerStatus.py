import nextcord
from nextcord.ext import commands, tasks
from datetime import datetime
import pytz

class ServerStatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.status_channel_id = None
        self.last_message = None
        self.update_status.start()

    def set_status_channel(self, channel_id):
        self.status_channel_id = channel_id

    def get_thai_time(self):
        tz = pytz.timezone('Asia/Bangkok')
        return datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')

    @tasks.loop(seconds=1)
    async def update_status(self):
        await self.bot.wait_until_ready()
        if self.status_channel_id:
            channel = self.bot.get_channel(self.status_channel_id)
        if not channel:
            return

        guild = channel.guild
        # --- ข้อมูลสมาชิกและบทบาท ---
        total_members = guild.member_count
        bot_count = sum(1 for m in guild.members if m.bot)
        roles_count = len(guild.roles)
        statuses = {
            "online": 0,
            "dnd": 0,
            "idle": 0,
            "offline": 0
        }
        for m in guild.members:
            if not m.bot:
                if str(m.status) in statuses:
                    statuses[str(m.status)] += 1

        # --- เวลาไทย ---
        tz = pytz.timezone('Asia/Bangkok')
        thai_time = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
        thai_time2 = datetime.now(tz).strftime('%Y-%m-%d')

        # --- Embed สถานะ ---
        embed = nextcord.Embed(
            title=f"สถานะของเซิร์ฟเวอร์ **{guild.name}**",
            color=0x00FF00
        )
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        embed.add_field(name="**🕒・เวลาประเทศไทย**", value=f"`{thai_time}`", inline=False)
        embed.add_field(name="**👥・สมาชิกทั้งหมด**", value=f"`{total_members}` คน", inline=True)
        embed.add_field(name="**💬・บอททั้งหมด**", value=f"`{bot_count}` บอท", inline=True)
        embed.add_field(name="**📖・บทบาททั้งหมด**", value=f"`{roles_count}` บทบาท", inline=True)
        embed.add_field(name="**🟢・ออนไลน์**", value=f"`{statuses['online']}` คน", inline=True)
        embed.add_field(name="**🔴・ห้ามรบกวน**", value=f"`{statuses['dnd']}` คน", inline=True)
        embed.add_field(name="**🟡・ไม่อยู่**", value=f"`{statuses['idle']}` คน", inline=True)
        embed.add_field(name="**⚫・ออฟไลน์**", value=f"`{statuses['offline']}` คน", inline=True)
        embed.set_footer(text=f"อัปเดตล่าสุด: {thai_time2}")

        try:
            if self.last_message:
                await self.last_message.edit(embed=embed)
            else:
                self.last_message = await channel.send(embed=embed)
        except nextcord.errors.NotFound:
            self.last_message = await channel.send(embed=embed)

    @commands.command(name="set_status")
    @commands.has_permissions(administrator=True)
    async def setstatus(self, ctx: commands.Context, channel: nextcord.TextChannel):
        self.set_status_channel(channel.id)
        await ctx.send(f"ตั้งค่าช่อง {channel.mention} เรียบร้อยแล้ว!")
        try:
            await ctx.message.delete()
        except:
            pass

def setup(bot):
    bot.add_cog(ServerStatus(bot))
