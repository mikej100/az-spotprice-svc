import os
# Settings for Azure assets management
#
LOG_FILE = 'logs/spot_price.log'
LOG_LEVEL = 'DEBUG'

MONGO_URI = os.environ["MONGO_CONN_STRING"]
MONGO_PORT = 27017
MONGO_DB = "azprice"

API_URI = "https://prices.azure.com/api/retail/prices?api-version=2021-10-01-preview"