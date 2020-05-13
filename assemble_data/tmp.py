""" pd_distribution.py
Load the pressure data and display total pressure x diameter for all cathodes
"""

import numpy as np
from sklearn.neighbors import KernelDensity
from sklearn.model_selection import GridSearchCV
#from sklearn.cross_validation import LeaveOneOut

import matplotlib.pyplot as plt

from assemble import assemble

data = assemble()

df = data.loc[(data['cathode'] != 'PLHC') & (data['cathode'] != 'JPL-1.5cm-3mm')]
Pdarr = np.array(df.pressureDiameter)
Pdarr = Pdarr[~np.isnan(Pdarr)]

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
#pdf = load_all_data()
#ldf = pdf['P'] * pdf['dc'] * 0.1
#ldf_do = pdf['P'] * pdf['do'] * 0.1

for cat in ['SC012','EK6','AR3']:
    Ptorr = data.loc[data['cathode'] == cat, 'totalPressure']
    do = data.loc[data['cathode'] == cat, 'orificeDiameter'] * 0.1
    data.loc[data['cathode'] == cat, 'pressureDiameter'] = Ptorr * do

df = data.loc[(data['cathode'] != 'PLHC') & (data['cathode'] != 'JPL-1.5cm-3mm')]
Pdarr_corr = np.array(df.pressureDiameter)
Pdarr_corr = Pdarr_corr[~np.isnan(Pdarr_corr)]

#Pdarr_corr = np.array([])
#for cat in ldf.index:
#    if (cat == 'SC012' or
#        cat == 'EK6' or
#        cat == 'AR3'):
#        vec = ldf_do[cat]
#    else:     
#        vec = ldf[cat]
#    
#    Pdarr_corr = np.concatenate((Pdarr_corr,vec))
#    
#plhc_data = pickle.load(open("20190404.pkl","rb"))
#for mdot in plhc_data:
#    data = plhc_data[mdot]
#    
#    Pd = data[:,2] * 2.715
#    
#    Pdarr_corr = np.concatenate((Pdarr_corr,Pd))
    
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
ax[1].hist(Pdarr_corr,bins=40,normed=True,histtype='step')

ax[0].fill_between(x_d, np.exp(logprob), alpha=0.5)
ax[0].plot(Pdarr, np.full_like(Pdarr, -0.01), '|k', markeredgewidth=1)


ax[1].fill_between(x_d, np.exp(logprob_corr), alpha=0.5)
ax[1].plot(Pdarr_corr, np.full_like(Pdarr_corr, -0.05), '|k', markeredgewidth=1)

