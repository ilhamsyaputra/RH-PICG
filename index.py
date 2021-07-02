import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc


# connect ke app.py
from app import app
from app import server

# connect ke pages
from apps import cuaca
from apps import gempa
from apps import index
from apps import notfound


content_style = {
    "margin-left": "2rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

content = html.Div(id='page-content', children=[], style=content_style)

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink('Cuaca', href='/cuaca')),
        dbc.NavItem(dbc.NavLink('Gempa', href='/gempa')),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem('More pages', header=True),
                dbc.DropdownMenuItem('Linkedin', href='https://www.linkedin.com/in/m-ilham-syaputra/'),
                dbc.DropdownMenuItem('Github', href='https://github.com/ilhamsyaputra'),
            ],
            nav=True,
            in_navbar=True,
            label='More',
        ),
    ],
    brand='RH-PICG',
    brand_href='/',
    color='dark',
    dark=True,
)


footer = html.Div([
    html.Hr(),
    dcc.Markdown('''
    Sumber data: BMKG - Code by [M. Ilham Syaputra](https://www.linkedin.com/in/m-ilham-syaputra/)
    '''),
], style={'margin-top': '1%', 'margin-bottom': '1%', 'margin-left': '12%', 'margin-right': '12%'})

#layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),  #https://dash.plotly.com/dash-core-components/location
    navbar,
    content,
    footer,
])

@app.callback(Output(component_id='page-content', component_property='children'),
              [Input(component_id='url', component_property='pathname')])
def display_page(pathname):
    if pathname == '/':
        app.title = 'RH-PICG'
        return index.layout
    elif pathname == '/cuaca':
        app.title = 'Gempabumi - RH-PICG'
        return cuaca.layout
    elif pathname == '/gempa':
        app.title = 'Gempabumi - RH-PICG'
        return gempa.layout
    else:
        app.title = '404 Not Found - RH-PICG'
        return notfound.layout

if __name__ == '__main__':
    app.run_server(debug=True)