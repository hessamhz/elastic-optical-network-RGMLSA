from pathlib import Path

import networkx as nx
import pandas as pd
from mpl_toolkits.basemap import Basemap as Basemap
from elnet.src.classes import AdvDiGraph


def eu_graph():

    base_path = Path(__file__).resolve().parent
    eu_node_p = (
        base_path / ".." / ".." / "data" / "continental" / "europe-nodes.csv"
    )
    eu_edge_p = (
        base_path / ".." / ".." / "data" / "continental" / "europe-edges.csv"
    )

    df_eu_nodes = pd.read_csv(eu_node_p)
    df_eu_edges = pd.read_csv(eu_edge_p)

    G = nx.from_pandas_edgelist(
        df_eu_edges,
        source="source",
        target="destination",
        edge_attr="weight",
        create_using=AdvDiGraph(),
    )

    G.graph["name"] = "Europe"
    m = Basemap(
        llcrnrlon=-2.5,
        llcrnrlat=37.5,
        urcrnrlon=22.5,
        urcrnrlat=55,
        resolution="i",
        projection="merc",
    )
    G.basemap = m
    G.add_node_attrs_from_panda(df_eu_edges)

    return G
