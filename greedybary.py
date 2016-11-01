#matplotlib inline

import numpy as np
import sys
import matplotlib.pyplot as plt

# insert path to greedy.py
sys.path.insert(0, '../src/python')
import greedy
from get_barycentre import emit 

[emitdt, emitte, emitdd, emitR, emitER, emitE, emitS] = emit

##### want to replace chirp model with time and time delay/frequency model
#Msun = 4.92549095e-6 # solar mass in geometrised units

# define a simple chirp-like model
#def calc_phase(frequency, Mchirp):
 #   """
  #  Calculate the phase of the model over a range of frequencies and for a given chirp mass
   # """
    #return -0.25*np.pi + ( 3./( 128. * pow(Mchirp*Msun*np.pi*frequency, 5./3.) ) )


#def real_model(frequency, Mchirp, modperiod):
 #   """
  #  Calculate the chirp signal over a range of frequencies, for a given chirp mass
   # and modulation period
    #"""
    #return ( frequency**(-7./6.) * (Mchirp*Msun)**(5./6.) * np.cos(calc_phase(frequency,Mchirp)) )*np.sin(np.pi*frequency/modperiod)

# create set of training waveforms
wl = 1024 # waveform length

# frequency range
freqmin = 48
freqmax = 256

freqs = np.linspace(freqmin, freqmax, wl)
df = freqs[1]-freqs[0] # frequency steps

# chirp mass range (solar masses) for creating training waveforms
Mcmin = 1.5
Mcmax = 2.
Mc = 0.

# modulatoin period range
periodmax = 1./99.995
periodmin = 1./100.

tssize = 1000 # training set size
TS = np.zeros((tssize, wl))

for i in range(tssize):
    # get chirp masses
    Mc = (Mcmin**(5./3.) + i*(Mcmax**(5./3.)-Mcmin**(5./3.))/(tssize-1))**(3./5.)
    
    # get modulation period
    modperiod = periodmin + (periodmax-periodmin)*np.random.rand()

    TS[i] = real_model(freqs, Mc, modperiod)

    # normalise training set
    TS[i] /= np.sqrt(np.abs(greedy.dot_product(df, TS[i], TS[i])))
    
# tolerance for stopping algorithm
tol = 1e-12

RB_matrix = greedy.greedy(TS, df, tol)