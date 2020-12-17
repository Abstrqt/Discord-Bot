import asyncio
import datetime
import aiohttp
import time

from aiohttp import ClientSession
import constants
from lib.exceptions import *

async def getpage(url,session):
    async with session.get(url) as response:
        if response.status != 200:
            return APIError
        response_json = await response.json()
        constants.pages.append(response_json['auctions'])
        return response_json

async def run():
    start_time = time.time()
    tasks = []
    url = 'https://api.hypixel.net/skyblock/auctions?key={}&page='.format(constants.key)
    async with ClientSession() as session:
        page  = await getpage(url+str(0),session)
        try:
            page = page['totalPages']+1
            for x in range(0,page):
                task = asyncio.ensure_future(getpage(url+str(x), session))
                tasks.append(task)
            responses = await asyncio.gather(*tasks)
            constants.pagerefresh = time.time()
        except Exception as e:
            pass
    #print('{} pages'.format(page))
    #print('Cached in %s seconds' % (time.time()-start_time))

async def auctions(profileid):
    url = 'https://api.hypixel.net/skyblock/auction?key={}&profile='.format(constants.key)
    try:
        async with ClientSession() as session:
            async with session.get(url+profileid) as response:
                if response.status == 429:
                    raise HypixelAPIThrottle
                elif response.status != 200:
                    raise APIError
                response_json = await response.json()
                return response_json
    except HypixelAPIThrottle:
        return HypixelAPIThrottle
    except APIError:
        return APIError


async def namefromuuid(uuid):
    url = 'https://api.mojang.com/user/profiles/{}/names'
    try:
        async with ClientSession() as session:
            async with session.get(url.format(uuid)) as response:
                if response.status != 200:
                    raise APIError
                response_json = await response.json()
                return response_json[-1]['name']
    except APIError:
        return APIError
