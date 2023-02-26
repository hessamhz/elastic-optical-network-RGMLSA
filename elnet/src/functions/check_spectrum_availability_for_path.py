


def check_spectral_occupation_for_groooming_intermediate_nodes(N,traffic_dict,route_path,n_channel):
      
    length=len(route_path)
    for r in range(length-1):
        rcurr = route_path[r]
        rnext = route_path[r+1]
        print(rcurr,rnext)
    # if not available in any of the next links, block.
        if N.edges[(rcurr, rnext)]['spectral_occupation'][n_channel] == 1:
            return False

    return True
