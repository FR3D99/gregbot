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
bot = commands.Bot(command_prefix='/', description="hey", intents=intents)

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
@bot.command(name='daylist')
async def daylist(ctx, *daylist_name: str):
    word_counts_dict = mpu.io.read('wordcount.json')
    new_words = []
    for word in daylist_name:
        word = word.lower()
        if word in word_counts_dict:
            word_counts_dict[word] = word_counts_dict[word] + 1
        else:
            new_words.append(word)
            word_counts_dict[word] = 1
    if new_words:
        await ctx.send(f"new words!!!!!!!!!!!!!!!: {new_words}")
    else:
        await ctx.send("no new words, fuck you")
    mpu.io.write('wordcount.json', word_counts_dict)
    
@bot.command(name='drink')
async def drink(ctx, amount: int = 1):
    # Check if the user has a local file
    user_file_path = 'drink_counter.json'

    if os.path.exists(user_file_path):
        # If the file exists, read the data
        with open(user_file_path, 'r') as file:
            data = json.load(file)
            user_counter = data.get(str(ctx.author.id), 0)
            user_counter += amount
    else:
        # If the file doesn't exist, create a new one
        user_counter = amount

    # Update the data and write it back to the file
    data[str(ctx.author.id)] = user_counter
    with open(user_file_path, 'w') as file:
        json.dump(data, file)

    await ctx.send(f'{ctx.author.mention} has successfully updated their total. Which now stands at {user_counter}')

bot.run(token)