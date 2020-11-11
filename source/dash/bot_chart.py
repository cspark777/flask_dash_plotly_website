"""Instantiate a Dash app."""
import numpy as np
import pandas as pd
import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc

from source.util.chart import *

def init_botchart(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/wallet_status/',        
    )

    # Create Layout
    dash_app.layout = html.Div(
        children=[
            html.Div(className='row',
                children=[
                    dcc.Location(id='url', refresh=False),                    
                    html.Div(className='div-for-charts bg-grey',
                        children=[
                         dcc.Graph(
                            id='chart_bot_timeseries', 
                            config={'displayModeBar': True}, 
                            animate=True, 
                            
                        )
                    ], style={"minHeight" : "1000px", "width" : "100%"})
            ])
        ]
    )

    init_callbacks(dash_app)

    return dash_app.server

def init_callbacks(dash_app):
    @dash_app.callback(Output('chart_bot_timeseries', 'figure'),
    [dash.dependencies.Input('url', 'search')])
    def update_chart_bot(search):    
        bot_id = 0
        try:
            print("----------")
            print(search)        

            bot_id = search[1:].split("bot_id=")[1].split("&")[0]
            print(bot_id)

            figure = get_graph(bot_id)
            return figure
        except:
            print("url_error")  

