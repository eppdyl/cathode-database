import pandas as pd
import numpy as np

from cathode.experimental.load_data import load_all_data

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
        
# Load all of the data
pdf = load_all_data()

### Columns
dtypes = np.dtype([
        ('cathode',str), # Cathode name
       ('dischargeCurrent',float), # Discharge current , A
       ('massFlowRate',float), # Mass flow rate, eqA
       ('gas',str), # Gas used (periodic table shortcut)
       ('orificeDiameter',float), # Orifice diam, mm
       ('orificeLength',float), # Orifice length, mm
       ('insertDiameter',float), # Insert diameter, mm
       ('insertLength',float), # Insert length, mm
       ('upstreamPressurePoint',float), # Distance upstream of the emitter where the pressure is measured, mm
       ('orificeTemperature',float), # Orifice temperature, degC
       ('insertTemperatureAverage',float), # Average insert temperature, degC
       ('insertTemperature',np.ndarray), # Insert temperature vs. position, degC
       ('totalPressure',float), # Total pressure, Torr
       ('totalPressureError_p',float), # Total pressure error (+)
       ('totalPressureError_m',float), # Total pressure error (-) 
       ('electronDensity',np.ndarray), # Density vs. position, 1/m3
       ('electronTemperature',np.ndarray), # Electron temp. vs position, eV
       ('plasmaPotential',np.ndarray), # Plasma potential vs position, V
       ('reference',str), # Literature reference
        ('note',str)]) # Any noteworthy comment

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
               "for various NSTAR throttle levels. The throttle levels TH4, " 
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
alldata.loc[alldata.cathode=='SC012','note'] = ek6_note



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



