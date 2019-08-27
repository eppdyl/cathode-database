import pandas as pd
import numpy as np
import ast

import cathode.constants as cc

root = '/Users/Pyt/Documents/Pyt/hollow_cathode/cathode-data'

def from_np_array(array_string):
    ''' See https://stackoverflow.com/questions/42755214/how-to-keep-numpy-array-when-saving-pandas-dataframe-to-csv
    Modified to take the possibility of a NaN into account
    '''
    try:
        array_string = ','.join(array_string.replace('[ ', '[').split())
        return np.array(ast.literal_eval(array_string))
    except:
        return np.nan

def populate_NEXIS(alldata):
    nexis_root = '/jpl/nexis/staging/'
    
    ### mdot = 5.5 sccm, Id = 25 A
    # Source: Mikellides JAP 2005
    # First get the density
    data = np.genfromtxt(root + nexis_root + 'ne_vs_x_mdot-5.5sccm_Id-25A.csv',
                         delimiter=',')
    
    data[:,1] *= 1e20
    
    ref = ("I. G. Mikellides, I. Katz, D. M. Goebel, and J. E. Polk, "
           "\"Hollow cathode theory and experiment. II. A two-dimensional "
           "theoretical model of the emitter region,\" J. Appl. Phys., "
           "vol. 98, no. 2005, pp. 0–14, 2005.")
    
    ne_data = np.copy(data)
    
    # Then get temperature and potential
    data = np.genfromtxt(root + nexis_root + 'Te-phip_vs_x_mdot-5.5sccm_Id-25A.csv',
                         skip_header = True,
                         delimiter=',')
    phip_data = data[~np.isnan(data[:,1])][:,0:2]
    Te_data = data[~np.isnan(data[:,2])][:,0::2]
    
    alldata = alldata.append({'cathode' : 'NEXIS', 
                              'dischargeCurrent' : 25.,
                              'massFlowRate': 5.5*cc.sccm2eqA,
                              'gas':'Xe',
                              'orificeDiameter': np.unique(alldata[alldata.cathode=='NEXIS'].orificeDiameter),
                              'orificeLength': np.unique(alldata[alldata.cathode=='NEXIS'].orificeLength),
                              'insertDiameter': np.unique(alldata[alldata.cathode=='NEXIS'].insertDiameter),
                              'insertLength': np.unique(alldata[alldata.cathode=='NEXIS'].insertLength),
                              'upstreamPressurePoint': np.unique(alldata[alldata.cathode=='NEXIS'].upstreamPressurePoint),
                              'electronDensity': np.copy(ne_data),
                              'electronTemperature': np.copy(Te_data),
                              'plasmaPotential': np.copy(phip_data),
                              'reference': ref,
                              'note': 'Fig. 5'
                              } , ignore_index=True)

    ### mdot = 5.5 sccm, Id = 10 A
    # Source: Goebel JPC 2004    
    ref = ("D. Goebel, K. K. Jameson, R. M. Watkins, and I. Katz, "
           "\"Hollow Cathode and Keeper-Region Plasma Measurements Using "
           "Ultra-Fast Miniature Scanning Probes,\" 40th JPC, 2004.")
    note = ("Fig. 12")
    
    # This one only has temperature and potential
    data = np.genfromtxt(root + nexis_root + 'Te-phip_vs_x_mdot-5.5-10sccm_Id-10-25A.csv',
                         skip_header = True,
                         delimiter=',')
    
    Te_data = data[~np.isnan(data[:,1])][:,[0,1]]
    phip_data = data[~np.isnan(data[:,2])][:,[0,2]]
    
    bcond = (alldata.cathode=='NEXIS') & (alldata.dischargeCurrent == 10.) & (alldata.massFlowRate == 5.5*cc.sccm2eqA)
    alldata.loc[bcond,'electronTemperature'] = alldata.loc[bcond,'electronTemperature'].apply(lambda x: np.copy(Te_data))
    alldata.loc[bcond,'plasmaPotential'] = alldata.loc[bcond,'plasmaPotential'].apply(lambda x: np.copy(phip_data))
    alldata.loc[bcond,'reference'] = alldata.loc[bcond,'reference'] + "[2] " + ref
    alldata.loc[bcond,'note'] = alldata.loc[bcond,'note'] + "[2] " + note


    ### mdot = 10 sccm, Id = 25 A
    # Source: Goebel JPC 2004    
    ref = ("D. Goebel, K. K. Jameson, R. M. Watkins, and I. Katz, "
           "\"Hollow Cathode and Keeper-Region Plasma Measurements Using "
           "Ultra-Fast Miniature Scanning Probes,\" 40th JPC, 2004.")
 
    data = np.genfromtxt(root + nexis_root + 'ne_vs_x_mdot-5-10sccm_Id-25A.csv',
                         delimiter=',')
    data[:,1] *= 1e20
    ne_data = np.copy(data)
    
    data = np.genfromtxt(root + nexis_root + 'Te-phip_vs_x_mdot-5.5-10sccm_Id-10-25A.csv',
                         skip_header = True,
                         delimiter=',')
    
    Te_data = data[~np.isnan(data[:,3])][:,[0,3]]
    phip_data = data[~np.isnan(data[:,4])][:,[0,4]]
    
    alldata = alldata.append({'cathode' : 'NEXIS', 
                              'dischargeCurrent' : 25.,
                              'massFlowRate': 10*cc.sccm2eqA,
                              'gas':'Xe',
                              'orificeDiameter': np.unique(alldata[alldata.cathode=='NEXIS'].orificeDiameter),
                              'orificeLength': np.unique(alldata[alldata.cathode=='NEXIS'].orificeLength),
                              'insertDiameter': np.unique(alldata[alldata.cathode=='NEXIS'].insertDiameter),
                              'insertLength': np.unique(alldata[alldata.cathode=='NEXIS'].insertLength),
                              'upstreamPressurePoint': np.unique(alldata[alldata.cathode=='NEXIS'].upstreamPressurePoint),
                              'electronDensity': np.copy(ne_data),
                              'electronTemperature': np.copy(Te_data),
                              'plasmaPotential': np.copy(phip_data),
                              'reference': ref,
                              'note': 'Fig. 12'
                              } , ignore_index=True)  
    
    
    return alldata


def populate_NSTAR(alldata):
    nstar_root = '/jpl/nstar/discharge/staging/'
    
    ### TH8
    # mdot = 2.47 sccm, Id = 8.24 A
    data = np.genfromtxt(root + nstar_root + 'ne_vs_position_TH8-TH15.csv',
                         skip_header = True,
                         delimiter=',')    
    
    ne_data = data[~np.isnan(data[:,1])][:,[0,1]]
    ne_data[:,1] = 10**ne_data[:,1]
    
    data = np.genfromtxt(root + nstar_root + 'phip-Te_vs_position_TH8-TH15.csv',
                         skip_header = True,
                         delimiter=',')     


    Te_data = data[~np.isnan(data[:,2])][:,[0,2]]
    phip_data = data[~np.isnan(data[:,1])][:,[0,1]]    
    
    bcond = (alldata.cathode=='NSTAR') & (alldata.dischargeCurrent == 8.24) & (alldata.massFlowRate == 3.7*cc.sccm2eqA)
    alldata.loc[bcond,'electronDensity'] = alldata.loc[bcond,'electronDensity'].apply(lambda x: np.copy(ne_data))
    alldata.loc[bcond,'electronTemperature'] = alldata.loc[bcond,'electronTemperature'].apply(lambda x: np.copy(Te_data))
    alldata.loc[bcond,'plasmaPotential'] = alldata.loc[bcond,'plasmaPotential'].apply(lambda x: np.copy(phip_data))
    
    
    ### TH15
    # mdot = 3.7 sccm, Id = 13.3 A
    # mdot = 2.47 sccm, Id = 8.24 A
    data = np.genfromtxt(root + nstar_root + 'ne_vs_position_TH8-TH15.csv',
                         skip_header = True,
                         delimiter=',')    
    
    ne_data = data[~np.isnan(data[:,2])][:,[0,2]]
    ne_data[:,1] = 10**ne_data[:,1]
    
    data = np.genfromtxt(root + nstar_root + 'phip-Te_vs_position_TH8-TH15.csv',
                         skip_header = True,
                         delimiter=',')     


    Te_data = data[~np.isnan(data[:,4])][:,[0,4]]
    phip_data = data[~np.isnan(data[:,3])][:,[0,3]] 
    
    bcond = (alldata.cathode=='NSTAR') & (alldata.dischargeCurrent == 13.3) & (alldata.massFlowRate == 3.7*cc.sccm2eqA)
    alldata.loc[bcond,'electronDensity'] = alldata.loc[bcond,'electronDensity'].apply(lambda x: np.copy(ne_data))
    alldata.loc[bcond,'electronTemperature'] = alldata.loc[bcond,'electronTemperature'].apply(lambda x: np.copy(Te_data))
    alldata.loc[bcond,'plasmaPotential'] = alldata.loc[bcond,'plasmaPotential'].apply(lambda x: np.copy(phip_data))
    
    return alldata

def populate_JPL_lab6(alldata):
    cat_root = '/jpl/goebel-lab6-cathodes/1.5cm-cathode/staging/'
    
    ref = ("E. Chu and D. M. Goebel, \"High-current lanthanum hexaboride " 
           "hollow cathode for 10-to-50-kW hall thrusters,\" IEEE Trans. "
           "Plasma Sci., vol. 40, no. 9, pp. 2133–2144, 2012.")
    
    ### Density at 8 sccm
    current_array = np.arange(20,110,10)    
    current_array[-1] = 90
    current_array[-2] = 100
    
    data = np.genfromtxt(root + cat_root + 'ne_vs_x_Id-multiple_mdot-8sccm_1.5cm-cathode-raw.csv',
                         skip_header = True,
                         delimiter=',')  
    
    for idx,Id in enumerate(current_array):
        ne_data = data[~np.isnan(data[:,idx+1])][:,[0,idx+1]]
        ne_data[:,0] *= 10 # mm
        ne_data[:,1] = 10**ne_data[:,1]
        print(idx,Id)
    
        alldata = alldata.append({'cathode' : 'JPL-1.5cm', 
                                  'dischargeCurrent' : Id,
                                  'massFlowRate': 8*cc.sccm2eqA,
                                  'gas':'Xe',
                                  'orificeDiameter': 3.8,
                                  'orificeLength': 1.0,
                                  'insertDiameter': 7.,
                                  'insertLength': 25.4,
                                  'upstreamPressurePoint': 13.0,
                                  'electronDensity': np.copy(ne_data),
#                                  'electronTemperature': np.copy(Te_data),
#                                  'plasmaPotential': np.copy(phip_data),
                                  'reference': ref,
                                  'note': 'Fig. 9'
                                  } , ignore_index=True) 

    ### Density at 10 sccm
    current_array = np.arange(20,110,10)    
    
    data = np.genfromtxt(root + cat_root + 'ne_vs_x_Id-multiple_mdot-10sccm_1.5cm-cathode-raw.csv',
                         skip_header = True,
                         delimiter=',')  
    
    for idx,Id in enumerate(current_array):
        ne_data = data[~np.isnan(data[:,idx+1])][:,[0,idx+1]]
        ne_data[:,0] *= 10 # mm
        ne_data[:,1] = 10**ne_data[:,1]
        print(idx,Id)
    
        alldata = alldata.append({'cathode' : 'JPL-1.5cm', 
                                  'dischargeCurrent' : Id,
                                  'massFlowRate': 10*cc.sccm2eqA,
                                  'gas':'Xe',
                                  'orificeDiameter': 3.8,
                                  'orificeLength': 1.0,
                                  'insertDiameter': 7.,
                                  'insertLength': 25.4,
                                  'upstreamPressurePoint': 13.0,
                                  'electronDensity': np.copy(ne_data),
#                                  'electronTemperature': np.copy(Te_data),
#                                  'plasmaPotential': np.copy(phip_data),
                                  'reference': ref,
                                  'note': 'Fig. 9'
                                  } , ignore_index=True) 
    ### Density at 12 sccm
    current_array = np.arange(20,110,10)    
    current_array[4] = 90.
    current_array[5] = 60.
    current_array[6] = 70.
    current_array[7] = 80.
    
    data = np.genfromtxt(root + cat_root + 'ne_vs_x_Id-multiple_mdot-12sccm_1.5cm-cathode-raw.csv',
                         skip_header = True,
                         delimiter=',')  
    
    for idx,Id in enumerate(current_array):
        ne_data = data[~np.isnan(data[:,idx+1])][:,[0,idx+1]]
        ne_data[:,0] *= 10 # mm
        ne_data[:,1] = 10**ne_data[:,1]
        print(idx,Id)
    
        alldata = alldata.append({'cathode' : 'JPL-1.5cm', 
                                  'dischargeCurrent' : Id,
                                  'massFlowRate': 12*cc.sccm2eqA,
                                  'gas':'Xe',
                                  'orificeDiameter': 3.8,
                                  'orificeLength': 1.0,
                                  'insertDiameter': 7.,
                                  'insertLength': 25.4,
                                  'upstreamPressurePoint': 13.0,
                                  'electronDensity': np.copy(ne_data),
#                                  'electronTemperature': np.copy(Te_data),
#                                  'plasmaPotential': np.copy(phip_data),
                                  'reference': ref,
                                  'note': 'Fig. 9'
                                  } , ignore_index=True) 
        
    return alldata
    