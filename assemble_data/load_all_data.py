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
File: load_all_data.py
Author: Pierre-Yves Taunay
Date: 2020

This file contains the necessary functions to load and process all of the CSV
data files.
'''
import pandas as pd
import numpy as np
import os

try:
    import cathode.constants as cc
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


from import_db import dtypes,from_np_array,fileDictionary,cathodeList

def special_cases(df,cat):
    '''
    Deals with special cases on cathode-by-cathode basis.
    '''
    if cat == 'NEXIS':
        ### Fill two pressures
        # 1. For 25 A, 5.5 sccm, we can arguably get the average pressure from 
        # the two closest cases (24 A and 26 A)
        # /!\ This is an estimate to get an idea of the total pressure /!\
        # It allows to plot a variety of things vs. pressure-diameter
        # bcond: the location where we should put new data
        bcond = (df.cathode == cat)
        bcond &= (df.massFlowRate_sccm == 5.5)
        bcond &= (df.orificeDiameter == 3.0)
        bcond &= (df.dischargeCurrent == 25.0)
        
        # datacond: the location we use as the data source
        datacond = (df.cathode == cat)
        datacond &= (df.massFlowRate_sccm == 5.5)
        datacond &= (df.orificeDiameter == 2.5)
        
        tdf = df[datacond]
        ddf = tdf[np.isclose(tdf.dischargeCurrent,25,atol=1)]
        averagePressure = np.nanmean(ddf.totalPressure)
       
        df.loc[df[bcond].index,'totalPressure'] = averagePressure
        
        # 2. For 25 A, 10 sccm, use the closest case (22 A, 10 sccm)
        # /!\ This is an estimate to get an idea of the total pressure /!\
        # It allows to plot a variety of things vs. pressure-diameter        
        bcond = df.cathode == cat
        bcond &= (df.massFlowRate_sccm == 10.0)
        bcond &= (df.orificeDiameter == 2.75)
        bcond &= (df.dischargeCurrent == 25.0)

        datacond = (df.cathode == cat)
        datacond &= (df.massFlowRate_sccm == 10.0)
        datacond &= (df.orificeDiameter == 2.5)
        datacond &= (df.dischargeCurrent == 22.0)
        
        averagePressure = df.at[df[datacond].index[0],'totalPressure']
        
        df.loc[df[bcond].index,'totalPressure'] = averagePressure
        
    elif (cat == 'JPL-1.5cm-3mm') or (cat == 'JPL-1.5cm-5mm'):
        ### The case 13.1 sccm, 25 A is pretty much the same as 13.0 sccm, 25 A
        ### Same with 13.1 sccm, 25.1 A is pretty much the same as 13.0 sccm, 25 A
        ### Use that value for the total pressure is pretty much the same as 13.0 sccm, 25 A
        bcond = df.cathode == cat
        bcond &= (df.massFlowRate_sccm == 13.1)
        bcond &= ((df.dischargeCurrent == 25.0) | (df.dischargeCurrent == 25.1))        
        
        datacond = (df.cathode == cat)
        datacond &= (df.massFlowRate_sccm == 13.0)
        datacond &= (df.dischargeCurrent == 25.0)
        
        averagePressure = df.at[df[datacond].index[0],'totalPressure']
        df.loc[df[bcond].index,'totalPressure'] = averagePressure
     

    elif (cat == 'AR3') or (cat == 'EK6'):
        ### Consider the emitter temperature to be that of the orifice
        bcond = df.cathode == cat          
        df.loc[df[bcond].index,'insertTemperatureAverage'] = \
        df.loc[df[bcond].index,'orificeTemperature']
        
    return df

def generate_dataframe():
    '''
    Loads the CSV data for all the cathodes specified by name in cathodeList. 
    Stores the corresponding results in a dataframe.
    Inputs: None
    Outputs:
        - df: the filled dataframe
    '''
    ### Pandas representation of the list of files to load
    df_Files = pd.DataFrame(fileDictionary,
                             columns = np.sort(list(fileDictionary)),
                             index = cathodeList)
    
    ### Pandas representation of the data that will be loaded
    # Empty dataframe
    df = np.empty(0, dtype=dtypes)
    df = pd.DataFrame(df)
    
    ### Iterate through all the pressure files
    root_folder = os.path.dirname(__file__)
    root_folder = os.path.join(root_folder,'..')
    
    for index, row  in df_Files.iterrows():
        if pd.isnull(row['folder']):
            continue
        else:                        
            ### Load data
            df = load_single_cathode(df,row)   
            
            ### Fill further geometry info
            Lemitter, Lupstream = row['additionalGeometry']
            
            df.loc[(df.cathode==row['cathode']),'insertLength'] = Lemitter
            df.loc[(df.cathode==row['cathode']),'upstreamPressurePoint'] = Lupstream
            df.loc[(df.cathode==row['cathode']),'reference'] = row['reference']
            df.loc[(df.cathode==row['cathode']),'note'] = row['note']
    
    df = populate_gas_info(df) 
    df = split_by_name(df)   
    df = calculate_electron_density_average(df)
    df = convert_flow_rates(df)
    
    ### Deal with any special cases
    for cat in cathodeList:
        df = special_cases(df,cat)
    
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
            # Has not, continue
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
        arr = arr.T
    except:
        arr = np.nan
    
    return arr
  
    
def populate_gas_info(df):
    '''Translates the gas mass to the gas name'''
    # Assign name by mass
    df.loc[(df.gasMass == 131.293),'gas'] = 'Xe'
    df.loc[(df.gasMass == 39.948) ,'gas'] = 'Ar'
    df.loc[(df.gasMass == 200.59) ,'gas'] = 'Hg'
            
    # Assign ionization potential by name
    df.loc[df.gas=='Ar','ionizationPotential'] = 15.75962
    df.loc[df.gas=='Xe','ionizationPotential'] = 12.1298
    df.loc[df.gas=='Hg','ionizationPotential'] = 10.4375
        
    return df

def calculate_electron_density_average(df):
    tdf = df[['electronDensityAverage']].dropna()
    df.loc[tdf.index,'electronDensityAverage'] = 10**tdf
    
    return df

def split_by_name(df):
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

def convert_flow_rates(df):
    '''
    Convert from one set of flow rates to another one
    '''
    
    ### sccm to eqA
    tdf = df['massFlowRate_sccm'].dropna()
    df.loc[tdf.index,'massFlowRate'] = tdf * cc.sccm2eqA
    
    ### SI to eqA
    tdf = df[['gasMass','massFlowRate_SI']].dropna()
    df.loc[tdf.index,'massFlowRate'] = tdf['massFlowRate_SI'] / tdf['gasMass'] * cc.e/cc.atomic_mass
    
    ### eqA to sccm
    tdf = df['massFlowRate'].dropna()
    df.loc[tdf.index,'massFlowRate_sccm'] = tdf / cc.sccm2eqA
    
    ### eqA to SI
    tdf = df[['gasMass','massFlowRate']].dropna()
    df.loc[tdf.index,'massFlowRate_SI'] = tdf['massFlowRate'] * tdf['gasMass'] * cc.atomic_mass/cc.e
    
    return df
    
