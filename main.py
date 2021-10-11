import discord
from discord.ext import commands

import music

cogs = [music]

bot = commands.Bot(command_prefix="!", Intents=discord.Intents.all())

for i in range(len(cogs)):
    cogs[i].setup(bot)


bot.run("ODk2Nzc4MDk3OTUxNjU3OTg0.YWMDrw.cfwvbGmI-BTQhndUnckrTDGIc5g")
