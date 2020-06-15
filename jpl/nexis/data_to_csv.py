'''
Author: Pierre-Yves Taunay
Date: June 2020
'''
import pandas as pd
import numpy as np

### Geometry
dc = 12.7 # mm
Lo = 0.74 # mm

master_ne = []
master_Te = []
master_phi = []

########################################
## DOCUMENT 1
# I. G. Mikellides, I. Katz, D. M. Goebel, and J. E. Polk, "Hollow cathode 
# theory and experiment. II. A two-dimensional theoretical model of the emitter
# region," Journal of Applied Physics, vol. 98, no. 2005
# 
# Density, temperature, and plasma potential at 5.5 sccm, 25 A
########################################
root = "../../original-material/mikellides-jap-2005/"

do = 2.75 # mm
dischargeCurrent = np.array([25.])
massFlow_sccm = np.array([5.5])

do = np.ones_like(dischargeCurrent) * do
Lo = np.ones_like(dischargeCurrent) * Lo
dc = np.ones_like(dischargeCurrent) * dc

idxmin = np.array([-40],dtype=np.int64)
idxmax = np.array([-10],dtype=np.int64)

### Density data
fname = "ne_vs_x_mdot-5.5sccm_Id-25A.csv"
ne_data = np.genfromtxt(root+"raw/ne_vs_x_mdot-5.5sccm_Id-25A.csv",delimiter=",")

# Convert to 1/m3
ne_data[:,1] *= 1e20
ne_data[:,1] = np.log10(ne_data[:,1])

# Append data; make a deep copy to be sure we don't overwrite later
master_ne.append(np.copy(ne_data))

### Extract Te and potential
data = np.genfromtxt(root + "raw/Te-phip_vs_x_mdot-5.5sccm_Id-25A.csv",delimiter=",",
                        skip_header=True)

phip_data = data[~np.isnan(data[:,1])][:,0:2]
Te_data = data[~np.isnan(data[:,2])][:,0::2]

# Append data
master_Te.append(np.copy(Te_data))
master_phi.append(np.copy(phip_data))

########################################
## DOCUMENT 2
# D. Goebel, K. K. Jameson, R. M. Watkins, and I. Katz, "Hollow Cathode and 
# Keeper-Region Plasma Measurements Using Ultra-Fast Miniature Scanning Probes,"
# 40th JPC, 2004.
# 
# Density, temperature, and plasma potential at :
# [5.5 sccm, 10 A]
# [10 sccm, 25 A]
# 
########################################
root = "../../original-material/goebel-jpc-2004/"

### Append cases
dischargeCurrent = np.append(dischargeCurrent,[10.0,25.0])
massFlow_sccm = np.append(massFlow_sccm,[5.5,10.0])
do = np.append(do,[2.75,2.75])
Lo = np.append(Lo,[0.74,0.74])
dc = np.append(dc,[12.7,12.7])

### Density data
# None for 5.5 sccm, 10 A
master_ne.append(np.nan)
idxmin = np.append(idxmin,np.nan)
idxmax = np.append(idxmax,np.nan)

# 10 sccm, 25 A
ne_data = np.genfromtxt(root + 'raw/ne_vs_x_mdot-5-10sccm_Id-25A.csv', 
        delimiter=',')
ne_data[:,1] *= 1e20
ne_data[:,1] = np.log10(ne_data[:,1])

master_ne.append(ne_data)
idxmin = np.append(idxmin,-40)
idxmax = np.append(idxmax,-10)

### Te, potential
data = np.genfromtxt(root + 'raw/Te-phip_vs_x_mdot-5.5-10sccm_Id-10-25A.csv',
        skip_header = True, delimiter=',')
# 5.5 sccm, 10 A
Te_data = data[~np.isnan(data[:,1])][:,[0,1]]
phip_data = data[~np.isnan(data[:,2])][:,[0,2]]

master_Te.append(np.copy(Te_data))
master_phi.append(np.copy(phip_data))

# 10 sccm, 25 A (it's in the same file)
Te_data = data[~np.isnan(data[:,3])][:,[0,3]]
phip_data = data[~np.isnan(data[:,4])][:,[0,4]]

master_Te.append(np.copy(Te_data))
master_phi.append(np.copy(phip_data))

########################################
## DOCUMENT 3
# D. M. Goebel, K. K. Jameson, R. M. Watkins, I. Katz, and I. G. Mikellides, 
# "Hollow cathode theory and experiment. I. Plasma characterization using fast 
# miniature scanning probes," Journal of Applied Physics, vol. 98, no. 11, 
# pp. 1-9, 2005.
# 
# Density with a smaller orifice size (2 mm), at:
# [5.5 sccm, 10 A]
# [10 sccm, 25 A]
########################################
### TODO


### Assemble and dump
df = pd.DataFrame({'dischargeCurrent':dischargeCurrent,
                   'massFlowRate_sccm':massFlow_sccm,
                   'idxmin':idxmin,'idxmax':idxmax,
                   'electronDensity':master_ne,
                   'electronTemperature':master_Te,
                   'plasmaPotential':master_phi,
                   'orificeLength':Lo,
                   'orificeDiameter':do,
                   'insertDiameter':dc})

# Write the header 
header_str = """############################
### DOCUMENT
# [1] I. G. Mikellides, I. Katz, D. M. Goebel, and J. E. Polk, "Hollow cathode theory and experiment. II. A two-dimensional theoretical model of the emitter region," Journal of Applied Physics, vol. 98, no. 2005
# [2] D. Goebel, K. K. Jameson, R. M. Watkins, and I. Katz, "Hollow Cathode and Keeper-Region Plasma Measurements Using Ultra-Fast Miniature Scanning Probes," 40th JPC, 2004.
### SOFTWARE
# Plot digitized using Engauge Digitizer
### CAPTION
# [1] FIG. 5. Comparison between model results and measurements taken at a discharge current of 25 A. The entrance to the orifice channel is at an axial location of 0 cm. Experimental error in the plasma particle density +/- 40%.
# [1] FIG. 7. Comparison between model results and measurements for the plasma potential and electron temperature at discharge current of 25 A. Experiment errors: ±1 V for the plasma potential, ±0.5 eV for the electron temperature.
# [2] Figure 9. Plasma density scans from the cathode probe a 25 A for two flow rates. 
# [2] Figure 12. Plasma potential and electron temperature in the hollow cathode showing variation with flow and discharge current. 
### DATA
# Id (A), log10(electron density) vs. x (in 1/m3 and mm, resp.), electron temperature vs. x (in eV and mm), idxmax, idxmin, dc (mm), mass flow (sccm of Xe), do (mm), Lo (mm), plasma potential vs. x (in V and mm)
### NOTES
############################
"""
f = open("positional_combined.csv","w")
f.write(header_str)
f.close()

# Dump data
df.to_csv("positional_combined.csv",index=False,mode="a")

