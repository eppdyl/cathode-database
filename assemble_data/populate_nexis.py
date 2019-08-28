import numpy as np
import cathode.constants as cc

def populate_mikellides_jap_2005(alldata,root,cat_root):
    ### mdot = 5.5 sccm, Id = 25 A
    # Source: Mikellides JAP 2005
    # First get the density
    data = np.genfromtxt(root + cat_root + 'ne_vs_x_mdot-5.5sccm_Id-25A.csv',
                         delimiter=',')
    
    data[:,1] *= 1e20
    
    ref = ("I. G. Mikellides, I. Katz, D. M. Goebel, and J. E. Polk, "
           "\"Hollow cathode theory and experiment. II. A two-dimensional "
           "theoretical model of the emitter region,\" J. Appl. Phys., "
           "vol. 98, no. 2005, pp. 0–14, 2005.")
    
    ne_data = np.copy(data)
    
    # Then get temperature and potential
    data = np.genfromtxt(root + cat_root + 'Te-phip_vs_x_mdot-5.5sccm_Id-25A.csv',
                         skip_header = True,
                         delimiter=',')
    phip_data = data[~np.isnan(data[:,1])][:,0:2]
    Te_data = data[~np.isnan(data[:,2])][:,0::2]
    
    alldata = alldata.append({'cathode' : 'NEXIS', 
                              'dischargeCurrent' : 25.,
                              'massFlowRate': 5.5*cc.sccm2eqA,
                              'gas':'Xe',
                              'orificeDiameter': np.unique(alldata[alldata.cathode=='NEXIS'].orificeDiameter)[0],
                              'orificeLength': np.unique(alldata[alldata.cathode=='NEXIS'].orificeLength)[0],
                              'insertDiameter': np.unique(alldata[alldata.cathode=='NEXIS'].insertDiameter)[0],
                              'insertLength': np.unique(alldata[alldata.cathode=='NEXIS'].insertLength)[0],
                              'upstreamPressurePoint': np.unique(alldata[alldata.cathode=='NEXIS'].upstreamPressurePoint)[0],
                              'electronDensity': np.copy(ne_data),
                              'electronTemperature': np.copy(Te_data),
                              'plasmaPotential': np.copy(phip_data),
                              'reference': ref,
                              'note': 'Fig. 5'
                              } , ignore_index=True)
    
    return alldata

def populate_goebel_jpc_2004(alldata,root,cat_root):
    ### mdot = 5.5 sccm, Id = 10 A
    # Source: Goebel JPC 2004    
    ref = ("D. Goebel, K. K. Jameson, R. M. Watkins, and I. Katz, "
           "\"Hollow Cathode and Keeper-Region Plasma Measurements Using "
           "Ultra-Fast Miniature Scanning Probes,\" 40th JPC, 2004.")
    note = ("Fig. 12")
    
    # This one only has temperature and potential
    data = np.genfromtxt(root + cat_root + 'Te-phip_vs_x_mdot-5.5-10sccm_Id-10-25A.csv',
                         skip_header = True,
                         delimiter=',')
    
    Te_data = data[~np.isnan(data[:,1])][:,[0,1]]
    phip_data = data[~np.isnan(data[:,2])][:,[0,2]]
    
    bcond = (alldata.cathode=='NEXIS') & (alldata.dischargeCurrent == 10.) & (alldata.massFlowRate == 5.5*cc.sccm2eqA)
    alldata.loc[bcond,'electronTemperature'] = alldata.loc[bcond,'electronTemperature'].apply(lambda x: np.copy(Te_data))
    alldata.loc[bcond,'plasmaPotential'] = alldata.loc[bcond,'plasmaPotential'].apply(lambda x: np.copy(phip_data))
    alldata.loc[bcond,'reference'] = alldata.loc[bcond,'reference'] + "[2] " + ref
    alldata.loc[bcond,'note'] = alldata.loc[bcond,'note'] + "[2] " + note


    ### mdot = 10 sccm, Id = 25 A
    # Source: Goebel JPC 2004    
    ref = ("D. Goebel, K. K. Jameson, R. M. Watkins, and I. Katz, "
           "\"Hollow Cathode and Keeper-Region Plasma Measurements Using "
           "Ultra-Fast Miniature Scanning Probes,\" 40th JPC, 2004.")
 
    data = np.genfromtxt(root + cat_root + 'ne_vs_x_mdot-5-10sccm_Id-25A.csv',
                         delimiter=',')
    data[:,1] *= 1e20
    ne_data = np.copy(data)
    
    data = np.genfromtxt(root + cat_root + 'Te-phip_vs_x_mdot-5.5-10sccm_Id-10-25A.csv',
                         skip_header = True,
                         delimiter=',')
    
    Te_data = data[~np.isnan(data[:,3])][:,[0,3]]
    phip_data = data[~np.isnan(data[:,4])][:,[0,4]]
    
    alldata = alldata.append({'cathode' : 'NEXIS', 
                              'dischargeCurrent' : 25.,
                              'massFlowRate': 10*cc.sccm2eqA,
                              'gas':'Xe',
                              'orificeDiameter': np.unique(alldata[alldata.cathode=='NEXIS'].orificeDiameter)[0],
                              'orificeLength': np.unique(alldata[alldata.cathode=='NEXIS'].orificeLength)[0],
                              'insertDiameter': np.unique(alldata[alldata.cathode=='NEXIS'].insertDiameter)[0],
                              'insertLength': np.unique(alldata[alldata.cathode=='NEXIS'].insertLength)[0],
                              'upstreamPressurePoint': np.unique(alldata[alldata.cathode=='NEXIS'].upstreamPressurePoint)[0],
                              'electronDensity': np.copy(ne_data),
                              'electronTemperature': np.copy(Te_data),
                              'plasmaPotential': np.copy(phip_data),
                              'reference': ref,
                              'note': 'Fig. 12'
                              } , ignore_index=True)  
    
    return alldata