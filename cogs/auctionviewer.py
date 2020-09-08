import discord
from discord.ext import commands
import datetime
import math
import asyncio
import time

from lib import checks
from lib.exceptions import *
from utils import auction
from utils.user import *
import constants


class auctionviewer(commands.Cog):
    
    def __init__(self,client):
        self.client= client

    @commands.command(aliases=['ahview','ahmenu','ah','bids','ahstats'])
    @commands.check(checks.findindb)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def auctionviewer(self,ctx, ign = ""):
        content = ctx.message.content
        channel = ctx.channel  
        em1 = discord.Embed(title = 'Retrieving from API . . .', color = 0x5e7dc5)
        em1.add_field(name = 'Please be patient', value = '\u200b', inline= False)
        msg =  await channel.send(embed=em1)
        member = ctx.message.author

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

            winning  = 0

            def initial():
                embed = discord.Embed(title='BetterSB Auction Viewer',
                                    color = discord.Color.blue(),
                                    timestamp = datetime.datetime.utcnow(),
                                    description = 'Info for ``{}``'.format(profileinfo[0]))
                embed.set_footer(icon_url = member.avatar_url, 
                                text = 'Requested by {0}'.format(ctx.author))                            
                embed.add_field(name='💰 Player Auctions', 
                                value = 'Player owns {} auctions that are in-progress\n{} items that didn\'t sell\n{} unclaimed auctions/bins totaling {:,d} coins'.format(len(auctions['active']),len(auctions['unsold']),len(auctions['unclaimed']),sum(auctions['unclaimed'])),
                                inline = False)
                embed.add_field(name='💸 Player Bids',
                                value = 'Player has {} bids, of which {} are the top bid!'.format(len(bids),winning),
                                inline = False)
                embed.add_field(name = '📈 Player Auction Stats',
                                value = 'View various statistics about player on the auction house')
                return embed

            def bidsembedgen(page): 
                seconds = float('%s' % (time.time()-constants.pagerefresh))
                hours = int(seconds/3600)
                minutes = int((seconds/3600)%1*60)
                if hours > 0:
                    refresh = 'Refreshed {} hours and {} minutes ago'.format(hours,minutes)
                elif minutes > 0:
                    refresh = 'Refreshed {} minutes ago'.format(int(minutes))
                else:
                    refresh = 'Refreshed {} seconds ago'.format(int(seconds))
                pages = math.ceil(len(bids)/5)
                if pages <= 1:
                    pages = 1
                if page > pages:
                    page = pages
                start = 5*(page-1)
                end = 5*page
                if end > len(bids):
                    end = len(bids)+1  
                embed = discord.Embed(title = 'Active Bids ({0}) - {1}'.format(len(bids),profileinfo[0]), color = discord.Color.blue(), timestamp = datetime.datetime.utcnow())
                embed.set_thumbnail(url = 'https://visage.surgeplay.com/head/{}'.format(profileinfo[1]))
                embed.set_footer(icon_url = member.avatar_url, text = '{3}\nRequested by {0} | Page {1} of {2}'.format(ctx.author,page,pages,refresh)) 

                for items in bids[start:end]:
                    embed.add_field(name = '{}'.format(items), value = '\u200b',inline=False)
                if bids == []:
                    embed.add_field(name = 'No items found', value = '\u200b',inline=False)
                return embed

            def ahembedgen(page): 
                pages = math.ceil(len(auctions['active'])/5)
                if pages <= 1:
                    pages = 1
                if page > pages:
                    page = pages
                start = 5*(page-1)
                end = 5*page
                if end > len(auctions['active']):
                    end = len(auctions['active'])+1  
                embed = discord.Embed(title = 'Auctions ({0}) - {1}'.format(len(auctions['active']),profileinfo[0]), color = discord.Color.blue(), timestamp = datetime.datetime.utcnow())
                embed.set_thumbnail(url = 'https://visage.surgeplay.com/head/{}'.format(profileinfo[1]))
                embed.set_footer(icon_url = member.avatar_url, text = 'Requested by {0} | Page {1} of {2}'.format(ctx.author,page,pages)) 

                for items in auctions['active'][start:end]:
                    embed.add_field(name = '{}'.format(items), value = '\u200b',inline=False)
                if auctions['active'] == []:
                    embed.add_field(name = 'No Active Actions', value = '\u200b',inline=False)
                if auctions['unclaimed'] != [] or auctions['unsold'] != []:
                    embed = embed.add_field(name = '{} items that didn\'t sell\nUnclaimed auctions/bins ({}) totalling: {:,d} coins'.format(len(auctions['unsold']),len(auctions['unclaimed']),sum(auctions['unclaimed'])),
                                            value = '\u200b',
                                            inline = False)
                return embed            

            def statsembedgen():
                if stats == False:
                    embed = discord.Embed(title = 'Auction Stats - {0} ({1})'.format(profileinfo[0],profileinfo[2]), 
                                        color = discord.Color.blue(), 
                                        timestamp = datetime.datetime.utcnow(),
                                        description = '\u200b')
                    embed.set_footer(icon_url = member.avatar_url, text = 'Requested by {0} '.format(ctx.author))
                    embed.add_field(name='Auction house stats could not be fetched due to missing stats',value='\u200b',inline=False)
                    return embed

                embed = discord.Embed(title = 'Auction Stats - {0} ({1})'.format(profileinfo[0],profileinfo[2]), color = discord.Color.blue(), timestamp = datetime.datetime.utcnow())
                embed.set_footer(icon_url = member.avatar_url, text = 'Requested by {0} '.format(ctx.author))
                embed.set_thumbnail(url = 'https://visage.surgeplay.com/head/{}'.format(profileinfo[1])) 
                embed.add_field(name = '__Buyer Stats__',value = '>>> Auctions Won: {:,.0f}\nTotal Bids: {:,.0f}\nHighest Bid: {:,.0f}\nGold Spent: {:,.2f}'.format(stats[0],stats[1],stats[2],stats[3]))
                embed.add_field(name='__Seller Stats__',value = '>>> Auctions Created: {:,.0f}\nFees: {:,.2f}\nGold Earned: {:,.2f}'.format(stats[4],stats[5],stats[6]))
                return embed

            emojis = ['💰','💸','📈']
            menu = ['↩️','◀️','▶️']
            allemojis = ['💰','💸','📈','↩️','◀️','▶️']
            smallmenu = ['◀️','▶️']

            async def add_reactions(emojitype):
                for emoji in emojitype:
                    await msg.add_reaction(emoji)

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in allemojis and reaction.message.id == msg.id

            if content.split(' ')[0] == '!ah':
                auctions = await auction.scan(profileinfo[3])
                if auctions == HypixelAPIThrottle:
                    raise HypixelAPIThrottle
                elif auctions == APIError:
                    raise APIError
                page = 1     
                pages = math.ceil(len(auctions['active'])/5)
                await msg.edit(embed=ahembedgen(page))
                self.client.loop.create_task(add_reactions(smallmenu))
                while True:
                    try:
                        reaction, user = await self.client.wait_for("reaction_add", timeout=30, check=check)
                        if str(reaction.emoji) == "▶️" and page < pages:
                            page += 1
                            await msg.edit(embed=ahembedgen(page))
                            await msg.remove_reaction(reaction, user)

                        elif str(reaction.emoji) == "◀️" and page > 1:
                            page -= 1
                            await msg.edit(embed=ahembedgen(page))
                            await msg.remove_reaction(reaction, user)
                        else:
                            await msg.remove_reaction(reaction, user)          
                    except asyncio.TimeoutError:
                        await msg.clear_reactions()
                        break
                    
            elif content.split(' ')[0] == '!bids':
                bids = await auction.parsebids(profileinfo[1]) 
                if bids == APIError:
                    raise APIError
                page = 1
                pages = math.ceil(len(bids)/5)
                await msg.edit(embed=bidsembedgen(page))
                self.client.loop.create_task(add_reactions(smallmenu))
                while True:
                    try:
                        reaction, user = await self.client.wait_for("reaction_add", timeout=30, check=check)
                        if str(reaction.emoji) == "▶️" and page < pages:
                            page += 1
                            await msg.edit(embed=bidsembedgen(page))
                            await msg.remove_reaction(reaction, user)

                        elif str(reaction.emoji) == "◀️" and page > 1:
                            page -= 1
                            await msg.edit(embed=bidsembedgen(page))
                            await msg.remove_reaction(reaction, user)
                        else:
                            await msg.remove_reaction(reaction, user)          
                    except asyncio.TimeoutError:
                        await msg.clear_reactions()
                        break
            elif content.split(' ')[0] == '!ahstats':
                stats = auction.stats(profilejson,profileinfo[1]) 
                await msg.edit(embed=statsembedgen())
            else:
                auctions = await auction.scan(profileinfo[3])
                if auctions == HypixelAPIThrottle:
                    raise HypixelAPIThrottle
                elif auctions == APIError:
                    raise APIError
                bids = await auction.parsebids(profileinfo[1])
                if bids == APIError:
                    raise APIError
                stats = auction.stats(profilejson,profileinfo[1])   
                for bid in bids:
                    if ':white_check_mark:' in bid:
                        winning += 1
                await msg.edit(embed=initial())
                self.client.loop.create_task(add_reactions(emojis))
                while True:                       
                    try:
                        reaction, user = await self.client.wait_for("reaction_add", timeout=30, check=check) 

                        if str(reaction.emoji) == '💰':   
                            await msg.remove_reaction(reaction, user)
                            page = 1     
                            pages = math.ceil(len(auctions['active'])/5)
                            await msg.edit(embed=ahembedgen(page))
                            await msg.clear_reactions()
                            self.client.loop.create_task(add_reactions(menu))
                            while True:
                                try:
                                    reaction, user = await self.client.wait_for("reaction_add", timeout=30, check=check)
                                    if str(reaction.emoji) == "▶️" and page < pages:
                                        page += 1
                                        await msg.edit(embed=ahembedgen(page))
                                        await msg.remove_reaction(reaction, user)

                                    elif str(reaction.emoji) == "◀️" and page > 1:
                                        page -= 1
                                        await msg.edit(embed=ahembedgen(page))
                                        await msg.remove_reaction(reaction, user)
                                    elif str(reaction.emoji) == '↩️':
                                        await msg.remove_reaction(reaction, user)
                                        await msg.edit(embed=initial())
                                        await msg.clear_reactions()
                                        self.client.loop.create_task(add_reactions(emojis))
                                        break
                                    else:
                                        await msg.remove_reaction(reaction, user)          
                                except asyncio.TimeoutError:
                                    await msg.clear_reactions()
                                    break

                        elif str(reaction.emoji) == '💸':   
                            await msg.remove_reaction(reaction, user)     
                            page = 1
                            pages = math.ceil(len(bids)/5)
                            await msg.edit(embed=bidsembedgen(page))
                            await msg.clear_reactions()
                            self.client.loop.create_task(add_reactions(menu))
                            while True:
                                try:
                                    reaction, user = await self.client.wait_for("reaction_add", timeout=30, check=check)
                                    if str(reaction.emoji) == "▶️" and page < pages:
                                        page += 1
                                        await msg.edit(embed=bidsembedgen(page))
                                        await msg.remove_reaction(reaction, user)

                                    elif str(reaction.emoji) == "◀️" and page > 1:
                                        page -= 1
                                        await msg.edit(embed=bidsembedgen(page))
                                        await msg.remove_reaction(reaction, user)
                                    elif str(reaction.emoji) == '↩️':
                                        await msg.remove_reaction(reaction, user)
                                        await msg.edit(embed=initial())
                                        await msg.clear_reactions()
                                        self.client.loop.create_task(add_reactions(emojis))
                                        break
                                    else:
                                        await msg.remove_reaction(reaction, user)          
                                except asyncio.TimeoutError:
                                    await msg.clear_reactions()
                                    break    

                        elif str(reaction.emoji) == '📈':   
                            await msg.remove_reaction(reaction, user) 
                            await msg.edit(embed=statsembedgen())    
                            await msg.clear_reactions()
                            await msg.add_reaction('↩️')                                                                                                                    
                            while True:
                                try:
                                    reaction, user = await self.client.wait_for("reaction_add", timeout=30, check=check)
                                    if str(reaction.emoji) == '↩️':
                                        await msg.remove_reaction(reaction, user)
                                        await msg.edit(embed=initial())
                                        await msg.clear_reactions()
                                        self.client.loop.create_task(add_reactions(emojis))
                                        break
                                    else:
                                        await msg.remove_reaction(reaction, user)          
                                except asyncio.TimeoutError:
                                    await msg.clear_reactions()
                                    break    

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
   
    @auctionviewer.error
    async def auctionviewer_error(self, ctx, error):
        channel = ctx.channel
        if isinstance(error, commands.CheckFailure):
            em1 = discord.Embed(title = 'Error!',
                                color = discord.Color.red(),
                                timestamp = datetime.datetime.utcnow(),
                                description = 'Please verify with the bot before sending commands')
            return await channel.send(embed=em1)   
        elif isinstance(error, commands.CommandOnCooldown):
            em1 = discord.Embed(title = 'Error!',
                    color = discord.Color.red(),
                    timestamp = datetime.datetime.utcnow(),
                    description = f'This command is on cooldown for you! Please try again in {error.retry_after:.2f}s.')
            return await ctx.send(embed=em1)

            
def setup(client):
    client.add_cog(auctionviewer(client))