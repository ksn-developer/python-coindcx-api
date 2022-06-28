import requests 
import hmac
import hashlib
import json
import time



BASE_URL = "https://api.coindcx.com"
PUBLIC_API_BASE_URL = "https://public.coindcx.com"

TICKER = "/exchange/ticker"
MARKETS = "/exchange/v1/markets"
MARKET_DETAILS = "/exchange/v1/markets_details"
TRADES = "/market_data/trade_history"
ORDER_BOOK = "/market_data/orderbook"
CANDLES = "/market_data/candles"
USER = "/exchange/v1/users/balances"
USER_INFO="/exchange/v1/users/info"
NEW_ORDER="/exchange/v1/orders/create"
ORDER_STATUS = "/exchange/v1/orders/status"
ACTIVE_ORDER_STATUS="/exchange/v1/orders/active_orders_count"
CANCEl_ALL = "/exchange/v1/orders/cancel_all"
CANCEl_BY_ID = "/exchange/v1/orders/cancel_by_ids"
CANCEl ="/exchange/v1/orders/cancel"
PLACE_ORDER="/exchange/v1/margin/create"
CANCEl_ORDER="/exchange/v1/margin/cancel"
EXIT="/exchange/v1/margin/exit"
STOP_LOSS="/exchange/v1/margin/edit_sl"
EDIT_STOP_LOSS="/exchange/v1/margin/edit_trailing_sl"
MARGIN_ORDER="/exchange/v1/margin/add_margin"
REMOVE_MARGIN = "/exchange/v1/margin/remove_margin"
FETCH_ORDER="/exchange/v1/margin/fetch_orders"
QUERY_ORDER="/exchange/v1/margin/order"


def get_secret_bytes(secret):
    return bytes(secret,'utf-8')

def generate_timeStamp():
    return int(round(time.time()* 1000))

def generate_signature(secret_bytes,json_body):
    return hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()

