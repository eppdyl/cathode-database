import numpy as np
import pandas as pd

import cathode.constants as cc

from compute_attachment_length import compute_attachment_length, compute_average_temperature

def find_JPL_indexing(Id,mdot):
    idx = -1
    if np.isclose(mdot,12.):
        if Id == 20:
            idx = 40
        elif Id == 30:
            idx = 30
        elif Id == 40:
            idx = 30
        elif Id == 50:
            idx = 11
        elif Id == 60:
            idx = 6
        elif Id == 70:
            idx = 20
        elif Id == 80:
            idx = 23
        elif Id == 90:
            idx = 30
        elif Id == 100:
            idx = 20

    elif np.isclose(mdot,10.):
        if Id <= 90:
            idx = 50
        elif Id == 100:
            idx = 30

    elif np.isclose(mdot,8.):
        if Id == 20:
            idx = 15
        elif Id == 30:
            idx = 20
        elif Id == 40:
            idx = 30
        elif Id == 50:
            idx = 40
        elif Id == 60:
            idx = 20
        elif Id == 70:
            idx = 15
        elif Id == 80:
            idx = 15
        elif Id == 90:
            idx = 7
        elif Id == 100:
            idx = 50
    return idx


def populate_chu_2012(alldata,root,cat_root):
    ref = ("E. Chu and D. M. Goebel, \"High-current lanthanum hexaboride " 
           "hollow cathode for 10-to-50-kW hall thrusters,\" IEEE Trans. "
           "Plasma Sci., vol. 40, no. 9, pp. 2133–2144, 2012.")
    
    cat_name = 'JPL-1.5cm'
    
    do = 3.8
    Lo = 1.0
    dc = 7.0
    Lc = 25.4
    
    ### Density at 8 sccm
    current_array = np.arange(20,110,10)    
    current_array[-1] = 90
    current_array[-2] = 100
    
    data = np.genfromtxt(root + cat_root + 'ne_vs_x_Id-multiple_mdot-8sccm.csv',
                         skip_header = True,
                         delimiter=',')  
    
    for idx,Id in enumerate(current_array):
        ne_data = data[~np.isnan(data[:,idx+1])][:,[0,idx+1]]
        ne_data[:,0] *= 10 # mm
        ne_data[:,1] = 10**ne_data[:,1]
    
        npoints = find_JPL_indexing(Id,8.0)
        Lem_xp, Lem_err = compute_attachment_length(ne_data, dc, idxmin=-npoints)
    
        alldata = alldata.append({'cathode' : cat_name, 
                                  'dischargeCurrent' : Id,
                                  'massFlowRate': 8*cc.sccm2eqA,
                                  'gas':'Xe',
                                  'orificeDiameter': do,
                                  'orificeLength': Lo,
                                  'insertDiameter': dc,
                                  'insertLength': Lc,
                                  'upstreamPressurePoint': 13.0,
                                  'electronDensity': np.copy(ne_data),
                                  'reference': ref,
                                  'note': 'Fig. 9',
                                  'attachmentLength': Lem_xp,
                                  'attachmentLength_err':Lem_err
                                  } , ignore_index=True) 

    ### Density at 10 sccm
    current_array = np.arange(20,110,10)    
    mdot_sccm = 10.0
    
    data = np.genfromtxt(root + cat_root + 'ne_vs_x_Id-multiple_mdot-10sccm.csv',
                         skip_header = True,
                         delimiter=',')  
    
    for idx,Id in enumerate(current_array):
        ne_data = data[~np.isnan(data[:,idx+1])][:,[0,idx+1]]
        ne_data[:,0] *= 10 # mm
        ne_data[:,1] = 10**ne_data[:,1]

        npoints = find_JPL_indexing(Id,mdot_sccm)
        Lem_xp, Lem_err = compute_attachment_length(ne_data, dc, idxmin=-npoints)
    
        alldata = alldata.append({'cathode' : cat_name, 
                                  'dischargeCurrent' : Id,
                                  'massFlowRate': mdot_sccm*cc.sccm2eqA,
                                  'gas':'Xe',
                                  'orificeDiameter': do,
                                  'orificeLength': Lo,
                                  'insertDiameter': dc,
                                  'insertLength': Lc,
                                  'upstreamPressurePoint': 13.0,
                                  'electronDensity': np.copy(ne_data),
                                  'reference': ref,
                                  'note': 'Fig. 9',
                                  'attachmentLength': Lem_xp,
                                  'attachmentLength_err':Lem_err
                                  } , ignore_index=True) 
    ### Density at 12 sccm
    current_array = np.arange(20,110,10)    
    current_array[4] = 90.
    current_array[5] = 60.
    current_array[6] = 70.
    current_array[7] = 80.
    mdot_sccm = 12.0
    
    data = np.genfromtxt(root + cat_root + 'ne_vs_x_Id-multiple_mdot-12sccm.csv',
                         skip_header = True,
                         delimiter=',')  
    
    for idx,Id in enumerate(current_array):
        ne_data = data[~np.isnan(data[:,idx+1])][:,[0,idx+1]]
        ne_data[:,0] *= 10 # mm
        ne_data[:,1] = 10**ne_data[:,1]
        
        npoints = find_JPL_indexing(Id,mdot_sccm)
        Lem_xp, Lem_err = compute_attachment_length(ne_data, dc, idxmin=-npoints)
    
        alldata = alldata.append({'cathode' : cat_name, 
                                  'dischargeCurrent' : Id,
                                  'massFlowRate': mdot_sccm*cc.sccm2eqA,
                                  'gas':'Xe',
                                  'orificeDiameter': do,
                                  'orificeLength': Lo,
                                  'insertDiameter': dc,
                                  'insertLength': Lc,
                                  'upstreamPressurePoint': 13.0,
                                  'electronDensity': np.copy(ne_data),
                                  'reference': ref,
                                  'note': 'Fig. 9',
                                  'attachmentLength': Lem_xp,
                                  'attachmentLength_err':Lem_err                                  
                                  } , ignore_index=True) 

    ### Te, phip vs x for 50 A and 100 A
    # 50 A
    data = np.genfromtxt(root + cat_root + 'Te-phip_vs_x_mdot-multiple_Id-50A.csv',
                         skip_header = True,
                         delimiter=',')  

    mdot_array = np.array([8.,10.,12.]) * cc.sccm2eqA
    Id = 50
    
    for idx,mdot in enumerate(mdot_array):
        Te_data = data[~np.isnan(data[:,idx+4])][:,[0,idx+4]]
        phip_data = data[~np.isnan(data[:,idx+1])][:,[0,idx+1]]
        
        Te_xp, Te_err = compute_average_temperature(Te_data, dc)

        
        bcond = (alldata.cathode==cat_name) 
        bcond &= (alldata.dischargeCurrent == Id) 
        bcond &= (alldata.massFlowRate == mdot) 

        alldata.loc[bcond,'electronTemperature'] = alldata.loc[bcond,'electronTemperature'].apply(lambda x: np.copy(Te_data))
        alldata.loc[bcond,'plasmaPotential'] = alldata.loc[bcond,'plasmaPotential'].apply(lambda x: np.copy(phip_data))
        alldata.loc[bcond,'electronTemperatureAverage'] = Te_xp
        alldata.loc[bcond,'electronTemperatureAverage_err'] = Te_err

    # 100 A
    data = np.genfromtxt(root + cat_root + 'Te-phip_vs_x_mdot-multiple_Id-100A.csv',
                         skip_header = True,
                         delimiter=',')  

    mdot_array = np.array([8.,10.,12.]) * cc.sccm2eqA
    Id = 100
    
    for idx,mdot in enumerate(mdot_array):
        Te_data = data[~np.isnan(data[:,idx+4])][:,[0,idx+4]]
        phip_data = data[~np.isnan(data[:,idx+1])][:,[0,idx+1]]
        
        Te_xp, Te_err = compute_average_temperature(Te_data, dc)
        
        bcond = (alldata.cathode==cat_name) 
        bcond &= (alldata.dischargeCurrent == Id) 
        bcond &= (alldata.massFlowRate == mdot) 

        alldata.loc[bcond,'electronTemperature'] = alldata.loc[bcond,'electronTemperature'].apply(lambda x: np.copy(Te_data))
        alldata.loc[bcond,'plasmaPotential'] = alldata.loc[bcond,'plasmaPotential'].apply(lambda x: np.copy(phip_data))        

        alldata.loc[bcond,'electronTemperatureAverage'] = Te_xp
        alldata.loc[bcond,'electronTemperatureAverage_err'] = Te_err

    ### Te 1 cm upstream
    data = np.genfromtxt(root + cat_root + 'Te_vs_Id_mdot-multiple_Id-multiple.csv',
                         skip_header = True,
                         delimiter=',')
    # Make sure we get the round discharge currents
    data[:,0] = np.round(data[:,0]) 
    
    mdot_array = np.array([8.,10.,12.]) * cc.sccm2eqA

    for idx,mdot in enumerate(mdot_array):
        Te_data = data[~np.isnan(data[:,idx+1])][:,[0,idx+1]]
                
        for idxId, Id in enumerate(Te_data[:,0]):
            bcond = (alldata.cathode==cat_name) 
            bcond &= (alldata.dischargeCurrent == Id) 
            bcond &= (alldata.massFlowRate == mdot) 
            
            Te_xp = Te_data[idxId,1]
            Te_err = 0.5

            # If there is nothing there, fill it
            # Otherwise we already stored that data in a Te vs x array
            if alldata.loc[bcond,'electronTemperature'].isnull().all():
                alldata.loc[bcond,'electronTemperature'] = alldata.loc[bcond,'electronTemperature'].apply(lambda x: np.copy(Te_data[idxId,1]))           
                alldata.loc[bcond,'electronTemperatureAverage'] = Te_xp
                alldata.loc[bcond,'electronTemperatureAverage_err'] = Te_err
     
    ### Pressure for the 100 A case
    data = np.genfromtxt(root + cat_root + 'P_vs_mdot_Id-100A.csv',
                         skip_header = True,
                         delimiter=',')    
    
    Id = 100
    mdot_array = data[:,0] * cc.sccm2eqA
    
    for idx, mdot in enumerate(mdot_array):
        bcond = (alldata.cathode==cat_name) 
        bcond &= (alldata.dischargeCurrent == Id) 
        bcond &= (alldata.massFlowRate == mdot)         
        alldata.loc[bcond,'totalPressure'] = data[idx,1]
            
        
    return alldata


def populate_becatti_2017(alldata,root,cat_root):
    ref = ("G. Becatti, D. M. Goebel, J. E. Polk, and P. Guerrero, \"Life " 
           "Evaluation of a Lanthanum Hexaboride Hollow Cathode for "
           "High-Power Hall Thruster,\" J. Propuls. Power, vol. 34, no. 4, "
           "pp. 893–900, 2017.")

    dc = 7.0 
    Lc = 25.4
    Lo = 1.0
    

    ### Pressure upstream
    Id = 25 # A
    mdot = 13 * cc.sccm2eqA # A

    data = np.genfromtxt(root + cat_root + 'P_vs_do_mdot-13sccm_Id-25A.csv',
                         skip_header = True,
                         delimiter=',')     
    
    P3mm = data[~np.isnan(data[:,1])][:,1]
    P5mm = data[~np.isnan(data[:,2])][:,2]
    
    alldata = alldata.append({'cathode' : 'JPL-1.5cm-3mm', 
                                  'dischargeCurrent' : Id,
                                  'massFlowRate': mdot,
                                  'gas':'Xe',
                                  'orificeDiameter': 3.0,
                                  'orificeLength': Lo,
                                  'insertDiameter': dc,
                                  'insertLength': Lc,
                                  'upstreamPressurePoint': 13.0,
                                  'totalPressure': P3mm[0],
                                  'reference': ref,
                                  'note': 'Fig. 8'
                                  } , ignore_index=True)  
    
    alldata = alldata.append({'cathode' : 'JPL-1.5cm-5mm', 
                                  'dischargeCurrent' : Id,
                                  'massFlowRate': mdot,
                                  'gas':'Xe',
                                  'orificeDiameter': 5.0,
                                  'orificeLength': Lo,
                                  'insertDiameter': dc,
                                  'insertLength': Lc,
                                  'upstreamPressurePoint': 13.0,
                                  'totalPressure': P5mm[0],
                                  'reference': ref,
                                  'note': 'Fig. 8'
                                  } , ignore_index=True) 


    ### Density at 25 A
    mdot_array = np.array([10.5,13.1,14.9,19.8]) # sccm
    mdot_array *= cc.sccm2eqA
    Id = 25 # A
    
    # 3 mm   
    data = np.genfromtxt(root + cat_root + 'ne_vs_x_mdot-multiple_Id-25A_do-3mm.csv',
                         skip_header = True,
                         delimiter=',')  
    
    
    
    for idx,mdot in enumerate(mdot_array):
        ne_data = data[~np.isnan(data[:,idx+1])][:,[0,idx+1]]
        ne_data[:,1] = 10**ne_data[:,1]
            
        # We can arguably use the pressure at 25 A, 13 sccm for the 13.1 sccm case
        if mdot / cc.sccm2eqA == 13.1:
            totalPressure = P3mm[0]
            Lem_xp, Lem_err = compute_attachment_length(ne_data, dc, idxmin=-20, idxmax=-2)
        else:
            totalPressure= np.nan
            Lem_xp = np.nan
            Lem_err = np.nan
            
        alldata = alldata.append({'cathode' : 'JPL-1.5cm-3mm', 
                                  'dischargeCurrent' : Id,
                                  'massFlowRate': mdot,
                                  'totalPressure': totalPressure,
                                  'gas':'Xe',
                                  'orificeDiameter': 3.0,
                                  'orificeLength': Lo,
                                  'insertDiameter': dc,
                                  'insertLength': Lc,
                                  'upstreamPressurePoint': 13.0,
                                  'electronDensity': np.copy(ne_data),
                                  'reference': ref,
                                  'note': 'Fig. 6b',
                                  'attachmentLength': Lem_xp,
                                  'attachmentLength_err':Lem_err   
                                  } , ignore_index=True)     
    # 5 mm
    do = 5 # mm
    data = np.genfromtxt(root + cat_root + 'ne_vs_x_mdot-multiple_Id-25A_do-5mm.csv',
                         skip_header = True,
                         delimiter=',')  
    
    for idx,mdot in enumerate(mdot_array):
        ne_data = data[~np.isnan(data[:,idx+1])][:,[0,idx+1]]
        ne_data[:,1] = 10**ne_data[:,1]  
        
        # We can arguably use the pressure at 25 A, 13 sccm for the 13.1 sccm case
        if mdot / cc.sccm2eqA == 13.1:
            totalPressure = P5mm[0]
            Lem_xp, Lem_err = compute_attachment_length(ne_data, dc, idxmin=-22, idxmax=-3)
        else:
            totalPressure= np.nan
            Lem_xp = np.nan
            Lem_err = np.nan       
        
        alldata = alldata.append({'cathode' : 'JPL-1.5cm-5mm', 
                                  'dischargeCurrent' : Id,
                                  'massFlowRate': mdot,
                                  'totalPressure': totalPressure,
                                  'gas':'Xe',
                                  'orificeDiameter': 5.0,
                                  'orificeLength': Lo,
                                  'insertDiameter': dc,
                                  'insertLength': Lc,
                                  'upstreamPressurePoint': 13.0,
                                  'electronDensity': np.copy(ne_data),
                                  'reference': ref,
                                  'note': 'Fig. 6a',
                                  'attachmentLength': Lem_xp,
                                  'attachmentLength_err':Lem_err                                     
                                  } , ignore_index=True)  
    
    
    
    ### Density at 13 sccm
    # 3 mm
    current_array = np.array([8.9,15.6,25.1,31.3])    
    mdot = 13.*cc.sccm2eqA
    do = 3 # mm
    data = np.genfromtxt(root + cat_root + 'ne_vs_x_mdot-13sccm_Id-multiple_do-3mm.csv',
                         skip_header = True,
                         delimiter=',')  
    
    for idx,Id in enumerate(current_array):
        ne_data = data[~np.isnan(data[:,idx+1])][:,[0,idx+1]]
        ne_data[:,1] = 10**ne_data[:,1]   
        
        # We can arguably use the pressure at 25 A, 13 sccm for the 13.1 sccm case
        if Id == 25.1:
            totalPressure = P3mm[0]
            Lem_xp, Lem_err = compute_attachment_length(ne_data, dc, idxmin=-16, idxmax=-3)
        else:
            totalPressure= np.nan
            Lem_xp = np.nan
            Lem_err = np.nan           
        
        alldata = alldata.append({'cathode' : 'JPL-1.5cm-3mm', 
                                  'dischargeCurrent' : Id,
                                  'massFlowRate': mdot,
                                  'totalPressure': totalPressure,
                                  'gas':'Xe',
                                  'orificeDiameter': do,
                                  'orificeLength': 1.0,
                                  'insertDiameter': 7.,
                                  'insertLength': 25.4,
                                  'upstreamPressurePoint': 13.0,
                                  'electronDensity': np.copy(ne_data),
                                  'reference': ref,
                                  'note': 'Fig. 7b',
                                  'attachmentLength': Lem_xp,
                                  'attachmentLength_err':Lem_err                                   
                                  } , ignore_index=True)  

    # 5 mm
    current_array = np.array([8.9,15.6,25.1,35.1])    
    mdot = 13.*cc.sccm2eqA
    do = 5 # mm
    data = np.genfromtxt(root + cat_root + 'ne_vs_x_mdot-13sccm_Id-multiple_do-5mm.csv',
                         skip_header = True,
                         delimiter=',')  
    
    for idx,Id in enumerate(current_array):
        ne_data = data[~np.isnan(data[:,idx+1])][:,[0,idx+1]]
        ne_data[:,1] = 10**ne_data[:,1]     
        
        # We can arguably use the pressure at 25 A, 13 sccm for the 13.1 sccm case
        if Id == 25.1:
            totalPressure = P5mm[0]
            Lem_xp, Lem_err = compute_attachment_length(ne_data, dc, idxmin=-16, idxmax=-2)
        else:
            totalPressure= np.nan
            Lem_xp = np.nan
            Lem_err = np.nan           
        
        alldata = alldata.append({'cathode' : 'JPL-1.5cm-5mm', 
                                  'dischargeCurrent' : Id,
                                  'massFlowRate': mdot,
                                  'totalPressure': totalPressure,
                                  'gas':'Xe',
                                  'orificeDiameter': 5.0,
                                  'orificeLength': Lo,
                                  'insertDiameter': dc,
                                  'insertLength': Lc,
                                  'upstreamPressurePoint': 13.0,
                                  'electronDensity': np.copy(ne_data),
                                  'reference': ref,
                                  'note': 'Fig. 7b',
                                  'attachmentLength': Lem_xp,
                                  'attachmentLength_err':Lem_err                                   
                                  } , ignore_index=True)  

        
    

   
    
    return alldata