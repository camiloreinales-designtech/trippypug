#!/usr/bin/env python3
"""Regenerate index.html (3D gallery) and simple.html from paintings.json. Run: python3 tools/build.py"""
import html, json, os, urllib.parse
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAIL = "trippypuginfo@gmail.com"
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
    buy = "" if p.get("sold") else f'<a class="buy" href="{mail}" aria-label="I want to buy {html.escape(p["title"], quote=True)}">i want<br>to buy<br>it</a>'
    lazy = "" if (n if pos is None else pos) < 2 else ' loading="lazy"'
    t = html.escape(p["title"], quote=False)
    return f'''<figure id="p{n + 1}">
  <a href="images/full/p{num}.jpg{ver("images/full/p"+num+".jpg")}" aria-label="View {html.escape(p["title"], quote=True)} full size"><img src="images/p{num}.jpg{ver("images/p"+num+".jpg")}" width="{p["w"]}" height="{p["h"]}" alt="{html.escape(p["alt"], quote=True)}"{lazy} decoding="async">{dot}</a>
  <figcaption>
    <div class="lab"><span class="a">trippypug</span><span class="t"><b>{t}</b> {p["year"]}</span><span>{html.escape(p["medium"], quote=False)}</span><span class="d">{html.escape(p["dimensions"], quote=True)}</span>{price}</div>
    {buy}
  </figcaption>
</figure>'''

import json as _j
_ld = {"@context":"https://schema.org","@graph":[{"@type":"Person","name":"Trippy Pug","alternateName":"trippypug","url":"https://gallery.trippypug.com/","sameAs":["https://www.instagram.com/trippypug/"]}]+[{"@type":"VisualArtwork","name":p["title"],"creator":{"@type":"Person","name":"Trippy Pug"},"dateCreated":str(p["year"]),"artMedium":p["medium"],"width":p["dimensions"],"image":"https://gallery.trippypug.com/images/full/"+p["id"]+".jpg"} for p in P]}
simple = rd("tools/simple.template.html").replace("<!--JSONLD-->", '<script type="application/ld+json">'+_j.dumps(_ld,ensure_ascii=False)+'</script>')
simple = simple.replace("<!--FIGURES-->", "\n".join(figure(n, p, i) for i, (n, p) in enumerate(reversed(list(enumerate(P))))))
open(os.path.join(ROOT, "simple.html"), "w", encoding="utf-8").write(simple)

docs = [dict(id=p["id"], assetId="", url=f'images/full/{p["id"]}.jpg' + ver(f'images/full/{p["id"]}.jpg'), w=p["w"], h=p["h"], ts=n + 1, artist="trippypug",
             title=p["title"], year=p["year"], medium=p["medium"], dimensions=p["dimensions"], price=p.get("price", ""), pay=p.get("pay", ""), sold=bool(p.get("sold")), origin="")
        for n, p in enumerate(P)]
stub = ("<script>window.claude={use:async n=>n==='db'?{collection:()=>({orderBy:()=>({onSnapshot:cb=>setTimeout(()=>cb({docs:"
        + json.dumps(docs, ensure_ascii=False).replace("</", "<\\/") + ".map(d=>({id:d.id,data:()=>d}))}),0)})})}:null};</script>")
open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(rd("tools/gallery.template.html").replace("<!--PAINTINGS_STUB-->", stub))
print(f"built {len(P)} paintings")

# One small page per painting at /p/<num>/ : the permanent address written to its NFC tag.
SITE = "https://gallery.trippypug.com"
ptpl = rd("tools/painting.template.html")
rows = ["id,title,tag_url"]
for p in P:
    num = p["id"][1:]
    url = f"{SITE}/p/{num}/"
    e = lambda s: html.escape(str(s), quote=True)
    q = lambda t: urllib.parse.quote(t, safe="")
    detail = f'{p["year"]}, {p["medium"]}, {p["dimensions"]}'
    mail = f'mailto:{MAIL}?subject={q("I want to buy: " + p["title"])}&amp;body={q(f"Hi! I am interested in \"{p["title"]}\" ({detail}). Is it available?")}'
    if p.get("sold"):
        price, buy = '<span class="sold">SOLD</span>', ""
    else:
        price = f'<span class="d">{e(p["price"])}</span>' if p.get("price") else ""
        pay = f'<a class="pri" href="{e(p["pay"])}" target="_blank" rel="noopener">pay securely online</a>' if str(p.get("pay", "")).startswith("https://") else ""
        buy = (f'<section class="buy" aria-label="Buy this painting"><h2>i want to buy it</h2><div class="btns">{pay}'
               f'<a class="{"" if pay else "pri"}" href="{mail}">email trippypug</a>'
               f'<a href="https://www.instagram.com/trippypug/" target="_blank" rel="noopener">message on Instagram</a></div>'
               f'<p>If your email app does not open, write to <b>{MAIL}</b> with the painting\'s title.</p></section>')
    full = f'images/full/p{num}.jpg'
    out = (ptpl.replace("{{TITLE_ATTR}}", e(p["title"])).replace("{{TITLE}}", e(p["title"])).replace("{{YEAR}}", e(p["year"]))
           .replace("{{MEDIUM}}", e(p["medium"])).replace("{{DIMS}}", e(p["dimensions"])).replace("{{ALT}}", e(p["alt"]))
           .replace("{{URL}}", url).replace("{{IMG_ABS}}", f"{SITE}/{full}").replace("{{IMG_FULL}}", f"../../{full}{ver(full)}")
           .replace("{{W}}", str(p["w"])).replace("{{H}}", str(p["h"])).replace("{{PRICE}}", price).replace("{{BUY}}", buy))
    os.makedirs(os.path.join(ROOT, "p", num), exist_ok=True)
    open(os.path.join(ROOT, "p", num, "index.html"), "w", encoding="utf-8").write(out)
    rows.append(f'{p["id"]},"{p["title"].replace(chr(34), chr(34)*2)}",{url}')
open(os.path.join(ROOT, "tools", "nfc-tags.csv"), "w", encoding="utf-8").write("\n".join(rows) + "\n")
print(f"built {len(P)} painting pages in p/ and tools/nfc-tags.csv")
