import discord
from discord.ext import commands
import datetime
from discord.utils import get

from utils import user
from lib import api, checks
from lib.exceptions import *

class profile(commands.Cog):
    
    def __init__(self,client):
        self.client= client

    @commands.command()
    @commands.check(checks.findindb)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def profile(self,ctx,ign = ""):
        channel = ctx.channel
        member = ctx.message.author
        em1 = discord.Embed(title = 'Loading Data . . .', color = 0x5e7dc5)
        em1.add_field(name = 'Please be patient', value = '\u200b', inline= False)
        msg = await channel.send(embed=em1)

        try:
            profileinfo = await user.findprofile(ign, member, '')
            if profileinfo == InvalidIGN:
                if ign == '':
                    ign = 'Your cached ign'
                raise InvalidIGN(ign)
            elif profileinfo == APIError:
                raise APIError

            guild = await api.guildinfo(profileinfo[1])
            if guild == APIError:
                raise APIError

            embed = discord.Embed(title = 'Profile Info - {}'.format(profileinfo[0]), color = discord.Color.blue(), timestamp = datetime.datetime.utcnow())
            embed.set_footer(icon_url = member.avatar_url, text = 'Requested by {0} '.format(ctx.author))
            embed.set_thumbnail(url = 'https://visage.surgeplay.com/head/{}'.format(profileinfo[1]))
            embed.set_image(url=f'https://gen.plancke.io/exp/{profileinfo[0]}.png') 

            if guild != None:
                embed.add_field(name = 'Guild', value = '>>> **{0} - joined {1}**\nRank: {2}'.format(guild[0],guild[1],guild[2]), inline = False)

            embed.add_field(name = 'Skyblock Stats', value = '>>> [Click Here](https://sky.lea.moe/stats/{0})'.format(profileinfo[0]), inline = False)
            embed.add_field(name = 'Auctions', value = '>>> [Click Here](https://auctions.craftlink.xyz/players/{0})'.format(profileinfo[1]), inline = False)
            embed.add_field(name = 'Hypixel Stats', value = '>>> [Click Here](https://plancke.io/hypixel/player/stats/{0})'.format(profileinfo[0]), inline = False)

            await msg.edit(embed=embed)

        except (APIError,TypeError):
            embed = discord.Embed(title = 'Error!', color = discord.Color.red(),description='There was an issue contacting the API')
            await msg.edit(embed=embed)
        except InvalidIGN as ign:
            embed = discord.Embed(title = 'Error!', color = discord.Color.red(), description = '{} is not a valid ign'.format(ign))
            await msg.edit(embed=embed)

def setup(client):
    client.add_cog(profile(client))