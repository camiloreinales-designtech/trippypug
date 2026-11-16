#!/usr/bin/env python3
"""Add one painting: resizes the photo, appends it to paintings.json, rebuilds the pages.

  python3 tools/add_painting.py photo.jpg --title "Name" --year 2025 --size '30" × 24"' \\
      --alt "One or two plain sentences describing the painting" [--medium "Acrylic on canvas"] [--price '$1,200 USD']

Needs Pillow (pip install pillow). Afterwards: git add -A && git commit && git push.
"""
import argparse, json, os, subprocess, sys
from PIL import Image, ImageOps
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser()
ap.add_argument("photo"); ap.add_argument("--title", required=True); ap.add_argument("--year", required=True)
ap.add_argument("--size", required=True, help='e.g. 36" × 28"  (long side first is fine)')
ap.add_argument("--alt", required=True, help="plain-language description for screen readers")
ap.add_argument("--medium", default="Acrylic on canvas"); ap.add_argument("--price", default="")
a = ap.parse_args()
path = os.path.join(ROOT, "paintings.json")
P = json.load(open(path, encoding="utf-8"))
if any(p["title"].lower() == a.title.lower() for p in P): sys.exit(f'"{a.title}" is already in paintings.json')
nid = "p%02d" % (max(int(p["id"][1:]) for p in P) + 1)
im = ImageOps.exif_transpose(Image.open(a.photo)).convert("RGB")
def save(max_side, out, q):
    c = im.copy(); c.thumbnail((max_side, max_side), Image.LANCZOS)
    os.makedirs(os.path.dirname(out), exist_ok=True); c.save(out, "JPEG", quality=q, optimize=True, progressive=True); return c.size
w, h = save(760, os.path.join(ROOT, "images", nid + ".jpg"), 82)
save(1800, os.path.join(ROOT, "images", "full", nid + ".jpg"), 85)
P.append(dict(id=nid, title=a.title, year=str(a.year), medium=a.medium, dimensions=a.size, price=a.price, alt=a.alt, w=w, h=h))
json.dump(P, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
subprocess.check_call([sys.executable, os.path.join(ROOT, "tools", "build.py")])
print("added", nid, "-", a.title)
