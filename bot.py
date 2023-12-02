import discord
import json
import io
import mpu.io
import dotenv
import os
from discord.ext import commands

# load token
dotenv.load_dotenv()
token = str(os.getenv("TOKEN"))

# bot setup or something idk
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='?', description="hey", intents=intents)

# log in
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands(s)")
    except Exception as e:
        print(e)
    print('------')

# daylist
@bot.command()
async def daylist(ctx, *playlistname: str):
    wordcount = mpu.io.read('data.json')
    newwords = []
    for word in playlistname:
        word = word.lower()
        if word in wordcount:
            wordcount[word] = wordcount[word] + 1
        else:
            newwords.append(word)
            wordcount[word] = 1
    if newwords:
        await ctx.send(f"new words!!!!!!!!!!!!!!!: {newwords}")
    else:
        await ctx.send("no new words, fuck you")
    mpu.io.write('data.json', wordcount)
    
bot.run(token)