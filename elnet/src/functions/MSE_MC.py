import pandas as pd

from elnet.src.classes import AdvDiGraph
from elnet.src.functions import compute_k_paths, create_path_df,shuffle_traffic_df_order,check_SO_for_groooming_intermediate_nodes,choose_MF,spectrum_first_fit,occupy_spectrum,spectrum_occupation

# MSE = Most Spectral Efficient
# MC = Maximum Capacity
def MSE_MC(G: AdvDiGraph, traffic: pd.DataFrame, k_shortest_path=3) -> None:
    # Making k shortest path dataframe
 
    #need to solve this 
    df_transponders = pd.read_csv(transponders.csv)

    path_dict = compute_k_paths(G, k_shortest_path)
    k_shortest_path_df = create_path_df(G, path_dict)

    shuffled_traffic_list=shuffle_traffic_df_order(traffic)
    overall_traffic_distribution=[]
    for i in range((len(shuffled_traffic_list))):
        # Creating the joined tables of traffic and k_shortest_path for being more optimized
        merged_traffic = pd.merge(
        shuffled_traffic_list[i], k_shortest_path_df, on=["src", "dst"], how="inner")

        overall_traffic_distribution.append(merged_traffic)
    
    
    for i in range(len(overall_traffic_distribution)):
        current_traffic=overall_traffic_distribution[i]
        OEO_for_each_demand=[]
        
        #looking for each traffic request set among 50 set 
        for j in range(len(current_traffic)):
            first_path=current_traffic.loc[j]["paths"][0][0]
            second_path=current_traffic.loc[j]["paths"][1][0]
            third_path=current_traffic.loc[j]["paths"][2][0]
            
            print(first_path,"deneme")
            modulation_levels=choose_MF(N,df_transponders,current_traffic.loc[j]['paths'])
            
            corresponding_OEO=df_transponders[df_transponders['OEO_id']==modulation_levels[0][1]]
            
            num_slots_will_be_occupied=corresponding_OEO.loc[modulation_levels[0][1]]['num_slots']
            
            for i in range(num_slots_will_be_occupied):
                
                if check_SO_for_groooming_intermediate_nodes(G,current_traffic.loc[j],first_path,i):
                    
                    first_slot_to_occupy=spectrum_first_fit(G,first_path,num_slots_will_be_occupied-i)
                                                            
                    occupied=occupy_spectrum(G,first_path,first_slot_to_occupy,i)
                
           


    return overall_traffic_distribution
