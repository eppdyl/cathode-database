# MIT License
# 
# Copyright (c) 2019-2020 Pierre-Yves Taunay 
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

''' 
File: derived_quantities.py
Author: Pierre-Yves Taunay
Date: 2019

This file contains functions to populate the database with the following 
derived quantities:
    1. Reynolds number, Knudsen number, entrance length
    2. Average insert wall temperature, if not specified
    3. Magnetic pressure, gasdynamic pressure, ionization pressure
    4. Total pressure in SI units
    5. Total pressure *if not specified* as calculated with an empirical
    correlation
    6. Speed of sound
    7. Pressure-diameter product
'''

import numpy as np
from scipy.optimize import root

import cathode.constants as cc
from cathode.models.flow import reynolds_number, viscosity
from lj_transport import transport_properties

from load_all_data import generate_dataframe
from compute_from_positional import compute_from_positional

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

def generate_dataframe_derived(empirical_pressure=False, pi_products=False):        
    # Load all of the data
    alldata = generate_dataframe()
    
    # Calculate quantities derived from the positional datas
    alldata = compute_from_positional(alldata)
    
    # Temperature data
    # Fill up AR3, EK6, SC012 by averaging AR3 and EK6
    bcond = (alldata.cathode=='AR3') | (alldata.cathode=='EK6')
    Tdf = np.array(alldata[bcond][['orificeTemperature']])
    Tave = np.nanmean(Tdf)
    
    bcondfill = (alldata.cathode=='AR3') | (alldata.cathode=='EK6') | (alldata.cathode=='SC012')
    alldata.loc[bcondfill,'insertTemperatureAverage'] = alldata.loc[bcondfill,'insertTemperatureAverage'].fillna(Tave)

    # NEXIS: use fit
    bcond = (alldata.cathode == 'NEXIS')
    Iddf = alldata[bcond]['dischargeCurrent']
    Tmax = 1370 + 3.971e-7 * Iddf ** 6 - 273.15
    alldata.loc[bcond,'insertTemperatureAverage'] = alldata.loc[bcond,'insertTemperatureAverage'].fillna(Tmax)
    
    # T6: use Richardson-Dushman law
    bcond = (alldata.cathode=='T6')
    phi_wf = lambda Tw: 1.67 + 2.87e-4 * Tw
    dc = np.unique(alldata[bcond].insertDiameter) * 1e-3
    fTw = lambda Id,Tw: Id - 120e6 * Tw**2 * np.exp(-cc.e * phi_wf(Tw) / (cc.Boltzmann * Tw)) * 2*np.pi * (dc/2) * 0.5 * dc
    for row in alldata[bcond].iterrows():
        Id = row[1]['dischargeCurrent']
        sol = root(lambda Tw: fTw(Id,Tw),1500)
        Temp = sol.x[0]-273.15
        alldata.loc[row[0],'insertTemperatureAverage'] = Temp


    # Salhi, Siegfried: average for a given geometry and gas
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
    

    ### Necessary constants    
    gam = 5/3
    
    constant_dict = {'pi':np.pi,
                     'q':cc.e,
                     'amu':cc.atomic_mass,
                     'gam':gam,
                     'kb':cc.Boltzmann,
                     'Torr':cc.Torr,
                     'mu0':cc.mu0}
    
    
    # Speed of sound
    sos_str = 'speedOfSound=(@gam*@kb/(gasMass*@amu)*(insertTemperatureAverage+273.15)*3)**(0.5)'
    alldata.eval(sos_str, local_dict=constant_dict, inplace=True)
    
    # Mass flow rate
    mdot_str = 'massFlowRate_SI = massFlowRate * gasMass * @amu / @q'
    alldata.eval(mdot_str, local_dict=constant_dict, inplace=True)
    
    ### Pressures
    # Use the empirical correlation if we want to add to the dataset 
    if empirical_pressure:
        print("YES")
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

    ### DERIVED QUANTITIES
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

    # Pressure diameter product
    pd_str = 'pressureDiameter = totalPressure * insertDiameter * 0.1'
    alldata.eval(pd_str, inplace=True)

    # Reynolds number
    alldata = df_reynolds_number(alldata)
        
    # Orifice entrance length
    entrance_str = 'entranceLength = 0.06 * reynoldsNumber * orificeDiameter / orificeLength'
    alldata.eval(entrance_str,inplace=True)
    
    # Orifice knudsen number
    knudsen_str = 'orificeKnudsenNumber = 1 / reynoldsNumber * (@gam * @pi/2)**(0.5)'
    alldata.eval(knudsen_str, local_dict=constant_dict, inplace=True)

    if pi_products:
        alldata = compute_pi_products(alldata)
    
    return alldata

def compute_pi_products(data):
    '''
    Calculate the Pi products that were defined in our 2018 JPC publication 
    Taunay, Wordingham, Choueiri, "An empirical scaling relationship for the
    total pressure in hollow cathodes," 2018, AIAA Propulsion and Energy Forum,
    AIAA-2018-4428
    '''
    gam = 5/3

    constant_dict = {'pi':np.pi,
                     'q':cc.e,
                     'amu':cc.atomic_mass,
                     'gam':gam,
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

    return data
