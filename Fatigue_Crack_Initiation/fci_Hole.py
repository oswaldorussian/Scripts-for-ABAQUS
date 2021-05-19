"""
Created on Sat Apr 25 15:40:50 2020

@author: ojrussia
"""

import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt

#Define number of simulations

nSim=2

##########################################################################################################

#SWT calculations

def func(x,*args):
    return (data[i][0])**2/data[i][1]*(2*x)**(2*data[i][2])+data[i][3]*data[i][0]*(2*x)**(data[i][2]+data[i][4])-(data[i][5]-data[i][6])/2*data[i][7]

initialGuess=4

#Parameters for A36 steel

data=[[1014,210000,-0.132,0.271,-0.451,0.0108759,0.0071225,487.13,155],
      [1014,210000,-0.132,0.271,-0.451,0.0359931,0.0291081,538.02,217]]

#SWT solution vector

swtVec=np.zeros((nSim,2))

#Solve the SWT equation for each simulation

for i in range (len(data)):
    
    x=opt.fsolve(func,initialGuess,args=[data[i]])
    swtVec[i][0]=data[i][8]
    swtVec[i][1]=x

##########################################################################################################

#Morrow Elastic calculation

def func(x,*args):
    return (data[i][0]-(data[i][1]+data[i][2])/2)/data[i][3]*(2*x)**(data[i][4])+data[i][5]*(2*x)**(data[i][6])-(data[i][7]-data[i][8])/2

initialGuess=4

#Parameters for A36 steel

data=[[1014,487.13,-349.274,210000,-0.132,0.271,-0.451,0.0108759,0.0071225,155],
      [1014,507.897,-466.821,210000,-0.132,0.271,-0.451,0.0359931,0.0291081,217]]

#Morrow elastic solution vector

moelVec=np.zeros((nSim,2))

#Solve the Morrow elastic equation for each simulation

for i in range (len(data)):
    
    x=opt.fsolve(func,initialGuess,args=[data[i]])
    moelVec[i][0]=data[i][9]
    moelVec[i][1]=x

##########################################################################################################

#Morrow Elastoplastic calculation

def func(x,*args):
    return (data[i][0]-(data[i][1]+data[i][2])/2)/data[i][3]*(2*x)**(data[i][4])+data[i][5]*((data[i][0]-(data[i][1]+data[i][2])/2)/data[i][0])**(data[i][6]/data[i][4])*(2*x)**(data[i][6])-(data[i][7]-data[i][8])/2

initialGuess=4

#Parameters for A36 steel

data=[[1014,487.13,-349.274,210000,-0.132,0.271,-0.451,0.0108759,0.0071225,155],
      [1014,507.897,-466.821,210000,-0.132,0.271,-0.451,0.0359931,0.0291081,217]]

#Morrow elastoplastic solution vector

moelplVec=np.zeros((nSim,2))

#Solve the Morrow elastoplastic equation for each simulation

for i in range (len(data)):
    
    x=opt.fsolve(func,initialGuess,args=[data[i]])
    moelplVec[i][0]=data[i][9]
    moelplVec[i][1]=x

##########################################################################################################

##Write experimental data
#
expVec=np.array([[155,155,155,217,217,217],[15000,16759,15865,2545,2621,2777]])
expVec=np.transpose(expVec)

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
ax=plt.axes(xlim=(0,160), ylim=(100,250))
ax.set_facecolor('xkcd:light grey blue')
plt.grid('on')


#Plot results
plt.plot(expVec[:,1],expVec[:,0], 'kx',label='Experimental data')
plt.plot(swtVec[:,1],swtVec[:,0], 'yo-',label='SWT Equation')
plt.plot(moelVec[:,1],moelVec[:,0], 'bo-',label='Morrow Elastic Equation')
plt.plot(moelplVec[:,1],moelplVec[:,0], 'ro-',label='Morrow Elastoplastic Equation')
#plt.axis([0,2000,7,15])
plt.xlabel('Cycles to crack initiation (thousands)',fontweight='bold')
plt.ylabel('Stress range (MPa)', fontweight='bold')
#plt.grid(True)
plt.legend()