import numpy as np
import pandas as pd
import ast

### Columns
dtypes = np.dtype([
        ('cathode',str), # Cathode name
       ('dischargeCurrent',float), # Discharge current , A
       ('massFlowRate',float), # Mass flow rate, eqA
       ('massFlowRate_sccm',float), # Mass flow rate, sccm
       ('massFlowRate_SI',float), # Mass flow rate, kg/s
       ('gas',str), # Gas used (periodic table shortcut)
       ('gasMass',float), # Mass of gas (amu)
       ('ionizationPotential',float), # Ionization potential
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

### See https://stackoverflow.com/questions/6116978/how-to-replace-multiple-substrings-of-a-string
### for multiple replacements
import re
#string_rep = {'[ ': '[', '[  ': '['}
#string_rep = dict((re.escape(k), v) for k, v in string_rep.items()) 
#pattern = re.compile("|".join(string_rep.keys()))

#dat = '[[-3.7242, 19.5563869], [-3.4435, 19.5977391], [-3.0552, 19.6354636], [-2.6882, 19.6768125], [-2.1704, 19.7185515], [-1.8678, 19.763892], [-1.5869, 19.8016643], [-1.435, 19.8424657], [-1.3477, 19.8811335], [-1.1937, 19.9722769], [-1.1741, 19.9178992], [-1.1733, 19.9423801], [-1.1282, 19.9939474], [-0.9333, 20.0185923], [-0.76, 20.0400166], [-0.5005, 20.0631419], [-0.3271, 20.0859574], [-0.2831, 20.103554], [-0.2174, 20.1236132], [-0.2164, 20.1397752], [-0.2155, 20.1568156], [-0.2141, 20.1787727], [-0.0407, 20.1963614], [0.0046, 20.2283182], [0.1754, 20.2061888], [0.1778, 20.241661], [0.3526, 20.2744465], [0.3945, 20.2592187], [0.4154, 20.2505249], [0.4829, 20.2880792], [0.5484, 20.298685], [0.7646, 20.3085239], [0.9809, 20.3191436], [1.0682, 20.3314617], [1.2416, 20.3434401], [1.4795, 20.3541718], [1.7389, 20.3641925], [2.1708, 20.3753051], [2.5376, 20.381835], [3.0549, 20.3852684], [3.5291, 20.3886766], [4.0673, 20.3860993], [4.5191, 20.3809146], [4.777, 20.3752318], [5.1427, 20.3708054], [5.4866, 20.3636364], [5.9175, 20.3649748], [6.1105, 20.3563376], [6.3894, 20.3442311], [6.7343, 20.3475115], [6.9274, 20.3394693], [7.2713, 20.3312734], [8.1315, 20.3164107], [8.9923, 20.3067166], [9.4002, 20.290989], [9.8947, 20.2796236], [10.4538, 20.2679504], [10.948, 20.2530568], [11.4211, 20.2424321], [11.7862, 20.2272438], [12.1944, 20.2134195], [12.8604, 20.1871003], [13.204, 20.1712173], [13.763, 20.154716], [14.2148, 20.1451], [14.4939, 20.129896], [14.9236, 20.1092984], [15.2029, 20.0969517], [15.7614, 20.0676027], [16.2766, 20.0303325], [16.7711, 20.0093914], [17.2657, 19.9895299], [17.8461, 19.9619334], [18.2328, 19.9336998], [18.706, 19.9150514], [19.1568, 19.8696189], [19.823, 19.8172678], [20.5321, 19.7522252], [21.0477, 19.6908515], [21.7144, 19.6389283], [22.2089, 19.5854156], [22.898, 19.5770895], [23.328, 19.5242403], [23.8226, 19.4640422], [24.382, 19.4106254], [25.0925, 19.3896975], [25.6519, 19.3205824], [26.2978, 19.2893883], [26.7714, 19.2558512], [27.5897, 19.2378452], [28.4081, 19.2314441], [29.1186, 19.1860518], [30.0015, 19.1576079], [30.7982, 19.1113297], [31.5949, 19.0773679], [32.3279, 19.198107], [33.3616, 19.1703791], [33.8356, 19.1908078], [34.4811, 19.084469]]'

def from_np_array(array_string):
    ''' See https://stackoverflow.com/questions/42755214/how-to-keep-numpy-array-when-saving-pandas-dataframe-to-csv
    Modified to take the possibility of a NaN into account
    '''
#    array_string = pattern.sub(lambda m: string_rep[re.escape(m.group(0))], array_string)
#    try:

    bcond = array_string is not None
    bcond &= array_string is not 'NaN'
    bcond &= array_string is not ' '
    bcond &= array_string is not ''
    
    if bcond:
#        print(array_string)
        t_str = re.sub('\[ *','[',array_string)
        t_str = ','.join(t_str.split())
            
#        print(ast.literal_eval(t_str))
#        try:
        ret = np.array(ast.literal_eval(t_str),dtype=np.float64)
            
    
#        ret = ret[~np.isnan(ret)]
        
        return ret
    else:
        return np.nan
    
def import_data(datafile):
    alldata = pd.read_csv(datafile,
                          converters = {'electronDensity': from_np_array,
                                        'electronTemperature': from_np_array,
                                        'plasmaPotential': from_np_array},
                          dtype= dtypes_import
                          )
    
    return alldata