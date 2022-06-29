#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 02:57:24 2022

@author: victhorvic
"""

import pandas as pd
import numpy as np

from datetime import datetime

import matplotlib as mpl
import matplotlib.pyplot as plt

# %% [1]
'''
Johns Hopkins GITHUB csv data

https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series |-> Infections

Centers for Civic Impact

https://github.com/govex/COVID-19/blob/a96dbc70eada30e83b1c475a328bb3cab4712741/data_tables/vaccine_data/global_data/time_series_covid19_vaccine_global.csv |-> Vaccinned

'''

data_path1 = 'https://github.com/govex/COVID-19/blob/a96dbc70eada30e83b1c475a328bb3cab4712741/data_tables/vaccine_data/global_data/time_series_covid19_vaccine_global.csv?raw=true'
## added ?raw=true to get last value and get the permantlink from Github

# data vaccined
pd_raw_vac=pd.read_csv(data_path1,)

''' Dates for vaccines COVID'''
# %% [2]
# to prepare the index timer 
time_idx=pd_raw_vac['Date'].unique()

df_plot = pd.DataFrame({
    'Date':time_idx})


pd2 = pd_raw_vac.drop(['Report_Date_String','UID','Province_State','People_partially_vaccinated'],axis=1)
''' check data of the countries '''

#Germany data 
testde = pd_raw_vac[pd_raw_vac['Country_Region']=='Germany'].iloc[:,1::].set_index(['Date'])
testde.dropna(subset=['People_fully_vaccinated']).iloc[:,0:3].plot(title = 'Germany')


#US Data
pd2[pd2['Country_Region']=='US'].iloc[:,1::].set_index('Date')
pd2[pd2['Country_Region']=='US'].iloc[:,1::].set_index('Date').plot(title = 'US')

# Mexico data
pd2[pd2['Country_Region']=='Mexico'].iloc[:,1::].set_index('Date')
pd2[pd2['Country_Region']=='Mexico'].iloc[:,1::].set_index('Date').plot(title ='Mexico')

# %% [3]
'''Cocatenate data '''

country_list=['Mexico',
              'US',
              'Germany'
             ]

# define the data for concatenate
c_de = testde.dropna(subset=['People_fully_vaccinated']).iloc[:,2:3]

c_mx =pd2[pd2['Country_Region'] == country_list[0]].groupby('Date').sum().drop(['Doses_admin'], axis=1)
                             
c_us =pd2[pd2['Country_Region'] == country_list[1]].iloc[:,1::].groupby('Date').sum().drop(['Doses_admin'], axis=1)                             

#concac =pd.concat([c_mx,c_us,c_de],axis=1,join="inner")
concac =pd.concat([c_mx,c_us,c_de],axis=1,join="inner", )#keys=['Mexico', 'US', 'Germany'])
concac.columns = country_list

# %%% [3.1]
# Total population for each country
        # Mexico US Germany
pop = [128.9E6, 329.5E6, 83.24E6]

# Look for divide the data 
concac[( 'Mexico')] = concac[('Mexico')].div(pop[0])
concac[( 'US')] = concac[('US')].div(pop[1])
concac[( 'Germany')] = concac[('Germany')].div(pop[2])

#concac[( 'Mexico', 'People_fully_vaccinated')] = concac[( 'Mexico', 'People_fully_vaccinated')].div(pop[0])
#concac[( 'US', 'People_fully_vaccinated')] = concac[( 'US', 'People_fully_vaccinated')].div(pop[1])
#concac[( 'Germany', 'People_fully_vaccinated')] = concac[( 'Germany', 'People_fully_vaccinated')].div(pop[2])


# test the value 
concac.plot()


# %% [4]
'''Plot matplotlib'''
''' Matplotlib Figure2: The vaccination rate over time '''


fig2 =concac.plot( grid = True,
                  xlabel = 'Date',
                  ylabel = 'Rate of the population',
                  title = 'The vaccination rate over time',  
                  
                  )

''' Save fig in the folder '''
fig2.figure.savefig('/Users/victhorvic/ads_covid-19/reports/figures/figure_2.png',dpi = 1000)
plt.show()

# %% [5] 
'''Export csv file'''
df_plot1 = concac.reset_index()
df_plot1.to_csv('../data/processed/COVID_vac_small_flat_table.csv',sep=';',index=False)


