import pickle
import pandas as pd
import numpy as np

import cathode.constants as cc

zerod_files = ['GOEBEL-1.5CM-LAB6_run_3000K.pkl',
         'GOEBEL-1.5CM-LAB6_run_3000K_12sccm.pkl',
         'NSTAR_run_3000K.pkl',
         'NEXIS_run_3000K.pkl']

catname = ['JPL-1.5cm',
           'JPL-1.5cm',
           'NSTAR',
           'NEXIS']

def build_zerod_dataframe():
    # Empty dataframe    
    zerod_data = pd.DataFrame()
    
    for cat,f in zip(catname,zerod_files):
        loc = 'zerod-results/' + f
        data = pickle.load(open(loc,'rb'))
        
        for entry in data:
            Pgvec = np.zeros((len(entry),2))
            
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
                                            'neutralPressureStd': np.nanstd(Pgvec[:,1])
                                            },ignore_index=True)
    

    return zerod_data
    
