import cathode.constants as cc
import numpy as np

import matplotlib.pyplot as plt

from assemble import assemble


#data = assemble()

constant_dict = {'pi':np.pi,
                 'q':cc.e,
                 'amu':cc.atomic_mass,
                 'gam':5/3,
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



### PLOT ALL PI PRODUCTS AGAINST ONE ANOTHER
plot_pp_all = True
if plot_pp_all:
    fig, ax = plt.subplots(7,7)
    
    # For each pi product...
    for idxi in range(7):
        PIi_str = 'PI' + str(idxi+1)
        
        for idxj in range(7):
            if idxj >= idxi:
                PIj_str = 'PI' + str(idxj+1)
                
                ax[idxi][idxj].plot(data[[PIj_str]],data[[PIi_str]],'ko')