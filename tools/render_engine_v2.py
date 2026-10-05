"""Shared renderer for Dogetlawyer Case Files 09+ (1080x1920, 30 fps, fades only, colour per SECTION not per scene).
A case module calls configure(...), defines scenes, then build(SCENES) and main()."""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from multitheme import theme, gradient, hexc, mix

W, H, FPS, M = 1080, 1920, 30, 84
CW = W - 2 * M; XF = 0.30
FD = HEAD = BODY = BODY_B = MONO = MONO_B = SERIF = CAP = None
LHK = 1.12; CASE = ""; STH = []; MAP = []; BGF = None; SC = []; DUR = 0; BG = {}; GRAIN = []

def configure(fd, fonts, case, sections, smap, bgf):
    global FD, HEAD, BODY, BODY_B, MONO, MONO_B, SERIF, CAP, CASE, STH, MAP, BGF
    FD = fd; HEAD, BODY, BODY_B, MONO, MONO_B, SERIF, CAP = fonts
    CASE = case; STH = [theme(*s) for s in sections]; MAP = smap; BGF = bgf

def cl(x): return 0.0 if x < 0 else (1.0 if x > 1 else x)
def eio(x): x = cl(x); return x * x * (3 - 2 * x)
_fc = {}
def F(n, s):
    if (n, s) not in _fc: _fc[(n, s)] = ImageFont.truetype(os.path.join(FD, n + ".ttf"), s)
    return _fc[(n, s)]
def tw(f, s, tr=0): return f.getlength(s) + tr * max(0, len(s) - 1)
def text(d, x, y, s, f, c, tr=0, align="l"):
    w = tw(f, s, tr)
    if align == "c": x -= w / 2
    elif align == "r": x -= w
    if tr == 0: d.text((x, y), s, font=f, fill=c); return w
    for ch in s: d.text((x, y), ch, font=f, fill=c); x += f.getlength(ch) + tr
    return w
def wrap(f, s, maxw):
    out, cur = [], ""
    for wd in s.split(" "):
        t = (cur + " " + wd).strip()
        if tw(f, t) <= maxw or not cur: cur = t
        else: out.append(cur); cur = wd
    if cur: out.append(cur)
    return out

class Ctx:
    def __init__(s, im, T, u): s.im = im; s.d = ImageDraw.Draw(im); s.T = T; s.u = u
    def a(s, t0, dur=0.4): return eio((s.u - t0) / dur)
    def c(s, role, al): return mix(s.T["bg"], s.T[role] if isinstance(role, str) else role, al)
    def head(s, lines, y, size, t0, role="fg", align="l", maxw=CW, stag=0.2, x=None, lh_k=None):
        f = F(HEAD, size)
        while max(tw(f, l) for l in lines) > maxw and size > 36: size -= 4; f = F(HEAD, size)
        bb = f.getbbox("H"); top, ch = bb[1], bb[3] - bb[1]; lh = int(ch * (lh_k or LHK))
        x = (M if align == "l" else W / 2) if x is None else x
        for i, l in enumerate(lines):
            al = s.a(t0 + i * stag)
            if al > 0: text(s.d, x, y + i * lh - top, l, f, s.c(role[i] if isinstance(role, list) else role, al), align=align)
        return y + (len(lines) - 1) * lh + ch
    def para(s, t, y, size, t0, role="mut", fn=None, maxw=CW, lead=1.32, align="l", x=None):
        f = F(fn or BODY, size); ls = wrap(f, t, maxw); al = s.a(t0)
        x = (M if align == "l" else W / 2) if x is None else x
        for i, l in enumerate(ls):
            if al > 0: text(s.d, x, y + i * int(size * lead), l, f, s.c(role, al), align=align)
        return y + len(ls) * int(size * lead)
    def mono(s, t, x, y, size, t0, role="dim", tr=2, align="l", fn=None):
        al = s.a(t0)
        if al > 0: text(s.d, x, y, t, F(fn or MONO, size), s.c(role, al), tr=tr, align=align)
    def box(s, x0, y0, x1, y1, t0, fill="panel", edge="edge", r=20, w=2):
        al = s.a(t0)
        if al > 0: s.d.rounded_rectangle([x0, y0, x1, y1], radius=r, fill=s.c(fill, al), outline=s.c(edge, al) if edge else None, width=w)
    def pill(s, t, x, y, t0, size=30, fill="acc", tcol="bg"):
        al = s.a(t0)
        if al <= 0: return 0
        f = F(MONO_B, size); w = tw(f, t, 2) + 48; h = size + 30
        s.d.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, fill=s.c(fill, al))
        text(s.d, x + 24, y + 13, t, f, s.c(tcol, al), tr=2); return w

def tick(c, x, y, s, t0, role="ok"):
    al = c.a(t0, 0.3)
    if al <= 0: return
    pts = [(x, y + 0.55 * s), (x + 0.38 * s, y + 0.9 * s), (x + s, y + 0.1 * s)]
    c.d.line(pts, fill=c.c(role, al), width=max(6, int(s * 0.14)), joint="curve")
def cross(c, x, y, s, t0, role="acc"):
    al = c.a(t0, 0.3)
    if al <= 0: return
    w = max(6, int(s * 0.14))
    c.d.line([(x, y), (x + s, y + s)], fill=c.c(role, al), width=w); c.d.line([(x + s, y), (x, y + s)], fill=c.c(role, al), width=w)
def win(c, t0, title, y0, y1):
    c.box(M, y0, W - M, y1, t0, r=20); al = c.a(t0)
    if al > 0:
        c.d.rounded_rectangle([M, y0, W - M, y0 + 70], radius=20, fill=c.c("edge", al))
        c.d.rectangle([M, y0 + 50, W - M, y0 + 70], fill=c.c("edge", al))
        for k in range(3): c.d.ellipse([M + 28 + k * 30, y0 + 26, M + 46 + k * 30, y0 + 44], fill=c.c("dim", al))
        text(c.d, M + 140, y0 + 20, title, F(MONO, 24), c.c("fg", al), tr=1)

def close_card(c, line2, sub):
    c.head(["DOGETLAWYER"], 560, 140, 0.1, role="acc", align="c")
    c.head(line2, 740, 170, 0.4, align="c")
    c.para(sub, 1070, 42, 0.9, role="mut", align="c", fn=SERIF)
    c.para("dogetlawyer.com", 1145, 44, 0.9, role="fg", fn=BODY_B, align="c")
    al = c.a(0.8)
    if al > 0:
        f = F(MONO_B, 30); w = tw(f, "LINK IN BIO", 3) + 60
        c.d.rounded_rectangle([W / 2 - w / 2, 1215, W / 2 + w / 2, 1275], radius=30, fill=c.c("acc", al))
        text(c.d, W / 2, 1229, "LINK IN BIO", f, c.c("bg", al), tr=3, align="c")
    c.para("Contract management software for UK small businesses — not a substitute for legal advice.", 1320, 30, 1.4, role="mut", align="c", maxw=CW - 40)
    c.para("All names, figures and documents shown are fictional examples.", 1410, 26, 1.5, role="dim", align="c")

def build(SCENES):
    global SC, DUR, BG, GRAIN
    t = 0.0; SC = []
    for i, (d, lab, demo, vo, fn) in enumerate(SCENES):
        SC.append((t, t + d, STH[MAP[i]], lab, demo, vo, fn)); t += d
    DUR = t
    BG = {id(T): BGF(T) for T in STH}
    rng = np.random.default_rng(9); GRAIN = []
    for _ in range(8):
        g = rng.normal(0, 1, (H // 4, W // 4)).astype(np.float32)
        g = np.array(Image.fromarray(((g * 40) + 128).clip(0, 255).astype(np.uint8)).resize((W, H), Image.BICUBIC), dtype=np.float32) - 128
        GRAIN.append((g * 0.07)[..., None])

def caption_at(si, u):
    a, b = SC[si][0], SC[si][1]; vo = SC[si][5]; dur = b - a - 0.4; tot = sum(len(s) for s in vo); tt = 0.15
    for s in vo:
        d = dur * len(s) / tot
        if tt <= u < tt + d: return s, cl((u - tt) / 0.15) * cl((tt + d - u) / 0.15)
        tt += d
    return None, 0

CHROME = None   # optional override: fn(d, T, label, demo, si)
def chrome(d, T, label, demo, si):
    text(d, M, 96, "DOGETLAWYER", F(MONO_B, 26), T["acc"], tr=3)
    text(d, W - M, 96, CASE, F(MONO, 24), T["dim"], tr=2, align="r")
    f = F(MONO_B, 22); w = tw(f, label, 2) + 40
    d.rounded_rectangle([M, 150, M + w, 196], radius=23, outline=T["fg"], width=2); text(d, M + 20, 159, label, f, T["fg"], tr=2)
    p = (si + 1) / len(SC)
    d.rectangle([M, 230, W - M, 233], fill=T["line"]); d.rectangle([M, 230, M + int(CW * p), 233], fill=T["acc"])
    d.rectangle([M, 1490, W - M, 1491], fill=T["line"])
    if demo: text(d, M, 1820, "FICTIONAL DEMO EXAMPLE", F(MONO, 22), T["dim"], tr=2)
    text(d, W - M, 1820, "dogetlawyer.com", F(MONO, 22), T["dim"], tr=1, align="r")

def draw_caption(d, T, s, al):
    if not s or al <= 0: return
    f = F(CAP, 44); ls = wrap(f, s, CW - 60); y0 = 1560 - (len(ls) - 1) * 30
    for i, l in enumerate(ls): text(d, W / 2, y0 + i * 60, l, f, mix(T["bg"], T["fg"], al), align="c")

def render_scene(si, t):
    a, b, T, label, demo, vo, fn = SC[si]
    im = BG[id(T)].copy(); c = Ctx(im, T, t - a); fn(c)
    (CHROME or chrome)(c.d, T, label, demo, si); s, al = caption_at(si, t - a); draw_caption(c.d, T, s, al)
    return im

def frame(i):
    t = i / FPS; si = max(k for k, s in enumerate(SC) if t >= s[0]); a, b = SC[si][0], SC[si][1]
    im = render_scene(si, t)
    if si + 1 < len(SC) and t > b - XF / 2: im = Image.blend(im, render_scene(si + 1, t), eio((t - (b - XF / 2)) / XF))
    elif si > 0 and t < a + XF / 2: im = Image.blend(render_scene(si - 1, t), im, eio((t - (a - XF / 2)) / XF))
    return (np.asarray(im, dtype=np.float32) + GRAIN[i % 8]).clip(0, 255).astype(np.uint8)

def main(here, vofile=None):
    if vofile:
        import json
        json.dump(dict(sc=[[s[0], s[1], s[3], s[5]] for s in SC], th=[s[2]["name"] for s in SC]), open(vofile, "w"), indent=1)
    cmd = sys.argv[1]
    if cmd == "info":
        print("duration", DUR, "frames", int(round(DUR * FPS)))
        for s in SC: print(f"{s[0]:6.1f}-{s[1]:6.1f} {s[2]['name']:28s} {s[3]}  words={sum(len(v.split()) for v in s[5])}")
    elif cmd == "preview":
        os.makedirs(os.path.join(here, "pv"), exist_ok=True)
        for ts in sys.argv[2:]:
            Image.fromarray(frame(int(round(float(ts) * FPS)))).save(os.path.join(here, "pv", f"t{float(ts):06.2f}.png"))
    else:
        import subprocess
        s, e, out = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                              "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "14",
                              "-pix_fmt", "yuv420p", "-g", "60", out], stdin=subprocess.PIPE)
        for i in range(s, e): p.stdin.write(frame(i).tobytes())
        p.stdin.close(); p.wait(); print("DONE", out, flush=True)
