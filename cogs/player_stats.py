import discord
from discord.ext import commands
import datetime
import math
import asyncio

from utils import player
from lib import checks
from utils.user import *
from lib.exceptions import *

class player_stats(commands.Cog):
    
    def __init__(self,client):
        self.client= client

    @commands.command()
    @commands.check(checks.findindb)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def bank(self,ctx,ign = '', profile = ''):
        channel = ctx.channel
        em1 = discord.Embed(title = 'Retrieving from Hypixel API . . .', color = 0x5e7dc5)
        em1.add_field(name = 'Please be patient', value = '\u200b', inline= False)
        msg =  await channel.send(embed=em1)
        member = ctx.message.author

        try:
            profileinfo = await findprofile(ign, member, profile)
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

            profilejson = await playerjson(profileinfo[3])
            embed = discord.Embed(title = 'Bank - {0} ({1})'.format(profileinfo[0],profileinfo[2]), color = discord.Color.blue(), timestamp = datetime.datetime.utcnow())
            embed.set_footer(icon_url = member.avatar_url, text = 'Requested by {0} '.format(ctx.author))
            embed.set_thumbnail(url = 'https://visage.surgeplay.com/head/{}'.format(profileinfo[1])) 
            if 'banking' not in profilejson['profile']:
                raise APIDisabledError
            embed.add_field(name = 'Coins', value = '>>> {0:,.2f}'.format(profilejson['profile']['banking']['balance']), inline = False)
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
        except APIDisabledError:
            embed = discord.Embed(title = 'Error!', color = discord.Color.red(), description = '~~Banking API~~')
            await msg.edit(embed=embed)        
        except BadProfileError as profile:              
            embed = discord.Embed(title = 'Error!', color = discord.Color.red(), description = '{} is not a valid profile'.format(profile))
            await msg.edit(embed=embed) 

    @commands.command(aliases=['ms','milestones'])
    @commands.check(checks.findindb)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def milestone(self,ctx,ign = "",profile = ""):
        channel = ctx.channel
        em1 = discord.Embed(title = 'Retrieving from Hypixel API . . .', color = 0x5e7dc5)
        em1.add_field(name = 'Please be patient', value = '\u200b', inline= False)
        msg =   await channel.send(embed=em1)
        member = ctx.message.author

        try:
            profileinfo = await findprofile(ign, member, profile)
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

            profilejson = await playerjson(profileinfo[3])
            embed = discord.Embed(title = 'Milestones - {0} ({1})'.format(profileinfo[0],profileinfo[2]), color = discord.Color.blue(), timestamp = datetime.datetime.utcnow())
            embed.set_footer(icon_url = member.avatar_url, text = 'Requested by {0} '.format(ctx.author))
            embed.set_thumbnail(url = 'https://visage.surgeplay.com/head/{}'.format(profileinfo[1])) 

            if 'pet_milestone_ores_mined' in profilejson['profile']['members'][profileinfo[1]]['stats']:
                embed.add_field(name = 'Ores Mined', value = '>>> {0:,d}'.format(int(profilejson['profile']['members'][profileinfo[1]]['stats']['pet_milestone_ores_mined'])), inline = False)
            else:
                embed.add_field(name = 'Ores Mined', value = '>>> 0', inline = False)
            if 'pet_milestone_sea_creatures_killed' in profilejson['profile']['members'][profileinfo[1]]['stats']:
                embed.add_field(name = 'Sea Creatures Killed', value = '>>> {0:,d}'.format(int(profilejson['profile']['members'][profileinfo[1]]['stats']['pet_milestone_sea_creatures_killed'])), inline = False)
            else:
                embed.add_field(name = 'Sea Creatures Killed', value = '>>> 0', inline = False)
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

    @commands.command()
    @commands.check(checks.findindb)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def purse(self,ctx,ign = '',profile = ''):
        channel = ctx.channel
        em1 = discord.Embed(title = 'Retrieving from Hypixel API . . .', color = 0x5e7dc5)
        em1.add_field(name = 'Please be patient', value = '\u200b', inline= False)
        msg =  await channel.send(embed=em1)
        member = ctx.message.author

        try:
            profileinfo = await findprofile(ign, member, profile)
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
            
            profilejson = await playerjson(profileinfo[3])    

            embed = discord.Embed(title = 'Purse - {0} ({1})'.format(profileinfo[0],profileinfo[2]), color = discord.Color.blue(), timestamp = datetime.datetime.utcnow())
            embed.set_footer(icon_url = member.avatar_url, text = 'Requested by {0} '.format(ctx.author))
            embed.set_thumbnail(url = 'https://visage.surgeplay.com/head/{}'.format(profileinfo[1])) 
            embed.add_field(name = 'Coins', value = '>>> {0:,.2f}'.format(profilejson['profile']['members'][profileinfo[1]]['coin_purse']), inline = False)
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

    @commands.command(aliases=['slayer'])
    @commands.check(checks.findindb)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def slayers(self,ctx,ign = "",profile=''):
        channel = ctx.channel
        em1 = discord.Embed(title = 'Retrieving from Hypixel API . . .', color = 0x5e7dc5)
        em1.add_field(name = 'Please be patient', value = '\u200b', inline= False)
        msg =   await channel.send(embed=em1)
        member = ctx.message.author

        try:
            profileinfo = await findprofile(ign, member, profile)
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

            profilejson = await playerjson(profileinfo[3])   

            embed = discord.Embed(title = 'Slayer Stats - {0} ({1})'.format(profileinfo[0],profileinfo[2]), color = discord.Color.blue(), timestamp = datetime.datetime.utcnow())
            embed.set_footer(icon_url = member.avatar_url, text = 'Requested by {0} '.format(ctx.author))
            embed.set_thumbnail(url = 'https://visage.surgeplay.com/head/{}'.format(profileinfo[1])) 

            zombie = []
            spider = []
            wolf = []
            spent = 0

            for x in range(0,4):
                if 'boss_kills_tier_'+str(x) in profilejson['profile']['members'][profileinfo[1]]['slayer_bosses']['zombie']:
                    zombie.append(profilejson['profile']['members'][profileinfo[1]]['slayer_bosses']['zombie']['boss_kills_tier_'+str(x)])
                else:
                    zombie.append(0)

            if 'xp' in profilejson['profile']['members'][profileinfo[1]]['slayer_bosses']['zombie']:
                zombiexp = profilejson['profile']['members'][profileinfo[1]]['slayer_bosses']['zombie']['xp'] 
            else:
                zombiexp = 0

            if zombie != []:                                       
                embed.add_field(name = 'Zombie Slayer :man_zombie: - Level {0}'.format(len(profilejson['profile']['members'][profileinfo[1]]['slayer_bosses']['zombie']['claimed_levels'])), 
                                value = '>>> {0:,d} XP\nTier 1: {1:,d}\nTier 2: {2:,d}\nTier 3: {3:,d}\nTier 4: {4:,d}'.format(zombiexp,zombie[0],zombie[1],zombie[2],zombie[3]), 
                                inline = False)
                spent += (zombie[0]*100 + zombie[1]*2000 + zombie[2]*10000 + zombie[3]*50000)
            else:
                embed.add_field(name = 'Zombie XP', value = '>>> 0', inline = False)

            for x in range(0,4):
                if 'boss_kills_tier_'+str(x) in profilejson['profile']['members'][profileinfo[1]]['slayer_bosses']['spider']:
                    spider.append(profilejson['profile']['members'][profileinfo[1]]['slayer_bosses']['spider']['boss_kills_tier_'+str(x)])
                else:
                    spider.append(0)

            if 'xp' in profilejson['profile']['members'][profileinfo[1]]['slayer_bosses']['spider']:
                spiderxp = profilejson['profile']['members'][profileinfo[1]]['slayer_bosses']['spider']['xp'] 
            else:
                spiderxp = 0

            if spider != []:                                    
                embed.add_field(name = 'Spider Slayer :spider_web: - Level {0}'.format(len(profilejson['profile']['members'][profileinfo[1]]['slayer_bosses']['spider']['claimed_levels'])), 
                                value = '>>> {0:,d} XP\nTier 1: {1:,d}\nTier 2: {2:,d}\nTier 3: {3:,d}\nTier 4: {4:,d}'.format(spiderxp,spider[0],spider[1],spider[2],spider[3]), 
                                inline = False)
                spent += (spider[0]*100 + spider[1]*2000 + spider[2]*10000 + spider[3]*50000)
            else:
                embed.add_field(name = 'Spider XP', value = '>>> 0', inline = False)
                spiderxp = 0

            for x in range(0,4):
                if 'boss_kills_tier_'+str(x) in profilejson['profile']['members'][profileinfo[1]]['slayer_bosses']['wolf']:
                    wolf.append(profilejson['profile']['members'][profileinfo[1]]['slayer_bosses']['wolf']['boss_kills_tier_'+str(x)])
                else:
                    wolf.append(0)
            if 'xp' in profilejson['profile']['members'][profileinfo[1]]['slayer_bosses']['wolf']:
                wolfxp = profilejson['profile']['members'][profileinfo[1]]['slayer_bosses']['wolf']['xp'] 
            else:
                wolfxp = 0

            if wolf != []:                                    
                embed.add_field(name = 'Wolf Slayer :wolf: - Level {0}'.format(len(profilejson['profile']['members'][profileinfo[1]]['slayer_bosses']['wolf']['claimed_levels'])), 
                                value = '>>> {0:,d} XP\nTier 1: {1:,d}\nTier 2: {2:,d}\nTier 3: {3:,d}\nTier 4: {4:,d}'.format(wolfxp,wolf[0],wolf[1],wolf[2],wolf[3]), 
                                inline = False)
                spent += (wolf[0]*100 + wolf[1]*2000 + wolf[2]*10000 + wolf[3]*50000)
            else:
                embed.add_field(name = 'Wolf XP', value = '>>> 0', inline = False)
                wolfxp = 0
                                                          
            embed.add_field(name = 'Coins spent : {:,d}'.format(spent),value='\u200b',inline=True)
            embed.add_field(name = 'Total XP : {:,d}'.format(wolfxp+spiderxp+zombiexp),value='\u200b',inline=True)
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

    @commands.command(aliases=['pet'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.check(checks.findindb)
    async def pets(self,ctx,ign = '',profile=''):
        channel = ctx.channel
        em1 = discord.Embed(title = 'Retrieving from Hypixel API . . .', color = 0x5e7dc5)
        em1.add_field(name = 'Please be patient', value = '\u200b', inline= False)
        msg =  await channel.send(embed=em1)
        member = ctx.message.author

        try:
            profileinfo = await findprofile(ign, member, profile)
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

            profilejson = await playerjson(profileinfo[3])

            if profilejson['profile']['members'][profileinfo[1]]['pets'] != []:
                pets = player.allpets(profilejson['profile']['members'][profileinfo[1]]['pets'])
                page = 1
                pages = math.ceil(len(pets['pets'])/5)
            else:
                page = 1
                pages = 1        

            def embedgen(page):
                pages = math.ceil(len(pets['pets'])/5)
                if pages <= 1:
                    pages = 1
                if page > pages:
                    page = pages
                start = 5*(page-1)
                end = 5*page
                if end > len(pets['pets']):
                    end = len(pets['pets'])+1  
                embed = discord.Embed(title = 'Pets ({2})- {0} ({1})'.format(profileinfo[0],profileinfo[2],len(pets['pets'])), color = discord.Color.blue(), timestamp = datetime.datetime.utcnow())
                embed.set_thumbnail(url = 'https://visage.surgeplay.com/head/{}'.format(profileinfo[1])) 
                embed.set_footer(icon_url = member.avatar_url, text = 'Requested by {0} | Page {1} of {2}'.format(ctx.author,page,pages))

                for items in pets['pets'][start:end]:
                    embed.add_field(name = items,value = u'\u200b',inline=False)
                embed.add_field(name = 'Pet Score: {}'.format(pets['petscore']),value = '\u200b')
                embed.add_field(name = 'Unique Pets: ({}/45)'.format(len(pets['upets'])),value = '\u200b')
                return embed
            if profilejson['profile']['members'][profileinfo[1]]['pets'] != []:
                await msg.edit(embed=embedgen(page))
            else:
                embed = discord.Embed(title = 'Pets- {0} ({1})'.format(profileinfo[0],profileinfo[2]), color = discord.Color.blue(), timestamp = datetime.datetime.utcnow())
                embed.set_thumbnail(url = 'https://visage.surgeplay.com/head/{}'.format(profileinfo[1])) 
                embed.set_footer(icon_url = member.avatar_url, text = 'Requested by {0} | Page {1} of {2}'.format(ctx.author,page,pages))
                embed.add_field(name='No Pets Found',value='\u200b')
                await msg.edit(embed=embed)
        
            #Reaction Menu
            menu = ['◀️','▶️']

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in menu and reaction.message.id == msg.id

            async def add_reactions():
                for emoji in menu:
                    await msg.add_reaction(emoji)

            self.client.loop.create_task(add_reactions())

            while True:                       
                try:
                    reaction, user = await self.client.wait_for("reaction_add", timeout=30, check=check) 
                    if str(reaction.emoji) == "▶️" and page < pages:
                        page += 1
                        await msg.edit(embed=embedgen(page))
                        await msg.remove_reaction(reaction, user)
                    elif str(reaction.emoji) == "◀️" and page > 1:
                        page -= 1
                        await msg.edit(embed=embedgen(page))
                        await msg.remove_reaction(reaction, user)                    
                    else:
                        await msg.remove_reaction(reaction, user)          
                except asyncio.TimeoutError:
                    await msg.clear_reactions()
                    break  

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

def setup(client):
    client.add_cog(player_stats(client))