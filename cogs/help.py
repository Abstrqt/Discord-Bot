import discord
from discord.ext import commands
import datetime

class help(commands.Cog):
    
    def __init__(self,client):
        self.client= client

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def help(self,ctx,view = 'General'):
        channel = ctx.channel
        member = ctx.message.author
        view = view.capitalize()
        if view == 'Verify':
            embed = discord.Embed(title = 'Verify Command', color = discord.Color.blue(), description = 'Usage: ``!verify``')
            embed.add_field(name = 'Info', value = 'Gives user verified role, changes discord-nick to ign, and creates database entry',inline=False)
            embed.add_field(name = 'Aliases', value = '```None```',inline=False)
            embed.add_field(name = 'Examples', value = 'Creates a verification session with the bot:\n```!verify abstrqt```',inline=False)
            await channel.send(embed=embed)
        elif view == 'Help':
            embed = discord.Embed(title = 'Help Command', color = discord.Color.blue(), description = 'Usage: ``!help [command]``')
            embed.add_field(name = 'Info', value = 'Displays a list of possible commands and more in-depth info about individual commands',inline=False)
            embed.add_field(name = 'Aliases', value = '```None```',inline=False)
            embed.add_field(name = 'Examples', value = 'Displays main help menu:\n```!help```\nDisplays verify command info:\n```!help verify```',inline=False)
            await channel.send(embed=embed)
        elif view == 'Profile':
            embed = discord.Embed(title = 'Profile Command', color = discord.Color.blue(), description = 'Usage: ``!profile [ign]``')
            embed.add_field(name = 'Info', value = 'Displays basic guild info and link redirects to sky.lea.moe, craftlink.auctions.xyz, and plancke.io',inline=False)
            embed.add_field(name = 'Aliases', value = '```None```',inline=False)
            embed.add_field(name = 'Examples', value = 'Displays user profile for yourself:\n```!profile```\nDisplays user profile for abstrqt:\n```!profile abstrqt```',inline=False)
            await channel.send(embed=embed)
        elif view == 'Bank':
            embed = discord.Embed(title = 'Bank Command', color = discord.Color.blue(), description = 'Usage: ``!bank [ign] [profile]``')
            embed.add_field(name = 'Info', value = 'Displays coins in bank for a specific user',inline=False)
            embed.add_field(name = 'Aliases', value = '```None```',inline=False)
            embed.add_field(name = 'Examples', value = 'Displays coins in bank for abstrqt\'s cached profile:\n```!bank abstrqt```\nDisplays coins in bank for abstrqt\'s Coconut profile:\n```!bank abstrqt coconut```',inline=False)
            await channel.send(embed=embed)
        elif view == 'Purse':
            embed = discord.Embed(title = 'Purse Command', color = discord.Color.blue(), description = 'Usage: ``!purse [ign] [profile]``')
            embed.add_field(name = 'Info', value = 'Displays coins in purse for a specific user',inline=False)
            embed.add_field(name = 'Aliases', value = '```None```',inline=False)
            embed.add_field(name = 'Examples', value = 'Displays coins in bank for abstrqt\'s cached profile:\n```!purse abstrqt```\nDisplays coins in purse for abstrqt\'s Coconut profile:\n```!purse abstrqt coconut```',inline=False)
            await channel.send(embed=embed)
        elif view == 'Milestones':
            embed = discord.Embed(title = 'Milestones Command', color = discord.Color.blue(), description = 'Usage: ``!milestones [ign] [profile]``')
            embed.add_field(name = 'Info', value = 'Displays milestone info for a specific user\'s profile',inline=False)
            embed.add_field(name = 'Aliases', value = '```milestone, ms```',inline=False)
            embed.add_field(name = 'Examples', value = 'Displays milestones for abstrqt\'s cached profile:\n```!milestones abstrqt```\nDisplays milestones for abstrqt\'s Coconut profile:\n```!milestones abstrqt coconut```',inline=False)
            await channel.send(embed=embed)
        elif view == 'Pets':
            embed = discord.Embed(title = 'Pets Command', color = discord.Color.blue(), description = 'Usage: ``!pets [ign] [profile]``')
            embed.add_field(name = 'Info', value = 'Displays milestone info for a specific user\'s profile',inline=False)
            embed.add_field(name = 'Aliases', value = '```pets, pet```',inline=False)
            embed.add_field(name = 'Examples', value = 'Displays pets for abstrqt\'s cached profile:\n```!pets abstrqt```\nDisplays pets for abstrqt\'s Coconut profile:\n```!pets abstrqt coconut```',inline=False)
            await channel.send(embed=embed)
        elif view == 'Skills':
            embed = discord.Embed(title = 'Skills Command', color = discord.Color.blue(), description = 'Usage: ``!skills [ign]``')
            embed.add_field(name = 'Info', value = 'Displays skill info for a specific user\'s profile',inline=False)
            embed.add_field(name = 'Aliases', value = '```skills, skill, s```',inline=False)
            embed.add_field(name = 'Examples', value = 'Displays skill info for abstrqt\'s cached profile:\n```!skills abstrqt```',inline=False)
            await channel.send(embed=embed)
        elif view == 'Slayers':
            embed = discord.Embed(title = 'Slayers Command', color = discord.Color.blue(), description = 'Usage: ``!slayers [ign] [profile]``')
            embed.add_field(name = 'Info', value = 'Displays slayer info for a specific user\'s profile',inline=False)
            embed.add_field(name = 'Aliases', value = '```slayers, Slayers, slayer, Slayer```',inline=False)
            embed.add_field(name = 'Examples', value = 'Displays slayer info for abstrqt\'s cached profile:\n```!slayer abstrqt```\nDisplays slayer info for abstrqt\'s Coconut profile:\n```!slayer abstrqt coconut```',inline=False)
            await channel.send(embed=embed) 
        elif view == 'Auctionviewer':
            embed = discord.Embed(title = 'Auctionviewer Command', color = discord.Color.blue(), description = 'Usage: ``!auctionviewer [ign]``')
            embed.add_field(name = 'Info', value = 'Displays auction house menu like the one in-game. !ah, !bids, and !ahstats can be used to invoke parts of the menu seperately',inline=False)
            embed.add_field(name = 'Aliases', value = '```ahview, ahmenu```',inline=False)
            embed.add_field(name = 'Examples', value = 'Displays auction house menu for abstrqt\'s cached profile:\n```!ahview abstrqt```',inline=False)
            await channel.send(embed=embed)          
        elif view == 'Calcpet':
            embed = discord.Embed(title = 'Calcpet Command', color = discord.Color.blue(), description = 'Usage: ``!calcpet <rarity> <start> <end>``')
            embed.add_field(name = 'Info', value = 'Calculates experience needed to level a pet of a specific rarity from a specified start level to a specified end level',inline=False)
            embed.add_field(name = 'Aliases', value = '```None```',inline=False)
            embed.add_field(name = 'Rarity Aliases', value = '```legendary, leg, l, epic, e, rare, r, uncommon, unc, u, common, c ```',inline=False)
            embed.add_field(name = 'Examples', value = 'Calculates experience need to level a legendary pet from 1-100:\n```!calcpet Leg 1 100```\nCalculates experience need to level a epic pet from 50-60:\n```!calcpet e 50 60```',inline=False)
            await channel.send(embed=embed)
        elif view == 'Calcskill':
            embed = discord.Embed(title = 'Calcskill Command', color = discord.Color.blue(), description = 'Usage: ``!calcskill <skill_type> <level>``')
            embed.add_field(name = 'Info', value = 'Calculates experience need to reach a certain skill level from your current skill level',inline=False)
            embed.add_field(name = 'Aliases', value = '```None```',inline=False)
            embed.add_field(name = 'Examples', value = 'Calculates experience need to level runecrafting to 24 for abstrqt\'s cached profile:\n```!calcskill runecrafting 24```',inline=False)
            await channel.send(embed=embed)  
        elif view == 'Calcxp':
            embed = discord.Embed(title = 'Calcxp Command', color = discord.Color.blue(), description = 'Usage: ``!calcxp <start> <end>``')
            embed.add_field(name = 'Info', value = 'Calculates experience needed to level a skill from a specified start level to a specified end level',inline=False)
            embed.add_field(name = 'Aliases', value = '```None```',inline=False)
            embed.add_field(name = 'Examples', value = 'Calculates experience need to level a skill from 0-50:\n```!calcskill 0 50```',inline=False)
            await channel.send(embed=embed)  
        elif view == 'Botstats':
            embed = discord.Embed(title = 'Botstats Command', color = discord.Color.blue(), description = 'Usage: ``!botstats``')
            embed.add_field(name = 'Info', value = 'Displays uptime,total queries, and queries per min for the bot',inline=False)
            embed.add_field(name = 'Aliases', value = '```None```',inline=False)
            embed.add_field(name = 'Example', value = '```!botstats```',inline=False)
            await channel.send(embed=embed)
        elif view == 'Info':
            embed = discord.Embed(title = 'Info Command', color = discord.Color.blue(), description = 'Usage: ``!info``')
            embed.add_field(name = 'Info', value = 'Displays bot information',inline=False)
            embed.add_field(name = 'Aliases', value = '```None```',inline=False)
            embed.add_field(name = 'Example', value = '```!info```',inline=False)
            await channel.send(embed=embed)                                 
        else:
            embed = discord.Embed(title = 'Help Menu', color = discord.Color.blue(), description = 'For more information about a command, type !help [command]\nFor example: ``!help verify``\nNote that <> indicates a necessary argument and [] means an argument can be ommited')
            embed.add_field(name = ':tools: General', value = '```verify, help, profile```',inline=False)
            embed.add_field(name = ':muscle: Player Stats', value = '```bank, purse, milestones, pets, skills, slayers```',inline=False)
            embed.add_field(name = ':game_die: Auction House', value = '```auctionviewer```',inline=False)
            embed.add_field(name = ':thinking: Calculators', value = '```calcpet, calcskill, calcxp```',inline=False)
            embed.add_field(name = ':mag_right: Misc.', value = '```botstats, info```',inline=False)
            await channel.send(embed=embed)                                                                                                 

def setup(client):
    client.add_cog(help(client))