def calculate_utilization(occupied_light_paths: list) -> tuple:
    """
    calculate the total cost of a deployed network
    """
    occupied_slots = 0
    total_slots = 0
    occupied_capacity = 0
    total_capacity = 0
    for index, light_path in occupied_light_paths.iterrows():
        OEO_on_nodes = light_path["OEO_on_nodes"]
        path = light_path["path"]
        remaining_slots = light_path["remaining_slots"]
        remaining_capacity = light_path["remaining_capacity"]
        for i in range(len(light_path["OEO_on_nodes"]) - 1):
            number_of_links = path.index(OEO_on_nodes[i + 1]) - path.index(
                OEO_on_nodes[i]
            )
            occupied_slots += number_of_links * remaining_slots[i].count(1)
            total_slots += number_of_links * light_path["num_slots"]
            occupied_capacity += number_of_links * remaining_capacity[i]
            total_capacity += number_of_links * light_path["OEO_capacity"]
    return (occupied_slots, total_slots), (occupied_capacity, total_capacity)
