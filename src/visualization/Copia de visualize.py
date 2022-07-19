#!/usr/bin/env python3# -*- coding: utf-8 -*-"""Created on Mon Jun 27 19:11:57 2022@author: victhorvic"""# %% [0] Libraries import pandas as pdimport numpy as npfrom datetime import datetimeimport matplotlib as mplimport matplotlib.pyplot as pltimport seaborn as snsimport plotlyimport plotly.graph_objects as gofrom plotly.subplots import make_subplots# %% [1] data for Modelpd_model_ger = pd.read_csv('/Users/victhorvic/ads_covid-19/data/interim/COVID_PR_Ger_table1.csv',                         sep=';',parse_dates=[0]).drop(['t'], axis = 1)pd_model_mx = pd.read_csv('/Users/victhorvic/ads_covid-19/data/interim/COVID_PR_Mx_table1.csv',                         sep=';',parse_dates=[0]).drop(['t'], axis = 1)pd_model_us = pd.read_csv('/Users/victhorvic/ads_covid-19/data/interim/COVID_PR_US_table1.csv',                         sep=';',parse_dates=[0]).drop(['t'], axis = 1)''' Concatenate '''pd_plot1 =pd.concat([pd_model_ger,pd_model_mx,pd_model_us],                    axis = 'columns',join="inner", keys=['Germany', 'Mexico', 'US'],                     names=['Country'])# %%% [1.5] Import the optimum value ''' Beta [1] Gamma [2] '''popt_Mx = np.loadtxt('/Users/victhorvic/ads_covid-19/data/interim/popt_Mx.txt')popt_US = np.loadtxt('/Users/victhorvic/ads_covid-19/data/interim/popt_US.txt')popt_Ge = np.loadtxt('/Users/victhorvic/ads_covid-19/data/interim/popt_Germany.txt')# %% [1] data for Covid infectors and vaccinated''' Marploblib Figure 2'''#df_plot.to_csv('../data/processed/COVID_inf_small_flat_table.csv',sep=';',index=False)df_plot_i=pd.read_csv('/Users/victhorvic/ads_covid-19/data/processed/COVID_inf_small_flat_table.csv',sep=';')df_plot_i.sort_values('date',ascending=False).head()# Vaccdf_plot_v=pd.read_csv('/Users/victhorvic/ads_covid-19/data/processed/COVID_vac_small_flat_table.csv',                      sep=';').rename(columns={"Date": "date"})                                                #df_plot_v.rename(columns={"Date": "date"}) # change name of the date columndf_plot_v.sort_values('date',ascending=False).head()# %% [2.1] Graph Matplotlib Figure 1_Infectors and vaccinatedcountry_list=['Mexico',              'US',              'Germany',             ] fig = go.Figure()## defines how to plot the individual tracefor each in country_list:    fig.add_trace(go.Scatter(x=df_plot_i.date,                                y=df_plot_i[each],                                mode='markers+lines',                                opacity=0.9,                                line_width=2,                                marker_size=4,                                 name=each                                 )                     )## defines the overall layout propertiesfig.update_layout(    #width=500,    #height=900,    xaxis_title="Time",    yaxis_title="Confirmed infected people (source johns hopkins csse, log-scale)",)fig.update_yaxes(type="log",range=[1.1,8.8])fig.update_layout(xaxis_rangeslider_visible=True)#fig.show(renderer='chrome')#fig.show()# %%% [2.2] for vaccinatedfig1 = go.Figure()## defines how to plot the individual tracefor each in country_list:    fig.add_trace(go.Scatter(x=df_plot_v.date,                                y=df_plot_v[each],                                mode='markers+lines',                                opacity=0.9,                                line_width=2,                                marker_size=4,                                 name=each                                 )                     )## defines the overall layout propertiesfig1.update_layout(    #width=500,    #height=900,    xaxis_title="Time",    yaxis_title="Confirmed vaccined people",)fig1.update_yaxes(type="log",range=[1.1,8.8])fig1.update_layout(xaxis_rangeslider_visible=True)#fig.show(renderer='chrome')#fig.show()# %%% [2.3] Graph Matplotlib Figure 1_Infectors''' Matplotlib Figure1: The relative cases overtime of Covid infectors (absolute Covid cases/population size) '''plt.figure(num = 1);ax=pd_plot1.iloc[:,:].plot()plt.xlabel('Date')plt.ylabel('Confirmed cases (absolute Covid cases/population size)')plt.title('The relative cases overtime of Covid infectors')plt.legend(['ydata' ,'fitted'])#plt.ylim(10,4000)ax.set_yscale('log')plt.show()# %% [3] Plot.lycountry_list=['Mexico',              'US',              'Germany',             ] each = country_list[1]fig3 = go.Figure()## defines how to plot the individual trace#for each in country_list:fig.add_trace(go.Scatter(#x=pd_plot1.index,                                y=pd_plot1[each,'ydata'],                                #y=pd_plot1.Germany.ydata,                                mode='markers+lines',                                opacity=0.9,                                line_width=2,                                marker_size=4,                                 name='Germany real data',                                                                 )                    ) fig.add_trace(go.Scatter(#x=pd_plot1.index,                                y = pd_plot1[each,'fitted'],                                #y=pd_plot1.Germany.fitted,                                mode='markers+lines',                                opacity=0.9,                                line_width=2,                                marker_size=4,                                 name='Germany model',                                                                 )                    ) ## defines the overall layout propertiesfig.update_layout(    #width=500,    #height=900,    xaxis_title="Time",    yaxis_title="Fit of SIR model for Germany cases",)fig.update_yaxes(type="log",range=[1.1,8.8])fig.update_layout(xaxis_rangeslider_visible=True)#fig.show(renderer='chrome')#fig.show()# %% [4] Dash app'''To refererence links:    https://medium.com/analytics-vidhya/plotting-multiple-figures-with-live-data-using-dash-and-plotly-4f5277870cd7    https://plotly.com/python/subplots/    https://community.plotly.com/t/two-graphs-side-by-side/5312/2'''import dashdash.__version__#import dash_core_components as dccfrom dash import dcc#import dash_html_components as htmlfrom dash import htmlapp = dash.Dash()app.layout = html.Div([        html.Div([        html.H3('Confirmed infected people (source johns hopkins csse, ratio Total population)'),        html.Label('Multi-Select Country'),            dcc.Dropdown(            id='country_drop_down',            options=[                {'label': 'Mexico', 'value': 'Mexico'},                {'label': 'US', 'value': 'US'},                {'label': 'Germany', 'value': 'Germany'},        ],            value=['Mexico','US', 'Germany'], # which are pre-selected            multi=True            ),                   dcc.Graph(figure=fig, id='main_window_slope')     ]),    html.Div([        html.H3('Confirmed vaccined people (source johns hopkins csse, ratio Total population)'),        html.Label('Multi-Select Country'),            dcc.Dropdown(            id='country_drop_down1',            options=[                {'label': 'Mexico', 'value': 'Mexico'},                {'label': 'US', 'value': 'US'},                {'label': 'Germany', 'value': 'Germany'},        ],            value=['Mexico','US', 'Germany'], # which are pre-selected            multi=True            ),                   dcc.Graph(figure=fig1, id='second_window_slope') #cambio aquí    ]),            # Section of the SIR Model        html.Div([        html.H3('Fit of SIR model for country cases (log-scale)'),        html.Label('Multi-Select Country'),            dcc.Dropdown(            id='country_drop_down2',            options=[                {'label': 'Mexico', 'value': 'Mexico'},                {'label': 'US', 'value': 'US'},                {'label': 'Germany', 'value': 'Germany'},        ],            value=[ 'Germany', 'US', 'Mexico'], # which are pre-selected            multi= True #_ boolean value to show diferent countries values                        ),                   dcc.Graph(figure=fig3, id='third_window_slope'),                html.Footer('Optimal parameters per country:'),        html.Footer('Germany = beta {:.5f} and gamma {:.5f} \n'.format(popt_Ge[0],popt_Ge[1])),        html.Footer('US      = beta {:.5f} and gamma {:.5f} \n'.format(popt_US[0],popt_US[1])),        html.Footer('Mexico  = beta {:.5f} and gamma {:.5f} \n'.format(popt_Mx[0],popt_Mx[1])),        html.Footer('\r This ratio is derived as the expected number of new infections (these new infections are sometimes called secondary infections from a single infection in a population where all subjects are susceptible. @wiki'),    ]),        ])# %% [4]callback function''' For infected population'''from dash.dependencies import Input, Output@app.callback(    Output('main_window_slope', 'figure'),    [Input('country_drop_down', 'value')])def update_figure(country_list):      traces = []     for each in country_list:        traces.append(dict(x=df_plot_i.date,                                y=df_plot_i[each],                                mode='markers+lines',                                opacity=0.9,                                line_width=2,                                marker_size=4,                                 name=each                        )                )                        return {            'data': traces,            'layout': dict (                width=1280,                height=720,                xaxis_title="Time",                yaxis_title="Confirmed infected people (source johns hopkins csse, log-scale)",                xaxis={'tickangle':-45,                        'nticks':20,                        'tickfont':dict(size=14,color="#7f7f7f"),                                              },                yaxis={'type':"line",                       'range':'[1.1,8,8]'                      },                                        ),                }# %%% [4.1] callback function vaccinated population@app.callback(    Output('second_window_slope', 'figure'),    [Input('country_drop_down1', 'value')])def update_figure1(country_list):      traces = []     for each in country_list:        traces.append(dict(x=df_plot_v.date,                                y=df_plot_v[each],                                mode='markers+lines',                                opacity=0.9,                                line_width=2,                                marker_size=4,                                 name=each                        )                )                        return {            'data': traces,            'layout': dict (                width=1280,                height=720,                xaxis_title="Time",                yaxis_title="Confirmed vaccined people ",                xaxis={'tickangle':-45,                        'nticks':20,                        'tickfont':dict(size=14,color="#7f7f7f"),                                              },                axis={'type':"line",                       'range':'[1.1,8,8]'                      },                                        ),                }# %%% [4.2] callback function SIR model''' Call back function of the third'''@app.callback(    Output('third_window_slope', 'figure'),    [Input('country_drop_down2', 'value')])def update_figure(country_list):      traces = []      '''  fig.add_trace(go.Scatter(#x=pd_plot1.index,                                    y=pd_plot1.Germany.ydata,                                    mode='markers+lines',                                    opacity=0.9,                                    line_width=2,                                    marker_size=4,                                     name='Germany real data',                                                                         )        '''    for each in country_list:        traces.append(dict( #x=df_plot1_i.date,                                y=pd_plot1[each, 'ydata'],                                mode='markers+lines',                                opacity=0.9,                                line_width=2,                                marker_size=4,                                 name= "Real data {}".format(each)                        )                )           traces.append(dict( #x=df_plot1_i.date,                                y=pd_plot1[each,'fitted'],                                mode='markers+lines',                                opacity=0.9,                                line_width=2,                                marker_size=3,                                 name= "SIR data {}".format(each)   #SIR model data                        )                )            return {            'data': traces,            'layout': dict (                width=1280,                height=720,                xaxis_title="Days",                yaxis_title="Population infected (source johns hopkins csse, log-scale)",                xaxis={'tickangle':-45,                        'nticks':20,                        'tickfont':dict(size=14,color="#7f7f7f"),                                              },                yaxis={'type':"log", #change to logaritmic scale #to change logaritmic "linear"                       'range':'[1.1,8,8]'                      },                                        ),                }# %%% Run Dash serverapp.run_server(debug=True, use_reloader=False)