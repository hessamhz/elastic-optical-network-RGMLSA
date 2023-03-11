import pandas as pd


def find_grooming_candidates(
    traffic_demand: pd.Series,
    occupied_light_paths: list,
) -> list:
    """
    Finding the Grooming candidate that fits the demand into an already occupied light path
    """
    candidate_LPs = []
    for i in range(len(traffic_demand["paths"])):
        # Used to check the feasiblity of creating the light path
        is_feasible = True

        # Iterating over the candidate paths
        path = traffic_demand["paths"][i][0]
        traffic = traffic_demand["traffic"]

        for j in range(len(occupied_light_paths)):
            occupied_LP = occupied_light_paths[j]
            # Getting list of deployed OEOs
            OEO_on_nodes = occupied_LP.get("OEO_on_nodes")

            # Checking if the starting and ending node of the path exists in deployed OEOs
            try:
                src_index = OEO_on_nodes.index(path[0])
                dst_index = OEO_on_nodes.index(path[-1])
            except ValueError:
                # Not in OEO => Continue
                continue

            # Checking if the order is right (graph is bidirectional)
            if src_index > dst_index:
                continue

            # We need to check if we have enough capacity in this canidate LP
            min_capacity = min(occupied_LP.get("remaining_capacity"))
            if j == 0:
                print(
                    "kir",
                    traffic,
                    min_capacity,
                    occupied_LP.get("remaining_capacity"),
                )
            if traffic > min_capacity:
                continue

            if min_capacity - traffic < 0:
                continue

            print(
                "min cap:",
                min_capacity,
                traffic,
                occupied_LP.get("remaining_capacity"),
            )

            # We add this LP to our candiate LP to later on decide on it
            candidate_LPs.append(
                {
                    "path_id": i,
                    "LP_id": j,
                    "OEO_capacity": occupied_LP.get("OEO_capacity"),  # MSE-MC
                    "OEO_slots": occupied_LP.get("num_slots"),  # MSE-MS
                }
            )

    return candidate_LPs
