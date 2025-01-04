from dash import dcc, html# type: ignore
from dash.dependencies import Input, Output, State # type: ignore
import dash_bootstrap_components as dbc # type: ignore

def create_allOptionsChart():
    return dcc.Loading(
            id="loading-spinner1",
            type="default", 
            children=[
                html.Label("StricePrice Filter", id="strikePrice-label"),
                dcc.Dropdown(id="strikePrice-select", className="dropdown-class-2"),
                dcc.Graph(id='options-graph-overall'),  # Placeholder for the graph
            ]
        )