# MIT License
# 
# Copyright (c) 2020 Pierre-Yves Taunay 
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
'''
File: flowrate_range.py
Author: Pierre-Yves Taunay
Date: 2020

Compute the allowed range of mass flow rates for a few cathodes, based on the
empirical result that Pd ~ 3.7 Torr-cm and a pressure model that is isentropic.
'''

import cathode.constants as cc
import numpy as np
import pandas as pd

data = pd.read_hdf("cathode_database.h5",key="data")

### NSTAR
### NEXIS
### PLHC
namelist = np.array(['NSTAR','NEXIS','PLHC'])
gam = 5/3
Tgmin = 2000 # K
Tgmax = 4000 # K

#alpha_min = 1 + 1/gam
#alpha_max = 1 + np.sqrt(2*np.pi) * (2/(gam+1)) ** (1/(gam-1)) / np.sqrt(gam)
#alpha_max = 1 + np.sqrt(2*np.pi) * ((gam+1)/2) ** (1/(gam-1)) / np.sqrt(gam)
#alpha_max = 3.2
alpha_min = 1/gam * ((gam+1)/2)**(gam/(gam-1))
alpha_max = np.sqrt(2*np.pi)*1/np.sqrt(gam)*(gam+1)/2

Cmin = 3.7 # Torr-cm
Cmax = 3.7 


print("cathode,demonstrated min, demonstrated max, estimated min, estimated max")
for name in namelist:
    df = data[data.cathode==name]
    
    if name == 'NEXIS':
        do = 2.5
    else:
        do = np.unique(df.orificeDiameter)[0]

    dc = np.unique(df.insertDiameter)[0]
    M = np.unique(df.gasMass)[0] * cc.atomic_mass
    Rg = cc.Boltzmann / M
       
    ### Min values
    amin = np.sqrt(gam * Rg * Tgmin)
    amax = np.sqrt(gam * Rg * Tgmax)
    
    mdot_max = Cmax * cc.Torr / (dc * 0.1) * np.pi * (do/2*1e-3)**2 / (amin  * alpha_min)
    mdot_min = Cmin * cc.Torr / (dc * 0.1) * np.pi * (do/2*1e-3)**2 / (amax  * alpha_max)
    
    xp_min = np.min(df.massFlowRate/cc.sccm2eqA)
    xp_max = np.max(df.massFlowRate/cc.sccm2eqA)
    
    print(name,xp_min,xp_max,mdot_min * cc.e / M / cc.sccm2eqA,mdot_max *  cc.e / M / cc.sccm2eqA)
