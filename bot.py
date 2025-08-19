import os
import asyncio
from dotenv import load_dotenv

import discord
from discord.ext import commands

# ======================
# CONFIG (easy to adapt)
# ======================
GUILD_ID = 1399458695473008760
DEFCOORD_CHANNEL_ID = 1399478687195205763
WELCOME_CHANNEL_ID = 1399458696358264966
PASSWORDS_CHANNEL_ID = 1399471391195271198
DEFCOORD_ROLE_NAME = "Def"

# ======================
# BOT SETUP
# ======================
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Needed for join/leave events

bot = commands.Bot(command_prefix="!", intents=intents)

# ======================
# COG: AUTO PING DEFCOORD
# ======================
class AutoPingDefcoord(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if message.channel.id != DEFCOORD_CHANNEL_ID:
            return

        guild = self.bot.get_guild(GUILD_ID)
        if not guild:
            return

        role = discord.utils.get(guild.roles, name=DEFCOORD_ROLE_NAME)
        if role:
            await message.channel.send(f"{role.mention}")

# ======================
# COG: WELCOME & FAREWELL
# ======================
class WelcomeFarewell(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = self.bot.get_channel(WELCOME_CHANNEL_ID)
        if not channel:
            return

        embed = discord.Embed(
            title="🚨 NEW RECRUIT ARRIVED 🚨",
            description=(
                f"{member.mention}, welcome to **朝鲜民主主义人民共和国**.\n\n"
                f"First order of business: kindly deposit your **Travian account passwords** "
                f"into {channel.guild.get_channel(PASSWORDS_CHANNEL_ID).mention}.\n\n"
                "Failure to comply will be interpreted as treason. 🚩"
            ),
            color=discord.Color.red()
        )
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        channel = self.bot.get_channel(WELCOME_CHANNEL_ID)
        if not channel:
            return

        embed = discord.Embed(
            title="⚠️ DEFECTOR DETECTED ⚠️",
            description=(
                f"{member.display_name} has abandoned the alliance.\n\n"
                "You know what to do: **FARM THEM INTO OBLIVION.** 💀🔥"
            ),
            color=discord.Color.red()
        )
        await channel.send(embed=embed)

# ======================
# BOT EVENTS
# ======================
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")

# ======================
# MAIN ENTRY
# ======================
async def main():
    async with bot:
        await bot.add_cog(AutoPingDefcoord(bot))
        await bot.add_cog(WelcomeFarewell(bot))
        await bot.start(os.getenv("DISCORD_BOT_TOKEN"))

asyncio.run(main())
