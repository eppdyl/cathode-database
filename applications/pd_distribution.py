# MIT License
# 
# Copyright (c) 2019-2021 Pierre-Yves Taunay 
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

""" 
File: pd_distribution.py
Author: Pierre-Yves Taunay
Date: 2019

Load the pressure data and display total pressure x diameter for all cathodes
"""

import numpy as np
from sklearn.neighbors import KernelDensity
from sklearn.model_selection import GridSearchCV

import matplotlib.pyplot as plt
import pandas as pd


data = pd.read_hdf("cathode_database.h5",key="data")


Pdarr = np.array(data[['pressureDiameter']].dropna())

## KERNEL DENSITY
# Calculate best kernel density bandwidth
bandwidths = 10 ** np.linspace(0, 1, 200)
grid = GridSearchCV(KernelDensity(kernel='gaussian'),
                    {'bandwidth': bandwidths},
                    cv=5,
                    verbose = 1)
grid.fit(Pdarr)

print('Best params:',grid.best_params_)

# Instantiate and fit the KDE model
print("Instantiate and fit the KDE model")
kde = KernelDensity(bandwidth=grid.best_params_['bandwidth'], 
                    kernel='gaussian')
kde.fit(Pdarr)

# Score_samples returns the log of the probability density
x_d = np.linspace(0,100,1000)
logprob = kde.score_samples(x_d[:,None])

### CORRECT DOMONKOS
for cat in ['SC012','EK6','AR3']:
    Ptorr = data.loc[data['cathode'] == cat, 'totalPressure']
    do = data.loc[data['cathode'] == cat, 'orificeDiameter'] * 0.1
    data.loc[data['cathode'] == cat, 'pressureDiameter'] = Ptorr * do

Pdarr_corr = np.array(data.pressureDiameter)
Pdarr_corr = Pdarr_corr[~np.isnan(Pdarr_corr)]

## KERNEL DENSITY
# Calculate best kernel density bandwidth
bandwidths = 10 ** np.linspace(-1, 1, 200)
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


### Plots
fig, ax = plt.subplots(2,1)


ax[0].hist(Pdarr,bins=40,normed=True,histtype='step')
ax[0].fill_between(x_d, np.exp(logprob), alpha=0.5)
ax[0].plot(Pdarr, np.full_like(Pdarr, -0.01), '|k', markeredgewidth=1)

ax[1].hist(Pdarr_corr,bins=40,normed=True,histtype='step')
ax[1].fill_between(x_d, np.exp(logprob_corr), alpha=0.5)
ax[1].plot(Pdarr_corr, np.full_like(Pdarr_corr, -0.05), '|k', markeredgewidth=1)

