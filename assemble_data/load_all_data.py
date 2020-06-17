# "cathode" Python package
# Version: 1.0
# A package of various cathode models that have been published throughout the
# years. Associated publication:
# Wordingham, C. J., Taunay, P.-Y. C. R., and Choueiri, E. Y., "A critical
# review of hollow cathode modeling: 0-D models," Journal of Propulsion and
# Power, in preparation.
#
# Copyright (C) 2019 Christopher J. Wordingham and Pierre-Yves C. R. Taunay
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https:/www.gnu.org/licenses/>.
#
# Contact info: https:/github.com/pytaunay
#
import cathode.constants as cc
import pandas as pd
import numpy as np
import os

from import_db import dtypes,from_np_array

# folder                 datafile skip_header  \
#NSTAR          jpl/nstar/discharge         P_vs_Id_mdot.csv          21   
#NEXIS                    jpl/nexis         P_vs_Id_mdot.csv          11   
#Salhi                  lewis/salhi         P_vs_Id_mdot.csv          16   
#Salhi-Ar-1.21                  NaN                      NaN         NaN   
#Salhi-Ar-0.76                  NaN                      NaN         NaN   
#Salhi-Xe                       NaN                      NaN         NaN   
#Siegfried          lewis/siegfried         P_vs_Id_mdot.csv          14   
#Friedly              lewis/friedly         P_vs_Id_mdot.csv          14   
#T6                          rae/t6         P_vs_Id_mdot.csv          15   
#AR3                  pepl/domonkos  P_vs_mdot_Id-1A_AR3.csv          14   
#EK6                  pepl/domonkos     P_vs_mdot_Id_EK6.csv          15   
#SC012                pepl/domonkos   P_vs_mdot_Id_SC012.csv          13   
#JPL 1.5cm     jpl/goebel-lab6-cathodes/1.5cm-cathode P_vs_Id_mdot.csv
#JPL 1.5cm-3mm NaN
#JPL 1.5cm-5mm NaN
cathodeList = ['NSTAR','NEXIS','Salhi','Salhi-Ar-1.21','Salhi-Ar-0.76',
               'Salhi-Xe','Siegfried','Siegfried-NG','Friedly','T6','AR3',
               'EK6','SC012','JPL-1.5cm','JPL-1.5cm-3mm','JPL-1.5cm-5mm',
               'PLHC'
               ]


folderList = ['jpl/nstar/discharge',
              'jpl/nexis',
              'lewis/salhi',
              None,None,None,
              'lewis/siegfried',
              None,
              'lewis/friedly',
              'rae/t6',
              'pepl/domonkos',
              'pepl/domonkos',
              'pepl/domonkos',
              'jpl/lab6-cathodes/1.5cm-cathode',
              None,None,
              'princeton/plhc']

fileList = [['P_vs_Id_mdot.csv','positional_combined.csv'],
            ['P_vs_Id_mdot.csv','positional_combined.csv'],
            ['P_vs_Id_mdot.csv','positional_combined.csv'],None,None,None,
            ['P_vs_Id_mdot.csv','positional_combined.csv'],None,
            ['P_vs_Id_mdot.csv'],
            ['P_vs_Id_mdot.csv'],
            ['P_vs_mdot_Id-1A_AR3.csv'],
            ['P_vs_mdot_Id_EK6.csv'],
            ['P_vs_mdot_Id_SC012.csv'],
            ['P_vs_Id_mdot.csv','positional_combined.csv'],None,None,
            ['P_vs_Id_mdot.csv']]

#headerNames = ['Id','mdot','P','mass','do','Lo','dc','Tw','To']
#headerSkip = [21, # NSTAR 
#              11, # NEXIS
#              16, # Salhi
#              None,None,None,
#              16, # Siegfried
#              None,
#              14, # Friedly
#              15, # T6
#              14, # AR3
#              15, # EK6
#              13, # SC012
#              13, # JPL 1.5 cm
#              None, None
#              ]

pressureFiles = {
        'cathode' :cathodeList ,
        'folder': folderList,
        'datafile': fileList
        }



def load_csv_data():
    '''
    Loads the CSV data for all the cathodes specified by name in cathode_idx. 
    Stores the corresponding results in the dataframe pdf ("pressure 
    dataframe")    
    '''
    ### Pandas representation of the list of files to load
    df_pFiles = pd.DataFrame(pressureFiles,
                             columns = np.sort(list(pressureFiles)),
                             index = cathodeList)
    
    ### Pandas representation of the data that will be loaded
    # Empty dataframe
    df = np.empty(0, dtype=dtypes)
    df = pd.DataFrame(df)
    
    ### Iterate through all the pressure files
    root_folder = os.path.dirname(__file__)
    root_folder = os.path.join(root_folder,'..')
    
    for index, row  in df_pFiles.iterrows():
        if pd.isnull(row['folder']):
            next
        else:                        
            ### Load data
            df = load_single_cathode(df,row)

    df = df.reset_index()
 
    
    
    return df

def load_single_cathode(df,row):
    cathode = row['cathode']
    folder = row['folder']
    datafiles = row['datafile']
        
    folder = '../' + folder  
        
    for _,fname in enumerate(datafiles):
        datafile = folder + '/' + fname
        
        ### What type of file are we loading? 
        # Are we loading pressure?
        if 'P_vs_' in datafile:            
            df_from_csv = pd.read_csv(datafile,comment='#',delimiter=',')
            df_from_csv['cathode'] = cathode
            
            ### Some necessary conversions
            if cathode == 'Friedly':
                # Convert to eqA from mA
                df_from_csv['massFlowRate'] = \
                df_from_csv['massFlowRate'].apply(lambda x: x * 1e-3)
                
            elif cathode == 'AR3' or cathode == 'EK6' or cathode == 'SC012':
                # Convert from Pa x 1e-3 to Torr
                df_from_csv['totalPressure'] = \
                df_from_csv['totalPressure'].apply(lambda x: x * 1e3 / cc.Torr)
                
            elif cathode == 'T6':
                # Convert mass flow rate from mg/s to kg/s
                df_from_csv['massFlowRate_SI'] = \
                df_from_csv['massFlowRate_SI'].apply(lambda x: x * 1e-6)
                
                        
            df = df.append(pd.DataFrame(df_from_csv,columns=df.columns))
            
        # Are we loading positional data?
        elif 'positional_' in datafile:
            print(cathode)
            df_from_csv = pd.read_csv(datafile,comment='#',
                                      delimiter=',',
                                      converters = {
                                        'electronDensity': from_np_array,
                                        'electronTemperature': from_np_array,
                                        'plasmaPotential': from_np_array})
    
            df_from_csv['cathode'] = cathode
            
            # Compute the actual density
            df_from_csv['electronDensity'] = \
            df_from_csv['electronDensity'].apply(lambda x: compute_ne(x))
                     
            ### Have we already entered the corresponding [Id,mdot] case?
            for index, row in df_from_csv.iterrows():
                bcond = (df.cathode == cathode)
                bcond &= (df.dischargeCurrent == row['dischargeCurrent'])
                bcond &= (df.massFlowRate_sccm == row['massFlowRate_sccm'])
           
                try:
                    df.loc[bcond] = row.copy(deep=True)
                    print(cathode,row['dischargeCurrent'],
                          row['massFlowRate_sccm'])
                except:
                    continue
            #dischargeCurrent,electronDensity,electronTemperature,idxmax,idxmin,insertDiameter,massFlowRate_sccm,orificeDiameter,orificeLength,plasmaPotential
            
    return df
    

def compute_ne(x):
    try:
        x0 = x[:,0]
        log10ne = x[:,1]
        
        arr = np.array([x0,10**log10ne])
    except:
        arr = np.nan
    
    return arr
    
#    # idx: name of the cathode
#    idx = ['NSTAR','NEXIS','Salhi','Salhi-Ar','Salhi-Xe','Salhi-Ar-1.21','Salhi-Ar-0.76','Siegfried','AR3','EK6','SC012','Friedly','T6']
#    cathode_idx = ['NSTAR','NEXIS','Salhi','Siegfried','AR3','EK6','SC012','Friedly','T6']
#
#    # col: name of the columns
#    # Id -> discharge current
#    # mdot -> mass flow rate
#    # P -> pressure
#    # do -> orifice diameter
#    # Lo -> orifice length
#    # species -> gas used
#    # corr -> P/mdot * do^2 for Siegfried and Wilbur
#    col = ['Id','mdot','P','do','Lo','mass','Tw','To','dc','eiz','corr','corr_up','corr_lo']
#
#    pdf = pd.DataFrame(index=idx, columns=col)
#
#    #### Load data
#    #root_folder = 'cathode-data'
#    root_folder = os.path.dirname(__file__)
#    root_folder = os.path.join(root_folder,'..')
#
##    di_str = pkg_resources.open_binary(files,'datafile_index.pkl')
#    df = pd.read_pickle('datafile_index.pkl')
#
#    for cat in cathode_idx:
#        folder = root_folder + '/' + df.folder[cat]
#        datafile = folder + '/' + df.datafile[cat]
#        nskip = df.skip_header[cat]
#        dtype = df.dtype[cat]
#
#        load_single_cathode(cat,datafile,nskip,dtype,pdf)
#
#    ## Make sure we fill the temperature array with an arbitrary temperature
#    ## when data is not available
#    for name in idx:
#        arr = pdf.Tw[name]
#        arr_idx = np.isnan(arr)
#        arr[arr_idx] = 1000
#        pdf.Tw[name] = arr
#
#    ## Extract unique data 
#    pdf_extract = pdf[(pdf.index != 'Salhi') & (pdf.index != 'Salhi-Ar') ]
#
##    return pdf_extract
#
#def load_single_cathode(cat,datafile,nskip,dtype,pdf):
#    '''
#    Loads the data from a single cathode. Since they each differ, there are 
#    tests to determine which cathode we are considering. 
#    The corresponding fields are then filled in the dataframe used
#    Inputs:
#        - cat: the cathode name of interest
#        - datafile: the datafile we are loading
#        - nskip: number of header lines to skipe
#        - dtype: the datatype loaded
#        - pdf: the pandas frame to fill
#    Note about the units for the final panda frame
#        - Id: current (A)
#        - mdot: mass flow rate (A)
#        - P: pressure (Torr)
#        - do: Orifice diameter (mm)
#        - Lo: Orifice length (mm)
#        - mass: propellant mass (amu)
#        - Tw: wall temperature (degC)
#    '''
#    # Read data
#    print(cat,datafile)
#    data = np.genfromtxt(datafile,delimiter=',',dtype=dtype,names=True,skip_header=nskip)
#    
#    pdf.Id[cat] = data['Id']
#    pdf.P[cat] = data['P']
#    pdf.do[cat] = data['do']
#    pdf.Lo[cat] = data['Lo']
#    pdf.mass[cat] = data['mass']
#    pdf.Tw[cat] = data['Tw']
#    pdf.dc[cat] = data['dc']
#    
#    
#    # Deduce the ionization energy from the mass
#    # TODO: Add the ionization energy to the cathode.constants package
#    pdf.eiz[cat] = (data['mass'] == 131.293) * 12.1298  # Xe
#    pdf.eiz[cat] += (data['mass'] == 39.948) * 15.75962 # Ar
#    pdf.eiz[cat] += (data['mass'] == 200.59) * 10.43750 # Hg
#    
#    
#    if cat != 'Siegfried':
#        pdf.mdot[cat] = data['mdot']
#
#    if cat == 'NSTAR' or cat == 'NEXIS':        
#        pdf.mdot[cat] *= cc.sccm2eqA # sccm to equivalent amperes
#
#    elif cat == 'Salhi':
#        # Get a couple of datasets separately
#        separate_salhi(pdf)
#
#    elif cat == 'Siegfried':     
#        # Round to 102 to have similar correlation
#        pdf.mdot[cat] = [102,102,102,102,102,78,62,35,25] 
#        
#        # mA to A
#        pdf.mdot[cat]  = np.asarray([mdot * 1e-3 for mdot in pdf.mdot[cat]]) 
#
#    elif cat == 'AR3' or cat == 'EK6' or cat == 'SC012':
#        pdf.P[cat] *= 1e3/cc.Torr
#        pdf.mdot[cat] *= cc.sccm2eqA # sccm to A
#
#    elif cat == 'Friedly':
#        pdf.mdot[cat] *= 1e-3 # mA to A
#
#    elif cat == 'T6':
#        mg2sccm = 22.413996 * 1e3 * 60.0 / (1e6*6.02214179e23) * 1.0 / cc.M.species('Xe')
#        mg2eqA = mg2sccm * cc.sccm2eqA
#        pdf.mdot[cat] *= mg2eqA # mg to A



def separate_salhi(pdf):
    salhi_ar = pdf.mass['Salhi'] == 39.948
    salhi_xe = pdf.mass['Salhi'] == 131.293
    
    pdf.Id['Salhi-Ar'] = pdf.Id['Salhi'][salhi_ar]
    pdf.mdot['Salhi-Ar'] = pdf.mdot['Salhi'][salhi_ar]
    pdf.P['Salhi-Ar'] = pdf.P['Salhi'][salhi_ar]
    pdf.do['Salhi-Ar'] = pdf.do['Salhi'][salhi_ar]
    pdf.Lo['Salhi-Ar'] = pdf.Lo['Salhi'][salhi_ar]
    pdf.mass['Salhi-Ar'] = pdf.mass['Salhi'][salhi_ar]
    pdf.Tw['Salhi-Ar'] = pdf.Tw['Salhi'][salhi_ar]
    pdf.dc['Salhi-Ar'] = pdf.dc['Salhi'][salhi_ar]
    pdf.eiz['Salhi-Ar'] = pdf.eiz['Salhi'][salhi_ar]
        
    pdf.Id['Salhi-Xe'] = pdf.Id['Salhi'][salhi_xe]
    pdf.mdot['Salhi-Xe'] = pdf.mdot['Salhi'][salhi_xe]
    pdf.P['Salhi-Xe'] = pdf.P['Salhi'][salhi_xe]
    pdf.do['Salhi-Xe'] = pdf.do['Salhi'][salhi_xe]
    pdf.Lo['Salhi-Xe'] = pdf.Lo['Salhi'][salhi_xe]
    pdf.mass['Salhi-Xe'] = pdf.mass['Salhi'][salhi_xe]
    pdf.Tw['Salhi-Xe'] = pdf.Tw['Salhi'][salhi_xe]
    pdf.dc['Salhi-Xe'] = pdf.dc['Salhi'][salhi_xe]
    pdf.eiz['Salhi-Xe'] = pdf.eiz['Salhi'][salhi_xe]

    # Get the 1.21 mm separately
    salhi_ar121 = pdf.do['Salhi-Ar'] == 1.21
    
    pdf.Id['Salhi-Ar-1.21'] = pdf.Id['Salhi-Ar'][salhi_ar121]
    pdf.mdot['Salhi-Ar-1.21'] = pdf.mdot['Salhi-Ar'][salhi_ar121]
    pdf.P['Salhi-Ar-1.21'] = pdf.P['Salhi-Ar'][salhi_ar121]
    pdf.do['Salhi-Ar-1.21'] = pdf.do['Salhi-Ar'][salhi_ar121]
    pdf.Lo['Salhi-Ar-1.21'] = pdf.Lo['Salhi-Ar'][salhi_ar121]
    pdf.mass['Salhi-Ar-1.21'] = pdf.mass['Salhi-Ar'][salhi_ar121]
    pdf.Tw['Salhi-Ar-1.21'] = pdf.Tw['Salhi-Ar'][salhi_ar121]
    pdf.dc['Salhi-Ar-1.21'] = pdf.dc['Salhi-Ar'][salhi_ar121]
    pdf.eiz['Salhi-Ar-1.21'] = pdf.eiz['Salhi-Ar'][salhi_ar121]
    
    salhi_ar076 = pdf.do['Salhi-Ar'] == 0.76
    
    pdf.Id['Salhi-Ar-0.76'] = pdf.Id['Salhi-Ar'][salhi_ar076]
    pdf.mdot['Salhi-Ar-0.76'] = pdf.mdot['Salhi-Ar'][salhi_ar076]
    pdf.P['Salhi-Ar-0.76'] = pdf.P['Salhi-Ar'][salhi_ar076]
    pdf.do['Salhi-Ar-0.76'] = pdf.do['Salhi-Ar'][salhi_ar076]
    pdf.Lo['Salhi-Ar-0.76'] = pdf.Lo['Salhi-Ar'][salhi_ar076]
    pdf.mass['Salhi-Ar-0.76'] = pdf.mass['Salhi-Ar'][salhi_ar076]
    pdf.Tw['Salhi-Ar-0.76'] = pdf.Tw['Salhi-Ar'][salhi_ar076]
    pdf.dc['Salhi-Ar-0.76'] = pdf.dc['Salhi-Ar'][salhi_ar076]
    pdf.eiz['Salhi-Ar-0.76'] = pdf.eiz['Salhi-Ar'][salhi_ar076]


