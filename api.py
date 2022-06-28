
import requests 
import hmac
import hashlib
import json
import pdb
import pprint
import pandas as pd
import time

from .urls import Urls
from .utils import coindcx_urls,to_datetime_object


class Api():

    def __init__(self,CREDENTIALS):
        
        self.key = CREDENTIALS["key"]
        self.secret = CREDENTIALS["secret"]
    
    def get(self):
        url = Urls.BASE_URL
        response = requests.get(url)
        data = response.json()
        return data

    def get_balances(self):

        url = Urls.BASE_URL+Urls.USER
        json = self.make_json()
        headers = self.make_headers()
        response = requests.post(url,data=json,headers=headers)
        return response.json()

    def get_user_info(self):
    

        url = Urls.BASE_URL+Urls.USER_INFO
        json = self.make_json()
        headers = self.make_headers()
        response = requests.post(url,data=json,headers=headers)
        return response.json()

    def get_market_details(self):
        url = Urls.BASE_URL+Urls.MARKET_DETAILS
        response = requests.get(url)
        data = response.json()
        return data

    def get_trade_history(self,pair,limit="50"):
       
        url = Urls.PUBLIC_API_BASE_URL+Urls.TRADES+"?pair="+pair+"&limit="+limit 
        response = requests.get(url)
        data = response.json()
        return data

    def get_candles(self,pair,start_time,end,interval = "5m"):
        """ Valid intervals

            m -> minutes, h -> hours, d -> days, w -> weeks, M -> months
            1m,5m,15m,30m,1h,2h,3h,6h,12h,1d,1w,1M

            pairs example B-BTC_USDT

            start_time "11 01 2021 12:00:00"
            end "11 01 2021 12:00:00"
        """
        global data
        data = None
        try:
            start_time = to_datetime_object(start_time)
            end = to_datetime_object(end)
            url = coindcx_urls(start_time, end, pair, interval)
            response = requests.get(url[0])           
            data = response.json()     
    
        except Exception as e:
            print(e)
       
        return data


    def get_ticker(self):

        url = Urls.BASE_URL+Urls.TICKER
        response = requests.get(url)
        data = response.json()
        return data

    def json_to_dframe(self,json_data):
        df = pd.json_normalize(json_data)
        return df

    def list_to_dframe(self,list_data):
        """ accepts a list of dicts and returns a dataframe 
            example: api = Api()
            tickers = api.get_ticker()
            dataframe = list_to_dframe(tickers)
        """
        df = pd.DataFrame(list_data)
        return df

    def list_to_dframe(self,dict_data):
        df=pd.DataFrame.from_dict(dict_data, orient='index')
        return df

    def prettyprint_json(self,json_data):
        pprint.pprint(json_data)

    def make_headers(self):

        timeStamp = self.generate_timeStamp()
        body = {
            "timestamp": timeStamp
            }
        json_body = json.dumps(body, separators = (',', ':'))
    
        secret_bytes = self.get_secret_bytes(self.secret)
        signature = self.generate_signature(secret_bytes,json_body)
        headers = {
            'Content-Type': 'application/json',
            'X-AUTH-APIKEY': self.key,
            'X-AUTH-SIGNATURE': signature
        }

        return headers

    def make_json(self):
        timeStamp = self.generate_timeStamp()
        body = {
            "timestamp": timeStamp
            }
        json_body = json.dumps(body, separators = (',', ':'))
        return json_body
    

    def get_secret_bytes(self,secret):

        return bytes(secret,"utf-8")

    def generate_timeStamp(self,):
        return int(round(time.time()* 1000))

    def generate_signature(self,secret_bytes,json_body):
        return hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()

