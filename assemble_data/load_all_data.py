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
            continue
        else:                        
            ### Load data
            df = load_single_cathode(df,row)    
    
    df = populate_gas_name(df) 
    df = apply_split(df)
    
    return df


def load_pressure_data(df,datafile,cathode):
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
    
    return df

def load_positional_data(df,datafile,cathode):
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
    for _, row in df_from_csv.iterrows():
        bcond = (df.cathode == cathode)
        bcond &= (df.dischargeCurrent == row['dischargeCurrent'])
        bcond &= (df.orificeDiameter == row['orificeDiameter'])
        
        # Has the gas mass been specified?
        try:
            bcond &= (df.gasMass == row['gasMass'])
        except KeyError:
            pass
        
        # Has the work function been specified?
        try:
            bcond &= (df.workFunction == row['workFunction'])
        except KeyError:
            # Has not, continue
            pass
        
        ### Grab the correct mass flow unit
        if 'massFlowRate_sccm' in row.index:
            bcond &= (df.massFlowRate_sccm == row['massFlowRate_sccm'])
        elif 'massFlowRate_SI' in row.index:
            bcond &= (df.massFlowRate_SI == row['massFlowRate_SI'])
        elif 'massFlowRate' in row.index:
            bcond &= (df.massFlowRate == row['massFlowRate'])
        else:
            # No flow rate specified, raise error
            raise KeyError
                 
        ### Extracted dataframe
        edf = df[bcond]
        # Did we find a spot for the data to go?
        if not edf.empty:                
            try:
                print(cathode,row['dischargeCurrent'],
                      row['massFlowRate_sccm'],row['orificeDiameter'])
            except:
                print(cathode,row['dischargeCurrent'],
                      row['massFlowRate'],row['orificeDiameter'])                        
            loc = (int)(df[bcond].index[0])
            

            print(cathode,df[bcond].index,loc)
            df.loc[loc,row.index] = row                        

        # We did not find an existing location. Append at the end.
        else:
            df = df.append(row)    
            
    return df

def load_single_cathode(df,row):
    '''Load the data from a single cathode.
    Inputs:
        - df: the main dataframe
        - row: a row of the files dataframe. It contains the name of the 
        cathode, the folder where the data resides, and the list of datafiles
        to load
    Ouput:
        - df: the updated dataframe
    '''
    cathode = row['cathode']
    folder = row['folder']
    datafiles = row['datafile']
        
    folder = '../' + folder  
        
    for _,fname in enumerate(datafiles):
        datafile = folder + '/' + fname
                
        ### What type of file are we loading? 
        # Are we loading pressure?
        if 'P_vs_' in datafile:            
            df = load_pressure_data(df,datafile,cathode)

                
        # Are we loading positional data?
        elif 'positional_' in datafile:
            df = load_positional_data(df,datafile,cathode)
                    
        df.reset_index(drop=True,inplace=True)                         
    return df
    

def compute_ne(x):
    '''From the 2D array stored in the csv file that contains 
    [position,log10(density)], compute the actual density'''
    
    try:
        x0 = x[:,0]
        log10ne = x[:,1]
        
        arr = np.array([x0,10**log10ne])
    except:
        arr = np.nan
    
    return arr
  
    
def populate_gas_name(df):
    '''Translates the gas mass to the gas name'''
    ### Go through each cathode
    for cat in cathodeList:
       xecat = (cat == 'NSTAR' or 
                   cat =='NEXIS' or 
                   cat == 'AR3' or
                   cat == 'EK6' or
                   cat == 'SC012' or
                   cat == 'Friedly' or
                   cat == 'T6' or
                   cat == 'JPL-1.5cm')
       
       arcat = (cat == 'PLHC')
       
       ### Check if xenon or argon cathode
       if xecat:
           df.loc[df.cathode==cat,'gas'] = 'Xe'
       elif arcat:
           df.loc[df.cathode==cat,'gas'] = 'Ar'
       else:
           ### Otherwise, case by case
           print(cat)
           if cat == 'Salhi':
               print(len(df.loc[(df.cathode==cat) & (df.gasMass == 131.293),'gas']))
               print(len(df.loc[(df.cathode==cat) & (df.gasMass == 39.948),'gas']))
               print(len(df.loc[(df.cathode==cat)]))
               
           # Check the obvious: gas mass
           df.loc[(df.cathode==cat) & (df.gasMass == 131.293),'gas'] = 'Xe'
           df.loc[(df.cathode==cat) & (df.gasMass == 39.948) ,'gas'] = 'Ar'
           df.loc[(df.cathode==cat) & (df.gasMass == 200.59) ,'gas'] = 'Hg'
           
               
           
           # TODO: Other cases?
           
    return df

def apply_split(df):
    '''Split some cathodes by gas and orifice size'''
    
    ### Salhi: split by gas and orifice size
    df.loc[(df.cathode=='Salhi') & (df.gas=='Xe'),'cathode'] = 'Salhi-Xe'
    df.loc[(df.cathode=='Salhi') & (df.gas=='Ar') & \
           (df.orificeDiameter == 0.76),'cathode'] = 'Salhi-Ar-0.76'
    df.loc[(df.cathode=='Salhi') & (df.gas=='Ar') & \
           (df.orificeDiameter == 1.21),'cathode'] = 'Salhi-Ar-1.21'    

    ### JPL 1.5 cm cathode: split by orifice size
    df.loc[(df.cathode=='JPL-1.5cm') & \
           (df.orificeDiameter == 3.0),'cathode'] = 'JPL-1.5cm-3mm'
    df.loc[(df.cathode=='JPL-1.5cm') & \
           (df.orificeDiameter == 5.0),'cathode'] = 'JPL-1.5cm-5mm' 
           
    ### Sigfried: split by gas type    
    df.loc[(df.cathode=='Siegfried') & \
           (df.gas=='Ar'),'cathode'] = 'Siegfried-NG'
    df.loc[(df.cathode=='Siegfried') & \
           (df.gas=='Xe'),'cathode'] = 'Siegfried-NG' 
           
    return df
