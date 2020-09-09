import discord
from discord.ext import commands
import datetime

from utils import user, player
from lib import checks
import constants
from lib.exceptions import *

class calculators(commands.Cog):
    
    def __init__(self,client):
        self.client= client

    @commands.command()
    @commands.check(checks.findindb)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def calcpet(self,ctx,rarity,start:int,end:int):
        channel = ctx.channel
        em1 = discord.Embed(title = 'Calculating . . .', color = 0x5e7dc5)
        em1.add_field(name = 'Please be patient', value = '\u200b', inline= False)
        msg =   await channel.send(embed=em1)
        member = ctx.message.author

        if end > 100:
            end = 100
        if start < 1: 
            start = 1
        if start <= end:
            rarity = rarity.capitalize()
            embed = discord.Embed(title = 'Pet XP Calculation', color = discord.Color.blue(), timestamp = datetime.datetime.utcnow())
            embed.set_footer(icon_url = member.avatar_url, text = 'Requested by {0} '.format(ctx.author)) 
            offset = 0
            if rarity == 'Legendary' or rarity == 'Leg' or rarity == 'L':
                offset = 20
                rarity = 'Legendary'
            elif rarity == 'Epic' or rarity == 'E':
                offset = 16
                rarity = 'Epic'
            elif rarity == 'Rare' or rarity == 'R':
                offset = 11
                rarity = 'Rare'
            elif rarity == 'Uncommon' or rarity == 'Unc' or rarity == 'U':
                offset = 6
                rarity = 'Uncommon'
            elif rarity == 'Common' or rarity == 'C':
                rarity = 'Common'
            if rarity in ['Legendary','Epic','Rare','Uncommon','Common']:
                embed.add_field(name='XP needed to level ``{0}`` pet from ``{1}``-``{2}``'.format(rarity,start,end), value = '>>> {:,d}'.format(sum(constants.petxp[int(start)-1+offset:int(end)-1+offset])))
                await msg.edit(embed=embed)
            else:
                embed = discord.Embed(title = 'Error!', color = discord.Color.red(), description = 'Invalid Arguments: \n``!calcpet [rarity] [start] [end]``')
                await msg.edit(embed=embed)       
        elif start>end:
            embed = discord.Embed(title = 'Error!', color = discord.Color.red(), description = 'Invalid Arguments: \n``!calcpet [rarity] [start] [end]``')
            await msg.edit(embed=embed)            
        
    @calcpet.error
    async def calcpet_error(self,ctx,error):  
        channel = ctx.channel
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title = 'Error!', color = discord.Color.red(), description = 'Missing Arguments: \n``!calcpet [rarity] [start] [end]``')
            await channel.send(embed=embed)
        elif isinstance(error, commands.CommandInvokeError):
            embed = discord.Embed(title = 'Error!', color = discord.Color.red(), description = 'Invalid Arguments: \n``!calcpet [rarity] [start] [end]``')
            await channel.send(embed=embed)

    @commands.command()
    @commands.check(checks.findindb)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def calcxp(self,ctx,arg1:int,arg2:int):

        channel = ctx.channel
        em1 = discord.Embed(title = 'Calculating . . .', color = 0x5e7dc5)
        em1.add_field(name = 'Please be patient', value = '\u200b', inline= False)
        msg =   await channel.send(embed=em1)
        member = ctx.message.author

        embed = discord.Embed(title = 'Skill XP Calculation', color = discord.Color.blue(), timestamp = datetime.datetime.utcnow())
        embed.set_footer(icon_url = member.avatar_url, text = 'Requested by {0} '.format(ctx.author)) 
        if arg1 <= arg2:
            if arg1 < 0:
                arg1 = 0
            if arg2 > 50:
                arg2 = 50
            embed.add_field(name='XP needed to level skill from ``{0}``-``{1}``'.format(arg1,arg2), value = '>>> {:,d}'.format(sum(constants.skillxp[arg1+1:arg2+1])))
            embed.set_thumbnail(url='https://gamepedia.cursecdn.com/minecraft_gamepedia/6/6a/Diamond_Sword_JE2_BE2.png?version=af7aeb1f9f856f57ddf2cb8076ed33d5')
            await msg.edit(embed=embed)    
        else:
            embed = discord.Embed(title = 'Error!', color = discord.Color.red(), description = 'Invalid Arguments: \n``!calcxp [start] [end]``')
            await msg.edit(embed=embed) 

    @calcxp.error
    async def calcxp_error(self,ctx,error):  
        channel = ctx.channel
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title = 'Error!', color = discord.Color.red(), description = 'Missing Arguments: \n``!calcxp [level_start] [level_end]``')
            await channel.send(embed=embed)  

    @commands.command()
    @commands.check(checks.findindb)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def calcskill(self,ctx,arg1,arg2): 
        channel = ctx.channel
        em1 = discord.Embed(title = 'Calculating . . .', color = 0x5e7dc5)
        em1.add_field(name = 'Please be patient', value = '\u200b', inline= False)
        msg =   await channel.send(embed=em1)
        member = ctx.message.author
        ign = ''

        if arg1.capitalize() in ['Combat','Farming','Enchanting','Alchemy','Foraging','Fishing','Mining','Taming','Runecrafting','Carpentry','Alch','Ench','Carp']:
            if arg1.capitalize() == 'Alch':
                arg1 = 'Alchemy'
            if arg1.capitalize() == 'Ench':
                arg1 = 'Enchanting'    
            if arg1.capitalize() == 'Carp':
                arg1 = 'Carpentry'                        
            try:
                if arg2.isdigit() == False:
                    raise TypeError

                profileinfo = await user.findprofile(ign, member, '')
                if profileinfo == InvalidIGN:
                    if ign == '':
                        ign = 'Your cached ign'
                    raise InvalidIGN(ign)
                elif profileinfo == APIError:
                    raise APIError
                elif profileinfo == HypixelAPIThrottle:
                    raise HypixelAPIThrottle
                elif profileinfo == NeverPlayedSkyblockError:
                    raise NeverPlayedSkyblockError(ign)
                elif profileinfo == BadProfileError:
                    raise BadProfileError(profile)

                profilejson = await user.playerjson(profileinfo[3])
                skills = player.cleanskills(profileinfo[1],profilejson)
                if skills == APIDisabledError:
                    raise APIDisabledError

                if int(arg2) > 50:
                    arg2 = 50

                embed = discord.Embed(title = '{0} XP Calculation - {1} ({2})'.format(arg1.capitalize(),profileinfo[0],profileinfo[2]), color = discord.Color.blue(), timestamp = datetime.datetime.utcnow())
                embed.set_footer(icon_url = member.avatar_url, text = 'Requested by {0} '.format(ctx.author))

                if arg1.capitalize() == 'Runecrafting':
                    if int(arg2) > 24:
                        arg2 =24
                    embed.add_field(name='{0} {1} - ({2:,.2f}/{3:,d})'.format(arg1.capitalize(),skills['Runecrafting'][0],skills['Runecrafting'][1],skills['runetotal']), value = '\u200b',inline=False)
                    if sum(constants.runecraftingxp[:int(arg2)+1])-skills['Runecrafting'][1] <= 0:
                        embed.add_field(name='You are already {0} {1}!'.format(arg1.capitalize(),arg2), value = '\u200b',inline=False)
                    else:
                        embed.add_field(name='{0:,.2f} XP needed  for {1} {2}!'.format(sum(constants.runecraftingxp[:int(arg2)+1])-skills['Runecrafting'][1],arg1.capitalize(),arg2), value = '\u200b',inline=False)
                
                else:
                    embed.add_field(name='{0} {1} - ({2:,.2f}/{3:,d})'.format(arg1.capitalize(),skills[arg1.capitalize()][0],skills[arg1.capitalize()][1],skills['skilltotal']), value = '\u200b',inline=False)
                    if sum(constants.skillxp[:int(arg2)+1])-skills[arg1.capitalize()][1] <= 0:
                        embed.add_field(name='You are already {0} {1}!'.format(arg1.capitalize(),arg2), value = '\u200b',inline=False)
                    else:
                        embed.add_field(name='{0:,.2f} XP needed  for {1} {2}!'.format(sum(constants.skillxp[:int(arg2)+1])-skills[arg1.capitalize()][1],arg1.capitalize(),arg2), value = '\u200b',inline=False)
                embed.set_thumbnail(url='https://raw.githubusercontent.com/LeaPhant/skybot/master/emotes/sb{}.png'.format(arg1.capitalize()))
                await msg.edit(embed=embed)

            except InvalidIGN as ign:
                embed = discord.Embed(title = 'Error!', color = discord.Color.red(), description = '{} is not a valid ign'.format(ign))
                await msg.edit(embed=embed)
            except APIError:
                embed = discord.Embed(title = 'Error!', color = discord.Color.red(), description = 'There was an issue contacting the API')
                await msg.edit(embed=embed)
            except HypixelAPIThrottle:
                embed = discord.Embed(title = 'Error!', color = discord.Color.red(), description = 'The API token is being used way too much. Try again in 1 minute')
                await msg.edit(embed=embed)
            except NeverPlayedSkyblockError as uname:
                embed = discord.Embed(title = 'Error!', color = discord.Color.red(), description = '{} has no skyblock profiles'.format(uname))
                await msg.edit(embed=embed)             
            except BadProfileError as profile:              
                embed = discord.Embed(title = 'Error!', color = discord.Color.red(), description = '{} is not a valid profile'.format(profile))
                await msg.edit(embed=embed)     
            except APIDisabledError:
                embed = discord.Embed(title = 'Error!', color = discord.Color.red(), description = '~~Skill API~~'.format(profile))
                await msg.edit(embed=embed)  
            except TypeError:
                embed = discord.Embed(title = 'Error!', color = discord.Color.red(), description = 'Invalid Arguments: \n``!calcskill [skill] [level]``')
                await msg.edit(embed=embed)  

        else:
            embed = discord.Embed(title = 'Error!', color = discord.Color.red(), description = 'Invalid Arguments: \n``!calcskill [skill] [level]``')
            await msg.edit(embed=embed)     

    @calcskill.error
    async def calcskill_error(self,ctx,error):  
        channel = ctx.channel
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title = 'Error!', color = discord.Color.red(), description = 'Missing Arguments: \n``!calcskill [skill] [level]``')
            await channel.send(embed=embed)

def setup(client):
    client.add_cog(calculators(client))