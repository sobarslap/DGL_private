"""Dogetlawyer Case File 07 - "We're updating our terms". Timeline format, multi-colour scenes (boss brief:
slide 1 purple+black, slide 2 grey+red, slide 3 sky blue, then other combinations).
Type: Oswald / Manrope / Space Mono / Lora italic.
Usage: python3 render7.py preview T...  |  python3 render7.py chunk START END OUT.mp4
"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); FD = os.path.join(HERE, "f")
sys.path.insert(0, os.path.join(HERE, ".."))
from multitheme import THEMES, gradient, hexc, mix

W, H, FPS, M = 1080, 1920, 30, 84
CW = W - 2 * M; XF = 0.30
def cl(x): return 0.0 if x < 0 else (1.0 if x > 1 else x)
def eio(x): x = cl(x); return x * x * (3 - 2 * x)
_fc = {}
def F(n, s):
    if (n, s) not in _fc: _fc[(n, s)] = ImageFont.truetype(os.path.join(FD, n + ".ttf"), s)
    return _fc[(n, s)]
HEAD = "Oswald_700Bold"; BODY = "Manrope_600SemiBold"; BODY_B = "Manrope_800ExtraBold"
MONO = "SpaceMono_400Regular"; MONO_B = "SpaceMono_700Bold"; SERIF = "Lora_500Medium_Italic"; CAP = "Manrope_700Bold"
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

# ---------------------------------------------------------------- scenes
def s1(c):
    c.mono("NEW EMAIL", M, 420, 28, 0.0)
    c.head(["“WE’RE UPDATING", "OUR TERMS AND", "CONDITIONS.”"], 490, 150, 0.1)
    c.para("You didn’t read it. Nobody does.", 1040, 52, 1.3, role="acc", fn=SERIF)

def s2(c):
    c.mono("BUT THAT EMAIL MIGHT HAVE JUST", M, 470, 28, 0.0)
    c.head(["PUT YOUR", "PRICES UP", "18%."], 540, 200, 0.15, role=["fg", "fg", "acc"])
    c.mono("FICTIONAL EXAMPLE", M, 1240, 22, 1.2)

def s3(c):
    c.mono("LET’S RUN THE CLOCK", M, 520, 28, 0.0)
    c.head(["HOW A “QUICK", "UPDATE” PLAYS", "OUT."], 590, 150, 0.15, role=["fg", "fg", "acc"])

def s4(c):
    spine(c, "DAY 1", "THE EMAIL LANDS")
    email(c, 580, 0.3, "Important: changes to our terms and conditions",
          ["We’re making some changes to our terms of business, effective 1 November.",
           "Continued use of our services means you accept the new terms."])

def s5(c):
    spine(c, "DAY 2", "BUSY WEEK")
    c.head(["YOU ARCHIVE IT."], 640, 150, 0.2)
    c.para("Same as every other “we’re updating our terms” email.", 820, 44, 1.0, role="mut", fn=SERIF)

def s6(c):
    spine(c, "DAY 30", "THE NEW TERMS KICK IN")
    c.head(["WHAT QUIETLY", "CHANGED:"], 600, 120, 0.2)
    items = [("Prices", "now reviewed every quarter"), ("Notice period", "60 days → 90 days"), ("Liability cap", "halved")]
    y = 900
    for i, (k, v) in enumerate(items):
        tt = 0.9 + i * 0.5
        c.box(M + 60, y, W - M, y + 118, tt, r=16)
        c.para(k, y + 34, 38, tt, role="fg", fn=BODY_B, x=M + 96)
        c.para(v, y + 36, 34, tt, role="acc", fn=BODY_B, x=W - M - 36 - tw(F(BODY_B, 34), v))
        y += 138

def s7(c):
    spine(c, "DAY 31–90", "BUSINESS AS USUAL")
    c.head(["YOU KEEP", "ORDERING."], 640, 170, 0.2)
    c.para("Same supplier. Same products. No idea anything changed.", 1000, 44, 1.0, role="mut", fn=SERIF)

def s8(c):
    spine(c, "DAY 91", "THE INVOICE")
    al = c.a(0.3)
    if al > 0:
        y0 = 620; c.d.rounded_rectangle([M + 60, y0, W - M, y0 + 420], radius=22, fill=c.c(PAPER, al))
        text(c.d, M + 100, y0 + 40, "INVOICE 2291 · HARROW PRINT", F(MONO, 26), c.c(GREYTXT, al), tr=1)
        text(c.d, M + 100, y0 + 110, "Last quarter", F(BODY, 38), c.c(GREYTXT, al))
        text(c.d, W - M - 40, y0 + 110, "£4,000", F(BODY_B, 38), c.c(GREYTXT, al), align="r")
        text(c.d, M + 100, y0 + 190, "This quarter", F(BODY_B, 44), c.c(INK, al))
        text(c.d, W - M - 40, y0 + 182, "£4,720", F(BODY_B, 56), c.c(RED, al), align="r")
        a2 = c.a(1.4)
        if a2 > 0:
            c.d.rounded_rectangle([M + 100, y0 + 300, M + 300, y0 + 372], radius=36, fill=c.c(RED, a2))
            text(c.d, M + 200, y0 + 310, "+18%", F(HEAD, 48), c.c(PAPER, a2), align="c")
    c.mono("FICTIONAL DEMO EXAMPLE", M + 60, 1080, 22, 0.5)

def s9(c):
    spine(c, "DAY 92", "YOU PUSH BACK")
    c.head(["THEY SEND YOU…", "THE EMAIL FROM", "DAY ONE."], 620, 130, 0.2, role=["fg", "fg", "acc"])

def s10(c):
    c.mono("THE BIG QUESTION", M, 520, 28, 0.0)
    c.head(["CAN A SUPPLIER", "JUST CHANGE", "THE TERMS", "ON YOU?"], 590, 150, 0.15, role=["fg", "fg", "fg", "acc"])

def s11(c):
    c.mono("USUALLY…", M, 470, 28, 0.0)
    yb = c.head(["ONLY IF THE", "CONTRACT", "LETS THEM."], 540, 160, 0.15, role=["fg", "fg", "acc"])
    c.para("Look for a “variation clause”: the bit that says they can change the terms, and how much notice they must give.", yb + 60, 42, 1.3, role="mut")

def s12(c):
    c.mono("AND HERE’S THE CATCH", M, 430, 28, 0.0)
    c.head(["SAYING NOTHING", "ISN’T ALWAYS", "AGREEING…"], 500, 140, 0.15)
    c.head(["…BUT CARRYING", "ON CAN BE."], 960, 140, 1.5, role="acc")
    c.mono("GENERAL POSITION, ENGLAND & WALES · OUTCOMES TURN ON THE FACTS", M, 1300, 20, 2.3, tr=1)

def s13(c):
    c.mono("REWIND TO DAY 1. DO THIS:", M, 380, 28, 0.0)
    steps = [("01", "Don’t archive it.", "Read what’s changing: price, notice, liability."),
             ("02", "Disagree? Say so in writing.", "Before the new terms start."),
             ("03", "Diary the start date.", "And who’s dealing with it.")]
    y = 470
    for i, (n, h, sub) in enumerate(steps):
        tt = 0.3 + i * 1.6
        c.box(M, y, W - M, y + 260, tt, r=22)
        c.mono(n, M + 40, y + 40, 40, tt, role="acc", fn=MONO_B)
        c.para(h, y + 34, 50, tt, role="fg", fn=BODY_B, x=M + 150, maxw=CW - 190)
        c.para(sub, y + 150, 36, tt + 0.2, role="mut", x=M + 150, maxw=CW - 190)
        y += 290

def win(c, t0, title, y0, y1):
    c.box(M, y0, W - M, y1, t0, r=20); al = c.a(t0)
    if al > 0:
        c.d.rounded_rectangle([M, y0, W - M, y0 + 70], radius=20, fill=c.c("edge", al))
        c.d.rectangle([M, y0 + 50, W - M, y0 + 70], fill=c.c("edge", al))
        for k in range(3): c.d.ellipse([M + 28 + k * 30, y0 + 26, M + 46 + k * 30, y0 + 44], fill=c.c("dim", al))
        text(c.d, M + 140, y0 + 20, title, F(MONO, 24), c.c("fg", al), tr=1)

def s14(c):
    c.mono("THAT’S WHAT DOGETLAWYER IS FOR", M, 330, 26, 0.0, role="acc")
    win(c, 0.2, "TERMS CHANGES · ALL SUPPLIERS", 400, 1170)
    rows = [("Harrow Print Supplies", "New terms 1 Nov", "Price review clause · notice 60 → 90 days", "acc"),
            ("Kestrel Fleet Hire", "Version 3 on file", "Liability cap unchanged", "fg"),
            ("Norbury Packaging", "No change", "Original terms, signed 2025", "dim")]
    y = 520
    for i, (n, v, b, r) in enumerate(rows):
        tt = 0.7 + i * 0.5
        c.para(n, y, 40, tt, role="fg", fn=BODY_B, x=M + 40)
        c.para(v, y + 2, 34, tt, role=r, fn=BODY_B, x=W - M - 40 - tw(F(BODY_B, 34), v))
        c.mono(b, M + 40, y + 62, 22, tt, tr=1)
        if i < 2: c.d.rectangle([M + 40, y + 130, W - M - 40, y + 131], fill=c.c("line", c.a(tt)))
        y += 190
    c.para("Every version of their terms on record, and the date the new ones kick in.", 1220, 42, 2.2, role="mut", fn=SERIF)

def s15(c):
    c.head(["SO DAY ONE", "NEVER SLIPS", "PAST YOU."], 580, 180, 0.0, role=["fg", "fg", "acc"])

def s16(c):
    c.mono("BE HONEST", M, 520, 28, 0.0)
    c.head(["HAD ONE OF", "THESE EMAILS", "THIS YEAR?"], 590, 150, 0.15)
    al = c.a(1.4)
    if al > 0:
        c.pill("COMMENT “TERMS” BELOW", M, 1120, 1.4, size=34)

def close(c):
    c.head(["DOGETLAWYER"], 560, 120, 0.1, role="acc", align="c")
    c.head(["KNOW WHEN YOUR", "TERMS CHANGE."], 760, 130, 0.4, align="c")
    c.para("Every supplier. Every version. One place.", 1060, 42, 0.9, role="mut", align="c", fn=SERIF)
    c.para("dogetlawyer.com", 1140, 44, 0.9, role="fg", fn=BODY_B, align="c")
    al = c.a(0.8)
    if al > 0:
        f = F(MONO_B, 30); w = tw(f, "LINK IN BIO", 3) + 60
        c.d.rounded_rectangle([W / 2 - w / 2, 1210, W / 2 + w / 2, 1270], radius=30, fill=c.c("acc", al))
        text(c.d, W / 2, 1222, "LINK IN BIO", f, c.c("bg", al), tr=3, align="c")
    c.para("Contract management software for UK small businesses — not a substitute for legal advice.", 1320, 30, 1.4, role="mut", align="c", maxw=CW - 40)
    c.para("All names, figures and documents shown are fictional examples.", 1410, 26, 1.5, role="dim", align="c")

SCENES = [
    (3.6, "THE EMAIL", False, ["Got an email saying, we’re updating our terms and conditions?", "Course you didn’t read it. Nobody does."], s1),
    (4.0, "THE EMAIL", False, ["But that email might have just put your prices up eighteen percent."], s2),
    (3.4, "THE TIMELINE", False, ["Let’s run the clock on how a quick update plays out."], s3),
    (7.0, "DAY 1", True, ["Day one. The email lands. Important changes to our terms and conditions.", "Continued use of our services means you accept the new terms."], s4),
    (4.4, "DAY 2", False, ["Day two. Busy week. You archive it.", "Same as every other one."], s5),
    (7.2, "DAY 30", True, ["Day thirty. The new terms kick in. Prices now reviewed every quarter.", "Your notice period goes from sixty days to ninety. The liability cap, halved."], s6),
    (5.0, "DAY 31–90", False, ["You keep ordering, same as always.", "No idea anything changed."], s7),
    (6.2, "DAY 91", True, ["Day ninety-one. The invoice lands. Four grand last quarter.", "Four thousand seven hundred and twenty this time. Up eighteen percent."], s8),
    (5.0, "DAY 92", False, ["You push back. And they send you the email from day one."], s9),
    (4.2, "THE LAW", False, ["So, can a supplier just change the terms on you?"], s10),
    (8.2, "THE LAW", False, ["Usually, only if the contract lets them. That's a variation clause.", "It says they can change the terms, and how much notice they have to give."], s11),
    (8.6, "THE LAW", False, ["And here's the catch. Saying nothing isn't always agreeing.", "But carrying on ordering after the new terms kick in can count as accepting them."], s12),
    (12.4, "YOUR MOVE", False, ["So rewind to day one. Don't archive it. Read what's changing: price, notice, liability.",
                               "If you don't agree, say so in writing, before the start date.", "And put that date in the diary, with a name against it."], s13),
    (9.4, "THE FIX", True, ["That's what Dogetlawyer's for. Every supplier, every version of their terms on record,",
                             "and the date the new ones kick in. So you can see what changed."], s14),
    (4.0, "THE FIX", False, ["So day one never slips past you again."], s15),
    (5.4, "YOUR TURN", False, ["Be honest. Had one of these emails this year?", "Comment terms below."], s16),
    (7.0, "DOGETLAWYER", False, ["Check what you've agreed to at dogetlawyer.com. Link in bio."], close),
]
t = 0.0; SC = []
for i, (d, lab, demo, vo, fn) in enumerate(SCENES):
    SC.append((t, t + d, THEMES[i % len(THEMES)], lab, demo, vo, fn)); t += d
DUR = t

def _bg(T):
    im = gradient(T, W, H); d = ImageDraw.Draw(im)
    ln = mix(T["bg"], T["fg"], 0.06)
    for k in range(-H, W, 120):  # faint diagonal pinstripes
        d.line([(k, H), (k + H, 0)], fill=ln, width=2)
    return im
BG = {id(T): _bg(T) for T in THEMES}
rng = np.random.default_rng(7); GRAIN = []
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
    text(d, W - M, 96, "CASE FILE 07", F(MONO, 24), T["dim"], tr=2, align="r")
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
