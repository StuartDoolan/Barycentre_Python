import numpy as np
import matplotlib.pyplot as plt
plt.close('all')



tEd1000 = np.load('tEdtRBcs1000.npy')
tFit1000 = np.load('tFitcs1000.npy')
tEd100 = np.load('csize100tEdtRB.npy')
tFit100 = np.load('csize100tFit.npy')
tEd10 = np.load('csize10tEdtRB.npy')
tFit10 = np.load('csize10tFit.npy')

rat1000 = tEd1000/tFit1000
rat100 = tEd100/tFit100
rat10 = tEd10/tFit10
#plt.hist((np.log10(rat10), np.log10(rat100), np.log10(rat1000)))
fig1= plt.figure()
ax1 = fig1.add_subplot(111)
ax1.hist((np.log10(tFit1000*10**6), np.log10((tEd1000*10**6))), bins = 30, log = True,
normed = 1, color =(['r', 'b']), label = (['Fit Time', 'Calculated Time']))
fig1.suptitle('Normalised Histogram Comparing Efficiency of Model and Calculations', fontsize = 18)
ax1.set_xlabel('log10 of Computation Time in Microseconds', fontsize = 16)
ax1.set_ylabel('log10 of Frequency', fontsize = 16)
plt.legend(loc = 'upper center')
plt.grid()

plt.show()