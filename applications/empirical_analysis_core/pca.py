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
File: pca.py
Author: Pierre-Yves Taunay
Date: July 2020

Performs the PCA and plots it.
'''
import numpy as np
import matplotlib.pyplot as plt

from sklearn.decomposition import PCA

def plot_pca(pidata):
    ### PCA
    # Based on PI2 through PI7
    # Use log10 to decrease variation (e.g. PI4 ~ 1e14 vs. PI7 ~ 1e0)
    if plot_pca:
        X_train = np.array(np.log10(pidata))[:,1::]
        pca = PCA(n_components=6)
        pca.fit(X_train)
        cumsum = np.cumsum(pca.explained_variance_ratio_)
        plt.figure()
        plt.plot(np.arange(1,7,1),cumsum,'ko')
