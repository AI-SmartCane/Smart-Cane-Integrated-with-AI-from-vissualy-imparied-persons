
# navigation/dijkstra.py

import os
import pickle
import networkx as nx


GRAPH_FILE = os.path.join(
    os.path.dirname(__file__),
    "campus_graph.pkl"
)


def load_graph():

    with open(GRAPH_FILE, "rb") as f:
        graph = pickle.load(f)

    return graph


def shortest_path(graph, source, destination):

    try:

        path = nx.dijkstra_path(
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

        return path, distance

    except nx.NetworkXNoPath:

        print("No walking path available.")
        return [], float("inf")


def main():

    graph = load_graph()

    # Select the largest connected component
    components = list(nx.connected_components(graph))

    largest_component = max(
        components,
        key=len
    )

    nodes = list(largest_component)

    # Select two nodes for testing
    source = nodes[0]
    destination = nodes[-1]

    path, distance = shortest_path(
        graph,
        source,
        destination
    )

    print("\n========== DIJKSTRA RESULTS ==========")

    print("Source:", source)
    print("Destination:", destination)

    print("Total route nodes:", len(path))

    print("Total walking distance:",
          round(distance, 2), "meters")

    print("\nRoute:")

    for node in path:
        print(node)


if __name__ == "__main__":
    main()
