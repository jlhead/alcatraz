import os
from dotenv import load_dotenv  # Add this import

load_dotenv()  # Add this line to load .env variables

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

        role = discord.utils.get(guild.roles, name="Defcoord")
        if role:
            await message.channel.send(f"{role.mention}")

intents = discord.Intents.default()
intents.message_content = True  # Needed to read message content in on_message

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")

async def main():
    async with bot:
        await bot.add_cog(AutoPingDefcoord(bot))
        print("Token:", os.getenv("DISCORD_BOT_TOKEN"))
        await bot.start(os.getenv("DISCORD_BOT_TOKEN"))

import asyncio
asyncio.run(main())
