import numpy as np
from cathode import constants as cs

from cathode.models.flow import poiseuille_flow

import matplotlib.pyplot as plt

from matplotlib2tikz import save as tikz_save

# Import data
data = np.genfromtxt('P_vs_Id_mdot.csv',delimiter=',',dtype=np.float64,skip_header=14,names=True)

Idxp = data['Id']
mdotxp = data['mdot']
Pxp = data['P']

do = 1.02 # Orifice diameter, mm
Lo = 0.74 # Orifice length, mm
dc = 0.38 # Insert diameter, cm
Lc = 2.54 # Diameter length, cm

Pdown = poiseuille_flow( Lo * cs.mm, do * cs.mm , mdotxp, 4000, 2.0)
Pup = poiseuille_flow( Lc * cs.cm, dc * cs.cm , mdotxp, 4000, Pdown)

print Pup


# Create the pressure ratio
mdotxp = mdotxp * cs.sccm2eqA * 1e3 # mdot in mA-eq

poiseuille_ratio = Pup/(mdotxp) * do**2 
ratio = Pxp/(mdotxp) * do**2.

# Siegfried and Wilbur model
Idvec = np.arange(5.,15.,0.1)
rvec_sw = (9.0 + 4.0 * Idvec)*1e-3

# Our own fit
m,b = np.polyfit(Idxp,ratio,1)



plt.plot(Idxp,ratio,'k.',Idvec,m*Idvec + b,'k',Idvec,rvec_sw,'k--',Idxp,poiseuille_ratio,'k^')
plt.ylim([0.0,0.1])
plt.show()
#tikz_save('../../../../tikz/tmp.tex',figureheight='4in',figurewidth='3in')

