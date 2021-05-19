"""
Created on Sat Apr 25 15:40:50 2020

@author: ojrussia
"""

import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt

#Define number of simulations

nSim=5

#SWT calculations

def func(x,*args):
    return (data[i][0])**2/data[i][1]*(2*x)**(2*data[i][2])+data[i][3]*data[i][0]*(2*x)**(data[i][2]+data[i][4])-(data[i][5]-data[i][6])/2*data[i][7]

initialGuess=4

#Parameters for Al6082-T6 aluminum and experiment from Wu et al. (2010)

data=[[485,68000,-0.0695,0.733,-0.827,0.0184457,0.0142466,332.508,17.41],
      [485,68000,-0.0695,0.733,-0.827,0.0170299,0.0129812,332.707,16.78],
      [485,68000,-0.0695,0.733,-0.827,0.0133815,0.00978397,332.358,14.92],
      [485,68000,-0.0695,0.733,-0.827,0.00973316,0.00670391,329.552,12.56],
      [485,68000,-0.0695,0.733,-0.827,0.00795704,0.00525757,325.47,11.20]]

#SWT solution vector

swtVec=np.zeros((nSim,2))

#Solve the SWT equation for each simulation

for i in range (len(data)):
    
    x=opt.fsolve(func,initialGuess,args=[data[i]])
    swtVec[i][0]=data[i][8]
    swtVec[i][1]=x

#Morrow Elastic calculation

def func(x,*args):
    return (data[i][0]-(data[i][1]+data[i][2])/2)/data[i][3]*(2*x)**(data[i][4])+data[i][5]*(2*x)**(data[i][6])-(data[i][7]-data[i][8])/2

initialGuess=4

#Parameters for Al6082-T6 aluminum and experiment from Wu et al. (2010)

data=[[485,332.508,30.3632,68000,-0.0695,0.733,-0.827,0.0184457,0.0142466,17.41],
      [485,332.707,41.383,68000,-0.0695,0.733,-0.827,0.0170299,0.0129812,16.78],
      [485,332.358,73.4937,68000,-0.0695,0.733,-0.827,0.0133815,0.00978397,14.92],
      [485,329.552,111.581,68000,-0.0695,0.733,-0.827,0.00973316,0.00670391,12.56],
      [485,325.47,131.229,68000,-0.0695,0.733,-0.827,0.00795704,0.00525757,11.20]]

#Morrow elastic solution vector

moelVec=np.zeros((nSim,2))

#Solve the Morrow elastic equation for each simulation

for i in range (len(data)):
    
    x=opt.fsolve(func,initialGuess,args=[data[i]])
    moelVec[i][0]=data[i][9]
    moelVec[i][1]=x

#Morrow Elastoplastic calculation

def func(x,*args):
    return (data[i][0]-(data[i][1]+data[i][2])/2)/data[i][3]*(2*x)**(data[i][4])+data[i][5]*((data[i][0]-(data[i][1]+data[i][2])/2)/data[i][0])**(data[i][6]/data[i][4])*(2*x)**(data[i][6])-(data[i][7]-data[i][8])/2

initialGuess=4

#Parameters for Al6082-T6 aluminum and experiment from Wu et al. (2010)

data=[[485,332.508,30.3632,68000,-0.0695,0.733,-0.827,0.0184457,0.0142466,17.41],
      [485,332.707,41.383,68000,-0.0695,0.733,-0.827,0.0170299,0.0129812,16.78],
      [485,332.358,73.4937,68000,-0.0695,0.733,-0.827,0.0133815,0.00978397,14.92],
      [485,329.552,111.581,68000,-0.0695,0.733,-0.827,0.00973316,0.00670391,12.56],
      [485,325.47,131.229,68000,-0.0695,0.733,-0.827,0.00795704,0.00525757,11.20]]

#Morrow elastoplastic solution vector

moelplVec=np.zeros((nSim,2))

#Solve the Morrow elastoplastic equation for each simulation

for i in range (len(data)):
    
    x=opt.fsolve(func,initialGuess,args=[data[i]])
    moelplVec[i][0]=data[i][9]
    moelplVec[i][1]=x

#Write experimental data

expVec=np.array([[17.41,17.41,12.56,12.56,11.20,11.20],[60000,32000,611000,580000,1150000,960000]])
expVec=np.transpose(expVec)

print(expVec)

#Print solution vectors
    
print('SWT Solution:')
print(swtVec)
print('Morrow Elastic Solution:')
print(moelVec)
print('Morrow Elastoplastic Solution:')
print(moelplVec)

#Get data in thousands of cycles for plotting purposes
    
expVec[:,1]=expVec[:,1]/1000
swtVec[:,1]=swtVec[:,1]/1000
moelVec[:,1]=moelVec[:,1]/1000
moelplVec[:,1]=moelplVec[:,1]/1000

#Create figure

fig=plt.figure()
ax=plt.axes(xlim=(0,2000), ylim=(10,20))
ax.set_facecolor('xkcd:light grey blue')
plt.grid('on')


#Plot results
plt.plot(expVec[:,1],expVec[:,0], 'kx',label='Experimental data - Wu et al. (2010)')
plt.plot(swtVec[:,1],swtVec[:,0], 'yo-',label='SWT Equation')
plt.plot(moelVec[:,1],moelVec[:,0], 'bo-',label='Morrow Elastic Equation')
plt.plot(moelplVec[:,1],moelplVec[:,0], 'ro-',label='Morrow Elastoplastic Equation')
#plt.axis([0,2000,7,15])
plt.xlabel('Cycles to crack initiation (thousands)',fontweight='bold')
plt.ylabel('Stress range (MPa)', fontweight='bold')
#plt.grid(True)
plt.legend()