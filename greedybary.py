#matplotlib inline
from random import randint
import numpy as np
import sys
import matplotlib.pyplot as plt

# insert path to greedy.py
sys.path.insert(0, '../src/python')
import greedy
from get_barycentre import get_barycentre

  
#creates time vector of 100 elements between values listed, far too few but just for tests

detector = 'gb'

sourcealpha = np.zeros(100)
sourcedelta = np.zeros(100)

## creates rough 'random' source locations, adjust delta ones to be truly random
for x in range(100):
    sourcealpha[x] = randint(0,360)*np.pi/180
    sourcedelta[x] = randint(-90, 90)*np.pi/180

source = [sourcealpha, sourcedelta]
sourcetest = [0.9, 0.622]

#create set of training waveforms, 86400s in a day
wl = 1024
tGPS = np.linspace(630720013, 630720013+86400, wl)
dt = tGPS[1]-tGPS[0]

tssize = 360 # training set size
TS = np.zeros((tssize, wl))

for i in range(tssize):
    # get chirp masses

    emit = get_barycentre(tGPS, detector, [source[0][i], source[1][i]], 'earth00-19-DE405.dat', 'sun00-19-DE405.dat') 
    [emitdt, emitte, emitdd, emitR, emitER, emitE, emitS] = emit
    TS[i]= emitdt[0][0]
    # normalise training set
    TS[i] /= np.sqrt(np.abs(greedy.dot_product(dt, TS[i], TS[i])))
    
print('outloop')
# tolerance for stopping algorithm
tol = 1e-12

RB_matrix = greedy.greedy(TS, dt, tol)