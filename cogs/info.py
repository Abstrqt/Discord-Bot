import discord
from discord.ext import commands
import datetime

class info(commands.Cog):
    
    def __init__(self,client):
        self.client= client

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def info(self,ctx):
        channel = ctx.channel
        member = ctx.message.author
        embed = discord.Embed(title = 'Bot Info - v1.0.0', url = 'https://github.com/Abstrqt/BetterSkyblock', color = discord.Color.blue(), description = 'This bot was originally created by abstrqt for himself and friends to use for the sole purpose of auction flipping. Since then, he has released the bot for the public to use!')
        embed.set_footer(text='Written in Python and Discord.py | Powered by Heroku and MongoDB')
        embed.add_field(name = 'Why make another Skyblock Stats Bot?', value = 'I wanted to make a bot that would make ah flipping easier. As I started working on this project, I noticed that other bots didn\'t look as nice or lacked features I wanted, so I started adding more features and designed a beautiful UI. This is just the first version of the bot, so there are going to be more features to come!',inline=False)
        embed.add_field(name = 'How does it work?', value = 'The bot sends asynchronous http requests to [Hypixel\'s Public API](https://api.hypixel.net/) for information about users when they use commands. For commands such as !bids, which takes up to 50 queries per command, the data is stored locally so the bot doesn\'t exceed 120 queries/min to the API.',inline=False)
        embed.add_field(name = 'Special Thanks', value = 'Much love to lil_tle, ilysmt, and other Hypixel bot makers for their help and insipration :heart:',inline=False)
        embed.add_field(name = 'Enjoy!', value = '-abstrqt',inline=False)
        await channel.send(embed=embed)  

def setup(client):
    client.add_cog(info(client))