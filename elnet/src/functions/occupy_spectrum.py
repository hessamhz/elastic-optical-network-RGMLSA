from elnet.src.classes import AdvDiGraph


# Occupy Spectrum As Number of Slots and starting with first slot that returns from first fit function
def occupy_spectrum(
    G: AdvDiGraph,
    path: list,
    first_slot: int,
    num_slots: int,
) -> None:

    for link in zip(path, path[1:]):
        for slot_shift in range(num_slots):
            G.edges[link]["spectrum_slots"][first_slot + slot_shift] = 1
