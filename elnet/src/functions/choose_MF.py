import pandas as pd

from elnet.src.classes import AdvDiGraph


def choose_MF(
    G: AdvDiGraph,
    transponders: pd.DataFrame,
    traffic_tuples: list,
) -> None:
    """
    For choosing the MF we go for a greedy approach
    In this approach we just choose the OEO with the
    highest spectral efficiency
    """
    results = []
    for path_tuple in traffic_tuples:
        # Filter the rows based on the condition that reach > max_edge
        max_weight_edge = transponders.loc[
            transponders["reach"] > path_tuple[2]
        ]

        # Filter the rows based on the condition that reach > max_edge
        total_weight_edge = transponders.loc[
            transponders["reach"] > path_tuple[1]
        ]

        # Get the row with the maximum entropy for each case
        max_weight_row = max_weight_edge.loc[
            max_weight_edge["bits_entropy"].idxmax()
        ]

        max_total_path_row = total_weight_edge.loc[
            total_weight_edge["bits_entropy"].idxmax()
        ]

        results.append(
            (max_weight_row["OEO_id"], max_total_path_row["OEO_id"])
        )

    return results
