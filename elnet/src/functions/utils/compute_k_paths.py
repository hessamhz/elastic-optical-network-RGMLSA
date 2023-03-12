import networkx as nx

from elnet.src.classes import AdvDiGraph


def compute_k_paths(G: AdvDiGraph, num_candidate_paths: int) -> dict:
    """
    Compute k_shortest_path for any given node pairs in our graph.
    """

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
                G, src_id, dst_id, weight="weight"
            )

            for path_ind, path in enumerate(path_generator):

                # Stop after k paths have been saved
                if path_ind == num_candidate_paths:
                    break

                else:
                    # Getting the total sum of the path and the max weight link
                    total_length = 0
                    max_weight = 0
                    for i, j in zip(path[:-1], path[1:]):
                        link_weight = G[i][j]["weight"]
                        total_length += link_weight
                        if link_weight > max_weight:
                            max_weight = link_weight
                    k_paths_dict[(src_id, dst_id)].append(
                        (path, total_length, max_weight)
                    )

    return k_paths_dict
