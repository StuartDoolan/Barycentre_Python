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
wl = 1000
#start = r.randint(630720013, 1261785618)
tGPS = np.linspace(900000000, 900000000+86400, 1000)
dt = tGPS[1]-tGPS[0]

#sets training set size and initialises source arrays
tssize = 1000
with open('skyposvals.txt') as f:
    content = f.readlines()
    
content = [x.strip() for x in content]



nearly = [x.split() for x in content]

myarray = np.asarray(nearly)
flarray =myarray.astype(float)
finarray = flarray.T
sourcealpha = finarray[0]
sourcedelta = finarray[1]
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