import math

import pandas as pd

from elnet.src.classes import AdvDiGraph
from elnet.src.functions import (
    choose_MF_for_JEC,
    node_pair_traffic_aggregator,
    occupy_new_LP_JEC,
)


def JEC(
    G: AdvDiGraph,
    traffic_df: pd.DataFrame,
    transponders_df: pd.DataFrame,
    occupied_light_paths: pd.DataFrame,
    k_shortest_path=3,
) -> tuple:
    """
    Algorithm w.r.t Just Enough Capacity
    """

    aggregated_traffic = node_pair_traffic_aggregator(G, traffic_df)

    service_status = []

    """
    occupied_light_paths = pd.DataFrame(
        columns=[
            "path",
            "OEO_id",
            "OEO_on_nodes",
            "num_slots",
            "OEO_cap_per_slot",
            "remaining_slots",
            "OEO_capacity",
            "OEO_reach",
            "remaining_capacity",
        ]
    )
    """

    # G.clear_spectrum()

    for index, demand in aggregated_traffic.iterrows():
        # Most spectral efficient MF for aggregated traffic
        MF = choose_MF_for_JEC(transponders_df, demand)
        # Capacity of the OEO
        MF_cap = transponders_df.iloc[MF[0]]["data_rate"]
        pair_count = demand["pair_count"]
        path = demand["paths"][MF[3]][0]
        # Total number of services served in this aggregated traffic
        services_served = 0
        for j in range(MF[1]):
            if j != MF[1] - 1:
                # Occupy the LP
                demand_capacity_slice = MF_cap
                G, new_occupied_path, is_blocked = occupy_new_LP_JEC(
                    G,
                    demand_capacity_slice,
                    transponders_df.iloc[MF[0]],
                    path,
                )
                if is_blocked:
                    break
                services_served += math.ceil(pair_count / MF[1]) - (
                    math.ceil(pair_count / MF[1]) * MF[1] - pair_count
                )
            else:
                demand_capacity_slice = (
                    demand["traffic_sum"]
                    - math.floor(demand["traffic_sum"] / MF_cap) * MF_cap
                )
                G, new_occupied_path, is_blocked = occupy_new_LP_JEC(
                    G,
                    demand_capacity_slice,
                    transponders_df.iloc[MF[0]],
                    path,
                )
                if is_blocked:
                    break
                services_served += math.ceil(pair_count / MF[1])

            # Updating the LP Datastructure
            occupied_light_paths = pd.concat(
                [occupied_light_paths, new_occupied_path],
                ignore_index=True,
            )

        # adding the number of services served
        service_status.append(services_served)

    return (occupied_light_paths, service_status, G)
