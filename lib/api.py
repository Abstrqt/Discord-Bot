import asyncio
import datetime
import aiohttp
import time
import json

from aiohttp import ClientSession
from lib.exceptions import *
from constants import key



async def mojangapi(ign):
    start = time.time()
    url = 'https://api.mojang.com/users/profiles/minecraft/'
    try:
        async with ClientSession() as session:
            async with session.get(url+ign) as response:
                if response.status == 204:
                    raise InvalidIGN(ign)
                elif response.status != 200:
                    raise APIError
                response_json = await response.json()
                await session.close()
                return response_json
    except InvalidIGN:
        return InvalidIGN
    except APIError:
        return APIError

async def hypixelapi(uuid):
    url = 'https://api.hypixel.net/skyblock/profiles?key={0}&uuid='.format(key)
    try:
        async with ClientSession() as session:
            async with session.get(url+uuid) as response:
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

async def hypixelprofile(profileid):
    url = 'https://api.hypixel.net/skyblock/profile?key={0}&profile='.format(key)
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

async def playerdiscord(ign):
    url = 'https://api.hypixel.net/player?key={0}&name='.format(key)
    try:
        async with ClientSession() as session:
            async with session.get(url+ign) as response:
                if response.status == 429:
                    raise HypixelAPIThrottle
                elif response.status != 200:
                    raise APIError
                response_json = await response.json()
                if response_json['player'] != None and 'DISCORD' in response_json['player']['socialMedia']['links']:
                    return response_json['player']['socialMedia']['links']['DISCORD'], response_json['player']['displayname']
                else:
                    raise KeyError
    except KeyError:
        return KeyError
    except HypixelAPIThrottle:
        return HypixelAPIThrottle
    except APIError:
        return APIError

async def guildinfo(uuid):
    try:
        async with ClientSession() as session:
            async with session.get(f'https://api.hypixel.net/guild?key={key}&player={uuid}') as response:
                if response.status != 200:
                    raise APIError
                response_json = await response.json()
                if response_json['guild'] != None:
                    guild = response_json['guild']['name']
                    for items in response_json['guild']['members']:
                        if items['uuid'] == str(uuid):
                            joined = datetime.datetime.fromtimestamp(items['joined']/1000).strftime('%m/%d/%Y')
                            rank = items['rank']
                            return guild,joined,rank
                else:
                    return None
    except APIError:
        return APIError

async def eventtime(url):
    base_url = "https://hypixel-api.inventivetalent.org/api/skyblock/"
    try:
        async with ClientSession() as session:
            async with session.get(base_url+url) as response:
                if response.status != 200:
                    raise APIError
                response_json = await response.json()
                return response_json['estimate']/1000
    except APIError:
        return APIError

async def products():
    try:
        async with ClientSession() as session:
            async with session.get(f'https://api.hypixel.net/skyblock/bazaar/products?key={key}') as response:
                if response.status != 200:
                    raise APIError
                response_json = await response.json()
                return response_json['productIds']
    except APIError:
        return APIError
            
async def productinfo(productid):
    try:
        async with ClientSession() as session:
            async with session.get(f'https://api.hypixel.net/skyblock/bazaar/product?key={key}&productId={productid}') as response:
                if response.status != 200:
                    raise APIError
                response_json = await response.json()
                return response_json['product_info']
    except APIError:
        return APIError