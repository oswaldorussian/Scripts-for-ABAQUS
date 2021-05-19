# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from abaqus import *
from part import *
from section import *
from assembly import *
from job import *
from visualization import *
from connectorBehavior import *
from odbAccess import *
import abaqusMath
from numpy import*
import xyPlot

#define model database

#MyMdb=openMdb('Debonding.cae')

#define interfacial fracture energies to try

modelList=[20, 27, 30, 40, 50, 60, 70, 80]

for i in range(0,len(modelList)):
    
    #make model name string

    modelName = str(modelList[i])
	  
    #define interfacial parameters
    
    mdb.models[modelName+'mm'].sections['Cohesive_Failure'].setValues(
    material='Cohesive_Failure', response=TRACTION_SEPARATION, 
    initialThicknessType=GEOMETRY, outOfPlaneThickness=None)
	
    mdb.models[modelName+'mm'].materials['Cohesive_Failure'].quadsDamageInitiation.setValues(
    table=((27.46, 24.71, 24.71), ))
	
    mdb.models[modelName+'mm'].materials['Cohesive_Failure'].quadsDamageInitiation.damageEvolution.setValues(
    type=ENERGY, table=((1.6, ), ))
	
    mdb.models[modelName+'mm'].materials['Cohesive_Failure'].elastic.setValues(table=((
    2960.0, 1088.0, 1088.0), ))
    
    #define material parameters
    
    mdb.models[modelName+'mm'].materials['Steel'].elastic.setValues(table=((210000, 
    0.3), ))
    
    mdb.models[modelName+'mm'].materials['CFRP'].elastic.setValues(table=((41500.0, 
    4567.0, 4567.0, 0.3, 0.3, 0.3, 1397.0, 1397.0, 1756.0), ))
    
    #assign load values
    
    mdb.models[modelName+'mm'].loads['Load-1'].setValues(magnitude=-241)
    
    #name the analysis job
        
    myJob = mdb.Job(name=modelName+'mm_217_Debonding',model=modelName+'mm')