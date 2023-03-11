import pandas as pd

from elnet.src.classes import AdvDiGraph
from elnet.src.functions import compute_k_paths, create_path_df
from elnet.src.functions.grooming_candidates import find_grooming_candidates
from elnet.src.functions.occupy_new_LP import occupy_new_LP


# MSE = Most Spectral Efficient
# MC = Maximum Capacity
def MSE_MS(
    G: AdvDiGraph,
    traffic: pd.DataFrame,
    transponders_df: pd.DataFrame,
    k_shortest_path=3,
) -> None:
    """
    Algorithm w.r.t Maximum Spectrum Efficiency and Minimum Spectrum
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

        demand = merged_traffic.loc[j]

        goorming_candidates = find_grooming_candidates(
            demand, occupied_light_paths
        )

        # Finding MSE-MS => Finding the minimum spectrum
        grooming_candidates_len = len(goorming_candidates)
        if grooming_candidates_len > 0:
            min_spectrum = 10000
            grooming_candidate_index = None

            # Finding the least spectrums (lower spacing)
            for k in range(grooming_candidates_len):
                OEO_slots = goorming_candidates[k].get("OEO_slots")
                if min_spectrum > OEO_slots:
                    min_spectrum = OEO_slots
                    grooming_candidate_index = k

            # Occupy the existing path
            previous_remaining_cap = occupied_light_paths[
                grooming_candidate_index
            ]["remaining_capacity"]
            occupied_light_paths[grooming_candidate_index][
                "remaining_capacity"
            ] = [x - demand["traffic"] for x in previous_remaining_cap]

            # Add the service as done and move to the next traffic
            service_status.append(1)
            continue

        # Occupying a new light path if it is feasible since we could not
        # assign our demand to an existing light path
        G, occupied_light_paths, is_blocked = occupy_new_LP(
            G, demand, transponders_df, occupied_light_paths
        )

        if is_blocked:
            service_status.append(0)
            continue
        else:
            service_status.append(1)

    return occupied_light_paths, service_status
