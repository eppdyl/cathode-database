'''
Author: Pierre-Yves Taunay
Date: June 2020

'''
import pandas as pd
import numpy as np
import cathode.constants as cc


master_ne = []
master_Te = []
master_Te_err = []
master_phi = []
master_idxmin = []
master_idxmax = []


    
### Geometry
do = 1.21 # mm
dc = 3.81 # mm
Lo = 1.24 # mm

### Define cases
dischargeCurrent = np.array([3,5,9,10,12,15,20],dtype=np.float64)
massFlow_sccm = np.ones_like(dischargeCurrent) * 0.5 / cc.sccm2eqA

do = np.ones_like(dischargeCurrent) * do
Lo = np.ones_like(dischargeCurrent) * Lo
dc = np.ones_like(dischargeCurrent) * dc

### Extract density data
root = "../../original-material/salhi-thesis-1993/"
ne_all_data = np.genfromtxt(root+"raw/ne_vs_x_do-1.21mm_Xe_Q-0.5A.csv",
                        delimiter=",",
                        names = True,
                        skip_header=13)


### Extract Te
data = np.genfromtxt(root + "raw/Te_vs_x_do-1.21mm_Xe_Q-0.5A_Id-5-9-15A.csv",
                     delimiter=",",
                     skip_header = True)

###  Electron temperature from spectroscopy measurements   
    # Ignore 15 A bc. we already have positional data for that one
Id_sp = np.array([3.0,10.0,15.0,20.0])
Te_sp = np.array([1.0,0.98,1.09,1.07])
Te_sp_err = np.array([0.1,0.12,0.15,0.15])

idx_sp = 0
idx_Tex = 0
for idx,Id in enumerate(dischargeCurrent):
    phi_val = np.nan
    idxmin_val = np.nan
    
    ne_bool = (Id == 5.0 or Id == 9.0 or Id == 12.0 or Id == 15.0)
    Te_bool = (Id == 5.0 or Id == 9.0 or Id == 15.0)
    
    if Id == 3.0 or Id == 10.0 or Id == 20.0:
        ne_val = np.nan
        Te_val = Te_sp[idx_sp]
        Te_err_val = Te_sp_err[idx_sp]
        
        idxmin_val = np.nan
        idxmax_val = np.nan
        idx_sp += 1
        
    if ne_bool:
        csvcond = (ne_all_data['Id'] == Id)
        tmp_data = ne_all_data[csvcond][['x','log_ne']]
        
        ne_data = np.zeros((len(tmp_data['x']),2))
        ne_idx = 0
        for x,lne in zip(tmp_data['x'],tmp_data['log_ne']):
            ne_data[ne_idx,0] = x
            ne_data[ne_idx,1] = lne + 6.0
            ne_idx = ne_idx + 1
            
        ne_val = np.copy(ne_data)
        idxmax_val = -1
        
        if Id == 12.0:
            Te_val = np.nan
            Te_err_val = np.nan

    if Te_bool:
        Te_data = data[~np.isnan(data[:,idx_Tex+1])][:,[0,idx_Tex+1]]  
        idx_Tex += 1
        
        Te_val = np.copy(Te_data)
        Te_err_val = np.nan
        
    
    master_ne.append(ne_val)
    master_Te.append(Te_val)
    master_Te_err.append(Te_err_val)
    master_phi.append(phi_val)
    master_idxmin.append(idxmin_val)
    master_idxmax.append(idxmax_val)
             



### Assemble and dump
df = pd.DataFrame({'dischargeCurrent':dischargeCurrent,
                   'massFlowRate_sccm':massFlow_sccm,
                   'idxmin': master_idxmin,'idxmax':master_idxmax,
                   'electronDensity':master_ne,
                   'electronTemperature':master_Te,
                   'electronTemperature_err':master_Te_err,
                   'plasmaPotential':master_phi,
                   'orificeLength':Lo,
                   'orificeDiameter':do,
                   'insertDiameter':dc})

# Write the header 
header_str = """############################
### DOCUMENT
# [1] A. Salhi, "Theoretical and experimental studies of orificed, hollow cathode operation," The Ohio State University, 1993.
### SOFTWARE
# Plot digitized using Engauge Digitizer
### CAPTION
# Fig 5.7 for Te vs. position
# Figs 5.28 - 5.31 for singular Te through spectrometry
# Figs 5.34 - 5.36 for ne vs. position
### DATA
# Id (A), log10(electron density) vs. x (in 1/m3 and mm, resp.), electron temperature vs. x (in eV and mm), electron temperature error, idxmax, idxmin, dc (mm), mass flow (sccm of Xe), do (mm), Lo (mm), plasma potential vs. x (in V and mm)
### NOTES
############################
"""
f = open("positional_combined.csv","w")
f.write(header_str)
f.close()

# Dump data
df.to_csv("positional_combined.csv",index=False,mode="a")

