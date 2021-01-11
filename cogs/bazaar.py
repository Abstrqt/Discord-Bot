import discord
from discord.ext import commands

import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style
import datetime
from datetime import timedelta
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
import io
from lib import api
from lib.exceptions import *
from utils.player import nicenum

original = ['INK_SACK:3','INK_SACK:4','LOG_2:1','HUGE_MUSHROOM_1','HUGE_MUSHROOM_2','ENCHANTED_HUGE_MUSHROOM_1','ENCHANTED_HUGE_MUSHROOM_2',
        'RAW_FISH:2','RAW_FISH:3','RAW_FISH:1','LOG:1','LOG:3','LOG:2','LOG_2','SULPHUR','BAZAAR_COOKIE']

converted = ['COCOA_BEAN','LAPIS_LAZULI','DARK_OAK_WOOD','BROWN_MUSHROOM_BLOCK','RED_MUSHROOM_BLOCK','ENCHANTED_BROWN_MUSHROOM_BLOCK','ENCHANTED_RED_MUSHROOM_BLOCk',
        'CLOWNFISH','PUFFERFISH','RAW_SALMON','SPRUCE_WOOD','JUNGLE_WOOD','BIRCH_WOOD','ACACIA_WOOD','GUNPOWDER']

class bazaar(commands.Cog):
    
    def __init__(self,client):
        self.client= client

    @commands.command(aliases=['bz'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def bazaar(self,ctx, *args):
        try: 
            if str(args) == '()':
                raise Exception
            channel = ctx.channel
            member = ctx.message.author
            searchfor = list(args)
            em1 = discord.Embed(title = 'Finding closest match to ``{}`` . . .'.format(' '.join(searchfor)), color = 0x5e7dc5)
            em1.add_field(name = 'Please be patient', value = '\u200b', inline= False)
            msg = await channel.send(embed=em1)

            products = await api.products()
            if products == APIError:
                raise APIError

            match = "x"
            highC = 0
            curC = 0
            for item in [ele for ele in products if ele not in original]+converted:
                if searchfor[0] == 'sc3k':
                    match = 'SUPER_COMPACTOR_3000'
                curItem = item.replace('_',' ').lower().split(" ")
                if len(curItem) < len(searchfor):
                    continue
                if searchfor[0] == 'e' or searchfor[0] == 'ench':
                    searchfor[0] = 'enchanted'
                curC = 0
                for i in range (len(searchfor)):
                    for k in range(len(curItem)):
                        for j in range (min(len(searchfor[i]), len(curItem[k]))):
                            if searchfor[i][j] == curItem[k][j] and searchfor[i][0] == curItem[k][0]:
                                curC += 1

                    if curC > highC:
                        highC = curC
                        match = item
                    elif highC/len(match.replace('_','')) < curC/len(''.join(curItem)) and curC == highC:
                        highC = curC
                        match = item

            productid = match 
            if match in converted:
                productid = original[converted.index(match)]

            data = await api.productinfo(productid)
            if data == APIError:
                raise APIError

            plt.style.use('dark_background')
            match = match.replace('_',' ').title()
            dates = []
            buy = []
            sell = []
            for x in range(0,len(data['week_historic']),4):
                if data['week_historic'][x]['buyVolume'] !=0 and data['week_historic'][x]['sellVolume'] != 0:
                    dates.append(datetime.datetime.fromtimestamp(data['week_historic'][x]['timestamp']/1000)) 
                    buy.append(data['week_historic'][x]['buyCoins']/data['week_historic'][x]['buyVolume'])
                    sell.append(data['week_historic'][x]['sellCoins']/data['week_historic'][x]['sellVolume'])

            fig, ax = plt.subplots(figsize = (10,8))

            plt.title('Click to Enlarge')
            plt.plot_date(dates,buy,color='#47a0ff', linestyle='-', ydate=False, xdate=False,label='Buy')
            plt.plot_date(dates,sell,color='#fac32a', linestyle='-', ydate=False, xdate=False,label='Sell')
            plt.figtext(0.5, 0.01, f'*{buy[-1]-buy[0]:+.2f} in buy price and {sell[-1]-sell[0]:+.2f} in sell price in the past week', wrap=True,horizontalalignment='center', fontsize=18)

            loc = mdates.DayLocator()
            formatter = DateFormatter('%d %b')
            ax.xaxis.set_major_locator(loc)
            ax.xaxis.set_major_formatter(formatter)
            ax.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
            ax.legend(loc='upper right',bbox_to_anchor=(1,1.15), fancybox=True, facecolor='0.2')
            ax.yaxis.grid()
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_visible(False)
            plt.savefig('./images/graph.png', transparent=True)
            plt.close(fig)

            with open('./images/graph.png', 'rb') as f:
                file = io.BytesIO(f.read())
            
            image = discord.File(file, filename='graph.png')

            embed = discord.Embed(title = '{}*'.format(match), url = 'https://stonks.gg/search?input={}'.format(match.replace(' ','+')), color = discord.Color.blue(), timestamp = datetime.datetime.utcnow())
            embed.add_field(name='Buy Price: {} \nBuy Volume: {}'.format(nicenum(data['buy_summary'][0]['pricePerUnit']), nicenum(data['quick_status']['buyVolume'])),value='\u200b')
            embed.add_field(name='Sell Price: {}\nSell Volume: {}'.format(nicenum(data['sell_summary'][0]['pricePerUnit']), nicenum(data['quick_status']['sellVolume'])),value='\u200b')
            embed.set_thumbnail(url=f'https://sky.lea.moe/item/{productid}')
            embed.set_image(url=f'attachment://graph.png')
            embed.set_footer(icon_url = member.avatar_url, text = f'Requested by {ctx.author} ')
            await msg.delete()
            await channel.send(file=image, embed=embed)
        
        except (APIError):
            embed = discord.Embed(title = 'Error!', color = discord.Color.red(),description='There was an issue contacting the API')
            await msg.edit(embed=embed)
        except Exception:
            embed = discord.Embed(title = 'Error!', color = discord.Color.red(),description='Please give a product name')
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(bazaar(client))