# Trippy Pug gallery (lightweight)
- `index.html`: plain HTML/CSS, no JavaScript. One `<figure>` per painting: thumbnail (`images/pNN.jpg`) linking to full size (`images/full/pNN.jpg`), museum-style caption, grey "i want to buy it" circle (mailto link).
- To add a painting: copy a `<figure>`, add a 760 px thumbnail and an 1800 px full image, fill in title, year, medium, size, alt text.
- Hosted free with GitHub Pages; pushing to `main` republishes in about a minute.
- The 3D walk-through version is a separate Claude artifact, not in this repo.

## How the site is built
- `paintings.json` is the single list of paintings (title, year, medium, size, price, screen-reader description).
- `index.html` (3D gallery) and `simple.html` are GENERATED from it by `python3 tools/build.py` using `tools/*.template.html`. Do not edit those two files by hand; edit the json or the templates, then rebuild.
- Add a painting in one step (needs `pip install pillow`):
  `python3 tools/add_painting.py photo.jpg --title "Name" --year 2025 --size '30" × 24"' --alt "plain description" [--medium "..."] [--price '$1,200 USD']`
  It resizes the photo (760 px thumb + 1800 px full), updates paintings.json, rebuilds both pages. Then commit and push.
- Edit a label or price: change it in `paintings.json`, run `python3 tools/build.py`, commit, push.
- 3D page: tap/click the floor to walk (RuneScape-style yellow X), drag to look, tap a painting to approach it, walk to the black door for the next room (12 paintings per room). `simple.html` is the no-JavaScript version.
- Hosted free by GitHub Pages at gallery.trippypug.com; pushing to `main` republishes in about a minute. Only the repo owner can push.
