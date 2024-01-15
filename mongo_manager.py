import logging
from pymongo import MongoClient
import settings

logger=logging.getLogger()

def write_to_mongo(data):
    client = MongoClient(settings.MONGO_URI)
    db = client[settings.MONGO_DB]

    coll = db["spot_prices"]
    logger.debug("Calling MongoDB insert_many")
    result = coll.insert_many(data)
    logger.debug("Returned from MongoDB insert_many")

    client.close()
    return result

def get_price_history(region):
    client = MongoClient(settings.MONGO_URI)
    db = client[settings.MONGO_DB]
    coll = db["spot_prices"]

    query = {"armRegionName": region}
    cursor = coll.find(query)

    a=1

