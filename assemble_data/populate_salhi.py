import numpy as np
import pandas as pd

import cathode.constants as cc

from compute_attachment_length import compute_attachment_length


def populate_salhi_thesis(alldata,root,cat_root):
    ref = ("A. Salhi, \"Theoretical and experimental studies of orificed,  " 
           "hollow cathode operation,\" Ph.D. Thesis, The Ohio State University "
           "1993.")
    
    ### XENON GAS
    cat_name = 'Salhi-Xe'
    
    
    
    # For electron temperature and neutral density measurements, the xenon 
    # cathode was operated at 0.5 A and with an orifice diameter of 1.21 mm
    mdot = 0.5 # eq-A
    do = 1.21 # mm
    dc = 3.81 # mm
    Lo = 1.24 # mm
    Lc = 25.4 # mm
    
    # Electron temperature as functionof position
    data = np.genfromtxt(root + cat_root + 'Te_vs_x_do-1.21mm_Xe_Q-0.5A_Id-5-9-15A.csv',
                         skip_header = True,
                         delimiter=',')  
    current_array = np.array([5.,9.,15.])
    
    for idx,Id in enumerate(current_array):
        bcond = (alldata.cathode=='Salhi-Xe')
        bcond &= (alldata.dischargeCurrent == Id) 
        bcond &= (alldata.massFlowRate == mdot)
        
        Te_data = data[~np.isnan(data[:,idx+1])][:,[0,idx+1]]
    
        if alldata.loc[bcond].empty:
            alldata = alldata.append({'cathode' : cat_name, 
                                  'dischargeCurrent' : Id,
                                  'massFlowRate': mdot,
                                  'gas':'Xe',
                                  'orificeDiameter': do,
                                  'orificeLength': Lo,
                                  'insertDiameter': dc,
                                  'insertLength': Lc,
                                  'upstreamPressurePoint': 130.0,
                                  'electronTemperature': np.copy(Te_data),
                                  'reference': ref,
                                  'note': 'Fig. 5.7'
                                  } , ignore_index=True) 
        else:
            alldata.loc[bcond,'electronTemperature'] = alldata.loc[bcond,'electronTemperature'].apply(lambda x: np.copy(Te_data))

    # Electron temperature from spectroscopy measurements
    # Ignore 15 A bc. we already have positional data for that one
    current_array = np.array([3.,10.,20])
    
    for idx,Id in enumerate(current_array):
        bcond = (alldata.cathode=='Salhi-Xe')
        bcond &= (alldata.dischargeCurrent == Id) 
        bcond &= (alldata.massFlowRate == mdot)
    
        if Id == 3:
            tmpTe = 1.0
        elif Id == 10:
            tmpTe = 0.98
        elif Id == 15:
            tmpTe = 1.09
        elif Id == 20:
            tmpTe = 1.07
    
        if alldata.loc[bcond].empty:
            alldata = alldata.append({'cathode' : cat_name, 
                                  'dischargeCurrent' : Id,
                                  'massFlowRate': mdot,
                                  'gas':'Xe',
                                  'orificeDiameter': do,
                                  'orificeLength': Lo,
                                  'insertDiameter': dc,
                                  'insertLength': Lc,
                                  'upstreamPressurePoint': 130.0,
                                  'electronTemperature': tmpTe,
                                  'reference': ref,
                                  'note': 'Te: Fig. 5.28-5.31, ne: Fig. 5.34-5.36'
                                  } , ignore_index=True)                
        else:
            alldata.loc[bcond,'electronTemperature'] = alldata.loc[bcond,'electronTemperature'].apply(lambda x: tmpTe)
 
    # Density data
    # Grab the compiled data
    data = np.genfromtxt(root + cat_root + 'ne_vs_x_do-1.21mm_Xe_Q-0.5A.csv',
                         skip_header = 13,
                         names = True,
                         delimiter=',')      
    
    current_array = np.array([5.,9.,12.,15.])
    for idx,Id in enumerate(current_array):
        bcond = (alldata.cathode=='Salhi-Xe')
        bcond &= (alldata.dischargeCurrent == Id) 
        bcond &= (alldata.massFlowRate == mdot)
        
        csvcond = (data['Id'] == Id)
        tmp_data = data[csvcond][['x','log_ne']]
        
        ne_data = np.zeros((len(tmp_data['x']),2))
        ne_idx = 0
        for x,lne in zip(tmp_data['x'],tmp_data['log_ne']):
            ne_data[ne_idx,0] = x
            ne_data[ne_idx,1] = 10**(lne + 6.)
            ne_idx = ne_idx + 1

        Lem_xp, Lem_err = compute_attachment_length(ne_data, dc, idxmax=-1)
        
        if alldata.loc[bcond].empty:
            alldata = alldata.append({'cathode' : cat_name, 
                                  'dischargeCurrent' : Id,
                                  'massFlowRate': mdot,
                                  'gas':'Xe',
                                  'orificeDiameter': do,
                                  'orificeLength': Lo,
                                  'insertDiameter': dc,
                                  'insertLength': Lc,
                                  'upstreamPressurePoint': 130.0,
                                  'electronDensity': np.copy(ne_data),
                                  'reference': ref,
                                  'note': 'ne: Fig. 5.34-5.36',
                                  'attachmentLength': Lem_xp,
                                  'attachmentLength_err': Lem_err
                                  } , ignore_index=True)                
        else:
            alldata.loc[bcond,'electronDensity'] = alldata.loc[bcond,'electronDensity'].apply(lambda x: np.copy(ne_data)) 
            alldata.loc[bcond,'attachmentLength'] = Lem_xp
            alldata.loc[bcond,'attachmentLength_err'] = Lem_err       
            
    return alldata