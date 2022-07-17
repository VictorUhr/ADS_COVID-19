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

data_path1 = 'https://github.com/govex/COVID-19/blob/a96dbc70eada30e83b1c475a328bb3cab4712741/data_tables/vaccine_data/global_data/time_series_covid19_vaccine_global.csv?raw=true'
## added ?raw=true to get last value and get the permantlink from Github


# data infections 
pd_raw_inf=pd.read_csv(data_path,)

# data for vaccined
pd_raw_vac=pd.read_csv(data_path1,)

# %% [2] Vaccination data
# to prepare the index timer 
time_idx=pd_raw_vac['Date'].unique()

df_plot = pd.DataFrame({
    'Date':time_idx})


pd2 = pd_raw_vac.drop(['Report_Date_String','UID','Province_State','People_partially_vaccinated'],axis=1)
''' check data of the countries '''

#Verify Germany data 
testde = pd_raw_vac[pd_raw_vac['Country_Region']=='Germany'].iloc[:,1::].set_index(['Date'])
#testde.dropna(subset=['People_fully_vaccinated']).iloc[:,0:3].plot(title = 'Germany')

#US Data
#pd2[pd2['Country_Region']=='US'].iloc[:,1::].set_index('Date')
#pd2[pd2['Country_Region']=='US'].iloc[:,1::].set_index('Date').plot(title = 'US')

# Mexico data
#pd2[pd2['Country_Region']=='Mexico'].iloc[:,1::].set_index('Date')
#pd2[pd2['Country_Region']=='Mexico'].iloc[:,1::].set_index('Date').plot(title ='Mexico')

# %%% [2.1] Cocatenate data
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

# %%%% [2.2] Verify data plot
# Total population for each country
        # Mexico US Germany
pop = [128.9E6, 329.5E6, 83.24E6]

''' Look for divide the data # not used '''
#concac[( 'Mexico')] = concac[('Mexico')].div(pop[0])
#concac[( 'US')] = concac[('US')].div(pop[1])
#concac[( 'Germany')] = concac[('Germany')].div(pop[2])


#concac[( 'Mexico', 'People_fully_vaccinated')] = concac[( 'Mexico', 'People_fully_vaccinated')].div(pop[0])
#concac[( 'US', 'People_fully_vaccinated')] = concac[( 'US', 'People_fully_vaccinated')].div(pop[1])
#concac[( 'Germany', 'People_fully_vaccinated')] = concac[( 'Germany', 'People_fully_vaccinated')].div(pop[2])

#not process data
concac[( 'Mexico')] = concac[('Mexico')]
concac[( 'US')] = concac[('US')]
concac[( 'Germany')] = concac[('Germany')]

# test the value 
#concac.plot()

# %%% [2.3] Save fig graph

''' Figure2: The vaccination rate over time '''

fig2 =concac.plot( grid = True,
                  xlabel = 'Date',
                  ylabel = 'Rate of the population',
                  title = 'The vaccination rate over time',  
                  
                  )

''' Save fig in the folder '''
fig2.figure.savefig('/Users/victhorvic/ads_covid-19/reports/figures/figure_2.png',dpi = 1000)
plt.show()

# %%% [2.4] Save to csv
'''Export csv file'''
df_plot1 = concac.reset_index()
df_plot1.to_csv('/Users/victhorvic/ads_covid-19/data/processed/COVID_vac_small_flat_table1.csv',sep=';',index=False)

# %% [3.1] Infections data
'''
Data for infections COVID¶
'''

# define time index
time_idx=pd_raw_inf.columns[4:]

df_plot= pd.DataFrame({'date':time_idx})

# define countries
country_list=['Mexico',
              'US',
              'Germany',
             ] 

for each in country_list:
    df_plot[each] = np.array(pd_raw_inf[pd_raw_inf['Country/Region']==each].iloc[:,4::].sum(axis=0))

#to see the graph
#df_plot.set_index('date').plot()


# %%% [3.2] Save fig graph
# Total population for each country: 
    # Mexico US Germany
pop = [128.9E6, 329.5E6, 83.24E6]

fig1 =df_plot.set_index('date').div(pop).plot( grid = True,
                                              xlabel = 'Date',
                                              ylabel = 'Confirmed cases (absolute Covid cases/population size)',
                                              title = 'The relative cases overtime of Covid infectors',        
                                              )

''' Save fig in the folder '''
#fig11 = fig1.figure 
#fig11.savefig('figure_1.png', dpi=300,)
fig1.figure.savefig('/Users/victhorvic/ads_covid-19/reports/figures/figure_1.png', dpi = 1000)
plt.show()

#to divided the data over population
#df_plot = df_plot.set_index('date').div(pop)
# not divided data 
df_plot = df_plot.set_index('date')
df_plot = df_plot.reset_index()

# %%% [3.3] Save to csv
'''Export csv file'''


''' Fix time_index'''
time_idx=[datetime.strptime( each,"%m/%d/%y") for each in df_plot.date] 
# convert to datetime

time_str=[each.strftime('%Y-%m-%d') for each in time_idx] 
# convert back to date ISO norm (str)


df_plot['date']=time_idx
type(df_plot['date'][0])


df_plot.to_csv('/Users/victhorvic/ads_covid-19/data/processed/COVID_inf_small_flat_table1.csv',sep=';',index=False)


