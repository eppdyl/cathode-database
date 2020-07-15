import cathode.constants as cc
import numpy as np
from assemble import assemble

#data = assemble()

### NSTAR
### NEXIS
### PLHC
namelist = np.array(['NSTAR','NEXIS','PLHC'])
gam = 5/3
Tgmin = 2000 # K
Tgmax = 4000 # K

#alpha_min = 1 + 1/gam
#alpha_max = 1 + np.sqrt(2*np.pi) * (2/(gam+1)) ** (1/(gam-1)) / np.sqrt(gam)
#alpha_max = 1 + np.sqrt(2*np.pi) * ((gam+1)/2) ** (1/(gam-1)) / np.sqrt(gam)
#alpha_max = 3.2
alpha_min = 1/gam * ((gam+1)/2)**(gam/(gam-1))
alpha_max = np.sqrt(2*np.pi)*1/np.sqrt(gam)*(gam+1)/2

Cmin = 3.7 # Torr-cm
Cmax = 3.7 


print("cathode,demonstrated min, demonstrated max, estimated min, estimated max")
for name in namelist:
    df = data[data.cathode==name]
    
    if name == 'NEXIS':
        do = 2.5
    else:
        do = np.unique(df.orificeDiameter)[0]

    dc = np.unique(df.insertDiameter)[0]
    M = np.unique(df.gasMass)[0] * cc.atomic_mass
    Rg = cc.Boltzmann / M
       
    ### Min values
    amin = np.sqrt(gam * Rg * Tgmin)
    amax = np.sqrt(gam * Rg * Tgmax)
    
    mdot_max = Cmax * cc.Torr / (dc * 0.1) * np.pi * (do/2*1e-3)**2 / (amin  * alpha_min)
    mdot_min = Cmin * cc.Torr / (dc * 0.1) * np.pi * (do/2*1e-3)**2 / (amax  * alpha_max)
    
    xp_min = np.min(df.massFlowRate/cc.sccm2eqA)
    xp_max = np.max(df.massFlowRate/cc.sccm2eqA)
    
    print(name,xp_min,xp_max,mdot_min * cc.e / M / cc.sccm2eqA,mdot_max *  cc.e / M / cc.sccm2eqA)
