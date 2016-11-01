# -*- coding: utf-8 -*-
def get_barycentre(tGPS, detector, source, efile, sfile):
    
    import numpy as np
    from math import floor
    from init_barycentre import init_barycentre
    from barycentre_earth import barycentre_earth
    from barycentre import barycentre
    
    #source = [sourcealpha, sourcedelta] = [1, 0.6] # dummy input
    
    # set speed of light in vacuum (m/s)
    C_SI = 299792458;
    
    # set the detector x, y and z positions on the Earth surface. For radio
    # telescopes use values from the TEMPO2 observatories.dat file, and for GW
    # telescopes use values from LAL.
    binsloc = np.zeros((3,1));  ## double brackets just cost me an hour!
    
    ##detector = 't1' # dummy input
    
    
    if detector.upper() == 'GB': # GREEN BANK #case insensitive string compare
        binsloc[0] = 882589.65;
        binsloc[1] = -4924872.32;
        binsloc[2] = 3943729.348;
    
    elif detector.upper() == 'NA': # NARRABRI
        binsloc[0] = -4752329.7000;
        binsloc[1] = 2790505.9340;
        binsloc[2] = -3200483.7470;
    elif detector.upper() == 'AO': # ARECIBO
        binsloc[0] = 2390490.0;
        binsloc[1] = -5564764.0;
        binsloc[2] = 1994727.0;
    elif detector.upper() == 'HO': # Hobart
        binsloc[0] = -3950077.96;
        binsloc[1] = 2522377.31;
        binsloc[2] = -4311667.52;
    elif detector.upper() == 'TD': # DSS 43
        binsloc[0] = -4460892.6;
        binsloc[1] = 2682358.9;
        binsloc[2] = -3674756.0;
    elif detector.upper() == 'PK': # PARKES
        binsloc[0] = -4554231.5;
        binsloc[1] = 2816759.1;
        binsloc[2] = -3454036.3;
    elif detector.upper() == 'JB': # JODRELL BANK
        binsloc[0] = 3822252.643;
        binsloc[1] = -153995.683;
        binsloc[2] = 5086051.443;
    elif detector.upper() == 'G3': # GB 300FT
        binsloc[0] = 881856.58;
        binsloc[1] = -4925311.86;
        binsloc[2] = 3943459.70;
    elif detector.upper() == 'G1RAD': # GB 140FT
        binsloc[0] = 882872.57;
        binsloc[1] = -4924552.73;
        binsloc[2] = 3944154.92;
    elif detector.upper() == 'VL': # VLA
        binsloc[0] = -1601192.0;
        binsloc[1] = -5041981.4;
        binsloc[2] = 3554871.4;
    elif detector.upper() == 'NC': # NANCAY
        binsloc[0] = 4324165.81;
        binsloc[1] = 165927.11;
        binsloc[2] = 4670132.83;
    elif detector.upper() == 'EF': # Effelsberg
        binsloc[0] = 4033949.5;
        binsloc[1] = 486989.4;
        binsloc[2] = 4900430.8;
    elif detector.upper() in ['H1','H2', 'LHO']: # LIGO Hanford
        binsloc[0] = -2161414.92636;
        binsloc[1] = -3834695.17889;
        binsloc[2] = 4600350.22664;
    elif detector.upper() ==  'LLO' or detector.upper() ==  'L1':# LIGO Livingston
        binsloc[0] = -74276.04472380;
        binsloc[1] = -5496283.71971000;
        binsloc[2] = 3224257.01744000;
    elif detector.upper() ==  'GEO' or detector.upper() ==  'G1': # GEO600
        binsloc[0] = 3856309.94926000;
        binsloc[1] = 666598.95631700;
        binsloc[2] = 5019641.41725000;
    elif detector.upper() ==  'V1' or detector.upper() ==  'VIRGO': # Virgo
        binsloc[0] = 4546374.09900000;
        binsloc[1] = 842989.69762600;
        binsloc[2] = 4378576.96241000;
    elif detector.upper() ==  'TAMA' or detector.upper() ==  'T1': # TAMA300
        binsloc[0] = -3946408.99111000;
        binsloc[1] = 3366259.02802000;
        binsloc[2] = 3699150.69233000;
    elif detector.upper() ==  'GEOCENTER' or detector.upper() ==  'GEOCENTRE': # the geocentre
        binsloc[0] = 0;
        binsloc[1] = 0;
        binsloc[2] = 0; ##it all works so far!
        
    binsloc[:] = [x / C_SI for x in binsloc]  # sets positions in light seconds
    
    # Set source info
    [sourcealpha, sourcedelta] = source
    binalpha = sourcealpha # right ascension in radians
    bindelta = sourcedelta # declination in radians
    bindInv = 0 # inverse distance (assumption is that source is very distant)
    baryinsource = [binalpha, bindelta, bindInv]
    
    #perform init_barycentre, import data
    [Eephem, Sephem] =init_barycentre('earth00-19-DE405.dat', 'sun00-19-DE405.dat')
    
    
    # check input from bary init ok
    #if type(Eephem) == len(Sephem):
        #if Eephem == 0 or Sephem == 0:
        #  print('Error reading in one of the ephemeris files');
    
    
    # length of time vector
    length = len(tGPS);
    emitdt = np.zeros([length,1]);
    emitte =np.zeros([length,1]);
    emitdd =np.zeros([length,1]);
    emitR =np.zeros([length,1]);
    emitER =np.zeros([length,1]);
    emitE =np.zeros([length,1]);
    emitS =np.zeros([length,1]);
    
    ### perform earth barycentring
    earthstruct = barycentre_earth(Eephem, Sephem, tGPS)
    
    [[earthposNow, earthvelNow, earthgmstRad],
    [earthtzeA, earthzA, earththetaA],
    [earthdelpsi, earthdeleps, earthgastRad],
    [eartheinstein, earthdeinstein],
    [earthse, earthdse, earthdrse, earthrse]] = earthstruct
    
    for i in range(length):
        # split time into seconds and nanoseconds
        tts = floor(tGPS[i]);
        ttns = np.multiply((tGPS[i]-tts),1e9) 
    
        bingpss = tts;
        bingpsns = ttns;
        bingps = [bingpss, bingpsns]
        baryinput = [binsloc, bingps, baryinsource]    
    
    emit = barycentre(baryinput, earthstruct)
    [emitdeltaT, emittDot, emittes, emittens, emitroemer,  emiterot, emiteinstein, 
    emitshapiro] = emit
    print emit
    
    for i in range(length):
        emitdt[i] = emitdeltaT;
        emitte[i] = [emittens*1e-9 + emittes]
        emitdd[i] = emittDot;
        emitR[i] = emitroemer;
        emitER[i] = emiterot;
        emitE[i] = emiteinstein;
        emitS[i] = emitshapiro;
    
    emit = [emitdt, emitte, emitdd, emitR, emitER, emitE, emitS] ## final output!!!
    return emit