def calculate_cost(occupied_light_paths: list) -> int:
    """
    calculate the total cost of a deployed network
    """
    cost = 0
    for index, light_path in occupied_light_paths.iterrows():
        cost += 2 * (len(light_path["OEO_on_nodes"]) - 1)
    return cost
