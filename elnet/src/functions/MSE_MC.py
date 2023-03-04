import pandas as pd

from elnet.src.classes import AdvDiGraph
from elnet.src.functions import compute_k_paths, create_path_df,shuffle_traffic_df_order


# MSE = Most Spectral Efficient
# MC = Maximum Capacity
def MSE_MC(G: AdvDiGraph, traffic: pd.DataFrame, k_shortest_path=3) -> None:
    # Making k shortest path dataframe
    path_dict = compute_k_paths(G, k_shortest_path)
    k_shortest_path_df = create_path_df(G, path_dict)

    shuffled_traffic_list=shuffle_traffic_df_order(traffic)
    overall_traffic_distribution=[]

    for i in range((len(shuffled_traffic_list))):
        # Creating the joined tables of traffic and k_shortest_path for being more optimized
        merged_traffic = pd.merge(
        shuffled_traffic_list[i], k_shortest_path_df, on=["src", "dst"], how="inner")

        overall_traffic_distribution.append(merged_traffic)


    

    return overall_traffic_distribution
