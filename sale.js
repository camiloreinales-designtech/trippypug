/* 50% OFF sale, Thanksgiving to Cyber Monday (Thu Nov 26 - Mon Nov 30, 2026).
   - Intro: an 8-bit skeleton turkey dancing over the sale text, once per visit
     (closes on tap, click, any key, or after a few seconds).
   - A "50% OFF" sign on every "i want to buy it" spot: main gallery, vortex and painting list.
   Everything switches off by itself after Cyber Monday (midnight, New York time).
   Turn it off early with SALE in tools/build.py, then rebuild. */
(() => {
  const END = Date.UTC(2026, 11, 1, 5, 0, 0);   // Tue Dec 1, 2026 00:00 in New York = end of Cyber Monday
  if (Date.now() >= END) return;
  const KEY = "tpSaleSeen";
  let seen = false;
  try { seen = !!sessionStorage.getItem(KEY); sessionStorage.setItem(KEY, "1"); } catch (e) {}
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;

  const font = document.createElement("link");
  font.rel = "stylesheet"; font.href = "https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap";
  document.head.appendChild(font);
  const style = document.createElement("style");
  style.textContent = `
.tp-sale { --ol: -2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 2px 2px 0 #000, 0 -2px 0 #000, 0 2px 0 #000, -2px 0 0 #000, 2px 0 0 #000;
  position: fixed; inset: 0; z-index: 1000; background: transparent; color: #fff; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 14px;
  padding: max(16px, env(safe-area-inset-top, 0px)) max(16px, env(safe-area-inset-right, 0px)) max(16px, env(safe-area-inset-bottom, 0px)) max(16px, env(safe-area-inset-left, 0px));
  font-family: "Press Start 2P", "Courier New", monospace; text-align: center; cursor: pointer; animation: tpSaleIn .3s ease both; }
.tp-sale.out { opacity: 0; transition: opacity .35s ease; }
.tp-sale canvas { width: min(72vw, 50vh, 360px); height: auto; aspect-ratio: 1; image-rendering: pixelated; image-rendering: crisp-edges; }
.tp-sale p { margin: 0; line-height: 1.3; }
.tp-sale .big { font-size: clamp(30px, 9vw, 64px); color: #f7d046; letter-spacing: .02em;
  text-shadow: -3px -3px 0 #000, 3px -3px 0 #000, -3px 3px 0 #000, 3px 3px 0 #000, 0 -3px 0 #000, 0 3px 0 #000, -3px 0 0 #000, 3px 0 0 #000, 7px 7px 0 #e2412f; }
.tp-sale .small { font-size: clamp(14px, 4vw, 26px); color: #fff; text-shadow: var(--ol); }
.tp-sale .go { font-size: clamp(9px, 2.4vw, 12px); color: #fff; text-shadow: var(--ol); margin-top: 10px; animation: tpSaleBlink 1s steps(1, end) infinite; }
.tp-sale .x { position: absolute; top: max(12px, env(safe-area-inset-top, 0px)); right: max(12px, env(safe-area-inset-right, 0px)); width: 44px; height: 44px; border: 0; background: none; color: #fff; text-shadow: var(--ol); font: 20px/1 "Press Start 2P", monospace; cursor: pointer; }
.tp-sale .x:focus-visible { outline: 2px solid #f7d046; outline-offset: 2px; }
@keyframes tpSaleIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes tpSaleBlink { 50% { opacity: 0; } }
.tp-sale .dates { font-size: clamp(12px, 3.4vw, 20px); color: #f7d046; text-shadow: var(--ol); margin-top: 6px; }
.tp-sale .when { font-size: clamp(8px, 2.2vw, 11px); color: #fff; text-shadow: var(--ol); }
@media (prefers-reduced-motion: reduce) { .tp-sale, .tp-sale .go { animation: none; } }
/* the "50% OFF" sign next to the buy buttons */
.tp-off { display: inline-flex; flex-direction: column; align-items: flex-start; align-self: flex-start; gap: 6px; margin: 0 0 12px; padding: 10px 12px 9px;
  background: #f7d046; color: #111; box-shadow: 3px 3px 0 #e2412f; font-family: "Press Start 2P", "Courier New", monospace; text-align: left; }
.tp-off b { font-size: 15px; line-height: 1; font-weight: 400; }
.tp-off span { font-size: 8px; line-height: 1.3; }
.opts .tp-off { margin: 6px 6px 8px; }
summary.buy { position: relative; }
.tp-sticker { position: absolute; top: -8px; right: -12px; padding: 5px 5px 4px; background: #f7d046; color: #111; box-shadow: 2px 2px 0 #e2412f;
  font: 9px/1 "Press Start 2P", "Courier New", monospace; transform: rotate(-8deg); pointer-events: none; }`;
  document.head.appendChild(style);

  // ---- "50% OFF" signs where people buy ----
  const sign = () => { const d = document.createElement("div"); d.className = "tp-off"; d.innerHTML = "<b>50% OFF</b><span>until Cyber Monday, Nov 30</span>"; return d; };
  const card = document.querySelector("#buy .card");                    // main gallery: the "i want to buy it" popup
  if (card) card.insertBefore(sign(), card.querySelector(".k") || card.firstChild);
  const pbuy = document.getElementById("pbuy");                         // vortex: the buy section of a painting
  if (pbuy) pbuy.insertBefore(sign(), pbuy.firstChild);
  document.querySelectorAll("details.buyw").forEach(d => {               // painting list: a sticker on each buy circle and a sign in its menu
    const st = document.createElement("span"); st.className = "tp-sticker"; st.textContent = "50%"; st.setAttribute("aria-hidden", "true");
    d.querySelector("summary").appendChild(st);
    const opts = d.querySelector(".opts"); if (opts) opts.insertBefore(sign(), opts.firstChild);
  });

  if (seen) return;                                                     // the intro below shows once per visit

  const ov = document.createElement("div");
  ov.className = "tp-sale"; ov.setAttribute("role", "dialog"); ov.setAttribute("aria-modal", "true"); ov.setAttribute("aria-label", "50% off all paintings");
  ov.innerHTML = '<button class="x" type="button" aria-label="Close">×</button><canvas width="320" height="320" aria-hidden="true"></canvas>'
    + '<p class="big">50% OFF</p><p class="small">ALL PAINTINGS</p><p class="dates">NOV 26 - NOV 30</p><p class="when">THANKSGIVING TO CYBER MONDAY</p><p class="go">TAP TO ENTER</p>';
  document.body.appendChild(ov);

  // ---- the turkey: drawn on a 32x32 pixel grid, scaled up without smoothing ----
  const N = 32, off = document.createElement("canvas"); off.width = off.height = N;
  const g = off.getContext("2d");
  const BONE = "#f4f1e6", SHADE = "#bdb7a6", HOLE = "#000", BEAK = "#f5a623", RED = "#e2412f", TIP = "#f7d046", MID = "#e07a2c", BASE = "#8a4b22";
  const px = (x, y, c) => { g.fillStyle = c; g.fillRect(Math.round(x), Math.round(y), 1, 1); };
  const line = (x0, y0, x1, y1, c) => {
    x0 = Math.round(x0); y0 = Math.round(y0); x1 = Math.round(x1); y1 = Math.round(y1);
    const dx = Math.abs(x1 - x0), sx = x0 < x1 ? 1 : -1, dy = -Math.abs(y1 - y0), sy = y0 < y1 ? 1 : -1; let e = dx + dy;
    for (;;) { px(x0, y0, c); if (x0 === x1 && y0 === y1) break; const e2 = 2 * e; if (e2 >= dy) { e += dy; x0 += sx; } if (e2 <= dx) { e += dx; y0 += sy; } }
  };
  const foot = (x, y, c) => { px(x - 1, y, c); px(x, y, c); px(x + 1, y, c); };

  function draw(f) {
    g.clearRect(0, 0, N, N);
    const bob = f % 2, sway = [0, 1, 0, -1][f], up = f % 2 === 0;
    // tail fan: seven feathers (brown base, orange band, yellow tip) with bone quills, swaying
    const cx = 12 + sway, cy = 18 + bob;
    for (let i = 0; i < 7; i++) {
      const t = Math.PI * (1.06 + i * .148), ux = Math.cos(t), uy = Math.sin(t), vx = -uy, vy = ux;
      for (let r = 4; r <= 11.5; r += .5) {
        const c = r > 9.5 ? TIP : r > 7.5 ? MID : BASE, w = r > 8 ? 1.2 : r > 6 ? .8 : .5;
        for (let o = -w; o <= w; o += .4) px(cx + ux * r + vx * o, cy + uy * r + vy * o, c);
      }
      line(cx + ux * 4, cy + uy * 4, cx + ux * 10, cy + uy * 10, SHADE);
    }
    // legs (one kicks while the other stands; both bend on the down beat)
    const hy = 23 + bob;
    if (f === 0) { line(13, hy, 13, 29, BONE); foot(13, 30, BEAK); line(17, hy, 20, 26, BONE); line(20, 26, 23, 25, BONE); px(24, 24, BEAK); px(24, 25, BEAK); }
    else if (f === 2) { line(17, hy, 17, 29, BONE); foot(17, 30, BEAK); line(13, hy, 10, 26, BONE); line(10, 26, 7, 25, BONE); px(6, 24, BEAK); px(6, 25, BEAK); }
    else { line(13, hy, 11, 27, BONE); line(11, 27, 12, 29, BONE); foot(12, 30, BEAK); line(17, hy, 19, 27, BONE); line(19, 27, 18, 29, BONE); foot(18, 30, BEAK); }
    // ribcage: an oval outline with ribs and a spine
    const bx = 15, by = 19 + bob;
    for (let a = 0; a < 64; a++) { const t = a / 64 * Math.PI * 2; px(bx + Math.cos(t) * 5.2, by + Math.sin(t) * 4.2, BONE); }
    for (let x = bx - 3; x <= bx + 3; x += 2) line(x, by - 2, x, by + 2, x % 4 === 0 ? SHADE : BONE);
    line(bx - 4, by, bx + 4, by, SHADE);
    // wings: bone arms raised on the up beat, held out on the down beat
    if (up) { line(18, by - 2, 21, by - 6, BONE); line(21, by - 6, 23, by - 9, BONE); line(23, by - 9, 25, by - 10, SHADE); line(23, by - 9, 24, by - 11, SHADE);
              line(12, by - 2, 9, by - 6, BONE); line(9, by - 6, 7, by - 9, BONE); line(7, by - 9, 5, by - 10, SHADE); line(7, by - 9, 6, by - 11, SHADE); }
    else    { line(19, by - 1, 23, by - 1, BONE); line(23, by - 1, 26, by + 1, BONE); line(26, by + 1, 27, by, SHADE);
              line(11, by - 1, 7, by - 1, BONE); line(7, by - 1, 4, by + 1, BONE); line(4, by + 1, 3, by, SHADE); }
    // neck vertebrae up to the skull
    const hx = 22 + (f === 1 ? 1 : f === 3 ? -1 : 0), hyy = 7 + bob;
    [[18, by - 4], [19, by - 6], [20, by - 8], [hx - 1, hyy + 4]].forEach(([x, y], i) => px(x, y, i % 2 ? SHADE : BONE));
    // skull with an eye socket, beak, wattle and snood
    for (let y = -3; y <= 3; y++) for (let x = -3; x <= 3; x++) if (x * x + y * y <= 10) px(hx + x, hyy + y, BONE);
    px(hx + 1, hyy - 1, HOLE); px(hx + 2, hyy - 1, HOLE); px(hx + 1, hyy, HOLE);
    px(hx - 1, hyy + 2, SHADE); px(hx + 1, hyy + 2, SHADE);                                  // teeth line
    px(hx + 4, hyy, BEAK); px(hx + 4, hyy + 1, BEAK); px(hx + 5, hyy + 1, BEAK); px(hx + 6, hyy + 1, BEAK); px(hx + 4, hyy + 2, BEAK);
    px(hx + 4, hyy + 3, RED); px(hx + 4, hyy + 4, RED); px(hx + 3, hyy + 4, RED); px(hx + 4, hyy + 5, RED);
    px(hx + 3, hyy - 3, RED); px(hx + 4, hyy - 2, RED);
    // dark 1-pixel outline around the sprite, so the white bones show on the white gallery
    const im = g.getImageData(0, 0, N, N), a = im.data, o = new Uint8ClampedArray(a);
    const on = (x, y) => x >= 0 && y >= 0 && x < N && y < N && a[(y * N + x) * 4 + 3] > 0;
    for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) {
      const i = (y * N + x) * 4;
      if (a[i + 3] === 0 && (on(x - 1, y) || on(x + 1, y) || on(x, y - 1) || on(x, y + 1))) { o[i] = o[i + 1] = o[i + 2] = 17; o[i + 3] = 255; }
    }
    g.putImageData(new ImageData(o, N, N), 0, 0);
  }
  const cv = ov.querySelector("canvas"), ctx = cv.getContext("2d"); ctx.imageSmoothingEnabled = false;
  let f = 0;
  const paint = () => { draw(f); ctx.clearRect(0, 0, 320, 320); ctx.drawImage(off, 0, 0, N, N, 0, 0, 320, 320); };
  paint();
  const timer = reduce ? 0 : setInterval(() => { f = (f + 1) % 4; paint(); }, 190);

  // ---- closing ----
  let closed = false;
  function close() {
    if (closed) return; closed = true; clearInterval(timer); clearTimeout(auto);
    removeEventListener("keydown", onKey, true);
    ov.classList.add("out"); setTimeout(() => ov.remove(), 380);
  }
  function onKey(e) { e.preventDefault(); e.stopPropagation(); close(); }
  ov.addEventListener("click", close);
  addEventListener("keydown", onKey, true);
  const auto = setTimeout(close, 6500);
  ov.tabIndex = -1; ov.style.outline = "none"; ov.focus({ preventScroll: true });   // focus the dialog itself, so no ring shows on the close button
  if (window.tpTrack) tpTrack("sale_popup", { action: "shown" });
})();
