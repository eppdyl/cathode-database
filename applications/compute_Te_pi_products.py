import cathode.constants as cc
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from assemble import assemble

from sklearn.decomposition import PCA

from sklearn.manifold import locally_linear_embedding, TSNE

from gplearn.genetic import SymbolicRegressor
from gplearn.functions import make_function
import scipy.stats as sst


data = assemble(empirical_pressure=True)
gam = 5/3

constant_dict = {'pi':np.pi,
                 'q':cc.e,
                 'amu':cc.atomic_mass,
                 'gam':gam,
                 'kb':cc.Boltzmann,
                 'Torr':cc.Torr,
                 'mu0':cc.mu0}


### PI PRODUCTS
PI1_str = 'PI1 = electronTemperatureAverage * @q/@kb / ( (insertTemperatureAverage + 273.15)*3)'
PI2_str = 'PI2 = orificeDiameter / insertDiameter'
PI3_str = 'PI3 = totalPressure_SI * insertDiameter * 1e-3 / (gasMass * @amu) * ((gasMass * @amu)**2 / (massFlowRate_SI)**2)'
PI4_str = 'PI4 = (massFlowRate_SI * @q / (gasMass * @amu * dischargeCurrent))'

data.eval(PI1_str, local_dict=constant_dict, inplace=True)
data.eval(PI2_str, local_dict=constant_dict, inplace=True)
data.eval(PI3_str, local_dict=constant_dict, inplace=True)
data.eval(PI4_str, local_dict=constant_dict, inplace=True)

pidata = data[['PI1','PI2','PI3','PI4']].dropna()

plot_pi_correlation = True
if plot_pi_correlation:
    from sklearn.neighbors import KernelDensity
    from sklearn.model_selection import GridSearchCV
    print('Pi-product LSQ Correlation')

    PI1 = np.array(pidata['PI1'])
    Y = np.log10(PI1)
    X = (np.array(pidata[['PI2','PI3','PI4']]))

    X0 = np.ones(len(Y))
    X1 = np.log10(X[:,0]) # PI2
    X2 = np.log10(X[:,1]) # PI3
    X3 = np.log10(X[:,2]) # PI4 
    
    Xlsq = np.array([X0,X1,X2,X3]) 


    At = np.copy(Xlsq) # Include all
    A = np.transpose(At)
    b_vec = np.linalg.inv(At@A)@At@Y

    print(b_vec)

    C = 10**b_vec[0]

    X_sum = np.transpose(np.array([X0,X1,X2,X3]))
    ## R squared
    # Residuals sum of squares
    rss = np.sum( (Y - np.sum(X_sum*b_vec,axis=1))**2)
    
    # Total sum of squares
#    PI1ave = np.average(PI1)
    Yave = np.average(Y)
    tss = np.sum( (Y-Yave)**2)
    
    R2 = 1 - rss / tss

    print(R2)
    
    ## Average error
    # Least squares
    Te_xp = np.array(data[['totalPressure','electronTemperatureAverage']].dropna())[:,1]
    T_model = data[['totalPressure','electronTemperatureAverage','insertTemperatureAverage']].dropna()
    T_model = np.array(T_model[['insertTemperatureAverage']])[:,0]
    T_model += 273.15
    T_model *= 3.0
    
    T_model *=  C *np.prod(X**b_vec[1:],axis=1) 
    T_model *= cc.Boltzmann/cc.e
    
    
    vec_err =  np.abs((Te_xp-T_model)/Te_xp)* 100
    
    ave_err = np.average(vec_err) 
    
    print("---------------")
    print("Statistics: R2 and average error")
    print("R^2,Average error")
    print(R2,ave_err)

