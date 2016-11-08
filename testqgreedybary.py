import numpy as np
import random as r
import greedy
from init_barycentre import init_barycentre
from get_bary_greedy import get_bary_in_loop

#import Eephem & Sephem data outside loop 
[Eephem, Sephem] = init_barycentre( 'earth00-19-DE405.dat', 'sun00-19-DE405.dat')
  
##set detector
detector = 'h1'


#sets vector of time intervals of length wl from random acceptable starting point for one days worth of data
wl = 1024
start = r.randint(630720013, 1261785618)
day = 86400
tGPS = np.linspace(start, start+day, wl)
dt = tGPS[1]-tGPS[0]

#sets training set size and initialises source arrays
tssize = 100
sourcealpha = np.zeros(tssize)
sourcedelta = np.zeros(tssize)

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
    [emitdt, emitte, emitdd, emitR, emitER, emitE, emitS] = emit
    TS[i]= np.reshape(emitdt, wl)
   

    ## normalises training vectors
    TS[i] /= np.sqrt(np.abs(greedy.dot_product(dt, TS[i], TS[i])))
    print[i]
   
##print('outloop')

# tolerance for stopping algorithm
tol = 1e-12



#forms normalised basis vectors, except happens far too quickly to be right
RB = greedy.greedy(TS, dt, tol)

##### Test this RB can recover a specific source from ephem data

#define location to test (arbitrary)
sourcealpha2 = 1
sourcedelta2 = 0.5
source = np.array([sourcealpha2, sourcedelta2 ])

#apply get barycentre and find emitdt data for this source
emit = get_bary_in_loop(tGPS, detector,source, Eephem, Sephem)
[emitdt, emitte, emitdd, emitR, emitER, emitE, emitS] = emit
Edt= np.reshape(emitdt, wl)
Edt /= np.sqrt(np.abs(greedy.dot_product(dt, Edt, Edt)))


#solve lin matrix eq RBx = Edt, gives residuals approx e-26, success? 
np.linalg.lstsq(RB.T,Edt, 1*10**-12)

