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
wl = 100
#start = r.randint(630720013, 1261785618)
tGPS = np.linspace(900000000, 900000000+86400, 100)
dt = tGPS[1]-tGPS[0]

tssize = 100

sourcealpha = np.linspace(0.01, 6, tssize)
sourcedelta = np.linspace(-1, 1, tssize)

TS = np.zeros((tssize, wl))
for i in range(tssize):
    
  
    #performs barycentring functions for source i
    emit = get_bary_in_loop(tGPS, detector,[sourcealpha[i], sourcedelta[i]], Eephem, Sephem) 

    #creates training vectors of time difference
    [emitdt, emitte, emitdd, emitR, emitER, emitE, emitS] = emit
    print(emitdt)
    TS[i]= np.reshape(emitdt, wl)
   

    ## normalises training vectors
    TS[i] /= np.sqrt(np.abs(greedy.dot_product(dt, TS[i], TS[i])))
    print[i]
    
# tolerance for stopping algorithm
tol = 1e-12



#forms normalised basis vectors
RB = greedy.greedy(TS, dt, tol)