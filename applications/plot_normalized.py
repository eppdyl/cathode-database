import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cathode.constants as cc
import pickle
import itertools

import scipy.stats

from import_db import import_data
from correlation import Lem, Te_insert
from build_numerical import build_zerod_dataframe

def plot_density(alldata,zerod_data):
    TgK = 3000
    ngvec = np.logspace(18,23)
    fig, ax = plt.subplots(1,2)
    
    ax[0].semilogx(cc.kB * ngvec * TgK/cc.Torr * 1,Lem(ngvec,1e-2,'Xe')/1e-2)
    ax[0].set_xlim([0.1,10])
    ax[0].set_ylim([0,1])
    
    ax[0].set_ylabel("Lem/dc")
    ax[0].set_xlabel("Pg*dc (Torr cm)")    
    ax[1].set_xlabel("Id")   
    ax[1].set_ylim([0,1])
    
    Lem_theory = pd.DataFrame()
    
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

            zdcond = massFlowCond
            zdcond &= (zerod_data.cathode == row['cathode'])             
            
            
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
            elif row['cathode'] == 'JPL-1.5cm':
                npoints = find_JPL_indexing(Id,mdot_sccm)
                rev = insert_ne[-npoints:]
            elif row['cathode'] == 'Salhi-Xe':
                rev = insert_ne[:-1]
#                plt.figure()
#                plt.semilogy(insert_ne[:,0],insert_ne[:,1],'.')
#                plt.title(row['cathode'] + ' ' + str(Id) + ' A ' + str(mdot_sccm) + ' sccm')
            
            
            rev[:,0] /= dc
            rev[:,1] /= np.max(insert_ne[:,1])
            
            # Fit XP data
            ret = np.polyfit(rev[:,0],np.log(rev[:,1]),1,full=True,cov=True)
            m,b = ret[0]
#            residuals = ret[1]
            
            # Estimate the error
            sig = 0.2 # 40% error (95% confidence interval)
            
            # Standard error on the slope
            tmp = rev[:,0]-np.mean(rev[:,0]) 
            tmp = tmp**2
            serr_slope = np.sqrt(sig**2 / (np.sum(tmp)))
            
            # Standard deviation of 1/X where X is normally distributed
            s_err = serr_slope ** 2 / m**2 * (1 + 2*serr_slope ** 2 / m**2)
            s_err = np.sqrt(s_err) # Standard dev.
            
            Lexp = np.abs(1/m)
            Lemerr = 2*s_err # 95% confidence
            
            ### Plot
#            print("Cathode","Lem","5/P","15/P")
            if(row['cathode'] == 'JPL-1.5cm' or 
               row['cathode'] == 'NSTAR' or 
               row['cathode'] == 'NEXIS' or
               row['cathode'] == 'Salhi-Xe'):
                
                if row['cathode'] == 'NEXIS':
                    print(Lexp*dc*1e-3,5/(1.15*101325./760.),15/(1.15*101325./760.))
                elif row['cathode'] == 'JPL-1.5cm':
                    if row['dischargeCurrent'] == 100:
                        print(Lexp*dc*1e-3,5/(2*101325./760.),15/(2*101325./760.))
                else:
                    print(Lexp*dc*1e-3,5/(row['totalPressure']*101325./760.),15/(row['totalPressure']*101325./760.))

    #                plt.semilogy(rev[:,0],
    #                         rev[:,1])
    #                
    #                plt.semilogy(rev[:,0],
    #                        np.exp(b + m*rev[:,0]),'k-')
    #                print(row['dischargeCurrent'],row['massFlowRate'] / cc.sccm2eqA, row['cathode'], 1/m*dc)
                
                if row['cathode'] == 'NSTAR':
                    style = 'ko'
                    Idstyle = 'bo'
                elif row['cathode'] == 'NEXIS':
                    style = 'k^'
                    Idstyle = 'b^'
                elif row['cathode'] == 'JPL-1.5cm':
                    if mdot_sccm == 8.:
                        style = 'k<'
                        Idstyle = 'b<'
                    elif mdot_sccm == 10.:
                        style = 'k*'
                        Idstyle = 'b*'
                    elif mdot_sccm == 12.:
                        style = 'k>'
                        Idstyle = 'b>'
                elif row['cathode'] == 'Salhi-Xe':
                    style = 'kv'
                    Idstyle = 'bv'
                else:
                    style = 'k.'
                    Idstyle = 'b.'

                
                Lem0d = 0.0
                if not zerod_data[bcond].empty:
                    Pd = zerod_data[bcond].neutralPressureAverage/cc.Torr
                    Pd *= zerod_data[bcond].insertDiameter / 10
                    Pd = Pd.tolist()[0]
                        
                    Pderr = zerod_data[bcond].neutralPressureStd / cc.Torr
                    Pderr *= zerod_data[bcond].insertDiameter / 10
                    Pderr = Pderr.tolist()[0]
                    
                    ng = zerod_data[bcond].neutralPressureAverage / cc.kB / 3000.
                    Lem0d = Lem(ng,zerod_data[bcond].insertDiameter*1e-3,'Xe')
                    

                    
#                    print(row['cathode'],Id,mdot_sccm,Pd,Lexp,Lemerr)
                    
                    ax[0].errorbar(Pd,Lexp,xerr=Pderr,yerr=Lemerr,fmt=style)
                                        
#                    ax[1].plot(zerod_data[bcond].dischargeCurrent/zerod_data[bcond].massFlowRate,
#                             Lem0d/(zerod_data[bcond].insertDiameter*1e-3),Idstyle)
#                    ax[1].plot(zerod_data[bcond].dischargeCurrent,Lexp,style)
                    ax[1].errorbar(zerod_data[bcond].dischargeCurrent,
                      Lexp,
                      yerr=Lemerr,
                      fmt=style)
                    
                    Lem0d /= (zerod_data[bcond].insertDiameter*1e-3)

                else:
                    # If we have the correct mass flow rate then we can possibly do an interpolation
                    if not zerod_data[zdcond].empty:
#                        print(row['cathode'],Id,mdot_sccm)
                        Idvec = zerod_data[zdcond].dischargeCurrent
                        Pgvec = zerod_data[zdcond].neutralPressureAverage
                        
                        
                        Pg = np.interp(row['dischargeCurrent'],Idvec,Pgvec)
                        Pg /= cc.Torr
                        
                        Pd = Pg * row['insertDiameter'] / 10
                        
                        ng = Pg * cc.Torr / cc.kB / 3000.
                        Lem0d = Lem(ng,row['insertDiameter']*1e-3,row['gas'])
                       
#                        print(row['cathode'],Id,mdot_sccm,Pd,Lexp,Lemerr)
                        
                        ax[0].errorbar(Pd,Lexp,yerr=Lemerr,fmt=style)
#                        ax[1].plot(row['dischargeCurrent']/row['massFlowRate'],Lem0d/(row['insertDiameter']*1e-3),Idstyle)
                        ax[1].plot(row['dischargeCurrent'],Lexp,style)
    
                        Lem0d /= (row['insertDiameter']*1e-3)
                        
                Lem_theory = Lem_theory.append({'cathode':row['cathode'],
                               'dischargeCurrent':Id,
                               'massFlowRate': mdot,
                               'massFlowRateSccm': mdot_sccm,
                               'Lem':Lem0d},
                                ignore_index=True)
    
    for cathode in np.unique(Lem_theory.cathode):
        ser = Lem_theory[Lem_theory.cathode == cathode]
        Idvec = ser.dischargeCurrent
        Lemvec = ser.Lem
        mdotvec = ser.massFlowRateSccm
        
        Idvec = np.array(Idvec)
        Lemvec = np.array(Lemvec,dtype=np.float64)
        mdotvec = np.array(mdotvec,dtype=np.float64)
        
#        print(cathode,Lemvec)
        Idvec = Idvec[Lemvec > 0]
        mdotvec = mdotvec[Lemvec > 0]
        Lemvec = Lemvec[Lemvec > 0]
        
        
        if cathode == 'NSTAR':
            ax[1].plot(Idvec,Lemvec,'^-')
        elif cathode == 'NEXIS':
            ax[1].plot(Idvec,Lemvec,'o-')  
        elif cathode == 'JPL-1.5cm':
#            print(Idvec,mdotvec,Lemvec)
            ax[1].plot(Idvec[mdotvec == 8.],Lemvec[mdotvec == 8.],'>-')  
            ax[1].plot(Idvec[np.isclose(mdotvec,12.)],Lemvec[np.isclose(mdotvec, 12.)],'*-') 
        elif cathode == 'Salhi-Xe':
            ax[1].plot(Idvec,Lemvec,'v-')
        
def plot_temperature(alldata,zerod_data):

    TgK = 3000
    ngvec = np.logspace(18,23)
    
    fig, ax = plt.subplots(1,2)
    
    ax[0].semilogx(cc.kB * ngvec * TgK/cc.Torr * 1,Te_insert(ngvec,1e-2,'Xe'))
    ax[0].set_xlim([0.1,10])
    ax[0].set_ylim([0,5])
    
    ax[0].set_ylabel("Te (eV)")
    ax[0].set_xlabel("Pg*dc (Torr cm)")    
    ax[1].set_xlabel("Id")    
    ax[1].set_ylim([0,5])
    
    Te_theory = pd.DataFrame()
    
    ### Position vs. density
    for index, row in alldata.iterrows():
        if np.isnan(row['electronTemperature']).any():
            continue
        else:
            #print(row['cathode'])
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
            
            zdcond = massFlowCond
            zdcond &= (zerod_data.cathode == row['cathode']) 
            
            ### Grab experimental data
            Te_data = row['electronTemperature']
            dc = row['insertDiameter']
            
            # Insert stuff only
            try:
                if len(Te_data) > 1:
                    insert_Te = Te_data[Te_data[:,0]>0]
                    insert_Te = insert_Te[:,1]
                
                    ### Average
                    if len(insert_Te) > 1:
                        Texp = np.average(insert_Te)
                        
                        tmp = Te_data[Te_data[:,0]>0]
                        Texp = np.trapz(tmp[:,1],tmp[:,0]) / (tmp[-1,0]-tmp[0,0])
                        Terr = 0.5
                    else:
                        Texp = insert_Te
                        Terr = 0.5
            except:
                Texp = Te_data.reshape(-1)[0]
                Terr = 0.5
            
            
            ### Plot            
            if row['cathode'] == 'NSTAR':
                style = 'ko'
                Idstyle = 'bo'
            elif row['cathode'] == 'NEXIS':
                style = 'k^'
                Idstyle = 'b^'
            elif row['cathode'] == 'JPL-1.5cm':
                if mdot_sccm == 8.:
                    style = 'k<'
                    Idstyle = 'b<'
                elif mdot_sccm == 10.:
                    style = 'k*'
                    Idstyle = 'b*'
                elif mdot_sccm == 12.:
                    style = 'k>'
                    Idstyle = 'b>'
            elif row['cathode'] == 'Salhi-Xe':
                style = 'kv'
                Idstyle = 'bv'
            else:
                style = 'k.'
                Idstyle = 'b.'
                
            Te0d = 0.0
            ### Did we compute the zero-D model for the conditions of that particular cathode?
            if not zerod_data[bcond].empty:
                Pd = zerod_data[bcond].neutralPressureAverage/cc.Torr
                Pd *= zerod_data[bcond].insertDiameter / 10
                
                Pd = np.array(Pd) # There should be only one
                if len(Pd)>1:
                    print(Pd)
                    raise Exception('Found more than one valid pressure-diameter product!')
                else:
                    Pd = Pd[0]
                
                Pderr = zerod_data[bcond].neutralPressureStd / cc.Torr
                Pderr *= zerod_data[bcond].insertDiameter / 10
                Pderr = np.array(Pderr) # There should be only one
                if len(Pderr)>1:
                    raise Exception('Found more than one valid pressure-diameter product!')
                else:
                    Pderr = Pderr[0]
    
                
                ng = zerod_data[bcond].neutralPressureAverage / cc.kB / 3000.
                Te0d = Te_insert(ng,zerod_data[bcond].insertDiameter*1e-3,'Xe')
               
                print(row['cathode'],Id,mdot_sccm,Pd,Texp,Terr)
#                print(Pd,Texp)
                ax[0].errorbar(Pd,Texp,yerr=Terr,xerr=Pderr,fmt=style)
                
#                ax[1].plot(zerod_data[bcond].dischargeCurrent,
#                         Te0d,style)
                ax[1].plot(zerod_data[bcond].dischargeCurrent,
                          Texp,style)
                
            ### If not...
            else:
                # If we have the correct mass flow rate then we can possibly do an interpolation based on current
                if not zerod_data[zdcond].empty:
                    
                    Idvec = zerod_data[zdcond].dischargeCurrent
                    Pgvec = zerod_data[zdcond].neutralPressureAverage
                    
                    Pg = np.interp(row['dischargeCurrent'],Idvec,Pgvec)
                    Pg /= cc.Torr
                    
                    if row['cathode'] == 'Salhi-Xe':
                        print(row['dischargeCurrent'],Idvec)
                    
                    Pd = Pg * row['insertDiameter'] / 10
                    print(row['cathode'],Id,mdot_sccm,Pd,Texp,Terr)
                    
                    ng = Pg * cc.Torr / cc.kB / 3000.
                    Te0d = Te_insert(ng,row['insertDiameter']*1e-3,row['gas'])
                    
                    ax[0].errorbar(Pd,Texp,yerr=Terr,fmt=style)
#                    ax[1].plot(row['dischargeCurrent'],Te0d,style)
                    ax[1].plot(row['dischargeCurrent'],
                          Texp,style)
    #                ng = Pg * cc.Torr / cc.kB / 3000.
    #                Lem0d = Lem(ng,row['insertDiameter']*1e-3,row['gas'])
    #               
    #                plt.plot(row['dischargeCurrent']/row['massFlowRate'],Lem0d/(row['insertDiameter']*1e-3),style)   

            Te_theory = Te_theory.append({'cathode':row['cathode'],
                               'dischargeCurrent':Id,
                               'massFlowRate': mdot,
                               'massFlowRateSccm': mdot_sccm,
                               'Te':Te0d},
                                ignore_index=True)         
            
#                print(Te0d)

    for cathode in np.unique(Te_theory.cathode):
        ser = Te_theory[Te_theory.cathode == cathode]
        Idvec = ser.dischargeCurrent
        Tevec = ser.Te
        mdotvec = ser.massFlowRateSccm
        
        Idvec = np.array(Idvec)
        Tevec = np.array(Tevec,dtype=np.float64)
        mdotvec = np.array(mdotvec,dtype=np.float64)
        
#        print(cathode,Lemvec)
        Idvec = Idvec[Tevec > 0]
        mdotvec = mdotvec[Tevec > 0]
        Tevec = Tevec[Tevec > 0]
        
        
        if cathode == 'NSTAR':
            ax[1].plot(Idvec,Tevec,'^-')
        elif cathode == 'NEXIS':
            ax[1].plot(Idvec,Tevec,'o-')  
        elif cathode == 'JPL-1.5cm':
#            print(Idvec,mdotvec,Lemvec)
            ax[1].plot(Idvec[mdotvec == 8.],Tevec[mdotvec == 8.],'>-')  
            ax[1].plot(Idvec[np.isclose(mdotvec,12.)],Tevec[np.isclose(mdotvec, 12.)],'*-') 
        elif cathode == 'Salhi-Xe':
            ax[1].plot(Idvec,Tevec,'v-')


zerod_data = build_zerod_dataframe()
alldata = import_data("assembled.csv")                                

plot_density(alldata,zerod_data)
#plot_temperature(alldata,zerod_data)
