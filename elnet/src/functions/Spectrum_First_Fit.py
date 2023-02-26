
def First_Fit(N, path, num_slots):
    '''find the first num_slots-wide free spectrum segment along the path'''
    
    slots_in_band = 320 
    print(slots_in_band)
    for first_slot in range(slots_in_band - num_slots + 1):

        spectrum_is_free = True
        
        #######################################################################################
        # the missing part is written by students
        
        for link in zip(path, path[1:]):
            
            if sum(N.edges[link]['spectrum_slots'][first_slot : first_slot + num_slots]) != 0:
                spectrum_is_free = False
                break
        #######################################################################################
                
        if spectrum_is_free:
            return first_slot
    
    return None