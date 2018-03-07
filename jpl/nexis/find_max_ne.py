import numpy as np

### Find thhe max electron density and corresponding location from the ne vs x plots
data = np.genfromtxt("ne_vs_x_Id-25A_mdot-5sccm-10sccm.csv",delimiter=",",skip_header=14,names=True)
data5 = data[data['mdot']==5]
data10  = data[data['mdot']==10]


print("Id,mdot,ne_max,x(ne_max)")
for data in [data5,data10]:
    xvec = data['x']
    yvec = data['ne']
    
    mdot = np.unique(data['mdot'])[0]
    Id = np.unique(data['Id'])[0]
    
    ne_max = np.max(yvec)*1e20
    idx = np.argmax(yvec)
    x_max = xvec[idx] * 10 # Convert from cm to mm

    print(Id,mdot,ne_max,x_max)
