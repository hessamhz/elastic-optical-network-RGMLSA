import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from mpl_toolkits.basemap import Basemap as Basemap


class AdvDiGraph(nx.DiGraph):
    def __init__(self, data=None, name=None, basemap=None, **attr):
        super().__init__(data=data, name=name, **attr)
        self.basemap = basemap

    def add_node_attrs_from_panda(self, node_attrs: pd.DataFrame) -> None:
        attrs = node_attrs.set_index("node").to_dict("index")
        nx.set_node_attributes(self, attrs)

    def clear_spectrum(self) -> None:
        """
        We are using 4THz optical band for each link and
        We choose each slot has 12.5 GHz; so it makes 320 channels
        This function cleans the already occupied spectrums
        """
        for link in self.edges:
            self.edges[link]["spectral_occupation"] = [0] * 320
            self.edges[link]["OEOs"] = []

    def spectrum_occupation(self) -> dict:
        """
        Function for calculating a dictionary of SOs that are occupied
        """
        slots_occupied = {}

        for link in self.edges:
            slots_occupied[link] = sum(self.edges[link]["spectral_occupation"])

        return slots_occupied

    def create_map(self) -> None:
        plt.figure(figsize=(9, 9))
        # get a dictionary of attribute values for all nodes
        longitude_attrs = nx.get_node_attributes(self, "longitude")
        latitude_attrs = nx.get_node_attributes(self, "latitude")

        # checking if values are given right
        if (
            len(longitude_attrs) != self.number_of_nodes()
            or len(latitude_attrs) != self.number_of_nodes()
        ):
            raise ValueError("Node attributes must be set accordingly.")
        # using dictionary is more efficient that iterating over attributes

        e_x, e_y = self.basemap(
            list(longitude_attrs.values()),
            list(latitude_attrs.values()),
        )
        pos = {}
        for count, elem in enumerate(self.nodes()):
            pos[elem] = (e_x[count], e_y[count])

        # drawing the map using nx
        nx.draw_networkx(
            self,
            pos,
            node_size=100,
            edgelist=self.edges(),
            node_color="r",
            width=2,
            label=self.name,
        )
        self.basemap.drawcountries(linewidth=1)
        self.basemap.drawstates(linewidth=1.5)
        self.basemap.drawcoastlines(linewidth=1)
        self.basemap.drawparallels(
            range(0, 90, 5), linewidth=0.5, labels=[1, 0, 0, 0]
        )
        self.basemap.drawmeridians(
            range(-180, 180, 5), linewidth=0.5, labels=[0, 0, 0, 1]
        )
        plt.tight_layout()
        plt.savefig(f"{self.name}.png")
