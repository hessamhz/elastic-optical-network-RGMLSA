import random

import pandas as pd


def shuffle_traffic_df_order(traffic: pd.DataFrame) -> pd.DataFrame:
    """
    Reshuffling the list of traffic
    """

    shuffled_traffic = traffic.sample(
        frac=1, random_state=random.randint(0, 1000)
    ).reset_index(drop=True)

    return shuffled_traffic
