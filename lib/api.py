import asyncio
import datetime
import aiohttp
import time
import requests
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

def guildinfo(uuid):
    try:
        response = requests.get('https://api.hypixel.net/guild?key={0}&player={1}'.format(key,uuid))
        if response.status_code != 200:
            raise APIError
        response = response.json()
        if response['guild'] != None:
            guild = response['guild']['name']
            for items in response['guild']['members']:
                if items['uuid'] == str(uuid):
                    joined = datetime.datetime.fromtimestamp(items['joined']/1000).strftime('%m/%d/%Y')
                    rank = items['rank']
                    return guild,joined,rank
        else:
            return None
    except APIError:
        return APIError
    