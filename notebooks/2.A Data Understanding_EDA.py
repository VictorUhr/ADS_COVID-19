#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 19:11:57 2022

@author: victhorvic
"""

import pandas as pd
import numpy as np

from datetime import datetime

import matplotlib as mpl
import matplotlib.pyplot as plt

import seaborn as sns
import plotly
import plotly.graph_objects as go

# %% [1] data for Covid infectors
''' Marploblib Figure 2'''
#df_plot.to_csv('../data/processed/COVID_inf_small_flat_table.csv',sep=';',index=False)
df_plot_i=pd.read_csv('/Users/victhorvic/ads_covid-19/data/processed/COVID_inf_small_flat_table.csv',sep=';')
df_plot_i.sort_values('date',ascending=False).head()

# Vacc
df_plot_v=pd.read_csv('/Users/victhorvic/ads_covid-19/data/processed/COVID_vac_small_flat_table.csv',
                      sep=';').rename(columns={"Date": "date"})
                                                
#df_plot_v.rename(columns={"Date": "date"}) # change name of the date column
df_plot_v.sort_values('date',ascending=False).head()

# %%% [2] Figure 1_Infectors
''' Matplotlib Figure1: The relative cases overtime of Covid infectors (absolute Covid cases/population size) '''

plt.figure(num = 1);
ax=df_plot_i.iloc[:,:].set_index('date').plot()
plt.xlabel('Date')
plt.ylabel('Confirmed cases (absolute Covid cases/population size)')
plt.title('The relative cases overtime of Covid infectors')
plt.legend(['Mexico' ,'US', 'Germany'])
#plt.ylim(10,4000)
#ax.set_yscale('log')
plt.show()


# %%% [2] Figure 2_Vaccines
''' Matplotlib Figure2: The vaccination rate over time'''

plt.figure(num = 2);
ax1=df_plot_v.iloc[:,:].set_index('date').plot()
plt.xlabel('Date')
plt.ylabel('Rate of the population vaccinated')
plt.title('The vaccination rate over time')
plt.legend(['Mexico' ,'US', 'Germany'])
#plt.ylim(10,4000)
#ax.set_yscale('log')
plt.show


# %% Plot.ly


country_list=['Mexico',
              'US',
              'Germany',
             ] 


# %%%
fig = go.Figure()
## defines how to plot the individual trace
for each in country_list:
    fig.add_trace(go.Scatter(x=df_plot_v.date,
                                y=df_plot_v[each],
                                mode='markers+lines',
                                opacity=0.9,
                                line_width=2,
                                marker_size=4, 
                                name=each
                                 )
                     )

## defines the overall layout properties
fig.update_layout(
    width=1024,
    height=900,
    xaxis_title="Time",
    yaxis_title="Confirmed infected people (source johns hopkins csse, log-scale)",
)
fig.update_yaxes(type="log",range=[1.1,8.8])


fig.update_layout(xaxis_rangeslider_visible=True)
#fig.show(renderer='chrome')
#fig.show()




# %%%

import dash
dash.__version__
#import dash_core_components as dcc
from dash import dcc
#import dash_html_components as html
from dash import html

app = dash.Dash()
app.layout = html.Div([
    
    html.Label('Multi-Select Country'),
    
    dcc.Dropdown(
        id='country_drop_down',
        options=[
            {'label': 'Mexico', 'value': 'Mexico'},
            {'label': 'US', 'value': 'US'},
            {'label': 'Germany', 'value': 'Germany'},

        ],
        value=['Mexico','US', 'Germany'], # which are pre-selected
        multi=True
    ),   
        
    dcc.Graph(figure=fig, id='main_window_slope')
])


# %%%

from dash.dependencies import Input, Output

@app.callback(
    Output('main_window_slope', 'figure'),
    [Input('country_drop_down', 'value')])
def update_figure(country_list):
    
    traces = [] 
    for each in country_list:
        traces.append(dict(x=df_plot_v.date,
                                y=df_plot_v[each],
                                mode='markers+lines',
                                opacity=0.9,
                                line_width=2,
                                marker_size=4, 
                                name=each
                        )
                )
        
    return {
            'data': traces,
            'layout': dict (
                width=1280,
                height=720,
                xaxis_title="Time",
                yaxis_title="Confirmed infected people (source johns hopkins csse, log-scale)",
                xaxis={'tickangle':-45,
                        'nticks':20,
                        'tickfont':dict(size=14,color="#7f7f7f"),
                        
                      },
                yaxis={'type':"log",
                       'range':'[1.1,8,8]'
                      }
        )
    }
# %%%
app.run_server(debug=True, use_reloader=False)



