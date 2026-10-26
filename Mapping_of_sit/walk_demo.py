# walk_demo.py — simulates the stick walking along the campus footpaths, with no hardware.
# Reads waypoints from walk.csv (lat,lon per line), routes between them along the mapped paths,
# walks STEP_M per second, adds GPS-like noise, averages the last few readings, calls locate()
# and speaks when the place changes. Draws the walk on walk_map.html.
#   python walk_demo.py          -> with voice, one reading per second
#   python walk_demo.py quiet    -> text only, no delays

import csv
import math
import random
import sys
import time

import folium
import geopandas as gpd
import networkx as nx
from shapely.geometry import LineString, Point

from build_map import make_map
from campus_data import CRS_LATLON, CRS_METRES, load_campus
from locator import locate

STEP_M = 5          # metres walked per reading (one reading per second)
NOISE_M = 4         # simulated GPS error, metres (standard deviation)
AVERAGE_N = 3       # readings averaged before locating (smooths the noise)
MIN_GAP_S = 8       # seconds between announcements, unless a building is reached

data = load_campus()
paths_m = data["paths"][data["paths"]["on_campus"]].to_crs(CRS_METRES)


def to_metres(latlons):
    pts = gpd.GeoSeries([Point(lon, lat) for lat, lon in latlons], crs=CRS_LATLON).to_crs(CRS_METRES)
    return [(p.x, p.y) for p in pts]


def to_latlon(points_m):
    pts = gpd.GeoSeries([Point(x, y) for x, y in points_m], crs=CRS_METRES).to_crs(CRS_LATLON)
    return [(p.y, p.x) for p in pts]


def path_graph():
    """Graph of the mapped paths: nodes are path vertices (metres), edges carry their length."""
    G = nx.Graph()
    for geom in paths_m.geometry:
        lines = geom.geoms if geom.geom_type == "MultiLineString" else [geom]
        for line in lines:
            coords = [(round(x, 1), round(y, 1)) for x, y in line.coords]
            for a, b in zip(coords, coords[1:]):
                G.add_edge(a, b, length=math.dist(a, b))
    return G


def route_along_paths(waypoints_m, G):
    """Waypoint -> nearest path node -> shortest way along the paths -> ... -> last waypoint."""
    def nearest(p):
        return min(G.nodes, key=lambda n: math.dist(n, p))
    route = [waypoints_m[0]]
    for a, b in zip(waypoints_m, waypoints_m[1:]):
        na, nb = nearest(a), nearest(b)
        try:
            route += nx.shortest_path(G, na, nb, weight="length")
        except nx.NetworkXNoPath:
            print("  no mapped path between two waypoints — walking straight instead")
            route += [na, nb]
    route.append(waypoints_m[-1])
    line = LineString(route)
    steps = list(range(0, int(line.length), STEP_M)) + [line.length]
    return [(p.x, p.y) for p in (line.interpolate(d) for d in steps)], line.length


def noisy(lat, lon):
    """What a GPS module would report for a true position."""
    return (lat + random.gauss(0, NOISE_M) / 111_000,
            lon + random.gauss(0, NOISE_M) / (111_000 * math.cos(math.radians(lat))))


def place_key(r):
    """What must change before we speak again: the place itself and the nearest landmark."""
    nearest = r["nearby"][0]["name"] if r["nearby"] else None
    return (r["inside_campus"], r["status"], r["building"], r["path"], r["area"], nearest)


def main(quiet):
    sys.stdout.reconfigure(encoding="utf-8")
    if not quiet:
        from speak import say
    with open("walk.csv", newline="", encoding="utf-8-sig") as f:
        waypoints = [(float(r["lat"]), float(r["lon"])) for r in csv.DictReader(f)]

    points_m, length = route_along_paths(to_metres(waypoints), path_graph())
    points = to_latlon(points_m)
    print(f"Route: {length:.0f} m along the mapped paths, {len(points)} readings\n")

    recent, last_key, last_here, last_time = [], None, None, -999
    announcements, lookup_ms = [], []
    for second, (lat, lon) in enumerate(points):
        glat, glon = noisy(lat, lon)
        recent = (recent + [(glat, glon)])[-AVERAGE_N:]
        alat = sum(p[0] for p in recent) / len(recent)      # smoothed position
        alon = sum(p[1] for p in recent) / len(recent)

        t0 = time.perf_counter()
        r = locate(alat, alon)
        lookup_ms.append((time.perf_counter() - t0) * 1000)

        key = place_key(r)
        here = r["building"] if r["status"] else None        # building we are at / beside
        reached = here is not None and here != last_here
        speak_now = key != last_key and (reached or second - last_time >= MIN_GAP_S)
        print(f"[{second:3d}s] {glat:.5f}, {glon:.5f}  lookup {lookup_ms[-1]:3.0f} ms  "
              f"{'ANNOUNCE' if speak_now else ''}")
        if speak_now:
            announcements.append((alat, alon, r["description"]))
            if quiet:
                print("       " + r["description"])
            else:
                say(r["description"])
            last_key, last_here, last_time = key, here, second
        if not quiet:
            time.sleep(1)

    print(f"\n{len(points)} readings, {len(announcements)} announcements, "
          f"average lookup {sum(lookup_ms) / len(lookup_ms):.0f} ms")

    m = make_map(data, "walk_map.html")
    folium.PolyLine(points, color="red", weight=3, tooltip="simulated walk").add_to(m)
    for lat, lon, text in announcements:
        folium.CircleMarker([lat, lon], radius=6, color="red", fill=True,
                            popup=folium.Popup(text, max_width=250)).add_to(m)
    m.save("walk_map.html")
    print("Saved walk_map.html")


if __name__ == "__main__":
    main(quiet="quiet" in sys.argv[1:])