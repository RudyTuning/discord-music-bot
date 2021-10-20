import discord
from discord.ext import commands

import riotAPI
import riotAPIVariables


class Lol(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def opgg(self, ctx, *, summonerName):
        print(summonerName)
        response: tuple = riotAPI.getMatch(summonerName)
        status: int = response[0]
        if status == 0:
            await ctx.send("Summoner not found")
        elif status == 1:
            await ctx.send("Summoner not in game")
        elif status == 2:
            await ctx.send("Summoner in game")
            matchData = response[1]
            queue: int = matchData[0]
            players: list = matchData[1]
            message: str = ""
            for i in range(len(players)):
                championName: str = riotAPIVariables.championName[players[i]["championId"]]
                player: str = "{p[chamionName]}        {p[summonerName]}        {p[tier]} {p[rank]} ({p[winRate]}% WR) \n".format(p=players[i])
                message += player
            await ctx.send(message)

            """
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
            """


def setup(client):
    client.add_cog(Lol(client))
