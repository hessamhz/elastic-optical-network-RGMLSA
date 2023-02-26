
#Occupy Spectrum As Number of Slots and starting with first slot that returns from first fit function


def occupy_spectrum(N, path, first_slot, num_slots):
    
    for link in zip(path, path[1:]):
        for slot_shift in range(num_slots):
            N.edges[link]['spectrum_slots'][first_slot + slot_shift] = 1





