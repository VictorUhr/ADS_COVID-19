#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 18:59:23 2022

@author: victhorvic
"""
# %% [0] Libraries
import pandas as pd
import numpy as np

from datetime import datetime


import matplotlib.pyplot as plt

#%% [1] Get data

'''
Links of the data

Johns Hopkins GITHUB csv data
https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series |-> Infections

Centers for Civic Impact
https://github.com/govex/COVID-19/blob/a96dbc70eada30e83b1c475a328bb3cab4712741/data_tables/vaccine_data/global_data/time_series_covid19_vaccine_global.csv |-> Vaccinned
'''

data_path = 'https://github.com/CSSEGISandData/COVID-19/blob/246eab67395dce9a4238fff77aa5f3561e253d48/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv?raw=true'
## added ?raw=true to get last value and get the permantlink from Github

#data_path1 = 'https://github.com/govex/COVID-19/blob/a96dbc70eada30e83b1c475a328bb3cab4712741/data_tables/vaccine_data/global_data/time_series_covid19_vaccine_global.csv?raw=true'
## added ?raw=true to get last value and get the permantlink from Github


# data infections 
pd_raw_inf=pd.read_csv(data_path,)


# %% [3.1] Infections data
'''Data for infections COVID¶'''

# define time index
time_idx=pd_raw_inf.columns[4:]

df_plot= pd.DataFrame({'date':time_idx})

# define countries
country_list=['Mexico',
              'US',
              'Germany',
             ] 
country_list = pd_raw_inf['Country/Region'].unique()

for each in country_list:
    df_plot[each] = np.array(pd_raw_inf[pd_raw_inf['Country/Region']==each].iloc[:,4::].sum(axis=0))


# %%% [3.3] Save to csv
'''Export csv file'''


''' Fix time_index'''
time_idx=[datetime.strptime( each,"%m/%d/%y") for each in df_plot.date] 
# convert to datetime

time_str=[each.strftime('%Y-%m-%d') for each in time_idx] 
# convert back to date ISO norm (str)


df_plot['date']=time_idx
type(df_plot['date'][0])


df_plot.to_csv('/Users/victhorvic/ads_covid-19/data/processed/COVID_inf_small_flat_table2.csv',sep=';',index=False)

# %% [4] Create relational model

''' Transformes the COVID data in a relational data set'''

#data_path='data/raw/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
pd_raw=pd.read_csv(data_path)

pd_data_base=pd_raw.rename(columns={'Country/Region':'country',
                      'Province/State':'state'})

pd_data_base['state']=pd_data_base['state'].fillna('no')

pd_data_base=pd_data_base.drop(['Lat','Long'],axis=1)


pd_relational_model=pd_data_base.set_index(['state','country']) \
                                .T                              \
                                .stack(level=[0,1])             \
                                .reset_index()                  \
                                .rename(columns={'level_0':'date',
                                                   0:'confirmed'},
                                                  )

pd_relational_model['date']=pd_relational_model.date.astype('datetime64[ns]')

pd_relational_model.to_csv('/Users/victhorvic/ads_covid-19/data/processed/COVID_relational_confirmed.csv',sep=';',index=False)
#print(' Number of rows stored: '+str(pd_relational_model.shape[0]))
#print(' Latest date is: '+str(max(pd_relational_model.date)))
