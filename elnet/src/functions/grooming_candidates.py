import math

import pandas as pd


def find_grooming_candidates(
    traffic_demand: pd.Series,
    occupied_light_paths: pd.DataFrame,
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

        for j, occupied_LP in occupied_light_paths.iterrows():
            # Getting list of deployed OEOs
            OEO_on_nodes = occupied_LP["OEO_on_nodes"]

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
            min_capacity = min(occupied_LP["remaining_capacity"])

            if traffic > min_capacity:
                continue

            if min_capacity - traffic < 0:
                continue

            # Checking if we have enough slots
            taken_slots = math.ceil(
                traffic_demand["traffic"] / occupied_LP["OEO_cap_per_slot"]
            )

            # Checking the feasibility of a possible continous path
            remaining_slots = occupied_LP["remaining_slots"]
            first_fit_ceiling = -1

            for l in range(occupied_LP["num_slots"] - taken_slots + 1):
                for k in range(src_index, dst_index):
                    is_slot_occupied = False
                    for o in range(taken_slots):
                        if remaining_slots[k][l + o]:
                            # print(remaining_slots, l, o)
                            is_slot_occupied = True
                            break
                    if is_slot_occupied:
                        break
                if not is_slot_occupied:
                    first_fit_ceiling = l
                    break

            # No continuous spectrum found in the sub-path
            if first_fit_ceiling == -1:
                continue

            # We add this LP to our candiate LP to later on decide on it
            candidate_LPs.append(
                {
                    "path_id": i,
                    "LP_id": j,
                    "OEO_capacity": occupied_LP["OEO_capacity"],  # MSE-MC
                    "OEO_slots": taken_slots,  # MSE-MS
                    "first_fit_ceiling": first_fit_ceiling,
                    "src_index": src_index,
                    "dst_index": dst_index,
                }
            )

    return candidate_LPs
