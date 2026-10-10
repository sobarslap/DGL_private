"""Shared helpers for the 3-minute Delivery videos (engine v3): chrome with PREVIEW / FICTIONAL / REAL AUTHORITY flags,
captions that read on light and dark sections, drawn arrows (fonts lack the arrow glyph), paper cards."""
import math
import engine3 as E
from engine3 import F, tw, text, wrap, M, W, CW
from multitheme import mix, hexc

PAPER = hexc("#FBFAF7"); INK = hexc("#1A1A1A"); GREY = hexc("#6F6A62"); RULE = hexc("#E2DED6"); RED = hexc("#D93025")
HIL = hexc("#FFE08A")

def arrow(c, p0, p1, t0, role="acc", w=10):
    al = c.a(t0)
    if al <= 0: return
    col = c.c(role, al); x0, y0 = p0; x1, y1 = p1
    ang = math.atan2(y1 - y0, x1 - x0); L = w * 2.6
    bx, by = x1 - L * math.cos(ang), y1 - L * math.sin(ang); nx, ny = -math.sin(ang), math.cos(ang)
    c.d.line([(x0, y0), (bx, by)], fill=col, width=w)
    c.d.polygon([(x1, y1), (bx + nx * w * 1.7, by + ny * w * 1.7), (bx - nx * w * 1.7, by - ny * w * 1.7)], fill=col)

def card(c, x0, y0, x1, y1, t0, r=24, fill=PAPER, bar=None):
    al = c.a(t0)
    if al <= 0: return 0
    c.d.rounded_rectangle([x0, y0, x1, y1], radius=r, fill=c.c(fill, al), outline=c.c(RULE, al) if c.T["light"] else None, width=2)
    if bar: c.d.rectangle([x0, y0 + r, x0 + 12, y1 - r], fill=c.c(bar, al))
    return al

def ptext(c, s, x, y, size, t0, fn=None, col=INK, maxw=None, lead=1.3):
    """Text on a paper card (fixed ink colours, faded with the scene)."""
    al = c.a(t0)
    if al <= 0: return y
    f = F(fn or E.BODY, size); ls = wrap(f, s, maxw) if maxw else [s]
    for i, l in enumerate(ls): text(c.d, x, y + i * int(size * lead), l, f, c.c(col, al))
    return y + len(ls) * int(size * lead)

def chip(c, s, x, y, t0, size=24, fill=None, tcol=None, fn=None):
    al = c.a(t0)
    if al <= 0: return 0
    f = F(fn or E.MONO_B, size); w = tw(f, s, 2) + 36; h = size + 24
    c.d.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, fill=c.c(fill or c.T["acc"], al))
    text(c.d, x + 18, y + 11, s, f, c.c(tcol or c.T["bg"], al), tr=2); return w

def make_chrome(product):
    def chrome(d, T, label, flags, si):
        flags = flags or ""
        text(d, M, 96, "DOGETLAWYER", F(E.MONO_B, 26), T["acc"], tr=3)
        text(d, W - M, 96, product, F(E.MONO, 24), T["dim"], tr=2, align="r")
        f = F(E.MONO_B, 22); w = tw(f, label, 2) + 40
        d.rounded_rectangle([M, 150, M + w, 196], radius=23, outline=T["fg"], width=2); text(d, M + 20, 159, label, f, T["fg"], tr=2)
        if "P" in flags:
            pw = tw(f, "PREVIEW", 2) + 40
            d.rounded_rectangle([W - M - pw, 150, W - M, 196], radius=23, fill=T["acc"]); text(d, W - M - pw + 20, 159, "PREVIEW", f, T["bg"], tr=2)
        p = (si + 1) / len(E.SC)
        d.rectangle([M, 230, W - M, 233], fill=T["line"]); d.rectangle([M, 230, M + int(CW * p), 233], fill=T["acc"])
        left = []
        if "F" in flags: left.append("FICTIONAL EXAMPLE")
        if "A" in flags: left.append("REAL AUTHORITY · ENGLAND & WALES")
        if left: text(d, M, 1820, " · ".join(left), F(E.MONO, 22), T["dim"], tr=2)
        text(d, W - M, 1820, "dogetlawyer.com", F(E.MONO, 22), T["dim"], tr=1, align="r")
    return chrome

def draw_caption(d, T, s, al):
    if not s or al <= 0: return
    f = F(E.CAP, 62); ls = wrap(f, s, CW - 80); lh = 78; h = len(ls) * lh + 40; y0 = 1600 - h // 2
    wmax = max(tw(f, l) for l in ls) + 70
    panel = mix(T["fg"], (0, 0, 0), 0.15) if T["light"] else mix(T["bg"], (0, 0, 0), 0.5)
    tc = T["bg"] if T["light"] else T["fg"]
    d.rounded_rectangle([W / 2 - wmax / 2, y0, W / 2 + wmax / 2, y0 + h], radius=26, fill=panel)
    for i, l in enumerate(ls): text(d, W / 2, y0 + 16 + i * lh, l, f, tc, align="c")

def install(product):
    E.CHROME = make_chrome(product); E.draw_caption = draw_caption
