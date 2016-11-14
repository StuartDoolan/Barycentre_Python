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
wl = 1024
start = r.randint(630720013, 1261785618)
day = 86400
tGPS = np.linspace(start, start+30*day, wl)
dt = tGPS[1]-tGPS[0]

#sets training set size and initialises source arrays
tssize = 1000
sourcealpha = np.zeros(tssize)
sourcedelta = np.zeros(tssize)

## initialise timetest vectors
# timebary = np.zeros(tssize)

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
    #print[i]
    
##print('outloop')
#time bary fin
# tolerance for stopping algorithm
tol = 1e-12



#forms normalised basis vectors
RB = greedy.greedy(TS, dt, tol)




#no of vectors in RB and tssize
[no_v,unused] = np.shape(RB)

##### Test this RB can span all random points
#length of check vector
csize = 100
sourcealpha2 = np.zeros(csize)
sourcedelta2 = np.zeros(csize)
Edt = np.zeros((csize,wl))
residuals = np.zeros(csize)

x= np.zeros((csize,no_v))#### cssize of 2x1
tRB = np.zeros((no_v,no_v))
#C = np.zeros((csize,2,2))
AB = np.zeros((csize,no_v))
#integer division for location of emitdt
p = np.zeros(no_v)

##creates positions along Edt vector used
#for i in range(no_v):
    
 #   p[i] = float((i+1))/float((no_v+2))
  #  print(p[i])

l = np.linspace(csize/(2*no_v),csize,no_v,False)
p = l.astype(int)
for i in range(no_v):
    for j in range(no_v):
        #creates vectors of reduced bases corresponding to time location of points used 
        tRB[i][j] = RB[i][p[j]]
    
#inverts tRB for use solving x = (AB)tRB
C = np.linalg.inv((tRB))
##creates Edt to be tested with RB
for i in range(csize):

    #define location to test (arbitrary)
    sourcealpha2[i] = 2*np.pi*(r.uniform(0,1))
    sourcedelta2[i] = np.arccos(2*(r.uniform(0,1))-1)-np.pi/2
    source = np.array([sourcealpha2, sourcedelta2 ])
    
    #apply get barycentre and find emitdt data for these sources
    emit = get_bary_in_loop(tGPS, detector,[sourcealpha2[i], sourcedelta2[i]], Eephem, Sephem)
    [emitdt2, emitte, emitdd, emitR, emitER, emitE, emitS] = emit
    Edt[i]= np.reshape(emitdt2, wl)
    
   
    
    #takes points from basis vectors at corresponding tGPS entries
    ## Want no_v points for each x[i] extracted from Edt[j]
    for j in range(no_v):
        x[i][j] = Edt[i][p[j]]    
        
#solves x=(AB)(tRB)
AB = np.dot(x,C)



##test this all returns x (nearly, rounding error somewhere of order ~e-10)
D = np.dot(AB,tRB)

##

newEdt=np.dot(AB,RB)
diff=Edt-newEdt
print('the mean difference is ' + str(np.mean(diff)))
print('the maximum difference is ' + str(np.max(diff)))
