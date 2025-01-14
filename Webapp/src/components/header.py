from dash import dcc, html# type: ignore

def create_header():
    return html.Div(
        children=[
            html.H1('Dual Investment Visualizer', style={'textAlign': 'left'}),
            html.P(
                children=[
                    "Binance Dual Investments simplify Covered Calls and Cash-Secured Puts for crypto assets, offering users a streamlined way to earn returns. This tool visualizes the Annual Percentage Rate (APR) of various Dual Investments available on Binance, helping users make informed decisions. Learn more about Binance Dual Investments by visiting the ",
                    html.A(
                        "official FAQ",
                        href="https://www.binance.com/en/dual-investment",
                        target="_blank",
                    ),
                    "."
                ]
            ),
            html.Hr(style={'border': '1px solid #ccc', 'margin': '20px 0'}),
        ]
    )