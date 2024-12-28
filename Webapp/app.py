from src.logic import fetch_historical_data_live
from flask import Flask # type: ignore
import dash # type: ignore
from dash import dcc, html # type: ignore
from dash.dependencies import Input, Output # type: ignore
import plotly.graph_objs as go # type: ignore


# Initialize Flask server
server = Flask(__name__)

# Initialize Dash app
app = dash.Dash(__name__, server=server, url_base_pathname='/')
app.title = "BNB DualOptions Analytics"
app._favicon = ("birdlogo1.png")

# Define Dash layout
app.layout = html.Div(
    className="contentSection",
    children=[
        html.H1('Binance Dual Options visualizer', style={'textAlign': 'left'} ),
        html.Div(
            className="filter-divs",
            children=[
                html.Div(
                    className="filter-item",
                    children=[
                        html.Label('Choose a Direction:', style={'color': '#4682B4'}),
                        dcc.Dropdown(
                            id='putcall',
                            className='dropdown-class-1',
                            options=[
                                {'label': 'Sell High (Price to go up)', 'value': 'Put'},
                                {'label': 'Buy Low (Price to go down)', 'value': 'Call'},
                            ],
                            value='Put',  # Default value
                            clearable=False
                        )
                    ]
                ),
                html.Div(
                    className="filter-item",
                    children=[
                        html.Label('Choose a Cryptocurrency:', style={'color': '#4682B4'}),
                        dcc.Dropdown(
                            id='crypto-dropdown',
                            className='dropdown-class-2',
                            options=[
                                {'label': 'Bitcoin (BTC)', 'value': 'BTC'},
                                {'label': 'Ethereum (ETH)', 'value': 'ETH'},
                                {'label': 'Dogecoin (DOGE)', 'value': 'DOGE'},
                                {'label': 'Solana (SOL)', 'value': 'SOL'},
                            ],
                            value='BTC',  # Default value
                            clearable=False
                        )
                    ]
                ),
                html.Div(
                    className="filter-item",
                    children=[
                        html.Label('USD value at play:', style={'color': '#4682B4'}),
                        dcc.Input(
                            className="numerical-input",
                            id='numeric-input',
                            type='text',  # Accept text to allow validation
                            placeholder="Enter a number",
                            debounce=True,  # Trigger callback on 'Enter' or when the user clicks away
                        ),
                        html.Div(id='error-message', style={'color': 'red'}),
                    ]
                )

                
            ]
        )
        ,
        dcc.Graph(id='price-graph'),
    ]
)

# Define callback for dropdown interaction
@app.callback(
    Output('price-graph', 'figure'),
    [Input('crypto-dropdown', 'value')]
)
def update_graph(selected_crypto):
    symbol = f"{selected_crypto}USDC"
    df = fetch_historical_data_live(symbol)
    
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


@app.callback(
    [Output('numeric-input', 'value'),
     Output('error-message', 'children')],
    [Input('numeric-input', 'value')]
)
def validate_and_format(value):
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

# Run the server
if __name__ == '__main__':
    app.run(debug=True)
