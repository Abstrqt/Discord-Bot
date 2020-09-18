import discord
from discord.ext import commands
import datetime

from lib.exceptions import *
from utils import player
from lib import checks
from utils.user import *
import constants
import asyncio

class skills(commands.Cog):
    
    def __init__(self,client):
        self.client= client

    @commands.command(aliases=['s','skill'])
    @commands.check(checks.findindb)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def skills(self,ctx,*args):
        channel = ctx.channel
        em1 = discord.Embed(title = 'Calculating . . .', color = 0x5e7dc5)
        em1.add_field(name = 'Please be patient', value = '\u200b', inline= False)
        msg =  await channel.send(embed=em1)
        member = ctx.message.author

        #Parse Args
        propernames = ['combat','foraging','farming','fishing','alchemy','enchanting','mining','taming','runecrafting','carpentry']
        skill = 'general'
        args = list(args)
        for arg in args:
            for names in propernames:
                if arg in names:
                    args.remove(arg)
                    skill = names
        if len(args) >= 1:
            ign = args[0]
        else:
            ign = ''

        try:
            profileinfo = await findprofile(ign, member, '')
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

            profilejson = await playerjson(profileinfo[3])
            skills = player.allskills(profileinfo[1], profilejson)
            if skills == APIDisabledError:
                raise APIDisabledError

            bonustype = {'taming':['','Pet Luck', '🐣', 9],
                        'combat':['%', 'Crit Chance', '⚔️', 2],
                        'foraging':['','Strength', '🪓', 3],
                        'farming':['', 'Health', '🌾', 4],
                        'alchemy':['', 'Int', '⚗️', 6],
                        'enchanting':['', 'Int', '📚', 7],
                        'fishing':['', 'Health', '🎣', 5],
                        'mining':['', 'Defense', '⛏️', 8],
                        'runecrafting':['','','🔮', 10],
                        'carpentry':['','','📏', 11]
                        }

            def general():
                embed = discord.Embed(title = 'Skills - {0} ({1})'.format(profileinfo[0],profileinfo[2]), 
                                    color = discord.Color.blue(), 
                                    timestamp = datetime.datetime.utcnow())
                embed.set_footer(icon_url = member.avatar_url, 
                                text = 'Requested by {0}'.format(ctx.author))
                embed.set_thumbnail(url = 'https://visage.surgeplay.com/head/{}'.format(profileinfo[1]))       
                embedcounter = 0  
                for skill in skills:
                    embedcounter += 1
                    if embedcounter > 10:
                        break
                    embed.add_field(name = '{} {} {}'.format(bonustype[skill.lower()][2], skill, skills[skill][0]), 
                                    value = '\u200b',
                                    inline = True)
                embed.add_field(name = 'True Skill Avg: \n{}'.format(skills['True Skill Average']),
                                value = '\u200b',
                                inline = True)
                embed.add_field(name = 'Total Skill XP: \n{}'.format(skills['Total Skill XP']),
                                value = '\u200b',
                                inline = True)  

                return embed

            def commonskill(skill):
                maxxp = 'skilltotal'
                maxlevel = 50
                if skill == 'Runecrafting':
                    maxxp = 'runetotal'
                    maxlevel = 24

                embed = discord.Embed(title = '{0} Skill - {1} ({2})'.format(skill,profileinfo[0],profileinfo[2]), 
                                    color = discord.Color.blue(), 
                                    timestamp = datetime.datetime.utcnow())
                embed.set_footer(icon_url = member.avatar_url, 
                                text = 'Requested by {0}'.format(ctx.author))
                embed.set_thumbnail(url = 'https://raw.githubusercontent.com/LeaPhant/skybot/master/emotes/sb{}.png'.format(skill))              
                embed.add_field(name = '{0} {1} {2}'.format(bonustype[skill.lower()][2],skill,skills[skill][0]), 
                                value = 'Total Progress: (**{}**/{})'.format(skills[skill][1],skills[maxxp]),
                                inline=False)   
                if skills[skill][4] != None:
                    embed.add_field(name = 'Skill Bonus:', 
                                    value = '>>> **+{0}{1}** {2}'.format(skills[skill][4],bonustype[skill.lower()][0],bonustype[skill.lower()][1]), 
                                    inline=False)
                if skills[skill][0] < maxlevel:   
                    embed.add_field(name = 'Progress to {0} {1}:'.format(skill,skills[skill][0]+1), 
                                    value = '>>> (**{0}**/{1})'.format(skills[skill][2],skills[skill][3]), 
                                    inline=False)                         
                return embed

            if skill.lower() in propernames:
                page = bonustype[skill.lower()][3]
                await msg.edit(embed=commonskill(skill.capitalize()))
            else:
                page = 1
                await msg.edit(embed = general())


            emojis = ['◀️','⚔️','🪓','🌾','🎣','⚗️','📚','⛏️','🐣','🔮','📏']

            #Reaction Menu
            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in emojis and reaction.message.id == msg.id

            async def add_reactions():
                for emoji in emojis:
                    await msg.add_reaction(emoji)
            
            self.client.loop.create_task(add_reactions())

            while True:                       
                try:
                    reaction, user = await self.client.wait_for("reaction_add", timeout=30, check=check)
                    if str(reaction.emoji) == "◀️" and page != 1:
                        page = 1                                        
                        await msg.edit(embed=general())
                        await msg.remove_reaction(reaction, user)
                    elif str(reaction.emoji) != "◀️":
                        for skill in bonustype:
                            if str(reaction.emoji) in bonustype[skill] and page not in bonustype[skill]:
                                page = bonustype[skill][3]
                                await msg.edit(embed=commonskill(skill.capitalize()))
                                await msg.remove_reaction(reaction, user)   
                            elif str(reaction.emoji) in bonustype[skill] and page in bonustype[skill]:
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
        except APIDisabledError:
            embed = discord.Embed(title = 'Error!', color = discord.Color.red(), description = '~~Skill API~~')
            await msg.edit(embed=embed)    

    @commands.command(aliases=['ds','dungeonskill'])
    @commands.check(checks.findindb)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def dungeonskills(self,ctx,*args):
        channel = ctx.channel
        em1 = discord.Embed(title = 'Calculating . . .', color = 0x5e7dc5)
        em1.add_field(name = 'Please be patient', value = '\u200b', inline= False)
        msg =  await channel.send(embed=em1)
        member = ctx.message.author

        #Parse Args
        propernames = ['mage','healer','berserker','archer','tank']
        skill = 'general'
        args = list(args)
        for arg in args:
            for names in propernames:
                if arg in names:
                    args.remove(arg)
                    skill = names
        if len(args) >= 1:
            ign = args[0]
        else:
            ign = ''

        try:
            profileinfo = await findprofile(ign, member, '')
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

            profilejson = await playerjson(profileinfo[3])
            skills = player.dungeonskills(profileinfo[1], profilejson)
            if skills == APIDisabledError:
                raise APIDisabledError

            bonustype = {'mage':['✨', 3, ['Renew','Healing Aura','Revive'],['Healing Circle','Wish'],['Healing Potion','Revive Self']],
                        'healer':['⚕️', 2, ['Mage Staff','Efficient Spells'],['Guided Sheep','Thunderstorm'],['Pop-up Wall','Fireball']],
                        'berserker':['🗡️', 4, ['Bloodlust'],['Throwing Axe','Ragnarok'],['Strength Potion','Ghost Axe']],
                        'archer':['🏹', 5, ['Doubleshot','Bone Plating','Bouncy Arrows'],['Explosive Shot','Machine Gun Bow'],['Drop Arrows','Stun Bow']],
                        'tank':['🛡️', 6, ['Protective Barrier','Taunt'],['Seismic Wave','Castle of Stone'],['Stun Potion','Absorption Potion']]
                        }

            def general():
                embed = discord.Embed(title = 'Dungeoneering Skills - {0} ({1})'.format(profileinfo[0],profileinfo[2]), 
                                    color = discord.Color.blue(), 
                                    timestamp = datetime.datetime.utcnow())
                embed.set_footer(icon_url = member.avatar_url, 
                                text = 'Note: Class levels may not be accurate due to limited xp tables\nRequested by {0}'.format(ctx.author))
                embed.set_thumbnail(url = 'https://visage.surgeplay.com/head/{}'.format(profileinfo[1]))       
                embedcounter = 0
                for skill in skills:
                    embedcounter += 1
                    if embedcounter > 5:
                        break
                    embed.add_field(name = '{} {} {}'.format(bonustype[skill.lower()][0], skill, skills[skill][0]), 
                                    value = '\u200b',
                                    inline = False)
                embed.add_field(name = 'Total Dungeon Skill XP\n{}'.format(skills['totalxp']), 
                                value = '\u200b',
                                inline = False)            
                return embed                                    

            def commonskill(skill):
                embed = discord.Embed(title = '{0} Skill - {1} ({2})'.format(skill,profileinfo[0],profileinfo[2]), 
                                    color = discord.Color.blue(), 
                                    timestamp = datetime.datetime.utcnow())
                embed.set_footer(icon_url = member.avatar_url, 
                                text = 'Requested by {0}'.format(ctx.author))          
                embed.add_field(name = '{0} {1} {2}'.format(bonustype[skill.lower()][0],skill,skills[skill][0]), 
                                value = 'Total Progress: **{}** XP'.format(skills[skill][1]),
                                inline=False)   
                embed.add_field(name='Class Passives',
                                value='\n'.join(bonustype[skill.lower()][2]))
                embed.add_field(name='Dungeon Orb Abilities',
                                value='\n'.join(bonustype[skill.lower()][3]))    
                embed.add_field(name='Ghost Abilities',
                                value='\n'.join(bonustype[skill.lower()][4]))                                                            

                return embed

            if skill.lower() in propernames:
                page = bonustype[skill.lower()][1]
                await msg.edit(embed=commonskill(skill.capitalize()))
            else:
                page = 1
                await msg.edit(embed = general())

            emojis = ['◀️','⚕️','✨','🗡️','🏹','🛡️']

            #Reaction Menu
            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in emojis and reaction.message.id == msg.id

            async def add_reactions():
                for emoji in emojis:
                    await msg.add_reaction(emoji)
            
            self.client.loop.create_task(add_reactions())

            while True:                       
                try:
                    reaction, user = await self.client.wait_for("reaction_add", timeout=30, check=check)
                    if str(reaction.emoji) == "◀️" and page != 1:
                        page = 1                                        
                        await msg.edit(embed=general())
                        await msg.remove_reaction(reaction, user)
                    elif str(reaction.emoji) != "◀️":
                        for skill in bonustype:
                            if str(reaction.emoji) in bonustype[skill] and page not in bonustype[skill]:
                                page = bonustype[skill][1]
                                await msg.edit(embed=commonskill(skill.capitalize()))
                                await msg.remove_reaction(reaction, user)   
                            elif str(reaction.emoji) in bonustype[skill] and page in bonustype[skill]:
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
        except APIDisabledError:
            embed = discord.Embed(title = 'Error!', color = discord.Color.red(), description = '~~Skill API~~')
            await msg.edit(embed=embed)               

def setup(client):
    client.add_cog(skills(client))