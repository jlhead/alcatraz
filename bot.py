import discord
from discord.ext import commands

class AutoPingDefcoord(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = 1376415242409738434  # Target channel ID
        self.guild_id = 1372507147153313897    # Alcatraz server ID

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if message.channel.id != self.channel_id:
            return

        guild = self.bot.get_guild(self.guild_id)
        if not guild:
            return

        # Get the role named "Defcoord"
        role = discord.utils.get(guild.roles, name="Defcoord")
        if role:
            await message.channel.send(f"{role.mention}", silent=True)

# Setup function for loading the cog
async def setup(bot):
    await bot.add_cog(AutoPingDefcoord(bot))

