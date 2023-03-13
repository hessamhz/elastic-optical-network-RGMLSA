import math

import pandas as pd

from elnet.src.classes import AdvDiGraph
from elnet.src.functions.occupation.deploy_OEO import deploy_OEO
from elnet.src.functions.occupation.occupy_spectrum import occupy_spectrum
from elnet.src.functions.utils import spectrum_first_fit


def occupy_new_LP_JEC(
    G: AdvDiGraph,
    capacity: int,
    MF: pd.Series,
    path: list,
):
    """
    Occupy a new light path in JEC algorithm
    """
    # Suggesting an OEO deployment for the path
    OEO_on_nodes = deploy_OEO(G, path, MF["reach"])

    # Total slots of a modulation format
    total_slots = MF["numberofslots"]

    # Getting the total spectrum occupations of our current network
    occupations = G.spectrum_occupation()

    # check feasibility of assigning the light path with the given occupations
    for j in range(len(path) - 1):

        # The light path is C-band so the total of slots is 320
        if (320 - occupations[(path[j], path[j + 1])]) < total_slots:
            return G, None, True

    # Trying to first fit the spectrum
    first_slot_to_occupy = spectrum_first_fit(G, path, total_slots)

    # Checking if we could first fit the spectrum
    if first_slot_to_occupy is None:
        return G, None, True

    # The light path is feasible, we derive the capacity & reach of modulation format
    OEO_cap = MF["data_rate"]
    remaining_cap = OEO_cap - capacity
    OEO_reach = MF["reach"]

    OEO_cap_per_slot = OEO_cap / total_slots
    taken_slots = math.ceil(capacity / OEO_cap_per_slot)

    # Making the data structure of light path
    new_occupied_path = pd.DataFrame(
        {
            "path": [path],
            "OEO_id": MF["OEO_id"],
            "OEO_on_nodes": [OEO_on_nodes],
            "num_slots": [total_slots],
            "OEO_cap_per_slot": [OEO_cap_per_slot],
            "remaining_slots": [
                [([1] * taken_slots) + ([0] * (total_slots - taken_slots))]
                * (len(OEO_on_nodes) - 1)
            ],
            "OEO_capacity": [OEO_cap],
            "OEO_reach": [OEO_reach],
            "remaining_capacity": [[remaining_cap] * (len(OEO_on_nodes) - 1)],
        }
    )

    # Occupy the light path
    G = occupy_spectrum(
        G, path, first_slot_to_occupy, total_slots, MF["OEO_id"]
    )

    # boolean is is_blocked
    return G, new_occupied_path, False
