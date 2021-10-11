import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

import music

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

cogs = [music]

bot = commands.Bot(command_prefix="!", Intents=discord.Intents.all())

for i in range(len(cogs)):
    cogs[i].setup(bot)


bot.run(DISCORD_TOKEN)
