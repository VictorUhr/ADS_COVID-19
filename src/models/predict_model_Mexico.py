#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 18:56:16 2022

@author: victhorvic
"""

# %% [0] Libraries
import pandas as pd
import numpy as np


from scipy import optimize
from scipy import integrate

import matplotlib as mpl
import matplotlib.pyplot as plt

import seaborn as sns

sns.set(style="darkgrid")

mpl.rcParams['figure.figsize'] = (16, 9)
pd.set_option('display.max_rows', 500)
from sklearn import linear_model
reg = linear_model.LinearRegression(fit_intercept=True)

# %% [0] Funtions

# %%% [2.1] SIR model
def SIR_model(SIR,beta,gamma):
    ''' Simple SIR model
        S: susceptible population
        I: infected people
        R: recovered people
        beta: 
        
        overall condition is that the sum of changes (differnces) sum up to 0
        dS+dI+dR=0
        S+I+R= N (constant size of population)
    
    '''
    
    S,I,R=SIR
    dS_dt=-beta*S*I/N0          #S*I is the 
    dI_dt=beta*S*I/N0-gamma*I
    dR_dt=gamma*I
    return([dS_dt,dI_dt,dR_dt])


# %%% Functions SIR_model_t , integration
def SIR_model_t(SIR,t,beta,gamma):
    ''' Simple SIR model
        S: susceptible population
        t: time step, mandatory for integral.odeint
        I: infected people
        R: recovered people
        beta: 
        
        overall condition is that the sum of changes (differnces) sum up to 0
        dS+dI+dR=0
        S+I+R= N (constant size of population)
    
    '''
    
    S,I,R=SIR
    dS_dt=-beta*S*I/N0          #S*I is the 
    dI_dt=beta*S*I/N0-gamma*I
    dR_dt=gamma*I
    return dS_dt,dI_dt,dR_dt

def fit_odeint(x, beta, gamma):
    '''
    helper function for the integration
    '''
    return integrate.odeint(SIR_model_t, (S0, I0, R0), t, args=(beta, gamma))[:,1] # we only would like to get dI


# %% [1] Get data

# try to parse the dates right at the beginning 
# it works out of the box if the date was stored ISO YYYY-MM-DD format

# infections
df_analyse = pd.read_csv('/Users/victhorvic/ads_covid-19/data/processed/COVID_inf_small_flat_table1.csv',
                           sep=';', parse_dates=[0])

# %% [2] Basic parameters
# set some basic parameters
# beta/gamma is denoted as  'basic reproduction number'

N0=1000000 #max susceptible population
beta=0.4  # infection spread dynamics
gamma= 0.1  # recovery rate


# condition I0+S0+R0=N0
I0=df_analyse.Mexico[60]
S0=N0-I0
R0=0



# %% [3] Simulative SIR curves
'''Simulative approach to calculate SIR curves'''
SIR=np.array([S0,I0,R0])
propagation_rates=pd.DataFrame(columns={'susceptible':S0,
                                        'infected':I0,
                                        'recovered':R0})



for each_t in np.arange(len(df_analyse.Mexico)-65):
   
    new_delta_vec=SIR_model(SIR,beta,gamma)
   
    SIR=SIR+new_delta_vec
    
    propagation_rates=propagation_rates.append({'susceptible':SIR[0],
                                                'infected':SIR[1],
                                                'recovered':SIR[2]}, ignore_index=True);

# %%% [3.1] Plot Simulative
fig, ax1 = plt.subplots(1, 1)

ax1.plot(propagation_rates.index,propagation_rates.infected,label='infected',color='k')
ax1.plot(propagation_rates.index,propagation_rates.recovered,label='recovered')
ax1.plot(propagation_rates.index,propagation_rates.susceptible,label='susceptible')

ax1.set_ylim(10, 1500000)
ax1.set_yscale('linear')
ax1.set_title('Szenario SIR simulations (demonstration purposes only)',size=16)
ax1.set_xlabel('time in days',size=16)
ax1.legend(loc='best',
           prop={'size': 16});


# %% [4] Fitting the parameters of SIR model

ydata = np.array(df_analyse.Mexico[65:])
t=np.arange(len(ydata))

# ensure re-initialization 
I0=ydata[0]
S0=N0-I0
R0=0
#beta _ beta valuee?


# %%% Curve of the dif eq
# example curve of our differential equationa
popt=[0.4,0.1]
curve = fit_odeint(t, *popt)
# the resulting curve has to be fitted
# free parameters are here beta and gamma

fig = plt.figure()
plt.plot(curve)

# %%% Optimization
popt, pcov = optimize.curve_fit(fit_odeint, t, ydata)
perr = np.sqrt(np.diag(pcov))
print('\n\n\n\n ')    
print('standard deviation errors : ',str(perr), ' start infect:',ydata[0])
print("Optimal parameters: beta =", popt[0], " and gamma = ", popt[1])

# get the final fitted curve
fitted=fit_odeint(t, *popt)

fig1 = plt.figure()
plt.plot(fitted)

# %% Graph
fig1 = plt.figure()
plt.semilogy(t, ydata, 'o')
plt.semilogy(t, fitted)
plt.title("Fit of SIR model for Germany cases")
plt.ylabel("Population infected")
plt.xlabel("Days")
plt.show()
print('\n\n\n')  
print("Optimal parameters: beta =", popt[0], " and gamma = ", popt[1])
print("Basic Reproduction Number R0 " , popt[0]/ popt[1])
print("This ratio is derived as the expected number of new infections (these new infections are sometimes called secondary infections from a single infection in a population where all subjects are susceptible. @wiki")

# %%% Export to CSV
''' Export to CSV'''

Table = pd.DataFrame([t,ydata, fitted]).T
Table.columns = ('t', 'ydata', 'fitted')
Table.to_csv('/Users/victhorvic/ads_covid-19/data/interim/COVID_PR_Mx_table1.csv',
                         sep=';',index=False)

# %%% Export to optimum value 

np.savetxt('/Users/victhorvic/ads_covid-19/data/interim/popt_Mx.txt', popt)

# %% Dynamic beta in SIR (infection rate)
'''
t_initial=50
t_intro_measures=300
t_hold=310
t_relax=210

beta_max = 2
beta_min = -0.0011
gamma = - 0.0043
pd_beta=np.concatenate((np.array(t_initial*[beta_max]),
                       np.linspace(beta_max,beta_min,t_intro_measures),
                       np.array(t_hold*[beta_min]),
                        np.linspace(beta_min,beta_max,t_relax),
                       ))


#pd_beta

SIR=np.array([S0,I0,R0])
propagation_rates=pd.DataFrame(columns={'susceptible':S0,
                                        'infected':I0,
                                        'recovered':R0})

for each_beta in pd_beta:
   
    new_delta_vec=SIR_model(SIR,each_beta,gamma)
   
    SIR=SIR+new_delta_vec
    
    propagation_rates=propagation_rates.append({'susceptible':SIR[0],
                                                'infected':SIR[1],
                                                'recovered':SIR[2]}, ignore_index=True)
# %%
# Plot

plt.figure()
fig2, ax2 = plt.subplots(1, 1)

#ax2.plot(propagation_rates.index,propagation_rates.infected,label='infected',linewidth=3)

t_phases=np.array([t_initial,t_intro_measures,t_hold,t_relax]).cumsum()

ax2.bar(np.arange(len(ydata)),ydata, width=0.5,label='current infected Germany', color='r')
#ax2.axvspan(0,t_phases[0], facecolor='b', alpha=0.2,label='no measures')
#ax2.axvspan(t_phases[0],t_phases[1], facecolor='b', alpha=0.3,label='hard measures introduced')
#ax2.axvspan(t_phases[1],t_phases[2], facecolor='b', alpha=0.4,label='hold measures')
#ax2.axvspan(t_phases[2],t_phases[3], facecolor='b', alpha=0.5,label='relax measures')
#ax2.axvspan(t_phases[3],len(propagation_rates.infected), facecolor='b', alpha=0.6,label='repead hard measures')

ax2.set_ylim(10, 1.5*max(propagation_rates.infected))
ax2.set_yscale('log')
ax2.set_title('Szenario SIR simulations  (demonstration purposes only)',size=16)
ax2.set_xlabel('time in days',size=16)
#ax2.legend(loc='best',
#           prop={'size': 16});
'''