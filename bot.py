import discord
from discord.ext import commands, tasks
import os
import time
import asyncio 
from utils import auctions
import constants
from constants import skyevents
from lib import api
from lib.exceptions import *
import datetime

import pymongo
from pymongo import MongoClient
cluster = MongoClient('mongodb+srv://{}@cluster0.dbfoh.mongodb.net/BetterSB?retryWrites=true&w=majority'.format(constants.dbtoken))
db = cluster['BetterSB']
collection = db['misc']

client = commands.Bot(command_prefix = '!', intents=discord.Intents.all())
client.remove_command('help')

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    loop.start()
    client.loop.create_task(status_task())

async def status_task():
    while True:
        await client.change_presence(status=discord.Status.online, activity= discord.Game(name = '!help or @BetterSB'))
        await asyncio.sleep(10)
        await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="user commands"))
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
            embed.add_field(name = ':tools: General', value = '```verify, help, profile, events```',inline=False)
            embed.add_field(name = ':muscle: Player Stats', value = '```bank, purse, milestones, pets, skills, slayers```',inline=False)
            embed.add_field(name = ':game_die: Auction House/Bazaar', value = '```auctionviewer, bazaar```',inline=False)
            embed.add_field(name = ':thinking: Calculators', value = '```calcpet, calcskill, calcxp```',inline=False)
            embed.add_field(name = ':mag_right: Misc.', value = '```botstats, info, serverconfig```',inline=False) 
            await message.channel.send(embed=embed)

    if message.guild is not None:
        message.content = message.content.lower()
        await client.process_commands(message)   


#@client.command()
#async def load(ctx,extension):
#    client.load_extension(f'cogs.{extension}')


#@client.command()
#async def unload(ctx,extension):
#    client.unload_extension(f'cogs.{extension}')


#@client.command()
#async def reload(ctx,extension):
#    client.unload_extension(f'cogs.{extension}')
#    client.load_extension(f'cogs.{extension}')

@tasks.loop(minutes=1)
async def loop():
    constants.pages = []
    task = auctions.run()
    await asyncio.gather(task)  

    tasks = []
    for event in skyevents:
        task = asyncio.ensure_future(api.eventtime(skyevents[event]['url']))
        tasks.append(task)
    response = await asyncio.gather(*tasks)

    index = 0
    for event in skyevents:
        if APIError not in response:
            skyevents[event]['time'] = response[index]
            seconds = float('%s' % (response[index]-time.time()))
        else:
            seconds = float('%s' % (skyevents[event]['time']-time.time()))
        days = int(seconds/86400)
        hours = int((seconds%86400)/3600)
        minutes = int((seconds%3600)/60)
        skyevents[event]['relative'] = '{} days {} hours {} minutes'.format(days,hours,minutes)
        index+=1

    embed = discord.Embed(title='Skyblock Events',color= discord.Color.blue(), timestamp = datetime.datetime.utcnow())
    embed.set_thumbnail(url='https://www.speedrun.com/themes/hypixel_sb/cover-256.png')
    for events in skyevents:
        embed.add_field(name=events,value='{}\n\u200b'.format(skyevents[events]['relative']),inline=False)
 
    post = collection.find_one({'type':'events'})
    markfordeletion = []
    for channels in post['data']['channels']:
        try:
            channel = client.get_channel(int(channels))
            msg = await channel.fetch_message(post['data']['channels'][channels])
            if channel != None:
                await msg.edit(embed=embed)
            else:
                raise Exception
        except Exception as e:
            markfordeletion.append(channels)
    
    collection.delete_one(post)
    for deletes in markfordeletion:
        post['data']['channels'].pop(deletes)
    collection.insert_one(post)


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')  

client.run(constants.token)
