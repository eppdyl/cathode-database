import cathode.constants as cc
import cathode.collisions.cross_section as cx
import cathode.collisions.reaction_rate as ccr
from cathode.math.bisect_next import bisect_next
import numpy as np

from scipy.special import jn_zeros,j0,j1
from scipy.optimize import root

l01 = jn_zeros(0,1)

def TeV(Pd,species):
    if species == 'Xe':
        return 0.52523 + 1.20072 / (Pd)**0.35592
    elif species == 'Ar':
        return 0.945 + 1.91 / (Pd)**0.341


def goal_function(logPd,M,TnK,rr_iz,scex,species):
    Pd = 10**logPd
    lTe = TeV(Pd,species)
#    lTe = Te
    
    TnV = TnK * cc.Kelvin2eV
    vn = np.sqrt(cc.e * TnV/M)
    
    rhs = cc.e / M * (TnV + lTe) / (scex*vn) 
    
    lhs = (1/(2*l01) * (cc.Torr / 100) * Pd / (cc.Boltzmann * TnK))**2 * rr_iz(lTe) 
    
    return (lhs/rhs - 1)

def goal_function_alt(logPd,M,TnK,rr_iz,scex,species):
    
    Pd = 10**logPd
#    print(Pd)
#    Pd = logPd
    lTe = TeV(Pd,species)
#    lTe = Te
    
    TnV = TnK * cc.Kelvin2eV
    vn = np.sqrt(cc.e * TnV/M)
    
    rhs = cc.e / M * (TnV + lTe) / (scex*vn) 
    
    lhs = (1/2*(cc.Torr / 100) * Pd / (cc.Boltzmann * TnK))**2 * rr_iz(lTe) 
    
    gam = lhs / rhs
    
    vb = np.sqrt(cc.e * lTe/M)
    lhs = vb * (1/2*(cc.Torr / 100) * Pd / (cc.Boltzmann * TnK))
    
    delta = lhs/rhs
    
        
    return -gam * j1(gam) + delta * j0(gam)

for species in ['Ar']:
    if species == 'Ar':
        M = cc.M.Ar * cc.atomic_mass
        fname = 'ar_all.dat'
        
    elif species == 'Xe':
        M = cc.M.Xe * cc.atomic_mass
        fname = 'xe_all.dat'
        
    spliz = cx.create_cross_section_spline(fname,'ionization')
    
    rr_iz = lambda Te: ccr.reaction_rate(spliz,Te)
    
#    print("Tn (K), Pd (Torr-cm), Te (eV), goal_function")
    Tnarray = np.linspace(2000,4000)
    Pdsol = np.zeros_like(Tnarray)
#    for TnK in np.array([2000.,3000.,4000.]):
    for idx,TnK in enumerate(Tnarray):
        scex = cx.charge_exchange(TnK*cc.Kelvin2eV,species)
        
#        sol = root(lambda Pd:goal_function_alt(Pd,M,TnK,rr_iz,scex),5.0,method='lm')
        gen = bisect_next(lambda Pd:goal_function_alt(Pd,M,TnK,rr_iz,scex,species),-2.,2.,min_spacing=1e-2)
        
#        ng = 7.5 * cc.Torr / (cc.Boltzmann * TnK)
#        TnV = TnK * cc.Kelvin2eV
#        vn = np.sqrt(cc.e * TnV/M)
#        
#        
#        rhs = lambda Te: cc.e / M * (TnV + Te) / (scex*vn) 
#        lhs = lambda Te: (0.36 * 1e-2 * ng/l01)**2 * rr_iz(Te)
#        sol = root(lambda Te:lhs(Te)/rhs(Te)-1,5.0)
        try:
            sol =  next(gen)
#            print(TnK,10**sol[0],TeV(10**sol[0]),goal_function_alt(sol[0],M,TnK,rr_iz,scex))
            Pdsol[idx] = 10**sol[0]
        except:
#            print(TnK,"No solution")
            Pdsol[idx] = 1e-4
#        print(TnK,sol.x[0],TeV(sol.x[0]),goal_function_alt(sol.x[0],M,TnK,rr_iz,scex))