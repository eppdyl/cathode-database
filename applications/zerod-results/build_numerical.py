# MIT License
# 
# Copyright (c) 2019-2021 Pierre-Yves Taunay 
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
import pickle
import pandas as pd
import numpy as np

try:
    import cathode.constants as cc
except ImportError:
    ### Ad-hoc solution if we don't have the cathode package
    ### Just define the constants...
    class cc:
        class M:
            Ar = 39.948
            Xe = 131.293
            Hg = 200.59

        atomic_mass = 1.66053904e-27
        Boltzmann = 1.38064852e-23
        e = 1.6021766208e-19
        kB = 1.38064852e-23
        mu0 = 4 * np.pi * 1e-6
        sccm2eqA = 0.07174496294893724
        Torr = 133.32236842105263

zerod_files = ['GOEBEL-1.5CM-LAB6_run_3000K.pkl',
         'GOEBEL-1.5CM-LAB6_run_3000K_12sccm.pkl',
         'NSTAR_run_3000K.pkl',
         'NEXIS_run_3000K.pkl',
         'Salhi-Xe_run_3000K.pkl',
         'Friedly_run_3000K.pkl',
         'plhc_run_2000K.pkl',
         'Salhi-Ar-1.21_run_3000K.pkl'
         ]

catname = ['JPL-1.5cm',
           'JPL-1.5cm',
           'NSTAR',
           'NEXIS',
           'Salhi-Xe',
           'Friedly',
           'PLHC',
           'Salhi-Ar-1.21']

def build_zerod_dataframe():
    # Empty dataframe    
    zerod_data = pd.DataFrame()
    
    for cat,f in zip(catname,zerod_files):
        loc = 'zerod-results/' + f
        data = pickle.load(open(loc,'rb'))
        
        for entry in data:
            Pgvec = np.zeros((len(entry),2))
            Ptotvec = np.zeros((len(entry),2))
            
            # Extract conditions
            extract = entry[0]
            conds = extract['input']
            
            massFlowRate = conds[0] * cc.e / conds[2]
            dischargeCurrent = conds[1]
            insertDiameter = conds[3] * 1e3
            orificeDiameter = conds[4] * 1e3
            orificeLength = conds[5] * 1e3
            
            if np.isclose(conds[2] / cc.atomic_mass, 131.293):
                gas = 'Xe'
            else:
                gas = 'Ar'
            
            
            for idx, elem in enumerate(entry):
                phis = elem['complete']['phi_s']
                Pg = elem['complete']['Pg']
                Ptot = elem['complete']['Ptot']
                Ptotvec[idx,0] = phis
                Ptotvec[idx,1] = Ptot
                
                Pgvec[idx,0] = phis
                Pgvec[idx,1] = Pg
                
            zerod_data = zerod_data.append({'cathode': cat,
                                            'dischargeCurrent': dischargeCurrent,
                                            'massFlowRate': massFlowRate,
                                            'gas': gas,
                                            'orificeDiameter': orificeDiameter,
                                            'orificeLength': orificeLength,
                                            'insertDiameter': insertDiameter,
                                            'neutralPressure': Pgvec,
                                            'neutralPressureAverage': np.nanmean(Pgvec[:,1]),
                                            'neutralPressureStd': np.nanstd(Pgvec[:,1]),
                                            'totalPressure': Ptotvec,
                                            'totalPressureAverage': np.nanmean(Ptotvec[:,1]),
                                            'totalPressureStd': np.nanstd(Ptotvec[:,1]),                                
                                            },ignore_index=True)
    

    return zerod_data
    
