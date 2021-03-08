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
File: randomization.py
Date: 2019
Author: Pierre-Yves Taunay

Perform the randomization analysis of the Pi products to find which ones do
not matter
'''
import numpy as np

def perform_randomization(data,pidata):
    print("==================================================================")
    print('Pi-product randomized Correlation')
    print("==================================================================")

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
    print("Remove PI3 and PI6")
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
    
    print("New R-squared and average error")
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

    pilist = ["PI2","PI4","PI5","PI7"]
    for idx in np.arange(0,4):
        print(pilist[idx],rand_results[idx,0]/NITER,rand_results[idx,1]/NITER)              
     
        
        
    ### REMOVE PI2 AND PI7
    print("-----")
    print("Remove PI2 and PI7")
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
    
    print("New R-squared and average error")
    print("reference",R2,ave_err)
