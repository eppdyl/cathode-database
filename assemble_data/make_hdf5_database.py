# MIT License
# 
# Copyright (c) 2020 Pierre-Yves Taunay 
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

'''
File: make_hdf5_database.py
Author: Pierre-Yves Taunay
Date: July 2020

The script to make the HDF5 library.
'''
import argparse
import h5py
import datetime

from derived_quantities import generate_dataframe_derived 
from load_all_data import generate_dataframe

### Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--pressureEmpirical", help="Should the pressure be\
        calculated with the empirical correlation if not provided?", 
        action='store_true')
parser.add_argument("-d", "--derivedQuantity", help="Should derived\
        quantities be calculated?", action='store_true')
parser.add_argument("-f", "--filename", help="Filename for the HDF5 file.",
        type=str, default="cathode_database.h5") 

args = parser.parse_args()

### Generate the dataframe
if args.pressureEmpirical:
    data = generate_dataframe_derived(empirical_pressure = args.pressureEmpirical)
elif args.derivedQuantity:
    data = generate_dataframe_derived()
else:
    data = generate_dataframe()

### Dump to HDF5
fname = args.filename 
f = h5py.File(fname,'w')
f.create_group("data")

# Get a timestamp
ts = datetime.datetime.utcnow()
ts = ts.strftime('%Y%m%d%H%M%S')
ts = (int)(ts)

f.create_dataset('timestamp',shape=(1,),data=ts,dtype=np.int64)
f.close()

data.to_hdf(fname,'data',complib='zlib',complevel=9)

