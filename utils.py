import pprint
import hmac
import time
import hashlib
import datetime 
import time, math
from datetime import timedelta
import requests

def prettyprint_json(json_data):
    pprint.pprint(json_data)

def get_secret_bytes(secret):
    return bytes(secret,'utf-8')

def generate_timeStamp():
    return int(round(time.time()* 1000))

def generate_signature(secret_bytes,json_body):
    return hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()

def local_time(epoch_time):
    return time.strftime('%d-%m-%Y %H:%M:%S', time.localtime(int(str(epoch_time)[0:10])))

def generate_date_time(days):
    """ create a date prior to current date """
    now = datetime.datetime.now()
    date = (now - timedelta(days = days)).strftime("%d %m %Y %H:%M:%S")
    date


def to_datetime_object(date_time_string):
    datetime_data = time.strptime(date_time_string, "%d %m %Y %H:%M:%S")
    timestamp = time.mktime(datetime_data)
    #date_time_object = date_time_string_to_time(datetime_data)
     
    my_datetime = datetime.datetime.fromtimestamp(timestamp)
    
    return my_datetime


def coindcx_urls(startDate, endDate, token, interval):

    urls_to_scrape = list()

    epoch_startDate = startDate.timestamp()
    epoch_endDate = endDate.timestamp()

    if interval == '1m':
        range_end = math.ceil((epoch_endDate - epoch_startDate)/60000)
    elif interval == '5m':
        range_end = math.ceil((epoch_endDate - epoch_startDate)/(60000 * 5))
    elif interval == '15m':
        range_end = math.ceil((epoch_endDate - epoch_startDate)/(60000 * 15))
    elif interval == '30m':
        range_end = math.ceil((epoch_endDate - epoch_startDate)/(60000 * 30))
    elif interval == '1h':
        range_end = math.ceil((epoch_endDate - epoch_startDate)/(60000 * 60))
    elif interval == '2h':
        range_end = math.ceil((epoch_endDate - epoch_startDate)/(60000 * 120))
    elif interval == '4h':
        range_end = math.ceil((epoch_endDate - epoch_startDate)/(60000 * 240))
    elif interval == '6h':
        range_end = math.ceil((epoch_endDate - epoch_startDate)/(60000 * 360))
    elif interval == '8h':
        range_end = math.ceil((epoch_endDate - epoch_startDate)/(60000 * 480))
    elif interval == '1d':
        range_end = math.ceil((epoch_endDate - epoch_startDate)/(60000 * 1440))
    elif interval == '3d':
        range_end = math.ceil((epoch_endDate - epoch_startDate)/(60000 * 1440 * 3))
    elif interval == '1w':
        range_end = math.ceil((epoch_endDate - epoch_startDate)/(60000 * 1440 * 7))
    elif interval == '1M':
        range_end = math.ceil((epoch_endDate - epoch_startDate)/(60000 * 1440 * 30))

    for i in range(0,range_end):

        if interval == '1m':
            url_endDate = (datetime.datetime.fromtimestamp(epoch_startDate) + timedelta(minutes = 1000)).timestamp()
        elif interval == '5m':
            url_endDate = (datetime.datetime.fromtimestamp(epoch_startDate) + timedelta(minutes = 5000)).timestamp()
        elif interval == '15m':
            url_endDate = (datetime.datetime.fromtimestamp(epoch_startDate) + timedelta(minutes = 15000)).timestamp()
        elif interval == '30m':
            url_endDate = (datetime.datetime.fromtimestamp(epoch_startDate) + timedelta(minutes = 30000)).timestamp()
        elif interval == '1h':
            url_endDate = (datetime.datetime.fromtimestamp(epoch_startDate) + timedelta(hours = 1000)).timestamp()
        elif interval == '2h':
            url_endDate = (datetime.datetime.fromtimestamp(epoch_startDate) + timedelta(hours = 2000)).timestamp()
        elif interval == '4h':
            url_endDate = (datetime.datetime.fromtimestamp(epoch_startDate) + timedelta(hours = 4000)).timestamp()
        elif interval == '8h':
            url_endDate = (datetime.datetime.fromtimestamp(epoch_startDate) + timedelta(hours = 8000)).timestamp()
        elif interval == '1d':
            url_endDate = (datetime.datetime.fromtimestamp(epoch_startDate) + timedelta(days = 1000)).timestamp()
        elif interval == '3d':
            url_endDate = (datetime.datetime.fromtimestamp(epoch_startDate) + timedelta(days = 3000)).timestamp()
        elif interval == '1w':
            url_endDate = (datetime.datetime.fromtimestamp(epoch_startDate) + timedelta(weeks = 1000)).timestamp()
        elif interval == '1M':
            url_endDate = (datetime.datetime.fromtimestamp(epoch_startDate) + timedelta(days = 30000)).timestamp()

        if epoch_endDate > url_endDate:
            urls_to_scrape.append(f"https://public.coindcx.com/market_data/candles?pair={token}&interval={interval}&startTime={int(epoch_startDate)}000&endTime={int(url_endDate)}000&limit=1000")

            epoch_startDate = url_endDate

        if epoch_endDate < url_endDate:
            urls_to_scrape.append(f"https://public.coindcx.com/market_data/candles?pair={token}&interval={interval}&startTime={int(epoch_startDate)}000&endTime={int(epoch_endDate)}000&limit=1000")

    return urls_to_scrape
