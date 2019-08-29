import numpy as np
import matplotlib.pyplot as plt
import cathode.constants as cc
import pickle

from import_db import import_data
from correlation import Lem
from build_numerical import build_zerod_dataframe

def plot_density():
    
    ### Position vs. density
    for index, row in alldata.iterrows():
        if np.isnan(row['electronDensity']).any():
            continue
        else:
            ### Grab the 0D model data
            # Get the experimental conditions
            Id = row['dischargeCurrent']
            mdot = row['massFlowRate']
            mdot_sccm = mdot/cc.sccm2eqA
            
            # Do we have anything close in the zero-d model?
            bcond = (zerod_data.cathode == row['cathode']) 
            bcond &= (zerod_data.dischargeCurrent == row['dischargeCurrent']) 
            
            massFlowCond = (zerod_data.massFlowRate == row['massFlowRate'])
            massFlowCond |= (np.isclose(zerod_data.massFlowRate/cc.sccm2eqA,
                                        row['massFlowRate']/cc.sccm2eqA,
                                        atol = 1))
            
            bcond &= massFlowCond
            
            
            
            ### Grab experimental data
            ne_data = row['electronDensity']
            dc = row['insertDiameter']
            
            # Insert stuff only
            insert_ne = ne_data[ne_data[:,0]>0]
            
            # Back only for fitting
            if row['cathode'] == 'NSTAR':
                rev = insert_ne[-50:]
            elif row['cathode'] == 'NEXIS':
                rev = insert_ne[-40:-10]
            else:
                rev = insert_ne[-10:]
            
            
            rev[:,0] /= dc
            rev[:,1] /= np.max(insert_ne[:,1])
            
            # Fit XP data
            ret = np.polyfit(rev[:,0],np.log(rev[:,1]),1,full=True)
            m,b = ret[0]
            residuals = ret[1]
            
            ### Plot
            if residuals < 5e-2 or row['cathode'] == 'NSTAR' or row['cathode'] == 'NEXIS':    
    #                plt.semilogy(rev[:,0],
    #                         rev[:,1])
    #                
    #                plt.semilogy(rev[:,0],
    #                        np.exp(b + m*rev[:,0]),'k-')
    #                print(row['dischargeCurrent'],row['massFlowRate'] / cc.sccm2eqA, row['cathode'], 1/m*dc)
                
                if row['cathode'] == 'NSTAR':
                    style = 'ko'
                elif row['cathode'] == 'NEXIS':
                    style = 'k^'
                else:
                    style = 'k<'
                
                Lexp = np.abs(1/m)
                if not zerod_data[bcond].empty:
                    Pd = zerod_data[bcond].neutralPressureAverage/cc.Torr
                    Pd *= zerod_data[bcond].insertDiameter / 10
                    
                    Pderr = zerod_data[bcond].neutralPressureStd / cc.Torr
                    Pderr *= zerod_data[bcond].insertDiameter / 10
                    
                    
                    ng = zerod_data[bcond].neutralPressureAverage / cc.kB / 3000.
                    Lem0d = Lem(ng,zerod_data[bcond].insertDiameter*1e-3,'Xe')
    #                plt.errorbar(Pd,Lexp,xerr=Pderr,fmt=style)
                    plt.plot(zerod_data[bcond].dischargeCurrent/zerod_data[bcond].massFlowRate,
                             Lem0d/(zerod_data[bcond].insertDiameter*1e-3),style)
                else:
                    # If we have the correct mass flow rate then we can possibly do an interpolation
                    if not zerod_data[massFlowCond].empty:
                        print(row['cathode'],Id,mdot_sccm)
                        Idvec = zerod_data[massFlowCond].dischargeCurrent
                        Pgvec = zerod_data[massFlowCond].neutralPressureAverage
                        
                        Pg = np.interp(row['dischargeCurrent'],Idvec,Pgvec)
                        Pg /= cc.Torr
                        
                        Pd = Pg * row['insertDiameter'] / 10
                        
                        ng = Pg * cc.Torr / cc.kB / 3000.
                        Lem0d = Lem(ng,row['insertDiameter']*1e-3,row['gas'])
                       
                        plt.plot(row['dischargeCurrent']/row['massFlowRate'],Lem0d/(row['insertDiameter']*1e-3),style)
                        
                                    

zerod_data = build_zerod_dataframe()
alldata = import_data("assembled.csv")

TgK = 3000
ngvec = np.logspace(18,23)
#plt.semilogx(cc.kB * ngvec * 3000/cc.Torr,Lem(ngvec,1,'Xe'))
plt.xlim([0,100])

plt.ylabel("Lem/dc")
#plt.xlabel("Pg*dc (Torr cm)")    
plt.xlabel("Id/mdot")

plot_density()
