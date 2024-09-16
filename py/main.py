import discord
from discord.ext import commands
import cog.music as music
import os
import random
from random import randint
from dotenv import load_dotenv

load_dotenv()

cogs = [music]

client = commands.Bot(command_prefix = "-")
intents = discord.Intents.all()

for i in range(len(cogs)):
    cogs[i].setup(client)

# Prints to console when bot is running and working!
@client.event
async def on_ready():
    print("8HW is ready to roll!")

#{name}: rn/10
@client.command()
async def roll(ctx):
    rn = randint(1, 10)
    await ctx.send(f"{ctx.author.name} rolled a **{rn}**/**10**")

# This is the Ping Pong command! Printing ping in ms to the chat...
@client.command()
async def ping(ctx):
    ping_ = client.latency
    ping = round(ping_ * 1000)
    await ctx.send(f"**Pong!** {ping}ms")

#Clear last 9999 messages from current tc.
@client.command()
async def clear(ctx, amount=9999):
    await ctx.channel.purge(limit=amount)

client.run(os.getenv('TOKEN'))