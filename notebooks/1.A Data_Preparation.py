#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 01:56:03 2022

@author: victhorvic
"""

import pandas as pd
import numpy as np

from datetime import datetime

import matplotlib as mpl
import matplotlib.pyplot as plt


'''
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
pd_raw_inf.to_csv('../data/raw/COVID_infections_raw.csv',sep=';');


# data vaccined
#pd_raw_vac=pd.read_csv(data_path1,)
#pd_raw_vac.to_csv('../data/raw/COVID_vaccines_raw.csv',sep=';');

# %% 1
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


# %% 2
# Total population for each country: 
    # Mexico US Germany
pop = [128.9E6, 329.5E6, 83.24E6]

'''df_plot.set_index('date').div(pop).plot( title = 'The relative cases overtime of Covid infectors', 
                                        grid= True,   
                                        xlabel = 'Date',
                                        ylabel = 'The relative cases overtime of Covid infectors' ,                                                                            
                                                                             
                                        )
'''

'''Figure1: The relative cases overtime of Covid infectors (absolute Covid cases/population size) '''

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


# %% 3
'''Export csv file'''


''' Fix time_index'''
time_idx=[datetime.strptime( each,"%m/%d/%y") for each in df_plot.date] 
# convert to datetime

time_str=[each.strftime('%Y-%m-%d') for each in time_idx] 
# convert back to date ISO norm (str)


df_plot['date']=time_idx
type(df_plot['date'][0])

df_plot.to_csv('../data/processed/COVID_inf_small_flat_table.csv',sep=';',index=False)


