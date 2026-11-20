# download_osm.py — downloads a fresh sit_campus.osm covering the WHOLE campus polygon
# plus a margin, replacing the small export. The old file is kept as sit_campus_old.osm.

import os
import shutil
import sys
import urllib.request

from campus_data import load_campus

sys.stdout.reconfigure(encoding="utf-8")

MARGIN = 0.0015      # degrees, roughly 160 m around the campus outline

campus = load_campus()["campus"]                       # reads the CURRENT file first
minx, miny, maxx, maxy = campus.geometry.iloc[0].bounds   # lon/lat extent of the red outline
print(f"Campus outline extent: lat {miny:.6f} to {maxy:.6f}, lon {minx:.6f} to {maxx:.6f}")

bbox = f"{minx - MARGIN:.6f},{miny - MARGIN:.6f},{maxx + MARGIN:.6f},{maxy + MARGIN:.6f}"
url = "https://api.openstreetmap.org/api/0.6/map?bbox=" + bbox
print("Downloading:", url)

request = urllib.request.Request(
    url, headers={"User-Agent": "SIT-SmartBlindStick-campus-map/0.1 (student project)"})
with urllib.request.urlopen(request, timeout=120) as response:
    data = response.read()

if os.path.exists("sit_campus.osm") and not os.path.exists("sit_campus_old.osm"):
    shutil.copy("sit_campus.osm", "sit_campus_old.osm")
    print("Old file backed up as sit_campus_old.osm")

with open("sit_campus.osm", "wb") as f:
    f.write(data)
print(f"Saved new sit_campus.osm ({len(data) / 1024:.1f} KB)")