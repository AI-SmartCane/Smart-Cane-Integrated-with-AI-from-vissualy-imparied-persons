# locator.py — turns a latitude/longitude into a campus location description.
#   from locator import locate          -> locate(lat, lon) returns a dict   (for the stick later)
#   python locator.py 13.32592 77.12459 -> prints the description, draws location_map.html
#   python locator.py                   -> asks for coordinates repeatedly

import math
import sys

import geopandas as gpd
from shapely.geometry import Point
from shapely.ops import nearest_points

from build_map import make_map
from campus_data import CRS_LATLON, CRS_METRES, load_campus

GPS_ERROR_M = 8     # typical GPS uncertainty; within this distance of a building = "beside"
NEAR_M = 40         # named buildings within this distance are reported as nearby
ON_PATH_M = 6       # within this distance of a path centreline = "on" it

AREA_WORDS = {"pitch": "on the sports ground", "stadium": "in the stadium",
              "park": "in the park", "parking": "in a parking area"}
COMPASS = ["north", "north-east", "east", "south-east", "south", "south-west", "west", "north-west"]

# load once and project everything to metres, so distances are real distances
_data = load_campus()
_campus = _data["campus"].to_crs(CRS_METRES).geometry.iloc[0]
_buildings = _data["buildings"].to_crs(CRS_METRES)
_paths = _data["paths"].to_crs(CRS_METRES)
_areas = _data["areas"].to_crs(CRS_METRES)


def _to_metres(lat, lon):
    return gpd.GeoSeries([Point(lon, lat)], crs=CRS_LATLON).to_crs(CRS_METRES).iloc[0]


def _direction(frm, to):
    """Compass direction from point frm to point to (both in metres)."""
    angle = math.degrees(math.atan2(to.x - frm.x, to.y - frm.y)) % 360    # 0 = north, 90 = east
    return COMPASS[int((angle + 22.5) // 45) % 8]


def locate(lat, lon):
    """Return a dict describing where (lat, lon) is on the SIT campus."""
    p = _to_metres(lat, lon)
    result = {"lat": lat, "lon": lon, "inside_campus": bool(_campus.contains(p)),
              "boundary_m": round(_campus.exterior.distance(p)),
              "building": None, "status": None, "path": None, "area": None, "nearby": []}

    if not result["inside_campus"]:
        far = result["boundary_m"] > GPS_ERROR_M
        result["description"] = "You are outside SIT campus" + (
            f", about {result['boundary_m']} metres from the boundary." if far else ", right at the boundary.")
        return result

    # 1. a building we are inside, or beside (within GPS error)
    dist = _buildings.distance(p)
    i = dist.idxmin()
    if dist[i] <= GPS_ERROR_M:
        name = _buildings.loc[i, "name"]
        result["building"] = name if isinstance(name, str) else "an unnamed building"
        result["status"] = "inside" if dist[i] == 0 else "beside"

    # 2. a walkable path — every road and footway inside the campus counts as a footpath
    pdist = _paths.distance(p)
    j = pdist.idxmin()
    if pdist[j] <= ON_PATH_M:
        result["path"] = "footpath"
        result["path_osm_type"] = _paths.loc[j, "type"]

    # 3. a ground, park or parking area (the smallest one containing the point)
    inside_areas = _areas[_areas.contains(p)]
    if len(inside_areas):
        a = inside_areas.loc[inside_areas.area.idxmin()]
        result["area"] = (f"at the {a['name']}" if isinstance(a["name"], str)
                          else AREA_WORDS.get(a["type"], "in an open area"))

    # 4. nearby named buildings, nearest first, one entry per name, never the one we are at
    named = _buildings[_buildings["name"].notna()].copy()
    named["dist"] = named.distance(p)
    named = named[(named["dist"] <= NEAR_M) & (named["name"] != result["building"])]
    for _, row in named.sort_values("dist").drop_duplicates("name").head(3).iterrows():
        target = nearest_points(p, row.geometry)[1]
        result["nearby"].append({"name": row["name"], "distance_m": round(row["dist"]),
                                 "direction": _direction(p, target)})

    # 5. put it into words (written to be spoken aloud, so "metres" rather than "m")
    if result["status"]:
        the = "" if result["building"] == "an unnamed building" else "the "
        first = f"You are {'at' if result['status'] == 'inside' else 'beside'} {the}{result['building']}"
    else:
        first = "You are inside SIT campus"
    if result["path"] and result["status"] != "inside":
        first += f", on a {result['path']}"
    if result["area"]:
        first += f", {result['area']}"
    sentences = [first + "."]
    if result["nearby"]:
        bits = [f"{'The' if k == 0 else 'the'} {n['name']} is {n['distance_m']} metres to the {n['direction']}"
                for k, n in enumerate(result["nearby"])]
        sentences.append("; ".join(bits) + ".")
    elif not result["status"]:
        sentences.append(f"No named building is within {NEAR_M} metres.")
    if result["boundary_m"] <= 2 * GPS_ERROR_M:
        sentences.append(f"The campus boundary is {result['boundary_m']} metres away.")
    result["description"] = " ".join(sentences)
    return result


def report(lat, lon):
    r = locate(lat, lon)
    print(r["description"])
    print("  details:", {k: v for k, v in r.items() if k not in ("description", "lat", "lon")})
    make_map(_data, "location_map.html",
             marker={"lat": lat, "lon": lon, "text": r["description"], "radius": GPS_ERROR_M})
    print("  marked on location_map.html")


def main(args):
    sys.stdout.reconfigure(encoding="utf-8")
    if len(args) == 2:
        report(float(args[0]), float(args[1]))
        return
    while True:
        text = input("\nEnter latitude, longitude (blank to quit): ").strip()
        if not text:
            break
        try:
            lat, lon = (float(x) for x in text.replace(",", " ").split())
        except ValueError:
            print("Please type two numbers, e.g. 13.32592 77.12459")
            continue
        report(lat, lon)


if __name__ == "__main__":
    main(sys.argv[1:])