import numpy as np
import random as r
import greedy
from init_barycentre import init_barycentre
from get_bary_greedy import get_bary_in_loop

#import Eephem & Sephem data outside loop 
[Eephem, Sephem] = init_barycentre( 'earth00-19-DE405.dat', 'sun00-19-DE405.dat')
  
##set detector
detector = 'gb'


#sets vector of time intervals of length wl from random acceptable starting point for one days worth of data
wl = 1024
start = r.randint(630720013, 1261785618)
day = 86400
tGPS = np.linspace(start, start+day, wl)
dt = tGPS[1]-tGPS[0]

#sets training set size and initialises source arrays
tssize = 1000
sourcealpha = np.zeros(tssize)
sourcedelta = np.zeros(tssize)

#initialises training sets
TS = np.zeros((tssize, wl))
for i in range(tssize):
    
    #randomise RA and Dec between 0,2pi and -pi/2, pi/2 respectively
    ##adjusted to smaller ranges to see if improves results
    sourcealpha[i] = 2*np.pi*(r.uniform(0,0.0025))
    sourcedelta[i] = np.arccos(2*(r.uniform(0,0.001))-1)-np.pi/2
    
    #performs barycentring functions for source i
    emit = get_bary_in_loop(tGPS, detector,[sourcealpha[i], sourcedelta[i]], Eephem, Sephem) 

    #creates training vectors of time difference
    [emitdt, emitte, emitdd, emitR, emitER, emitE, emitS] = emit
    TS[i]= np.reshape(emitdt, wl)
 
    
   

    ## normalises training vectors
    TS[i] /= np.sqrt(np.abs(greedy.dot_product(dt, TS[i], TS[i])))
   
##print('outloop')

# tolerance for stopping algorithm
tol = 1e-12

##concatenates arrays, so each i array now [emitdt, emitte emitdd] 
##fTS = np.hstack((TS[0],TS[1], TS[2]))

#forms normlised basis vectors, except happens far too quickly to be right
RB_matrix = greedy.greedy(TS, dt, tol)