import pandas as pd
from src.boilerplate import boilerplate1
from dotenv import load_dotenv
import os
import requests
import time
import hashlib
import hmac
import plotly.express as px
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import json

def get_price(symbol):
    # Define the endpoint and base URL
    endpoint = '/api/v3/avgPrice'

    # Define request parameters
    params = {
        'symbol': symbol
    }

    return boilerplate1(params, endpoint)

def get_price_historical(symbol, interval):
    
    # Define the endpoint and base URL
    endpoint = '/api/v3/klines'

    # Define request parameters
    params = {
        'symbol': symbol,   
        'interval': interval  
    }
    return boilerplate1(params, endpoint)

# Function to fetch historical data from Binance
def fetch_historical_data_cache(symbol):

    # Reading the data back from the file
    with open(f'data/{symbol}.txt', 'r') as filehandles:
        klinesed = json.load(filehandles)
    
    # Create a DataFrame
    df = pd.DataFrame(
        klinesed, 
        columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time',
                 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 
                 'taker_buy_quote_asset_volume', 'ignore']
    )
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['close'] = df['close'].astype(float)
    return df[['timestamp', 'close']]

# Function to fetch historical data from Binance
def fetch_historical_data_live(symbol):

    klinesed = get_price_historical(symbol, "1d")
    
    # Create a DataFrame
    df = pd.DataFrame(
        klinesed, 
        columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time',
                 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 
                 'taker_buy_quote_asset_volume', 'ignore']
    )
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['close'] = df['close'].astype(float)
    return df[['timestamp', 'close']]