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
ne_data = np.genfromtxt("raw/ne_vs_position_TH8-TH15.csv",delimiter=",",
                        skip_header=1)

ne_th8 = ne_data[~np.isnan(ne_data[:,1])][:,[0,1]]
ne_th15 = ne_data[~np.isnan(ne_data[:,2])][:,[0,2]]

# Extract Te and potential
data = np.genfromtxt("raw/phip-Te_vs_position_TH8-TH15.csv",delimiter=",",
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

df.to_csv("positional_combined.csv",index=False)

### Note: we add the header by hand thereafter