# MIT License
# 
# Copyright (c) 2017-2021 Pierre-Yves Taunay 
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

import numpy as np

### Find thhe max electron density and corresponding location from the ne vs x plots
data = np.genfromtxt("xenon_ne_vs_x_do-0.76mm_Id-2.3A.csv",delimiter=",",skip_header=13,names=True)
data19 = data[data['phi_wf']==1.9]
data25  = data[data['phi_wf']==2.5]

Id = 2.3 # A

print("Id,ne_max,x(ne_max)")
for data in [data19,data25]:
    xvec = data['x']
    yvec = data['ne']
        
    ne_max = np.max(yvec)*1e19
    idx = np.argmax(yvec)
    x_max = xvec[idx] # Convert from cm to mm

    print(Id,ne_max,x_max)
