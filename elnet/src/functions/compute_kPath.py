import networkx as nx

def compute_k_paths(N, num_candidate_paths = 5):
    
    k_paths_dict = {}
    
    # go through all the node pairs
    for src_ind,src_id, in enumerate(N.nodes()):
        for dst_ind,dst_id in enumerate(N.nodes()):
        
            # ignore paths from node_i to node_j of i >= j
            if src_ind >= dst_ind:
                continue
                
            # a list of paths with a key tuple of (src_node_id, dst_node_id)
            k_paths_dict[(src_id, dst_id)] = []
                    
            path_generator = nx.shortest_simple_paths(N, src_id, dst_id, weight = 'length')
                
            for path_ind, path in enumerate(path_generator):
                
                # stop after k paths have been saved
                if path_ind == num_candidate_paths:
                    break

                else:
                    k_paths_dict[(src_id, dst_id)].append(path)

    return k_paths_dict


