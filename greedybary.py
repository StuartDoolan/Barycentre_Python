#matplotlib inline

import numpy as np
import sys
import matplotlib.pyplot as plt

# insert path to greedy.py
sys.path.insert(0, '../src/python')
import greedy
from get_barycentre import get_barycentre

  

tGPS = np.linspace(630720013, 1261872018)
dt = tGPS[1]-tGPS[0]
detector = 'gb'
sourcealpha = np.linspace(0,2,10)
sourcedelta = np.linspace(0, 1, 10)
source = [sourcealpha, sourcedelta]
sourcetest = [0.9, 0.622]
wl = 7
tssize = 1000 # training set size
TS = np.zeros((tssize, wl))

for i in range(tssize):
    # get chirp masses

    emit = get_barycentre(tGPS, detector, sourcetest, 'earth00-19-DE405.dat', 'sun00-19-DE405.dat') 
    [emitdt, emitte, emitdd, emitR, emitER, emitE, emitS] = emit
    TS[i]= emitdt[0][0]
    # normalise training set
    TS[i] /= np.sqrt(np.abs(greedy.dot_product(dt, TS[i], TS[i])))
    
# tolerance for stopping algorithm
tol = 1e-12

RB_matrix = greedy.greedy(TS, dt, tol)