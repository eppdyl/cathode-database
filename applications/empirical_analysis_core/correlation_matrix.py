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
File: correlation_matrix.py
Author: Pierre-Yves Taunay
Date: July 2020

Plot the correlation matrix of all of the Pi-products
'''
import matplotlib.pyplot as plt
import numpy as np

def plot_correlation_matrix(pidata):
    plt.figure()
    plt.imshow(np.abs(pidata.corr()), cmap='hot', interpolation='nearest')
    plt.title("Pi-to-pi correlation matrix")
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

