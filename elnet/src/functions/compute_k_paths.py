import networkx as nx

from elnet.src.classes import AdvDiGraph


def compute_k_paths(G: AdvDiGraph, num_candidate_paths: int) -> dict:

    # k = 3 is a logical default
    if num_candidate_paths is None:
        num_candidate_paths = 3

    k_paths_dict = {}

    # Go through all the node pairs
    for (
        src_ind,
        src_id,
    ) in enumerate(G.nodes()):
        for dst_ind, dst_id in enumerate(G.nodes()):
            # Not counting nodes going back to each other
            if src_ind == dst_ind:
                continue

            # A list of paths with a key tuple of (src_node_id, dst_node_id)
            k_paths_dict[(src_id, dst_id)] = []

            path_generator = nx.shortest_simple_paths(
                G, src_id, dst_id, weight="length"
            )

            for path_ind, path in enumerate(path_generator):

                # Stop after k paths have been saved
                if path_ind == num_candidate_paths:
                    break

                else:
                    k_paths_dict[(src_id, dst_id)].append(path)

    return k_paths_dict
