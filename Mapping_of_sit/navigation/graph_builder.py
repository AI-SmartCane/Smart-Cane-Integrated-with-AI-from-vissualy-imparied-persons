
# navigation/graph_builder.py

import sys
import os
import pickle
import math

import networkx as nx

# Allow importing campus_data.py from parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from campus_data import load_campus, CRS_METRES


def coordinate_key(x, y):
    """Create a stable key for a walking-path coordinate."""
    return round(x, 3), round(y, 3)


def build_graph():

    print("Loading SIT campus data...")

    data = load_campus()

    # Extract campus walking paths
    paths = data["paths"]
    paths = paths[paths["on_campus"]]

    # Convert paths into metre-based coordinates
    paths = paths.to_crs(CRS_METRES)

    graph = nx.Graph()

    print("Building walking graph...")

    for _, row in paths.iterrows():

        geometry = row.geometry

        coordinates = list(geometry.coords)

        # Process consecutive coordinates
        for i in range(len(coordinates) - 1):

            x1, y1 = coordinates[i]
            x2, y2 = coordinates[i + 1]

            node1 = coordinate_key(x1, y1)
            node2 = coordinate_key(x2, y2)

            distance = math.sqrt(
                (x2 - x1) ** 2 +
                (y2 - y1) ** 2
            )

            if distance == 0:
                continue

            # Store node coordinates
            graph.add_node(
                node1,
                x=x1,
                y=y1
            )

            graph.add_node(
                node2,
                x=x2,
                y=y2
            )

            # Add weighted walking edge
            graph.add_edge(
                node1,
                node2,
                weight=distance
            )

    print("\nGraph created successfully!")

    print("Total nodes:", graph.number_of_nodes())
    print("Total edges:", graph.number_of_edges())

    # Connectivity analysis
    components = list(nx.connected_components(graph))

    print("Connected components:", len(components))

    if components:
        largest = max(components, key=len)
        print("Largest component nodes:", len(largest))

    # Save graph
    output_file = os.path.join(
        os.path.dirname(__file__),
        "campus_graph.pkl"
    )

    with open(output_file, "wb") as f:
        pickle.dump(graph, f)

    print("\nGraph saved at:")
    print(output_file)

    return graph


if __name__ == "__main__":
    build_graph()
