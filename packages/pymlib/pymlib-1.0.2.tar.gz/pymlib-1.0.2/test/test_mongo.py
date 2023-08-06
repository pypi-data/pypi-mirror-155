# coding: utf-8

import mlib

mlib.initMongo(uri="mongodb://root:rootPass@10.0.0.13:27017/?authSource=admin")

mongo = mlib.getMongoClient()

r = mongo["logs"]["logs"].find_one({})
print(r)