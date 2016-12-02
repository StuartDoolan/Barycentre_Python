from init_barycentre import init_barycentre
import numpy as np

[Eephem, Sephem] = init_barycentre( 'earth00-19-DE405.dat', 'sun00-19-DE405.dat')
#print Eephem
#print Sephem
([ephemEgps, Edttables, Eentries, ephemEpos, ephemEvel, ephemEacc]) = Eephem
### so Eephem[3][0] is np array of x positons, all fine!


