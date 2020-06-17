'''
Author: Pierre-Yves Taunay
Date: June 2020

'''
import pandas as pd
import numpy as np
import cathode.constants as cc

def Pcorr(mdot,do,Id,species):
    if species == 'Ar':
        P = mdot/do**2 * (0.0056 + 0.0012*Id)
    elif species == 'Xe':
        P = mdot/do**2 * (0.0090 + 0.0040*Id)
    elif species == 'Hg':
        P = mdot/do**2 * (0.0137 + 0.00782*Id)
    return P

### Geometry
do = 0.76
Lo = 1.8

### Start with the pressure data
### Note that we also have plasma potential and (single-point) density 
### for argon and xenon (but not for mercury)
## Mercury data
root = '../../original-material/siegfried-iepc-1981/raw/'
hg_pdata = np.genfromtxt(root + 'P_vs_Id_mdot.csv', delimiter=',', names=True,
                      skip_header=9)

dischargeCurrent = hg_pdata['Id']
massFlow_eqA = hg_pdata['mdot'] * 1e-3
pressureArray = np.copy(hg_pdata['P'])
massArray = cc.M.Hg * np.ones_like(dischargeCurrent)
twallArray = np.copy(hg_pdata['Tw'])
dc = np.copy(hg_pdata['dc'])
neArray = np.nan * np.ones_like(dischargeCurrent)
phipArray = np.nan * np.ones_like(dischargeCurrent)

## Argon data
root = '../../original-material/wilbur-CR168340-1984/csv/'
dcval = 3.8 # mm

# Pressure known, back out mass flow rate
ar_pdata = np.genfromtxt(root + 'argon_do-0.76mm_Id-2.3A.csv', delimiter=',', 
                         names=True,
                         skip_header=15)
Id = 2.3

mdot = ar_pdata['P'] * do**2 / (0.0056 + 0.0012 * Id) * 1e-3

dischargeCurrent = np.append(dischargeCurrent,np.ones_like(ar_pdata['P']) * Id)
massFlow_eqA = np.append(massFlow_eqA,mdot)
pressureArray = np.append(pressureArray,ar_pdata['P'])
massArray = np.append(massArray,cc.M.Ar *np.ones_like(ar_pdata['P']))
twallArray = np.append(twallArray,ar_pdata['Tc'])
dc = np.append(dc,dcval*np.ones_like(ar_pdata['P']))

neArray = np.append(neArray,ar_pdata['ne_ave'])
phipArray = np.append(phipArray,ar_pdata['Vp'])

# Mass flow rate known, back out pressure
ar_pdata = np.genfromtxt(root + 'argon_do-0.76mm_mdot-287mA.csv', delimiter=',', names=True,
                      skip_header=15)

mdot = 287 # mA
mdot_A = mdot * 1e-3 # eqA
P = Pcorr(mdot,do,ar_pdata['Id'],'Ar')

dischargeCurrent = np.append(dischargeCurrent,ar_pdata['Id'])
massFlow_eqA = np.append(massFlow_eqA,mdot_A*np.ones_like(ar_pdata['Id']))
pressureArray = np.append(pressureArray,P)
massArray = np.append(massArray,cc.M.Ar *np.ones_like(ar_pdata['Id']))
twallArray = np.append(twallArray,ar_pdata['Tc'])
dc = np.append(dc,dcval*np.ones_like(ar_pdata['Id']))

neArray = np.append(neArray,ar_pdata['ne_ave'])
phipArray = np.append(phipArray,ar_pdata['Vp'])

## Xenon data
root = '../../original-material/wilbur-CR168340-1984/csv/'

# Pressure known, back out mass flow rate
xe_pdata = np.genfromtxt(root + 'xenon_do-0.76mm_Id-2.3A.csv', delimiter=',', names=True,
                      skip_header=15)

mdot = xe_pdata['P'] * do**2 / (0.0090 + 0.0040*Id) * 1e-3

dischargeCurrent = np.append(dischargeCurrent,np.ones_like(xe_pdata['P']) * Id)
massFlow_eqA = np.append(massFlow_eqA,mdot)
pressureArray = np.append(pressureArray,xe_pdata['P'])

massArray = np.append(massArray,cc.M.Xe *np.ones_like(xe_pdata['P']))
twallArray = np.append(twallArray,xe_pdata['Tc'])
dc = np.append(dc,dcval*np.ones_like(xe_pdata['P']))

neArray = np.append(neArray,xe_pdata['ne_ave'])
phipArray = np.append(phipArray,xe_pdata['Vp'])

# Mass flow rate known, back out pressure
xe_pdata = np.genfromtxt(root + 'xenon_do-0.76mm_mdot-92mA.csv', delimiter=',', names=True,
                      skip_header=15)

mdot = 92 # mA
mdot_A = mdot * 1e-3 # eqA
P = Pcorr(mdot,do,xe_pdata['Id'],'Ar')

dischargeCurrent = np.append(dischargeCurrent,xe_pdata['Id'])
massFlow_eqA = np.append(massFlow_eqA,mdot_A*np.ones_like(xe_pdata['Id']))
pressureArray = np.append(pressureArray,P)
massArray = np.append(massArray,cc.M.Xe *np.ones_like(xe_pdata['Id']))
twallArray = np.append(twallArray,xe_pdata['Tc'])
dc = np.append(dc,dcval*np.ones_like(xe_pdata['Id']))

neArray = np.append(neArray,xe_pdata['ne_ave'])
phipArray = np.append(phipArray,xe_pdata['Vp'])

do = do * np.ones_like(dischargeCurrent)
Lo = Lo * np.ones_like(dischargeCurrent)
neArray *= 1e20
neArray = np.log10(neArray)

#Id,mdot,P,mass,do,Tw,Lo,dc
### Assemble and dump
df = pd.DataFrame({'dischargeCurrent':dischargeCurrent,
                   'massFlowRate':massFlow_eqA,
                   'totalPressure':pressureArray,
                   'gasMass': massArray,
                   'insertTemperatureAverage':twallArray,
                   'orificeLength':Lo,
                   'orificeDiameter':do,
                   'insertDiameter':dc,
                   'electronDensity':neArray,
                   'plasmaPotential':phipArray})

    
# Write the header 
header_str = """############################
### DOCUMENT
# [1] P. J. Wilbur, "Ion and advanced electric thruster research," CR-165253, 1980.
# [2] Siegfried, D. E., Wilbur, P. J. "Phenomenological model describing orificed, hollow cathode operation," 15th IEPC, 1981 
# [3] Siegfried, D. E. "A Phenomenological Model for Orificed Hollow Cathodes", Ph.D. thesis, Colorado State University, 1982 
# [4] P. J. Wilbur, "Advanced Ion Thruster Research," CR-168340, 1984.
### DATA
# Id (A), log10(Electron Density) (1/m3), Propellant mass (amu), Insert diameter (mm), Insert temperature (degC), Mass flow rate (eqA), Orifice diameter (mm), Orifice length (mm), Plasma potential (V), Total pressure (Torr)
### NOTES
# Mercury cathode with a 0.76mm diameter orifice
# Table p. 14 of Ref. [1], p.4 of Ref. [2]. 
# Temperature data for the cases at 3.3 A are from Ref. [2] 
# Orifice length is from Ref. [3], p.130
# The insert temperature for the experiments at fixed Id = 3.31 A but varying mass flow rate are taken to be the same as the one reported for 3.31 A
# [4] Plots are p.101-104 for Argon and p.105-108 for Xenon
############################
"""
f = open("P_vs_Id_mdot.csv","w")
f.write(header_str)
f.close()

# Dump data
df.to_csv("P_vs_Id_mdot.csv",index=False,mode="a")


### Positional data
master_ne = []
master_Te = []
master_Te_err = []
master_phi = []
master_idxmin = []
master_idxmax = []
master_mass = []
    
### Geometry
do_val = 0.76 # mm
Lo_val = 1.8 # mm 
dc_val = 3.8 # mm

### Id,do,dc,P,phi_wf,x,ne
data = np.genfromtxt(root + 'xenon_ne_vs_x_do-0.76mm_Id-2.3A.csv',
                     skip_header = 13,
                     names = True,
                     delimiter=',') 

### Got two work functions there
P = 4
Id = 2.3
nevec = np.zeros((len(data['x']),2))
nevec[:,0] = np.copy(data['x'])
nevec[:,1] = np.copy(data['ne']) * 1e19 # was in 1e-13/cm3
nevec[:,1] = np.log10(nevec[:,1]) # Apply log10

# Get the mass flow rate from P and Id
mdot = P * do_val**2 / (0.0090 + 0.0040 * Id) * 1e-3
    
ne_data = nevec[data['phi_wf']==1.9]
master_ne.append(np.copy(ne_data))
master_mass.append(cc.M.Xe)

ne_data = nevec[data['phi_wf']==2.5]
master_ne.append(np.copy(ne_data))
master_mass.append(cc.M.Xe)

master_idxmin = [-20,-30]
master_idxmax = [np.nan,np.nan]
master_wf = [1.9,2.5]  
totalPressure = np.array([P,P])
dischargeCurrent = np.array([Id,Id])
massFlowRate_eqA = np.array([mdot,mdot])

### Assemble and dump
df = pd.DataFrame({'totalPressure':totalPressure,
                    'dischargeCurrent':dischargeCurrent,
                   'massFlowRate':massFlowRate_eqA,
                   'idxmin': master_idxmin,'idxmax':master_idxmax,
                   'electronDensity':master_ne,
                   'gasMass':master_mass,
                   'orificeLength':[Lo_val,Lo_val],
                   'orificeDiameter':[do_val,do_val],
                   'insertDiameter':[dc_val,dc_val],
                   'workFunction': master_wf})

### Electron temperature
data = np.genfromtxt(root + 'Te_vs_P_xenon_do-0.76mm_Id-2.3A.csv',
                     names = True,
                     delimiter=',') 

    
Pvec = data['totalPressure'][~np.isnan(data['19eV'])]
Te_data = data['19eV'][~np.isnan(data['19eV'])]
mdotvec = Pvec * do_val**2 / (0.0090 + 0.0040 * Id) * 1e-3


for idx,P in enumerate(Pvec):
    mdot = mdotvec[idx]
    P = Pvec[idx]
    Te_xp = Te_data[idx]
    df = df.append({'totalPressure': P,
                              'dischargeCurrent' : Id,
                              'massFlowRate': mdot,                          
                              'orificeDiameter': do_val,
                              'orificeLength': Lo_val,
                              'insertDiameter': dc_val,
                              'electronTemperatureAverage':Te_xp,
                              'gasMass':cc.M.Xe
                              } , ignore_index=True) 

Pvec = data['totalPressure'][~np.isnan(data['25eV'])]
Te_data = data['25eV'][~np.isnan(data['25eV'])]
mdotvec = Pvec * do_val**2 / (0.0090 + 0.0040 * Id) * 1e-3

for idx,P in enumerate(Pvec):
    mdot = mdotvec[idx]
    P = Pvec[idx]
    Te_xp = Te_data[idx]
    df = df.append({'totalPressure': P,
                              'dischargeCurrent' : Id,
                              'massFlowRate': mdot,                          
                              'orificeDiameter': do_val,
                              'orificeLength': Lo_val,
                              'insertDiameter': dc_val,
                              'electronTemperatureAverage':Te_xp,
                              'gasMass':cc.M.Xe
                              } , ignore_index=True) 

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
# Id (A), log10(electron density) vs. x (in 1/m3 and mm, resp.), idxmax, idxmin, dc (mm), mass flow (eqA), do (mm), Lo (mm), total pressure (Torr), electron temperature (eV)
### NOTES
############################
"""
f = open("positional_combined.csv","w")
f.write(header_str)
f.close()

# Dump data
df.to_csv("positional_combined.csv",index=False,mode="a")

