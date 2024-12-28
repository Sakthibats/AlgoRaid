import time
from src.binance_boilerplate import boilerplate
from src.binance_boilerplate import boilerplate1
from src.generic import get_price
import pandas as pd
import plotly.express as px


def get_DCI_products(optionType, exercisedCoin, investCoin, pageSize, pageIndex):

    # Define the endpoint and base URL
    endpoint = '/sapi/v1/dci/product/list'

    # Define request parameters
    params = {
        'optionType': optionType,  #'CALL' or 'PUT'
        'exercisedCoin': exercisedCoin,  # Target exercised asset
        'investCoin': investCoin,  # Asset used for subscribing
        'pageSize': pageSize,  # Optional
        'pageIndex': pageIndex,  # Optional
        'recvWindow': 60000,  # Optional
        'timestamp': int(time.time() * 1000)  # Current timestamp in milliseconds
    }

    return boilerplate(params, endpoint)


def get_DualInvestment_assetPair(Direction, TargetItem, AssetItem, USDamt, curr_price):
    print(Direction, TargetItem, AssetItem)
    first = get_DCI_products(Direction, TargetItem, AssetItem, pageIndex=1, pageSize=1)
    full_list = first["list"]
    total = first["total"]
    print(total)

    for i in range(total//100+1):
        try:
            curr = get_DCI_products(Direction, TargetItem, AssetItem, pageIndex=i+1, pageSize=100)
            full_list.extend(curr["list"])
        except Exception as e:
            print(f"ERROR found: {e}")

    print("---------------------------")
    print(len(full_list))
    df = pd.DataFrame(full_list)
    df["curr_price"]  = curr_price
    df["strikePrice"] = pd.to_numeric(df["strikePrice"])

    df["Percent_to_strikeprice"] = 100*(df["strikePrice"] - df["curr_price"])/df["curr_price"]

    df = df.sort_values(by=['apr', 'duration'], ascending=[False, True])
    df["strikePrice"] = df.strikePrice.astype(float)
    df["apr"] = df.apr.astype(float)
    df["1000return"] = df["apr"]*df["duration"]*1000/365
    df["USDamt"] = df["1000return"]*USDamt/1000
    return df

def get_dualInvestment_options(direction, target, USDamt):

    curr_price = float(get_price(f"{target}USDC")["price"]) #ETH

    print(f"{target} price {curr_price}")

    listt = ["USDC", "USDT", "FDUSD"]
    fin = []

    if direction=="CALL":
        for i in listt:
            try:
                partial_df = get_DualInvestment_assetPair(direction, i, target, USDamt, curr_price)
                fin.append(partial_df)
            except Exception as e:
                print(f"exception found: {e}")
    else:
        for i in listt:
            partial_df = get_DualInvestment_assetPair(direction, target, i, USDamt, curr_price)
            fin.append(partial_df)

    df = pd.concat(fin)

    df_copy = df[df["duration"]<=20]

    return df

def getGraph_dualInvestment_options_all_func(df_copy, direction):

    if direction=="CALL":
        fig = px.scatter(df_copy, x="duration", y="apr", color='exercisedCoin', hover_data=["1000return", "USDamt", "Percent_to_strikeprice", "strikePrice"])
    else:
        fig = px.scatter(df_copy, x="duration", y="apr", color='investCoin', hover_data=["1000return", "USDamt", "Percent_to_strikeprice", "strikePrice"])
    
    return fig