# MIT License
# 
# Copyright (c) 2020-2021 Pierre-Yves Taunay 
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


import numpy as np
from scipy.interpolate import splev,splrep
from scipy.optimize import root
import matplotlib.pyplot as plt

try:
    import cathode.constants as cc
    from cathode.models.flow import viscosity
except ImportError:
    ### Ad-hoc solution if we don't have the cathode package
    ### Just define the constants...
    class cc:
        class M:
            Ar = 39.948
            Xe = 131.293
            Hg = 200.59

        atomic_mass = 1.66053904e-27
        Boltzmann = 1.38064852e-23
        e = 1.6021766208e-19
        kB = 1.38064852e-23
        mu0 = 4 * np.pi * 1e-6
        sccm2eqA = 0.07174496294893724
        Torr = 133.32236842105263


    def viscosity(T,species='Xe-Goebel',units='poise', T_LJ=None, MU_LJ=None):
        """
        Calculates the gas species viscosity in poises given the temperature in 
        Kelvin and the species name.
        Inputs:
            temperature in Kelvin
        Optional Inputs:
            species - string with abbreviated identifier for each gas species
                -defaults to Goebel's Xe fit
            units - desired viscosity output unit
                -defaults to poise
        Output:
            viscosity in chosen unit (default poise)
            
        Refs:
            Goebel's 2008 Textbook for Xe-Goebel fit
            Stiel and Thodos 1961 for remaining gases
        """
        if species == 'Hg':
            mu = np.interp(T,T_LJ,MU_LJ)
            
            units_dict = {'poise' : 10.,
                          'centipoise' : 1000.0,
                          'Pa-s' : 1.0,
                          'kg/(m-s)' : 1.0}
    
            mu *= units_dict[units]
        else:
            #species dictionary: [Tc,upsilon]
            species_dict = {'Xe-Goebel' :   [289.7,None],
                            'Xe'        :   [289.8,0.0151],
                            'Ar'        :   [151.2,0.0276],
                            'Kr'        :   [209.4,0.0184],
                            'Ne'        :   [44.5,0.0466],
                            'N2'        :   [126.2,0.0407]}
            
            #unpack species data
            Tc, upsilon = species_dict[species]
            Tr = T/Tc
            
            #apply the appropriate fit equation
            if species == 'Xe-Goebel':
                zeta = 2.3E-4*Tr**(0.71+0.29/Tr)
            else:
                zeta = (17.78E-5*(4.58*Tr-1.67)**(5.0/8.0))/(upsilon*100.0)
                
            #convert to chosen units
            units_dict = {'poise' : 1.0,
                          'centipoise' : 100.0,
                          'Pa-s' : 0.1,
                          'kg/(m-s)' : 0.1}
    
            mu = zeta*units_dict[units]
        
        return mu

def pressure_empirical(Id, TgK, mdot_sccm, Locm, Mamu, eps, dccm, docm):
    
    if Mamu == 131.293:
        species = 'Xe'
    elif Mamu == 39.948:
        species = 'Ar'
    else:
        species = 'Hg'
        
    mu = viscosity(TgK,species=species,units='Pa-s')
    
    Pval = 2.47287280477684e-7   
    Pval *= Id**0.401051279571408 * Mamu**0.547870293394218 * TgK**0.365393042518454
    Pval *= mdot_sccm**0.683717435287032 * eps**0.298234175803028
    Pval /= Locm**0.233998925947759 * dccm ** 0.791908626218164 * docm ** 1.91389567576415
    Pval /= mu**0.412023151501404
    
    return Pval

def Lem(Ptorr,dccm,f):
    return f*dccm/2*(0.72389 + 0.17565 / (Ptorr*dccm)**1.22140)

def compute_erosion(dc0,dcmax,rho_emitter,evap,Id,TgK,mdot_sccm,Locm,Mamu,eps,docm,Lemitter,emitter,f=None):
    dc = dc0
    dt = 3600 # seconds
    ttotal = 0
    niter = 0
    m0 = np.pi/4 * ((dcmax*1e-2)**2 - (dc * 1e-2) ** 2) * (Lemitter * 1e-2) * rho_emitter # kg
    mn = m0
    
    print("Initial mass (mg):", m0 * 1e6)
    print("Time (hr), Insert diameter (cm), Mass lost (mg)")
    arr = []
    while dc < dcmax:
        Pn = pressure_empirical(Id,TgK,mdot_sccm,Locm,Mamu,eps,dc,docm) # Torr
#        Pd = Pn * dc # Torr-cm
        Lemn = Lem(Pn,dc,f) # cm      
        
        # Emission area
        A_em = np.pi * dc * Lemn # cm2
#        A_em = np.pi * dc * Lemitter
        
        # Current density in A/cm2
        Jd = Id / A_em # A/cm2
#        if niter < 10:
#            print(Jd,Id,dc,docm,Lemn)
            
        # Corresponding evaporation rate
        if emitter == 'LaB6':
            fRd = lambda Tw: 29 * Tw**2 * np.exp(-cc.e * 2.67 / (cc.Boltzmann * Tw))
            sol = root(lambda Tw:Jd-fRd(Tw),2000)
#            print(sol)
            
            if sol.success:
                Tw = sol.x[0]   
            else:
                print("Could not find solution")
                break
            
            evapn = 10**(13-36850/(Tw)) / np.sqrt(Tw) * 1e-3 * 1e4  # kg/m2/s


        else:
            evapn = splev(Jd,evap) * (1e-3) * (1e4) # kg/m2/s
            
#        print(Jd,evapn)
            

        
        dcn = (dc*1e-2)**2 + 4 * evapn * (dc * 1e-2) * dt / rho_emitter # in m2
        dcn = np.sqrt(dcn) # m
        dcn *= 1e2 # Back to cm
        
        dc = dcn
        
        ttotal += dt
        
        mn -= evapn * np.pi * (dc*1e-2) * (Lemn*1e-2) * dt
        
        niter = niter + 1
        
        if np.mod(niter,25000) == 0:
            print(ttotal/3600, dc, (m0-mn) * 1e6, evapn,Tw)
            
        arr.append([ttotal,dc,(m0-mn)*1e6])
    print("Total time (hours, kh): ", ttotal / 3600, ttotal / (1e3*3600))
        
    return arr
            
        
    
    
        

data_bao = np.genfromtxt("emitter-evaporation-data/evaporation-bao.csv",
                         delimiter=',',
                         skip_header=1,
                         names=True)

data_lab6 = np.genfromtxt("emitter-evaporation-data/evaporation-lab6.csv",
                         delimiter=',',
                         skip_header=1,
                         names=True)

evap_bao = splrep(data_bao['Jd'],data_bao['epsilon'])
evap_lab6 = splrep(data_lab6['Jd'],data_lab6['epsilon'])

rho_lab6 = 4.72 * 1e3
rho_bao = 5.72 * 1e3


#### CONSIDER TH15 FOR NSTAR
##Id = 15 
##mdot_sccm = 3.7
##dc0 = 3.8 * 0.1 # cm
##dcmax = 4.3 * 0.1 # cm
##TgK = 3000 # K
##Locm = 0.74 * 0.1 # cm
##docm = 1.02 * 0.1 # cm
##Mamu = 131.293
##eps = 12.1298
##Lemitter = 2.54
##
##arr = compute_erosion(dc0,dcmax,rho_bao,evap_bao,Id,TgK,mdot_sccm,Locm,Mamu,eps,docm,Lemitter,'BaO')
#
#
#### CONSIDER LAB6 1.5 CM
#Id = 25 
#mdot_sccm = 13
#dc0 = 0.7 # cm
#dcmax = 1.2 # cm
#TgK = 3000 # K
#Locm = 1.0 * 0.1 # cm
#docm = 3.0 * 0.1 # cm
#Mamu = 131.293
#eps = 12.1298
#Lemitter = 2.54
#Lem_fac = 1.0
#
#arr = compute_erosion(dc0,dcmax,rho_lab6,evap_lab6,Id,TgK,mdot_sccm,Locm,Mamu,eps,docm,Lemitter,'LaB6',Lem_fac)
#arr = np.array(arr)
##    ttot = arr[:,0][-1] / (3.6e3*1e3)
##    ttotal[idx] = ttot 
#
##Larr = np.linspace(1,3,15)
##ttotal = np.zeros_like(Larr)
##for idx,Lem_fac in enumerate(Larr):
##    arr = compute_erosion(dc0,dcmax,rho_lab6,evap_lab6,Id,TgK,mdot_sccm,Locm,Mamu,eps,docm,Lemitter,'LaB6',Lem_fac)
##    arr = np.array(arr)
##    ttot = arr[:,0][-1] / (3.6e3*1e3)
##    ttotal[idx] = ttot 
##    
##arr = np.array(arr)
#plt.plot(arr[::10,0]/3600*1e-3,arr[::10,2],'k-')
##
###plt.plot([0,2,4,10],[0,152,302,700])
#plt.plot([2,4],[152,302],'ko')
#plt.xlabel('Time (kh)')
#plt.ylabel('Mass loss (mg)')



#fig, ax = plt.subplots()
#
#ax.set_xlabel('Time (kh)')
#ax.set_ylabel('Mass loss (mg)')
#ax.plot(arr[:,0]/3600*1e-3,arr[:,2],color='tab:orange')
#plt.plot([2,4],[152,302],'o',color='tab:orange')
#ax.tick_params(axis='y',labelcolor='tab:orange')

#ax2 = ax.twinx()  # instantiate a second axes that shares the same x-axis
#
#ax2.set_ylabel('Thickness eroded (%)')  # we already handled the x-label with ax1
#ax2.plot(arr[:,0]/3600*1e-3, (arr[:,1]-dc0) / (dcmax-dc0) * 100,color='tab:blue')
#ax2.tick_params(axis='y', labelcolor='tab:blue')
#


### CONSIDER PLHC
#Id = 200
#mdot_sccm = 100
#dc0 = 2.715 # cm
#dcmax = 3.26 # cm
#TgK = 2000 # K
#Locm = 0.15 # cm
#docm = 0.56 # cm
#Mamu = 39.948
#eps = 15.75962
#Lemitter = 8.04 # cm
#Lem_fac = 1.0
#
#arr = compute_erosion(dc0,dcmax,rho_lab6,evap_lab6,Id,TgK,mdot_sccm,Locm,Mamu,eps,docm,Lemitter,'LaB6',Lem_fac)

## CONSIDER NOMINAL LAB6
Id = 25
mdot_sccm = 10
TgK = 3000 # K
Locm = 1.0 * 0.1 # cm
docm = 2.0 * 0.1 # cm

rbar = 0.1
dc0 = 1.0 # cm
dcmax = 1.05 * dc0

Mamu = 131.293
eps = 12.1298
Lemitter = 2.54
Lem_fac = 1.0

# Keep mass constant
Vtotal = np.pi /4 *( dcmax**2 - dc0**2) * Lemitter # m3
mass = Vtotal * rho_lab6

rbarr = np.linspace(0.01,0.3,20)
ttotal = np.zeros_like(rbarr)

for idx,rbar in enumerate(rbarr):
    docm = rbar * dc0
    
    arr = compute_erosion(dc0,dcmax,rho_lab6,evap_lab6,Id,TgK,mdot_sccm,Locm,Mamu,eps,docm,Lemitter,'LaB6',Lem_fac)
    arr = np.array(arr)
    
    ttot = arr[:,0][-1] / (3600*1e3)
    ttotal[idx] = ttot
    
plt.plot(rbarr,ttotal / ttotal[0],'k-')
plt.xlabel("rbar")
plt.ylabel("Lifetime (a.u.)")
##plt.plot(rbarr,7.24730039*rbarr**2 -1.17789696*rbarr + 1.04553994)
##plt.plot(rbarr,9.19973986*rbarr**3 +  0.2094994*rbarr**2 +  0.21723905*rbarr + 0.99486893)
##plt.plot(rbarr, 17.61513503*rbarr**5 -13.273627*rbarr**4 + 9.93571707*rbarr**3 + 1.34617392*rbarr**2 + 0.02150109*rbarr**1+ 0.9996931)
#
#
mdotarr = np.arange(5,20,1,dtype=np.float64)
ttotal = np.zeros_like(mdotarr)
rbar = 0.2
for idx,mdot_sccm in enumerate(mdotarr):
    docm = rbar * dc0
    
    print(mdot_sccm,pressure_empirical(Id,TgK,mdot_sccm,Locm,Mamu,eps,dc0,docm) * dc0)

    arr = compute_erosion(dc0,dcmax,rho_lab6,evap_lab6,Id,TgK,mdot_sccm,Locm,Mamu,eps,docm,Lemitter,'LaB6',Lem_fac)
    arr = np.array(arr)
    
    ttot = arr[:,0][-1] / (3.6e3*1e3)
    ttotal[idx] = ttot
    
    
#    plt.plot(arr[::10,0]/3600*1e-3,arr[::10,2],'-')
#    plt.xlabel('Time (kh)')
#    plt.ylabel('Mass loss (mg)')

plt.figure()
plt.plot(mdotarr*cc.sccm2eqA/Id, ttotal / ttotal[0],'k-')
plt.xlabel("mdot/Id")
plt.ylabel("Time (kh)")


Idarr = np.arange(10,30,1,dtype=np.float64)
ttotal = np.zeros_like(Idarr)
mdot_sccm = 10
rbar = 0.1
for idx,Id in enumerate(Idarr):
    docm = rbar * dc0
    
#    print(mdot_sccm,pressure_empirical(Id,TgK,mdot_sccm,Locm,Mamu,eps,dc0,docm) * dc0)

    arr = compute_erosion(dc0,dcmax,rho_lab6,evap_lab6,Id,TgK,mdot_sccm,Locm,Mamu,eps,docm,Lemitter,'LaB6',Lem_fac)
    arr = np.array(arr)
    
    ttot = arr[:,0][-1] / (3.6e3*1e3)
    ttotal[idx] = ttot

plt.figure()
plt.plot(Idarr / (mdot_sccm * cc.sccm2eqA),ttotal / ttotal[0],'k-')
plt.xlabel("Id")
plt.ylabel("Time (kh)")


#Idnom = 25
#mdotnom = 10
#rbarr = np.linspace(0.1,0.3,11) # rbar
#ratarr = np.logspace(-2,-0.5,10) # mdot/Id
#
#V = np.zeros((len(rbarr),len(ratarr)))
#
#for ii, rbar in enumerate(rbarr):
#    docm = rbar * dc0
#    for jj, rat in enumerate(ratarr):
##        mdot_eqA = rat * Idnom
##        mdot_sccm = mdot_eqA/cc.sccm2eqA
#        
#        Id = mdotnom / rat
#                
#        arr = compute_erosion(dc0,dcmax,rho_lab6,evap_lab6,Id,TgK,mdotnom,Locm,Mamu,eps,docm,Lemitter,'LaB6',Lem_fac)
#        arr = np.array(arr) 
#        ttot = arr[:,0][-1] / (3.6e3*1e3)
#        
#        V[ii,jj] = ttot
#        
#        
#plt.contourf(ratarr,rbarr,V/np.max(V),levels=np.linspace(0.4,1,20))
#plt.xlabel("mdot/Id")
#plt.ylabel("rbar")
#plt.colorbar()
#plt.xscale("log")


#
##Idnom = 25
##mdotnom = 10
#Idvec = np.linspace(5,25,10) # rbar
#mdotvec = np.linspace(4,30,11) # mdot/Id
#
#V = np.zeros((len(Idvec),len(mdotvec)))
#
#rbar = 0.1
#for ii, Id in enumerate(Idvec):
#    docm = rbar * dc0
#    for jj, mdot_sccm in enumerate(mdotvec):
##        mdot_eqA = rat * Idnom
##        mdot_sccm = mdot_eqA/cc.sccm2eqA
#        
#        arr = compute_erosion(dc0,dcmax,rho_lab6,evap_lab6,Id,TgK,mdot_sccm,Locm,Mamu,eps,docm,Lemitter,'LaB6',Lem_fac)
#        arr = np.array(arr) 
#        ttot = arr[:,0][-1] / (3.6e3*1e3)
#        
#        V[ii,jj] = ttot
#        
#        
#plt.contourf(mdotvec,Idvec,V/np.max(V),levels=np.linspace(0.4,1,20))
#plt.xlabel("mdot/Id")
#plt.ylabel("rbar")
#plt.colorbar()
#plt.xscale("log")
