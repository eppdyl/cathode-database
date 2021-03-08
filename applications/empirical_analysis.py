# MIT License
# 
# Copyright (c) 2020-2021 Pierre-Yves Taunay 
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
File: empirical_analysis.py
Author: Pierre-Yves Taunay
Date: 2020

This file contains everything needed to perform the empirical analysis
presented in the following references:
    1. Taunay, P-Y, Wordingham, C J, and Choueiri, E Y, "An empirical
    scaling relationship for the total pressure in hollow cathodes," AIAA 
    Propulsion and Energy Forum, 2018, AIAA-2018-4428.
    2. Taunay, P-Y, "Scaling laws in thermionic orificed hollow cathodes," 
    Ph.D. dissertation, Princeton University, 2020
The following flags can be used to control the outputs:
- plot_pp_all: plot all Pi products against one another 
- plot_correlation: plot the correlation matrix 
- plot_pca: perform the PCA analysis 
- plot_lle: perform the manifold learning analysis (LLE) 
- plot_pi_correlation: plot the Pi-product power law correlation 
- randomization: perform the data randomization analysis   
- plot_theory_correlation: plot the Pi-product correlation from theory 

'''
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

try:
    import cathode.constants as cc
except ImportError:
    ### Ad-hoc solution if we don't have the cathode package
    ### Just define the constants...
    class cc:
        class M:
            Ar = 39.948
            Xe = 131.293
            Hg = 200.59

        atomic_mass = 1.66053904e-27
        Boltzmann = 1.38064852e-23
        e = 1.6021766208e-19
        kB = 1.38064852e-23
        mu0 = 4 * np.pi * 1e-6
        sccm2eqA = 0.07174496294893724
        Torr = 133.32236842105263


from empirical_analysis_core.correlation_matrix import plot_correlation_matrix 
from empirical_analysis_core.lle import plot_lle
from empirical_analysis_core.pca import plot_pca 
from empirical_analysis_core.power_law import power_law_analysis  
from empirical_analysis_core.pi_to_pi import plot_pi_to_pi
from empirical_analysis_core.randomization import perform_randomization

data = pd.read_hdf("cathode_database.h5",key="data")
gam = 5/3

constant_dict = {'pi':np.pi,
                 'q':cc.e,
                 'amu':cc.atomic_mass,
                 'gam':gam,
                 'kb':cc.Boltzmann,
                 'Torr':cc.Torr,
                 'mu0':cc.mu0}

#### PI PRODUCTS
# ASSUME ALL PI PRODUCTS ARE ALREADY CALCULATED. IF NOT, THEN UNCOMMENT THE
# LINES BELOW
#PI1_str = 'PI1 = totalPressure_SI / magneticPressure'
#PI2_str = 'PI2 = orificeDiameter / insertDiameter'
#PI3_str = 'PI3 = orificeDiameter / orificeLength'
#PI4_str = 'PI4 = (massFlowRate_SI * @q / (gasMass * @amu * dischargeCurrent))**2 * (gasMass * @amu * orificeDiameter * 1e-3)/(@mu0 * @q**2)'
#PI5_str = 'PI5 = gdPressure / magneticPressure'
#PI6_str = 'PI6 = izPressure / magneticPressure * orificeLength / orificeDiameter'
#PI7_str = 'PI7 = reynoldsNumber'
#
#data.eval(PI1_str, local_dict=constant_dict, inplace=True)
#data.eval(PI2_str, local_dict=constant_dict, inplace=True)
#data.eval(PI3_str, local_dict=constant_dict, inplace=True)
#data.eval(PI4_str, local_dict=constant_dict, inplace=True)
#data.eval(PI5_str, local_dict=constant_dict, inplace=True)
#data.eval(PI6_str, local_dict=constant_dict, inplace=True)
#data.eval(PI7_str, local_dict=constant_dict, inplace=True)

#### Pick out particular cathodes 
# Uncomment to pick some in particular
#bcond = (data.cathode == 'NSTAR') | (data.cathode=='NEXIS') 
#bcond |= (data.cathode =='Salhi-Xe') | (data.cathode=='Salhi-Ar-1.21') | (data.cathode =='Salhi-Ar-0.76')
#bcond |= (data.cathode =='Siegfried') | (data.cathode =='AR3') | (data.cathode=='EK6')
#bcond |= (data.cathode == 'SC012') | (data.cathode =='Friedly') | (data.cathode =='T6')
#bcond |= (data.cathode == 'Siegfried-NG') 
#bcond |= (data.cathode =='JPL-1.5cm') | (data.cathode =='JPL-1.5cm-3mm') | (data.cathode =='JPL-1.5cm-5mm')
#bcond |= (data.cathode=='PLHC')

### Grab the Pi products
pidata = data[['PI1','PI2','PI3','PI4','PI5','PI6','PI7']].dropna()


### PLOT ALL PI PRODUCTS AGAINST ONE ANOTHER
bplot_pp_all = False
bplot_correlation = False
bplot_pca = False 
bplot_lle = False
bplot_pi_correlation = False 
brandomization = True
bplot_theory_correlation = True

if bplot_pp_all:
    plot_pi_to_pi(data)
                
if bplot_correlation:
    plot_correlation_matrix(pidata)

if bplot_pca:
    plot_pca(pidata)

if bplot_lle:
    plot_lle(pidata)

if bplot_pi_correlation:
    power_law_analysis(data,pidata)
    
if brandomization:
    perform_randomization(data,pidata)

            
if bplot_theory_correlation:
    gam = 5/3
    Tgmin = 2000 # K
    Tgmax = 4000 # K
    
    alpha_min = 1 + 1/gam
    alpha_max = 1 + np.sqrt(2*np.pi) * (2/(gam+1)) ** (1/(gam-1)) / np.sqrt(gam)
    
    sqrt_min = 1
    sqrt_max = 2
    
    pidata = data[['PI1','PI2','PI5']]
    
    pi2 = np.array(pidata[['PI2']])
    pi5 = np.array(pidata[['PI5']])
    
    corr = 1/4 - np.log(pi2) + pi5 * (sqrt_min + alpha_min + (sqrt_max + alpha_max))/2

    plt.loglog(np.logspace(0,5),np.logspace(0,5),'k--')
    plt.xlim([0.5,1e5])
    plt.ylim([0.5,1e5])    
    plt.loglog(corr,pidata[['PI1']],'ko')

    plt.xlabel("1/4 - ln(PI2) + C PI5")
    plt.ylabel("Pi1")
    plt.title("Pi correlation from theory")
