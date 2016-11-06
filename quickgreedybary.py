import numpy as np
import random as r
import greedy
from init_barycentre import init_barycentre
from get_bary_greedy import get_bary_in_loop

###import Eephem & Sephem data outside loop 
[Eephem, Sephem] = init_barycentre( 'earth00-19-DE405.dat', 'sun00-19-DE405.dat')
  
##set detector
detector = 'gb'


#sets vector of time intervals of length wl from random acceptable starting point for one days worth of data
wl = 102
start = r.randint(630720013, 1261785618)
day = 86400
tGPS = np.linspace(start, start+day, wl)
dt = tGPS[1]-tGPS[0]

#sets training set size and initialises source arrays
tssize = 100 
sourcealpha = np.zeros(tssize)
sourcedelta = np.zeros(tssize)

#initialises training sets
TS = np.zeros((3,tssize, wl))
fTS = np.zeros((tssize, 3*wl))
for i in range(tssize):
    
    #randomise RA and Dec between 0,2pi and -pi/2, pi/2 respectively
    ##adjusted to smaller ranges to see if improves results
    sourcealpha[i] = 2*np.pi*(r.uniform(0,0.000025))
    sourcedelta[i] = np.arccos(2*(r.uniform(0,0.00001))-1)-np.pi/2
    
    #performs barycentring functions for source i
    emit = get_bary_in_loop(tGPS, detector,[sourcealpha[i], sourcedelta[i]], Eephem, Sephem) 

    #creates training vectors 
    [emitdt, emitte, emitdd, emitR, emitER, emitE, emitS] = emit
    TS[0][i]= np.reshape(emitdt, wl)
    TS[1][i]= np.reshape(emitte, wl)
    TS[2][i]= np.reshape(emitdd, wl)
    
    #concatenates arrays
    fTS[i] = np.hstack((TS[0][i],TS[1][i], TS[2][i]))
    fTS[i] /= np.sqrt(np.abs(greedy.dot_product(dt, fTS[i], fTS[i])))

    ## normalises training vectors
    ##TS[0][i] /= np.sqrt(np.abs(greedy.dot_product(dt, TS[0][i], TS[0][i])))
    ##TS[1][i] /= np.sqrt(np.abs(greedy.dot_product(dt, TS[1][i], TS[1][i])))
    ##TS[2][i] /= np.sqrt(np.abs(greedy.dot_product(dt, TS[2][i], TS[2][i])))

##print('outloop')

# tolerance for stopping algorithm
tol = 1e-12

##concatenates arrays, so each i array now [emitdt, emitte emitdd] 
##fTS = np.hstack((TS[0],TS[1], TS[2]))

#forms normlised basis vectors, except happens far too quickly to be right
RB_matrix = greedy.greedy(fTS, dt, tol)