from pathlib import Path, PureWindowsPath

import discord
import youtube_dl
from discord.ext import commands

ffmppeg = Path("C:/Program Files/ffmpeg/bin/ffmpeg.exe")
ffmppeg = PureWindowsPath(ffmppeg)


class Music(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def connect(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("MAIS VA DANS UN VOCAL CONIO !!")
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

    @commands.command()
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("pong")

    @commands.command()
    async def trou(self, ctx):
        await ctx.send("du cul")

    @commands.command()
    async def play(self, ctx, url):
        ctx.voice_client.stop()
        
        # le bot fait pas de bruits avec ces options
        # FFMPEG_OPTIONS = {
        #     "before_options": "-reconnect 1 -reconnect_streamed 1 - reconnect_delay_max 5",
        #     "options": "-vn"}
        
        FFMPEG_OPTIONS = {"options": "-vn"}
        YDL_OPTIONS = {
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        }
        vc = ctx.voice_client

        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]["url"]  # type: ignore
            
            # source = await discord.FFmpegOpusAudio.from_probe(url2,
            # executable=ffmppeg)

            source = discord.FFmpegPCMAudio(
                url2, executable=ffmppeg, **FFMPEG_OPTIONS)
            vc.play(source)

    @commands.command()
    async def pause(self, ctx):
        ctx.voice_client.pause()
        await ctx.send("Pause")

    @commands.command()
    async def resume(self, ctx):
        ctx.voice_client.resume()
        await ctx.send("Reprise")


def setup(client):
    client.add_cog(Music(client))
