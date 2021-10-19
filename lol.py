import discord
from discord.ext import commands

import riotAPI


class Lol(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def opgg(self, ctx, *, summonerName):
        print(summonerName)
        match = riotAPI.getMatch(summonerName)
        if match:
            queue = match["gameQueueConfigId"]
            # blueTeam = [player for player in match['participants'] if match['participants'][player]['teamId'] == 100]
            participants = match['participants']
            blueTeam = [participants[i] for i in range(0, 5)]
            redTeam = [participants[i] for i in range(5, 10)]
            await ctx.send(
                "**Game type : **" + riotAPI.queues[queue]["description"] + " on " + riotAPI.queues[queue]["map"] + "\n\n"
                "Blue Team : \n"
                + blueTeam[0]['summonerName'] + "\n"
                + blueTeam[1]['summonerName'] + "\n"
                + blueTeam[2]['summonerName'] + "\n"
                + blueTeam[3]['summonerName'] + "\n"
                + blueTeam[4]['summonerName'] + "\n\n" +
                "Red Team : \n"
                + redTeam[0]['summonerName'] + "\n"
                + redTeam[1]['summonerName'] + "\n"
                + redTeam[2]['summonerName'] + "\n"
                + redTeam[3]['summonerName'] + "\n"
                + redTeam[4]['summonerName'] + "\n"
            )
        else:
            await ctx.send("Ce joueur n'est pas dans une partie\n ou le pseudo n'existe pas")


def setup(client):
    client.add_cog(Lol(client))
