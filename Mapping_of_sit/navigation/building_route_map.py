
import pickle
import sys
from pathlib import Path

import folium
import networkx as nx
from pyproj import Transformer

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from destination import get_building_node

GRAPH_PATH = Path(__file__).parent / "campus_graph.pkl"
OUTPUT_PATH = Path(__file__).parent / "building_route.html"


def main():

    # Load graph
    with open(GRAPH_PATH, "rb") as f:
        graph = pickle.load(f)

    # Input buildings
    source_name = input("Enter starting building: ").strip()
    source_node = get_building_node(graph, source_name)

    destination_name = input("Enter destination building: ").strip()
    destination_node = get_building_node(graph, destination_name)

    # Dijkstra shortest path
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

    print("\nShortest distance:", round(distance, 2), "meters")
    print("Route nodes:", len(route))

    # Convert UTM to latitude/longitude
    transformer = Transformer.from_crs(
        "EPSG:32643",
        "EPSG:4326",
        always_xy=True
    )

    route_latlon = []

    for x, y in route:
        lon, lat = transformer.transform(x, y)
        route_latlon.append((lat, lon))

    start_lat, start_lon = route_latlon[0]
    end_lat, end_lon = route_latlon[-1]

    # Create map
    campus_map = folium.Map(
        location=route_latlon[0],
        zoom_start=18,
        tiles=None
    )

    # Esri tiles
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}",
        attr="Tiles © Esri",
        name="Esri Street Map",
        overlay=False
    ).add_to(campus_map)

    # Starting building
    folium.Marker(
        [start_lat, start_lon],
        popup=f"Start: {source_name}",
        tooltip=source_name,
        icon=folium.Icon(color="green", icon="play")
    ).add_to(campus_map)

    # Destination building
    folium.Marker(
        [end_lat, end_lon],
        popup=f"Destination: {destination_name}",
        tooltip=destination_name,
        icon=folium.Icon(color="red", icon="flag")
    ).add_to(campus_map)

    # Dijkstra path
    folium.PolyLine(
        route_latlon,
        color="blue",
        weight=6,
        opacity=0.9,
        tooltip=f"Dijkstra route: {distance:.2f} m"
    ).add_to(campus_map)

    # Display route nodes
    for i, point in enumerate(route_latlon, 1):
        folium.CircleMarker(
            location=point,
            radius=3,
            color="blue",
            tooltip=f"Node {i}"
        ).add_to(campus_map)

    campus_map.fit_bounds(route_latlon)

    # Save HTML
    campus_map.save(str(OUTPUT_PATH))

    print("\nMap saved:", OUTPUT_PATH)


if __name__ == "__main__":
    main()
