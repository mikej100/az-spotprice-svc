from datetime import datetime, timezone
from bson.objectid import ObjectId
import subprocess
import sys

import az_spotprice_svc as sp
import mongo_manager as mm

def test_fetch_prices():
    price_data = sp.fetch_price()
    assert( len(price_data) >= 5)
    assert( price_data[1]["currencyCode"] == "USD")

def test_write_to_mongo():
    result = sp.fetch_and_store_prices()
    ids = result.inserted_ids
    latest_id_time = ids[-1].generation_time
    seconds_since_written = (datetime.now(timezone.utc) - latest_id_time).seconds
    assert(seconds_since_written < 1.1)

def test_argparse():
    pid = subprocess.Popen([sys.executable, "az_spotprice_service.py --freq 1 --count 3"])