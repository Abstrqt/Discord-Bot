import discord
from discord.ext import commands

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

def setup(client):
    client.add_cog(listeners(client))