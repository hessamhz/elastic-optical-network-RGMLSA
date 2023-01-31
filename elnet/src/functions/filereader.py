import pandas as pd


def node_reader(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)
    # Might need to change according to our plot at the end.
    # df["coordinates"] = list(zip(df["latitude"], df["longitude"]))
    # df = df.drop(columns=["latitude", "longitude"])
    return df
