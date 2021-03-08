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

'''
Author: Pierre-Yves Taunay
Date: June 2020
'''
import pandas as pd
import numpy as np
try:
    import cathode.constants as cc
except ImportError:
    ### Ad-hoc solution if we don't have the cathode package
    ### Just define the constants...
    class cc:
        class M:
            Xe = 131.293

def find_indexing(Id,mdot):
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

### Geometry
dc = 7.0 # mm
Lo = 1.0 # mm

master_ne = []
master_Te_positional = []
master_Te_average = []
master_phi = []
master_idxmin = []
master_idxmax = []

########################################
## DOCUMENT 1
# E. Chu and D. M. Goebel, "High-current lanthanum hexaboride hollow cathode 
# for 10-to-50-kW hall thrusters," IEEE Transactions on Plasma Science, vol. 
# 40, no. 9, pp. 2133–2144, 2012.
# 
# Density, temperature, and plasma potential at 5.5 sccm, 25 A
########################################
root = "../../../original-material/chu-ieee-2012/csv/"

do = 3.8 # mm
current_array = np.arange(20,110,10) 
massFlow_array = np.array([8.,10.,12])

# Correct for scrambled currents 
current_array_8sccm = np.copy(current_array) 
current_array_8sccm[-1] = 90.
current_array_8sccm[-2] = 100. 

current_array_12sccm = np.copy(current_array) 
current_array_12sccm[4] = 90.
current_array_12sccm[5] = 60.
current_array_12sccm[6] = 70.
current_array_12sccm[7] = 80.

### Density data at 8, 10, 12 sccm
for idx, mdot in enumerate(massFlow_array):
    if idx == 0:
        dischargeCurrent = np.copy(current_array_8sccm) 
        massFlow_sccm = np.ones_like(current_array_8sccm) * 8.0
    elif idx==2:
        dischargeCurrent = np.append(dischargeCurrent,current_array_12sccm)
        massFlow_sccm = np.append(massFlow_sccm, np.ones_like(current_array) * massFlow_array[idx]) 
    else:
        dischargeCurrent = np.append(dischargeCurrent,current_array)
        massFlow_sccm = np.append(massFlow_sccm, np.ones_like(current_array) * massFlow_array[idx]) 

do = np.ones_like(dischargeCurrent) * do


### Temperature and potential data
Te_data_50A = np.genfromtxt(root + 'Te-phip_vs_x_mdot-multiple_Id-50A.csv',
                         skip_header = True,
                         delimiter=',')  

Te_data_100A = np.genfromtxt(root + 'Te-phip_vs_x_mdot-multiple_Id-100A.csv',
                         skip_header = True,
                         delimiter=',')  


### Te 1 cm upstream
Te_data_1cm = np.genfromtxt(root + 'Te_vs_Id_mdot-multiple_Id-multiple.csv',
                     skip_header = True,
                     delimiter=',')
# Make sure we get the round discharge currents for boolean conditions
Te_data_1cm[:,0] = np.round(Te_data_1cm[:,0]) 
    
### All data
# 8 sccm
mdot = 8.0

data = np.genfromtxt(root + 'ne_vs_x_Id-multiple_mdot-8sccm.csv',
        skip_header = True, delimiter=',')  

idxTe = 0

for idx,Id in enumerate(current_array_8sccm):
    ne_data = data[~np.isnan(data[:,idx+1])][:,[0,idx+1]]
    ne_data[:,0] *= 10 # Convert to mm
    npoints = find_indexing(Id,mdot)

    
    master_ne.append(np.copy(ne_data))
    master_idxmin.append(-npoints)
    master_idxmax.append(np.nan)
    
    if Id == 50.:
        Te_data = Te_data_50A[~np.isnan(Te_data_50A[:,idxTe+4])][:,[0,idxTe+4]]
        phip_data = Te_data_50A[~np.isnan(Te_data_50A[:,idxTe+1])][:,[0,idxTe+1]]  
        master_Te_positional.append(np.copy(Te_data))
        master_Te_average.append(np.nan)
        master_phi.append(np.copy(phip_data))
        
    elif Id == 100.:
        Te_data = Te_data_100A[~np.isnan(Te_data_100A[:,idxTe+4])][:,[0,idxTe+4]]
        phip_data = Te_data_100A[~np.isnan(Te_data_100A[:,idxTe+1])][:,[0,idxTe+1]]        
        master_Te_positional.append(np.copy(Te_data))
        master_Te_average.append(np.nan)
        master_phi.append(np.copy(phip_data))
        
    else:
        # Grab data from Te 1cm upstream
        bcond = ~np.isnan(Te_data_1cm[:,idxTe+1])
        bcond &= (Te_data_1cm[:,0] == Id)
        Te_data = Te_data_1cm[bcond][:,idxTe+1]
        Te_data = Te_data[0]
        
        master_Te_positional.append(np.nan)
        master_Te_average.append(Te_data)
        master_phi.append(np.nan)

# 10 sccm
mdot = 10.0
data = np.genfromtxt(root + 'ne_vs_x_Id-multiple_mdot-10sccm.csv',
        skip_header = True, delimiter=',')  

idxTe = idxTe + 1

for idx,Id in enumerate(current_array):
    ne_data = data[~np.isnan(data[:,idx+1])][:,[0,idx+1]]
    ne_data[:,0] *= 10 # Convert to mm
    npoints = find_indexing(Id,mdot)
    
    master_ne.append(np.copy(ne_data))
    master_idxmin.append(-npoints)
    master_idxmax.append(np.nan)

    if Id == 50.:
        Te_data = Te_data_50A[~np.isnan(Te_data_50A[:,idxTe+4])][:,[0,idxTe+4]]
        phip_data = Te_data_50A[~np.isnan(Te_data_50A[:,idxTe+1])][:,[0,idxTe+1]]  
        master_phi.append(np.copy(phip_data))
        master_Te_positional.append(np.copy(Te_data))
        master_Te_average.append(np.nan)
        
    elif Id == 100.:
        Te_data = Te_data_100A[~np.isnan(Te_data_100A[:,idxTe+4])][:,[0,idxTe+4]]
        phip_data = Te_data_100A[~np.isnan(Te_data_100A[:,idxTe+1])][:,[0,idxTe+1]]        
        master_phi.append(np.copy(phip_data))
        master_Te_positional.append(np.copy(Te_data))
        master_Te_average.append(np.nan)
        
    else:
        # Grab data from Te 1cm upstream
        bcond = ~np.isnan(Te_data_1cm[:,idxTe+1])
        bcond &= (Te_data_1cm[:,0] == Id)
        Te_data = Te_data_1cm[bcond][:,idxTe+1]
        Te_data = Te_data[0]
        
        master_Te_positional.append(np.nan)
        master_Te_average.append(Te_data)
        master_phi.append(np.nan)
    
# 12 sccm
mdot = 12.0
data = np.genfromtxt(root + 'ne_vs_x_Id-multiple_mdot-12sccm.csv',
        skip_header = True, delimiter=',')  
idxTe = idxTe + 1

for idx,Id in enumerate(current_array_12sccm):
    ne_data = data[~np.isnan(data[:,idx+1])][:,[0,idx+1]]
    ne_data[:,0] *= 10 # Convert to mm
    npoints = find_indexing(Id,mdot)
    
    master_ne.append(np.copy(ne_data))
    master_idxmin.append(-npoints)
    master_idxmax.append(np.nan)   

    if Id == 50.:
        Te_data = Te_data_50A[~np.isnan(Te_data_50A[:,idxTe+4])][:,[0,idxTe+4]]
        phip_data = Te_data_50A[~np.isnan(Te_data_50A[:,idxTe+1])][:,[0,idxTe+1]]  
        master_phi.append(np.copy(phip_data))
        master_Te_positional.append(np.copy(Te_data))
        master_Te_average.append(np.nan)
        
    elif Id == 100.:
        Te_data = Te_data_100A[~np.isnan(Te_data_100A[:,idxTe+4])][:,[0,idxTe+4]]
        phip_data = Te_data_100A[~np.isnan(Te_data_100A[:,idxTe+1])][:,[0,idxTe+1]]        
        master_phi.append(np.copy(phip_data))
        master_Te_positional.append(np.copy(Te_data))
        master_Te_average.append(np.nan)
        
    else:
        # Grab data from Te 1cm upstream
        bcond = ~np.isnan(Te_data_1cm[:,idxTe+1])
        bcond &= (Te_data_1cm[:,0] == Id)
        Te_data = Te_data_1cm[bcond][:,idxTe+1]
        Te_data = Te_data[0]
        
        master_Te_positional.append(np.nan)
        master_Te_average.append(Te_data)
        master_phi.append(np.nan)

########################################
## DOCUMENT 2
# 3mm, 5mm
# [2] G. Becatti, D. M. Goebel, J. E. Polk, and P. Guerrero, "Life Evaluation 
# of a Lanthanum Hexaboride Hollow Cathode for High-Power Hall Thruster," 
# Journal of Propulsion and Power, vol. 34, no. 4, pp. 893–900, 2017.
# 
# Density:
# 10.5,13.1,14.9,19.8 sccm, 25 A
# 13 sccm, 8.9,15.6,25.1,31.3 A
########################################
root = "../../../original-material/becatti-jpp-2017/csv/"

### Append cases
massFlow_array = np.array([10.5,13.1,14.9,19.8])
current_array = np.array([8.9,15.6,25.1,31.3]) 
master_idxmin.extend([-20,-20,-20,-20])
master_idxmax.extend([-2,-2,-2,-7])

### Density data at constant current
# 3 mm
data = np.genfromtxt(root + 'ne_vs_x_mdot-multiple_Id-25A_do-3mm.csv',
                     skip_header = True,
                     delimiter=',')  

do_val = 3 # mm
for idx,mdot in enumerate(massFlow_array):
    ne_data = data[~np.isnan(data[:,idx+1])][:,[0,idx+1]]

    dischargeCurrent = np.append(dischargeCurrent,25.0)
    massFlow_sccm = np.append(massFlow_sccm,mdot)
    do = np.append(do,do_val)
    
    master_ne.append(np.copy(ne_data))
    
    master_Te_positional.append(np.nan)
    master_Te_average.append(np.nan)
    master_phi.append(np.nan)

# 5 mm
data = np.genfromtxt(root + 'ne_vs_x_mdot-multiple_Id-25A_do-5mm.csv',
                     skip_header = True,
                     delimiter=',')  

master_idxmin.extend([-22,-22,-22,-22])
master_idxmax.extend([-3,-3,-3,-5])
do_val = 5 # mm
for idx,mdot in enumerate(massFlow_array):
    ne_data = data[~np.isnan(data[:,idx+1])][:,[0,idx+1]]

    dischargeCurrent = np.append(dischargeCurrent,25.0)
    massFlow_sccm = np.append(massFlow_sccm,mdot)
    do = np.append(do,do_val)

    master_ne.append(np.copy(ne_data))
    
    master_Te_positional.append(np.nan)
    master_Te_average.append(np.nan)
    master_phi.append(np.nan)

### Density data at constant mass flow
# 3 mm
data = np.genfromtxt(root + 'ne_vs_x_mdot-13sccm_Id-multiple_do-3mm.csv',
                     skip_header = True,
                     delimiter=',')  
master_idxmin.extend([-16,-11,-16,-16])
master_idxmax.extend([-3,-1,-3,-3])

do_val = 3 # mm
for idx,Id in enumerate(current_array):
    ne_data = data[~np.isnan(data[:,idx+1])][:,[0,idx+1]]

    dischargeCurrent = np.append(dischargeCurrent,Id)
    massFlow_sccm = np.append(massFlow_sccm,13.1)
    do = np.append(do,do_val)

    master_ne.append(np.copy(ne_data))
    
    master_Te_positional.append(np.nan)
    master_Te_average.append(np.nan)
    master_phi.append(np.nan)

# 5 mm
data = np.genfromtxt(root + 'ne_vs_x_mdot-13sccm_Id-multiple_do-5mm.csv',
                     skip_header = True,
                     delimiter=',')  

master_idxmin.extend([-16,-11,-16,-16])
master_idxmax.extend([-2,-3,-2,-2])

do_val = 5 # mm
for idx,Id in enumerate(current_array):
    ne_data = data[~np.isnan(data[:,idx+1])][:,[0,idx+1]]

    dischargeCurrent = np.append(dischargeCurrent,Id)
    massFlow_sccm = np.append(massFlow_sccm,13.1)
    do = np.append(do,do_val)
 
    master_ne.append(np.copy(ne_data))
    
    master_Te_positional.append(np.nan)
    master_Te_average.append(np.nan)
    master_phi.append(np.nan)
    

#### Assemble and dump
# Lo and dc do not change
Lo = np.ones_like(dischargeCurrent) * Lo
dc = np.ones_like(dischargeCurrent) * dc

df = pd.DataFrame({'dischargeCurrent':dischargeCurrent,
                   'massFlowRate_sccm':massFlow_sccm,
                   'idxmin':master_idxmin,'idxmax':master_idxmax,
                   'electronDensity':master_ne,
                   'electronTemperature':master_Te_positional,
                   'electronTemperatureAverage':master_Te_average,
                   'plasmaPotential':master_phi,
                   'gasMass': cc.M.Xe * np.ones_like(Lo),
                   'orificeLength':Lo,
                   'orificeDiameter':do,
                   'insertDiameter':dc})

# Write the header 
header_str = """############################
### DOCUMENT
# [1] E. Chu and D. M. Goebel, "High-current lanthanum hexaboride hollow cathode for 10-to-50-kW hall thrusters," IEEE Transactions on Plasma Science, vol. 40, no. 9, pp. 2133–2144, 2012.
# [2] D. M. Goebel and E. Chu, "High Current Lanthanum Hexaboride Hollow Cathodes for High Power Hall Thrusters," 32nd IEPC, 2011.
# [3] G. Becatti, D. M. Goebel, J. E. Polk, and P. Guerrero, “Life Evaluation of a Lanthanum Hexaboride Hollow Cathode for High-Power Hall Thruster,” Journal of Propulsion and Power, vol. 34, no. 4, pp. 893–900, 2017.
### SOFTWARE
# Plot digitized using Engauge Digitizer
### CAPTION
# [1] Fig. 7. Plasma potential and electron temperature profiles in the 1.5-cm cathode at three xenon flow rates and (top) 50 and (bottom) 100 A.
# [1] Fig. 8. Electron temperature versus discharge current for three xenon flow rates.
# [1] Fig. 9. Plasma density profiles inside the 1.5-cm cathode for two xenon flow rates.
# [2] Figure 10. Density profiles inside the insert at discharge currents up to 100 A for the 1.5-cm cathode at three xenon flow rates.
# [3] Fig. 6 Plasma density profiles at 25 A for a) 5 mm orifice, and b) 3 mm orifice.
# [3] Fig. 7 Plasma density profiles at 13 sccm for a) 5 mm orifice, and b) 3 mm orifice.
### DATA
# Id (A), log10(electron density) vs. x (in 1/m3 and mm, resp.), electron temperature vs. x (in eV and mm), electron temperature average (eV), idxmax, idxmin, dc (mm), mass flow (sccm of Xe), do (mm), Lo (mm), plasma potential vs. x (in V and mm)
### NOTES
# We merged the 10 sccm plot from [2] into the folder of [1].
############################
"""
f = open("positional_combined.csv","w")
f.write(header_str)
f.close()

# Dump data
df.to_csv("positional_combined.csv",index=False,mode="a")

