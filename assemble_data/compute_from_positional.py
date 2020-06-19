import numpy as np

def compute_attachment_length(ne_data, dc, idxmin=None, idxmax=None):
    ''' Calculates the attachment length as the insert density exponential 
    decay length scale. The attachment length is normalized to the insert 
    diameter.
    Inputs:
        - ne_data: the density data ne vs position. Assumes that it is a Nx2 
        array where the first column is the position in mm, and the second 
        column is the density in 1/m3
        - dc: insert diameter, mm
        - idxmin, idxmax: the indices to limit the data to the exponential
        decay of the density
    Returns:
        - Emission length
        - Error of the emission length
    ''' 
    # Grab only insert data
    insert_ne = ne_data[ne_data[:,0]>0]

    # Grab only the density decay points (back of the curve)
    if idxmin and idxmax:
        rev = insert_ne[idxmin:idxmax]
    elif idxmin:
        rev = insert_ne[idxmin:]
    elif idxmax:
        rev = insert_ne[:idxmax]
    
#    if row['cathode'] == 'NSTAR':
#        rev = insert_ne[-50:]
#    elif row['cathode'] == 'NEXIS':
#        rev = insert_ne[-40:-10]
#    elif row['cathode'] == 'JPL-1.5cm':
#        npoints = find_JPL_indexing(Id,mdot_sccm)
#        rev = insert_ne[-npoints:]
#    elif row['cathode'] == 'Salhi-Xe':
#        rev = insert_ne[:-1]
    rev[:,0] /= dc
    rev[:,1] /= np.max(insert_ne[:,1])
    
    # Fit XP data
    ret = np.polyfit(rev[:,0],np.log(rev[:,1]),1,full=True,cov=True)
    m,b = ret[0]
    
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
    
    return Lexp, Lemerr

def compute_average_temperature(Te_data, dc):
    ''' Calculates the electron temperature as the 1D average of the 
    temperature data if more than multiple data points are available.
    Inputs:
        - Te_data: the density data ne vs position. Assumes that it is a Nx2 
        array where the first column is the position in mm, and the second 
        column is the density in eV
        - dc: insert diameter, mm
    Returns:
        - Average electron temperature
        - Error of the electron temperature
    '''     
    # Insert stuff only
    Texp = -1.0
    Terr = -1.0
    try:
        if len(Te_data) > 1:
            insert_Te = Te_data[Te_data[:,0]>0]
            insert_Te = insert_Te[:,1]
        
            ### Line average (integral)
            if len(insert_Te) > 1:
                tmp = Te_data[Te_data[:,0]>0]
                Texp = np.trapz(tmp[:,1],tmp[:,0]) / (tmp[-1,0]-tmp[0,0])
                Terr = 0.5
            else:
                Texp = insert_Te
                Terr = 0.5
    except:
        Texp = Te_data.reshape(-1)[0]
        Terr = 0.5
        
    return Texp, Terr


def compute_from_positional(df):
    ''' Calculates the decay length and line-averaged electron temperature
    from the positional data.
    '''        
    ### Iterate only on the part of the dataframe that has electron density
    idxlist = ['cathode','idxmin','idxmax','insertDiameter','electronDensity']
    howna = ['electronDensity']
    tdf = df[idxlist].dropna(subset=howna)
    for idx,row in tdf.iterrows():
        ne_data = row['electronDensity']
        # Cast idx as (int). The dataframe has the column type as float because
        # of NaN's that are present. Make sure we catch that exception
        try:
            idxmin = (int)(row['idxmin'])
        except ValueError:
            idxmin = np.nan
            
        try:
            idxmax = (int)(row['idxmax'])
        except ValueError:
            idxmax = np.nan
            
        dc = row['insertDiameter']
                
        if np.isnan(idxmax) and np.isnan(idxmin):
            raise ValueError("Cannot have both idxmin and idxmax as NaN!")
        elif np.isnan(idxmax) and ~np.isnan(idxmin):
            Lem_xp, Lem_err = compute_attachment_length(ne_data, dc, idxmin=idxmin)
        elif ~np.isnan(idxmax) and np.isnan(idxmin):
            Lem_xp, Lem_err = compute_attachment_length(ne_data, dc, idxmax=idxmax)
        else:
            Lem_xp, Lem_err = compute_attachment_length(ne_data, dc, idxmin=idxmin,idxmax=idxmax)
            
        df.loc[idx,'attachmentLength'] = Lem_xp
        df.loc[idx,'attachmentLength_err'] = Lem_err

    idxlist = ['cathode','electronTemperature','electronTemperatureAverage','insertDiameter']
    howna = ['electronTemperature']
    tdf = df[idxlist].dropna(subset=howna)
    
    for idx,row in tdf.iterrows():
        Te_data = row['electronTemperature']
#        Te_data = Te_data.T
        
        dc = row['insertDiameter'] 
        
#        if row['cathode'] == 'NEXIS' and ~np.isnan(Te_data.all()):
#            print(Te_data.shape)
        
        Te_xp, Te_err = compute_average_temperature(Te_data, dc)
#        print(row['cathode'],Te_xp,Te_err)
        
        # If we don't already have data there?
        if np.isnan(row['electronTemperatureAverage']):
            print(row['cathode'],idx,Te_xp,Te_err)
            df.loc[idx,'electronTemperatureAverage'] = Te_xp
            df.loc[idx,'electronTemperatureAverage_err'] = Te_err        
        
    return df
    