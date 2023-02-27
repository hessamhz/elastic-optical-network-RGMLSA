from pathlib import Path

import networkx as nx
import pandas as pd
from mpl_toolkits.basemap import Basemap as Basemap
from elnet.src.classes import AdvDiGraph


def italy_graph():

    base_path = Path(__file__).resolve().parent
    it_node_p = (
        base_path / ".." / ".." / "data" / "national" / "italy-nodes.csv"
    )
    it_edge_p = (
        base_path / ".." / ".." / "data" / "national" / "italy-edges.csv"
    )

    df_it_nodes = pd.read_csv(it_node_p)
    df_it_edges = pd.read_csv(it_edge_p)

    G = nx.from_pandas_edgelist(
        df_it_edges,
        source="source",
        target="destination",
        edge_attr="weight",
        create_using=AdvDiGraph(),
    )

    G.graph["name"] = "Italy"
    m = Basemap(
        llcrnrlon=6.75,
        llcrnrlat=36.62,
        urcrnrlon=18.52,
        urcrnrlat=47.09,
        resolution="i",
        projection="merc",
    )
    G.basemap = m
    G.add_node_attrs_from_panda(df_it_nodes)

    return G
