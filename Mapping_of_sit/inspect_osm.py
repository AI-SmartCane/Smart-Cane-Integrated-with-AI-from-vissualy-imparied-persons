# inspect_osm.py — prints a summary of what sit_campus.osm contains.
# Standard library only; no packages required.

import os
import sys
import xml.etree.ElementTree as ET
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")   # Kannada/Unicode names print safely

FILE = "sit_campus.osm"

if not os.path.exists(FILE):
    print(f"ERROR: {FILE} not found in {os.getcwd()}")
    sys.exit(1)

print(f"File: {FILE}  ({os.path.getsize(FILE) / 1024:.1f} KB)")

root = ET.parse(FILE).getroot()

bounds = root.find("bounds")
print("Bounds:", bounds.attrib if bounds is not None else "none")

nodes = root.findall("node")
ways = root.findall("way")
relations = root.findall("relation")
print(f"Nodes: {len(nodes)}   Ways: {len(ways)}   Relations: {len(relations)}")


def tags_of(element):
    return {t.get("k"): t.get("v") for t in element.findall("tag")}


building_types = Counter()
highway_types = Counter()
named_buildings = set()
named_highways = set()
other_areas = []

for way in ways:
    tags = tags_of(way)
    name = tags.get("name")
    if "building" in tags:
        building_types[tags["building"]] += 1
        if name:
            named_buildings.add(name)
    elif "highway" in tags:
        highway_types[tags["highway"]] += 1
        if name:
            named_highways.add(f"{name}  [{tags['highway']}]")
    elif name or "amenity" in tags or "landuse" in tags or "leisure" in tags:
        keys = {k: v for k, v in tags.items()
                if k in ("name", "amenity", "landuse", "leisure", "barrier")}
        other_areas.append(f"way {way.get('id')}: {keys}")

print(f"\nBUILDINGS by type: {dict(building_types)}")
print(f"Named buildings ({len(named_buildings)}):")
for n in sorted(named_buildings):
    print("  -", n)

print(f"\nROADS/PATHS by type: {dict(highway_types)}")
print(f"Named roads/paths ({len(named_highways)}):")
for n in sorted(named_highways):
    print("  -", n)

print(f"\nOTHER AREAS (campus boundary, grounds, etc.) ({len(other_areas)}):")
for a in other_areas:
    print("  -", a)

print(f"\nRELATIONS ({len(relations)}):")
for rel in relations:
    tags = tags_of(rel)
    print(f"  - relation {rel.get('id')}: type={tags.get('type')}  "
          f"name={tags.get('name')}  amenity={tags.get('amenity')}")

named_points = set()
for node in nodes:
    tags = tags_of(node)
    if "name" in tags:
        kind = (tags.get("amenity") or tags.get("shop") or tags.get("barrier")
                or tags.get("highway") or "point")
        named_points.add(f"{tags['name']}  [{kind}]")

print(f"\nNAMED POINTS ({len(named_points)}):")
for n in sorted(named_points):
    print("  -", n)