def init_barycentre(efile, sfile):
    import numpy as np
    ## Reads in Earth and Sun ephemeris data with 3 main outputs
    ## Eephem
    # read in file
    f = open(efile, 'r')
    if False:
        print('Error, could not open Earth ephemeris file');   # displays error message
    filecontents = f.readlines()
    f.close()
    
    
    # skip through header lines starting with '#'
    filestart = 0
    while 1:
        if filecontents[filestart][0] == '#':
            filestart += 1
        else:
            break
    
    # assign details of header to variables: initgps, no. of reading, no. of entries
    [Einitgps, Edttables, Eentries] = np.array([
    float((filecontents[filestart].split()[0]).strip()),
    float((filecontents[filestart].split()[1]).strip()), 
    int((filecontents[filestart].split()[2]).strip())])
    
    # create array for data (nentries rows by 10 columns)
    ephemdata = np.zeros((Eentries, 10)) 
    
    # read in the actual data
    for i in range(int(Eentries)):
        thisline = []
        for j in range(4):
            lines = filecontents[filestart+1+(i*4)+j].split()
            for val in lines:
                thisline.append(float(val.strip()))
        ephemdata[i,:] = np.array(thisline)
    
    #assign each variable
    [ephemEgps, xpos, ypos, zpos, velx, vely, velz, accx, accy, accz] = np.array([
    ephemdata[:,0], ephemdata[:,1], ephemdata[:,2], ephemdata[:,3], ephemdata[:,4],
    ephemdata[:,5], ephemdata[:,6], ephemdata[:,7], ephemdata[:,8], ephemdata[:,9]])
    ephemEpos = np.array([xpos, ypos, zpos])
    ephemEvel = np.array([velx, vely, velz])
    ephemEacc = np.array([accx, accy, accz])
    
    Eephem = np.array([ephemEgps, Edttables, Eentries, ephemEpos, ephemEvel, ephemEacc])
    
    ####### Sun Stuff
    
    # read in file
    f = open(sfile, 'r')
    if False:
        print('Error, could not open Sun ephemeris file');   # displays error message
    filecontents = f.readlines()
    f.close()
    
    
    # skip through header lines starting with '#'
    filestart = 0
    while 1:
        if filecontents[filestart][0] == '#':
            filestart += 1
        else:
            break
    
    # find number of entries in the file
    [Sinitgps, Sdttables, Sentries] = np.array([
    float((filecontents[filestart].split()[0]).strip()),
    float((filecontents[filestart].split()[1]).strip()), 
    int((filecontents[filestart].split()[2]).strip())])
    # create array for data (nentries rows by 10 columns)
    ephemdata = np.zeros((Sentries, 10)) 
    
    # read in the actual data
    for i in range(int(Sentries)):
        thisline = []
        for j in range(4):
            lines = filecontents[filestart+1+(i*4)+j].split()
            for val in lines:
                thisline.append(float(val.strip()))
        ephemdata[i,:] = np.array(thisline)
    
    #assign each variable
    [ephemSgps, Sxpos, Sypos, Szpos, Svelx, Svely, Svelz, Saccx, Saccy, Saccz] = np.array([
    ephemdata[:,0], ephemdata[:,1], ephemdata[:,2], ephemdata[:,3], ephemdata[:,4],
    ephemdata[:,5], ephemdata[:,6], ephemdata[:,7], ephemdata[:,8], ephemdata[:,9]])
    
    ephemSpos = np.array([Sxpos, Sypos, Szpos])
    ephemSvel = np.array([Svelx, Svely, Svelz])
    ephemSacc = np.array([Saccx, Saccy, Saccz])
    
    ### Returns ndarrays Eephem & Sephem, Eephem[3][0] = xpos, for example
    Sephem = np.array([ephemSgps, Sdttables, Sentries, ephemSpos, ephemSvel, ephemSacc]) 
    return Eephem, Sephem
  ##confident this does exactly the same as matlab!
