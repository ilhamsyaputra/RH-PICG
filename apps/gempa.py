import json
import urllib
import pandas as pd
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

from dash.dependencies import Input, Output, State
from app import app


def getInfo():
    urlData = 'https://data.bmkg.go.id/DataMKG/TEWS/gempaterkini.json'
    web = urllib.request.urlopen(urlData)
    if web.getcode() == 200:
        data = web.read()
        JSON = json.loads(data)

        dicts = []
        df_gempa = pd.DataFrame()

        for i in JSON['Infogempa']['gempa']:
            dicts.append(i)

        df_gempa = df_gempa.append(dicts, ignore_index=True)

        waktu_gempa = df_gempa['Tanggal'] + '\n' + df_gempa['Jam']

        df_gempa.insert(loc=0, column='Waktu Gempa', value=waktu_gempa)
        df_gempa.rename(columns={'Coordinates': 'Titik Gempa', 'Magnitude': 'Magnitudo'}, inplace=True)

        df_gempa = df_gempa.drop(['Tanggal', 'Jam', 'Lintang', 'Bujur', 'DateTime'], axis=1)
    else:
        print('Something wrong, cannot proceed')

    return df_gempa


def gempaTerbaru():
    urlData = 'https://data.bmkg.go.id/DataMKG/TEWS/autogempa.json'
    web = urllib.request.urlopen(urlData)
    if web.getcode() == 200:
        data = web.read()
        JSON = json.loads(data)

        wilayah = JSON['Infogempa']['gempa']['Wilayah']
        shakemap = 'https://ews.bmkg.go.id/TEWS/data/' + JSON['Infogempa']['gempa']['Shakemap']
        dirasakan = JSON['Infogempa']['gempa']['Dirasakan']
        waktu = JSON['Infogempa']['gempa']['Tanggal'] + ' - ' + JSON['Infogempa']['gempa']['Jam']
        magnitudo = JSON['Infogempa']['gempa']['Magnitude']
        kedalaman = JSON['Infogempa']['gempa']['Kedalaman']
        lokasi = JSON['Infogempa']['gempa']['Lintang'] + ' ' + JSON['Infogempa']['gempa']['Bujur']
        map = 'https://www.google.com/maps/search/' + JSON['Infogempa']['gempa']['Coordinates']

        terbaru = dbc.Card(
            dbc.CardBody(
                [
                    html.H5('Gempabumi Terkini', className='card-title'),
                    html.P(wilayah),
                    html.Label('Dirasakan (Skala MMI)'),
                    dbc.Badge(dirasakan, color='warning', className='mr-1'),
                    html.Br(),
                    dbc.Button('Detail Gempa', id='open', color='primary'),
                    dbc.Modal(
                        [
                            dbc.ModalHeader('Informasi Gempabumi'),
                            dbc.ModalBody([
                                    html.P('Peta Guncangan Gempabumi (Earthquake Shakemap)'),
                                    dbc.CardImg(src=shakemap, style={'width': '300px'}),
                                    dcc.Markdown(f'''
                                                **Parameter Gempabumi**  
                                                {waktu}  
                                                Magnitudo: {magnitudo}  
                                                Kedalaman: {kedalaman}  
                                                Lokasi: {lokasi}  
                                                Google maps: [Lokasi Gempa]({map} 'Lokasi kejadian gempabumi')
                                                ''')
                            ]),
                            dbc.ModalFooter(
                                dbc.Button(
                                    'Tutup', id='close', className='ml-auto', n_clicks=0
                                )
                            ),
                        ],
                        id="modal",
                        is_open=False,
                    ),
                ]
            )
        )

    return terbaru

# layout web app
layout = html.Div([
    html.H1('Informasi Gempabumi'),
    html.Hr(),
    dbc.Row([
        dbc.Col(gempaTerbaru(), width='auto')
    ]),
    html.Br(),
    html.H3('Gempabumi Terkini (M≥5.0)'),
    dbc.Table.from_dataframe(getInfo(), striped=True, hover=True),
], style={'margin-top': '1%', 'margin-bottom': '1%', 'margin-left': '10%', 'margin-right': '10%'})

@app.callback(
    Output('modal', 'is_open'),
    [Input('open', 'n_clicks'), Input('close', 'n_clicks')],
    [State('modal', 'is_open')],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open