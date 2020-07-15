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
File: lj_transport.py
Author: Pierre-Yves Taunay
Date: June 2020

This file contains functions to calculate transport properties assuming a
Lennard-Jones 12-6 interatomic potential.
'''

import cathode.resources as cres
import cathode.constants as cc
import numpy as np
import math

from scipy.interpolate import splrep,splev

def transport_properties(sig_lj,kbeps,M,Tvec):
    '''Calculate the transport properties from the Chapman-Enskog expansion,
    assuming a Lennard-Jones 12-6 potential. 
    The collision integrals for the 12-6 potential are stored in the file 
    'collision-integrals-lj.csv', as part of the "cathode" package.
    Inputs:
        - sig_lj: "sigma" in the Lennard-Jones 12-6 potential, m
        - kbeps: "epsilon" in the Lennard-Jones 12-6 potential normalized by 
        the Boltzmman constant, K
        - M: mass of the atom, in amu
        - Tvec: a vector of temperatures for which we compute the transport
        properties, K
    '''
    collision_file = cres.__path__[0] + '/collision-integrals-lj.csv'
    data = np.genfromtxt(collision_file,delimiter=',',names=True)
    
    Tlj = data['Tstar']
    omega22_data = splrep(Tlj,data['omega22'])
    omega23_data = splrep(Tlj,data['omega23'])
    omega24_data = splrep(Tlj,data['omega24'])
    
    
    omega_hs = lambda l,s:  math.factorial(s+1)/2. * (1. - 1./2.*(1. + (-1)**l)/(1.+l))*np.pi*sig_lj**2
    omega_hs22 = omega_hs(2,2)
    omega_hs23 = omega_hs(2,3)
    omega_hs24 = omega_hs(2,4)
        
    omega22 = np.sqrt(cc.Boltzmann*Tvec/(np.pi*M))*splev(Tvec/kbeps,omega22_data) * omega_hs22
    omega23 = np.sqrt(cc.Boltzmann*Tvec/(np.pi*M))*splev(Tvec/kbeps,omega23_data) * omega_hs23
    omega24 = np.sqrt(cc.Boltzmann*Tvec/(np.pi*M))*splev(Tvec/kbeps,omega24_data) * omega_hs24
    
    b11 = 4.* omega22
    b12 = 7.*omega22 - 2*omega23
    b22 = 301./12.*omega22 - 7*omega23 + omega24
    
    mu_lj = 5.*cc.Boltzmann*Tvec/2.*(1./b11 + b12**2./b11 * 1./(b11*b22-b12**2.))    
    
    return mu_lj
