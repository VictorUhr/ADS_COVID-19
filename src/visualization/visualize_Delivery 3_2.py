#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 23 17:00:19 2022

@author: victhorvic
"""


# %% [0] Libraries 
import pandas as pd
import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt

import dash
dash.__version__
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output,State

import plotly.graph_objects as go

import os
print(os.getcwd())

# %% [1] data for Model

#Data from build_features_2.py
df_input_large=pd.read_csv('/Users/victhorvic/ads_covid-19/data/processed/COVID_final_set_2.csv',sep=';')

countries = df_input_large.columns[1:200]

# %% [2] Dash app

'''To refererence links:
    https://medium.com/analytics-vidhya/plotting-multiple-figures-with-live-data-using-dash-and-plotly-4f5277870cd7

    https://plotly.com/python/subplots/
    https://community.plotly.com/t/two-graphs-side-by-side/5312/2
'''
fig = go.Figure()

app = dash.Dash()
app.layout = html.Div([

    dcc.Markdown('''
    #  Applied Data Science on COVID-19 data

    Goal of the project is to teach data science by applying a cross industry standard process,
    it covers the full walkthrough of: automated data gathering, data transformations,
    filtering and machine learning to approximating the doubling time, and
    (static) deployment of responsive dashboard.

    '''),

    dcc.Markdown('''
    ## Multi-Select Country for visualization
    '''),


    dcc.Dropdown(
        id='country_drop_down',
        options=[ {'label': each,'value':each} for each in countries],
        value=['US', 'Germany','Mexico'], # which are pre-selected
        multi=True
    ),

    dcc.Markdown('''
        ## Select Timeline of confirmed COVID-19 cases or the approximated doubling time
        '''),


    dcc.Dropdown(
    id='doubling_time',
    options=[
        {'label': 'Timeline Confirmed ', 'value': 1},
        {'label': 'Timeline Confirmed Filtered', 'value': 2},
        {'label': 'Timeline Doubling Rate', 'value': 3},
        {'label': 'Timeline Doubling Rate Filtered', 'value': 4},
    ],
    value=1,
    multi=False
    ),

    dcc.Graph(figure=fig, id='main_window_slope')
])

# %% [3] Callback function 

@app.callback(
    Output('main_window_slope', 'figure'),
    [Input('country_drop_down', 'value'),
    Input('doubling_time', 'value')])
def update_figure(country_list,show_doubling):


    if show_doubling > 2:
        my_yaxis={'type':"log",
               'title':'Approximated doubling rate over 3 days (larger numbers are better #stayathome)'
              }
    else:
        my_yaxis={'type':"log",
                  'title':'Confirmed infected people (source johns hopkins csse, log-scale)'
              }


    traces = []
    for each in country_list:
        
        if show_doubling == 2: 
            df_plot=df_input_large[each+'_filter']
        elif show_doubling == 3: 
            df_plot=df_input_large[each+'_DR']
        elif show_doubling == 4: 
            df_plot=df_input_large[each+'_filter_DR']
        else:
            df_plot=df_input_large[each]

        traces.append(dict(x=df_input_large.date,
                                y=df_plot,
                                mode='markers+lines',
                                opacity=0.9,
                                name=each
                        )
                )

    return {
            'data': traces,
            'layout': dict (
                width=1280,
                height=720,

                xaxis={'title':'Timeline',
                        'tickangle':-45,
                        'nticks':20,
                        'tickfont':dict(size=14,color="#7f7f7f"),
                      },

                yaxis=my_yaxis
        )
    }

# %% [4] Run dashboard
app.run_server(debug=True, use_reloader=False)

