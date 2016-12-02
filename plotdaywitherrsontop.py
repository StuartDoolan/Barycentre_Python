#from lincomtest import *
import matplotlib.pyplot as plt
import numpy as np
import random as r
#plt.hist(diff, bins=np.logspace(-1, 1.0, 100))
#plt.show()
#plt.plot(newEdt[0], 'b.')
#emit = np.load('dayEmitdtdata.npy')
emitday = np.load('emitdaydata.npy')
#close open plots
plt.close('all')
#import np arrays of diff for different periods
ydiff =np.load('yeardiff.npy')
mdiff = np.load('monthdiff.npy')
ddiff = np.load('daydiff.npy')
error = ddiff[80]
Edtwhi = emitday[5]
Edt =np.load('dayEdt100data.npy')
ydata = error + emitday[5]
#create max and min difference data for use in residual plots
##difference in microseconds (all points) Period of Yyar
ydiffmics = np.multiply(ydiff, 10**6)
#min and max difference  in microseconds, 1 each per vector 
minydiff = np.amin(ydiffmics.T, 0)
maxydiff =np.amax(ydiffmics.T, 0)
useydiff = np.array((minydiff, maxydiff)).T

#Period of 1 day
ddiffmics = np.multiply(ddiff, 10**6)
#min and max difference  in microseconds, 1 each per vector 
minddiff = np.amin(ddiffmics.T, 0)
maxddiff =np.amax(ddiffmics.T, 0)
useddiff = np.array((minddiff, maxddiff)).T

wl = 1024
day = 86400
start = r.randint(630720013, 1261872018-day)
x = np.linspace(start, start+day, wl)



#PLOT
fig1 = plt.figure(1)
ax1 = fig1.add_subplot(111)
ax1.plot(x*10**-9,ydata.T[0],'r.', label = 'Error') #Noisy data
ax1.plot(x*10**-9,emitday[5],'-k', label = 'Time Delay') #Best fit model
#frame1.set_xticklabels([]) #Remove x-tic labels for the first frame
fig1.suptitle('Plot of Largest Errors on Typical Time Delay Vector for Scale', fontsize = 18)
ax1.set_xlabel('GPS Time (One Day in Gigaseconds)', fontsize = 16)
ax1.set_ylabel('Time Delay (Seconds)', fontsize = 16)
plt.legend(numpoints=1, loc = 'upper center')
plt.grid()
plt.show()


#
#fig9 = plt.figure()
#ax9 = fig9.add_subplot(111)
#ax9.plot(useddiff, 'r.')
#fig9.suptitle('Plot of Max and Min Residuals for Period of a Day')
#ax9.set_xlabel('Vector Number ')
#ax9.set_ylabel('Residuals (Microseconds)')
#plt.grid()
