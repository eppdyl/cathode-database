'''
Author: Pierre-Yves Taunay
Date: June 2020

This script takes in the raw positional data from the JPC 2005 paper, moves it 
into a Pandas dataframe, then re-writes it as a monolithic csv file.
'''
import pandas as pd
import numpy as np

# Geometry
do = 1.02 # mm
dc = 3.8 # mm
Lo = 0.74 # mm

# Define cases
dischargeCurrent = np.array([8.29,13.2])
massFlow_sccm = np.array([2.47,3.7])

do = np.ones_like(dischargeCurrent) * do
Lo = np.ones_like(dischargeCurrent) * Lo
dc = np.ones_like(dischargeCurrent) * dc

idxmin = np.array([-50,-50],dtype=np.int64)
idxmax = np.array([np.nan,np.nan])

# Extract density data
root = "../../../original-material/jameson-jpc-2005/"
ne_data = np.genfromtxt(root+"raw/ne_vs_position_TH8-TH15.csv",delimiter=",",
                        skip_header=1)

ne_th8 = ne_data[~np.isnan(ne_data[:,1])][:,[0,1]]
ne_th15 = ne_data[~np.isnan(ne_data[:,2])][:,[0,2]]

# Extract Te and potential
data = np.genfromtxt(root + "raw/phip-Te_vs_position_TH8-TH15.csv",delimiter=",",
                        skip_header=1)

Te_th8 = data[~np.isnan(data[:,2])][:,[0,2]]
Te_th15 = data[~np.isnan(data[:,4])][:,[0,4]]

phip_th8 = data[~np.isnan(data[:,1])][:,[0,1]]    
phip_th15 = data[~np.isnan(data[:,3])][:,[0,3]]   

### Assemble and dump
df = pd.DataFrame({'dischargeCurrent':dischargeCurrent,
                   'massFlowRate_sccm':massFlow_sccm,
                   'idxmin':idxmin,'idxmax':idxmax,
                   'electronDensity':[ne_th8,ne_th15],
                   'electronTemperature':[Te_th8,Te_th15],
                   'plasmaPotential':[phip_th8,phip_th15],
                   'orificeLength':Lo,
                   'orificeDiameter':do,
                   'insertDiameter':dc})

#df.to_csv("positional_combined.csv",index=False)

### Note: we add the header by hand thereafter
header_str = """
############################
### DOCUMENT
# [1] K. K. Jameson, D. M. Goebel, and R. M. Watkins, “Hollow Cathode and Keeper-Region Plasma Measurements,” 41st AIAA/ASME/SAE/ASEE Jt. Propuls. Conf. Exhib., 2005.
### SOFTWARE
# Plot digitized using Engauge Digitizer
### CAPTION
# [1] Fig.4 Axial density cathode and anode profiles plotted on a semi-log scale for TH8 and TH15. 
# [1] Fig.6 Cathode plasma potential and electron temperature profiles for TH8 and TH15 
### DATA
# Id (A), log10(electron density) vs. x (in 1/m3 and mm, resp.), electron temperature vs. x (in eV and mm), idxmax, idxmin, dc (mm), mass flow (sccm of Xe), do (mm), Lo (mm), plasma potential vs. x (in V and mm)
### NOTES
############################
dischargeCurrent,electronDensity,electronTemperature,idxmax,idxmin,insertDiameter,massFlowRate_sccm,orificeDiameter,orificeLength,plasmaPotential
"""

