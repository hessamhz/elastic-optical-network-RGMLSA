from elnet.src.classes import AdvDiGraph


def spectrum_first_fit(G: AdvDiGraph, path: list, num_slots: int) -> int:
    """
    find the first num_slots-wide free spectrum segment along the path
    """

    slots_in_band = 320

    for first_slot in range(slots_in_band - num_slots + 1):

        spectrum_is_free = True

        for link in zip(path, path[1:]):
            if (
                sum(
                    G.edges[link]["spectral_occupation"][
                        first_slot : first_slot + num_slots
                    ]
                )
                != 0
            ):
                spectrum_is_free = False
                break

        if spectrum_is_free:
            return first_slot

    return None
