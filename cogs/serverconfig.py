import discord
from discord.ext import commands

import datetime
import pymongo
from pymongo import MongoClient
import constants
cluster = MongoClient('mongodb+srv://{}@cluster0.dbfoh.mongodb.net/BetterSB?retryWrites=true&w=majority'.format(constants.dbtoken))
db = cluster['BetterSB']
collection = db['misc']

class events(commands.Cog):
    
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def serverconfig(self,ctx):
        embed = discord.Embed(title = 'Channel set as Skyblock Events Channel', 
                    color = discord.Color.blue(),
                    timestamp = datetime.datetime.utcnow(),
                    description = 'DO NOT DELETE THIS MESSAGE it will update in < 1 min')
        msg = await ctx.channel.send(embed=embed)
        doc = {str(ctx.channel.id):msg.id}
        post = collection.find_one({'type':'events'})
        if str(ctx.channel.id) not in post['data']['channels']:
            collection.delete_one(post)
            post['data']['channels'].update(doc)
            collection.insert_one(post)
        else:
            embed = discord.Embed(title = 'Error!', 
                                color = discord.Color.red(),
                                description = 'This channel is already set as an event channel')
            await msg.edit(embed=embed)

def setup(client):
    client.add_cog(events(client))