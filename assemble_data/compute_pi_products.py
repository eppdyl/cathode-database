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

#tdf = pd.read_csv("old_data.csv")
bcond = (data.cathode == 'NSTAR') | (data.cathode=='NEXIS') 
bcond |= (data.cathode =='Salhi-Xe') | (data.cathode=='Salhi-Ar-1.21') | (data.cathode =='Salhi-Ar-0.76')
bcond |= (data.cathode =='Siegfried') | (data.cathode =='AR3') | (data.cathode=='EK6')
bcond |= (data.cathode == 'SC012') | (data.cathode =='Friedly') | (data.cathode =='T6')
bcond |= (data.cathode == 'Siegfried-NG') 
bcond |= (data.cathode =='JPL-1.5cm') | (data.cathode =='JPL-1.5cm-3mm') | (data.cathode =='JPL-1.5cm-5mm')
bcond |= (data.cathode=='PLHC')
#bcond = (data.cathode != 'PLHC')
#pidata = data[bcond][['PI1','PI2','PI3','PI4','PI5','PI6','PI7']].dropna()
pidata = data[['PI1','PI2','PI3','PI4','PI5','PI6','PI7']].dropna()


### PLOT ALL PI PRODUCTS AGAINST ONE ANOTHER
plot_pp_all = False
plot_correlation = False
plot_pca = False
plot_lle = False
plot_gp = False
plot_pi_correlation = True
randomization = False
plot_theory_correlation = False

if plot_pp_all:
    fig, ax = plt.subplots(7,7)
    
    # For each pi product...
    for idxi in range(7):
        PIi_str = 'PI' + str(idxi+1)
        
        for idxj in range(7):
            if idxj >= idxi:
                PIj_str = 'PI' + str(idxj+1)
                
                ax[idxi][idxj].plot(data[[PIj_str]],data[[PIi_str]],'ko')
                
if plot_correlation:
    plt.imshow(np.abs(pidata.corr()), cmap='hot', interpolation='nearest')
    plt.show()
    # Commented code allows to output the colors for tikz
    #def cstm(x):
    #    return plt.cm.hot((np.clip(x,0,1)-0)/1.)
#    arr = np.abs(pidata.corr())
#    arr2 = np.array(arr)
#    for idxi,row in enumerate(arr2):
#        for idxj,col in enumerate(row):
#            cs = cstm(col)
#            cs1 = cs[0]
#            cs2 = cs[1]
#            cs3 = cs[2]
#            rcstr = 'c' + str(idxi+1) + str(idxj+1)
#            pstr = "\definecolor{" + rcstr + "}{rgb}{" + str(cs1) + "," + str(cs2) +"," + str(cs3) + "}"
#            print(pstr)
#        print(" ")
    


### PCA
# Based on PI2 through PI7
# Use log10 so decrease variation (e.g. PI4 ~ 1e14 vs. PI7 ~ 1e0)
if plot_pca:
    X_train = np.array(np.log10(pidata))[:,1::]
    pca = PCA(n_components=6)
    pca.fit(X_train)
    cumsum = np.cumsum(pca.explained_variance_ratio_)
    plt.figure()
    plt.plot(np.arange(1,7,1),cumsum,'ko')

if plot_lle:
    lle_data = np.array(pidata)
    n_components = 2  # 2 dimension

    X_r, err = locally_linear_embedding(lle_data, n_neighbors=14,
                                             n_components=n_components,
                                             eigen_solver='dense',
                                             method = 'standard')
    
    print("Done. Reconstruction error: %g" % err)
#    plt.scatter(X_r[:, 0], X_r[:, 1], s=5, c=np.log(lle_data[:,3])) 
    plt.scatter(X_r[:, 0], X_r[:, 1], s=5, c=np.log10(np.array(pidata[['PI4']]))) 
    
#    namedata = data[['cathode','pressureDiameter']].dropna()
#    arrnamed = np.array(namedata)[:,1]
    
#    shapeidx = np.array(['o','v','^','<','>','s','p','P','*','h','X','D','x'])
##, , , 'JPL-1.5cm', 'JPL-1.5cm-3mm',
##       'JPL-1.5cm-5mm', 'NEXIS', 'NSTAR', 'PLHC', 'SC012', 'Salhi-Ar-0.76',
##       'Salhi-Ar-1.21', 'Salhi-Xe', 'Siegfried', 'Siegfried-NG', 'T6'
#
#
#    shapeidx = np.array(['ro', # 'AR3'
#                         'ro', # 'EK6'
#                         'v', #'Friedly'
#                         'k^', # JPL
#                         'k^', # JPL
#                         'k^', # JPL
#                         '<', # NEXIS
#                         '>', # NSTAR
#                         's', # PLHC 
#                         'o', # SC012
#                         'p', # Salhi
#                         'p', # Salhi
#                         'p', # Salhi
#                         'P', # Siegfried Hg
#                         '*', # Siegfried NG
#                         'D']) # T6
 
#    plt.scatter(X_r[:, 0], X_r[:, 1], s=5,c=np.log10(namedata['pressureDiameter']))
#    for idx,name in enumerate(catname[0:9]):
#        X_sx = X_r[:,0][namedata['cathode']==name]
#        X_sy = X_r[:,1][namedata['cathode']==name]
        
#        plt.scatter(X_s[:, 0], X_s[:, 1], s=5) 
#        plt.plot(X_sx,X_sy,shapeidx[idx])
    
#    plt.figure()
#    X_embedded = TSNE(n_components=2,perplexity=30).fit_transform(lle_data)
#    plt.scatter(X_embedded[:, 0], X_embedded[:, 1], s=5, c=np.log(lle_data[:,3])) 


if plot_gp:
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import MinMaxScaler
    from sympy import init_printing
    
    init_printing(use_latex=True,forecolor="White")
    
#    Y = np.array(pidata['PI1'])
#    X = np.array(pidata[['PI2','PI3','PI4','PI5','PI6','PI7']])

    XY = np.array(pidata)
    min_max_scaler = MinMaxScaler()
    min_max_scaler.feature_range = (0.1,1)
    XY_train_minmax = min_max_scaler.fit_transform(XY)
    
    Y = XY_train_minmax[:,0]
    X = XY_train_minmax[:,1:]

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.1)

#    xm = np.min(X_train[:,2])
#    xM = np.max(X_train[:,2])
##    X_train[:,2] = (X_train[:,2] - xm) / (xM-xm)
##    X_train[:,2] *= 1e-12
##    X_train[:,4] *= 1e12
#
#    xm = np.min(X_train[:,4])
#    xM = np.max(X_train[:,4])
##    X_train[:,4] = (X_train[:,4] - xm) / (xM-xm)    
    
    
    def _powf(x1,x2):        
        with np.errstate(over='ignore'):
            return np.where(np.abs(x1**x2) < 100, x1**x2, 0.)

        
    
    powf = make_function(function=_powf,
                        name='powf',
                        arity=2)
    
    function_set = ['add', 'sub', 'mul', 'div',
                    'neg', 'inv']
    
    est_gp = SymbolicRegressor(population_size=5000,
                               generations=20, 
#                               tournament_size=50,
                               stopping_criteria=0.01,
                               const_range = (-10,10),
                               init_depth = (2,10),
                               function_set=function_set,
#                               p_crossover=0.7, 
#                               p_subtree_mutation=0.05,
#                               p_hoist_mutation=0.1, 
#                               p_point_mutation=0.1,
#                               max_samples=0.9, 
                               verbose=1,
#                               feature_names = ('\Pi_2','\Pi_3','\Pi_4','\Pi_5','\Pi_6','\Pi_7'),
#                               parsimony_coefficient=0.01, 
                               random_state=0,
                               n_jobs=1
                               )
    est_gp.fit(X_train, Y_train)
 
    from sympy import symbols, Add, Mul, Lambda, sympify
    import sympy as sp

    
    x,y = symbols('x y')
    loc = {
        "add": Add,
        "mul": Mul,
        "sub": Lambda((x, y), x - y),
        "div": Lambda((x, y), x/y),
        "sqrt": Lambda(x,sp.sqrt(sp.Abs(x))),
        "neg": Lambda(x,-x),
        "inv": Lambda(x,1/x),
        "powf": Lambda((x, y),x**y),
        "log": Lambda(x,sp.log(x)),
        "abs": Lambda(x,sp.Abs(x))
    }
    exp = sympify(est_gp._program,locals=loc)

    score_gp = est_gp.score(X_test, Y_test)
    print(exp)    
    print(score_gp)

    fres = []
    for row in pidata.iterrows():
        drow = row[1]
        X0 = (drow['PI2']- np.min(pidata[['PI2']])) / (np.max(pidata[['PI2']])-np.min(pidata[['PI2']]))
        X1 = (drow['PI3']- np.min(pidata[['PI3']]))/ (np.max(pidata[['PI3']])-np.min(pidata[['PI3']])) 
        X2 = (drow['PI4']- np.min(pidata[['PI4']]))/ (np.max(pidata[['PI4']])-np.min(pidata[['PI4']])) 
        X3 = (drow['PI5']- np.min(pidata[['PI5']]))/ (np.max(pidata[['PI5']])-np.min(pidata[['PI5']])) 
        X4 = (drow['PI6']- np.min(pidata[['PI6']]))/ (np.max(pidata[['PI6']])-np.min(pidata[['PI6']]))
        X5 = (drow['PI7']- np.min(pidata[['PI7']]))/ (np.max(pidata[['PI7']])-np.min(pidata[['PI7']]))
        tmp = exp.subs({'X0':X0,'X1':X1,'X2':X2,'X3':X3,'X4':X4,'X5':X5})
        fres.append(tmp)
    fres = np.array(fres)
    dPi = np.max(pidata[['PI1']]) - np.min(pidata[['PI1']])
    plt.loglog(fres,(pidata[['PI1']]-np.min(pidata[['PI1']]))/dPi,'ko')
#    plt.xlim([0.5,1e5])
#    plt.ylim([0.5,1e5])
    plt.loglog(np.logspace(0,5),np.logspace(0,5),'k--')

#    print(est_gp._program)
    
#    y_gp = est_gp.predict(np.c_[x0.ravel(), x1.ravel()]).reshape(x0.shape)
#    score_gp = est_gp.score(X_test, y_test)
    
if plot_pi_correlation:
    from sklearn.neighbors import KernelDensity
    from sklearn.model_selection import GridSearchCV
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

    print(b_vec)

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

    print(R2)
    
    ## Average error
    # Least squares
    P_xp = np.array(data[['totalPressure_SI']].dropna())[:,0]
    P_model = data[['totalPressure_SI','magneticPressure']].dropna()
    P_model = np.array(P_model[['magneticPressure']])[:,0]
    
    P_model *=  C *np.prod(X**b_vec[1:],axis=1) 
    
    
    vec_err =  np.abs((P_xp-P_model)/P_xp)* 100
    
    ave_err = np.average(vec_err) 
 
    # Poiseuille
    b_vec_poiseuille = np.array([0.0,-0.5,0.0,1.0,0.0,-0.5])
    C_poiseuille = 4/np.sqrt(gam)
    P_xp = np.array(data[['totalPressure_SI']].dropna())[:,0]
    P_model_poiseuille = data[['totalPressure_SI','magneticPressure']].dropna()
    P_model_poiseuille = np.array(P_model_poiseuille[['magneticPressure']])[:,0]
    
    P_model_poiseuille *=  C_poiseuille *np.prod(X**b_vec_poiseuille,axis=1) 
    vec_err_poiseuille =  np.abs((P_xp-P_model_poiseuille)/P_xp)* 100
    ave_err_poiseuille = np.average(vec_err_poiseuille) 




    # Isentropic
    b_vec_iso = np.array([0.0,0.0,0.0,1.0,0.0,0.0])
    C_iso = 1/gam * ((gam+1)/2)**((gam+1)/(gam-1))
    P_xp = np.array(data[['totalPressure_SI']].dropna())[:,0]
    P_model_iso = data[['totalPressure_SI','magneticPressure']].dropna()
    P_model_iso = np.array(P_model_iso[['magneticPressure']])[:,0]
    
    P_model_iso *=  C_iso *np.prod(X**b_vec_iso,axis=1) 
    vec_err_iso =  np.abs((P_xp-P_model_iso)/P_xp)* 100
    ave_err_iso = np.average(vec_err_iso)     

    ## R squared
    # Same job for Poiseuille
    X_models = np.transpose(np.array([X1,X2,X3,X4,X5,X6]))
    rss_pois = np.sum( (Y- np.log10(C_poiseuille) - np.sum(X_models*b_vec_poiseuille,axis=1))**2)
    R2_pois = 1 - rss_pois/tss
    
    # Same job for isentropic
    rss_iso = np.sum( (Y - np.log10(C_iso) - np.sum(X_models*b_vec_iso,axis=1))**2)
    R2_iso = 1 - rss_iso/tss


    ## KERNEL DENSITY
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
    plt.plot(x_d,np.exp(logprob))
    _ = plt.hist(vec_err,bins=40,normed=True,histtype='step')
    
    print("---------------")
    print("Statistics: R2 and average error")
    print("R^2,Average error")
    print(R2,ave_err)
    print("R^2,Average error (Poiseuille)")
    print(R2_pois,ave_err_poiseuille)
    print("R^2,Average error (isentropic)")
    print(R2_iso,ave_err_iso)

    plt.figure()
    plt.loglog(np.logspace(0,5),np.logspace(0,5),'k--')
    plt.xlim([0.5,1e5])
    plt.ylim([0.5,1e5])
    
    tmp_df = data[['totalPressure','massFlowRate','dischargeCurrent']].dropna()
    carr = np.array(tmp_df['massFlowRate']/tmp_df['dischargeCurrent'])
    plt.scatter(C *np.prod(X**b_vec[1:],axis=1) ,pidata[['PI1']],c=np.log10(np.array(pidata[['PI5']])))
    
    plt.figure()
    plt.loglog(C *np.prod(X**b_vec[1:],axis=1) ,pidata[['PI1']],'ko')
    plt.loglog(np.logspace(0,5),np.logspace(0,5),'k--')
    plt.xlim([0.5,1e5])
    plt.ylim([0.5,1e5])

    import cathode
    df = pd.read_pickle(cathode.__path__[0] + '/experimental/files/datafile_index.pkl')
    
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

        print(idx+1,R2,ave_err)    
        
        
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

        print(idx+1,R2,ave_err)           
     
        
        
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
    
    corr = 1/4 + np.log(pi2) + pi5 * (sqrt_min + alpha_min + (sqrt_max + alpha_max))/2

    plt.loglog(np.logspace(0,5),np.logspace(0,5),'k--')
    plt.xlim([0.5,1e5])
    plt.ylim([0.5,1e5])    
    plt.loglog(corr,pidata[['PI1']],'ko')


    