#!/usr/bin/env python3
"""Regenerate index.html (3D gallery) and simple.html from paintings.json. Run: python3 tools/build.py"""
import html, json, os, urllib.parse
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAIL = "trippypuginfo@gmail.com"
P = json.load(open(os.path.join(ROOT, "paintings.json"), encoding="utf-8"))
rd = lambda f: open(os.path.join(ROOT, f), encoding="utf-8").read()

def figure(n, p):
    num = p["id"][1:]
    q = lambda t: urllib.parse.quote(t, safe="")
    detail = f'{p["year"]}, {p["medium"]}, {p["dimensions"]}'
    body = f'Hi! I\'m interested in "{p["title"]}" ({detail}). Is it available?'
    mail = f'mailto:{MAIL}?subject={q("I want to buy: " + p["title"])}&amp;body={q(body)}'
    price = f'<span class="d">{"SOLD" if p.get("sold") else html.escape(p["price"], quote=True)}</span>' if p.get("price") or p.get("sold") else ""
    dot = '<i class="dot" aria-hidden="true"></i>' if p.get("sold") else ""
    buy = "" if p.get("sold") else f'<a class="buy" href="{mail}" aria-label="I want to buy {html.escape(p["title"], quote=True)}">i want<br>to buy<br>it</a>'
    lazy = "" if n < 2 else ' loading="lazy"'
    t = html.escape(p["title"], quote=False)
    return f'''<figure id="p{n + 1}">
  <a href="images/full/p{num}.jpg" aria-label="View {html.escape(p["title"], quote=True)} full size"><img src="images/p{num}.jpg" width="{p["w"]}" height="{p["h"]}" alt="{html.escape(p["alt"], quote=True)}"{lazy} decoding="async">{dot}</a>
  <figcaption>
    <div class="lab"><span class="a">trippypug</span><span class="t"><b>{t}</b> {p["year"]}</span><span>{html.escape(p["medium"], quote=False)}</span><span class="d">{html.escape(p["dimensions"], quote=True)}</span>{price}</div>
    {buy}
  </figcaption>
</figure>'''

simple = rd("tools/simple.template.html").replace("<!--FIGURES-->", "\n".join(figure(n, p) for n, p in enumerate(P)))
open(os.path.join(ROOT, "simple.html"), "w", encoding="utf-8").write(simple)

docs = [dict(id=p["id"], assetId="", url=f'images/full/{p["id"]}.jpg', w=p["w"], h=p["h"], ts=n + 1, artist="trippypug",
             title=p["title"], year=p["year"], medium=p["medium"], dimensions=p["dimensions"], price=p.get("price", ""), pay=p.get("pay", ""), sold=bool(p.get("sold")), origin="")
        for n, p in enumerate(P)]
stub = ("<script>window.claude={use:async n=>n==='db'?{collection:()=>({orderBy:()=>({onSnapshot:cb=>setTimeout(()=>cb({docs:"
        + json.dumps(docs, ensure_ascii=False).replace("</", "<\\/") + ".map(d=>({id:d.id,data:()=>d}))}),0)})})}:null};</script>")
open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(rd("tools/gallery.template.html").replace("<!--PAINTINGS_STUB-->", stub))
print(f"built {len(P)} paintings")
