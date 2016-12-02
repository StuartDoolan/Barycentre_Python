#matplotlib inline
import numpy as np
import sys
import matplotlib.pyplot as plt
import random as r

# insert path to greedy.py
sys.path.insert(0, '../src/python')
import greedy
from get_barycentre import get_barycentre

  

detector = 'gb'

#sourcetest = [0.5, -0.3]
#source = [sourcealpha, sourcedelta]

#create set of training waveforms
wl = 102
#sets vector of time intervals of length wl from random acceptable starting point for one days worth of data
start = 630720013
day = 86400
tGPS = np.linspace(start, start+day, wl)
dt = tGPS[1]-tGPS[0]

tssize = 100 # training set size
TS = np.zeros((tssize, wl))

sourcealpha = np.zeros(tssize)
sourcedelta = np.zeros(tssize)



for i in range(tssize):

    sourcealpha[i] = 2*np.pi*(r.uniform(0,0.1))
    sourcedelta[i] = np.arccos(2*(r.uniform(0,0.05))-1)-np.pi/2
    #source[i] = [sourcealpha[i], sourcedelta[i]]

    #emit = get_barycentre(tGPS, detector, [source[0][i], source[1][i]], 'earth00-19-DE405.dat', 'sun00-19-DE405.dat') 
    emit = get_barycentre(tGPS, detector,[sourcealpha[i], sourcedelta[i]], 'earth00-19-DE405.dat', 'sun00-19-DE405.dat') 

    [emitdt, emitte, emitdd, emitR, emitER, emitE, emitS] = emit
    TS[i]= np.reshape(emitdt, wl)
    # normalise training set
    TS[i] /= np.sqrt(np.abs(greedy.dot_product(dt, TS[i], TS[i])))
    
print('outloop')
# tolerance for stopping algorithm
tol = 1e-12

RB_matrix = greedy.greedy(TS, dt, tol)