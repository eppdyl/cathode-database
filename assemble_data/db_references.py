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

'''
File: db_references.py
Author: Pierre-Yves Taunay
Date: May 2020

This file contains the list of reference and any noteworthy comment for the data
loaded in the database.
'''


referenceList = [
### NSTAR
("K. K. Jameson, D. M. Goebel, and R. M. Watkins, "
    "Hollow Cathode and Keeper-Region Plasma Measurements, " 
    "41st JPC, 2005.\n "
"I. G. Mikellides, \"Effects of viscosity in a partially ionized " 
"channel flow with thermionic emission,\" Phys. Plasmas, vol. 16, " 
"no. 1, 2009.\n"
"J. Polk, A. Grubisic, N. Taheri, D. Goebel, R. Downey, and " 
"S. E. Hornbeck, \"Emitter Temperature Distributions in the NSTAR " 
"Discharge Hollow Cathode,\" 41st JPC, 2005."),
### NEXIS
 ("K. K. Jameson, D. M. Goebel, and R. M. Watkins, \"Hollow Cathode " 
 "and Thruster Discharge Chamber Plasma Measurements Using "
 "High-Speed Scanning Probes,\" 29th International Electric Propulsion Conference, 2005.\n"
 "D. Goebel, K. K. Jameson, R. M. Watkins, and I. Katz, "
 "\"Hollow Cathode and Keeper-Region Plasma Measurements Using Ultra-Fast Miniature Scanning Probes,\" "
 "40th JPC, 2004."),
### SALHI
("A. Salhi, \"Theoretical and experimental studies of orificed, " 
"hollow cathode operation,\" The Ohio State University, 1993"),
None,None,None,
### SIEGFRIED AND WILBUR
("P. J. Wilbur, "
"\"Ion and advanced electric thruster research,\" "
"CR-165253, 1980.\n "
"Siegfried, D. E., Wilbur, P. J. "
"\"Phenomenological model describing orificed, hollow cathode operation,\" "
"15th IEPC, 1981 \n "
"Siegfried, D. E. \"A Phenomenological Model for Orificed Hollow Cathodes\","
"Ph.D. thesis, Colorado State University, 1982\n "
"P. J. Wilbur, \"Advanced Ion Thruster Research,\" CR-168340, 1984."),
None,
### FRIEDLY
("V. J. Friedly, \"Hollow cathode operation at high discharge currents\", "
"M. Sc. Thesis, NASA CR-185238, 1990"),
### T6
("S. W. Patterson, D. G. Fearn, \"The generation of high energy "
  "ions in hollow cathode discharges\", IEPC, 1999;\n "
  "D. G. Fearn, S. W. Patterson, \"Characterisation of the high "
  "current hollow cathode for the T6 thruster\", 34th JPC, 1998"),
### AR3, EK6, SC012
("M. T. Domonkos, \"Evaluation of low-current orificed hollow "
"cathodes,\" University of Michigan, 1999."),
("M. T. Domonkos, \"Evaluation of low-current orificed hollow "
"cathodes,\" University of Michigan, 1999."),
("M. T. Domonkos, \"Evaluation of low-current orificed hollow "
"cathodes,\" University of Michigan, 1999."),
### JPL 1.5 CM CATHODE
("E. Chu and D. M. Goebel, "
  "\"High-current lanthanum hexaboride hollow cathode for 10-to-50-kW hall thrusters,\" "
  "IEEE Trans. Plasma Sci., vol. 40, no. 9, pp. 2133–2144, 2012.\n"
  "G. Becatti, D. M. Goebel, J. E. Polk, and P. Guerrero, "
  "\"Life Evaluation of a Lanthanum Hexaboride Hollow Cathode for High-Power Hall Thruster,\" "
  "J. Propuls. Power, vol. 34, no. 4, pp. 893–900, 2017"),
                      None,None,
### PLHC
("P-Y Taunay, PhD dissertation, Princeton University, 2020"),
]       
             
noteList = [
### NSTAR
("Fig 3 - Pressure measured inside the 1/4\" hollow cathode " 
   "for various NSTAR throttle levels.\n"
   "Fig 4 - Axial density cathode and anode profiles plotted "
   "on a semi-log scale for TH8 and TH15.\n"
   "Fig 6 - Cathode plasma potential and electron temperature "
   "profiles for TH8 and TH15. The throttle levels TH4, " 
   "TH8, TH15 are from: V. Rawlin, J. Sovey, J. Anderson, and " 
   "J. Polk, \"NSTAR flight thruster qualification testing, " 
   "34th AIAA/ASME/SAE/ASEE JPC, 1998.\n"
   "TH12: W. G. Tighe, K. Chien, D. M. Goebel, and R. T. Longo, " 
   "\"Hollow Cathode Ignition and Life Model,\" 41st JPC, 2005. "
   "Tw is calculated with Polk's fit\n"
   "Fig. 10 - Comparisons between measured and computed " 
   "values of the cathode gas pressure.\n "
   "Tw is calculated with Polk's fit\n"
   "Fig.4 - Comparison of temperatures from the NSTAR cathode " 
   "and the plasma contactor.\n"
   "Fig.8 - Internal hollow cathode pressure increases with flow"
   "rate and discharge current"),
### NEXIS
("Fig. 7 - Internal NEXIS cathode pressure (a) constant flow "
   "rate at 5.5 sccm (b) constant discharge current at 22 A.\n"
 "Fig. 8 - Pressure measured and calculated inside the hollow "
   "cathode without plasma (a) and with plasma (b)"),
### SALHI
 ("Xe, mdot = 0.5 A, T vs Id for 1.21 mm: Fig 5.68\n"
  "Xe, mdot = 0.93 A, T vs Id for 1.21 mm: Fig 6.3\n"
  "Ar, mdot = 0.5 A, T vs Id for 1.21 mm: Fig 5.68. Measurements are taken 6 mm away from the orifice\n"
  "Ar, mdot = 0.93 A, T vs Id for 1.27 mm: Fig 5.70. We consider "
   "1.27 mm approximately equal to 1.21 mm to keep same orifice sizes "
   "(possibly typo)\n"
  "Ar, mdot = 0.93 A, T vs Id for 0.76 mm: Fig 5.70 "),
          None,None,None,
### SIEGFRIED AND WILBUR          
("[4] Ar: Figs. 37-40. Mass flow deduced from P, Id, do and correlation. "
 "OR Pressure deduced from mdot, Id, do and correlation.\n "
 "Xe: Figs. 41-44. Same as above\n"
 "Fig. 29 Mass flow deduced from P, Id, do and correlation.\n"
 "Fig. 32 Mass flow deduced from P, Id, do and correlation."), None,
### FRIEDLY
("Fig 30 p.65: Effects of discharge current and cathode "
"configuration on cathode wall temperature "
"Fig 33a p.69: Effects of discharge current and propellant flowrate on cathode "
"internal pressure; "
"Xenon cathode; "
"6.4 mm outer tube, 0.74 mm orifice diameter => 4.7 mm insert diameter; "
"Lo is not specified so we set it as 1 mm; "
"The cathode wall temperature is plotted with a single point for a flow rate; " 
"range of 180 to 550 mA; we consider that the wall temperature stays constant "
"with flow rate (typically an acceptable assumption)."),
## T6
("[1] Fig 15 Measured pressure as mdot is varied;\n "
"[2] Fig 16 The influence of orifice diameter and flow rate on " 
"temperature at 15 A; "
"Extracted from Fig. 15. Gas is xenon. Mass flow rate error: 1 to " 
"2%. The orifice diameter is probably 1 mm as Ref. [1] refers to "
"Ref. [2], which uses 1 mm in Figs 6 and 12. [2] Fig 16 The wall "
"temperature is the exterior casing temperature, NOT the insert temperature."),
### AR3
 ("Reduction of Cathode Internal Pressure for Spot-Mode Operation "
"Fig 3.27 Orifice plate temperature dependence on aspect ratio in a 1.00-A discharge to the keeper "
"Extracted from the overall plot; this data is for the AR3, at Id = 1A. "
"The wall temperature is here equal to the orifice plate temperature "),
### EK6
("Cathode Internal Pressure Under Various Operating Conditions "
"Fig 3.29: Orifice plate temperature dependence on keeper type in a diode discharge "
"Extracted from the overall plot; this data is for the EK6. "
"The temperature data is the orifice plate temperature"),
### SC012
 ("Reduction of Cathode Internal Pressure for Spot-Mode Operation "
"Extracted from the overall plot; this data is for the SC012. "
"The mass flow rate values are not exactly the same from one run to the other "
"one, so I kept them as raw data values extracted from the plot"),
### JPL 1.5 CM CATHODE
 ("[1] Fig. 9\n "
  "[2] Figs 6-8"),
 None, None,
 ("Experimental data from Chapter 2. Last 5 measurements are made with Baratron gauge")
]

