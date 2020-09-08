import discord
from discord.ext import commands
import json
from json import JSONDecodeError
import datetime
import requests
import time
import datetime

from utils import checkkey

start_time = time.time()

class botstats(commands.Cog):
    
    def __init__(self,client):
        self.client= client

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def botstats(self,ctx):
        channel = ctx.channel
        member = ctx.message.author
        embed = discord.Embed(title = 'Bot Statistics', color = discord.Color.blue(), timestamp = datetime.datetime.utcnow())
        embed.set_footer(icon_url = member.avatar_url, text = 'Requested by {0} '.format(ctx.author))

        seconds = float('%s' % (time.time()-start_time))
        hours = int(seconds/3600)
        minutes = int((seconds/3600)%1*60)

        qinfo = checkkey.checkkey()
        if hours > 0:
            endtime = '{} hours and {} minutes'.format(hours,minutes)
        else:
            endtime = '{} minutes'.format(int(minutes))
        embed.add_field(name = 'Uptime', value = 'The bot has been online for {}'.format(endtime), inline = False)
        embed.add_field(name = 'API Queries per min', value = '>>> {} per min'.format(int(qinfo[1])+1), inline = True)
        embed.add_field(name = 'Total Queries', value = '>>> {:,d}'.format(qinfo[0]), inline = True     )
        await channel.send(embed=embed)

    @botstats.error
    async def botstats_error(self, ctx, error):
        channel = ctx.channel
        if isinstance(error, commands.CommandOnCooldown):
            em1 = discord.Embed(title = 'Error!',
                    color = discord.Color.red(),
                    timestamp = datetime.datetime.utcnow(),
                    description = f'This command is on cooldown for you! Please try again in {error.retry_after:.2f}s.')
            return await ctx.send(embed=em1)

def setup(client):
    client.add_cog(botstats(client))