import nextcord
from nextcord.ext import commands
from nextcord.ui import View, Button

ROLE_ID = 1350767999862177812  # ID ยศที่จะให้
GUILD_ID = 1350767999862177812  # ID ของเซิร์ฟเวอร์

class RoleButtonView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(label="รับยศ", style=nextcord.ButtonStyle.gray, emoji="🔘")
    async def get_role(self, button: Button, interaction: nextcord.Interaction):
        role = interaction.guild.get_role(ROLE_ID)
        if not role:
            await interaction.response.send_message("ไม่พบยศที่ตั้งไว้", ephemeral=True)
            return

        if role in interaction.user.roles:
            await interaction.response.send_message("⚠️ คุณมียศนี้อยู่แล้ว", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"✅ รับยศ `{role.name}` เรียบร้อยแล้ว", ephemeral=True)

    @nextcord.ui.button(label="เช็คยศ", style=nextcord.ButtonStyle.gray, emoji="⚙")
    async def check_role(self, button: Button, interaction: nextcord.Interaction):
        roles = [r.name for r in interaction.user.roles if r.id != interaction.guild.id]
        role_list = ", ".join(roles) if roles else "ไม่มียศ"
        await interaction.response.send_message(f"🔍 ยศของคุณ: `{role_list}`", ephemeral=True)

    @nextcord.ui.button(label="รายละเอียดดิส", style=nextcord.ButtonStyle.gray, emoji="📃")
    async def check_guild_info(self, button: Button, interaction: nextcord.Interaction):
        guild = interaction.guild
        await interaction.response.send_message(f"🌐 เซิร์ฟเวอร์ `{guild.name}` มีสมาชิก `{guild.member_count}` คน", ephemeral=True)

class RolePanel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_view(RoleButtonView())  # เพื่อให้ปุ่มทำงานแม้บอทรีสตาร์ท

    @nextcord.slash_command(name="send_role_panel", description="ส่ง Embed ปุ่มรับยศให้ผู้ใช้กด")
    @commands.has_permissions(administrator=True)
    async def send_role_panel(self, interaction: nextcord.Interaction):
        embed = nextcord.Embed(
            title="__.....__",
            description="`🟢` **ระบบรับยศฟรี**\n- กดปุ่มเพื่อรับยศฟรี\n- ผู้สร้างบอท: Mr Emptiness\n- discord.gg/SErSdUxtTQ",
            color=0x780cc5
        )
        embed.set_thumbnail(url=GUILD_ID.icon.url)
        embed.set_image(url="https://i.pinimg.com/originals/d6/6a/d1/d66ad1a0ce0fc09370424075125b06b7.gif")
        embed.set_footer(text="รับยศกันด้วยนะ 🟢")

        await interaction.response.send_message(embed=embed, view=RoleButtonView())

def setup(bot):
    bot.add_cog(RolePanel(bot))
