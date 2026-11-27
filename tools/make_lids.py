#!/usr/bin/env python3
"""Make the eyelid overlays for the blinking/winking pug logo: images/lid-*.png.
Each overlay is the size of images/logo.png and is see-through except over the eyes it closes.
The pages stack them on the logo and switch them on and off with CSS (see BLINK_CSS in build.py).
Run: python3 tools/make_lids.py"""
import os
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logo = Image.open(os.path.join(ROOT, "images", "logo.png")).convert("RGBA")
SS = 4                                                    # draw 4x larger, then shrink, for smooth lines
SKIN = logo.getpixel((250, 120))[:3] + (255,)
INK = (12, 12, 12, 255)
EYES = {"left": (186, 140, 29, 35), "right": (359, 132, 29, 33), "third": (273, 66, 37, 26)}   # centre x, y, radius x, y

def lid(eyes, state):
    big = logo.resize((logo.width * SS, logo.height * SS), Image.LANCZOS)
    d = ImageDraw.Draw(big)
    mask = Image.new("L", logo.size, 0); md = ImageDraw.Draw(mask)
    for name in eyes:
        cx, cy, rx, ry = EYES[name]
        md.ellipse([cx - rx - 4, cy - ry - 4, cx + rx + 4, cy + ry + 4], fill=255)
        cx, cy, rx, ry = (v * SS for v in EYES[name])
        box, w = [cx - rx, cy - ry, cx + rx, cy + ry], 4 * SS
        if state == "closed":
            d.ellipse(box, fill=SKIN)
            d.arc([cx - rx * .95, cy - ry * .55, cx + rx * .95, cy + ry * .45], 15, 165, fill=INK, width=w)
        else:                                             # half shut: the lid covers the top half
            d.chord(box, 180, 360, fill=SKIN)
            d.line([cx - rx * .98, cy, cx + rx * .98, cy], fill=INK, width=w)
    out = big.resize(logo.size, Image.LANCZOS)
    mask = mask.filter(ImageFilter.GaussianBlur(1))
    out.putalpha(Image.composite(out.getchannel("A"), Image.new("L", logo.size, 0), mask))
    clear = Image.new("RGBA", logo.size, (0, 0, 0, 0))     # blank the hidden pixels so the file stays small
    return Image.composite(out, clear, out.getchannel("A").point(lambda a: 255 if a else 0))

for key, eyes in {"main": ("left", "right"), "third": ("third",), "wink": ("right",)}.items():
    for state in ("half", "closed"):
        path = os.path.join(ROOT, "images", f"lid-{key}-{state}.png")
        lid(eyes, state).save(path, optimize=True)
        print("wrote", os.path.relpath(path, ROOT), os.path.getsize(path), "bytes")
