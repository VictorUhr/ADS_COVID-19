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

# %%% [1] data for Model SIR

pd_model_ger = pd.read_csv('/Users/victhorvic/ads_covid-19/data/interim/COVID_PR_Ger_table1.csv',
                         sep=';',parse_dates=[0]).drop(['t'], axis = 1)

pd_model_mx = pd.read_csv('/Users/victhorvic/ads_covid-19/data/interim/COVID_PR_Mx_table1.csv',
                         sep=';',parse_dates=[0]).drop(['t'], axis = 1)

pd_model_us = pd.read_csv('/Users/victhorvic/ads_covid-19/data/interim/COVID_PR_US_table1.csv',
                         sep=';',parse_dates=[0]).drop(['t'], axis = 1)



''' Concatenate '''
pd_plot1 =pd.concat([pd_model_ger,pd_model_mx,pd_model_us],
                    axis = 'columns',join="inner", keys=['Germany', 'Mexico', 'US'], 
                    names=['Country'])

# %%% [1.5] Import the optimum value 
''' Beta [1] Gamma [2] '''
popt_Mx = np.loadtxt('/Users/victhorvic/ads_covid-19/data/interim/popt_Mx.txt')
popt_US = np.loadtxt('/Users/victhorvic/ads_covid-19/data/interim/popt_US.txt')
popt_Ge = np.loadtxt('/Users/victhorvic/ads_covid-19/data/interim/popt_Germany.txt')


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

    dcc.Graph(figure=fig, id='main_window_slope'),
    
    # SIR Model Section
    html.Div([
        html.H3('Fit of SIR model for country cases'),
        html.Label('Multi-Select Country'),
    
        dcc.Dropdown(
            id='country_drop_down2',
            options=[
                {'label': 'Mexico', 'value': 'Mexico'},
                {'label': 'US', 'value': 'US'},
                {'label': 'Germany', 'value': 'Germany'},

        ],
            value=[ 'Germany', 'US', 'Mexico'], # which are pre-selected
            multi= True #_ boolean value to show diferent countries values
            
            ),   
        
        dcc.Graph(figure=fig, id='main_window_slope2'),
        
        dcc.Markdown('''### Optimal parameters per country:'''),        
        html.Footer(' Germany = beta {:.5f} and gamma {:.5f} \n'.format(popt_Ge[0],popt_Ge[1])),
        html.Footer('US      = beta {:.5f} and gamma {:.5f} \n'.format(popt_US[0],popt_US[1])),
        html.Footer('Mexico  = beta {:.5f} and gamma {:.5f} \n'.format(popt_Mx[0],popt_Mx[1])),
        html.Footer('\rThis ratio is derived as the expected number of new infections (these new infections are sometimes called secondary infections from a single infection in a population where all subjects are susceptible. @wiki'),
        html.Footer('''Data from: 
        Johns Hopkins GITHUB csv data
        https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series |-> Infections '''),
        #html.Footer('''Centers for Civic Impact https://github.com/govex/COVID-19/blob/a96dbc70eada30e83b1c475a328bb3cab4712741/data_tables/vaccine_data/global_data/time_series_covid19_vaccine_global.csv |-> Vaccinned '''),
    ]),
    
       
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

# %% [3.1] Callback SIR

''' SIR Dashboard'''
@app.callback(
    Output('main_window_slope2', 'figure'),
    [Input('country_drop_down2', 'value')])
def update_figure2(country_list):
  
    traces = [] 
 
    '''  fig.add_trace(go.Scatter(#x=pd_plot1.index,
                                    y=pd_plot1.Germany.ydata,
                                    mode='markers+lines',
                                    opacity=0.9,
                                    line_width=2,
                                    marker_size=4, 
                                    name='Germany real data',
                                    
                                     )

    
    '''
    for each in country_list:
        traces.append(dict( #x=df_plot1_i.date,
                                y=pd_plot1[each, 'ydata'],
                                mode='markers+lines',
                                opacity=0.9,
                                line_width=2,
                                marker_size=4, 
                                name= "Real data {}".format(each)
                        )
                )
   
        traces.append(dict( #x=df_plot1_i.date,
                                y=pd_plot1[each,'fitted'],
                                mode='markers+lines',
                                opacity=0.9,
                                line_width=2,
                                marker_size=3, 
                                name= "SIR data {}".format(each)   #SIR model data
                        )
                )
        
    return {
            'data': traces,
            'layout': dict (
                width=1280,
                height=720,
                xaxis_title="Days",
                yaxis_title="Population infected (source johns hopkins csse, log-scale)",
                xaxis={'tickangle':-45,
                        'nticks':20,
                        'tickfont':dict(size=14,color="#7f7f7f"),
                        
                      },
                yaxis={'type':"log", #change to logaritmic scale #to change logaritmic "linear"
                       'range':'[1.1,8,8]'
                      },
                
                
        ),
            
    }
# %% [4] Run dashboard
app.run_server(debug=True, use_reloader=False)

