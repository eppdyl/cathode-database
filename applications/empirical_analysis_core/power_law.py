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
File: power_law.py
Author: Pierre-Yves Taunay
Date: 2020

Perform the least-squares analysis, correlation, and plots the results.
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.neighbors import KernelDensity
from sklearn.model_selection import GridSearchCV

model_list = ["Power law","Poiseuille","Isentropic"]

def power_law_analysis(data,pidata):
    print("==================================================================")
    print('Pi-product LSQ Correlation')
    print("==================================================================")
    gam = 5./3.
    
    # Perform the actual regression
    Y, X, X_sum, C, b_vec = lsq_regression(pidata)

    ### R-squared and error
    ## Power law
    # Calculate the error in pressure
    ave_err = []
    err, vec_err = dimensional_error(data,C,X,b_vec)
    ave_err.append(err)

    # Calculate the R-squared for that fit
    R2 = []
    R2.append(r_squared(Y, X_sum, b_vec))

    ## Poiseuille
    C_poiseuille = 4/np.sqrt(gam)
    b_vec_poiseuille = np.array([np.log10(C_poiseuille),
                                 0.0,-0.5,0.0,1.0,0.0,-0.5])
    
    R2.append(r_squared(Y, X_sum, b_vec_poiseuille))
    err, _ = dimensional_error(data,C_poiseuille,X,b_vec_poiseuille)
    ave_err.append(err)

    ## Isentropic
    C_iso = 1/gam * ((gam+1)/2)**((gam+1)/(gam-1))
    b_vec_iso = np.array([np.log10(C_iso),0.0,0.0,0.0,1.0,0.0,0.0])


    R2.append(r_squared(Y, X_sum, b_vec_iso))
    err, _ = dimensional_error(data,C_iso,X,b_vec_iso)
    ave_err.append(err)

    print("---------------")
    print("STATISTICS: R2 AND AVERAGE ERROR")
    print("Model\t R^2 \t Average error")
    for r,e,m in zip(R2,ave_err,model_list):
        print(m,r,e)

    ### Plots
    plot_lsq_results(data,pidata,X,C,b_vec,vec_err)


def lsq_regression(pidata): 
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

    print("BETA VECTOR:")
    print(b_vec)

    # The leading constant of the power law 
    C = 10**b_vec[0]

    X_sum = np.transpose(np.array([X0,X1,X2,X3,X4,X5,X6]))

    return Y, X, X_sum, C, b_vec

def dimensional_error(data, C, X, b_vec):
    ## Average error
    # Least squares
    P_xp = np.array(data[['totalPressure_SI']].dropna())[:,0]
    P_model = data[['totalPressure_SI','magneticPressure']].dropna()
    P_model = np.array(P_model[['magneticPressure']])[:,0]
    
    P_model *=  C *np.prod(X**b_vec[1:],axis=1) 
    
    
    vec_err =  np.abs((P_xp-P_model)/P_xp)* 100
    
    ave_err = np.average(vec_err) 

    return ave_err, vec_err


def r_squared(Y, X_sum, b_vec):
    ### R squared
    # Residuals sum of squares
    rss = np.sum( (Y - np.sum(X_sum*b_vec,axis=1))**2)
    
    # Total sum of squares
    Yave = np.average(Y)
    tss = np.sum( (Y-Yave)**2)
    
    R2 = 1 - rss / tss


    return R2
    

def plot_lsq_results(data,pidata,X,C,b_vec,vec_err):
    print("---------------")
    print("KERNEL DENSITY FOR PRESSURE ERROR")
    
    ### KERNEL DENSITY OF PRESSURE ERROR
    # Calculate best kernel density bandwidth
    bandwidths = 10 ** np.linspace(0, 1, 200)
    grid = GridSearchCV(KernelDensity(kernel='gaussian'),
                        {'bandwidth': bandwidths},
                        cv=5,
                        verbose = 1)
    grid.fit(vec_err[:,None])
    
    print('Best params:',grid.best_params_)
    
    # Instantiate and fit the KDE model
    print("Instantiate and fit the KDE model")
    kde = KernelDensity(bandwidth=grid.best_params_['bandwidth'], 
                        kernel='gaussian')
    kde.fit(vec_err[:,None])
    # Score_samples returns the log of the probability density
    x_d = np.linspace(0,100,1000)
    logprob = kde.score_samples(x_d[:,None])
    plt.figure()
    plt.plot(x_d,np.exp(logprob))
    _ = plt.hist(vec_err,bins=40,normed=True,histtype='step')

    plt.title("Pressure error histogram and KDE")
    plt.xlabel("Pressure error (%)")
    plt.ylabel("Counts (a.u.)")


    print("---------------")
    plt.figure()
    plt.loglog(np.logspace(0,5),np.logspace(0,5),'k--')
    plt.xlim([0.5,1e5])
    plt.ylim([0.5,1e5])
    
    tmp_df = data[['totalPressure','massFlowRate','dischargeCurrent']].dropna()
    carr = np.array(tmp_df['massFlowRate']/tmp_df['dischargeCurrent'])
    plt.scatter(C *np.prod(X**b_vec[1:],axis=1) ,pidata[['PI1']],c=np.log10(np.array(pidata[['PI5']])))
    plt.title("Power law regression colored by PI5")
    plt.xlabel("G(Pi)")
    plt.ylabel("Pi1")
    
    
    plt.figure()
    plt.loglog(C *np.prod(X**b_vec[1:],axis=1) ,pidata[['PI1']],'ko')
    plt.loglog(np.logspace(0,5),np.logspace(0,5),'k--')
    plt.xlim([0.5,1e5])
    plt.ylim([0.5,1e5])
    plt.title("Power law regression")
    plt.xlabel("G(Pi)")
    plt.ylabel("Pi1")

#    df = pd.read_pickle(cathode.__path__[0] + '/experimental/files/datafile_index.pkl')
    df = pd.read_pickle("../../assemble_data/old/datafile_index.pkl")
    
    df_lsq = data[['cathode','totalPressure_SI','magneticPressure']].dropna() 
    model = C *np.prod(X**b_vec[1:],axis=1)

    df_lsq['model']= np.copy(model)
    
    plt.figure()
    for name in np.unique(data[['cathode']]):
#        print(name)
        
        try:
            color = np.unique(df['colors_mf'][name])[0]
        except:
            color = 'k'
        
        databycathode = data[['cathode','totalPressure']].dropna()
        lPI1 = pidata[['PI1']][databycathode.cathode==name]
        llsq = np.array(df_lsq[df_lsq.cathode==name][['model']])
        
        style = color
        # Get the style
        if name == 'AR3':
            color = 'k'
            marker = 'o'
        elif name == 'EK6':
            color = 'tab:olive'
            marker = 'o' 
        elif name == 'SC012':
            color = 'tab:cyan'
            marker = 'o' 
        elif name == 'Friedly':
            color = 'tab:pink'
            marker = 'o' 
        elif name == 'JPL-1.5cm' or name == 'JPL-1.5cm-3mm' or name == 'JPL-1.5cm-5mm':
            marker = 'o'
        elif name == 'NEXIS':
            color = 'tab:orange'
            marker = 'o' 
        elif name == 'NSTAR':
            color = 'tab:blue'
            marker = 'o' 
        elif name == 'PLHC':
            marker = 'o'
        elif name == 'Salhi-Ar-0.76' or name == 'Salhi-Ar-1.21':
#            color = np.unique(df['colors_mf']['Salhi-Ar-0.76'])[0]
            color = 'tab:red'
            marker = 'o' 
        elif name == 'Salhi-Xe':
            color = 'tab:purple'
            marker = 'o' 
        elif name == 'Siegfried':
            color = 'tab:brown'
            marker = 'o' 
        elif name == 'Siegfried-NG':
            color = 'tab:green'
            marker = 'o'
        elif name == 'T6':
            color = 'tab:gray'
            marker = 'o' 
        
#        print(color,marker)
        plt.loglog(llsq,lPI1,markerfacecolor=color,marker=marker,markeredgecolor='k',linestyle='')

    plt.title("Power law regression colored by cathode")
    plt.xlabel("G(Pi)")
    plt.ylabel("Pi1")            


def statistical_analysis(): 
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
    
#    # We redo the fits, but remove one pi product at a time
#    for idx_stat in np.arange(1,7,1):
#        Xvec = [X0,X1,X2,X3,X4,X5,X6]
#        
#        del(Xvec[idx_stat])
#        At = np.array(Xvec)     
#        A = np.transpose(At)
#        beta_vec = np.linalg.inv(At@A)@At@Y    
#        
#        print(idx_stat+1,"Solution:", beta_vec)
#        exp_vec_l = beta_vec[1:]
#        C_l = 10**beta_vec[0]
#        # RSS
#        X_sum = np.transpose(np.array(Xvec))
#        rss_0 = np.sum( (Y - np.sum(X_sum*beta_vec,axis=1))**2)
#    
#        # Fstat
#        nmp = len(Y) - len(exp_vec) - 1 # n-p-1
#        q = 1
#        Fstat = (rss_0 - rss)/q 
#        Fstat /= (rss/nmp)
#        Fstat = np.abs(Fstat)
#        
#        tstat = np.sqrt(Fstat)
#        
#        pval = 2*(1-sst.t.cdf(tstat, len(Y)-1))
#        pval = 2*sst.t.sf(tstat,len(Y)-1)
#        
#        print(idx_stat+1,Fstat,tstat,pval)
#        print("--")    

