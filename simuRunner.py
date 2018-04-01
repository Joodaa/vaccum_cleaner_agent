# Author: stephan.manuel@posteo.de
# Purpose:
# Configuration for AI simulation
# Multi-Runs of AI simulation
# Statistic of multirun AI simulations
# Plots of multirun simulations
from pandas import *
import json # import json after pandas, it will overwrite something in a way you need it!
from numpy import matrix
from simu import Simu
from agents import BasicAgent
from agents import DustPerceptAgent
import sys

import matplotlib.pyplot as plt



# this file contains the 'environment matrix' for the agent
environmentFilePath = "complex_environment.json"

numberOfIterations = 1

with open(environmentFilePath) as json_file:
    data = json.load(json_file)

myEnvironment =  matrix( data['environment'] )
print "Simu runner: Environment loaded"

print DataFrame( myEnvironment )



# update_progress() : Displays or updates a console progress bar
## Accepts a float between 0 and 1. Any int will be converted to a float.
## A value under 0 represents a 'halt'.
## A value at 1 or bigger represents 100%
def update_progress(progress):
    barLength = 15 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rSimulation complete: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()


total_energy_cost_basic = []
total_energy_cost_dust= []


print ""
print "   ____      _____                     _____    _____     __    __     __    __  "
print "  (    )    (_   _)                   / ____\  (_   _)    \ \  / /     ) )  ( (  "
print "  / /\ \      | |       ________     ( (___      | |      () \/ ()    ( (    ) ) "
print " ( (__) )     | |      (________)     \___ \     | |      / _  _ \     ) )  ( (  "
print "  )    (      | |                         ) )    | |     / / \/ \ \   ( (    ) ) "
print " /  /\  \    _| |__                   ___/ /    _| |__  /_/      \_\   ) \__/ (  "
print "/__(  )__\  /_____(                  /____/    /_____( (/          \)  \______/  "
print ""

for iteration in range(0,numberOfIterations):
    update_progress(float(iteration)/numberOfIterations)
    myRobot = DustPerceptAgent( "Reflexive_002" )
    mySimu = Simu( myEnvironment.copy(),myRobot,[1,1], True)
    mySimu.run( 100000,0.01 )
    total_energy_cost_dust.append(mySimu.give_total_energy_cost())
    mySimu.print_statistics()
    #myRobot = BasicAgent( "Reflexive_001" )
    #mySimu = Simu( myEnvironment.copy(),myRobot,[1,1], False)
    #mySimu.run( 100000,0.000 )
    #total_energy_cost_basic.append(mySimu.give_total_energy_cost())
    #total_time_cost.append(mySimu.give_total_time_cost())

#plt.plot(total_energy_cost_basic)
#plt.plot(total_energy_cost_dust)
#plt.legend(['BasicAgent','DustPerceptAgent'])
#plt.xlabel('Simu Iteration')
#plt.ylabel('Energy Consumption')
#plt.title('AI-Agent Battle result: BasicAgent -vs- DustPerceptAgent')
#plt.show()
