#!/usr/bin/env python3# -*- coding: utf-8 -*-"""Created on Mon Jul  4 18:59:23 2022@author: victhorvic"""# %% [0] Librariesimport pandas as pdimport numpy as npfrom sklearn import linear_modelreg = linear_model.LinearRegression(fit_intercept=True)from scipy import signalimport matplotlib.pyplot as plt# %% [1] Get data# try to parse the dates right at the beginning # it works out of the box if the date was stored ISO YYYY-MM-DD format# infectionsdf_analyse = pd.read_csv('/Users/victhorvic/ads_covid-19/data/processed/COVID_inf_small_flat_table1.csv',                           sep=';', parse_dates=[0])