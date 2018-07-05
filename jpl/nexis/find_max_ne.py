import numpy as np
import matplotlib.pyplot as plt

### Find thhe max electron density and corresponding location from the ne vs x plots
data = np.genfromtxt("ne_vs_x_Id-25A_mdot-5sccm-10sccm.csv",delimiter=",",skip_header=14,names=True)
data5 = data[data['mdot']==5]
data10  = data[data['mdot']==10]

r_ins = 1.2e-2

print("Id,mdot,ne_max,x(ne_max),alpha,alpha*r_ins")
for data in [data5,data10]:
    xvec = data['x']
    yvec = data['ne']
    
    mdot = np.unique(data['mdot'])[0]
    Id = np.unique(data['Id'])[0]
    
    ne_max = np.max(yvec)*1e20
    idx = np.argmax(yvec)
    x_max = xvec[idx] * 10 # Convert from cm to mm
    
    if mdot == 5.0:
        a,b = np.polyfit(xvec[xvec>1],np.log(yvec[xvec>1]*1e20),1)
        plt.semilogy(xvec,yvec*1e20,'C0')
        plt.semilogy(xvec,np.exp(a*xvec+b),'C0--')
    else:
        a,b = np.polyfit(xvec[ (xvec>0.75) & (xvec<2.0)],np.log(yvec[ (xvec>0.75) & (xvec<2.0) ]*1e20),1)
        plt.semilogy(xvec,yvec*1e20,'C1')
        plt.semilogy(xvec,np.exp(a*xvec+b),'C1--') 

    
    print(Id,mdot,ne_max,x_max,np.abs(a)*1e2,np.abs(a)*1e2*r_ins)
