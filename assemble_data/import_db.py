import numpy as np
import ast
import re

from db_references import referenceList,noteList


### Columns and respective type
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

### List of cathode names
cathodeList = ['NSTAR','NEXIS','Salhi','Salhi-Ar-1.21','Salhi-Ar-0.76',
               'Salhi-Xe','Siegfried','Siegfried-NG','Friedly','T6','AR3',
               'EK6','SC012','JPL-1.5cm','JPL-1.5cm-3mm','JPL-1.5cm-5mm',
               'PLHC'
               ]

### Folders where the data lives
folderList = ['jpl/nstar/discharge',
              'jpl/nexis',
              'lewis/salhi',
              None,None,None,
              'lewis/siegfried',
              None,
              'lewis/friedly',
              'rae/t6',
              'pepl/domonkos',
              'pepl/domonkos',
              'pepl/domonkos',
              'jpl/lab6-cathodes/1.5cm-cathode',
              None,None,
              'princeton/plhc']

### List of files to parse in each folder
fileList = [['P_vs_Id_mdot.csv','positional_combined.csv'],
            ['P_vs_Id_mdot.csv','positional_combined.csv'],
            ['P_vs_Id_mdot.csv','positional_combined.csv'],None,None,None,
            ['P_vs_Id_mdot.csv','positional_combined.csv'],None,
            ['P_vs_Id_mdot.csv'],
            ['P_vs_Id_mdot.csv'],
            ['P_vs_mdot_Id-1A_AR3.csv'],
            ['P_vs_mdot_Id_EK6.csv'],
            ['P_vs_mdot_Id_SC012.csv'],
            ['P_vs_Id_mdot.csv','positional_combined.csv'],None,None,
            ['P_vs_Id_mdot.csv']]

### Further geometry info
# For each cathode, tuple with (emitter length, upstream pressure point) 
# Dimensions are in mm
additionalGeometry = [(25.4,130.), # NSTAR See Mikellides, Physics of Plasmas, 2009, p. 013501-7
                      (25.4,120.), # NEXIS
                      (25.4,130.), # Salhi Not sure what the upstream length is. Set to same as NSTAR / NEXIS
                      None,None,None,
                      (25.4,np.nan), # Siegfried
                      None,
                      (25.4,120.), # Friedly
                      (25.4,np.nan), # T6
                      (25.4,500.), # AR3 Domonkos dissertation "0.5-m upstream of the cathode insert" p.26
                      (25.4,500.), # EK6
                      (25.4,500.), # SC012
                      (25.4,130.), # JPL 1.5 cm cathode: same pressure point as NSTAR / NEXIS bc. same setup
                      None, None,
                      (80.4,220) # PLHC
                      ]
fileDictionary = {
        'cathode' :cathodeList ,
        'folder': folderList,
        'datafile': fileList,
        'additionalGeometry': additionalGeometry,
        'reference': referenceList,
        'note': noteList
        }


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
    