from elnet.src.classes import AdvDiGraph
import networkx as nx
import pandas as pd


def create_path_df(G: AdvDiGraph, k_path_dict: list) -> pd.DataFrame:
    # Creating a new pd.DataFrame for services
    path_df = pd.DataFrame(columns=["src", "dst", "paths"])
    path_df = path_df.astype(
        {"src": "string", "dst": "string", "paths": "object"}
    )

    # Adding the dict values to the df
    for key, value in k_path_dict.items():
        new_row = pd.DataFrame(
            {
                "src": [key[0]],
                "dst": [key[1]],
                "paths": [value],
            },
        )
        path_df = pd.concat([path_df, new_row], ignore_index=True)

    return path_df
