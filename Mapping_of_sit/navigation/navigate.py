
import networkx as nx
import pickle
import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from navigation.destination import get_building_node


# Load campus graph
GRAPH_PATH = Path(__file__).parent / "campus_graph.pkl"

with open(GRAPH_PATH, "rb") as file:
    graph = pickle.load(file)


def nearest_graph_node(graph, x, y):
    """Find nearest graph node to given coordinates."""
    return min(
        graph.nodes,
        key=lambda node: (node[0] - x) ** 2 + (node[1] - y) ** 2
    )


def calculate_route(source, destination):
    """Calculate shortest walking route using Dijkstra."""
    try:
        route = nx.dijkstra_path(
            graph,
            source,
            destination,
            weight="weight"
        )

        distance = nx.dijkstra_path_length(
            graph,
            source,
            destination,
            weight="weight"
        )

        return route, distance

    except nx.NetworkXNoPath:
        print("No walking route exists between these locations.")
        return None, None


def main():

    # Select destination
    destination_name = input("Enter destination building: ")

    destination_node = get_building_node(
        graph,
        destination_name
    )

    if destination_node is None:
        print("Destination not found.")
        return

    # Temporary starting node for testing
    largest_component = max(
        nx.connected_components(graph),
        key=len
    )

    test_source = next(iter(largest_component))

    print("\nStarting graph node:", test_source)
    print("Destination graph node:", destination_node)

    # Calculate route
    route, distance = calculate_route(
        test_source,
        destination_node
    )

    if route is None:
        return

    print("\n========== ROUTE RESULTS ==========")
    print("Destination:", destination_name)
    print("Total route nodes:", len(route))
    print("Walking distance:", round(distance, 2), "meters")

    print("\nRoute coordinates:")

    for i, node in enumerate(route):
        print(i + 1, node)


if __name__ == "__main__":
    main()
