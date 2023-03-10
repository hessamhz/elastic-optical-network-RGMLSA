from elnet.src.classes import AdvDiGraph


def clear_spectrum(G: AdvDiGraph, num_slot=320) -> None:
    """
    We are using 4THz optical band for each link and
    We choose each slot has 12.5 GHz; so it makes 320 channels
    This function cleans the already occupied spectrums
    """
    for link in G.edges:
        G.edges[link]["spectral_occupation"] = [0] * num_slot
        G.edges[link]["OEOs"] = []

    return G
