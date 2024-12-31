from src.dualInvestments import data_pandas, getData_dualInvestment, getDummyGraph, getGraph_dualInvestment_all_func, getGraph_dualInvestment_day_func
from src.generic import getData_historical_live, getGraph_historical_live, numeric_formating_validation
from flask import Flask # type: ignore
import dash # type: ignore
from dash import dcc, html# type: ignore
from dash.dependencies import Input, Output, State # type: ignore
import plotly.graph_objs as go # type: ignore
import dash_bootstrap_components as dbc # type: ignore
import pandas as pd # type: ignore



# Initialize Flask server
server = Flask(__name__)

# Initialize Dash app
app = dash.Dash(__name__, server=server, url_base_pathname='/', external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "DualOptions Analytics"
app._favicon = ("birdlogo1.png")

# Define Dash layout
app.layout = html.Div(
    className="contentSection",
    children=[
        html.H1('Binance Dual Options visualizer', style={'textAlign': 'left'} ),
        html.Div(
            className="filter-divs",
            children=[
                dcc.Store(id='stored-data'),
                html.Div(
                    className="filter-item",
                    children=[
                        html.Label('Choose a Direction:'),
                        dcc.Dropdown(
                            id='putcall-select',
                            className='dropdown-class-1',
                            options=[
                                {'label': 'Sell High (Price to go up)', 'value': 'CALL'},
                                {'label': 'Buy Low (Price to go down)', 'value': 'PUT'},
                            ],
                            value='CALL',  # Default value
                            clearable=False
                        )
                    ]
                ),
                html.Div(
                    className="filter-item",
                    children=[
                        html.Label('Choose a Cryptocurrency:', style={'color': '#4682B4'}),
                        dcc.Dropdown(
                            id='crypto-select',
                            className='dropdown-class-2',
                            options=[
                                {'label': 'Bitcoin (BTC)', 'value': 'BTC'},
                                {'label': 'Ethereum (ETH)', 'value': 'ETH'},
                                {'label': 'Binance Coin (BNB)', 'value': 'BNB'},
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
                        dbc.Input(
                            className="numerical-input",
                            id='numeric-input',
                            type='text',  # Accept text to allow validation
                            placeholder="Enter a number",
                            debounce=True,  # Trigger callback on 'Enter' or when the user clicks away
                            autoComplete="off",
                            value="10,000"
                        ),
                        html.Div(id='error-message', style={'color': 'red'}),
                    ]
                ),
                html.Div(
                    className="filter-item",
                    children=[
                        dbc.Button("Update Graph", 
                                    className="submit-button",
                                    id='submit-button', 
                                    n_clicks=0)
                    ]
                ),
            ]
        ),
        dcc.Graph(id='price-graph'),

        # Loading spinner
        dcc.Loading(
            id="loading-spinner",
            type="default",  # Spinner type: "circle", "dot", or "default"
            children=[
                html.Label( id="strikePrice-label", style={'color': '#4682B4'}),
                dcc.Dropdown(id="strikePrice-select", className="dropdown-class-2"),
                dcc.Graph(id='options-graph-overall'),  # Placeholder for the graph
                html.Label('Number of days to expiration:', style={'color': '#4682B4'}),
                dcc.Dropdown(id="duration-select", className="dropdown-class-2"),
                dcc.Graph(id='options-graph-day'),  # Placeholder for the graph
            ]
        ),
        html.Div(id='error-message2', style={'color': 'red'}),

    ]
)

@app.callback(
    Output('price-graph', 'figure'),
    [Input('crypto-select', 'value')]
)
def update_historical_live(selected_crypto):
    symbol = f"{selected_crypto}USDC"
    df = getData_historical_live(symbol)
    fig = getGraph_historical_live(df, selected_crypto)
    return fig

@app.callback(
    [Output('numeric-input', 'value'),
     Output('error-message', 'children')],
    [Input('numeric-input', 'value')]
)
def validate_and_format(number_text):
    value, error = numeric_formating_validation(number_text)
    return value, error
    
@app.callback(
    Output('stored-data', 'data'),
    Output("duration-select", "options"),
    Output("duration-select", "value"),
    Output("strikePrice-select", "options"),
    Output("strikePrice-select", "value"),
    Output("strikePrice-label", "children"),
    Input('submit-button', 'n_clicks'),
    State('putcall-select', 'value'),
    State('crypto-select', 'value'),
)
def makeGraph_dualInvestment_all_func(n_clicks, option_dir, crypto):
    if n_clicks is None:
        # If the button hasn't been clicked, prevent any action
        raise dash.exceptions.PreventUpdate
    data, durations,strikprices = getData_dualInvestment( option_dir, crypto)
    strikeprice_label = f"{["Minimum", "Maximum"][option_dir=="PUT"]} StrikePrice:"
    return data, durations, durations[0], strikprices, strikprices[0], strikeprice_label



@app.callback(
    Output('options-graph-overall', 'figure'),
    Output('options-graph-day', 'figure'),
    Input('stored-data', 'data'),
    Input("duration-select", "value"),
    State('putcall-select', 'value'),
    State('crypto-select', 'value'),
    Input('numeric-input', 'value'),
    Input("strikePrice-select", "value"),
)
def makeGraph_dualInvestment_day_func(stored_data, duration, option_dir, crypto, usd_amt_string, strikprice_target):
    USDAmt = int("".join(usd_amt_string.split(",")))
    data_df = pd.DataFrame.from_records(stored_data)
    data = data_pandas(data_df, crypto, USDAmt)
    getGraph_dualInvestment_all = getGraph_dualInvestment_all_func(data, option_dir, crypto, strikprice_target)
    getGraph_dualInvestment_day = getGraph_dualInvestment_day_func(data, option_dir, crypto, duration)
    return getGraph_dualInvestment_all, getGraph_dualInvestment_day


# Run the server
if __name__ == '__main__':
    from waitress import serve
    serve(app.server, host='0.0.0.0', port=8050, threads=8)  # Increase thread count
    # app.run(debug=True) #debug mode
