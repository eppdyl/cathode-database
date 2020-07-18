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
- plot_gp: attempt at Genetic Programming 
- plot_pi_correlation: plot the Pi-product power law correlation 
- randomization: perform the data randomization analysis   
- plot_theory_correlation: plot the Pi-product correlation from theory 

'''

import cathode.constants as cc
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt


import scipy.stats as sst

from empirical_analysis.pi_to_pi import plot_pi_to_pi


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
plot_pp_all = False
plot_correlation = False
plot_pca = False 
plot_lle = False
#plot_gp = False
plot_pi_correlation = False 
randomization = False
plot_theory_correlation = False

if plot_pp_all:
    plot_pi_to_pi(data)
                
if plot_correlation:
    plot_correlation_matrix(pidata)

if plot_pca:
    plot_pca(pidata)

if plot_lle:
    plot_lle(pidata)

if plot_pi_correlation:
    
if randomization:
    print('Pi-product randomized Correlation')

    PI1 = np.array(pidata['PI1'])
    Y = np.log10(PI1)
    X = (np.array(pidata[['PI2','PI3','PI4','PI5','PI6','PI7']]))

    X0 = np.ones(len(Y))
    X1 = np.log10(X[:,0]) # PI2
    X2 = np.log10(X[:,1]) # PI3
    X3 = np.log10(X[:,2]) # PI4 
    X4 = np.log10(X[:,3]) # PI5 
    X5 = np.log10(X[:,4]) # PI6
    X6 = np.log10(X[:,5]) # PI7


    rand_results = np.zeros((6,2))
    
    NITER=1000
    for niter in range(NITER):    
        for idx in np.arange(1,7):        
            Xlsq = np.array([X0,X1,X2,X3,X4,X5,X6]) 
            
            Xidx = Xlsq[idx,:]
            np.random.shuffle(Xidx)
            Xlsq[idx,:] = np.copy(Xidx)
        
        
            At = np.copy(Xlsq) # Include all
            A = np.transpose(At)
            b_vec = np.linalg.inv(At@A)@At@Y
        
    #        print(b_vec)
        
            C = 10**b_vec[0]
        
            X_sum = np.transpose(np.array([X0,X1,X2,X3,X4,X5,X6]))
            ## R squared
            # Residuals sum of squares
            rss = np.sum( (Y - np.sum(X_sum*b_vec,axis=1))**2)
            
            # Total sum of squares
        #    PI1ave = np.average(PI1)
            Yave = np.average(Y)
            tss = np.sum( (Y-Yave)**2)
            
            R2 = 1 - rss / tss
            
            ## Average error
            # Least squares
            P_xp = np.array(data[['totalPressure_SI']].dropna())[:,0]
            P_model = data[['totalPressure_SI','magneticPressure']].dropna()
            P_model = np.array(P_model[['magneticPressure']])[:,0]
            
            P_model *=  C *np.prod(X**b_vec[1:],axis=1) 
            
            
            vec_err =  np.abs((P_xp-P_model)/P_xp)* 100
            
            ave_err = np.average(vec_err) 
            
            rand_results[idx-1,0] += R2
            rand_results[idx-1,1] += ave_err
        
    for idx in np.arange(1,7):
        print(idx+1,rand_results[idx-1,0]/NITER,rand_results[idx-1,1]/NITER)    
        
        
    ### REMOVE PI3 AND PI6
    print("-----")
    X = (np.array(pidata[['PI2','PI4','PI5','PI7']]))
    X0 = np.ones(len(Y))
    X1 = np.log10(X[:,0]) # PI2
    X3 = np.log10(X[:,1]) # PI4 
    X4 = np.log10(X[:,2]) # PI5 
    X6 = np.log10(X[:,3]) # PI7

    # REFERENCE
    Xlsq = np.array([X0,X1,X3,X4,X6]) 
    At = np.copy(Xlsq) # Include all
    A = np.transpose(At)
    b_vec = np.linalg.inv(At@A)@At@Y
    C = 10**b_vec[0]

    X_sum = np.transpose(np.array([X0,X1,X3,X4,X6]))
    ## R squared
    # Residuals sum of squares
    rss = np.sum( (Y - np.sum(X_sum*b_vec,axis=1))**2)
    
    # Total sum of squares
    Yave = np.average(Y)
    tss = np.sum( (Y-Yave)**2)
    
    R2 = 1 - rss / tss
    
    ## Average error
    # Least squares
    P_xp = np.array(data[['totalPressure_SI']].dropna())[:,0]
    P_model = data[['totalPressure_SI','magneticPressure']].dropna()
    P_model = np.array(P_model[['magneticPressure']])[:,0]
    
    P_model *=  C *np.prod(X**b_vec[1:],axis=1) 
    
    
    vec_err =  np.abs((P_xp-P_model)/P_xp)* 100
    ave_err = np.average(vec_err)  
    
    print("reference",R2,ave_err)

    rand_results = np.zeros((4,2))
    NITER=1000
    for niter in range(NITER):     
        for idx in np.arange(1,5):
            Xlsq = np.array([X0,X1,X3,X4,X6]) 
            
            Xidx = Xlsq[idx,:]
            np.random.shuffle(Xidx)
            Xlsq[idx,:] = np.copy(Xidx)
        
        
            At = np.copy(Xlsq) # Include all
            A = np.transpose(At)
            b_vec = np.linalg.inv(At@A)@At@Y
        
    #        print(b_vec)
        
            C = 10**b_vec[0]
        
            X_sum = np.transpose(np.array([X0,X1,X3,X4,X6]))
            ## R squared
            # Residuals sum of squares
            rss = np.sum( (Y - np.sum(X_sum*b_vec,axis=1))**2)
            
            # Total sum of squares
        #    PI1ave = np.average(PI1)
            Yave = np.average(Y)
            tss = np.sum( (Y-Yave)**2)
            
            R2 = 1 - rss / tss
            
            ## Average error
            # Least squares
            P_xp = np.array(data[['totalPressure_SI']].dropna())[:,0]
            P_model = data[['totalPressure_SI','magneticPressure']].dropna()
            P_model = np.array(P_model[['magneticPressure']])[:,0]
            
            P_model *=  C *np.prod(X**b_vec[1:],axis=1) 
            
            
            vec_err =  np.abs((P_xp-P_model)/P_xp)* 100
            
            ave_err = np.average(vec_err) 
            
            rand_results[idx-1,0] += R2
            rand_results[idx-1,1] += ave_err

    for idx in np.arange(1,5):
        print(idx+1,rand_results[idx-1,0]/NITER,rand_results[idx-1,1]/NITER)              
     
        
        
    ### REMOVE PI2 AND PI7
    print("-----")
    X = (np.array(pidata[['PI4','PI5']]))
    X0 = np.ones(len(Y))
    X3 = np.log10(X[:,0]) # PI4 
    X4 = np.log10(X[:,1]) # PI5 

    # REFERENCE
    Xlsq = np.array([X0,X3,X4]) 
    At = np.copy(Xlsq) # Include all
    A = np.transpose(At)
    b_vec = np.linalg.inv(At@A)@At@Y
    C = 10**b_vec[0]

    X_sum = np.transpose(np.array([X0,X3,X4]))
    ## R squared
    # Residuals sum of squares
    rss = np.sum( (Y - np.sum(X_sum*b_vec,axis=1))**2)
    
    # Total sum of squares
    Yave = np.average(Y)
    tss = np.sum( (Y-Yave)**2)
    
    R2 = 1 - rss / tss
    
    ## Average error
    # Least squares
    P_xp = np.array(data[['totalPressure_SI']].dropna())[:,0]
    P_model = data[['totalPressure_SI','magneticPressure']].dropna()
    P_model = np.array(P_model[['magneticPressure']])[:,0]
    
    P_model *=  C *np.prod(X**b_vec[1:],axis=1) 
    
    
    vec_err =  np.abs((P_xp-P_model)/P_xp)* 100
    ave_err = np.average(vec_err)  
    
    print("reference",R2,ave_err)
            
if plot_theory_correlation:
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

