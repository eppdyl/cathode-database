import cathode.constants as cc
import numpy as np

import matplotlib.pyplot as plt

from assemble import assemble

from sklearn.decomposition import PCA

from sklearn.manifold import locally_linear_embedding, TSNE

#data = assemble()

constant_dict = {'pi':np.pi,
                 'q':cc.e,
                 'amu':cc.atomic_mass,
                 'gam':5/3,
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

### PLOT ALL PI PRODUCTS AGAINST ONE ANOTHER
plot_pp_all = False
plot_correlation = False
plot_pca = False
plot_lle = True

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
    plt.scatter(X_r[:, 0], X_r[:, 1], s=5, c=np.log(lle_data[:,3])) 
    
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
#    ### Define the geometry
#    adjacency_method = 'cyflann'
#    adjacency_kwds = {'n_neighbors':10}
#    affinity_method = 'gaussian'
#    affinity_kwds = {'radius':1}
#    laplacian_method = 'symmetricnormalized'
#    laplacian_kwds = {'scaling_epps':1}
#    
#    geom  = {'adjacency_method':adjacency_method, 'adjacency_kwds':adjacency_kwds,
#             'affinity_method':affinity_method, 'affinity_kwds':affinity_kwds,
#             'laplacian_method':laplacian_method, 'laplacian_kwds':laplacian_kwds}
#    geom = Geometry(adjacency_method=adjacency_method, adjacency_kwds=adjacency_kwds,
#                    affinity_method=affinity_method, affinity_kwds=affinity_kwds,
#                    laplacian_method=laplacian_method, laplacian_kwds=laplacian_kwds)
#    
#    geom.set_data_matrix(lle_data)
#    
#    ### Define the embedding
#    lle = LocallyLinearEmbedding(n_components=n_components, eigen_solver='dense',geom=geom)
#    embed_lle = lle.fit_transform(lle_data)
#    
#    ### 
#    iso = Isomap(n_components=n_components, eigen_solver='dense', geom=geom)
#    embded_iso = iso.fit_transform(lle_data)
#    
##    plt.scatter(embed_lle[:, 0], embed_lle[:, 1], s=5, c=np.log(lle_data[:,3]))
#    
#    plt.scatter(embded_iso[:, 0], embded_iso[:, 1], s=5, c=np.log(lle_data[:,3]))

    
    

