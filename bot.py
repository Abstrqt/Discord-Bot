import discord
from discord.ext import commands, tasks
import os
import time
import asyncio 
from utils import auctions
import constants

client = commands.Bot(command_prefix = '!')
client.remove_command('help')

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    getpages.start()
    client.loop.create_task(status_task())

async def status_task():
    while True:
        await client.change_presence(status=discord.Status.online, activity= discord.Game(name = '!help or @BetterSB'))
        await asyncio.sleep(10)
        await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="to user commands"))
        await asyncio.sleep(10)
        await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="the auction house"))        
        await asyncio.sleep(10)
        await client.change_presence(status=discord.Status.online, activity= discord.Game(name = 'Hypixel Skyblock')) 
        await asyncio.sleep(10)    

@client.event    
async def on_message(message):
    for x in message.mentions:
        if(x==client.user):
            embed = discord.Embed(title = 'Help Menu', color = discord.Color.blue(), description = 'For more information about a command, type !help [command]\nFor example: ``!help verify``\nNote that <> indicates a necessary argument and [] means an argument can be ommited')
            embed.add_field(name = ':tools: General', value = '```verify, help, profile```',inline=False)
            embed.add_field(name = ':muscle: Player Stats', value = '```bank, purse, milestones, pets, skills, slayers```',inline=False)
            embed.add_field(name = ':game_die: Auction House', value = '```auctionviewer```',inline=False)
            embed.add_field(name = ':thinking: Calculators', value = '```calcpet, calcskill, calcxp```',inline=False)
            embed.add_field(name = ':mag_right: Misc.', value = '```botstats, info```',inline=False) 
            await message.channel.send(embed=embed)

    if message.guild is not None:
        message.content = message.content.lower()
        await client.process_commands(message)   

@commands.has_any_role('Lead Developer')
@client.command()
async def load(ctx,extension):
    client.load_extension(f'cogs.{extension}')

@commands.has_any_role('Lead Developer')
@client.command()
async def unload(ctx,extension):
    client.unload_extension(f'cogs.{extension}')

@commands.has_any_role('Lead Developer')
@client.command()
async def reload(ctx,extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')

@tasks.loop(minutes=1)
async def getpages():
    constants.pages = []
    task = auctions.run()
    await asyncio.gather(task)  

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')  

client.run(constants.token)

