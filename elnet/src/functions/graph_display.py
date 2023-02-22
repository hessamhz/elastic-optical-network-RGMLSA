
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from src.classes import AdvDiGraph
from src.functions import node_reader
from src.functions import edges_reader



df=node_reader("data/italianTopologyNodes.xlsx")
df_edges=edges_reader("data/italianTopologyEdges.xlsx")

N = AdvDiGraph()
N.add_nodes_from(df["node"].tolist())
node_latitude = dict(zip(df["node"], df["latitude"]))
node_longitude = dict(zip(df["node"], df["longitude"]))
nx.set_node_attributes(N, node_latitude,"node_latitude")
nx.set_node_attributes(N, node_longitude,"node_longitude")
dict_new=[]
for i in range(len(df_new)):
    dict_new.append((df_new["Source"][i],df_new["Destination"][i],{"weight":df_new["Weight"][i]}))

N.add_edges_from(dict_new)



positions = dict(zip(N.nodes, coordinates))
nx.draw_networkx(N, positions, node_size=100,edgelist=N.edges(), node_color="r",width=2,label="ItalianNetwork")
plt.show()