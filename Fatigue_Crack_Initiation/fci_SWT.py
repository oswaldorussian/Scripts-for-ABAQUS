"""
Created on Sat Apr 25 15:40:50 2020

@author: ojrussia
"""


import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt

#Define number of simulations

nSR=3

#Define constant parameters

fsc = 1014
E = 210000
fse = -0.132
fdc = 0.271
fde = -0.451

#Define variable parameters

params = np.array([(0.0362733,0.0243432,490.53,155),(0.0622307,0.0462127,505.83,186),(0.106567,0.0862458,534.174,217),\
                   (0.0257846,0.0163262,443.196,155),(0.043997,0.0314708,446.478,186),(0.0767478,0.0608063,463.809,217),\
                   (0.0108759,0.0071225,487.13,155),(0.0190678,0.0138665,494.75,186),(0.0359931,0.0291081,538.02,217),\
                   (0.0123,0.00840192,455.37,155),(0.0224213,0.0169391,456.576,186),(0.0485937,0.0416136,471.764,217),\
                   (0.0180091,0.0124529,388.89,155),(0.0348014,0.0273631,391.995,186),(0.0954281,0.0862097,431.447,217)])

##########################################################################################################

#Initialize final solution vector
    
swtVec=np.zeros((len(params),2))

for j in range(int(len(params)/nSR)):

    #SWT calculations
    
    def func(x,*args):
        return (data[i][0])**2/data[i][1]*(2*x)**(2*data[i][2])+data[i][3]*data[i][0]*(2*x)**(data[i][2]+data[i][4])-(data[i][5]-data[i][6])/2*data[i][7]
    
    initialGuess=4
    
    #Parameters for A36 steel
    
    data=[[fsc,E,fse,fdc,fde,params[nSR*j,0],params[nSR*j,1],params[nSR*j,2],params[nSR*j,3]],
          [fsc,E,fse,fdc,fde,params[nSR*j+1,0],params[nSR*j+1,1],params[nSR*j+1,2],params[nSR*j+1,3]],
          [fsc,E,fse,fdc,fde,params[nSR*j+2,0],params[nSR*j+2,1],params[nSR*j+2,2],params[nSR*j+2,3]]]
    
    #SWT temporary solution vector
    
    swtVect_temp=np.zeros((nSR,2))
    
    #Solve the SWT equation for each simulation
    
    for i in range (len(data)):
        
        x=opt.fsolve(func,initialGuess,args=[data[i]])
        
        swtVect_temp[i][0]=data[i][8]
        swtVect_temp[i][1]=x
        
    #SWT final solution vector
    
    swtVec[nSR*j] = swtVect_temp[0]
    swtVec[nSR*j+1] = swtVect_temp[1]
    swtVec[nSR*j+2] = swtVect_temp[2]


#Print solution vectors
    
print('SWT Solution:')
print(swtVec)

#Get data in thousands of cycles for plotting purposes

swtVec[:,1]=swtVec[:,1]/1000

#Create figure

fig=plt.figure()
ax=plt.axes(xlim=(0,20), ylim=(100,240))
ax.set_facecolor('xkcd:light grey blue')
plt.grid('on')


#Plot results

plt.plot(swtVec[0:3,1],swtVec[0:3,0], 'ro-',label='SWT Equation, 2-mm SDH')
plt.plot(swtVec[3:6,1],swtVec[3:6,0], 'bo-',label='SWT Equation, 4-mm SDH')
plt.plot(swtVec[6:9,1],swtVec[6:9,0], 'yo-',label='SWT Equation, 8-mm SDH')
plt.plot(swtVec[9:12,1],swtVec[9:12,0], 'co-',label='SWT Equation, 12-mm SDH')
plt.plot(swtVec[12:15,1],swtVec[12:15,0], 'go-',label='SWT Equation, 16-mm SDH')

#plt.axis([0,2000,7,15])
plt.xlabel('Cycles to crack initiation (thousands)',fontweight='bold')
plt.ylabel('Stress range (MPa)', fontweight='bold')
#plt.grid(True)
plt.legend()