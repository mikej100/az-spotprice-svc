import logging
from pymongo import MongoClient
import settings

def write_to_mongo(data):
    client = MongoClient(settings.MONGO_URI)
    db = client[settings.MONGO_DB]
    logging.debug("Connected to MongoDB") 

    coll = db["spot_prices"]
    result = coll.insert_many(data)

    client.close()
    return result

def get_price_history(region):
    client = MongoClient(settings.MONGO_URI)
    db = client[settings.MONGO_DB]
    coll = db["spot_prices"]

    query = {"armRegionName": region}
    cursor = coll.find(query)

    a=1

