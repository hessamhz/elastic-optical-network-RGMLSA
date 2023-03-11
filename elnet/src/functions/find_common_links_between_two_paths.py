from elnet.src.classes import AdvDiGraph


def find_common_links_between_two_paths(
    G: AdvDiGraph, traffic_demand1_path: list, traffic_demand2_path: list
):

    common_links = []
    common_nodes = set(traffic_demand1_path) & set(traffic_demand2_path)

    for node in common_nodes:
        # Find the index of the current node in both paths
        index1 = traffic_demand1_path.index(node)
        index2 = traffic_demand2_path.index(node)

        # If the node is not the first node in either path, add the link that connects it to the previous node
        if index1 > 0 and index2 > 0:
            link1 = (traffic_demand1_path[index1 - 1], node)
            link2 = (traffic_demand2_path[index2 - 1], node)
            if link1 == link2:
                common_links.append(link1)

    return common_links
