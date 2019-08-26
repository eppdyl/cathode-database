import pandas as pd
import numpy as np

from cathode.experimental.load_data import load_all_data

# Load all of the data
pdf = load_all_data()

### Columns
#col = ['cathode',
#       'Id',
#       'mdot',
#       'gas',
#       'do',
#       'Lo',
#       'dc',
#       'Lemitter',
#       'Lupstream_P',
#       'To',
#       'Tw',
#       'P',
#       'ne',
#       'Te',
#       'phip',
#       'reference','note']
#
#dt = ['str', #cathode
#         'float', #Id
#         'float', #mdot
#         'str', #gas
#         'float', #do
#         'float', #Lo
#         'float', #dc
#         'float', #Lemitter
#         'float', #Lupstream_P
#         'float', #To
#         'object', #Tw
#         'float', #P
#         'object', #ne
#         'object', #Te
#         'object', #phip
#         'str', #reference
#         'str']

dtypes = np.dtype([
        ('cathode',str),
       ('Id',float),
       ('mdot',float),
       ('gas',str),
       ('do',float),
       ('Lo',float),
       ('dc',float),
       ('Lemitter',float),
       ('Lupstream_P',float),
       ('To',float),
       ('Tw',np.ndarray),
       ('P',float),
       ('ne',np.ndarray),
       ('Te',np.ndarray),
       ('phip',np.ndarray),
       ('reference',str),
        ('note',str)])

#alldata = pd.DataFrame(columns=col,dtype=np.dtype(dt))
data = np.empty(0, dtype=dtypes)
alldata = pd.DataFrame(data)

first = True
for idx in pdf.index:
    Idvec  = pdf.Id[idx]
    mdotvec = pdf.mdot[idx]
    Pvec  = pdf.P[idx]
    dovec = pdf.do[idx]
    Lovec = pdf.Lo[idx]
   
    Tovec = pdf.To[idx]
    dcvec = pdf.dc[idx]
    
    length = len(Idvec)

    if first == True:
        alldata['Id'] = Idvec
        alldata['mdot'] = mdotvec
        alldata['Pvec'] = Pvec
        alldata['do'] = dovec
        alldata['Lo'] = Lovec
        alldata['To'] = Tovec
        alldata['dc'] = dcvec
        alldata['cathode'] = idx
        first = False
    else:
        tmp = pd.DataFrame(data)
        tmp['Id'] = Idvec
        tmp['mdot'] = mdotvec
        tmp['Pvec'] = Pvec
        tmp['do'] = dovec
        tmp['Lo'] = Lovec
        tmp['To'] = Tovec
        tmp['dc'] = dcvec      
        tmp['cathode'] = idx
        
        alldata = alldata.append(tmp,ignore_index=True)

