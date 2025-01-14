from src.components.header import create_header
from src.components.footer import create_footer
from src.components.mainFilters import create_mainFilters
from src.components.allOptionsChart import create_allOptionsChart
from src.components.dayOptionsChart import create_dayOptionsChart
from src.dualInvestments import data_pandas, getData_dualInvestment, getGraph_dualInvestment_all_func, getGraph_dualInvestment_day_func
from src.generic import getData_historical_live, getGraph_historical_live, numeric_formating_validation
from flask import Flask # type: ignore
import dash # type: ignore
from dash import dcc, html# type: ignore
from dash.dependencies import Input, Output, State # type: ignore
import dash_bootstrap_components as dbc # type: ignore
import pandas as pd # type: ignore
import os
from dotenv import load_dotenv # type: ignore

load_dotenv(override=True)
GA_TRACKING_ID = os.getenv('GA_TRACKING_ID')  # Default ID

# Initialize Flask server
server = Flask(__name__)

# Initialize Dash app
app = dash.Dash(__name__, server=server, url_base_pathname='/', external_stylesheets=[dbc.themes.BOOTSTRAP])

PORT = os.environ['PORT']

# Add Google Analytics script to the index_string
app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Dual Investment(Options) Analytics</title>
        <link rel="icon" type="image/png" href="birdlogo1.png">
        <!-- Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id={GA_TRACKING_ID}"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){{dataLayer.push(arguments);}}
          gtag('js', new Date());
          gtag('config', '{GA_TRACKING_ID}');
        </script>
        {%metas%}
        {%favicon%}
        {%css%}
    </head>
    <body>
        <div id="app">
            {%app_entry%}
        </div>
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""


# Define Dash layout
app.layout = html.Div(
    className="contentSection",
    children=[
        dcc.Store(id='stored-data'),
        create_header(),
        create_mainFilters(),
        dcc.Graph(id='price-graph'),
        create_allOptionsChart(),
        create_dayOptionsChart(),
        create_footer()
    ]
)

# Callbacks
@app.callback(
    Output("price-graph", "figure"),
    Input("crypto-select", "value"),
)
def update_historical_live(selected_crypto: str):
    symbol = f"{selected_crypto}USDC"
    df = getData_historical_live(symbol)
    return getGraph_historical_live(df, selected_crypto)


@app.callback(
    [Output("numeric-input", "value"), Output("error-message", "children")],
    Input("numeric-input", "value"),
)
def validate_and_format(number_text: str):
    value, error = numeric_formating_validation(number_text)
    return value, error


@app.callback(
    [
        Output("stored-data", "data"),
        Output("duration-select", "options"),
        Output("duration-select", "value"),
        Output("strikePrice-select", "options"),
        Output("strikePrice-select", "value"),
        Output("strikePrice-label", "children"),
    ],
    Input("submit-button", "n_clicks"),
    State("putcall-select", "value"),
    State("crypto-select", "value"),
)
def update_data(n_clicks: int, option_dir: str, crypto: str):
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate

    data, durations, strike_prices = getData_dualInvestment(option_dir, crypto)
    strike_price_label = (
        "Maximum StrikePrice:" if option_dir == "PUT" else "Minimum StrikePrice:"
    )
    return (
        data,
        durations,
        durations[0],
        strike_prices,
        strike_prices[0],
        strike_price_label,
    )

@app.callback(
    Output("options-graph-overall", "figure"),
    [
        Input("stored-data", "data"),
        State("putcall-select", "value"),
        State("crypto-select", "value"),
        Input("numeric-input", "value"),
        Input("strikePrice-select", "value"),
    ],
)
def update_graphs_all(
    stored_data: dict,
    option_dir: str,
    crypto: str,
    usd_amt_string: str,
    strike_price_target: str,
):
    try:
        usd_amt = int(usd_amt_string.replace(",", ""))
        data_df = pd.DataFrame.from_records(stored_data)
        processed_data = data_pandas(data_df, crypto, usd_amt)

        overall_fig = getGraph_dualInvestment_all_func(
            processed_data, option_dir, crypto, strike_price_target
        )

        return overall_fig
    except ValueError:
        return {}
    
@app.callback(
    Output("options-graph-day", "figure"),
    [
        Input("stored-data", "data"),
        Input("duration-select", "value"),
        State("putcall-select", "value"),
        State("crypto-select", "value"),
        Input("numeric-input", "value"),
    ],
)
def update_graphs_day(
    stored_data: dict,
    duration: int,
    option_dir: str,
    crypto: str,
    usd_amt_string: str,
):
    try:
        usd_amt = int(usd_amt_string.replace(",", ""))
        data_df = pd.DataFrame.from_records(stored_data)
        processed_data = data_pandas(data_df, crypto, usd_amt)

        day_fig = getGraph_dualInvestment_day_func(
            processed_data, option_dir, crypto, duration
        )
        return day_fig
    except ValueError:
        return {}


# Run the server
if __name__ == '__main__':
    from waitress import serve
    serve(app.server, host="0.0.0.0", port=PORT, threads=8)  # Increase thread count
    # app.run(debug=True) #debug mode
