from lincomtest import *
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
#Test interpolation method, expect emitdt between two points in time to be roughly linear
#test goodness of fit for linear between any two points?

#take points halfway between each existing time point
#tGPStest = tRB+30826.979472160339/2

#initialise y for use creating point from rb
y = np.zeros(no_v)


newtime = np.arange(tGPS[0], tGPS[1023], dt/2)

Edt = np.zeros((csize,np.size(newtime)))

#calculate specific emitdt values for new time vectors at particular source
for i in range(csize):


    
    #apply get barycentre and find emitdt data for these sources
    emit = get_bary_in_loop(newtime, detector,[sourcealpha2[i], sourcedelta2[i]], Eephem, Sephem)
    [emitdt2, emitte, emitdd, emitR, emitER, emitE, emitS] = emit
    Edt[i]= np.reshape(emitdt2, np.size(newtime))
    
   
    

#probably dont use, vectors i would use to check RB if we werent using interp1d
for j in range(no_v):
    y[j] = Edt[0][p[j]]  

#defines function of form Edt = f(tGPS) 
f =interp1d(tGPS, newEdt)
interEdt = f(newtime)
diff = Edt-interEdt
plt.plot(newtime, Edt[0], 'o', newtime, interEdt[0], '-')