import numpy as np

### Find thhe max electron density and corresponding location from the ne vs x plots
data = np.genfromtxt("xenon_ne_vs_x_do-0.76mm_Id-2.3A.csv",delimiter=",",skip_header=13,names=True)
data19 = data[data['phi_wf']==1.9]
data25  = data[data['phi_wf']==2.5]

Id = 2.3 # A

print("Id,ne_max,x(ne_max)")
for data in [data19,data25]:
    xvec = data['x']
    yvec = data['ne']
        
    ne_max = np.max(yvec)*1e19
    idx = np.argmax(yvec)
    x_max = xvec[idx] # Convert from cm to mm

    print(Id,ne_max,x_max)
