# build_map.py — draws the interactive SIT campus map.
#   python build_map.py        -> sit_map.html, and keeps building_names.csv up to date
#   python build_map.py draw   -> draw_map.html, with tools to draw missing building outlines
#   locator.py imports make_map() from here to mark a position on the same map.

import csv
import os
import sys

import folium
import pandas as pd
from folium.plugins import Draw
from campus_data import CRS_METRES, NAMES_FILE, load_campus

SATELLITE = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
NAMED_STYLE = "font:bold 11px sans-serif;color:#001a66;text-shadow:0 0 3px #fff;white-space:nowrap"
NUMBER_STYLE = "font:bold 11px sans-serif;color:#fff;background:#d9480f;border-radius:8px;padding:1px 4px"
AREA_STYLE = "font:bold 11px sans-serif;color:#0b5e2a;text-shadow:0 0 3px #fff;white-space:nowrap"
AREA_NUMBER_STYLE = "font:bold 11px sans-serif;color:#fff;background:#1b7f3b;border-radius:8px;padding:1px 4px"
FIELDS = ["label", "osm_id", "area_m2", "lat", "lon", "osm_name", "new_name"]


def _label(m, feature, style):
    c = feature.geometry.centroid
    folium.Marker([c.y, c.x], icon=folium.DivIcon(
        html=f'<div style="{style};display:inline-block">{feature["label"]}</div>')).add_to(m)


def make_map(data, output="sit_map.html", marker=None, draw=False):
    """Draw the campus map to `output`. marker={"lat","lon","text","radius"} marks a position;
    draw=True adds drawing tools and an Export button instead of the click-for-lat/lon popup."""
    campus = data["campus"]
    campus_geom = campus.geometry.iloc[0]
    buildings = data["buildings"][data["buildings"]["on_campus"]]
    paths = data["paths"][data["paths"]["on_campus"]]
    areas = data["areas"][data["areas"]["on_campus"]]

    if marker:
        centre, zoom = [marker["lat"], marker["lon"]], 18
    else:
        centre, zoom = [campus_geom.centroid.y, campus_geom.centroid.x], 17
    m = folium.Map(location=centre, zoom_start=zoom, max_zoom=20, tiles=None)
    folium.TileLayer("OpenStreetMap", name="Street map", max_native_zoom=19, max_zoom=20).add_to(m)
    folium.TileLayer(tiles=SATELLITE, attr="Esri World Imagery", name="Satellite",
                     max_native_zoom=19, max_zoom=20).add_to(m)

    folium.GeoJson(campus, name="Campus boundary",
                   style_function=lambda f: {"color": "red", "weight": 3, "fill": False}).add_to(m)
    folium.GeoJson(areas, name="Grounds / parking",
                   style_function=lambda f: {"color": "green", "weight": 1, "fillOpacity": 0.2},
                   tooltip=folium.GeoJsonTooltip(fields=["label", "type", "area_m2", "osm_id"])).add_to(m)
    folium.GeoJson(paths, name="Walkable paths",
                   style_function=lambda f: {"color": "orange", "weight": 3},
                   tooltip=folium.GeoJsonTooltip(fields=["type", "osm_id"])).add_to(m)
    folium.GeoJson(buildings, name="Buildings",
                   style_function=lambda f: {"color": "blue" if f["properties"]["name"] else "gray",
                                             "weight": 1, "fillOpacity": 0.5},
                   tooltip=folium.GeoJsonTooltip(fields=["label", "type", "area_m2", "osm_id"])).add_to(m)

    for _, b in buildings.iterrows():                           # text label or number on every feature
        _label(m, b, NUMBER_STYLE if pd.isna(b["name"]) else NAMED_STYLE)
    for _, a in areas.iterrows():
        _label(m, a, AREA_NUMBER_STYLE if pd.isna(a["name"]) else AREA_STYLE)

    if marker:                                                  # the position being described
        folium.Circle([marker["lat"], marker["lon"]], radius=marker.get("radius", 8),
                      color="red", fill=True, fill_opacity=0.2).add_to(m)
        folium.Marker([marker["lat"], marker["lon"]], icon=folium.Icon(color="red"),
                      popup=folium.Popup(marker["text"], max_width=300, show=True)).add_to(m)

    if draw:                                                    # drawing tools + Export button
        Draw(export=True, filename="drawn_buildings.geojson",
             draw_options={"polyline": False, "circle": False,
                           "circlemarker": False, "marker": False}).add_to(m)
    else:
        folium.LatLngPopup().add_to(m)                          # click anywhere to see lat/lon
    folium.LayerControl().add_to(m)
    m.save(output)
    return m


def update_names_file(buildings, areas, path=NAMES_FILE):
    """Create building_names.csv, or add rows for features not listed yet. Returns rows added."""
    existing = []
    if os.path.exists(path):
        with open(path, newline="", encoding="utf-8-sig") as f:
            existing = list(csv.DictReader(f))
    known = {row.get("osm_id") for row in existing}
    new_rows = []
    for gdf, kind in ((buildings, "building"), (areas, "area")):
        for _, b in gdf.iterrows():
            if b["osm_id"] in known:
                continue
            c = b.geometry.centroid
            label = b["label"] if kind == "building" else f"{b['label']} ({b['type']})"
            new_rows.append({"label": label, "osm_id": b["osm_id"], "area_m2": b["area_m2"],
                             "lat": f"{c.y:.5f}", "lon": f"{c.x:.5f}",
                             "osm_name": "" if pd.isna(b["osm_name"]) else b["osm_name"], "new_name": ""})
    if new_rows:
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore", restval="")
            writer.writeheader()
            writer.writerows(existing + new_rows)
    return len(new_rows)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    draw = "draw" in sys.argv[1:]
    data = load_campus()
    buildings = data["buildings"][data["buildings"]["on_campus"]]
    areas = data["areas"][data["areas"]["on_campus"]]
    added = update_names_file(buildings, areas)
    if added:
        print(f"Added {added} row(s) to {NAMES_FILE} — type their names in the last column.")
    unnamed = buildings["name"].isna()
    hectares = data["campus"].to_crs(CRS_METRES).area.iloc[0] / 10_000
    print(f"Campus area: {hectares:.1f} ha.  On campus: {len(buildings)} buildings "
          f"({(~unnamed).sum()} named, {unnamed.sum()} still numbered), "
          f"{data['paths']['on_campus'].sum()} walkable paths, {len(areas)} areas "
          f"({areas['name'].isna().sum()} unnamed)")
    output = "draw_map.html" if draw else "sit_map.html"
    make_map(data, output, draw=draw)
    print(f"Saved {output}")