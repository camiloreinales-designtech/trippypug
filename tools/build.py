#!/usr/bin/env python3
"""Regenerate index.html (3D gallery), vortex.html (looping corridor) and simple.html from paintings.json. Run: python3 tools/build.py"""
import html, json, os, urllib.parse
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAIL = "trippypuginfo@gmail.com"
GOOGLE_TAG = "GTM-TWCG6DS8"   # Google tag from Google Analytics (GTM-... or G-...). Empty = no tracking script is loaded.
_tag = ""
if GOOGLE_TAG.startswith("GTM-"):   # the snippet Google Analytics gave for this site
    _tag = (f'<script async src="https://www.googletagmanager.com/gtm.js?id={GOOGLE_TAG}"></script>'
            '<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag("js",new Date());</script>')
elif GOOGLE_TAG:
    _tag = (f'<script async src="https://www.googletagmanager.com/gtag/js?id={GOOGLE_TAG}"></script>'
            f'<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag("js",new Date());gtag("config","{GOOGLE_TAG}");</script>')
# _tag first (as Google asks), then a tiny helper the pages use for painting_view / buy_open / buy_click events
ANALYTICS = _tag + '<script>window.tpTrack=function(n,p){try{if(window.gtag)gtag("event",n,p||{})}catch(e){}};</script>'
P = json.load(open(os.path.join(ROOT, "paintings.json"), encoding="utf-8"))
rd = lambda f: open(os.path.join(ROOT, f), encoding="utf-8").read()

import hashlib
def ver(path):
    try: return "?v=" + hashlib.md5(open(os.path.join(ROOT, path), "rb").read()).hexdigest()[:8]
    except Exception: return ""

def figure(n, p, pos=None):
    num = p["id"][1:]
    q = lambda t: urllib.parse.quote(t, safe="")
    detail = f'{p["year"]}, {p["medium"]}, {p["dimensions"]}'
    body = f'Hi! I\'m interested in "{p["title"]}" ({detail}). Is it available?'
    mail = f'mailto:{MAIL}?subject={q("I want to buy: " + p["title"])}&amp;body={q(body)}'
    price = f'<span class="d">{"SOLD" if p.get("sold") else html.escape(p["price"], quote=True)}</span>' if p.get("price") or p.get("sold") else ""
    dot = '<i class="dot" aria-hidden="true"></i>' if p.get("sold") else ""
    buy = "" if p.get("sold") else (f'<details class="buyw" data-title="{html.escape(p["title"], quote=True)}"><summary class="buy" aria-label="I want to buy {html.escape(p["title"], quote=True)}">i want<br>to buy<br>it</summary>'
           f'<div class="opts"><a href="{mail}">send an email</a>'
           f'<a class="ig" href="https://ig.me/m/trippypug" target="_blank" rel="noopener" data-msg="{html.escape(body, quote=True)}">message @trippypug on instagram</a></div></details>')
    lazy = "" if (n if pos is None else pos) < 2 else ' loading="lazy"'
    t = html.escape(p["title"], quote=False)
    return f'''<figure id="p{n + 1}" data-title="{html.escape(p["title"], quote=True)}">
  <a href="images/full/p{num}.jpg{ver("images/full/p"+num+".jpg")}" aria-label="View {html.escape(p["title"], quote=True)} full size"><img src="images/p{num}.jpg{ver("images/p"+num+".jpg")}" width="{p["w"]}" height="{p["h"]}" alt="{html.escape(p["alt"], quote=True)}"{lazy} decoding="async">{dot}</a>
  <figcaption>
    <div class="lab"><span class="a">trippypug</span><span class="t"><b>{t}</b> {p["year"]}</span><span>{html.escape(p["medium"], quote=False)}</span><span class="d">{html.escape(p["dimensions"], quote=True)}</span>{price}</div>
    {buy}
  </figcaption>
</figure>'''

import json as _j
_ld = {"@context":"https://schema.org","@graph":[{"@type":"Person","name":"Trippy Pug","alternateName":"trippypug","url":"https://gallery.trippypug.com/","sameAs":["https://www.instagram.com/trippypug/"]}]+[{"@type":"VisualArtwork","name":p["title"],"creator":{"@type":"Person","name":"Trippy Pug"},"dateCreated":str(p["year"]),"artMedium":p["medium"],"width":p["dimensions"],"image":"https://gallery.trippypug.com/images/full/"+p["id"]+".jpg"} for p in P]}
simple = rd("tools/simple.template.html").replace("<!--JSONLD-->", '<script type="application/ld+json">'+_j.dumps(_ld,ensure_ascii=False)+'</script>')
simple = simple.replace("<!--ANALYTICS-->", ANALYTICS).replace("<!--FIGURES-->", "\n".join(figure(n, p, i) for i, (n, p) in enumerate(reversed(list(enumerate(P))))))
open(os.path.join(ROOT, "simple.html"), "w", encoding="utf-8").write(simple)

docs = [dict(id=p["id"], assetId="", url=f'images/full/{p["id"]}.jpg' + ver(f'images/full/{p["id"]}.jpg'), w=p["w"], h=p["h"], ts=n + 1, artist="trippypug",
             title=p["title"], year=p["year"], medium=p["medium"], dimensions=p["dimensions"], price=p.get("price", ""), pay=p.get("pay", ""), sold=bool(p.get("sold")), origin="")
        for n, p in enumerate(P)]
stub = ("<script>window.claude={use:async n=>n==='db'?{collection:()=>({orderBy:()=>({onSnapshot:cb=>setTimeout(()=>cb({docs:"
        + json.dumps(docs, ensure_ascii=False).replace("</", "<\\/") + ".map(d=>({id:d.id,data:()=>d}))}),0)})})}:null};</script>")
open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(rd("tools/gallery.template.html").replace("<!--PAINTINGS_STUB-->", stub).replace("<!--ANALYTICS-->", ANALYTICS))
vdata = [dict(id=p["id"], title=p["title"], year=str(p["year"]), medium=p["medium"], dimensions=p["dimensions"], price=p.get("price", ""), sold=bool(p.get("sold")),
              w=p["w"], h=p["h"], alt=p.get("alt", ""), thumb=f'images/{p["id"]}.jpg' + ver(f'images/{p["id"]}.jpg'), full=f'images/full/{p["id"]}.jpg' + ver(f'images/full/{p["id"]}.jpg'))
         for p in P]
open(os.path.join(ROOT, "vortex.html"), "w", encoding="utf-8").write(rd("tools/vortex.template.html").replace("<!--ANALYTICS-->", ANALYTICS).replace("__DATA__", json.dumps(vdata, ensure_ascii=False).replace("</", "<\\/")))
print(f"built {len(P)} paintings")
