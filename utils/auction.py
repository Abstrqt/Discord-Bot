import datetime
import time
import asyncio

from utils.auctions import *
import constants
from lib.exceptions import *

def sortbytime(lst,indexlst):
    if lst == []:
        return lst
    maxval = max(indexlst)+1
    out = []
    for x in range(0,len(lst)):
        idx = indexlst.index(min(indexlst))
        indexlst[idx] = maxval
        out.append(lst[idx])
    return out


async def scan(profileid):
    out = {'active':[],'unsold':[],'unclaimed':[]}
    times = []
    comparetime = time.time()
    playerahjson = await asyncio.gather(auctions(profileid))
    playerah = playerahjson[0]
    if playerah == HypixelAPIThrottle:
        return HypixelAPIThrottle
    elif playerah == APIError:
        return APIError

    for x in range(1,len(playerah['auctions'])+1):
        if playerah['auctions'][-x]['claimed'] == False and playerah['auctions'][-x]['end']/1000 > comparetime:
            seconds = float('%s' % (playerah['auctions'][-x]['end']/1000-time.time()))
            times.append(seconds)
            hours = int(seconds/3600)
            minutes = int((seconds/3600)%1*60)
            if hours > 0:
                endtime = '{} hours and {} minutes'.format(hours,minutes)
            elif minutes > 0:
                endtime = '{} minutes'.format(int(minutes))
            else:
                endtime = '{} seconds'.format(int(seconds))
            try:
                if playerah['auctions'][-x]['bin'] == True:
                    out['active'].append('__{} {}__ (Bin)\nBin Amount: {:,d}\nEnding in {}'.format(playerah['auctions'][-x]['tier'].capitalize(),playerah['auctions'][-x]['item_name'],playerah['auctions'][-x]['starting_bid'],endtime))
            except KeyError:
                out['active'].append('__{} {}__ (Auction)\nHighest Bid: {:,d}\nBids: {}\nEnding in {}'.format(playerah['auctions'][-x]['tier'].capitalize(),playerah['auctions'][-x]['item_name'],playerah['auctions'][-x]['highest_bid_amount'],len(playerah['auctions'][-x]['bids']),endtime))
        if playerah['auctions'][-x]['claimed'] == False and playerah['auctions'][-x]['end']/1000 <= comparetime:
            if playerah['auctions'][-x]['highest_bid_amount'] > 0:
                out['unclaimed'].append(playerah['auctions'][-x]['highest_bid_amount'])
            else:
                out['unsold'].append(playerah['auctions'][-x]['item_name'])
    out['active'] = list(dict.fromkeys(sortbytime(out['active'],times)))
    return out

async def parsebids(uuid):
    bids = []
    times = []
    tasks = []
    for pages in constants.pages:
        for auctions in pages:
            for x in range(1,len(auctions['bids'])+1):
                if auctions['bids'][-x]['bidder'] == uuid:
                    seconds = float('%s' % (auctions['end']/1000-time.time()))
                    times.append(seconds)
                    hours = int(seconds/3600)
                    minutes = int((seconds/3600)%1*60)
                    if hours > 0:
                        endtime = '{} hours and {} minutes'.format(hours,minutes)
                    elif minutes > 0:
                        endtime = '{} minutes'.format(int(minutes))
                    else:
                        endtime = '{} seconds'.format(int(seconds))
                    if auctions['bids'][-x] == auctions['bids'][-1]:
                        status = ':white_check_mark:' 
                    else:
                        status = ':x:'
                    yourbid = auctions['bids'][-x]['amount']
                    topbid = auctions['bids'][-1]['amount']
                    task = asyncio.ensure_future(namefromuuid(auctions['auctioneer']))
                    tasks.append(task)
                    if auctions['item_name'][:4] == '[Lvl':
                        bids.append('__{0} {1}__ - {2}\n>>> Top bid: {3:,d}\nYour bid: {4:,d}\nEnding in {5}\nBy '.format(auctions['tier'].capitalize(),auctions['item_name'],status,topbid,yourbid,endtime))
                        break
                    else:
                        bids.append('__{0}__ - {1}\n>>> Top bid: {2:,d}\nYour bid: {3:,d}\nEnding in {4}\nBy '.format(auctions['item_name'],status,topbid,yourbid,endtime))
                        break

    creators = await asyncio.gather(*tasks)
    if APIError in creators:
        return APIError
    for x in range(len(bids)):
        bids[x] += creators[x]
    return list(dict.fromkeys(sortbytime(bids,times)))

def stats(profilesjson,uuid):
    try:
        #buyer stats
        won = profilesjson['profile']['members'][uuid]['stats']['auctions_won']
        totalbids = profilesjson['profile']['members'][uuid]['stats']['auctions_bids']
        highestbid = profilesjson['profile']['members'][uuid]['stats']['auctions_highest_bid']
        goldspent = profilesjson['profile']['members'][uuid]['stats']['auctions_gold_spent']
        #seller stats
        created = profilesjson['profile']['members'][uuid]['stats']['auctions_created']
        fees = profilesjson['profile']['members'][uuid]['stats']['auctions_fees']
        goldearned = profilesjson['profile']['members'][uuid]['stats']['auctions_gold_earned']
        return won,totalbids,highestbid,goldspent,created,fees,goldearned
    except Exception as e:
        return False