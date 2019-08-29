import numpy as np
import pandas as pd
import ast

### Columns
dtypes = np.dtype([
        ('cathode',str), # Cathode name
       ('dischargeCurrent',float), # Discharge current , A
       ('massFlowRate',float), # Mass flow rate, eqA
       ('gas',str), # Gas used (periodic table shortcut)
       ('orificeDiameter',float), # Orifice diam, mm
       ('orificeLength',float), # Orifice length, mm
       ('insertDiameter',float), # Insert diameter, mm
       ('insertLength',float), # Insert length, mm
       ('upstreamPressurePoint',float), # Distance upstream of the emitter where the pressure is measured, mm
       ('orificeTemperature',float), # Orifice temperature, degC
       ('insertTemperatureAverage',float), # Average insert temperature, degC
       ('insertTemperature',np.ndarray), # Insert temperature vs. position, degC
       ('totalPressure',float), # Total pressure, Torr
       ('totalPressureError_p',float), # Total pressure error (+)
       ('totalPressureError_m',float), # Total pressure error (-) 
       ('electronDensity',np.ndarray), # Density vs. position, 1/m3
       ('electronTemperature',np.ndarray), # Electron temp. vs position, eV
       ('plasmaPotential',np.ndarray), # Plasma potential vs position, V
       ('reference',str), # Literature reference
        ('note',str)]) # Any noteworthy comment

dtypes_import = np.dtype([
        ('',int),
        ('cathode',str), # Cathode name
       ('dischargeCurrent',float), # Discharge current , A
       ('massFlowRate',float), # Mass flow rate, eqA
       ('gas',str), # Gas used (periodic table shortcut)
       ('orificeDiameter',float), # Orifice diam, mm
       ('orificeLength',float), # Orifice length, mm
       ('insertDiameter',float), # Insert diameter, mm
       ('insertLength',float), # Insert length, mm
       ('upstreamPressurePoint',float), # Distance upstream of the emitter where the pressure is measured, mm
       ('orificeTemperature',float), # Orifice temperature, degC
       ('insertTemperatureAverage',float), # Average insert temperature, degC
       ('insertTemperature',np.ndarray), # Insert temperature vs. position, degC
       ('totalPressure',float), # Total pressure, Torr
       ('totalPressureError_p',float), # Total pressure error (+)
       ('totalPressureError_m',float), # Total pressure error (-) 
       ('electronDensity',np.ndarray), # Density vs. position, 1/m3
       ('electronTemperature',np.ndarray), # Electron temp. vs position, eV
       ('plasmaPotential',np.ndarray), # Plasma potential vs position, V
       ('reference',str), # Literature reference
        ('note',str)]) # Any noteworthy comment

def from_np_array(array_string):
    ''' See https://stackoverflow.com/questions/42755214/how-to-keep-numpy-array-when-saving-pandas-dataframe-to-csv
    Modified to take the possibility of a NaN into account
    '''
    try:
        array_string = ','.join(array_string.replace('[ ', '[').split())
        return np.array(ast.literal_eval(array_string))
    except:
        return np.nan
    
    
def import_data(datafile):
    alldata = pd.read_csv(datafile,
                          converters = {'electronDensity': from_np_array,
                                        'electronTemperature': from_np_array,
                                        'plasmaPotential': from_np_array},
                          dtype= dtypes_import
                          )
    
    return alldata