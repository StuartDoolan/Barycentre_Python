#testing script for running barycentring functions 

import random as r
import numpy as np
from get_barycentre import get_barycentre

#should work for times between 630720013 and 1261872018, otherwise dummy values
tGPS = np.linspace(630720013, 630720013+86400, 360)
detector = 'gb'
sourcealpha = np.zeros((10))
sourcedelta = np.zeros((10))

for i in range(1,10):
    sourcealpha[i] = 2*np.pi*(r.uniform(0,1))
    sourcedelta[i]= np.arccos(2*(r.uniform(0,1))-1)-np.pi/2
    source = [sourcealpha[i], sourcedelta[i]]
    emit = get_barycentre(tGPS, detector, source, 'earth00-19-DE405.dat', 'sun00-19-DE405.dat')
    [emitdt, emitte, emitdd, emitR, emitER, emitE, emitS] = emit
    print emitdt[0][0]
    #print emitte[0][0]
    #print emitdd[0][0]
source = [sourcealpha, sourcedelta]