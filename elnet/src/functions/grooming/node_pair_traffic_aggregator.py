import pandas as pd

from elnet.src.classes import AdvDiGraph
from elnet.src.functions.utils import compute_k_paths, create_path_df


def node_pair_traffic_aggregator(
    G: AdvDiGraph, traffic: pd.DataFrame
) -> pd.DataFrame:

    # Group by 'src' and 'dst' columns, aggregate the 'traffic' column with sum and count, and reset the index
    aggregated_df = (
        traffic.groupby(["src", "dst"])
        .agg({"traffic": ["sum", "count"]})
        .reset_index()
    )
    aggregated_df.columns = ["src", "dst", "traffic_sum", "pair_count"]

    k_shortest_path = 3
    path_dict = compute_k_paths(G, k_shortest_path)
    k_shortest_path_df = create_path_df(G, path_dict)

    # Clearing the previously assigned spectrums for the graph

    merged_traffic = pd.merge(
        aggregated_df, k_shortest_path_df, on=["src", "dst"], how="inner"
    )
    return merged_traffic
