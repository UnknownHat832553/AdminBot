import nextcord
from nextcord.ext import commands, tasks
import asyncio
from datetime import datetime

class ServerStatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.status_channel_id = None
        self.last_message = None
        self.update_status.start()

    def set_status_channel(self, channel_id):
        self.status_channel_id = channel_id

    @tasks.loop(seconds=30)
    async def update_status(self):
        if self.status_channel_id:
            channel = self.bot.get_channel(self.status_channel_id)
            if not channel:
                return
            guild = channel.guild
            total_members = len(guild.members)
            bot_count = sum(1 for m in guild.members if m.bot)
            roles_count = len(guild.roles)
            online_members = sum(1 for m in guild.members if m.status == nextcord.Status.online)
            dnd_members = sum(1 for m in guild.members if m.status == nextcord.Status.dnd)
            idle_members = sum(1 for m in guild.members if m.status == nextcord.Status.idle)
            offline_members = sum(1 for m in guild.members if m.status == nextcord.Status.offline)

            embed = nextcord.Embed(
                title=f"สถานะของเซิร์ฟเวอร์ **{guild.name}**",
                color=0x00FF00
            )
            embed.set_thumbnail(url=guild.icon.url)
            embed.add_field(name="**🕒・เวลาประเทศไทย**", value=f"`{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`", inline=False)
            embed.add_field(name="**👥・สมาชิกทั้งหมด**", value=f"`{total_members}` คน", inline=True)
            embed.add_field(name="**💬・บอททั้งหมด**", value=f"`{sum(1 for m in guild.members if m.bot)}` บอท", inline=True)
            embed.add_field(name="**📖・บทบาททั้งหมด**", value=f"`{len(guild.roles)}` บทบาท", inline=True)
            embed.add_field(name="**🟢・ออนไลน์**", value=f"`{online_members}` คน", inline=True)
            embed.add_field(name="**🔴・ห้ามรบกวน**", value=f"`{dnd_members}` คน", inline=True)
            embed.add_field(name="**🟡・ไม่อยู่**", value=f"`{idle_members}` คน", inline=True)
            embed.add_field(name="**⚫・ออฟไลน์**", value=f"`{offline_members}` คน", inline=True)
            embed.set_footer(text=f"อัปเดตล่าสุด: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            if self.last_message:
                try:
                    await self.last_message.delete()
                except nextcord.errors.NotFound:
                    pass
            self.last_message = await channel.send(embed=embed)

    @nextcord.slash_command(name="setstatuschannel", description="ตั้งค่าช่องเพื่ออัปเดตสถานะของเซิร์ฟเวอร์")
    @commands.has_permissions(administrator=True)
    async def setstatuschannel(self, interaction: nextcord.Interaction, channel: nextcord.TextChannel):
        self.set_status_channel(channel.id)
        await interaction.response.send_message(f"ตั้งค่าช่อง {channel.mention} เรียบร้อยแล้ว!", ephemeral=True)

    @nextcord.slash_command(name="stopstatus", description="หยุดการอัปเดตสถานะของเซิร์ฟเวอร์")
    @commands.has_permissions(administrator=True)
    async def stopstatus(self, interaction: nextcord.Interaction):
        self.update_status.stop()
        await interaction.response.send_message("การอัปเดตสถานะถูกปิดแล้ว!", ephemeral=True)

def setup(bot):
    bot.add_cog(ServerStatus(bot))
