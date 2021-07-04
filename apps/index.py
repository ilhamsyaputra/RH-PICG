import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from app import app

app.title = 'RH Portal Informasi Cuaca dan Gempabumi'

layout = html.Div([
    html.H1('Portal Informasi Cuaca dan Gempabumi Indonesia'),
    html.P('Sumber Data: BMKG'),
    html.Hr(),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardImg(src='../assets/cuaca.svg', top=True),
                dbc.CardBody([
                    html.H4('Data Prakiraan Cuaca', className='card-title'),
                    html.P('Data prakiraan cuaca kabupaten dan kota di Indonesia',
                           className='card-text'),
                    dbc.Button('SELENGKAPNYA', href='/cuaca', color='primary'),
                ]),
            ], style={'width': '18rem'})
        ], width='auto'),
        dbc.Col([
            dbc.Card([
                dbc.CardImg(src='../assets/gempa.svg', top=True),
                dbc.CardBody([
                    html.H4('Data Gempabumi', className='card-title'),
                    html.P('Data kejadian gempabumi yang terjadi di seluruh wilayah Indonesia',
                           className='card-text'),
                    dbc.Button('SELENGKAPNYA', href='/gempa', color='primary'),
                ]),
            ], style={'width': '18rem'})
        ], width='auto')
    ], justify='center'),

], style={'margin-top': '1%', 'margin-bottom': '1%', 'margin-left': '10%', 'margin-right': '10%'})