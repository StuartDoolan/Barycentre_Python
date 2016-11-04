import numpy as np
import random as r
# insert path to greedy.py
import greedy
from init_barycentre import init_barycentre
from get_bary_greedy import get_bary_in_loop

###import Eephem & Sephem data outside loop 
[Eephem, Sephem] = init_barycentre( 'earth00-19-DE405.dat', 'sun00-19-DE405.dat')
  
##set detector
detector = 'gb'




#create set of training waveforms, 86400s in a day
wl = 1024
tGPS = np.linspace(630720013, 630720013+864000, wl)
dt = tGPS[1]-tGPS[0]

tssize = 1000 # training set size
sourcealpha = np.zeros(tssize)
sourcedelta = np.zeros(tssize)
TS = np.zeros((tssize, wl))
nTS=TS
##fTS= TS+TS
for i in range(tssize):
    
    #randomise RA and Dec between 0,pi/2 and -pi/2, pi/2 respectively
    ##adjusted to smaller ranges to see if improves results
    sourcealpha[i] = 2*np.pi*(r.uniform(0,0.5))
    sourcedelta[i] = np.arccos(2*(r.uniform(0,0.25))-1)-np.pi/2
    
    #performs barycentring functions for source i
    emit = get_bary_in_loop(tGPS, detector,[sourcealpha[i], sourcedelta[i]], Eephem, Sephem) 

    [emitdt, emitte, emitdd, emitR, emitER, emitE, emitS] = emit
    TS[i]= np.reshape(emitdt, wl)
    #TS[1][i]= np.reshape(emitte[0], wl)
    #TS[2][i]= np.reshape(emitdd, wl)
    #print(emitte[0])
    #print(emitdt[0][0])
    #print TS[i]

    # normalise training set
    nTS[i] /= np.sqrt(np.abs(greedy.dot_product(dt, TS[i], TS[i])))

    #nTS[0][0][i] /= np.sqrt(np.abs(greedy.dot_product(dt, TS[0][i], TS[0][i])))
    #nTS[1][0][i] /= np.sqrt(np.abs(greedy.dot_product(dt, TS[1][i], TS[1][i])))
    #TS[2][i] /= np.sqrt(np.abs(greedy.dot_product(dt, TS[2][i], TS[2][i])))

##fTS=TS+TS
#print('outloop')
#print(TS)
# tolerance for stopping algorithm
tol = 1e-12

RB_matrix = greedy.greedy(nTS, dt, tol)