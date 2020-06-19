from app import app
from app import server
import dash_html_components as html
import dash_core_components as dcc
import dash_table
from dash.dependencies import Input, Output
from datetime import datetime
import pandas as pd
from covidcfr.california import adjusted_cfr

fig, cases, deaths, cfr, a_cfr = adjusted_cfr()


def get_data_table(name, df):
    df_new = df.reset_index().rename(columns={'index': 'Age'})
    data_table = dash_table.DataTable(
        id='datatable-'+name,
        data=df_new.to_dict('Records'),
        columns=[{'id': c, 'name': c} for c in df_new.columns],
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        }
    )
    return data_table


app.layout = html.Div([html.H1('Ajusted CFR',
                               style={
                                   'textAlign': 'center',
                                   "background": "yellow"}),
                       html.Div([
                           dcc.Dropdown(
                               id='pick-state',
                               options=[
                                   {'label': 'California', 'value': 'ca'}
                               ],
                               value='NYC'
                           ),
                            html.Div(id='dd-output-container')
                           ]),
                           html.H3('California'),
                       html.Div([dcc.Graph(figure=fig)]),
                       html.Div(children=[html.H5(children='Cases by Race and Age', style={'textAlign': 'center'}), get_data_table('cases', cases)]),
                       html.Div(children=[html.H5(children='Deaths by Race and Age', style={'textAlign': 'center'}), get_data_table('deaths', deaths)]),
                       html.Div(children=[html.H5(children='Reported CFR by Race and Age', style={'textAlign': 'center'}), get_data_table('reported-cfr', cfr)]),
                       html.Div(children=[html.H5(children='Adjusted CFR by Race and Age', style={'textAlign': 'center'}), get_data_table('adjusted-cfr', a_cfr)]),
                       ], style={}
                      )



if __name__ == '__main__':
    app.run_server(debug=True)