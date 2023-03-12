import pandas as pd

from elnet.src.classes import AdvDiGraph
from elnet.src.functions import compute_k_paths, create_path_df
from elnet.src.functions.grooming_candidates import find_grooming_candidates
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

    # Clearing the previously assigned spectrums for the graph
    G.clear_spectrum()

    merged_traffic = pd.merge(
        traffic, k_shortest_path_df, on=["src", "dst"], how="inner"
    )

    # Trying to occupy the first demand
    G, new_occupied_light_paths, is_blocked = occupy_new_LP(
        G, merged_traffic.iloc[0], transponders_df
    )

    occupied_light_paths = pd.concat(
        [occupied_light_paths, new_occupied_light_paths], ignore_index=True
    )

    # We could not make the light path for the first demand
    # this happens probably due to a bad topology
    if is_blocked:
        return None

    # Auditing the status of each demand
    service_status = [1]

    for j in range(1, len(merged_traffic)):

        demand = merged_traffic.loc[j]

        goorming_candidates = find_grooming_candidates(
            demand, occupied_light_paths
        )

        # Finding MSE-MC => Finding the highest capacity
        grooming_candidates_len = len(goorming_candidates)
        if grooming_candidates_len > 0:
            max_capacity = 0
            grooming_candidate_index = None

            # Finding the most capacity
            for k in range(grooming_candidates_len):
                OEO_capacity = goorming_candidates[k].get("OEO_capacity")
                if max_capacity < OEO_capacity:
                    max_capacity = OEO_capacity
                    grooming_candidate_index = goorming_candidates[k].get(
                        "LP_id"
                    )

            # Occupy the existing path
            previous_remaining_cap = occupied_light_paths.iloc[
                grooming_candidate_index
            ]["remaining_capacity"]

            for x in range(len(previous_remaining_cap)):
                occupied_light_paths.iloc[grooming_candidate_index][
                    "remaining_capacity"
                ][x] -= demand["traffic"]

            for x in range(goorming_candidates.get("taken_slots")):
                for y in range(
                    goorming_candidates.get("src_index"),
                    goorming_candidates.get("dst_index") + 1,
                ):
                    occupied_light_paths.iloc[grooming_candidate_index][
                        "remaining_slots"
                    ][y] = 1

            # Add the service as done and move to the next traffic
            service_status.append(1)
            continue

        # Occupying a new light path if it is feasible since we could not
        # assign our demand to an existing light path
        G, new_occupied_light_paths, is_blocked = occupy_new_LP(
            G, demand, transponders_df
        )
        occupied_light_paths = pd.concat(
            [occupied_light_paths, new_occupied_light_paths], ignore_index=True
        )

        if is_blocked:
            service_status.append(0)
            continue
        else:
            service_status.append(1)

    return occupied_light_paths, service_status
