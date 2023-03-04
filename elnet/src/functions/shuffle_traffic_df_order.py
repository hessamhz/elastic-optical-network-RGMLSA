#The frac keyword argument specifies the fraction of rows to return in the random sample,
#so frac=1 means to return all rows (in random order).

import random
import pandas as pd


def shuffle_traffic_df_order(traffic:pd.DataFrame,shuffling_parameter=50)->None:
    
    shuffled_traffic_list=[]
    for i in range(shuffling_parameter):
        shuffled_traffic = traffic.sample(frac=1, random_state=random.randint(0, 1000)).reset_index(drop=True)
        shuffled_traffic_list.append(shuffled_traffic)
    
    
    return shuffled_traffic_list 



