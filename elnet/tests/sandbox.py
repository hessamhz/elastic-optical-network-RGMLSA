from src.classes import AdvDiGraph
from src.functions import node_reader
from src.functions import edges_reader
from src.functions import graph_display
import networkx as nx




df=node_reader("data/italianTopologyNodes.xlsx")
df_edges=edges_reader("data/italianTopologyEdges.xlsx")
N = AdvDiGraph()

N.add_nodes_from(df["node"].tolist())
node_latitude = dict(zip(df["node"], df["latitude"]))
node_longitude = dict(zip(df["node"], df["longitude"]))
nx.set_node_attributes(N, node_latitude,"node_latitude")
nx.set_node_attributes(N, node_longitude,"node_longitude")
dict_new=[]
for i in range(len(df_edges)):
    dict_new.append((df_edges["Source"][i],df_edges["Destination"][i],{"weight":df_edges["Weight"][i]}))

N.add_edges_from(dict_new)

graph_display(N,df)