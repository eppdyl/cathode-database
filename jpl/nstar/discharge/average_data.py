import csv
import re
import numpy as np

f='implemented_models/data/nstar/discharge/phip_vs_x_TH8-TH15.tsv'
csvfile = open(f,'r')
reader = csv.reader(csvfile,delimiter='\t')
next(reader,None)

for row in reader:
    xvec = (row[0].split())[2]
    xvec = re.sub('[\["\]]','',xvec)
    xvec = [np.float64(x) for x in xvec.split(',')]    
    
    yvec = (row[0].split())[3]
    yvec = re.sub('[\["\]]','',yvec)
    yvec = [np.float64(y) for y in yvec.split(',')] 
    
    xvec = np.array(xvec)
    yvec = np.array(yvec)
    
    
    integral  = np.trapz(yvec[xvec>=0],xvec[xvec>=0])
    fac = 1./(xvec[xvec>=0][-1] - xvec[xvec>=0][0])
    
    print "Average potential"
    print fac * integral
    

f='implemented_models/data/nstar/discharge/Te_vs_x_TH8-TH15.tsv'
csvfile = open(f,'r')
reader = csv.reader(csvfile,delimiter='\t')
next(reader,None)

for row in reader:
    xvec = (row[0].split())[2]
    xvec = re.sub('[\["\]]','',xvec)
    xvec = [np.float64(x) for x in xvec.split(',')]    
    
    yvec = (row[0].split())[3]
    yvec = re.sub('[\["\]]','',yvec)
    yvec = [np.float64(y) for y in yvec.split(',')] 
    
    xvec = np.array(xvec)
    yvec = np.array(yvec)
    
    
    integral  = np.trapz(yvec[xvec>=0],xvec[xvec>=0])
    fac = 1./(xvec[xvec>=0][-1] - xvec[xvec>=0][0])
    
    print "Average temperature"
    print fac * integral
    
f='implemented_models/data/nstar/discharge/ne_vs_x_TH8-TH15.tsv'
csvfile = open(f,'r')
reader = csv.reader(csvfile,delimiter='\t')
next(reader,None)

for row in reader:
    xvec = (row[0].split())[2]
    xvec = re.sub('[\["\]]','',xvec)
    xvec = [np.float64(x) for x in xvec.split(',')]    
    
    yvec = (row[0].split())[3]
    yvec = re.sub('[\["\]]','',yvec)
    yvec = [np.float64(y) for y in yvec.split(',')] 
    
    xvec = np.array(xvec)
    yvec = np.array(yvec)
    
    
    integral  = np.trapz( (10**yvec[xvec>=0])*1e6,xvec[xvec>=0])
    fac = 1./(xvec[xvec>=0][-1] - xvec[xvec>=0][0])
    
    print "Average density"
    print fac * integral
    
