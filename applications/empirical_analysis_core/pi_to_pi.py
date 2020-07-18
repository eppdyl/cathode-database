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
File: pi_to_pi.py
Author: Pierre-Yves Taunay
Date: July 2020

Plot the pi products for the total pressure against one-another
'''

import matplotlib.pyplot as plt

def plot_pi_to_pi(data):
    fig, ax = plt.subplots(7,7)
    
    # For each pi product...
    for idxi in range(7):
        PIi_str = 'PI' + str(idxi+1)
        
        for idxj in range(7):
            if idxj >= idxi:
                PIj_str = 'PI' + str(idxj+1)
                
                ax[idxi][idxj].plot(data[[PIj_str]],data[[PIi_str]],'ko')
