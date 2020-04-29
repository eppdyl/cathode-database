import numpy as np

def Pcorr(mdot,do,Id,species):
    if species == 'Ar':
        P = mdot/do**2 * (0.0056 + 0.0012*Id)
    elif species == 'Xe':
        P = mdot/do**2 * (0.0090 + 0.0040*Id)
    elif species == 'Hg':
        P = 1
        
    return P

#['cathode',
# 'dischargeCurrent',
# 'electronDensity',
# 'electronTemperature',
# 'gas',
# 'insertDiameter',
# 'insertLength',
# 'insertTemperature',
# 'insertTemperatureAverage',
# 'ionizationPotential',
# 'massFlowRate',
# 'note',
# 'orificeDiameter',
# 'orificeLength',
# 'orificeTemperature',
# 'plasmaPotential',
# 'reference',
# 'totalPressure',
# 'totalPressureError_m',
# 'totalPressureError_p',
# 'upstreamPressurePoint',]
    
def populate_sgng(alldata,root,cat_root):
    ref = ("P. J. Wilbur, \"Advanced Ion Thruster Research,\" CR-168340, 1984.")
    
    cat_name = 'Siegfried-NG'    
    do = 0.76
    dc = 3.8
    Lo = 1.8 
    Lem = 25.4
    
    ### DATA FROM FIGURES 37 THROUGH 44
    # Argon
    species = 'Ar'   
    # P,Lemit,Tc,Vp,Va,Vk,ne_max,ne_ave
    note = 'Figs. 37-40. Mass flow deduced from P, Id, do and correlation.'
    data = np.genfromtxt(root + cat_root + 'argon_do-0.76mm_Id-2.3A.csv',
                         skip_header = 15,
                         names = True,
                         delimiter=',') 
    
    Pvec = data['P']
    Lemit = data['Lemit']
    Tw = data['Tc']
    phip = data['Vp']
    ne_ave = data['ne_ave']
    Id = 2.3
    # Get the mass flow rate from P and Id
    mdot = Pvec * do**2 / (0.0056 + 0.0012 * Id) * 1e-3
    
    for idx,P in enumerate(Pvec):  
        alldata = alldata.append({'cathode' : cat_name, 
                                  'totalPressure': P,
                                  'dischargeCurrent' : Id,
                                  'electronDensity': ne_ave[idx],
                                  'gas':species,
                                  'massFlowRate': mdot[idx],                          
                                  'orificeDiameter': do,
                                  'orificeLength': Lo,
                                  'insertDiameter': dc,
                                  'insertLength': Lem,
                                  'insertTemperatureAverage': Tw[idx],
                                  'plasmaPotential':phip[idx],
#                                  'attachmentLength':Lemit[idx],
                                  'reference': ref,
                                  'note': note
                                  } , ignore_index=True) 
 
    # Id,Lemit,Tc,Vp,Va,Vk,ne_max,ne_ave
    note = 'Figs. 37-40. Pressure deduced from mdot, Id, do and correlation.'
    data = np.genfromtxt(root + cat_root + 'argon_do-0.76mm_mdot-287mA.csv',
                         skip_header = 15,
                         names = True,
                         delimiter=',') 
    
    Idvec = data['Id']
    Lemit = data['Lemit']
    Tw = data['Tc']
    phip = data['Vp']
    ne_ave = data['ne_ave']
    mdot = 287e-3 # A
    Pvec = Pcorr(mdot*1e3,do,Idvec,species)
    
    
    for idx,Id in enumerate(Idvec):        
        alldata = alldata.append({'cathode' : cat_name, 
                                  'totalPressure': Pvec[idx],
                                  'dischargeCurrent' : Id,
                                  'electronDensity': ne_ave[idx],
                                  'gas':species,
                                  'massFlowRate': mdot,                          
                                  'orificeDiameter': do,
                                  'orificeLength': Lo,
                                  'insertDiameter': dc,
                                  'insertLength': Lem,
                                  'insertTemperatureAverage': Tw[idx],
                                  'plasmaPotential':phip[idx],
#                                  'attachmentLength':Lemit[idx],
                                  'reference': ref,
                                  'note': note
                                  } , ignore_index=True) 
    
    # Xenon
    species = 'Xe'   
    # P,Lemit,Tc,Vp,Va,Vk,ne_max,ne_ave
    note = 'Figs. 41-44. Mass flow deduced from P, Id, do and correlation.'
    data = np.genfromtxt(root + cat_root + 'xenon_do-0.76mm_Id-2.3A.csv',
                         skip_header = 15,
                         names = True,
                         delimiter=',') 
    
    Pvec = data['P']
    Lemit = data['Lemit']
    Tw = data['Tc']
    phip = data['Vp']
    ne_ave = data['ne_ave']
    Id = 2.3
    # Get the mass flow rate from P and Id
    mdot = Pvec * do**2 / (0.0090 + 0.0040 * Id) * 1e-3
    
    for idx,P in enumerate(Pvec):  
        alldata = alldata.append({'cathode' : cat_name, 
                                  'totalPressure': P,
                                  'dischargeCurrent' : Id,
                                  'electronDensity': ne_ave[idx],
                                  'gas':species,
                                  'massFlowRate': mdot[idx],                          
                                  'orificeDiameter': do,
                                  'orificeLength': Lo,
                                  'insertDiameter': dc,
                                  'insertLength': Lem,
                                  'insertTemperatureAverage': Tw[idx],
                                  'plasmaPotential':phip[idx],
#                                  'attachmentLength':Lemit[idx],
                                  'reference': ref,
                                  'note': note
                                  } , ignore_index=True) 
 
    # Id,Lemit,Tc,Vp,Va,Vk,ne_max,ne_ave
    note = 'Figs. 41-44. Pressure deduced from mdot, Id, do and correlation.'
    data = np.genfromtxt(root + cat_root + 'xenon_do-0.76mm_mdot-92mA.csv',
                         skip_header = 15,
                         names = True,
                         delimiter=',') 
    
    Idvec = data['Id']
    Lemit = data['Lemit']
    Tw = data['Tc']
    phip = data['Vp']
    ne_ave = data['ne_ave']
    mdot = 92e-3 # A
    Pvec = Pvec = Pcorr(mdot*1e3,do,Idvec,species)
    
    for idx,Id in enumerate(Idvec):        
        alldata = alldata.append({'cathode' : cat_name, 
                                  'totalPressure': Pvec[idx],
                                  'dischargeCurrent' : Id,
                                  'electronDensity': ne_ave[idx],
                                  'gas':species,
                                  'massFlowRate': mdot,                          
                                  'orificeDiameter': do,
                                  'orificeLength': Lo,
                                  'insertDiameter': dc,
                                  'insertLength': Lem,
                                  'insertTemperatureAverage': Tw[idx],
                                  'plasmaPotential':phip[idx],
#                                  'attachmentLength':Lemit[idx],
                                  'reference': ref,
                                  'note': note
                                  } , ignore_index=True)     
    

    
    # Xenon positional data
    note = 'Fig. 29 Mass flow deduced from P, Id, do and correlation.'
    data = np.genfromtxt(root + cat_root + 'xenon_ne_vs_x_do-0.76mm_Id-2.3A.csv',
                         skip_header = 13,
                         names = True,
                         delimiter=',') 
    
    # Id,do,dc,P,phi_wf,x,ne
    P = 4
    Id = 2.3
    nevec = np.zeros((len(data['x']),2))
    nevec[:,0] = np.copy(data['x'])
    nevec[:,1] = np.copy(data['ne'])
    
    
    # Get the mass flow rate from P and Id
    mdot = P * do**2 / (0.0090 + 0.0040 * Id) * 1e-3
    alldata = alldata.append({'cathode' : cat_name, 
                              'totalPressure': P,
                              'dischargeCurrent' : Id,
                              'electronDensity': nevec[data['phi_wf']==1.9],
                              'gas':species,
                              'massFlowRate': mdot,                          
                              'orificeDiameter': do,
                              'orificeLength': Lo,
                              'insertDiameter': dc,
                              'reference': ref,
                              'note': note
                              } , ignore_index=True) 

    alldata = alldata.append({'cathode' : cat_name, 
                          'totalPressure': P,
                          'dischargeCurrent' : Id,
                          'electronDensity': nevec[data['phi_wf']==2.5],
                          'gas':species,
                          'massFlowRate': mdot,                          
                          'orificeDiameter': do,
                          'orificeLength': Lo,
                          'insertDiameter': dc,
                          'reference': ref,
                          'note': note
                          } , ignore_index=True)


    return alldata
    
#    ''