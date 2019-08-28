import pandas as pd
import numpy as np
import ast

import cathode.constants as cc

from populate_nexis import populate_goebel_jpc_2004,populate_mikellides_jap_2005
from populate_nstar import populate_th8, populate_th15
from populate_jpl_lab6 import populate_chu_2012, populate_becatti_2017

root = '/Users/Pyt/Documents/Pyt/hollow_cathode/cathode-data'

def from_np_array(array_string):
    ''' See https://stackoverflow.com/questions/42755214/how-to-keep-numpy-array-when-saving-pandas-dataframe-to-csv
    Modified to take the possibility of a NaN into account
    '''
    try:
        array_string = ','.join(array_string.replace('[ ', '[').split())
        return np.array(ast.literal_eval(array_string))
    except:
        return np.nan

def populate_NEXIS(alldata):
    nexis_root = '/jpl/nexis/staging/'
    
    alldata = populate_mikellides_jap_2005(alldata,root,nexis_root)
    alldata = populate_goebel_jpc_2004(alldata,root,nexis_root)
    
    return alldata


def populate_NSTAR(alldata):
    nstar_root = '/jpl/nstar/discharge/staging/'
    
    alldata = populate_th8(alldata,root,nstar_root)
    alldata = populate_th15(alldata,root,nstar_root)
    
    return alldata


def populate_JPL_lab6(alldata):
    jpl_lab6_root = '/jpl/goebel-lab6-cathodes/1.5cm-cathode/staging/'
    
    alldata = populate_chu_2012(alldata,root,jpl_lab6_root)
    
    jpl_lab6_root = '/original-material/becatti-jpp-2017/csv/'
    alldata = populate_becatti_2017(alldata,root,jpl_lab6_root)
    
    return alldata
