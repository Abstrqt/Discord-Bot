import discord
from discord.ext import commands
import datetime

import pymongo
from pymongo import MongoClient
import constants
cluster = MongoClient('mongodb+srv://{}@cluster0.dbfoh.mongodb.net/BetterSB?retryWrites=true&w=majority'.format(constants.dbtoken))
db = cluster['BetterSB']
collection = db['userInfo']

class listeners(commands.Cog):
    
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        if str(before) != str(after):
            prev = collection.find_one({'tag': str(before)})
            if prev != None:
                collection.update_one({'tag': str(before)}, {'$set' : {'tag': str(after)}})
        pass

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            pass

        elif isinstance(error, commands.CheckFailure):
            if 'command verify' in str(error):
                em1 = discord.Embed(title = 'Error!',
                                color = discord.Color.red(),
                                timestamp = datetime.datetime.utcnow(),
                                description = 'Please verify on the [main server](https://discord.gg/CeZ3vSn)!')                                    
            elif 'Administrator' in str(error):
                em1 = discord.Embed(title = 'Error!',
                                    color = discord.Color.red(),
                                    timestamp = datetime.datetime.utcnow(),
                                    description = 'You need administrator permissions in this server to do that')                
            else:
                em1 = discord.Embed(title = 'Error!',
                                    color = discord.Color.red(),
                                    timestamp = datetime.datetime.utcnow(),
                                    description = 'Please verify with the bot before sending commands')
            return await ctx.channel.send(embed=em1)   

        elif isinstance(error, commands.CommandOnCooldown):
            em1 = discord.Embed(title = 'Error!',
                    color = discord.Color.red(),
                    timestamp = datetime.datetime.utcnow(),
                    description = f'This command is on cooldown for you! Please try again in {error.retry_after:.2f}s.')
            return await ctx.channel.send(embed=em1)   

        elif isinstance(error, commands.MissingRequiredArgument):
            pass

        else:
            return await ctx.send(error)
            
def setup(client):
    client.add_cog(listeners(client))