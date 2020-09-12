import discord
from discord.ext import commands

import datetime
from constants import skyevents
from lib import checks

class events(commands.Cog):
    
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.check(checks.findindb)
    async def events(self,ctx):  
        embed = discord.Embed(title='Skyblock Events (UTC-0)',color= discord.Color.blue(), timestamp = datetime.datetime.utcnow())
        embed.set_thumbnail(url='https://www.speedrun.com/themes/hypixel_sb/cover-256.png')
        for events in skyevents:
            embed.add_field(name=events,value='{}\n\u200b'.format(skyevents[events]['relative']),inline=False)

        await ctx.channel.send(embed=embed)



def setup(client):
    client.add_cog(events(client))