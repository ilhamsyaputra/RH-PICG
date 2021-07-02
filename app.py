import dash
import dash_bootstrap_components as dbc


app = dash.Dash(__name__, suppress_callback_exceptions=True,
                meta_tags=[
                    {"name": "viewport",
                     'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}
                ],
                external_stylesheets=[dbc.themes.BOOTSTRAP]
                )
server = app.server
