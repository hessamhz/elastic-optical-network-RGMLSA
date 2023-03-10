from elnet.src.classes import AdvDiGraph
import pandas as pd

# SO = Spectrum Occupation
def check_SO_for_groooming_intermediate_nodes(
    G: AdvDiGraph, route_path: list, n_channel: int
) -> bool:
    """
    Checking if there is any continous n_channel in
    all links of a given path.
    """

    path_length = len(route_path)

    for r in range(path_length - 1):
        rcurr = route_path[r]
        rnext = route_path[r + 1]
        sum_dynamic = sum(G.edges[(rcurr, rnext)]["spectral_occupation"])

        # if not available in any of the next links, block.
        for i in range(sum_dynamic, sum_dynamic + n_channel):
            if G.edges[(rcurr, rnext)]["spectral_occupation"][i] == 1:
                return False

    return True
