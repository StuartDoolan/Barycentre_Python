#testing script for running barycentring functions 


import numpy as np
from get_barycentre import get_barycentre

#should work for times between 630720013 and 1261872018, otherwise dummy values
tGPS = np.linspace(630720013, 1261872018)
detector = 'gb'
source = [1, 0.6]

emit = get_barycentre(tGPS, detector, source, 'earth00-19-DE405.dat', 'sun00-19-DE405.dat')
[emitdt, emitte, emitdd, emitR, emitER, emitE, emitS] = emit
