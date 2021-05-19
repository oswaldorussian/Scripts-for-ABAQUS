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

MyMdb=openMdb('Trials.cae')

#define interfacial fracture energies to try

energyList=[6.25,6,5.75,5.5,5.25,5,4.75,4.5,4.25,4,3.75,3.5,3.25,3,2.75,2.5,2.25,1.75,1.5]

for i in range(0,len(energyList)):
    
    #make counter string

    counter=str(i+1)
    
    #define interfacial fracture energy
    
    mdb.models['SWL150_Coh_Int'].materials['Adhesive_Interfacial'].quadsDamageInitiation.damageEvolution.setValues(
    type=ENERGY, table=((energyList[i], ), ))
    
    #create job
            
    mdb.Job(contactPrint=OFF, description='', echoPrint=OFF, explicitPrecision=
        SINGLE, historyPrint=OFF, memory=90, memoryUnits=PERCENTAGE, model=
        'SWL150_Coh_Int', modelPrint=OFF, multiprocessingMode=
        DEFAULT,name='SWL150_Trials_'+counter,nodalOutputPrecision=SINGLE, 
        numCpus=4,numDomains=4,parallelizationMethodExplicit=DOMAIN, scratch='', 
        type=ANALYSIS,userSubroutine='')
        
    #name the analysis job
        
    myJob = mdb.Job(name='SWL150_Trials_'+counter,model='SWL150_Coh_Int')
    
    #submit the job

    myJob.submit()
    
    #wait for job completion
    
    myJob.waitForCompletion()
    
    #access output database

    mySession = session.openOdb(name='C:\Temp\Abaqus\DLS_SLS\OR\Current\SWL150_Trials_'+counter+'.odb')

    odb = session.odbs['C:\Temp\Abaqus\DLS_SLS\OR\Current\SWL150_Trials_'+counter+'.odb']
    
    #Compile reaction data
    
    xy_result = session.XYDataFromHistory(name='Displacement', odb=odb, 
        outputVariableName='Spatial displacement: U1 PI: STEEL-2 Node 4961 in NSET DISPLACEMENT', 
        steps=('Step-1', ), )
    
    session.XYDataFromHistory(name='Reaction-1', odb=odb, 
        outputVariableName='Reaction force: RF1 PI: STEEL-1 Node 1 in NSET REACTION', 
        steps=('Step-1', ), )
    session.XYDataFromHistory(name='Reaction-2', odb=odb, 
        outputVariableName='Reaction force: RF1 PI: STEEL-1 Node 452 in NSET REACTION', 
        steps=('Step-1', ), )
    session.XYDataFromHistory(name='Reaction-3', odb=odb, 
        outputVariableName='Reaction force: RF1 PI: STEEL-1 Node 903 in NSET REACTION', 
        steps=('Step-1', ), )
    session.XYDataFromHistory(name='Reaction-4', odb=odb, 
        outputVariableName='Reaction force: RF1 PI: STEEL-1 Node 1354 in NSET REACTION', 
        steps=('Step-1', ), )
    session.XYDataFromHistory(name='Reaction-5', odb=odb, 
        outputVariableName='Reaction force: RF1 PI: STEEL-1 Node 1805 in NSET REACTION', 
        steps=('Step-1', ), )
    session.XYDataFromHistory(name='Reaction-6', odb=odb, 
        outputVariableName='Reaction force: RF1 PI: STEEL-1 Node 2256 in NSET REACTION', 
        steps=('Step-1', ), )
    session.XYDataFromHistory(name='Reaction-7', odb=odb, 
        outputVariableName='Reaction force: RF1 PI: STEEL-1 Node 2707 in NSET REACTION', 
        steps=('Step-1', ), )
    session.XYDataFromHistory(name='Reaction-8', odb=odb, 
        outputVariableName='Reaction force: RF1 PI: STEEL-1 Node 3158 in NSET REACTION', 
        steps=('Step-1', ), )
    session.XYDataFromHistory(name='Reaction-9', odb=odb, 
        outputVariableName='Reaction force: RF1 PI: STEEL-1 Node 3609 in NSET REACTION', 
        steps=('Step-1', ), )
    session.XYDataFromHistory(name='Reaction-10', odb=odb, 
        outputVariableName='Reaction force: RF1 PI: STEEL-1 Node 4060 in NSET REACTION', 
        steps=('Step-1', ), )
    session.XYDataFromHistory(name='Reaction-11', odb=odb, 
        outputVariableName='Reaction force: RF1 PI: STEEL-1 Node 4511 in NSET REACTION', 
        steps=('Step-1', ), )
    
    #Extract Displacement Data
    
    xy1 = session.xyDataObjects['Displacement']
    xy2 = session.xyDataObjects['Reaction-1']
    xy3 = session.xyDataObjects['Reaction-2']
    xy4 = session.xyDataObjects['Reaction-3']
    xy5 = session.xyDataObjects['Reaction-4']
    xy6 = session.xyDataObjects['Reaction-5']
    xy7 = session.xyDataObjects['Reaction-6']
    xy8 = session.xyDataObjects['Reaction-7']
    xy9 = session.xyDataObjects['Reaction-8']
    xy10 = session.xyDataObjects['Reaction-9']
    xy11 = session.xyDataObjects['Reaction-10']
    xy12 = session.xyDataObjects['Reaction-11']
    
    #Create L-D curve
    
    xy41 = combine(xy1, -2*(xy2+ xy3+ xy4+ xy5+ xy6+ xy7+ xy8+ xy9+ xy10+ xy11+ 
        xy12)/1000)
    xy41.setValues(
        sourceDescription='combine ( "Displacement",-2*sum("Reaction-1", "Reaction-2", "Reaction-3", "Reaction-4", "Reaction-5", "Reaction-6", "Reaction-7", "Reaction-8", "Reaction-9", "Reaction-10", "Reaction-11")/1000 )')
    tmpName = xy41.name
    session.xyDataObjects.changeKey(tmpName, 'SWL150_Trials_'+counter)
	
	#Append L-D curves
    
    xyp = session.xyPlots['XYPlot-1']
    chartName = xyp.charts.keys()[0]
    chart = xyp.charts[chartName]
    xy1 = session.xyDataObjects['SWL150_Trials_'+counter]
    c1 = session.Curve(xyData=xy1)
    chart.setValues(curvesToPlot=(c1, ), appendMode=True)
    session.viewports['Viewport: 1'].setValues(displayedObject=xyp)
#        
#    xyp = session.xyPlots['XYPlot-1']
#    chartName = xyp.charts.keys()[0]
#    chart = xyp.charts[chartName]
#    xy1 = session.xyDataObjects['G-WL-150-Experimental-1']
#    c1 = session.Curve(xyData=xy1)
#    chart.setValues(curvesToPlot=(c1, ), appendMode=True)
#    
#    xyp = session.xyPlots['XYPlot-1']
#    chartName = xyp.charts.keys()[0]
#    chart = xyp.charts[chartName]
#    xy1 = session.xyDataObjects['G-WL-150-Experimental-2']
#    c1 = session.Curve(xyData=xy1)
#    chart.setValues(curvesToPlot=(c1, ), appendMode=True)
#    
#    xyp = session.xyPlots['XYPlot-1']
#    chartName = xyp.charts.keys()[0]
#    chart = xyp.charts[chartName]
#    xy1 = session.xyDataObjects['G-WL-150-Experimental-3']
#    c1 = session.Curve(xyData=xy1)
#    chart.setValues(curvesToPlot=(c1, ), appendMode=True)
    
    #Delete junk
    
    del session.xyDataObjects['Displacement']
    del session.xyDataObjects['Reaction-1']
    del session.xyDataObjects['Reaction-2']
    del session.xyDataObjects['Reaction-3']
    del session.xyDataObjects['Reaction-4']
    del session.xyDataObjects['Reaction-5']
    del session.xyDataObjects['Reaction-6']
    del session.xyDataObjects['Reaction-7']
    del session.xyDataObjects['Reaction-8']
    del session.xyDataObjects['Reaction-9']
    del session.xyDataObjects['Reaction-10']
    del session.xyDataObjects['Reaction-11']
	
