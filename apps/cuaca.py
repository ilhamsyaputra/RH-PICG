import urllib.request
import pandas as pd
import xml.etree.ElementTree as ET
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import plotly.express as px

from datetime import datetime, time
from dash.dependencies import Input, Output, State
from app import app

kota = []

layout = html.Div([
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
            id='provinsi',
            options=[
                {'label': 'Aceh', 'value': 'Aceh'},
                {'label': 'Bali', 'value': 'Bali'},
                {'label': 'Bangka Belitung', 'value': 'BangkaBelitung'},
                {'label': 'Banten', 'value': 'Banten'},
                {'label': 'Bengkulu', 'value': 'Bengkulu'},
                {'label': 'DI Yogyakarta', 'value': 'DIYogyakarta'},
                {'label': 'DKI Jakarta', 'value': 'DKIJakarta'},
                {'label': 'Gorontalo', 'value': 'Gorontalo'},
                {'label': 'Jambi', 'value': 'Jambi'},
                {'label': 'Jawa Barat', 'value': 'JawaBarat'},
                {'label': 'Jawa Tengah', 'value': 'JawaTengah'},
                {'label': 'Jawa Timur', 'value': 'JawaTimur'},
                {'label': 'Kalimantan Barat', 'value': 'KalimantanBarat'},
                {'label': 'Kalimantan Selatan', 'value': 'KalimantanSelatan'},
                {'label': 'Kalimantan Tengah', 'value': 'KalimantanTengah'},
                {'label': 'Kalimantan Timur', 'value': 'KalimantanTimur'},
                {'label': 'Kalimantan Utara', 'value': 'KalimantanUtara'},
                {'label': 'Kepulauan Riau', 'value': 'KepulauanRiau'},
                {'label': 'Lampung', 'value': 'Lampung'},
                {'label': 'Maluku', 'value': 'Maluku'},
                {'label': 'Maluku Utara', 'value': 'MalukuUtara'},
                {'label': 'Nusa Tenggara Barat', 'value': 'NusaTenggaraBarat'},
                {'label': 'Nusa Tenggara Timur', 'value': 'NusaTenggaraTimur'},
                {'label': 'Papua', 'value': 'Papua'},
                {'label': 'Papua Barat', 'value': 'PapuaBarat'},
                {'label': 'Riau', 'value': 'Riau'},
                {'label': 'Sulawesi Barat', 'value': 'SulawesiBarat'},
                {'label': 'Sulawesi Selatan', 'value': 'SulawesiSelatan'},
                {'label': 'Sulawesi Tengah', 'value': 'SulawesiTengah'},
                {'label': 'Sulawesi Tenggara', 'value': 'SulawesiTenggara'},
                {'label': 'Sulawesi Utara', 'value': 'SulawesiUtara'},
                {'label': 'Sumatera Barat', 'value': 'SumateraBarat'},
                {'label': 'Sumatera Selatan', 'value': 'SumateraSelatan'},
                {'label': 'Sumatera Utara', 'value': 'SumateraUtara'},
                {'label': 'Indonesia', 'value': 'Indonesia'},
            ],
            placeholder='Pilih Provinsi',
            ),
            html.Br(),
        ])
    ], justify='center'),
    dbc.Row([
        dbc.Col([
            html.Div(id='outputkota')
        ]),


    ], justify='center'),
    dbc.Row([
        html.Div(id='output')
    ], justify='center'),
], style={'margin-top': '1%', 'margin-bottom': '1%', 'margin-left': '10%', 'margin-right': '10%'})

@app.callback(
    Output('outputkota', 'children'),
    Input('provinsi', 'value')
)
def update_kota(value):
    if value != None:
        global doc
        urlXml = 'https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-' + value + '.xml'
        web = urllib.request.urlopen(urlXml)
        data = web.read()
        doc = ET.fromstring(data)


        daftar_kota = []

        for n, i in enumerate(doc[0]):
            if n == 0:
                pass
            else:
                daftar_kota.append(doc[0][n][1].text)

        out = dcc.Dropdown(
            id='kota',
            options=[{'label': i, 'value': n} for n, i in enumerate(daftar_kota)],
            placeholder='Pilih Kota',
            style={'width': '100%'}
            ),

        return out


@app.callback(
    Output('output', 'children'),
    Input('kota', 'value')
)
def update_status(value):
    if value != None:

        humidity = doc[0][value + 1][2]
        temperature = doc[0][value + 1][7]
        cuaca = doc[0][value + 1][8]
        timeseries = []
        humidity_plot = []
        temperature_plot = []
        cuaca_plot = []
        kondisi_cuaca = []
        kondisi = ''
        t = 0
        t_final = []
        arah_angin = doc[0][1][9]
        arah_angin_df = []
        kecepatan_angin = doc[0][1][10]
        kecepatan_angin_df = []


        df_cuaca = pd.DataFrame()

        for n, i in enumerate(humidity):
            for j in humidity[n]:
                datetime_str = i.attrib['datetime']
                datetime_object = datetime.strptime(datetime_str, '%Y%m%d%H%M%S')

                timeseries.append(datetime_object)
                humidity_plot.append(int(j.text))

        for n, i in enumerate(temperature):
            for j in temperature[n]:
                temperature_plot.append(j.text)

        for n, i in enumerate(temperature_plot):
            while t < 24:
                t_final.append(int(temperature_plot[t]))
                t += 2

        for n, i in enumerate(cuaca):
            for j in cuaca[n]:
                cuaca_plot.append(int(j.text))

        df_cuaca.insert(loc=0, column='Datetime', value=timeseries)
        df_cuaca['Tanggal'] = [d.date() for d in df_cuaca['Datetime']]
        df_cuaca['Waktu'] = [d.time() for d in df_cuaca['Datetime']]
        df_cuaca = df_cuaca.drop(['Datetime'], axis=1)
        df_cuaca['Kode Cuaca'] = cuaca_plot

        for i in df_cuaca['Kode Cuaca']:
            if i == 0:
                kondisi = 'Cerah'
            elif i == 1 or i == 2:
                kondisi = 'Cerah Berawan'
            elif i == 3:
                kondisi = 'Berawan'
            elif i == 4:
                kondisi = 'Berawan Tebal'
            elif i == 10:
                kondisi = 'Asap'
            elif i == 45:
                kondisi = 'kabut'
            elif i == 60:
                kondisi = 'Hujan Ringan'
            elif i == 61:
                kondisi = 'Hujan Sedang'
            elif i == 63:
                kondisi = 'Hujan Lebat'
            elif i == 80:
                kondisi = 'Hujan Lokal'
            elif i == 95 or i == 97:
                kondisi = 'Hujan Petir'
            kondisi_cuaca.append(kondisi)

        df_cuaca['Prakiraan Cuaca'] = kondisi_cuaca

        for n, i in enumerate(arah_angin):
            a = arah_angin[n][0]
            arah_angin_df.append(float(a.text))

        df_cuaca['Arah Angin'] = arah_angin_df

        for n, i in enumerate(kecepatan_angin):
            a = kecepatan_angin[n][2]
            kecepatan_angin_df.append(float(a.text))

        df_cuaca['Kecepatan Angin (KM/Jam)'] = kecepatan_angin_df

        # d = time(12, 0)
        # icon = []
        # iconimg = []
        # for n, i in enumerate(df_cuaca['Prakiraan Cuaca']):
        #     if df_cuaca['Waktu'][n] > d:
        #         path = './assets/icon-cuaca/' + i.lower() + '-pm.png'
        #         icon.append(path)
        #     else:
        #         path = './assets/icon-cuaca/' + i.lower() + '-am.png'
        #         icon.append(path)
        #
        # df_cuaca['Icon'] = icon





        batas = max(humidity_plot) + 20

        # kelembaban
        fig = px.line(x=timeseries, y=humidity_plot,
                      title='Kelembaban',
                      labels=dict(x='Waktu', y='Kelembaban (%)'))
        fig.update_yaxes(range=[0, batas], fixedrange=True)
        fig.update_xaxes(fixedrange=True)
        fig.update_layout(hovermode="x",
                          margin=dict(l=20, r=20, t=30, b=20))

        # temperature
        fig2 = px.line(x=timeseries, y=t_final,
                       title='Temperature',
                       labels=dict(x='Waktu', y='Temprature (°C)'))
        fig2.update_yaxes(fixedrange=True)
        fig2.update_xaxes(fixedrange=True)
        fig2.update_layout(hovermode="x",
                           margin=dict(l=20, r=20, t=30, b=20))


        output_cuaca = html.Div([
            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        id='kelembaban',
                        figure=fig,
                        config={'displayModeBar': False},
                        style={'width': '60vh', 'height': '40vh'}
                    ),
                ]),
                dbc.Col([
                    dcc.Graph(
                        id='temperature',
                        figure=fig2,
                        config={'displayModeBar': False},
                        style={'width': '60vh', 'height': '40vh'}
                    ),
                ]),

            ], style={'margin-top': '50px'}),
            dbc.Row([
                dbc.Table.from_dataframe(df_cuaca, striped=True, hover=True),
            ], style={'margin-top': '50px'}),
        ])

        return output_cuaca