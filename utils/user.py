import asyncio
import pymongo
from pymongo import MongoClient
import constants
cluster = MongoClient('mongodb+srv://{}@cluster0.dbfoh.mongodb.net/BetterSB?retryWrites=true&w=majority'.format(constants.dbtoken))
db = cluster['BetterSB']
collection = db['userInfo']

from lib import api
from lib.exceptions import *
compare = []


async def findprofile(ign,member,profile):
    compare = []
    lastsave = 0
    post = None
    if ign == "":
        post = collection.find_one({'tag': str(member)})
        ign = post['name']

    mojangresponse = await asyncio.gather(api.mojangapi(ign))
    mojangresponse = mojangresponse[0]
    if mojangresponse == InvalidIGN:
        return InvalidIGN
    elif mojangresponse == APIError:
        return APIError
    ign = mojangresponse['name']
    uuid = mojangresponse['id']

    if post == None or profile != '':

        hypixelresponse = await asyncio.gather(api.hypixelapi(uuid))
        hypixelresponse = hypixelresponse[0]
        if hypixelresponse == HypixelAPIThrottle:
            return HypixelAPIThrottle
        elif hypixelresponse['profiles'] == None:
            return NeverPlayedSkyblockError

        profilename = None
        if profile == "":
            for x in range(0,len(hypixelresponse['profiles'])):
                if 'last_save' in hypixelresponse['profiles'][x]['members'][uuid] and hypixelresponse['profiles'][x]['members'][uuid]['last_save'] >= lastsave: 
                    lastsave = hypixelresponse['profiles'][x]['members'][uuid]['last_save']
                    profilename = hypixelresponse['profiles'][x]['cute_name']
        elif profile != "":
            profilename = profile.capitalize()

        for x in range(0,len(hypixelresponse['profiles'])):
            compare.append(hypixelresponse['profiles'][x]['cute_name'])
            if hypixelresponse['profiles'][x]['cute_name'] == profilename:
                profileid = hypixelresponse['profiles'][x]['profile_id']            
        if profilename in compare:
            return ign, uuid, profilename, profileid
        return BadProfileError

    else:
        return post['name'], post['uuid'], post['profilename'], post['profileid']


async def playerjson(profileid):
    response = await asyncio.gather(api.hypixelprofile(profileid))
    return response[0]

async def allprofiles(ign):
    mojangresponse = await asyncio.gather(api.mojangapi(ign))
    hypixelresponse = await asyncio.gather(api.hypixelapi(mojangresponse[0]['id']))
    hypixelresponse = hypixelresponse[0]
    if hypixelresponse == HypixelAPIThrottle:
        return HypixelAPIThrottle
    elif hypixelresponse['profiles'] == None:
        return NeverPlayedSkyblockError

    profiles = ''
    for x in range(0,len(hypixelresponse['profiles'])):
        profilename = hypixelresponse['profiles'][x]['cute_name']
        profiles += profilename
        profiles += ', '
    return profiles[:-2]