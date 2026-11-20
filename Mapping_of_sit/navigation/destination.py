
# navigation/destination.py

import os
import sys
import pickle
import networkx as nx

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from campus_data import load_campus, CRS_METRES


GRAPH_FILE = os.path.join(
    os.path.dirname(__file__),
    "campus_graph.pkl"
)


def load_graph():

    with open(GRAPH_FILE, "rb") as f:
        return pickle.load(f)


def get_buildings():

    data = load_campus()

    buildings = data["buildings"]

    buildings = buildings[
        buildings["on_campus"]
    ]

    buildings = buildings.to_crs(CRS_METRES)

    return buildings


def nearest_graph_node(graph, x, y):

    nearest_node = min(
        graph.nodes,
        key=lambda node:
        (graph.nodes[node]["x"] - x) ** 2
        + (graph.nodes[node]["y"] - y) ** 2
    )

    return nearest_node


def get_building_node(graph, building_name):

    buildings = get_buildings()

    building = buildings[
        buildings["name"].str.lower()
        == building_name.lower()
    ]

    if building.empty:
        raise ValueError(
            f"Building not found: {building_name}"
        )

    # Building centroid
    centroid = building.geometry.iloc[0].centroid

    # Find nearest walking graph node
    node = nearest_graph_node(
        graph,
        centroid.x,
        centroid.y
    )

    return node


if __name__ == "__main__":

    graph = load_graph()

    print("\nAvailable buildings:")

    buildings = get_buildings()

    for name in buildings["name"].dropna().unique():
        print(name)

    destination_name = input(
        "\nEnter destination building: "
    )

    node = get_building_node(
        graph,
        destination_name
    )

    print("\nDestination graph node:")
    print(node)
