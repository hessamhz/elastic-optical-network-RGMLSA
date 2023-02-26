

#We are using 4THz optical band for each link and we choose each slot has 12.5 GHz; so it makes 320 channels 


def clearSpectrum(N,num_slot=320):
    num_slot=320
    for link in N.edges:
        N.edges[link]['spectral_occupation']= [0]*num_slot

