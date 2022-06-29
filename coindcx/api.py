
import requests 
import hmac
import hashlib
import json
import pdb
import pprint

import time
import random
import string
import pandas as pd

from coindcx.request import Request
from coindcx.urls import(
    BASE_URL,
    USER,
    USER_INFO,
    MARKET_DETAILS,
    PUBLIC_API_BASE_URL,
    TRADES,
    TICKER,
    NEW_ORDER,
    CANCEL_ORDER,
    CANCEL_BY_IDS,
    ORDER_STATUS,
    EDIT_ORDER_PRICE
)

from .utils import get_coindcx_url,to_datetime_object

class Api:

    def __init__(self,CREDENTIALS):
        
        self.key = CREDENTIALS["key"]
        self.secret = CREDENTIALS["secret"]
    
    def get_base_data(self):
        url = BASE_URL
        response = requests.get(url)
        return response

    def get_balances(self):

        url = BASE_URL+USER
        json = self.make_json()
        headers = self.make_headers()
        response = requests.post(url,data=json,headers=headers)
        return response

    def get_user_info(self):
    
        url = BASE_URL+USER_INFO
        json = self.make_json()
        headers = self.make_headers()
        response = requests.post(url,data=json,headers=headers)
        return response

    def get_market_details(self):
        url = BASE_URL+MARKET_DETAILS
        response = requests.get(url)
        return response

    def get_trade_history(self,pair,limit="50"):
       
        url = PUBLIC_API_BASE_URL+TRADES+"?pair="+pair+"&limit="+limit 
        response = requests.get(url)
        return response

    def get_candles(self,pair,start_time,end,interval = "5m"):
        
        start_time = to_datetime_object(start_time)
        end = to_datetime_object(end)
        url = get_coindcx_url(start_time, end, pair, interval)
        response = requests.get(url[0])           
        return response    
   
    def get_ticker(self):

        url = BASE_URL+TICKER
        response =requests.get(url)
        return response

    def limit_order(self,side,order_type,market,price_per_unit,total_quantity):
        timeStamp = self.generate_timeStamp()
        length  = 10
        letters = string.ascii_lowercase
        order_id = ''.join(random.choice(letters) for i in range(length))
        body = {
          "side":side,    #Toggle between 'buy' or 'sell'.
          "order_type": order_type, #Toggle between a 'market_order' or 'limit_order'.
          "market": market, 
          "price_per_unit":price_per_unit, #This parameter is only required for a 'limit_order'
          "total_quantity": total_quantity, #Replace this with the quantity you want
          "timestamp": timeStamp,
          "client_order_id": order_id #Replace this with the client order id you want
        }
        
        json_body = self.make_json_body(body)
        secret_bytes = self.get_secret_bytes(self.get_secret())
        signature = self.generate_signature(secret_bytes, json_body)
        url = BASE_URL+NEW_ORDER
        headers = self.make_headers(signature)
        response = self.post(url, data = json_body, headers = headers)
        return response

    def cancel_order(self,order_id):
        url = BASE_URL+CANCEL_ORDER
        body = {
            "id": order_id, 
            "timestamp": self.generate_timeStamp()
        }
        response = self.send_request(url,body)
        return response

    def get_order_status(self,order_id):
        url = BASE_URL+ORDER_STATUS
        body = {
            "id": order_id,
            "timestamp": self.generate_timeStamp()
        }
        response = self.send_request(url,body)
        return response

    def cancle_multiple_orders(self,ids = []):
        url = BASE_URL+CANCEL_BY_IDS
        body = {
            "ids": ids,
        }
        response = self.send_request(url,body)
        return response

    def edit_order_price(self,order_id,new_price):
        url = BASE_URL+EDIT_ORDER_PRICE
        body = {
            "id": order_id, 
            "timestamp": self.generate_timeStamp(),
            "price_per_unit": new_price 
        }
        response = self.send_request(url,body)
        return response

    def send_request(self,url,body = {}):
        json_body = self.make_json_body(body)
        secret_bytes = self.get_secret_bytes(self.get_secret())
        signature = self.generate_signature(secret_bytes, json_body)
        headers = self.make_headers(signature)
        response = requests.post(url, json_body, headers)
        return response



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

