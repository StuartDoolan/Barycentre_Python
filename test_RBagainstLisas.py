import numpy as np
import random as r
import greedy
from init_barycentre import init_barycentre
from get_bary_greedy import get_bary_in_loop
import math as m
import matplotlib.pyplot as plt
#import Eephem & Sephem data outside loop 
[Eephem, Sephem] = init_barycentre( 'earth00-19-DE405.dat', 'sun00-19-DE405.dat')
  
##set detector
detector = 'h1'


#sets vector of time intervals of length wl from random acceptable starting point for one days worth of data
wl = 400
#start = r.randint(630720013, 1261785618)
start = 630720013
day = 86400
tGPS = np.linspace(start, start+day, wl)
dt = tGPS[1]-tGPS[0]

#sets training set size and initialises source arrays
tssize = 100
sourcealpha = np.zeros(tssize)
sourcedelta = np.zeros(tssize)

sourcealpha = np.linspace(0.1,2*np.pi-0.1, tssize)
sourcedelta = np.linspace(-np.pi/2, np.pi/2, tssize)
#initialises training sets
TS = np.zeros((tssize, wl))
for i in range(tssize):
    
    #randomise RA and Dec between 0,2pi and -pi/2, pi/2 respectively
    ##adjusted to smaller ranges to see if improves results
    
    #performs barycentring functions for source i
    emit = get_bary_in_loop(tGPS, detector,[sourcealpha[i], sourcedelta[i]], Eephem, Sephem) 

    #creates training vectors of time difference
    [emitdt, emitte, emitdd, emitR, emitER, emitE, emitS] = emit
    TS[i]= np.reshape(emitdt, wl)
   

    ## normalises training vectors
    TS[i] /= np.sqrt(np.abs(greedy.dot_product(dt, TS[i], TS[i])))
    #print[i]
   
##print('outloop')

# tolerance for stopping algorithm
tol = 1e-12



#forms normalised basis vectors
RB = greedy.greedy(TS, dt, tol)