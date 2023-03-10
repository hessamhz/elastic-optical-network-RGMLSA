import pandas as pd

from elnet.src.classes import AdvDiGraph


def deploy_OEO(G: AdvDiGraph, path: list, OEO_reach: int) -> list:
    """
    Suggests an OEO deployment on a given path
    """
    distance = []

    # Adding the distance of the edges to a list
    for link in zip(path, path[1:]):
        distance.append(G.edges[link]["weight"])

    # First node of a given path should always have an OEO deployed
    current_distance = distance[0]
    nodes_with_OEO = [path[0]]

    # Setting OEOs in the path
    for i in range(1, len(distance)):

        # We greedily add edge distances until the OEO reach is not exceeded
        current_distance += distance[i]

        # We add an OEO when we exceed the OEO Reach
        if current_distance > OEO_reach:
            nodes_with_OEO.append(path[i])
            current_distance = distance[i]

    # Last node of a given path should always have an OEO deployed
    nodes_with_OEO.append(path[-1])

    return nodes_with_OEO
