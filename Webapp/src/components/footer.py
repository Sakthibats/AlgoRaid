
from dash import dcc, html# type: ignore


def create_footer():
    return html.Footer(
        children=[
            html.P("© 2025 Dual Investment(Options) Analytics", style={'marginBottom': '10px'}),
            html.P(
                "The tools and information provided here are for informational purposes only and do not constitute financial advice.",
                style={'fontSize': '12px', 'color': '#777', 'marginBottom': '15px'}
            ),
            html.Div(
                children=[
                    # GitHub Logo and Link
                    html.A(
                        children=[
                            html.Img(
                                src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg",
                                alt="GitHub",
                                style={'height': '24px', 'marginRight': '10px'}
                            ),
                        ],
                        href="https://github.com/Sakthibats/AlgoRaid",
                        target="_blank",
                        style={'textDecoration': 'none', 'color': '#4682B4', 'marginRight': '20px'}
                    ),
                    # LinkedIn Logo and Link
                    html.A(
                        children=[
                            html.Img(
                                src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/81/LinkedIn_icon.svg/1200px-LinkedIn_icon.svg.png",
                                alt="LinkedIn",
                                style={'height': '24px', 'marginRight': '10px'}
                            ),
                        ],
                        href="https://www.linkedin.com/in/sakthibas98/",
                        target="_blank",
                        style={'textDecoration': 'none', 'color': '#4682B4', 'marginRight': '20px'}
                    )
                ],
                style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'gap': '15px'}
            )
        ],
        style={
            'textAlign': 'center',
            'padding': '20px',
            'backgroundColor': '#fffefb',
            'borderTop': '1px solid #ccc',
            'marginTop': '20px'
        }
    )