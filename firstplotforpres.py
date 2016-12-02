import numpy as np
import random as r
import greedy
from init_barycentre import init_barycentre
from get_bary_greedy import get_bary_in_loop
import math as m
import matplotlib.pyplot as plt
#import Eephem & Sephem data outside loop 
[Eephem, Sephem] = init_barycentre( 'earth00-19-DE405.dat', 'sun00-19-DE405.dat')
plt.close()
##set detector
detector = 'h1'
plt.close()


emitdt = np.load('dayyearemitdt.npy')
sourcealpha = np.load('dayyearalpha.npy')
sourcedelta = np.load('dayyeardelta.npy')
tGPSstartvec = np.load('dayyeartGPS.npy')

#sets vector of time intervals of length wl from random acceptable starting point for one days worth of data
wl = 1024
day = 86400
tGPS = np.linspace(tGPSstartvec[0], tGPSstartvec[0]+day, wl)
dt = tGPS[1]-tGPS[0]

#sets training set size and initialises source arrays
tssize = 10

## initialise timetest vectors
# timebary = np.zeros(tssize)
emitdtday = np.zeros((tssize, wl,1))
#initialises training sets
TS = np.zeros((tssize, wl))
for i in range(tssize):
    
    #randomise RA and Dec between 0,2pi and -pi/2, pi/2 respectively
    ##adjusted to smaller ranges to see if improves results
    
    #performs barycentring functions for source i
    emit = get_bary_in_loop(tGPS, detector,[sourcealpha[i], sourcedelta[i]], Eephem, Sephem) 

    #creates training vectors of time difference
    [emitdtday[i], emitte, emitdd, emitR, emitER, emitE, emitS] = emit

x3 = tGPSstartvec*10**-6



fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
x1 = tGPS*10**-9
ax2.plot(x1, np.ravel(emitdtday[5]), 'bo')
fig2.suptitle('Time Delay from Source to SSB Over Period of a Day', fontsize = 18)
ax2.set_xlabel('GPS Time (One Day in Gigaseconds)', fontsize = 16)
ax2.set_ylabel('Time Delay (Microseconds)', fontsize = 16)
plt.grid()

fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
x2 = tGPSstartvec*10**-9
ax1.plot(x2, np.ravel(emitdt[5]), 'r.', label = 'Year')
ax1.plot(x1, np.ravel(emitdtday[5]), 'b', label = 'Day', linewidth = '3')
fig1.suptitle('Time Delay from Source to SSB over Period of a Year', fontsize = 18)
ax1.set_xlabel('GPS Time (One Year in Gigaseconds) ', fontsize = 16)
ax1.set_ylabel('Time Delay (Microseconds)', fontsize = 18)
plt.axhline(0, color='black')
plt.grid()
plt.legend(numpoints=1)



plt.show()