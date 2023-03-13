import math

import pandas as pd


def choose_MF_for_JEC(
    transponders: pd.DataFrame,
    traffic_demand: pd.DataFrame,
) -> list:
    """
    For choosing the MF we go for a greedy approach
    In this approach we just choose the OEO with the
    highest data rate and if it is greater than highest
    data rate we will split it.
    """
    traffic_tuples = traffic_demand["paths"]
    traffic = traffic_demand["traffic_sum"]

    min_slots = 100000
    for i in range(len(traffic_tuples)):
        path_tuple = traffic_tuples[i]
        # Filter the rows based on the condition that reach > max_edge
        max_weight_edge = transponders.loc[
            transponders["reach"] > path_tuple[2]
        ]

        max_traffic_OEO = max_weight_edge["data_rate"].max()

        if traffic < max_traffic_OEO:

            traffic_ceiling = math.ceil(traffic / 100) * 100
            max_weight_rows = max_weight_edge.loc[
                (max_weight_edge["data_rate"] >= traffic_ceiling)
            ]
            max_weight_row = max_weight_rows.loc[
                max_weight_rows["data_rate"].idxmin()
            ]

            occupied_slots = max_weight_row["numberofslots"]
            if occupied_slots < min_slots:
                # min_slots_index for path
                min_slots = occupied_slots
            results = (
                max_weight_row["OEO_id"],
                1,
                max_weight_row["numberofslots"],
                i,
            )

        else:
            max_weight_row = max_weight_edge.loc[
                max_weight_edge["data_rate"].idxmax()
            ]
            number_of_OEO = math.ceil(traffic / max_weight_row["data_rate"])

            occupied_slots = max_weight_row["numberofslots"] * number_of_OEO
            if occupied_slots < min_slots:
                # min_slots_index for path
                min_slots = occupied_slots

            results = (
                max_weight_row["OEO_id"],
                number_of_OEO,
                max_weight_row["numberofslots"],
                i,
            )

    return results
