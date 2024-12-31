import time
from src.binance_boilerplate import boilerplate
from src.generic import get_price
import pandas as pd # type: ignore
import plotly.express as px # type: ignore


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


def get_DualInvestment_assetPair(Direction, TargetItem, AssetItem):
    first = get_DCI_products(Direction, TargetItem, AssetItem, pageIndex=1, pageSize=100)
    full_list = first["list"]
    total = first["total"]

    for i in range(1, total//100+1):
        try:
            curr = get_DCI_products(Direction, TargetItem, AssetItem, pageIndex=i+1, pageSize=100)
            full_list.extend(curr["list"])
        except Exception as e:
            print(f"ERROR found: {e}")
            
    return full_list

def getData_dualInvestment_across_stablecoins(direction,target):

    stablecoin_list = ["USDC", "USDT", "FDUSD"]
    fin = []

    if direction=="CALL":
        for stablecoin in stablecoin_list:
            try:
                partial_data = get_DualInvestment_assetPair(direction, stablecoin, target )
                fin.extend(partial_data)
            except Exception as e:
                print(f"exception found: {e}")
    else:
        for stablecoin in stablecoin_list:
            partial_data = get_DualInvestment_assetPair(direction, target, stablecoin)
            fin.extend(partial_data)
    return fin


def getData_dualInvestment(direction, target):
    
    fin = getData_dualInvestment_across_stablecoins(direction,target)
    
    durations = set()
    strikePrices = set()
    filtered_data = []
    for item in fin:
        filtered_data.append(
            {
                "ID": item["id"],
                "InvestCoin": item["investCoin"],
                "ExercisedCoin": item["exercisedCoin"],
                "StrikePrice": item["strikePrice"],
                "Duration": item["duration"], 
                "APR": item["apr"],
                "OrderId": item["orderId"],
                "OptionType": item["optionType"]
            }
        )
        durations.add(item["duration"])
        strikePrices.add(item["strikePrice"])
        
    durations_list = sorted([int(duration) for duration in durations])
    if direction=="CALL":
        strikprices_list = sorted([float(strikprice) for strikprice in strikePrices])
    else:
        strikprices_list = sorted([float(strikprice) for strikprice in strikePrices], reverse=True)
    return filtered_data, durations_list, strikprices_list

def data_pandas(df,target, USDAmt):
    curr_price = float(get_price(f"{target}USDC")["price"])
    df["Curr_price"]  = curr_price
    df["StrikePrice"] = pd.to_numeric(df["StrikePrice"])
    df["Percent_to_strikeprice"] = 100*(df["StrikePrice"] - df["Curr_price"])/df["Curr_price"]
    df["StrikePrice"] = df.StrikePrice.astype(float)
    df["APR"] = df.APR.astype(float)
    df["PremiumReceived(USD)"] = df["APR"]*df["Duration"]*USDAmt/365
    return df

def getGraph_dualInvestment_all_func(df, direction, target, strikprice_target):
    if direction=="CALL":
        df_strikeprice = df[df["StrikePrice"]>=strikprice_target]
    else:
        df_strikeprice = df[df["StrikePrice"]<=strikprice_target]

    color_text = ['ExercisedCoin', 'InvestCoin'][direction=="PUT"]
    verbose = ["Sell-High", "Buy-Low"][direction=="PUT"]
    
    fig = px.scatter(df_strikeprice, x="Duration", y="APR", color=color_text, title=f"{target} {direction} ({verbose}) Options under Dual investment", hover_data=["PremiumReceived(USD)", "Percent_to_strikeprice", "StrikePrice", "InvestCoin"])
    
    return fig

def getGraph_dualInvestment_day_func(df, direction, target, duration):

    df_time = df[df["Duration"]==duration]

    color_text = ['ExercisedCoin', 'InvestCoin'][direction=="PUT"]
    verbose = ["Sell-High", "Buy-Low"][direction=="PUT"]

    fig = px.line(df_time, x="StrikePrice", y="APR", color=color_text, title=f"{target} {direction} ({verbose}) Options under Dual investment ({duration} days)", markers=True, hover_data=["PremiumReceived(USD)", "Percent_to_strikeprice", "StrikePrice", "InvestCoin"])

    return fig

def getDummyGraph():
    # Create an empty dataframe to pass to px
    dummy_data = pd.DataFrame({"x": [], "y": []})
    
    # Create a blank line graph with a title
    fig = px.line(
        dummy_data,
        x="x",
        y="y",
        title="No Data Available",
        markers=True
    )
    
    # Add a placeholder message using layout annotations
    fig.add_annotation(
        text="No data available please press the update graph button",
        xref="paper", yref="paper",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=20, color="red"),
        align="center"
    )
    
    # Customize axes and layout
    fig.update_layout(
        xaxis=dict(title="X-axis", visible=False),  # Hide x-axis
        yaxis=dict(title="Y-axis", visible=False),  # Hide y-axis
        plot_bgcolor="rgba(0, 0, 0, 0)",  # Transparent background
    )
    
    return fig