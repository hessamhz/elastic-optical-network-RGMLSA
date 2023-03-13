from pathlib import Path

import networkx as nx
import pandas as pd
from mpl_toolkits.basemap import Basemap as Basemap

from elnet.src.classes import AdvDiGraph
from elnet.src.functions import (
    JEC,
    MSE_MC,
    MSE_MS,
    calculate_cost,
    calculate_utilization,
    compute_k_paths,
    generate_services,
    occupy_new_LP,
    shuffle_traffic_df_order,
)
from elnet.tests.utils import eu_graph

G = eu_graph()
G.create_map()
it_node_p = "elnet/data/continental/europe-nodes.csv"
it_node = pd.read_csv(it_node_p)
# services = pd.read_csv("elnet/data/tests/sample-traffics.csv")
transponders = pd.read_csv("elnet/data/params/transponders.csv")

results = pd.DataFrame(
    columns=[
        "traffic_id",
        "shuffle_id",
        "type",
        "total_traffic",
        "total_LP",
        "cost",
        "served_services",
        "LP_utilized",
        "total_LP_utilized",
        "cap_utilized",
        "total_cap_utilized",
        "four_slot_count",
        "total_slots",
        "OEO_slots_occupied",
    ]
)

occupied_light_paths = pd.DataFrame(
    columns=[
        "path",
        "OEO_id",
        "OEO_on_nodes",
        "num_slots",
        "OEO_cap_per_slot",
        "remaining_slots",
        "OEO_capacity",
        "OEO_reach",
        "remaining_capacity",
    ]
)


total_slots = 320 * G.number_of_edges()
for i in range(20):

    services, done = generate_services(350, it_node)
    service_slices = [shuffle_traffic_df_order(services)]
    for l in range(45):
        services, done = generate_services(50, it_node)
        service_slices.append(services)

    for j in range(20):
        print(f"traffic {i+1} - shuffle {j+1}")
        for p in range(len(service_slices)):
            service_slices[p] = shuffle_traffic_df_order(service_slices[p])

        occupied_light_paths = occupied_light_paths.drop(
            index=occupied_light_paths.index
        )
        #### MSE_MC
        G.clear_spectrum()

        service_count = 0
        merged_slices = pd.DataFrame()
        cum_served_count = 0
        for t in range(len(service_slices)):
            service_slice = service_slices[t]
            service_count += service_slice.shape[0]
            merged_slices = pd.concat([merged_slices, service_slice])

            q = MSE_MC(
                G,
                service_slice,
                transponders,
                occupied_light_paths,
                t,
                3,
            )
            # print(q)
            occupied_light_paths, service_status, G = q
            x = calculate_utilization(occupied_light_paths)

            counter = 0
            for ind, info in occupied_light_paths.iterrows():
                if info["num_slots"] == 4:
                    counter += 1

            spectrum_occupation = G.spectrum_occupation()
            OEO_slots = 0
            for key, element in spectrum_occupation.items():
                OEO_slots += element

            cum_served_count += sum(service_status)
            new_row = pd.DataFrame(
                {
                    "traffic_id": [i],
                    "shuffle_id": [j],
                    "type": ["MSE_MC"],
                    "total_traffic": [merged_slices["traffic"].sum()],
                    "total_LP": [len(occupied_light_paths)],
                    "cost": [calculate_cost(occupied_light_paths)],
                    "served_services": [cum_served_count],
                    "total_services": [merged_slices.shape[0]],
                    "LP_utilized": [x[0][0]],
                    "total_LP_utilized": [x[0][1]],
                    "cap_utilized": [x[1][0]],
                    "total_cap_utilized": [x[1][1]],
                    "four_slot_count": [counter],
                    "total_slots": total_slots,
                    "OEO_slots_occupied": OEO_slots,
                },
            )

            if cum_served_count / merged_slices.shape[0] < 0.99:
                results = pd.concat([results, new_row], ignore_index=True)
                results.to_csv("benchmark-eu.csv", index=False)
                break

        #### MSE_MS
        occupied_light_paths = occupied_light_paths.drop(
            index=occupied_light_paths.index
        )

        G.clear_spectrum()

        service_count = 0
        merged_slices = pd.DataFrame()
        cum_served_count = 0
        for t in range(len(service_slices)):
            service_slice = service_slices[t]
            service_count += service_slice.shape[0]
            merged_slices = pd.concat([merged_slices, service_slice])

            occupied_light_paths, service_status, G = MSE_MS(
                G, service_slice, transponders, occupied_light_paths, t, 3
            )
            x = calculate_utilization(occupied_light_paths)

            counter = 0
            for ind, info in occupied_light_paths.iterrows():
                if info["num_slots"] == 4:
                    counter += 1

            spectrum_occupation = G.spectrum_occupation()
            OEO_slots = 0
            for key, element in spectrum_occupation.items():
                OEO_slots += element

            cum_served_count += sum(service_status)
            new_row = pd.DataFrame(
                {
                    "traffic_id": [i],
                    "shuffle_id": [j],
                    "type": ["MSE_MS"],
                    "total_traffic": [merged_slices["traffic"].sum()],
                    "total_LP": [len(occupied_light_paths)],
                    "cost": [calculate_cost(occupied_light_paths)],
                    "served_services": [cum_served_count],
                    "total_services": [merged_slices.shape[0]],
                    "LP_utilized": [x[0][0]],
                    "total_LP_utilized": [x[0][1]],
                    "cap_utilized": [x[1][0]],
                    "total_cap_utilized": [x[1][1]],
                    "four_slot_count": [counter],
                    "total_slots": total_slots,
                    "OEO_slots_occupied": OEO_slots,
                },
            )

            if cum_served_count / merged_slices.shape[0] < 0.99:
                results = pd.concat([results, new_row], ignore_index=True)
                results.to_csv("benchmark-eu.csv", index=False)
                break

        #### JEC
        occupied_light_paths = occupied_light_paths.drop(
            index=occupied_light_paths.index
        )

        G.clear_spectrum()

        service_count = 0
        merged_slices = pd.DataFrame()
        cum_served_count = 0
        for service_slice in service_slices:
            service_count += service_slice.shape[0]
            merged_slices = pd.concat([merged_slices, service_slice])

            occupied_light_paths, service_status, G = JEC(
                G, service_slice, transponders, occupied_light_paths, 3
            )
            x = calculate_utilization(occupied_light_paths)

            counter = 0
            for ind, info in occupied_light_paths.iterrows():
                if info["num_slots"] == 4:
                    counter += 1

            spectrum_occupation = G.spectrum_occupation()
            OEO_slots = 0
            for key, element in spectrum_occupation.items():
                OEO_slots += element

            cum_served_count += sum(service_status)
            new_row = pd.DataFrame(
                {
                    "traffic_id": [i],
                    "shuffle_id": [j],
                    "type": ["JEC"],
                    "total_traffic": [merged_slices["traffic"].sum()],
                    "total_LP": [len(occupied_light_paths)],
                    "cost": [calculate_cost(occupied_light_paths)],
                    "served_services": [cum_served_count],
                    "total_services": [merged_slices.shape[0]],
                    "LP_utilized": [x[0][0]],
                    "total_LP_utilized": [x[0][1]],
                    "cap_utilized": [x[1][0]],
                    "total_cap_utilized": [x[1][1]],
                    "four_slot_count": [counter],
                    "total_slots": total_slots,
                    "OEO_slots_occupied": OEO_slots,
                },
            )

            if cum_served_count / merged_slices.shape[0] < 0.99:
                results = pd.concat([results, new_row], ignore_index=True)
                results.to_csv("benchmark-eu.csv", index=False)
                break
