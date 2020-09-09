import discord 
from discord.ext import commands
import datetime
import asyncio

from lib import api, checks
from utils import user
from lib.exceptions import *

import pymongo
from pymongo import MongoClient
import constants
cluster = MongoClient('mongodb+srv://{}@cluster0.dbfoh.mongodb.net/BetterSB?retryWrites=true&w=majority'.format(constants.dbtoken))
db = cluster['BetterSB']
collection = db['userInfo']

class verify(commands.Cog): 

    def __init__(self,client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.check(checks.checkguild)
    async def verify(self,ctx):
        channel = ctx.channel
        embed = discord.Embed(title = 'Verification Process Started!', 
                    color = discord.Color.blue(),
                    timestamp = datetime.datetime.utcnow())   
        msg = await ctx.send(embed=embed, delete_after=30)
        role = discord.utils.get(ctx.guild.roles, name="Verified")
        member = ctx.guild.get_member(ctx.message.author.id)


        try:
            embed = discord.Embed(title = '**BetterSB** is a multi-purpose discord bot made for everything Hypixel Skyblock!', 
                                color = discord.Color.blue(),
                                timestamp = datetime.datetime.utcnow(),
                                description = '\u200b')
            embed.set_image(url='https://hypixel.net/attachments/2020-04-25_16-17-48-png.1640146/')
            embed.add_field(name='Please tell me your minecraft username to get started!',value='\u200b',inline=False)
            dm = await ctx.author.send(embed=embed)
        except discord.Forbidden:
            embed = discord.Embed(title = 'Error!', 
                    color = discord.Color.red(),
                    timestamp = datetime.datetime.utcnow(),
                    description = 'Please allow dm\'s from server members')
            return await msg.edit(embed=embed, delete_after=30)

        try:
            ign = await self.client.wait_for("message", check=lambda m : m.author == ctx.author and m.channel == dm.channel, timeout=60)
            discordtag = await asyncio.gather(api.playerdiscord(str(ign.content)))

            if discordtag[0] == APIError:
                raise APIError
            elif discordtag[0] == InvalidIGN:
                raise InvalidIGN(str(ign.content))      
            elif discordtag[0] == HypixelAPIThrottle:
                raise HypixelAPIThrottle
            elif discordtag[0] == KeyError:
                raise KeyError

            if str(ctx.author) != discordtag[0][0]:
                em1 = discord.Embed(title = 'Error!',
                                    color = discord.Color.red(),
                                    timestamp = datetime.datetime.utcnow(),
                                    description = 'Please make sure your discord tag is {} in-game'.format(ctx.author))
                return await ctx.author.send(embed=em1)
            post = collection.find_one({'tag': discordtag[0][0]})
            if post != None:
                collection.delete_one(post)

        except asyncio.TimeoutError: 
            em1 = discord.Embed(title = 'Session Timeout!',
                                color = discord.Color.red(),
                                timestamp = datetime.datetime.utcnow(),
                                description = 'You took too long to respond')
            return await ctx.author.send(embed=em1)       
        except APIError:
            em1 = discord.Embed(title = 'Error!',
                                color = discord.Color.red(),
                                timestamp = datetime.datetime.utcnow(),
                                description = 'There was an issue when reaching the API')
            return await ctx.author.send(embed=em1)       
        except HypixelAPIThrottle:
            em1 = discord.Embed(title = 'Error!',
                                color = discord.Color.red(),
                                timestamp = datetime.datetime.utcnow(),
                                description = 'The API key is being used way too much. Try again in 1 minute')
            return await ctx.author.send(embed=em1)                             
        except KeyError:
            em1 = discord.Embed(title = 'Error!',
                                color = discord.Color.red(),
                                timestamp = datetime.datetime.utcnow(),
                                description = 'The ign given doesn\'t appear to have discord connected in-game or doesn\'t exist')
            return await ctx.author.send(embed=em1)              

        try:
            profiles = await user.allprofiles(discordtag[0][1])
            checkprofile = []
            checkprofile.extend(profiles.split(', '))
            embed.add_field(name ='Hi {}! Please enter your main profile: ``{}``'.format(discordtag[0][1], profiles),value='\u200b',inline=False)
            await ctx.author.send(embed=embed)

            profile = await self.client.wait_for("message", check=lambda m : m.author == ctx.author and m.channel == dm.channel, timeout=60)
            if str(profile.content).capitalize() not in checkprofile:
                em1 = discord.Embed(title = 'Error!',
                                    color = discord.Color.red(),
                                    timestamp = datetime.datetime.utcnow(),
                                    description = 'Invalid profile given')
                return await ctx.author.send(embed=em1)   
        except asyncio.TimeoutError: 
            em1 = discord.Embed(title = 'Session Timeout!',
                                color = discord.Color.red(),
                                timestamp = datetime.datetime.utcnow(),
                                description = 'You took too long to respond')
            return await ctx.author.send(embed=em1)   
        except HypixelAPIThrottle:
            em1 = discord.Embed(title = 'Error!',
                                color = discord.Color.red(),
                                timestamp = datetime.datetime.utcnow(),
                                description = 'The API key is being used way too much. Try again in 1 minute')
            return await ctx.author.send(embed=em1)    
        except NeverPlayedSkyblockError: 
            em1 = discord.Embed(title = 'Error!',
                                color = discord.Color.red(),
                                timestamp = datetime.datetime.utcnow(),
                                description = 'User has no skyblock profiles')
            return await ctx.author.send(embed=em1)                        

        try:
            profileinfo = await user.findprofile(discordtag[0][1], ctx.author, profile.content)
            if profileinfo == APIError:
                raise APIError
            elif profileinfo == HypixelAPIThrottle:
                raise HypixelAPIThrottle

            collection.insert_one({'name': profileinfo[0],'uuid': profileinfo[1],'profilename': profileinfo[2],'profileid': profileinfo[3],'tag': str(ctx.author)})
        
        except APIError:
            em1 = discord.Embed(title = 'Error!',
                                color = discord.Color.red(),
                                timestamp = datetime.datetime.utcnow(),
                                description = 'An API error arose while trying to save profile info to database')
            return await ctx.author.send(embed=em1)   
        except HypixelAPIThrottle:
            em1 = discord.Embed(title = 'Error!',
                                color = discord.Color.red(),
                                timestamp = datetime.datetime.utcnow(),
                                description = 'API key limit reached while trying to save profile info to database')
            return await ctx.author.send(embed=em1)                
        
        embed.add_field(name ='Successfully verified using {}\'s {} profile!'.format(ign.content,str(profile.content).capitalize()), 
                        value='You can now use this bot in any server',
                        inline=False)   
        await ctx.author.send(embed=embed)
        await member.add_roles(role)
        await member.edit(nick=discordtag[0][1])

def setup(client):
    client.add_cog(verify(client))