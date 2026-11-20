
import pickle
import networkx as nx
from pathlib import Path
from destination import get_building_node

GRAPH_PATH = Path(__file__).parent / "campus_graph.pkl"

with open(GRAPH_PATH, "rb") as f:
    graph = pickle.load(f)


# Enter starting building
source_name = input("Enter starting building: ").strip()

source_node = get_building_node(graph, source_name)

# Enter destination building
destination_name = input("Enter destination building: ").strip()

destination_node = get_building_node(graph, destination_name)


# Calculate shortest path
try:
    route = nx.dijkstra_path(
        graph,
        source_node,
        destination_node,
        weight="weight"
    )

    distance = nx.dijkstra_path_length(
        graph,
        source_node,
        destination_node,
        weight="weight"
    )

    print("\n========== NAVIGATION RESULTS ==========")
    print("Starting location:", source_name)
    print("Destination:", destination_name)
    print("Total route nodes:", len(route))
    print("Walking distance:", round(distance, 2), "meters")

    print("\nRoute:")
    for i, node in enumerate(route, 1):
        print(i, node)

except nx.NetworkXNoPath:
    print("No walking path available between these buildings.")
