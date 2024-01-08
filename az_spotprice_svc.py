#!/bin/python3
#!/usr/bin/python3
#!/usr/bin/python3
#
#
# Code derived from https://learn.microsoft.com/en-gb/rest/api/cost-management/retail-prices/azure-retail-prices
#
import argparse
import datetime
import json
import logging
import logging.config
import requests
import settings
import threading
from time import sleep
import yaml

from mongo_manager import write_to_mongo



with open("./logging.yaml", "r") as stream:
    config = yaml.load(stream, Loader=yaml.FullLoader)
logging.config.dictConfig(config)
logger = logging.getLogger()

def main():
    parser = argparse.ArgumentParser(description = "Azure spot price capturing")
    parser.add_argument('-i', '--interval', 
                        type=int, default=300,
                        help="number of seconds between fetching data")
    parser.add_argument('-c', '--count', 
                        type=int, default=-1,
                        help="count of fetches (-1 for indefinitely)")
    args = parser.parse_args()
    
    poll_price(args.interval, args.count)

def poll_price(interval, count):

    fetch_and_store_prices()
    
    sleep(interval)
    count = count - 1
    if (count != 0 ): 
        poll_price(interval, count)


def fetch_and_store_prices() :
    prices = fetch_price()
    timestamp = datetime.datetime.now()
    prices_with_date = prices
    [p.update({"timestamp": timestamp}) for p in prices_with_date]
    result = write_to_store(prices_with_date)
    #logger.info("Fetched only Azure spot pricing")
    logger.info("Fetched and stored Azure spot pricing")
    return result

def fetch_price():
    query = "armSkuName eq 'Standard_NC4as_T4_v3' and priceType eq 'Consumption' and contains(meterName, 'Spot')"

    response = requests.get(settings.API_URI, params={'$filter': query})
    response_data = json.loads(response.text)
    
    price_data = response_data["Items"]
    nextPage = response_data['NextPageLink']
    
    while(nextPage):
        response = requests.get(nextPage)
        response_data = json.loads(response.text)
        nextPage = response_data['NextPageLink']
        price_data.append(response_data["Items"])

    return price_data


def write_to_store(data):
    return write_to_mongo(data)

if __name__ == "__main__":
    main()