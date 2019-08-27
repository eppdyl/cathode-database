import pandas as pd
import numpy as np

from cathode.experimental.load_data import load_all_data

def assign_geometry(idx):
    if idx == 'NSTAR':
        # Length before actual pressure measurement and emitter length
        # See Mikellides, Physics of Plasmas, 2009, p. 013501-7
        Lupstream = 130. 
        Lemitter = 25.4        
    elif idx == 'NEXIS':
        Lupstream = 120. # Length before actual pressure measurement
        Lemitter = 25.4
    elif idx == 'Salhi-Xe' or idx == 'Salhi-Ar-1.21' or idx == 'Salhi-Ar-0.76':
        Lupstream = 130. # Not sure what the upstream length is. Set to same as NSTAR / NEXIS
        Lemitter = 25.4 # 1 in emitter
    elif idx == 'AR3' or idx == 'EK6' or idx == 'SC012':
        Lemitter = 25.4
        Lupstream = 500. # Length before actual pressure measurement
        # See Domonkos dissertation
        # "0.5-m upstream of the cathode insert" p.26
    elif idx == 'Siegfried':
        Lemitter = 25.4
        Lupstream = np.nan
    elif idx == 'T6':
        Lemitter = 25.4
        Lupstream = np.nan
    elif idx == 'Friedly':
        Lemitter = 25.4
        Lupstream = 120. # Length before actual pressure measurement
        
    return Lemitter,Lupstream
        
# Load all of the data
pdf = load_all_data()

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

# Empty dataframe
data = np.empty(0, dtype=dtypes)
alldata = pd.DataFrame(data)

### Fill dataframe with pressure data
first = True
for idx in pdf.index:
    Idvec  = pdf.Id[idx]
    mdotvec = pdf.mdot[idx]
    Pvec  = pdf.P[idx]
    dovec = pdf.do[idx]
    Lovec = pdf.Lo[idx]
   
    Twvec = pdf.Tw[idx]
    Tovec = pdf.To[idx]
    dcvec = pdf.dc[idx]
    
    length = len(Idvec)

    # Type of cathode?
    xecathodes = (idx == 'NSTAR' or 
                   idx =='NEXIS' or 
                   idx == 'Salhi-Xe' or 
                   idx == 'AR3' or
                   idx == 'EK6' or
                   idx == 'SC012' or
                   idx == 'Friedly' or
                   idx == 'T6')
    
    hgcathode = (idx == 'Siegfried')

    # If this is the first index, directly populate the dataframe
    if first == True:
        
        alldata['dischargeCurrent'] = Idvec
        alldata['massFlowRate'] = mdotvec
        if xecathodes:
            alldata['gas'] = 'Xe'
        elif hgcathode:
            alldata['gas'] = 'Hg'
        else:
            alldata['gas'] = 'Ar'
        
        alldata['orificeDiameter'] = dovec
        alldata['orificeLength'] = Lovec
        alldata['insertDiameter'] = dcvec
        alldata['insertTemperatureAverage'] = Twvec
        
        Lemitter, Lupstream = assign_geometry(idx)
        
        alldata['insertLength'] = Lemitter
        alldata['upstreamPressurePoint'] = Lupstream
        
        
        alldata['totalPressure'] = Pvec
        alldata['orificeTemperature'] = Tovec
        
        alldata['cathode'] = idx
        
        first = False
        
    # Otherwise, create temporary dataframe to append
    else:
        tmp = pd.DataFrame(data)
        
        tmp['dischargeCurrent'] = Idvec
        tmp['massFlowRate'] = mdotvec
        tmp['totalPressure'] = Pvec
        tmp['orificeDiameter'] = dovec
        tmp['orificeLength'] = Lovec
        tmp['orificeTemperature'] = Tovec
        tmp['insertDiameter'] = dcvec    
        tmp['insertTemperatureAverage'] = Twvec
        
        
        if xecathodes:
            tmp['gas'] = 'Xe'
        elif hgcathode:
            tmp['gas'] = 'Hg'
        else:
            tmp['gas'] = 'Ar'

        Lemitter, Lupstream = assign_geometry(idx)
        
        tmp['insertLength'] = Lemitter
        tmp['upstreamPressurePoint'] = Lupstream
        
        tmp['cathode'] = idx
        
        alldata = alldata.append(tmp,ignore_index=True)

### Populate references
alldata.loc[0:4,'reference'] = 'K. K. Jameson, D. M. Goebel, and R. M. Watkins, "Hollow Cathode and Keeper-Region Plasma Measurements," 41st AIAA/ASME/SAE/ASEE Joint Propulsion Conference and Exhibit, 2005.'
alldata.loc[0:4,'note'] = 'Figure 3 - Pressure measured inside the 1/4" hollow cathode for various NSTAR throttle levels. The throttle levels TH4, TH8, TH15 are from: V. Rawlin, J. Sovey, J. Anderson, and J. Polk, "NSTAR flight thruster qualification testing," 34th AIAA/ASME/SAE/ASEE JPC, 1998.TH12: W. G. Tighe, K. Chien, D. M. Goebel, and R. T. Longo, “Hollow Cathode Ignition and Life Model,” 41st AIAA/ASME/SAE/ASEE Jt. Propuls. Conf. Exhib., 2005.


