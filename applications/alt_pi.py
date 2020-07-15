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


data = assemble()
gam = 5/3

constant_dict = {'pi':np.pi,
                 'q':cc.e,
                 'amu':cc.atomic_mass,
                 'gam':gam,
                 'kb':cc.Boltzmann,
                 'Torr':cc.Torr,
                 'mu0':cc.mu0}



### PI PRODUCTS
PI1_str = 'PI1 = totalPressure_SI / magneticPressure'
PI2_str = 'PI2 = orificeDiameter / insertDiameter'
PI3_str = 'PI3 = orificeDiameter / orificeLength'
PI4_str = 'PI4 = (massFlowRate_SI * @q / (gasMass * @amu * dischargeCurrent))**2 * (gasMass * @amu * orificeDiameter * 1e-3)/(@mu0 * @q**2)'
PI5_str = 'PI5 = gdPressure / magneticPressure'
PI6_str = 'PI6 = izPressure / magneticPressure * orificeLength / orificeDiameter'
PI7_str = 'PI7 = reynoldsNumber'

data.eval(PI1_str, local_dict=constant_dict, inplace=True)
data.eval(PI2_str, local_dict=constant_dict, inplace=True)
data.eval(PI3_str, local_dict=constant_dict, inplace=True)
data.eval(PI4_str, local_dict=constant_dict, inplace=True)
data.eval(PI5_str, local_dict=constant_dict, inplace=True)
data.eval(PI6_str, local_dict=constant_dict, inplace=True)
data.eval(PI7_str, local_dict=constant_dict, inplace=True)


pidata = data[['PI1','PI2','PI3','PI4','PI5','PI6','PI7']].dropna()

print('Pi-product LSQ Correlation')

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

Xlsq = np.array([X0,X1,X2,X3,X4,X5,X6]) 

At = np.copy(Xlsq) # Include all
A = np.transpose(At)
b_vec = np.linalg.inv(At@A)@At@Y

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

### Compute the F-statistic
print("---------------")
print("F statistics,t statistics,p-value")
exp_vec = b_vec[1:]

Y = np.log10(PI1)
X = (np.array(pidata[['PI2','PI3','PI4','PI5','PI6','PI7']]))

X0 = np.ones(len(Y))
X1 = np.log10(X[:,0]) # PI2
X2 = np.log10(X[:,1]) # PI3
X3 = np.log10(X[:,2]) # PI4 
X4 = np.log10(X[:,3]) # PI5 
X5 = np.log10(X[:,4]) # PI6
X6 = np.log10(X[:,5]) # PI7

# We redo the fits, but remove one pi product at a time
for idx_stat in np.arange(1,7,1):
    Xvec = [X0,X1,X2,X3,X4,X5,X6]
    
    del(Xvec[idx_stat])
    At = np.array(Xvec)     
    A = np.transpose(At)
    beta_vec = np.linalg.inv(At@A)@At@Y    
    
    print(idx_stat+1,"Solution:", beta_vec)
    exp_vec_l = beta_vec[1:]
    C_l = 10**beta_vec[0]
    # RSS
    X_sum = np.transpose(np.array(Xvec))
    rss_0 = np.sum( (Y - np.sum(X_sum*beta_vec,axis=1))**2)

    # Fstat
    nmp = len(Y) - len(exp_vec) - 1 # n-p-1
    q = 1
    Fstat = (rss_0 - rss)/q 
    Fstat /= (rss/nmp)
    Fstat = np.abs(Fstat)
    
    tstat = np.sqrt(Fstat)
    
    pval = 2*(1-sst.t.cdf(tstat, len(Y)-1))
    pval = 2*sst.t.sf(tstat,len(Y)-1)
    
    print(idx_stat+1,Fstat,tstat,pval)
    print("--")    
    
    