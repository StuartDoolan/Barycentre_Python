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


#sets vector of time intervals of length wl from random acceptable starting point for one days worth of data
wl = 1024
day = 86400
start = r.randint(630720013, 1261872018-365*day)
tGPS = np.linspace(start, start+365*day, wl)
dt = tGPS[1]-tGPS[0]

#sets training set size and initialises source arrays
tssize = 10
sourcealpha = np.zeros(tssize)
sourcedelta = np.zeros(tssize)

## initialise timetest vectors
# timebary = np.zeros(tssize)
emitdt = np.zeros((tssize, wl,1))
#initialises training sets
TS = np.zeros((tssize, wl))
for i in range(tssize):
    
    #randomise RA and Dec between 0,2pi and -pi/2, pi/2 respectively
    ##adjusted to smaller ranges to see if improves results
    sourcealpha[i] = 2*np.pi*(r.uniform(0,1))
    sourcedelta[i] = np.arccos(2*(r.uniform(0,1))-1)-np.pi/2
    
    #performs barycentring functions for source i
    emit = get_bary_in_loop(tGPS, detector,[sourcealpha[i], sourcedelta[i]], Eephem, Sephem) 

    #creates training vectors of time difference
    [emitdt[i], emitte, emitdd, emitR, emitER, emitE, emitS] = emit
   

    
fig = plt.figure()
ax = fig.add_subplot(111)
x = tGPS*10**-9
ax.plot(x, np.ravel(emitdt[5]), 'r')
fig.suptitle('Time Delay from Source to SSB over 1 Day Period')
ax.set_xlabel('Time (One Day in Gigaseconds) ')
ax.set_ylabel('Time Delay (Microseconds)')
plt.grid()
plt.show()