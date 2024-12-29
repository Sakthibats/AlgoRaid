import pandas as pd # type: ignore
from src.binance_boilerplate import boilerplate1
import plotly.graph_objs as go # type: ignore
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
def getData_historical_live(symbol):

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


def getGraph_historical_live(df, selected_crypto):
    # Create the figure
    fig = go.Figure(
        data=[go.Scatter(x=df['timestamp'], y=df['close'], mode='lines', name=selected_crypto)],
        layout=go.Layout(
            title=f'{selected_crypto}/USDC Price Over the Past Year',
            xaxis_title='Date',
            yaxis_title='Price (USDC)',
            plot_bgcolor='#fffefb',
            paper_bgcolor='#fffefb'
        )
    )
    return fig

def numeric_formating_validation(value):
    if value is None or value.strip() == "":
        return "", ""  # Reset value if empty

    try:
        # Remove commas and validate the input as a positive number
        clean_value = value.replace(",", "")
        number = float(clean_value)
        if number < 0:
            return value, "Please enter a positive number."
        
        # Format the value with commas and return
        formatted_value = f"{number:,.0f}"  # Format to 3-digit comma delimited (no decimals)
        return formatted_value, ""  # No error message
    except ValueError:
        return value, "Please enter a valid numeric value."