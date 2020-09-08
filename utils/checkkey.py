import requests
import json

import constants

def checkkey():
    profilesjson = requests.get('https://api.hypixel.net/key?key={0}'.format(constants.key))
    totalq = profilesjson.json()['record']['totalQueries']
    qpm = profilesjson.json()['record']['queriesInPastMin']
    return totalq, qpm