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

# %% data for Covid infectors
#df_plot.to_csv('../data/processed/COVID_inf_small_flat_table.csv',sep=';',index=False)
df_plot=pd.read_csv('../data/processed/COVID_inf_small_flat_table.csv',sep=';')
df_plot.sort_values('date',ascending=False).head()



# %%% Figure 
''' Matplotlib Figure1: The relative cases overtime of Covid infectors (absolute Covid cases/population size) '''

plt.figure();
ax=df_plot.iloc[15:,:].set_index('date').plot()
plt.xlabel('Date')
plt.ylabel('confirmed cases (absolute Covid cases/population size)')
plt.title('Covid-19 Case PlotThe relative cases overtime of Covid infectors')
#plt.legend(['Turkey' ,'Germany', 'US'])
#plt.ylim(10,4000)
#ax.set_yscale('log')
plt.show()




# %% data for Covid infectors vaccinates





# %% 
# Plot.ly


country_list=['Mexico',
              'US',
              'Germany',
             ] 

'''
# %%%
fig = go.Figure()
## defines how to plot the individual trace
for each in country_list:
    fig.add_trace(go.Scatter(x=df_plot.date,
                                y=df_plot[each],
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
fig.show()



'''
# %%%
'''
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

#%%
# app.run_server(debug=True, use_reloader=False)

'''

