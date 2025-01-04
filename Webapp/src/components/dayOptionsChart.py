from dash import dcc, html# type: ignore
from dash.dependencies import Input, Output, State # type: ignore
import dash_bootstrap_components as dbc # type: ignore

def create_dayOptionsChart():
    return dcc.Loading(
            id="loading-spinner2",
            type="default", 
            children=[
                html.Label('Number of days to expiration:'),
                dcc.Dropdown(id="duration-select", className="dropdown-class-2"),
                dcc.Graph(id='options-graph-day'),  # Placeholder for the graph

            ]
        )