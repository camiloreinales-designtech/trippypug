---
name: trippypug
description: Work on the Trippy Pug 3D gallery site (gallery.trippypug.com). Use for adding or editing paintings, changing labels or prices, tweaking the gallery, and publishing. Starts cheap in a fresh session by reading only what is needed.
---

# Trippy Pug gallery: fresh-session workflow

Keep token use low: do not re-explain the project, do not read big files whole.

## 1. Orient (cheap)
- Read `NOTES.md` only. It says how the site is built.
- Do NOT open `index.html` or `simple.html` (generated, huge, base64). Never edit them by hand.

## 2. Where things live
- `paintings.json`: the 11+ paintings (id, title, year, medium, dimensions, price, alt, w, h).
- `images/`: thumbnails; `images/full/`: large versions; lettering PNGs (`hint.png`, `gy_on.png`, `gy_off.png`).
- `tools/gallery.template.html`: the 3D gallery source (HTML, CSS, JS). `tools/simple.template.html`: lightweight page.
- `tools/build.py`: regenerates `index.html` and `simple.html` from templates + `paintings.json`.
- `tools/add_painting.py <photo>`: resizes a photo, appends to `paintings.json`, rebuilds.
- `CNAME`: `gallery.trippypug.com`. Do not change it.

## 3. Common jobs
- Add painting: `python3 tools/add_painting.py <photo> --title ... --year ... --size "36\" × 28\"" --alt "..." [--medium ...] [--price ...]`.
- Payment link / sold: set `"pay": "https://..."` or `"sold": true` on the painting in `paintings.json`, then rebuild (see NOTES.md).
- Edit label/price: edit `paintings.json`, then `python3 tools/build.py`.
- Gallery behaviour or look: edit `tools/gallery.template.html` with targeted greps and small edits, then rebuild.
- Always rebuild after any change; confirm `index.html` changed.

## 4. Check, then publish
- Quick test: serve the folder (`python3 -m http.server 8124`) and load a phone-size page with Playwright; confirm no page errors.
- Commit with a short message and push to `main` (GitHub Pages deploys in about a minute). Do not create PRs.
- The Claude artifact (private copy) is optional and only republished when asked.

## 5. Rules
- Only the owner edits content. Never put personal details (real name, personal email) in commits or files. Buy email is `trippypuginfo@gmail.com`; Instagram is `@trippypug`.
- Be honest about what was not tested (real phones, live domain).
- Batch several requested changes into one build and one commit.
- Keep replies short; report what changed and what is untested.
