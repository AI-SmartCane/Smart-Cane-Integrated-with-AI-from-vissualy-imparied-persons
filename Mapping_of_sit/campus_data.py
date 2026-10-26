# campus_data.py — reads sit_campus.osm, our own drawn*.geojson outlines and building_names.csv,
# and returns the campus features as GeoDataFrames. Other scripts import load_campus() from here.

import csv
import glob
import hashlib
import json
import os
import xml.etree.ElementTree as ET

import geopandas as gpd
import pandas as pd
from shapely.geometry import LineString, Polygon, shape

OSM_FILE = "sit_campus.osm"
NAMES_FILE = "building_names.csv"   # our own names for buildings AND areas (fills gaps in OSM)
DRAWN_FILES = "drawn*.geojson"      # outlines we drew ourselves on draw_map.html
CRS_LATLON = "EPSG:4326"            # GPS latitude/longitude (degrees)
CRS_METRES = "EPSG:32643"           # UTM zone 43N — metres, correct for Tumakuru


def _tags(element):
    return {t.get("k"): t.get("v") for t in element.findall("tag")}


def _read_osm(osm_file):
    """Parse the OSM XML into lists of campus / buildings / paths / areas."""
    root = ET.parse(osm_file).getroot()
    nodes = {n.get("id"): (float(n.get("lon")), float(n.get("lat")))
             for n in root.findall("node")}                      # (lon, lat) = (x, y)
    ways = {}
    for w in root.findall("way"):
        coords = [nodes[nd.get("ref")] for nd in w.findall("nd") if nd.get("ref") in nodes]
        if len(coords) >= 2:
            ways[w.get("id")] = (_tags(w), coords)

    campus, buildings, paths, areas = [], [], [], []

    def add_polygon(osm_id, tags, polygon):
        name = tags.get("name")
        if "building" in tags:
            buildings.append({"osm_id": osm_id, "name": name,
                              "type": tags["building"], "geometry": polygon})
        elif tags.get("amenity") == "university":
            campus.append({"osm_id": osm_id, "name": name, "geometry": polygon})
        elif name or "leisure" in tags or "amenity" in tags:
            kind = tags.get("leisure") or tags.get("amenity") or "area"
            areas.append({"osm_id": osm_id, "name": name, "type": kind, "geometry": polygon})

    for osm_id, (tags, coords) in ways.items():
        if "highway" in tags:
            paths.append({"osm_id": osm_id, "name": tags.get("name"),
                          "type": tags["highway"], "geometry": LineString(coords)})
        elif len(coords) >= 4 and coords[0] == coords[-1]:      # closed way = polygon
            add_polygon(osm_id, tags, Polygon(coords))

    for rel in root.findall("relation"):                        # multipolygon relations
        tags = _tags(rel)
        if tags.get("type") != "multipolygon":
            continue
        outer = [m.get("ref") for m in rel.findall("member") if m.get("role") == "outer"]
        inner = [m.get("ref") for m in rel.findall("member") if m.get("role") == "inner"]
        if len(outer) == 1 and outer[0] in ways:
            holes = [ways[i][1] for i in inner if i in ways]
            add_polygon("rel" + rel.get("id"), tags, Polygon(ways[outer[0]][1], holes))

    return campus, buildings, paths, areas


def _read_drawn():
    """Outlines drawn on draw_map.html. Each gets a stable id made from its shape."""
    rows, seen = [], set()
    for path in sorted(glob.glob(DRAWN_FILES)):
        with open(path, encoding="utf-8") as f:
            features = json.load(f).get("features", [])
        for feat in features:
            if not feat.get("geometry"):
                continue
            geom = shape(feat["geometry"]).buffer(0)          # buffer(0) repairs crossed edges
            if geom.is_empty or geom.geom_type not in ("Polygon", "MultiPolygon"):
                continue
            osm_id = "drawn-" + hashlib.md5(geom.wkt.encode()).hexdigest()[:6]
            if osm_id not in seen:
                seen.add(osm_id)
                rows.append({"osm_id": osm_id, "name": (feat.get("properties") or {}).get("name"),
                             "type": "drawn", "geometry": geom})
    return rows


def load_campus(osm_file=OSM_FILE, names_file=NAMES_FILE):
    campus, buildings, paths, areas = _read_osm(osm_file)

    def to_gdf(rows, columns):
        return gpd.GeoDataFrame(rows, columns=columns, geometry="geometry", crs=CRS_LATLON)

    campus = to_gdf(campus, ["osm_id", "name", "geometry"])
    buildings = to_gdf(buildings, ["osm_id", "name", "type", "geometry"])
    paths = to_gdf(paths, ["osm_id", "name", "type", "geometry"])
    areas = to_gdf(areas, ["osm_id", "name", "type", "geometry"])

    # our own outlines win over OSM where they overlap (e.g. splitting one footprint in two)
    drawn = to_gdf(_read_drawn(), ["osm_id", "name", "type", "geometry"])
    if len(drawn):
        cover = drawn.to_crs(CRS_METRES).geometry.union_all()
        metres = buildings.to_crs(CRS_METRES)
        hit = metres.intersects(cover)
        trimmed = metres.loc[hit].geometry.difference(cover).buffer(-1).buffer(1)  # drops slivers < 2 m
        buildings.loc[hit, "geometry"] = trimmed.to_crs(CRS_LATLON)
        buildings = buildings[~buildings.geometry.is_empty].copy()
        buildings = pd.concat([buildings, drawn], ignore_index=True)
        print(f"Using {len(drawn)} drawn outline(s); trimmed {int(hit.sum())} OSM footprint(s)")

    campus_geom = campus.geometry.iloc[0]
    for gdf in (buildings, paths, areas):
        gdf["on_campus"] = gdf.intersects(campus_geom)

    # keep OSM's names; number the unnamed on-campus features (#1.. buildings, A1.. areas)
    buildings["is_drawn"] = buildings["osm_id"].str.startswith("drawn")
    buildings = buildings.sort_values(["is_drawn", "osm_id"]).reset_index(drop=True)
    areas = areas.sort_values("osm_id").reset_index(drop=True)
    for gdf in (buildings, areas):
        gdf["osm_name"] = gdf["name"]
        gdf["area_m2"] = gdf.to_crs(CRS_METRES).area.round().astype(int)
        unnamed = gdf["on_campus"] & gdf["name"].isna()
        gdf["number"] = None
        gdf.loc[unnamed, "number"] = list(range(1, unnamed.sum() + 1))

    # apply our own names from the CSV to buildings and areas alike
    if os.path.exists(names_file):
        applied = 0
        with open(names_file, newline="", encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                new_name = (row.get("new_name") or "").strip()
                if not new_name:
                    continue
                for gdf in (buildings, areas):
                    hit = gdf["osm_id"] == row["osm_id"].strip()
                    gdf.loc[hit, "name"] = new_name
                    applied += int(hit.sum())
        print(f"Applied {applied} names from {names_file}")

    for gdf, prefix in ((buildings, "#"), (areas, "A")):
        gdf["label"] = gdf["name"]
        still = gdf["name"].isna() & gdf["number"].notna()
        gdf.loc[still, "label"] = prefix + gdf.loc[still, "number"].astype(int).astype(str)
    areas["label"] = areas["label"].fillna("(unnamed)")

    return {"campus": campus, "buildings": buildings, "paths": paths, "areas": areas}