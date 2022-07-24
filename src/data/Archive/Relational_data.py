#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 14:03:19 2022

@author: victhorvic
"""

# %% [0] Libraries
import pandas as pd
import numpy as np

from datetime import datetime

#%% [1] Get data

# infections
pd_proc1_inf = pd.read_csv('/Users/victhorvic/ads_covid-19/data/processed/COVID_inf_small_flat_table1.csv',
                           sep=';', parse_dates=[0])
# vaccines

pd_proc1_vac = pd.read_csv('/Users/victhorvic/ads_covid-19/data/processed/COVID_vac_small_flat_table1.csv',
                           sep=';', parse_dates=[0])

#%% [2] check data and convert to datetime formar correct

pd_proc1_inf.dtypes
pd_proc1_inf['date']=pd_proc1_inf.date.astype('datetime64[ns]')

pd_proc1_vac.dtypes
pd_proc1_vac['date']=pd_proc1_vac.date.astype('datetime64[ns]')