import os
import discord
from discord.client import Client
from discord.ext import commands
import re
from chess import ChessBoard

TOKEN = None
prefix = '!'

TOKEN = None
try:
    TOKEN = os.environ.get('CHESS_TOKEN')
except Exception:
    pass


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

boards = {}

@client.event
async def on_ready():
    print(f'logged in as {client.user}')
    for filename in os.listdir('boards'):
        os.remove(f"boards/{filename}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!clear'):
        await clearChannel(message)
    if message.content.startswith('!create'):
        await createGame(message)

    expr = "^[a-h][1-8] [a-h][1-8]$"
    if re.match(expr, message.content):
        if message.author.name in boards:
            text = boards[message.author.name].makeMove(message.content)
            await message.delete()
            await showBoard(message, text)




async def createGame(message):
    name = message.author.name
    if name in boards:
        await message.channel.send("You already have a game!")
        return
    board = ChessBoard(name)
    boards[name] = board
    await showBoard(message, "New game created!")

async def showBoard(message, text):
    name = message.author.name
    file = discord.File(f"boards/{name}.png", filename=f"{name}.png")
    embed = discord.Embed()
    embed.set_image(url=f"attachment://{name}.png")
    embed.title = text
    await message.channel.send(file=file, embed=embed)


async def clearChannel(message):
    await message.channel.purge(limit=100)

client.run(TOKEN)

