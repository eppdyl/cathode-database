import numpy as np
import pandas as pd
from import_db import dtypes

import cathode.constants as cc

### For our cathode we have so few data that we directly insert them here

def append_PLHC(alldata):
    data = np.empty(0, dtype=dtypes)
    
    Idvec = np.array([173.737217316,226.309499823,252.120895328,
                      202.857445668,158.760843979,255.883993674,
                      226.509883685,275.785704668,
                      100, 159, 200, 250.67, 306.67])
    
    mdotvec_sccm = np.array([109,109,109,
                             145,145,145,
                             218,218,
                             109,109,109,109,109])
    mdotvec = mdotvec_sccm * cc.sccm2eqA
    
    Pvec = np.array([2.7202039443,3.11963348215,3.13307955714,
                     3.30721753878,3.11336077807,3.75572869208,
                     4.75656737511,4.5589258277,
                     2.44,3.11,3.63,4.3,5.4])
    
#    dovec = np.ones(len(Pvec)) * 5.6
#    Lovec = np.ones(len(Pvec)) * 1.5
#    Tovec = np.ones(len(Pvec)) * np.nan
#    dcvec = np.ones(len(Pvec)) * 27.15
#    Twvec = np.copy(Tovec)

    tmp = pd.DataFrame(data)
    
    tmp['dischargeCurrent'] = Idvec
    tmp['massFlowRate'] = mdotvec
    tmp['totalPressure'] = Pvec
    tmp['orificeDiameter'] = 5.6
    tmp['orificeLength'] = 1.5
    tmp['orificeTemperature'] = np.nan
    tmp['insertDiameter'] = 27.15    
    tmp['insertTemperatureAverage'] = np.nan
    tmp['gas'] = 'Ar'
    
    tmp['insertLength'] = 80.4
    tmp['upstreamPressurePoint'] = 220
    
    tmp['cathode'] = 'PLHC'
    
    alldata = alldata.append(tmp,ignore_index=True)
    alldata.loc[alldata.cathode=='PLHC','reference'] = "PY Taunay, PhD dissertation, Princeton, 2020"
    alldata.loc[alldata.cathode=='PLHC','note'] = 'Experimental data from Chapter 2. Last 5 measurements are made with Baratron gauge'

    return alldata