import numpy as np
import cathode.constants as cc

def populate_th8(alldata,root,cat_root):
    ### TH8
    # mdot = 2.47 sccm, Id = 8.24 A
    data = np.genfromtxt(root + cat_root + 'ne_vs_position_TH8-TH15.csv',
                         skip_header = True,
                         delimiter=',')    
    
    ne_data = data[~np.isnan(data[:,1])][:,[0,1]]
    ne_data[:,1] = 10**ne_data[:,1]
    
    data = np.genfromtxt(root + cat_root + 'phip-Te_vs_position_TH8-TH15.csv',
                         skip_header = True,
                         delimiter=',')     


    Te_data = data[~np.isnan(data[:,2])][:,[0,2]]
    phip_data = data[~np.isnan(data[:,1])][:,[0,1]]    
    
    bcond = (alldata.cathode=='NSTAR') & (alldata.dischargeCurrent == 8.24) & (alldata.massFlowRate == 2.47*cc.sccm2eqA)
    alldata.loc[bcond,'electronDensity'] = alldata.loc[bcond,'electronDensity'].apply(lambda x: np.copy(ne_data))
    alldata.loc[bcond,'electronTemperature'] = alldata.loc[bcond,'electronTemperature'].apply(lambda x: np.copy(Te_data))
    alldata.loc[bcond,'plasmaPotential'] = alldata.loc[bcond,'plasmaPotential'].apply(lambda x: np.copy(phip_data))
    
    return alldata

def populate_th15(alldata,root,cat_root):
    ### TH15
    # mdot = 3.7 sccm, Id = 13.3 A
    # mdot = 2.47 sccm, Id = 8.24 A
    data = np.genfromtxt(root + cat_root + 'ne_vs_position_TH8-TH15.csv',
                         skip_header = True,
                         delimiter=',')    
    
    ne_data = data[~np.isnan(data[:,2])][:,[0,2]]
    ne_data[:,1] = 10**ne_data[:,1]
    
    data = np.genfromtxt(root + cat_root + 'phip-Te_vs_position_TH8-TH15.csv',
                         skip_header = True,
                         delimiter=',')     


    Te_data = data[~np.isnan(data[:,4])][:,[0,4]]
    phip_data = data[~np.isnan(data[:,3])][:,[0,3]] 
    
    bcond = (alldata.cathode=='NSTAR') & (alldata.dischargeCurrent == 13.3) & (alldata.massFlowRate == 3.7*cc.sccm2eqA)
    alldata.loc[bcond,'electronDensity'] = alldata.loc[bcond,'electronDensity'].apply(lambda x: np.copy(ne_data))
    alldata.loc[bcond,'electronTemperature'] = alldata.loc[bcond,'electronTemperature'].apply(lambda x: np.copy(Te_data))
    alldata.loc[bcond,'plasmaPotential'] = alldata.loc[bcond,'plasmaPotential'].apply(lambda x: np.copy(phip_data))
    
    return alldata