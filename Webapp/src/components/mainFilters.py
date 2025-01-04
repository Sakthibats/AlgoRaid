from dash import dcc, html# type: ignore
from dash.dependencies import Input, Output, State # type: ignore
import dash_bootstrap_components as dbc # type: ignore

def create_mainFilters():
    return html.Div(
            className="filter-divs",
            children=[
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
                        html.Label('Choose a Cryptocurrency:'),
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
                        html.Label('USD value at play:'),
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
        )
