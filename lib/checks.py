import pymongo
from pymongo import MongoClient
import constants
cluster = MongoClient('mongodb+srv://{}@cluster0.dbfoh.mongodb.net/BetterSB?retryWrites=true&w=majority'.format(constants.dbtoken))
db = cluster['BetterSB']
collection = db['userInfo']

def findindb(ctx):
    post = collection.find_one({'tag': str(ctx.author)})
    if post != None:
        return True
    else:
        return False