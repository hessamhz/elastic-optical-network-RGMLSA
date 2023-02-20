from src.classes import AdvDiGraph
from src.functions import node_reader
import networkx as nx

G = AdvDiGraph()
G.add_edges_from([(1, 2), (2, 1), (3, 2)])
G.add_edge(1, 2)
G.graph
print(G.nodes())
print(G.edges())

df = node_reader("elnet/data/italy-nodes.csv")
N = AdvDiGraph()
N.add_nodes_from(df["node"].tolist())
node_latitude = dict(zip(df["node"], df["latitude"]))
node_longitude = dict(zip(df["node"], df["longitude"]))
nx.set_node_attributes(N, node_latitude)
nx.set_node_attributes(N, node_longitude)
print(N.nodes)
print(N["Milan"])
