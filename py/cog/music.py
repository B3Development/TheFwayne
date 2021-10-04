import discord

import youtube_dl

import os

from discord.ext import commands

from discord import FFmpegPCMAudio

#This communicates to youtube what quality of file we want to download.
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

def endSong(guild, path):
    os.remove(path)  

class music(commands.Cog):

    __slots__ =('client', 'players')

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("You're not in a voice channel!")
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

    @commands.command()
    async def leave(self, ctx):
            await ctx.voice_client.disconnect()

    @commands.command()
    async def pause(self, ctx):
        vc = ctx.voice_client
        if vc.is_paused():
            await ctx.send("The song is already paused!")
        else:
            await vc.pause()
            await ctx.send("Paused...")

    @commands.command()
    async def resume(self, ctx):
        vc = ctx.voice_client
        if vc.is_playing():
            await ctx.send("The song is already playing!")
        else:
            await ctx.voice_client.resume()
            await ctx.send("Resumed...")

    @commands.command(name='play', aliases=['sing','p'], description="streams music")
    async def play_(self, ctx, url : str):



        channel = ctx.message.author.voice.channel

        voice_client = await channel.connect()

        guild = ctx.message.guild

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            file = ydl.extract_info(url, download=True)
            path = str(file['title']) + "-" + str(file['id'] + ".mp3")

        voice_client.play(discord.FFmpegPCMAudio(path), after=lambda x: endSong(guild, path))
        voice_client.source = discord.PCMVolumeTransformer(voice_client.source, 1)
        await ctx.send("Your song is being played!")

def setup(client):
    client.add_cog(music(client))