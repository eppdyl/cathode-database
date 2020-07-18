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
File: lle.py
Author: Pierre-Yves Taunay
Date: 2020

Perform the Local Linear Embedding of the total pressure Pi products.
'''
import numpy as np
import matplotlib.pyplot as plt

from sklearn.manifold import locally_linear_embedding, TSNE

def plot_lle(pidata, nneigh=14):
    lle_data = np.array(pidata)
    n_components = 2  # 2 dimension

    X_r, err = locally_linear_embedding(lle_data, n_neighbors=nneigh,
                                             n_components=n_components,
                                             eigen_solver='dense',
                                             method = 'standard')
    
    print("Done. Reconstruction error: %g" % err)
    plt.scatter(X_r[:, 0], X_r[:, 1], s=5, 
            c=np.log10(np.array(pidata[['PI4']]))) 
    
    ### COMMENTED CODE IS JUSTT ATTEMPTS AT DIFFERENT COLORINGS AND EMBEDDINGS
#    plt.scatter(X_r[:, 0], X_r[:, 1], s=5, c=np.log(lle_data[:,3])) 
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

