
import pickle
import sys
from pathlib import Path

import folium
import networkx as nx

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from navigation.destination import get_building_node

GRAPH_PATH = Path(__file__).parent / "campus_graph.pkl"
OUTPUT_PATH = Path(__file__).parent / "route_map.html"


def load_graph():
    with open(GRAPH_PATH, "rb") as file:
        return pickle.load(file)


def calculate_route(graph, source, destination):
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


def create_route_map(route, distance, destination_name):

    from pyproj import Transformer

    # Convert UTM coordinates to latitude/longitude
    transformer = Transformer.from_crs(
        "EPSG:32643",
        "EPSG:4326",
        always_xy=True
    )

    latlon_route = []

    for x, y in route:
        lon, lat = transformer.transform(x, y)
        latlon_route.append((lat, lon))

    start_lat, start_lon = latlon_route[0]
    end_lat, end_lon = latlon_route[-1]

    # Create map
    campus_map = folium.Map(
        location=[start_lat, start_lon],
        zoom_start=18,
        tiles=None
    )

    # Esri street map tiles
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}",
        attr="Tiles © Esri — Sources: Esri, HERE, Garmin, OpenStreetMap contributors",
        name="Esri World Street Map",
        overlay=False,
        control=True
    ).add_to(campus_map)

    # Starting marker
    folium.Marker(
        [start_lat, start_lon],
        popup="Starting Location",
        tooltip="Start",
        icon=folium.Icon(color="green", icon="play")
    ).add_to(campus_map)

    # Destination marker
    folium.Marker(
        [end_lat, end_lon],
        popup=destination_name,
        tooltip=destination_name,
        icon=folium.Icon(color="red", icon="flag")
    ).add_to(campus_map)

    # Dijkstra route
    folium.PolyLine(
        latlon_route,
        color="blue",
        weight=6,
        opacity=0.8,
        tooltip=f"Walking distance: {distance:.2f} m"
    ).add_to(campus_map)

    # Fit map to route
    campus_map.fit_bounds(latlon_route)

    # Save map
    campus_map.save(str(OUTPUT_PATH))

    print("\nRoute map created successfully!")
    print("Saved at:", OUTPUT_PATH)


def main():

    graph = load_graph()

    destination_name = input("Enter destination building: ")

    destination_node = get_building_node(
        graph,
        destination_name
    )

    if destination_node is None:
        print("Destination not found.")
        return

    # Temporary starting node
    largest_component = max(
        nx.connected_components(graph),
        key=len
    )

    source_node = next(iter(largest_component))

    # Calculate route
    route, distance = calculate_route(
        graph,
        source_node,
        destination_node
    )

    print("\nWalking distance:", round(distance, 2), "meters")

    create_route_map(
        route,
        distance,
        destination_name
    )


if __name__ == "__main__":
    main()
