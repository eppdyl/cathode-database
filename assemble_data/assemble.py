import pandas as pd
import numpy as np
from scipy.interpolate import splrep,splev
import math

from cathode.experimental.load_data import load_all_data
import cathode.experimental.files as cef
import cathode.constants as cc
from cathode.models.flow import reynolds_number

from import_db import dtypes
from populate_positional_data import populate_NEXIS, populate_NSTAR, populate_JPL_lab6, populate_Salhi
from populate_PLHC import append_PLHC
from populate_positional_data import populate_Siegfried_ng

def df_reynolds_number(alldata):
    ### Hg viscosity
    collision_file = cef.__path__[0] + '/collision-integrals-lj.csv'
    data = np.genfromtxt(collision_file,delimiter=',',names=True)
    
    MHg = cc.M.species('Hg')
    
    Tlj = data['Tstar']
    omega22_data = splrep(Tlj,data['omega22'])
    omega23_data = splrep(Tlj,data['omega23'])
    omega24_data = splrep(Tlj,data['omega24'])
    
    Tvec = np.arange(300,4001,10)
    
    sig_lj = 2.898e-10
    omega_hs = lambda l,s:  math.factorial(s+1)/2. * (1. - 1./2.*(1. + (-1)**l)/(1.+l))*np.pi*sig_lj**2
    omega_hs22 = omega_hs(2,2)
    omega_hs23 = omega_hs(2,3)
    omega_hs24 = omega_hs(2,4)
    #np.sqrt(cs.Boltzmann*Tvec/(pi*MXe)) *
    
    kbeps = 851.
    
    omega22 = np.sqrt(cc.Boltzmann*Tvec/(np.pi*MHg))*splev(Tvec/kbeps,omega22_data) * omega_hs22
    omega23 = np.sqrt(cc.Boltzmann*Tvec/(np.pi*MHg))*splev(Tvec/kbeps,omega23_data) * omega_hs23
    omega24 = np.sqrt(cc.Boltzmann*Tvec/(np.pi*MHg))*splev(Tvec/kbeps,omega24_data) * omega_hs24
    
    b11 = 4.* omega22
    b12 = 7.*omega22 - 2*omega23
    b22 = 301./12.*omega22 - 7*omega23 + omega24
    
    mu_lj = 5.*cc.Boltzmann*Tvec/2.*(1./b11 + b12**2./b11 * 1./(b11*b22-b12**2.))    
    
#    re_str = 'reynoldsNumber = @reynolds_number(massFlowRate_SI,orificeDiameter*1e-3,insertTemperatureAverage*3,gas)'
#    alldata.eval(re_str, local_dict={'reynolds_number':reynolds_number}, inplace=True)  
    alldata.loc[alldata['gas'] == 'Xe', 'reynoldsNumber'] = reynolds_number(alldata['massFlowRate_SI'],alldata['orificeDiameter']*1e-3,(alldata['insertTemperatureAverage']+273.15)*3,'Xe')
    alldata.loc[alldata['gas'] == 'Ar', 'reynoldsNumber'] = reynolds_number(alldata['massFlowRate_SI'],alldata['orificeDiameter']*1e-3,(alldata['insertTemperatureAverage']+273.15)*3,'Ar')
    alldata.loc[alldata['gas'] == 'Hg', 'reynoldsNumber'] = reynolds_number(alldata['massFlowRate_SI'],alldata['orificeDiameter']*1e-3,(alldata['insertTemperatureAverage']+273.15)*3,'Hg',Tvec,mu_lj)

    return alldata

def assign_geometry(idx):
    if idx == 'NSTAR':
        # Length before actual pressure measurement and emitter length
        # See Mikellides, Physics of Plasmas, 2009, p. 013501-7
        Lupstream = 130. 
        Lemitter = 25.4        
    elif idx == 'NEXIS':
        Lupstream = 120. # Length before actual pressure measurement
        Lemitter = 25.4
    elif idx == 'Salhi-Xe' or idx == 'Salhi-Ar-1.21' or idx == 'Salhi-Ar-0.76':
        Lupstream = 130. # Not sure what the upstream length is. Set to same as NSTAR / NEXIS
        Lemitter = 25.4 # 1 in emitter
    elif idx == 'AR3' or idx == 'EK6' or idx == 'SC012':
        Lemitter = 25.4
        Lupstream = 500. # Length before actual pressure measurement
        # See Domonkos dissertation
        # "0.5-m upstream of the cathode insert" p.26
    elif idx == 'Siegfried':
        Lemitter = 25.4
        Lupstream = np.nan
    elif idx == 'T6':
        Lemitter = 25.4
        Lupstream = np.nan
    elif idx == 'Friedly':
        Lemitter = 25.4
        Lupstream = 120. # Length before actual pressure measurement
        
    return Lemitter,Lupstream

def assemble():        
    # Load all of the data
    pdf = load_all_data()
    
    # Empty dataframe
    data = np.empty(0, dtype=dtypes)
    alldata = pd.DataFrame(data)
    
    ### Fill dataframe with pressure data
    first = True
    for idx in pdf.index:
        Idvec  = pdf.Id[idx]
        mdotvec = pdf.mdot[idx]
        Pvec  = pdf.P[idx]
        dovec = pdf.do[idx]
        Lovec = pdf.Lo[idx]
       
        Twvec = pdf.Tw[idx]
        Tovec = pdf.To[idx]
        dcvec = pdf.dc[idx]
        
        eizvec = pdf.eiz[idx]
        
        Twvec[Twvec == 1000.] = np.nan
        
        length = len(Idvec)
    
        # Type of cathode?
        xecathodes = (idx == 'NSTAR' or 
                       idx =='NEXIS' or 
                       idx == 'Salhi-Xe' or 
                       idx == 'AR3' or
                       idx == 'EK6' or
                       idx == 'SC012' or
                       idx == 'Friedly' or
                       idx == 'T6')
        
        hgcathode = (idx == 'Siegfried')
    
        # If this is the first index, directly populate the dataframe
        if first == True:
            
            alldata['dischargeCurrent'] = Idvec
            alldata['massFlowRate'] = mdotvec
            if xecathodes:
                alldata['gas'] = 'Xe'
            elif hgcathode:
                alldata['gas'] = 'Hg'
            else:
                alldata['gas'] = 'Ar'
            
            alldata['orificeDiameter'] = dovec
            alldata['orificeLength'] = Lovec
            alldata['insertDiameter'] = dcvec
            alldata['insertTemperatureAverage'] = Twvec
            
            Lemitter, Lupstream = assign_geometry(idx)
            
            alldata['insertLength'] = Lemitter
            alldata['upstreamPressurePoint'] = Lupstream
            
            
            alldata['totalPressure'] = Pvec
            alldata['orificeTemperature'] = Tovec
            
            alldata['ionizationPotential'] = eizvec
            
            alldata['cathode'] = idx
            
            first = False
            
        # Otherwise, create temporary dataframe to append
        else:
            tmp = pd.DataFrame(data)
            
            tmp['dischargeCurrent'] = Idvec
            tmp['massFlowRate'] = mdotvec
            tmp['totalPressure'] = Pvec
            tmp['orificeDiameter'] = dovec
            tmp['orificeLength'] = Lovec
            tmp['orificeTemperature'] = Tovec
            tmp['insertDiameter'] = dcvec    
            tmp['insertTemperatureAverage'] = Twvec
            tmp['ionizationPotential'] = eizvec
            
            if xecathodes:
                tmp['gas'] = 'Xe'
            elif hgcathode:
                tmp['gas'] = 'Hg'
            else:
                tmp['gas'] = 'Ar'
    
            Lemitter, Lupstream = assign_geometry(idx)
            
            tmp['insertLength'] = Lemitter
            tmp['upstreamPressurePoint'] = Lupstream
            
            tmp['cathode'] = idx
            
    
            
            alldata = alldata.append(tmp,ignore_index=True)
    
    ### Populate references
    # NSTAR
    NSTAR_ref = [("K. K. Jameson, D. M. Goebel, and R. M. Watkins,"
                 "Hollow Cathode and Keeper-Region Plasma Measurements," 
                 "41st JPC, 2005."),
                 ("I. G. Mikellides, \"Effects of viscosity in a partially ionized " 
                 "channel flow with thermionic emission,\" Phys. Plasmas, vol. 16, " 
                 "no. 1, 2009."),
                 ("J. Polk, A. Grubisic, N. Taheri, D. Goebel, R. Downey, and " 
                 "S. E. Hornbeck, \"Emitter Temperature Distributions in the NSTAR " 
                 "Discharge Hollow Cathode,\" 41st JPC, 2005.")]   
    NSTAR_notes = [("Fig 3 - Pressure measured inside the 1/4\" hollow cathode " 
                   "for various NSTAR throttle levels. "
                   "Fig 4 - Axial density cathode and anode profiles plotted "
                   "on a semi-log scale for TH8 and TH15. "
                   "Fig 6 - Cathode plasma potential and electron temperature "
                   "profiles for TH8 and TH15. The throttle levels TH4, " 
                   "TH8, TH15 are from: V. Rawlin, J. Sovey, J. Anderson, and " 
                   "J. Polk, \"NSTAR flight thruster qualification testing, " 
                   "34th AIAA/ASME/SAE/ASEE JPC, 1998. "
                   "TH12: W. G. Tighe, K. Chien, D. M. Goebel, and R. T. Longo, " 
                   "\"Hollow Cathode Ignition and Life Model,\" 41st JPC, 2005. "
                   "Tw is calculated with Polk's fit"),
                   ("Fig. 10 - Comparisons between measured and computed " 
                   "values of the cathode gas pressure. "
                   "Tw is calculated with Polk's fit"),
                   ("Fig.4 - Comparison of temperatures from the NSTAR cathode " 
                   "and the plasma contactor. "
                   "Fig.8 - Internal hollow cathode pressure increases with flow"
                   "rate and discharge current")]
              
    alldata.loc[0:3,'reference'] = NSTAR_ref[0]
    alldata.loc[0:3,'note'] = NSTAR_notes[0]
    alldata.loc[4:24,'reference'] = NSTAR_ref[1]
    alldata.loc[4:24,'note'] = NSTAR_notes[1]
    alldata.loc[25:42,'reference'] = NSTAR_ref[2]
    alldata.loc[25:42,'note'] = NSTAR_notes[2]
    
    # NEXIS
    NEXIS_ref = [("K. K. Jameson, D. M. Goebel, and R. M. Watkins, \"Hollow Cathode " 
    "and Thruster Discharge Chamber Plasma Measurements Using "
    "High-Speed Scanning Probes,\" 29th International Electric Propulsion Conference, 2005."),
    ("D. Goebel, K. K. Jameson, R. M. Watkins, and I. Katz, "
    "\"Hollow Cathode and Keeper-Region Plasma Measurements Using Ultra-Fast Miniature Scanning Probes,\" "
    "40th JPC, 2004.")]
    NEXIS_notes = [("Fig. 7 - Internal NEXIS cathode pressure (a) constant flow "
                   "rate at 5.5 sccm (b) constant discharge current at 22 A."),
                   ("Fig. 8 - Pressure measured and calculated inside the hollow "
                   "cathode without plasma (a) and with plasma (b)")]
    
    alldata.loc[43:56,'reference'] = NEXIS_ref[0]
    alldata.loc[43:56,'note'] = NEXIS_notes[0]
    alldata.loc[57:63,'reference'] = NEXIS_ref[1]
    alldata.loc[57:63,'note'] = NEXIS_notes[1]
    
    alldata.loc[57:63,'orificeDiameter'] = 2.75 # 2.75 mm explicitely
    alldata.loc[43:56,'orificeDiameter'] = 2.5 # "Between 2 and 3 mm"
    
    # Salhi
    Salhi_ref = ("A. Salhi, \"Theoretical and experimental studies of orificed, " 
    "hollow cathode operation,\" The Ohio State University, 1993")
    Salhi_notes = [("Xe, mdot = 0.5 A, T vs Id for 1.21 mm: Fig 5.68"),
                   ("Xe, mdot = 0.93 A, T vs Id for 1.21 mm: Fig 6.3"),
                   ("Ar, mdot = 0.5 A, T vs Id for 1.21 mm: Fig 5.68. Measurements are taken 6 mm away from the orifice"),
                   ("Ar, mdot = 0.93 A, T vs Id for 1.27 mm: Fig 5.70. We consider "
                   "1.27 mm approximately equal to 1.21 mm to keep same orifice sizes "
                   "(possibly typo)"),
                   ("Ar, mdot = 0.93 A, T vs Id for 0.76 mm: Fig 5.70 ")
                   ]
    
    alldata.loc[alldata.cathode == 'Salhi-Xe','reference'] = Salhi_ref
    alldata.loc[alldata.cathode == 'Salhi-Ar-1.21','reference'] = Salhi_ref
    alldata.loc[alldata.cathode == 'Salhi-Ar-0.76','reference'] = Salhi_ref
    
    # Xenon, mass flow of 0.5 A and 0.93 A
    boolcond = (alldata.cathode == 'Salhi-Xe') & (alldata.massFlowRate == 0.5)
    alldata.loc[boolcond,'note'] = Salhi_notes[0]
    boolcond = (alldata.cathode == 'Salhi-Xe') & (alldata.massFlowRate == 0.93)
    alldata.loc[boolcond,'note'] = Salhi_notes[1]
    
    # Argon
    boolcond = (alldata.cathode == 'Salhi-Ar-1.21') & (alldata.massFlowRate == 0.5)
    alldata.loc[boolcond,'note'] = Salhi_notes[2]
    boolcond = (alldata.cathode == 'Salhi-Ar-1.21') & (alldata.massFlowRate == 0.93)
    alldata.loc[boolcond,'note'] = Salhi_notes[3]
    boolcond = (alldata.cathode == 'Salhi-Ar-0.76') & (alldata.massFlowRate == 0.93)
    alldata.loc[boolcond,'note'] = Salhi_notes[4]
    
    
    # Siegfried
    siegfried_refs = ("[1] P. J. Wilbur, \"Ion and advanced electric thruster research,\" CR-165253, 1980., "
    "[2] Siegfried, D. E., Wilbur, P. J. \"Phenomenological model describing orificed, hollow cathode operation\", 15th IEPC, 1981 "
    "[3] Siegfried, D. E. \"A Phenomenological Model for Orificed Hollow Cathodes\", Ph.D. thesis, Colorado State University, 1982")
    siegfried_notes = ("# Mercury cathode with a 0.76mm diameter orifice "
    "Table p. 14 of Ref. [1], p.4 of Ref. [2]. "
    "Temperature data for the cases at 3.3 A are from Ref. [2] "
    "Orifice length is from Ref. [3], p.130 "
    "The insert temperature for the experiments at fixed Id = 3.31 A but "
    "varying mass flow rate are taken to be the same as the one reported for 3.31 A")
    
    alldata.loc[alldata.cathode=='Siegfried','reference'] = siegfried_refs
    alldata.loc[alldata.cathode=='Siegfried','note'] = siegfried_notes
    
    # Domonkos
    domonkos_ref = ("M. T. Domonkos, \"Evaluation of low-current orificed hollow "
    "cathodes,\" University of Michigan, 1999.")
    
    # AR3
    ar3_note = ("Reduction of Cathode Internal Pressure for Spot-Mode Operation "
    "Fig 3.27 Orifice plate temperature dependence on aspect ratio in a 1.00-A discharge to the keeper "
    "Extracted from the overall plot; this data is for the AR3, at Id = 1A. "
    "The wall temperature is here equal to the orifice plate temperature ")
    alldata.loc[alldata.cathode=='AR3','reference'] = domonkos_ref
    alldata.loc[alldata.cathode=='AR3','note'] = ar3_note
    alldata.loc[alldata.cathode=='AR3','orificeTemperature'] = alldata.loc[alldata.cathode=='AR3','insertTemperatureAverage']
    
    # EK6
    ek6_note = ("Cathode Internal Pressure Under Various Operating Conditions "
    "Fig 3.29: Orifice plate temperature dependence on keeper type in a diode discharge "
    "Extracted from the overall plot; this data is for the EK6. "
    "The temperature data is the orifice plate temperature")
    alldata.loc[alldata.cathode=='EK6','reference'] = domonkos_ref
    alldata.loc[alldata.cathode=='EK6','note'] = ek6_note
    alldata.loc[alldata.cathode=='EK6','orificeTemperature'] = alldata.loc[alldata.cathode=='EK6','insertTemperatureAverage']
    
    # SC012
    sc012_note = ("Reduction of Cathode Internal Pressure for Spot-Mode Operation "
    "Extracted from the overall plot; this data is for the SC012. "
    "The mass flow rate values are not exactly the same from one run to the other "
    "one, so I kept them as raw data values extracted from the plot")
    alldata.loc[alldata.cathode=='SC012','reference'] = domonkos_ref
    alldata.loc[alldata.cathode=='SC012','note'] = sc012_note
    
    
    
    # Friedly
    friedly_ref = ("V. J. Friedly, \"Hollow cathode operation at high discharge currents\", "
    "M. Sc. Thesis, NASA CR-185238, 1990")
    friedly_note = ("Fig 30 p.65: Effects of discharge current and cathode "
    "configuration on cathode wall temperature "
    "Fig 33a p.69: Effects of discharge current and propellant flowrate on cathode "
    "internal pressure; "
    "Xenon cathode; "
    "6.4 mm outer tube, 0.74 mm orifice diameter => 4.7 mm insert diameter; "
    "Lo is not specified so we set it as 1 mm; "
    "The cathode wall temperature is plotted with a single point for a flow rate; " 
    "range of 180 to 550 mA; we consider that the wall temperature stays constant "
    "with flow rate (typically an acceptable assumption).")
    
    alldata.loc[alldata.cathode=='Friedly','reference'] = friedly_ref
    alldata.loc[alldata.cathode=='Friedly','note'] = friedly_note
    
    # T6
    t6_ref = ("[1] S. W. Patterson, D. G. Fearn, \"The generation of high energy "
              "ions in hollow cathode discharges\", IEPC, 1999; "
              "[2] D. G. Fearn, S. W. Patterson, \"Characterisation of the high "
              "current hollow cathode for the T6 thruster\", 34th JPC, 1998")
    t6_notes = ("[1] Fig 15 Measured pressure as mdot is varied; "
                "[2] Fig 16 The influence of orifice diameter and flow rate on " 
                "temperature at 15 A; "
                "Extracted from Fig. 15. Gas is xenon. Mass flow rate error: 1 to " 
                "2%. The orifice diameter is probably 1 mm as Ref. [1] refers to "
                "Ref. [2], which uses 1 mm in Figs 6 and 12. [2] Fig 16 The wall "
                "temperature is the exterior casing temperature, NOT the insert temperature.")
    
    
    
    alldata.loc[alldata.cathode=='T6','reference'] = t6_ref
    alldata.loc[alldata.cathode=='T6','note'] = t6_notes
    
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
    
    ### FIX TEMPERATURES THAT ARE NAN
    ### TODO: DO WE USE K OR DEGC?
    alldata.insertTemperatureAverage.fillna(1273,inplace=True)

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
    # Mass of gass in amu
    alldata.loc[alldata['gas'] == 'Xe', 'gasMass'] = cc.M.Xe
    alldata.loc[alldata['gas'] == 'Ar', 'gasMass'] = cc.M.Ar
    alldata.loc[alldata['gas'] == 'Hg', 'gasMass'] = cc.M.Hg
    
    # Ionization potential in eV
    alldata.loc[alldata['gas'] == 'Xe', 'ionizationPotential'] = 12.1298
    alldata.loc[alldata['gas'] == 'Ar', 'ionizationPotential'] = 15.75962
    alldata.loc[alldata['gas'] == 'Hg', 'ionizationPotential'] = 10.4375
    
    # Speed of sound
    sos_str = 'speedOfSound=(@gam*@kb/(gasMass*@amu)*insertTemperatureAverage*3)**(0.5)'
    alldata.eval(sos_str, local_dict=constant_dict, inplace=True)
    
    # Mass flow rate
    mdot_str = 'massFlowRate_SI = massFlowRate * gasMass * @amu / @q'
    alldata.eval(mdot_str, local_dict=constant_dict, inplace=True)
    
    ### Pressures
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

    ### COMPUTE REYNOLDS NUMBER
    alldata = df_reynolds_number(alldata)
        
    return alldata
