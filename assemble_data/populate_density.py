import pandas as pd
import numpy as np

import cathode.constants as cc

root = '/Users/Pyt/Documents/Pyt/hollow_cathode/cathode-data'

def NEXIS_density(alldata):
    nexis_root = '/jpl/nexis/staging/'
    
    # mdot = 5.5 sccm, Id = 25 A
    # Source: Goebel JAP 2005
    data = np.genfromtxt(root + nexis_root + 'ne_vs_x_mdot-5.5sccm_Id-25A.csv',
                         delimiter=',')
    
    data[:,1] *= 1e20
    
    ref = ("I. G. Mikellides, I. Katz, D. M. Goebel, and J. E. Polk, "
           "\"Hollow cathode theory and experiment. II. A two-dimensional "
           "theoretical model of the emitter region,\" J. Appl. Phys., "
           "vol. 98, no. 2005, pp. 0–14, 2005.")
    alldata = alldata.append({'cathode' : 'NEXIS', 
                              'dischargeCurrent' : 25.,
                              'massFlowRate': 5.5*cc.sccm2eqA,
                              'gas':'Xe',
                              'orificeDiameter': np.unique(alldata[alldata.cathode=='NEXIS'].orificeDiameter),
                              'insertDiameter': np.unique(alldata[alldata.cathode=='NEXIS'].insertDiameter),
                              'insertLength': np.unique(alldata[alldata.cathode=='NEXIS'].insertLength),
                              'upstreamPressurePoint': np.unique(alldata[alldata.cathode=='NEXIS'].upstreamPressurePoint),
                              'electronDensity': data,
                              'reference': ref,
                              'note': 'Fig. 5'
                              } , ignore_index=True)
#
#dtypes = np.dtype([
#        ('cathode',str), # Cathode name
#       ('dischargeCurrent',float), # Discharge current , A
#       ('massFlowRate',float), # Mass flow rate, eqA
#       ('gas',str), # Gas used (periodic table shortcut)
#       ('orificeDiameter',float), # Orifice diam, mm
#       ('orificeLength',float), # Orifice length, mm
#       ('insertDiameter',float), # Insert diameter, mm
#       ('insertLength',float), # Insert length, mm
#       ('upstreamPressurePoint',float), # Distance upstream of the emitter where the pressure is measured, mm
#       ('orificeTemperature',float), # Orifice temperature, degC
#       ('insertTemperatureAverage',float), # Average insert temperature, degC
#       ('insertTemperature',np.ndarray), # Insert temperature vs. position, degC
#       ('totalPressure',float), # Total pressure, Torr
#       ('totalPressureError_p',float), # Total pressure error (+)
#       ('totalPressureError_m',float), # Total pressure error (-) 
#       ('electronDensity',np.ndarray), # Density vs. position, 1/m3
#       ('electronTemperature',np.ndarray), # Electron temp. vs position, eV
#       ('plasmaPotential',np.ndarray), # Plasma potential vs position, V
#       ('reference',str), # Literature reference
#        ('note',str)]) # Any noteworthy comment