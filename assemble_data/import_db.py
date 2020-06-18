import numpy as np
#import pandas as pd
import ast
import re


### Columns
dtypes = np.dtype([('cathode',str), # Cathode name
       ### Controllable parameters: Id, mdot
       ('dischargeCurrent',float), # Discharge current , A
       ('massFlowRate',float), # Mass flow rate, eqA
       ('massFlowRate_sccm',float), # Mass flow rate, sccm
       ('massFlowRate_SI',float), # Mass flow rate, kg/s
       ### Gas information
       ('gas',str), # Gas used (periodic table shortcut)
       ('gasMass',float), # Mass of gas (amu)
       ('ionizationPotential',float), # Ionization potential
       ### Geometry
       ('orificeDiameter',float), # Orifice diam, mm
       ('orificeLength',float), # Orifice length, mm
       ('insertDiameter',float), # Insert diameter, mm
       ('insertLength',float), # Insert length, mm
       ('upstreamPressurePoint',float), # Distance upstream of the emitter where the pressure is measured, mm
       ### Insert material
       ('workFunction',float), # Work function in eV if specified, eV
       ('insertMaterial',str), # Insert material if specified       
       ### Data of interest
       ## Cathode temperatures
       ('orificeTemperature',float), # Orifice temperature, degC
       ('insertTemperatureAverage',float), # Average insert temperature, degC
       ('insertTemperature',np.ndarray), # Insert temperature vs. position, degC
       ## Total pressure
       ('totalPressure',float), # Total pressure, Torr
       ('totalPressureError_p',float), # Total pressure error (+)
       ('totalPressureError_m',float), # Total pressure error (-) 
       ## Plasma quantity
       # Positional data
       ('electronDensity',np.ndarray), # Density vs. position, 1/m3
       ('electronDensity_err',np.ndarray), # Error in density vs. position, 1/m3
       ('electronTemperature',np.ndarray), # Electron temp. vs position, eV
       ('electronTemperature_err',np.ndarray), # Error on the electron temperature vs. position, eV
       ('plasmaPotential',np.ndarray), # Plasma potential vs position, V
       ('plasmaPotential_err',np.ndarray), # Error in plasma potential vs position, V
       ('idxmin',int), # Indices used to calculate the attachment length
       ('idxmax',int), # Indices used to calculate the attachment length       
       # Average and max. data
       ('electronDensityMax',float), # Maximum electron density, 1/m3
       ('electronDensityAverage',float), # Average electron density, 1/m3
       ('electronDensityAverage_err',float), # Error in electron density, 1/m3
       ('electronTemperatureAverage',float), # Line-averaged electron temp, eV
       ('electronTemperatureAverage_err',float), # Line-averaged electron temp error, eV
       ('plasmaPotentialAverage',float), # Line-averaged plasma potential, V
       ('plasmaPotentialAverage_err',float), # Line-averaged plasma potential err, V
       # Discharge voltage
       ('dischargeVoltage',float),
       ### Information
       ('reference',str), # Literature reference
       ('note',str)]) # Any noteworthy comment

#dtypes_import = np.dtype([
#        ('',int),
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



def from_np_array(array_string):
    ''' See https://stackoverflow.com/questions/42755214/how-to-keep-numpy-array-when-saving-pandas-dataframe-to-csv
    Modified to take the possibility of a NaN into account
    '''

    bcond = array_string is not None
    bcond &= array_string is not 'NaN'
    bcond &= array_string is not ' '
    bcond &= array_string is not ''
    
    if bcond:
        # See https://stackoverflow.com/questions/6116978/how-to-replace-multiple-substrings-of-a-string
        t_str = re.sub('\[ *','[',array_string)
        t_str = ','.join(t_str.split())
            
        ret = np.array(ast.literal_eval(t_str),dtype=np.float64)

        return ret
    else:
        return np.nan
    
#def import_data(datafile):
#    alldata = pd.read_csv(datafile,
#                          converters = {'electronDensity': from_np_array,
#                                        'electronTemperature': from_np_array,
#                                        'plasmaPotential': from_np_array},
#                          dtype= dtypes_import
#                          )
    
#    return alldata