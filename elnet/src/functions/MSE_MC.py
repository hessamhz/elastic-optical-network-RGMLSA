import pandas as pd

from elnet.src.classes import AdvDiGraph
from elnet.src.functions import compute_k_paths, create_path_df
from elnet.src.functions.occupy_new_LP import occupy_new_LP


# MSE = Most Spectral Efficient
# MC = Maximum Capacity
def MSE_MC(
    G: AdvDiGraph,
    traffic: pd.DataFrame,
    transponders_df: pd.DataFrame,
    k_shortest_path=3,
) -> None:
    """
    Algorithm w.r.t Maximum Spectrum Efficiency and Maximum Capacity
    """
    # Making k shortest path dataframe
    path_dict = compute_k_paths(G, k_shortest_path)
    k_shortest_path_df = create_path_df(G, path_dict)

    # Clearing the previously assigned spectrums for the graph
    G.clear_spectrum()

    merged_traffic = pd.merge(
        traffic, k_shortest_path_df, on=["src", "dst"], how="inner"
    )

    # Trying to occupy the first demand
    G, occupied_light_paths, is_blocked = occupy_new_LP(
        G, merged_traffic.iloc[0], transponders_df, []
    )

    # We could not make the light path for the first demand
    # this happens probably due to a bad topology
    if is_blocked:
        return None

    # Auditing the status of each demand
    service_status = [1]

    for j in range(1, len(merged_traffic)):

        """
        k_paths=merged_traffic.loc[j]["paths"]

        for path in k_paths:
            for info in occupied_infos:
                OEO_nodes = info.get("OEO_on_nodes")
                src = path[0][0]; dst = path[0][-1]
                if src in OEO_nodes and dst in OEO_nodes:
                    if OEO_nodes.index(dst) > OEO_nodes.index(src):
                        # print("I was here", src, dst, OEO_nodes, info.get("Path"))
        """

        # Occupying a new light path if it is feasible since we could not
        # assign our demand to an existing light path
        G, occupied_light_paths, is_blocked = occupy_new_LP(
            G, merged_traffic.loc[j], transponders_df, occupied_light_paths
        )

        if is_blocked:
            service_status.append(0)
            continue
        else:
            service_status.append(1)

    return occupied_light_paths, service_status
