import pandas as pd

from elnet.src.classes import AdvDiGraph
from elnet.src.functions import compute_k_paths, create_path_df


# MSE = Most Spectral Efficient
# MC = Maximum Capacity
def MSE_MC(G: AdvDiGraph, traffic: pd.DataFrame, k_shortest_path=3) -> None:
    # Making k shortest path dataframe
    path_dict = compute_k_paths(G, k_shortest_path)
    k_shortest_path_df = create_path_df(G, path_dict)

    # Creating the joined tables of traffic and k_shortest_path for being more optimized
    merged_traffic = pd.merge(
        traffic, k_shortest_path_df, on=["src", "dst"], how="inner"
    )

    

    return merged_traffic
