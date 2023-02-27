from src.classes import AdvDiGraph
import pandas as pd

# SO = Spectrum Occupation
def check_SO_for_groooming_intermediate_nodes(
    G: AdvDiGraph, traffic: pd.DataFrame, route_path: list, n_channel: int
) -> bool:

    length = len(route_path)
    for r in range(length - 1):
        rcurr = route_path[r]
        rnext = route_path[r + 1]
        print(rcurr, rnext)
        # if not available in any of the next links, block.
        if G.edges[(rcurr, rnext)]["spectral_occupation"][n_channel] == 1:
            return False

    return True
