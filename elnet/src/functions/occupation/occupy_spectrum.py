from elnet.src.classes import AdvDiGraph


def occupy_spectrum(
    G: AdvDiGraph, path: list, first_slot: int, num_slots: int, OEO_id: int
) -> AdvDiGraph:
    """
    Occupy Spectrum As Number of Slots and starting
    with first slot that returns from first fit function
    """
    for link in zip(path, path[1:]):

        G.edges[link]["OEOs"].append(OEO_id)

        for slot_shift in range(num_slots):
            G.edges[link]["spectral_occupation"][first_slot + slot_shift] = 1

    return G
