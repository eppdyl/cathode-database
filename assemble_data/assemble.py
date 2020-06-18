import pandas as pd
import numpy as np
from scipy.optimize import root

import cathode.constants as cc
from cathode.models.flow import reynolds_number, viscosity
from lj_transport import transport_properties

from import_db import dtypes
from populate_positional_data import populate_NEXIS, populate_NSTAR, populate_JPL_lab6, populate_Salhi
from populate_PLHC import append_PLHC
from populate_positional_data import populate_Siegfried_ng

from load_all_data import generate_dataframe


def df_reynolds_number(alldata):
    gam = 5/3    
    Tvec = np.arange(300,4001,10)

    ### Hg data
    sig_lj_hg = 2.898e-10
    kbeps_hg = 851.    
    mu_hg = transport_properties(sig_lj_hg,kbeps_hg,cc.M.Hg,Tvec)
    
    ### Orifice Reynolds number
    alldata.loc[alldata['gas'] == 'Xe', 'reynoldsNumber'] = reynolds_number(alldata['massFlowRate_SI'],alldata['orificeDiameter']*1e-3,(alldata['insertTemperatureAverage']+273.15)*3,'Xe')
    alldata.loc[alldata['gas'] == 'Ar', 'reynoldsNumber'] = reynolds_number(alldata['massFlowRate_SI'],alldata['orificeDiameter']*1e-3,(alldata['insertTemperatureAverage']+273.15)*3,'Ar')
    alldata.loc[alldata['gas'] == 'Hg', 'reynoldsNumber'] = reynolds_number(alldata['massFlowRate_SI'],alldata['orificeDiameter']*1e-3,(alldata['insertTemperatureAverage']+273.15)*3,'Hg',Tvec,mu_hg)

    ### Insert Reynolds number
    alldata.loc[alldata['gas'] == 'Xe', 'reynoldsNumberInsert'] = reynolds_number(alldata['massFlowRate_SI'],alldata['insertDiameter']*1e-3,(alldata['insertTemperatureAverage']+273.15)*3 * (gam+1)/2,'Xe')
    alldata.loc[alldata['gas'] == 'Ar', 'reynoldsNumberInsert'] = reynolds_number(alldata['massFlowRate_SI'],alldata['insertDiameter']*1e-3,(alldata['insertTemperatureAverage']+273.15)*3 * (gam+1)/2,'Ar')
    alldata.loc[alldata['gas'] == 'Hg', 'reynoldsNumberInsert'] = reynolds_number(alldata['massFlowRate_SI'],alldata['insertDiameter']*1e-3,(alldata['insertTemperatureAverage']+273.15)*3 * (gam+1)/2,'Hg',Tvec,mu_hg)

    return alldata

def assemble(empirical_pressure=False):        
    # Load all of the data
    alldata = generate_dataframe()

    ### DENSITY AND TEMPERATURE DATA
    alldata = populate_NSTAR(alldata)
    alldata = populate_NEXIS(alldata)
    alldata = populate_JPL_lab6(alldata)
    alldata = populate_Salhi(alldata)
    alldata = populate_Siegfried_ng(alldata)
    
    # Correct NEXIS cases
    alldata.loc[366,'orificeDiameter'] = 3.0 
    alldata.loc[367,'orificeDiameter'] = 2.75
    
    ### ADD THE DATA FOR THE PLHC
    alldata = append_PLHC(alldata)
    
    # Fill up AR3, EK6, SC012 by averaging AR3 and EK6
    bcond = (alldata.cathode=='AR3') | (alldata.cathode=='EK6')
    Tdf = np.array(alldata[bcond][['insertTemperatureAverage']])
    Tave = np.nanmean(Tdf)
    
    bcondfill = (alldata.cathode=='AR3') | (alldata.cathode=='EK6') | (alldata.cathode=='SC012')
    alldata.loc[bcondfill,'insertTemperatureAverage'] = alldata.loc[bcondfill,'insertTemperatureAverage'].fillna(Tave)

    # NEXIS
    bcond = (alldata.cathode == 'NEXIS')
    Iddf = alldata[bcond]['dischargeCurrent']
    Tmax = 1370 + 3.971e-7 * Iddf ** 6 - 273.15
    alldata.loc[bcond,'insertTemperatureAverage'] = alldata.loc[bcond,'insertTemperatureAverage'].fillna(Tmax)
    
    # T6: use the same values as NSTAR
#    Iddf = alldata[bcond]['dischargeCurrent']
#    Tmax = 1191.6 * Iddf ** 0.0988 - 273.15
#    alldata.loc[bcond,'insertTemperatureAverage'] = Tmax
    bcond = (alldata.cathode=='T6')
    phi_wf = lambda Tw: 1.67 + 2.87e-4 * Tw
    dc = np.unique(alldata[bcond].insertDiameter) * 1e-3
    fTw = lambda Id,Tw: Id - 120e6 * Tw**2 * np.exp(-cc.e * phi_wf(Tw) / (cc.Boltzmann * Tw)) * 2*np.pi * (dc/2) * 0.5 * dc
    for row in alldata[bcond].iterrows():
        Id = row[1]['dischargeCurrent']
        sol = root(lambda Tw: fTw(Id,Tw),1500)
        Temp = sol.x[0]-273.15
        alldata.loc[row[0],'insertTemperatureAverage'] = Temp


    # Salhi, T6: average for a given geometry and gas
    for name in ['Salhi-Ar-0.76','Salhi-Ar-1.21','Salhi-Xe','Siegfried-NG']:
        bcond = (alldata.cathode == name)
        
        if name == 'Siegfried-NG':
            bcond &= (alldata.gas == 'Xe')
        Tdf = np.array(alldata[bcond][['insertTemperatureAverage']])
        Tave = np.nanmean(Tdf)
        
        
        alldata.loc[bcond,'insertTemperatureAverage'] = alldata.loc[bcond,'insertTemperatureAverage'].fillna(Tave)
        
    # JPL 1.5 cm: fit to orifice plate temperature
    for name in ['JPL-1.5cm','JPL-1.5cm-3mm','JPL-1.5cm-5mm']:
        bcond = (alldata.cathode == name)
        Iddf = alldata[bcond]['dischargeCurrent']
        Tmax = 1144 + 5.56 * Iddf
        alldata.loc[bcond,'insertTemperatureAverage'] = alldata.loc[bcond,'insertTemperatureAverage'].fillna(Tmax)
    
    # PLHC: assume Lem ~ 0.5 dc, and compute the temperature from R-D
    bcond = (alldata.cathode=='PLHC')
    phi_wf = 2.67
    dc = np.unique(alldata[bcond].insertDiameter) * 1e-3
    fTw = lambda Id,Tw: Id - 29e6 * Tw**2 * np.exp(-cc.e * phi_wf / (cc.Boltzmann * Tw)) * 2*np.pi * (dc/2) * 0.5 * dc
    for row in alldata[bcond].iterrows():
        Id = row[1]['dischargeCurrent']
        sol = root(lambda Tw: fTw(Id,Tw),1500)
        Temp = sol.x[0]-273.15
        alldata.loc[row[0],'insertTemperatureAverage'] = Temp
    
    ### PRESSURE DIAMETER PRODUCT
    pd_str = 'pressureDiameter = totalPressure * insertDiameter * 0.1'
    alldata.eval(pd_str, inplace=True)

    ### CHANGE TO SI UNITS
    # Gamma
    gam = 5/3
    
    constant_dict = {'pi':np.pi,
                     'q':cc.e,
                     'amu':cc.atomic_mass,
                     'gam':gam,
                     'kb':cc.Boltzmann,
                     'Torr':cc.Torr,
                     'mu0':cc.mu0}
    
    ### Necessary constants    
    # Speed of sound
    sos_str = 'speedOfSound=(@gam*@kb/(gasMass*@amu)*(insertTemperatureAverage+273.15)*3)**(0.5)'
    alldata.eval(sos_str, local_dict=constant_dict, inplace=True)
    
    # Mass flow rate
    mdot_str = 'massFlowRate_SI = massFlowRate * gasMass * @amu / @q'
    alldata.eval(mdot_str, local_dict=constant_dict, inplace=True)
    
    ### Pressures
    # Use the empirical correlation if we want to add to the dataset 
    if empirical_pressure:
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
            
        for row in alldata.iterrows():
            if np.isnan(row[1]['totalPressure']):
                TwC = row[1]['insertTemperatureAverage']
                Id = row[1]['dischargeCurrent']
                TgK = (TwC + 273.15) * 3
                Locm = row[1]['orificeLength'] * 0.1
                docm = row[1]['orificeDiameter'] * 0.1
                dccm = row[1]['insertDiameter'] * 0.1
                Mamu = row[1]['gasMass']
                eps = row[1]['ionizationPotential']
                mdot_sccm = row[1]['massFlowRate'] / cc.sccm2eqA
                
                P = pressure_empirical(Id, TgK, mdot_sccm, Locm, Mamu, eps, dccm, docm)
                
                alldata.loc[row[0],'totalPressure'] = P

    # Total pressure
    p_str = 'totalPressure_SI=totalPressure*@Torr'
    alldata.eval(p_str, local_dict=constant_dict, inplace=True)
        
    # Magnetic pressure
    pmag_str = 'magneticPressure=@mu0*dischargeCurrent**2 / (@pi**2*(orificeDiameter*1e-3)**2)'
    alldata.eval(pmag_str, local_dict=constant_dict, inplace=True)
    
    # Gasdynamic  pressure
    pgd_str = 'gdPressure = 4/@pi * massFlowRate_SI * speedOfSound / (orificeDiameter*1e-3)**2'
    alldata.eval(pgd_str, local_dict=constant_dict, inplace=True)
    
    # Ionization pressure
    piz_str = 'izPressure = 4/@pi * @q * ionizationPotential / ( (orificeDiameter * 1e-3)**2 * orificeLength * 1e-3)'
    alldata.eval(piz_str, local_dict=constant_dict, inplace=True)

    # Ratio of total pressure to magnetic pressure (includes the log term)
    rat_str = 'totalToMagnetic = totalPressure_SI / magneticPressure * 1/(1/4 + log(insertDiameter/orificeDiameter))'
    alldata.eval(rat_str, local_dict=constant_dict, inplace=True)
    
    # Ratio of Id over mdot
    rat_str = 'IdToMdot = dischargeCurrent / massFlowRate'
    alldata.eval(rat_str, local_dict=constant_dict, inplace=True)

    ### COMPUTE REYNOLDS NUMBER
    alldata = df_reynolds_number(alldata)
        
    # Orifice entrance length
    entrance_str = 'entranceLength = 0.06 * reynoldsNumber * orificeDiameter / orificeLength'
    alldata.eval(entrance_str,inplace=True)
    
    # Orifice Knudsen number
    knudsen_str = 'orificeKnudsenNumber = 1 / reynoldsNumber * (@gam * @pi/2)**(0.5)'
    alldata.eval(knudsen_str, local_dict=constant_dict, inplace=True)
    
    return alldata
