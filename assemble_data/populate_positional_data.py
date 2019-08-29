from populate_nexis import populate_goebel_jpc_2004,populate_mikellides_jap_2005
from populate_nstar import populate_th8, populate_th15
from populate_jpl_lab6 import populate_chu_2012, populate_becatti_2017

root = '/Users/Pyt/Documents/Pyt/hollow_cathode/cathode-data'

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
    jpl_lab6_root = '/original-material/chu-ieee-2012/csv/'
    
    alldata = populate_chu_2012(alldata,root,jpl_lab6_root)
    
    jpl_lab6_root = '/original-material/becatti-jpp-2017/csv/'
    alldata = populate_becatti_2017(alldata,root,jpl_lab6_root)
    
    return alldata
