# Trippy Pug gallery (lightweight)
- `index.html`: plain HTML/CSS, no JavaScript. One `<figure>` per painting: thumbnail (`images/pNN.jpg`) linking to full size (`images/full/pNN.jpg`), museum-style caption, grey "i want to buy it" circle (mailto link).
- To add a painting: copy a `<figure>`, add a 760 px thumbnail and an 1800 px full image, fill in title, year, medium, size, alt text.
- Hosted free with GitHub Pages; pushing to `main` republishes in about a minute.
- The 3D walk-through version is a separate Claude artifact, not in this repo.

## Update
- `index.html` is now the 3D walk-through gallery (works on phones). Tap/click the floor to walk there (old-school RuneScape style, yellow X marker), drag to look, tap a painting to approach it, walk to the black door for the next room.
- `simple.html` is the lightweight no-JavaScript version (linked as "simple view").
- Painting data for the 3D page is the `window.claude` stub near the top of `index.html`; add a painting by adding an object there plus its image in `images/full/`.
