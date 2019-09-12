""" pd_distribution.py
Load the pressure data and display total pressure x diameter for all cathodes
"""

import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import cathode.constants as cc

from cathode.experimental.load_data import load_all_data
from build_numerical import build_zerod_dataframe

from sklearn.neighbors import KernelDensity
from sklearn.grid_search import GridSearchCV
#from sklearn.cross_validation import LeaveOneOut

### FIRST CALCULATE THE TOTAL PRESSURE-DIAMETER PRODUCT
# Load total pressure data
pdf = load_all_data()
ldf = pdf['P'] * pdf['dc'] * 0.1

Pdarr = np.array([])
for cat in ldf.index:
    vec = ldf[cat]
    Pdarr = np.concatenate((Pdarr,vec))
    
plhc_data = pickle.load(open("20190404.pkl","rb"))
for mdot in plhc_data:
    data = plhc_data[mdot]
    
    Pd = data[:,2] * 2.715
    
    Pdarr = np.concatenate((Pdarr,Pd))
    
    
## KERNEL DENSITY
# Calculate best kernel density bandwidth
bandwidths = 10 ** np.linspace(0, 1, 200)
grid = GridSearchCV(KernelDensity(kernel='gaussian'),
                    {'bandwidth': bandwidths},
                    cv=5,
                    verbose = 1)
grid.fit(Pdarr[:,None])

print('Best params:',grid.best_params_)

# Instantiate and fit the KDE model
print("Instantiate and fit the KDE model")
kde = KernelDensity(bandwidth=grid.best_params_['bandwidth'], 
                    kernel='gaussian')
kde.fit(Pdarr[:,None])

# Score_samples returns the log of the probability density
x_d = np.linspace(0,100,1000)
logprob = kde.score_samples(x_d[:,None])

### CORRECT DOMONKOS
pdf = load_all_data()
ldf = pdf['P'] * pdf['dc'] * 0.1
ldf_do = pdf['P'] * pdf['do'] * 0.1

Pdarr_corr = np.array([])
for cat in ldf.index:
    if (cat == 'SC012' or
        cat == 'EK6' or
        cat == 'AR3'):
        vec = ldf_do[cat]
    else:     
        vec = ldf[cat]
    
    Pdarr_corr = np.concatenate((Pdarr_corr,vec))
    
plhc_data = pickle.load(open("20190404.pkl","rb"))
for mdot in plhc_data:
    data = plhc_data[mdot]
    
    Pd = data[:,2] * 2.715
    
    Pdarr_corr = np.concatenate((Pdarr_corr,Pd))
    
## KERNEL DENSITY
# Calculate best kernel density bandwidth
bandwidths = 10 ** np.linspace(0, 1, 200)
grid = GridSearchCV(KernelDensity(kernel='gaussian'),
                    {'bandwidth': bandwidths},
                    cv=5,
                    verbose = 1)
grid.fit(Pdarr_corr[:,None])

print('Best params:',grid.best_params_)

# Instantiate and fit the KDE model
print("Instantiate and fit the KDE model")
kde = KernelDensity(bandwidth=grid.best_params_['bandwidth'], 
                    kernel='gaussian')
kde.fit(Pdarr_corr[:,None])

# Score_samples returns the log of the probability density
x_d = np.linspace(0,100,1000)
logprob_corr = kde.score_samples(x_d[:,None])

#
#
#### NOW CALCULATE THE NEUTRAL GAS PRESSURE-DIAMETER PRODUCT FROM 0D RESULTS
#zerod = build_zerod_dataframe()
#ldf = zerod['neutralPressureAverage'] /cc.Torr * zerod['insertDiameter'] * 0.1
#
#Pdarr_zd = np.array([ldf])
#Pdarr_zd = Pdarr_zd[~np.isnan(Pdarr_zd)]
#
#    
### KERNEL DENSITY
## Calculate best kernel density bandwidth
#grid = GridSearchCV(KernelDensity(kernel='gaussian'),
#                    {'bandwidth': bandwidths},
#                    cv=5,
#                    verbose = 1)
#grid.fit(Pdarr_zd[:,None])
#
#print('Best params:',grid.best_params_)
#
## Instantiate and fit the KDE model
#print("Instantiate and fit the KDE model")
#kde = KernelDensity(bandwidth=grid.best_params_['bandwidth'], 
#                    kernel='gaussian')
#kde.fit(Pdarr_zd[:,None])
#
## Score_samples returns the log of the probability density
#x_d = np.linspace(0,100,1000)
#logprob_zd = kde.score_samples(x_d[:,None])

### Plots
plt.hist(Pdarr,bins=40,normed=True,histtype='step')
plt.hist(Pdarr_corr,bins=40,normed=True,histtype='step')

plt.fill_between(x_d, np.exp(logprob), alpha=0.5)
plt.plot(Pdarr, np.full_like(Pdarr, -0.01), '|k', markeredgewidth=1)


plt.fill_between(x_d, np.exp(logprob_corr), alpha=0.5)
plt.plot(Pdarr_corr, np.full_like(Pdarr_corr, -0.05), '|k', markeredgewidth=1)

