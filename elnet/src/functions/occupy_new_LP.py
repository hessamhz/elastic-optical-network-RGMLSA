import pandas as pd

from elnet.src.classes import AdvDiGraph
from elnet.src.functions import choose_MF, deploy_OEO
from elnet.src.functions.occupy_spectrum import occupy_spectrum
from elnet.src.functions.spectrum_first_fit import spectrum_first_fit


def occupy_new_LP(
    G: AdvDiGraph,
    traffic_demand: pd.Series,
    transponders_df: pd.DataFrame,
    occupied_light_paths: list,
) -> tuple:
    """
    Occupy a new light path for a given demand if it is feasible
    """
    # Getting modulation level for all path of a request.
    mod_levels = choose_MF(G, transponders_df, traffic_demand["paths"])

    for i in range(len(mod_levels)):
        # Used to check the feasiblity of creating the light path
        is_feasible = True

        # Modulation format for the given path
        MF_id = mod_levels[i][1]
        path = traffic_demand["paths"][i][0]

        # Getting the modulation format row
        MF = transponders_df[transponders_df["OEO_id"] == int(MF_id)]

        # Suggesting an OEO deployment for the path
        OEO_on_nodes = deploy_OEO(G, path, MF.iloc[0, 5])

        # Total slots of a modulation format
        total_slots = MF.loc[MF_id]["numberofslots"]

        # Getting the total spectrum occupations of our current network
        occupations = G.spectrum_occupation()

        # check feasibility of assigning the light path with the given occupations
        for j in range(len(path) - 1):

            # The light path is C-band so the total of slots is 320
            if (320 - occupations[(path[j], path[j + 1])]) < total_slots:
                is_feasible = False

        # Trying to first fit the spectrum
        first_slot_to_occupy = spectrum_first_fit(G, path, total_slots)

        # Checking if we could first fit the spectrum
        if first_slot_to_occupy is None:
            is_feasible = False

        # Going to next path since it wasn't feasible
        if not is_feasible:
            continue

        # The light path is feasible, we derive the capacity of modulation format
        OEO_cap = MF.loc[MF_id]["data_rate"]

        # Making the data structure of light path
        light_path = {
            "path": path,
            "OEO_id": MF_id,
            "OEO_on_nodes": OEO_on_nodes,
            "num_slots": total_slots,
            "OEO_capacity": OEO_cap,
            "remaining_capacity": OEO_cap - traffic_demand["traffic"],
        }

        # Occupy the light path
        G = occupy_spectrum(G, path, first_slot_to_occupy, total_slots, MF_id)

        occupied_light_paths.append(light_path)

        # boolean is is_blocked
        return G, occupied_light_paths, False

    return G, occupied_light_paths, True
