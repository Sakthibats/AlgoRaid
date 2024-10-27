import os
from flask import Flask, render_template
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
# from binance.client import Client
# from dotenv import load_dotenv
import pandas as pd
import json

# Load environment variables
# load_dotenv()

# Initialize Binance client
# binance_api_key = os.getenv('API_KEY')
# binance_api_secret = os.getenv('SECRET_KEY')
# client = Client(api_key=binance_api_key, api_secret=binance_api_secret)

# Initialize Flask server
server = Flask(__name__)

# Initialize Dash app
app = dash.Dash(__name__, server=server, url_base_pathname='/')

# Define Dash layout
app.layout = html.Div(
    style={'backgroundColor': '#f0f8ff', 'textAlign': 'center', 'fontFamily': 'Arial'},
    children=[
        html.H1('Algoraid Options', style={'color': '#1E90FF'}),
        html.Label('Choose a Cryptocurrency:', style={'color': '#4682B4'}),
        dcc.Dropdown(
            id='crypto-dropdown',
            options=[
                {'label': 'Bitcoin (BTC)', 'value': 'BTC'},
                {'label': 'Ethereum (ETH)', 'value': 'ETH'},
                {'label': 'Dogecoin (DOGE)', 'value': 'DOGE'},
                {'label': 'Solana (SOL)', 'value': 'SOL'},
            ],
            value='BTC',  # Default value
            style={'width': '50%', 'margin': 'auto'}
        ),
        dcc.Graph(id='price-graph'),
    ]
)

# Function to fetch historical data from Binance
def fetch_historical_data(symbol):
    # klines = client.get_historical_klines(
    #     symbol,
    #     Client.KLINE_INTERVAL_1DAY,
    #     "1 year ago UTC"
    # )
    # print(klines)

    # with open(f'data/{symbol}.txt', 'w') as filehandle:
    #     json.dump(klines, filehandle)

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

# Define callback for dropdown interaction
@app.callback(
    Output('price-graph', 'figure'),
    [Input('crypto-dropdown', 'value')]
)
def update_graph(selected_crypto):
    symbol = f"{selected_crypto}USDC"
    df = fetch_historical_data(symbol)
    
    # Create the figure
    fig = go.Figure(
        data=[go.Scatter(x=df['timestamp'], y=df['close'], mode='lines', name=selected_crypto)],
        layout=go.Layout(
            title=f'{selected_crypto}/USDC Price Over the Past Year',
            xaxis_title='Date',
            yaxis_title='Price (USDC)',
            plot_bgcolor='#f0f8ff',
            paper_bgcolor='#f0f8ff'
        )
    )
    return fig

# Define Flask route
@server.route('/')
def index():
    return render_template('index.html')

# Run the server
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
