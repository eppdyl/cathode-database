import cathode.constants as cc
import numpy as np
import h5py
import datetime

from assemble import assemble

data = assemble()
gam = 5/3

constant_dict = {'pi':np.pi,
                 'q':cc.e,
                 'amu':cc.atomic_mass,
                 'gam':gam,
                 'kb':cc.Boltzmann,
                 'Torr':cc.Torr,
                 'mu0':cc.mu0}


### PI PRODUCTS
PI1_str = 'PI1 = totalPressure_SI / magneticPressure'
PI2_str = 'PI2 = orificeDiameter / insertDiameter'
PI3_str = 'PI3 = orificeDiameter / orificeLength'
PI4_str = 'PI4 = (massFlowRate_SI * @q / (gasMass * @amu * dischargeCurrent))**2 * (gasMass * @amu * orificeDiameter * 1e-3)/(@mu0 * @q**2)'
PI5_str = 'PI5 = gdPressure / magneticPressure'
PI6_str = 'PI6 = izPressure / magneticPressure * orificeLength / orificeDiameter'
PI7_str = 'PI7 = reynoldsNumber'

data.eval(PI1_str, local_dict=constant_dict, inplace=True)
data.eval(PI2_str, local_dict=constant_dict, inplace=True)
data.eval(PI3_str, local_dict=constant_dict, inplace=True)
data.eval(PI4_str, local_dict=constant_dict, inplace=True)
data.eval(PI5_str, local_dict=constant_dict, inplace=True)
data.eval(PI6_str, local_dict=constant_dict, inplace=True)
data.eval(PI7_str, local_dict=constant_dict, inplace=True)

### Create HDF5 file
fname = 'cathode_database.h5'
f = h5py.File(fname,'w')
f.create_group("data")

# Get a timestamp
ts = datetime.datetime.utcnow()
ts = ts.strftime('%Y%m%d%H%M%S')
ts = (int)(ts)

f.create_dataset('timestamp',shape=(1,),data=ts,dtype=np.int64)
f.close()

# Dump the data, compressed
data.to_hdf(fname,'data',complib='zlib',complevel=9)