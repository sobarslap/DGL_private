"""Dogetlawyer Case File 08 - "Paid for it. Own the copyright?" Quiz format, multi-colour scenes (boss brief:
slide 1 purple+black, slide 2 grey+red, slide 3 sky blue, then other combinations).
Type: Oswald / Manrope / Space Mono / Lora italic.
Usage: python3 render7.py preview T...  |  python3 render7.py chunk START END OUT.mp4
"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); FD = os.path.join(HERE, "f")
sys.path.insert(0, os.path.join(HERE, ".."))
from multitheme import theme, gradient, hexc, mix
SPEC8 = [
 ("Electric blue & hot pink", "#2433E0", "#D10F70", "#FFFFFF", "#FFE14D", "#7CFFB2"),
 ("Black & lime",             "#0D0D0D", "#2F4A00", "#FFFFFF", "#C6FF3D", "#7CFFB2"),
 ("Sunshine yellow",          "#FFE45C", "#FFB800", "#1A1300", "#C2185B", "#0B6B3A"),
 ("Teal & coral",             "#00706B", "#D24B40", "#FFFFFF", "#FFF1A8", "#B8FFD6"),
 ("Magenta & navy",           "#B1006A", "#0B1640", "#FFFFFF", "#7FE3FF", "#7CFFB2"),
 ("Turquoise",                "#8EF2E6", "#3CC9C0", "#062A2C", "#B0123A", "#0B6B3A"),
 ("Violet & tangerine",       "#4A148C", "#D9550B", "#FFFFFF", "#FFE14D", "#9BF0C0"),
 ("Cherry & cream",           "#FFE9E3", "#FFB3A7", "#3A0A10", "#C2003A", "#0B6B3A"),
]
THEMES = [theme(*s) for s in SPEC8]

W, H, FPS, M = 1080, 1920, 30, 84
CW = W - 2 * M; XF = 0.30
def cl(x): return 0.0 if x < 0 else (1.0 if x > 1 else x)
def eio(x): x = cl(x); return x * x * (3 - 2 * x)
_fc = {}
def F(n, s):
    if (n, s) not in _fc: _fc[(n, s)] = ImageFont.truetype(os.path.join(FD, n + ".ttf"), s)
    return _fc[(n, s)]
HEAD = "BebasNeue_400Regular"; BODY = "DMSans_600SemiBold"; BODY_B = "DMSans_800ExtraBold"
MONO = "DMMono_400Regular"; MONO_B = "DMMono_500Medium"; SERIF = "Fraunces_500Medium_Italic"; CAP = "DMSans_700Bold"
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
    def head(s, lines, y, size, t0, role="fg", align="l", maxw=CW, stag=0.2, x=None):
        f = F(HEAD, size)
        while max(tw(f, l) for l in lines) > maxw and size > 36: size -= 4; f = F(HEAD, size)
        bb = f.getbbox("H"); top, ch = bb[1], bb[3] - bb[1]; lh = int(ch * 1.22)
        x = (M if align == "l" else W / 2) if x is None else x
        for i, l in enumerate(lines):
            al = s.a(t0 + i * stag)
            if al > 0: text(s.d, x, y + i * lh - top, l, f, s.c(role[i] if isinstance(role, list) else role, al), align=align)
        return y + (len(lines) - 1) * lh + ch
    def para(s, t, y, size, t0, role="mut", fn=BODY, maxw=CW, lead=1.32, align="l", x=None):
        f = F(fn, size); ls = wrap(f, t, maxw); al = s.a(t0)
        x = (M if align == "l" else W / 2) if x is None else x
        for i, l in enumerate(ls):
            if al > 0: text(s.d, x, y + i * int(size * lead), l, f, s.c(role, al), align=align)
        return y + len(ls) * int(size * lead)
    def mono(s, t, x, y, size, t0, role="dim", tr=2, align="l", fn=MONO):
        al = s.a(t0)
        if al > 0: text(s.d, x, y, t, F(fn, size), s.c(role, al), tr=tr, align=align)
    def box(s, x0, y0, x1, y1, t0, fill="panel", edge="edge", r=20, w=2):
        al = s.a(t0)
        if al > 0: s.d.rounded_rectangle([x0, y0, x1, y1], radius=r, fill=s.c(fill, al), outline=s.c(edge, al) if edge else None, width=w)
    def pill(s, t, x, y, t0, size=30, fill="acc", tcol="bg"):
        al = s.a(t0)
        if al <= 0: return 0
        f = F(MONO_B, size); w = tw(f, t, 2) + 48; h = size + 30
        s.d.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, fill=s.c(fill, al))
        text(s.d, x + 24, y + 13, t, f, s.c(tcol, al), tr=2); return w

PAPER = hexc("#FBFAF7"); INK = hexc("#1A1A1A"); GREYTXT = hexc("#6B6B6B"); RED = hexc("#C21F30")

def email(c, y0, t0, subj, lines):
    al = c.a(t0)
    if al <= 0: return
    c.d.rounded_rectangle([M, y0, W - M, y0 + 470], radius=22, fill=c.c(PAPER, al))
    text(c.d, M + 40, y0 + 34, "From: Harrow Print Supplies Ltd", F(MONO, 24), c.c(GREYTXT, al))
    text(c.d, M + 40, y0 + 74, "To: accounts@yourbusiness.co.uk", F(MONO, 24), c.c(GREYTXT, al))
    c.d.rectangle([M + 40, y0 + 124, W - M - 40, y0 + 126], fill=c.c(hexc("#DDDDDD"), al))
    yy = y0 + 150
    for l in wrap(F(BODY_B, 38), subj, CW - 80): text(c.d, M + 40, yy, l, F(BODY_B, 38), c.c(INK, al)); yy += 50
    yy += 16
    for i, ln in enumerate(lines):
        for l in wrap(F(BODY, 32), ln, CW - 80):
            hl = i == len(lines) - 1
            if hl:
                c.d.rectangle([M + 34, yy - 4, M + 46 + tw(F(BODY, 32), l), yy + 42], fill=c.c(hexc("#FFE08A"), c.a(t0 + 1.4)))
            text(c.d, M + 40, yy, l, F(BODY, 32), c.c(INK, al)); yy += 44

def spine(c, day, sub, t0=0.0):
    """Timeline chip: big DAY n + small sub-label, plus a vertical spine on the left."""
    al = c.a(t0)
    if al <= 0: return
    x = M + 6
    c.d.rectangle([x, 300, x + 4, 1460], fill=c.c("line", al))
    c.d.ellipse([x - 14, 380, x + 18, 412], fill=c.c("acc", al))
    text(c.d, x + 52, 350, day, F(HEAD, 92), c.c("acc", al))
    text(c.d, x + 56, 470, sub, F(MONO_B, 26), c.c("dim", al), tr=2)

def win(c, t0, title, y0, y1):
    c.box(M, y0, W - M, y1, t0, r=20); al = c.a(t0)
    if al > 0:
        c.d.rounded_rectangle([M, y0, W - M, y0 + 70], radius=20, fill=c.c("edge", al))
        c.d.rectangle([M, y0 + 50, W - M, y0 + 70], fill=c.c("edge", al))
        for k in range(3): c.d.ellipse([M + 28 + k * 30, y0 + 26, M + 46 + k * 30, y0 + 44], fill=c.c("dim", al))
        text(c.d, M + 140, y0 + 20, title, F(MONO, 24), c.c("fg", al), tr=1)

# ---------------------------------------------------------------- scenes (Case 08: copyright)
def tick(c, x, y, s, t0, role="ok"):
    p = eio((c.u - t0) / 0.35)
    if p <= 0: return
    pts = [(x, y + 0.55 * s), (x + 0.38 * s, y + 0.9 * s), (x + s, y + 0.1 * s)]
    c.d.line(pts[:2] if p < 0.5 else pts, fill=c.c(role, 1.0), width=max(6, int(s * 0.14)), joint="curve")

def cross(c, x, y, s, t0, role="acc"):
    al = c.a(t0, 0.3)
    if al <= 0: return
    w = max(6, int(s * 0.14))
    c.d.line([(x, y), (x + s, y + s)], fill=c.c(role, al), width=w); c.d.line([(x + s, y), (x, y + s)], fill=c.c(role, al), width=w)

def s1(c):
    c.mono("TRUE STORY. WELL, NEARLY.", M, 470, 28, 0.0)
    c.head(["YOU PAID", "£800 FOR", "YOUR LOGO."], 540, 230, 0.1, role=["fg", "acc", "fg"])

def s2(c):
    c.head(["SO WHY MIGHT", "IT STILL", "BELONG TO", "THE DESIGNER?"], 470, 190, 0.0, role=["fg", "fg", "fg", "acc"])

def s3(c):
    c.mono("THE BIT NOBODY TELLS YOU", M, 520, 28, 0.0)
    c.head(["PAYING ≠", "OWNING."], 590, 300, 0.15, role=["fg", "acc"])

def s4(c):
    c.mono("SOURCE: GOV.UK · INTELLECTUAL PROPERTY OFFICE", M, 400, 24, 0.0, role="acc", fn=MONO_B)
    al = c.a(0.2)
    if al > 0:
        c.d.rounded_rectangle([M, 460, W - M, 1080], radius=24, fill=c.c(PAPER, al))
        c.d.rectangle([M, 460, M + 14, 1080], fill=c.c("acc", al))
        y = 510
        for l in wrap(F(SERIF, 48), "“When you … commission another person or organisation to create a copyright work for you, the first legal owner of copyright is the person or organisation that created the work and not you the commissioner, unless you otherwise agree it in writing.”", CW - 100):
            text(c.d, M + 56, y, l, F(SERIF, 48), c.c(INK, al)); y += 66
    c.head(["UNLESS IT’S", "IN WRITING."], 1140, 130, 1.8, role="acc")

def s5(c):
    c.mono("QUICK QUIZ", M, 520, 30, 0.0)
    c.head(["WHO OWNS", "IT?"], 590, 300, 0.15, role=["fg", "acc"])
    c.para("Four things most businesses pay for. Guess before the answer lands.", 1180, 44, 1.2, role="mut", fn=SERIF)

def quiz(n, item, made, owner, note, you=False):
    def fn(c):
        c.pill(f"QUESTION {n} OF 4", M, 330, 0.0, size=28)
        c.mono("YOU PAID FOR…", M, 450, 26, 0.1)
        yb = c.head([item], 500, 190, 0.2)
        c.para(made, yb + 40, 46, 0.6, role="mut")
        # reveal
        al = c.a(2.0)
        if al > 0:
            y0 = 1000
            c.d.rounded_rectangle([M, y0, W - M, y0 + 370], radius=26, fill=c.c("panel", al), outline=c.c("ok" if you else "acc", al), width=5)
            text(c.d, M + 40, y0 + 34, "WHO OWNS THE COPYRIGHT?", F(MONO_B, 26), c.c("dim", al), tr=2)
            fs = 150
            while F(HEAD, fs).getlength(owner) > CW - 260: fs -= 6
            text(c.d, M + 40, y0 + 86 + (150 - fs) // 2, owner, F(HEAD, fs), c.c("ok" if you else "acc", al))
            (tick if you else cross)(c, W - M - 150, y0 + 110, 100, 2.2, role="ok" if you else "acc")
            for i, l in enumerate(wrap(F(BODY, 32), note, CW - 80)):
                text(c.d, M + 40, y0 + 250 + i * 40, l, F(BODY, 32), c.c("mut", al))
    return fn

def s10(c):
    c.mono("SO WHAT DO YOU ACTUALLY HAVE?", M, 430, 28, 0.0)
    c.head(["PERMISSION.", "NOT", "OWNERSHIP."], 500, 210, 0.15, role=["acc", "fg", "fg"])
    c.para("A court may find you can use it for what you paid for. That’s a limited licence, not ownership.", 1220, 40, 1.5, role="mut")

def s11(c):
    c.mono("WHY IT BITES", M, 380, 28, 0.0)
    rows = ["You want to tweak it, or use it somewhere new.", "You’re selling the business.", "They reuse it for someone else."]
    y = 470
    for i, s in enumerate(rows):
        tt = 0.3 + i * 0.9
        c.box(M, y, W - M, y + 210, tt, r=22)
        text_al = c.a(tt)
        if text_al > 0: text(c.d, M + 40, y + 40, f"0{i + 1}", F(HEAD, 120), c.c("acc", text_al))
        c.para(s, y + 66, 46, tt, role="fg", fn=BODY_B, x=M + 190, maxw=CW - 230)
        y += 240
    c.head(["IT’S NOT YOURS", "TO DECIDE."], 1220, 110, 3.0, role="acc")

def s12(c):
    c.mono("THE FIX", M, 380, 28, 0.0)
    c.head(["GET IT IN", "WRITING."], 440, 200, 0.1, role=["fg", "acc"])
    steps = [("A copyright assignment", "In writing, signed by them."), ("Final files AND source files", "The logo, the site, the code, the raw photos."),
             ("Kept with the invoice", "Where you can actually find it.")]
    y = 860
    for i, (h, s) in enumerate(steps):
        tt = 1.0 + i * 1.0
        al = c.a(tt)
        if al > 0:
            c.d.rounded_rectangle([M, y, M + 70, y + 70], radius=14, outline=c.c("ok", al), width=6)
            tick(c, M + 14, y + 12, 44, tt + 0.2)
        c.para(h, y - 2, 44, tt, role="fg", fn=BODY_B, x=M + 100)
        c.para(s, y + 56, 34, tt, role="mut", x=M + 100)
        y += 150
    c.mono("COPYRIGHT, DESIGNS AND PATENTS ACT 1988 · s.90(3)", M, 1330, 22, 3.4)

def s13(c):
    c.mono("ALREADY PAID WITHOUT ONE?", M, 520, 28, 0.0)
    c.head(["IT’S NOT TOO", "LATE TO ASK."], 590, 190, 0.15, role=["fg", "acc"])
    c.para("Ask for a written assignment now, while you’re still on good terms.", 1060, 44, 1.2, role="mut", fn=SERIF)

def s14(c):
    c.mono("THAT’S WHAT DOGETLAWYER IS FOR", M, 330, 26, 0.0, role="acc")
    win(c, 0.2, "WHO OWNS WHAT · ALL SUPPLIERS", 400, 1170)
    rows = [("Kite & Co Design", "Logo", "Assignment signed", "ok"),
            ("Northgate Web Studio", "Website", "No assignment on file", "acc"),
            ("Fenwick Photography", "Product photos", "Licence only", "acc")]
    y = 520
    for i, (n, what, st, r) in enumerate(rows):
        tt = 0.7 + i * 0.5
        c.para(n, y, 40, tt, role="fg", fn=BODY_B, x=M + 40)
        c.para(st, y + 2, 32, tt, role=r, fn=BODY_B, x=W - M - 40 - tw(F(BODY_B, 32), st))
        c.mono(what.upper(), M + 40, y + 62, 22, tt, tr=1)
        if i < 2: c.d.rectangle([M + 40, y + 130, W - M - 40, y + 131], fill=c.c("line", c.a(tt)))
        y += 190
    c.para("Every supplier who’s made something for you, and whether you actually own it.", 1220, 42, 2.2, role="mut", fn=SERIF)

def s15(c):
    c.head(["SO YOU KNOW", "WHAT’S", "ACTUALLY", "YOURS."], 520, 200, 0.0, role=["fg", "fg", "fg", "acc"])

def s16(c):
    c.mono("BE HONEST", M, 500, 28, 0.0)
    c.head(["WHICH ONE", "SURPRISED", "YOU?"], 570, 190, 0.15, role=["fg", "fg", "acc"])
    for i in range(4):
        tt = 1.2 + i * 0.2; a = c.a(tt)
        if a <= 0: continue
        x = M + i * 230
        c.d.rounded_rectangle([x, 1120, x + 190, 1300], radius=24, fill=c.c("panel", a), outline=c.c("acc", a), width=4)
        text(c.d, x + 95, 1140, str(i + 1), F(HEAD, 140), c.c("acc", a), align="c")

def close(c):
    c.head(["DOGETLAWYER"], 560, 140, 0.1, role="acc", align="c")
    c.head(["OWN WHAT YOU", "PAID FOR."], 740, 170, 0.4, align="c")
    c.para("Every supplier. Every assignment. One place.", 1060, 42, 0.9, role="mut", align="c", fn=SERIF)
    c.para("dogetlawyer.com", 1140, 44, 0.9, role="fg", fn=BODY_B, align="c")
    al = c.a(0.8)
    if al > 0:
        f = F(MONO_B, 30); w = tw(f, "LINK IN BIO", 3) + 60
        c.d.rounded_rectangle([W / 2 - w / 2, 1210, W / 2 + w / 2, 1270], radius=30, fill=c.c("acc", al))
        text(c.d, W / 2, 1222, "LINK IN BIO", f, c.c("bg", al), tr=3, align="c")
    c.para("Contract management software for UK small businesses — not a substitute for legal advice.", 1320, 30, 1.4, role="mut", align="c", maxw=CW - 40)
    c.para("All names, figures and documents shown are fictional examples.", 1410, 26, 1.5, role="dim", align="c")

SCENES = [
    (3.6, "THE LOGO", False, ["You paid eight hundred quid for your logo."], s1),
    (4.2, "THE LOGO", False, ["So why might it still belong to the designer?"], s2),
    (4.0, "THE CATCH", False, ["Here's the bit nobody tells you. Paying for it isn't the same as owning it."], s3),
    (8.4, "THE LAW", False, ["The government's own guidance says it. If you commission work,",
                             "the person who made it owns the copyright, unless you agree otherwise in writing."], s4),
    (4.4, "QUIZ", False, ["Quick quiz. Who owns it? Guess before the answer lands."], s5),
    (6.8, "QUIZ · 1", False, ["Number one. Your logo, made by a freelance designer.", "Who owns the copyright? The designer. Unless you've got it in writing."],
     quiz(1, "YOUR LOGO", "Made by a freelance designer.", "THE DESIGNER", "Unless there’s a written assignment.")),
    (6.8, "QUIZ · 2", False, ["Number two. Your website, built by an agency.", "The agency. Or it's shared, if your own team helped build it."],
     quiz(2, "YOUR WEBSITE", "Built by a web agency.", "THE AGENCY", "Or joint owners, if your own staff helped build it.")),
    (6.6, "QUIZ · 3", False, ["Number three. Your product photos, taken by a photographer.", "The photographer."],
     quiz(3, "PRODUCT PHOTOS", "Taken by a freelance photographer.", "THE PHOTOGRAPHER", "Unless there’s a written assignment.")),
    (6.8, "QUIZ · 4", False, ["Number four. Something your own employee made, as part of their job.", "That one's usually yours."],
     quiz(4, "STAFF’S WORK", "Made by your employee, as part of their job.", "YOU", "Employers usually own work made in the course of employment.", you=True)),
    (6.8, "WHAT YOU HAVE", False, ["So what have you actually got? Usually, permission. Not ownership.",
                                   "You can use it for what you paid for. That's a licence. It's not the same thing."], s10),
    (7.6, "WHY IT BITES", False, ["And that matters when you want to change it, or use it somewhere new.",
                                  "When you sell the business. Or when they reuse it for someone else."], s11),
    (9.6, "THE FIX", False, ["The fix? Get it in writing. A copyright assignment, signed by them.",
                             "Covering the final files and the source files.", "And keep it with the invoice, where you can find it."], s12),
    (5.0, "THE FIX", False, ["Already paid without one? It's not too late. Ask for it now, while you're on good terms."], s13),
    (8.6, "THE FIX", True, ["That's what Dogetlawyer's for. Every supplier who's made something for you,",
                            "and whether you actually own it, or just have a licence."], s14),
    (3.8, "THE FIX", False, ["So you know what's actually yours."], s15),
    (5.0, "YOUR TURN", False, ["Be honest. Which one surprised you? Comment one, two, three or four."], s16),
    (7.0, "DOGETLAWYER", False, ["Check who owns what at dogetlawyer.com. Link in bio."], close),
]

t = 0.0; SC = []
for i, (d, lab, demo, vo, fn) in enumerate(SCENES):
    SC.append((t, t + d, THEMES[i % len(THEMES)], lab, demo, vo, fn)); t += d
DUR = t

def _bg(T):
    im = gradient(T, W, H); d = ImageDraw.Draw(im)
    ln = mix(T["bg"], T["fg"], 0.06)
    for r in range(160, 2400, 140):  # faint concentric rings from the top-right
        d.ellipse([W - r, -r, W + r, r], outline=ln, width=3)
    return im
BG = {id(T): _bg(T) for T in THEMES}
rng = np.random.default_rng(8); GRAIN = []
for _ in range(8):
    g = rng.normal(0, 1, (H // 4, W // 4)).astype(np.float32)
    g = np.array(Image.fromarray(((g * 40) + 128).clip(0, 255).astype(np.uint8)).resize((W, H), Image.BICUBIC), dtype=np.float32) - 128
    GRAIN.append((g * 0.08)[..., None])

def caption_at(si, u):
    a, b = SC[si][0], SC[si][1]; vo = SC[si][5]; dur = b - a - 0.4; tot = sum(len(s) for s in vo); tt = 0.15
    for s in vo:
        d = dur * len(s) / tot
        if tt <= u < tt + d: return s, cl((u - tt) / 0.15) * cl((tt + d - u) / 0.15)
        tt += d
    return None, 0

def chrome(d, T, label, demo, si):
    text(d, M, 96, "DOGETLAWYER", F(MONO_B, 26), T["acc"], tr=3)
    text(d, W - M, 96, "CASE FILE 08", F(MONO, 24), T["dim"], tr=2, align="r")
    f = F(MONO_B, 22); w = tw(f, label, 2) + 40
    d.rounded_rectangle([M, 150, M + w, 196], radius=23, fill=T["fg"]); text(d, M + 20, 159, label, f, T["bg"], tr=2)
    # progress: thin bar across the top of the frame
    p = (si + 1) / len(SC)
    d.rectangle([0, 0, int(W * p), 8], fill=T["acc"])
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
    chrome(c.d, T, label, demo, si); s, al = caption_at(si, t - a); draw_caption(c.d, T, s, al)
    return im

def frame(i):
    t = i / FPS; si = max(k for k, s in enumerate(SC) if t >= s[0]); a, b = SC[si][0], SC[si][1]
    im = render_scene(si, t)
    if si + 1 < len(SC) and t > b - XF / 2: im = Image.blend(im, render_scene(si + 1, t), eio((t - (b - XF / 2)) / XF))
    elif si > 0 and t < a + XF / 2: im = Image.blend(render_scene(si - 1, t), im, eio((t - (a - XF / 2)) / XF))
    return (np.asarray(im, dtype=np.float32) + GRAIN[i % 8]).clip(0, 255).astype(np.uint8)

if __name__ == "__main__":
    if sys.argv[1] == "info":
        print("duration", DUR, "frames", int(round(DUR * FPS)))
        for s in SC: print(f"{s[0]:6.1f}-{s[1]:6.1f} {s[2]['name']:18s} {s[3]}")
    elif sys.argv[1] == "preview":
        os.makedirs(os.path.join(HERE, "pv"), exist_ok=True)
        for ts in sys.argv[2:]:
            Image.fromarray(frame(int(round(float(ts) * FPS)))).save(os.path.join(HERE, "pv", f"t{float(ts):06.2f}.png"))
    else:
        import subprocess
        s, e, out = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                              "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "14",
                              "-pix_fmt", "yuv420p", "-g", "60", out], stdin=subprocess.PIPE)
        for i in range(s, e): p.stdin.write(frame(i).tobytes())
        p.stdin.close(); p.wait(); print("DONE", out, flush=True)
