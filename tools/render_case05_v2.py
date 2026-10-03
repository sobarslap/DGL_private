"""Dogetlawyer Case File 05 v2 - liability caps, side-by-side, conversational.
Usage: python3 render.py preview T1 T2 ...  -> PNG stills
       python3 render.py chunk START END OUT.mp4  -> frames [START, END)
"""
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FD = os.path.join(HERE, "f")
W, H, FPS = 1080, 1920, 30
DUR = 105.0
M = 84
CW = W - 2 * M
XF = 0.30

def hexc(h):
    h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def mix(a, b, t):
    return tuple(int(round(x + (y - x) * t)) for x, y in zip(a, b))

def cl(x): return 0.0 if x < 0 else (1.0 if x > 1 else x)
def eio(x): x = cl(x); return x * x * (3 - 2 * x)

PLUM, BLUSH = hexc("#241528"), hexc("#F2E8EC")
DARK = dict(bg=PLUM, fg=hexc("#F0E4E8"), acc=hexc("#E86A8A"))
LIGHT = dict(bg=BLUSH, fg=hexc("#221326"), acc=hexc("#A8325C"))
for T in (DARK, LIGHT):
    T["mut"] = mix(T["bg"], T["fg"], 0.62)
    T["dim"] = mix(T["bg"], T["fg"], 0.45)
    T["line"] = mix(T["bg"], T["fg"], 0.12)
    T["panel"] = mix(T["bg"], T["fg"], 0.07)
    T["edge"] = mix(T["bg"], T["fg"], 0.20)

_fc = {}
def F(name, size):
    k = (name, size)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(os.path.join(FD, name + ".ttf"), size)
    return _fc[k]

ANTON = "Anton_400Regular"; INTER = "Inter_500Medium"; INTER_SB = "Inter_600SemiBold"
INTER_B = "Inter_700Bold"; MONO = "JetBrainsMono_500Medium"; MONO_B = "JetBrainsMono_700Bold"
SERIF_I = "EBGaramond_500Medium_Italic"

def tw(f, s, tr=0):
    return f.getlength(s) + tr * max(0, len(s) - 1)

def text(d, x, y, s, f, c, tr=0, align="l"):
    w = tw(f, s, tr)
    if align == "c": x = x - w / 2
    elif align == "r": x = x - w
    if tr == 0:
        d.text((x, y), s, font=f, fill=c); return w
    for ch in s:
        d.text((x, y), ch, font=f, fill=c); x += f.getlength(ch) + tr
    return w

def wrap(f, s, maxw):
    out, cur = [], ""
    for wd in s.split(" "):
        t = (cur + " " + wd).strip()
        if tw(f, t) <= maxw or not cur: cur = t
        else: out.append(cur); cur = wd
    if cur: out.append(cur)
    return out

# ---------------------------------------------------------------- frame ctx
class Ctx:
    """Drawing context for one scene at local time u; colours fade from bg."""
    def __init__(self, im, T, u):
        self.d = ImageDraw.Draw(im); self.T = T; self.u = u
    def a(self, t0, dur=0.45):
        return eio((self.u - t0) / dur)
    def c(self, role, alpha):
        col = self.T[role] if isinstance(role, str) else role
        return mix(self.T["bg"], col, alpha)
    def head(self, lines, y, size, t0, role="fg", gap=0.18, align="l", maxw=CW, stag=0.22, x=None):
        f = F(ANTON, size)
        while max(tw(f, ln, 1) for ln in lines) > maxw and size > 40:
            size -= 4; f = F(ANTON, size)
        bb = f.getbbox("H"); top, ch = bb[1], bb[3] - bb[1]
        lh = int(ch * (1 + gap))
        x = (M if align == "l" else W / 2) if x is None else x
        for i, ln in enumerate(lines):
            al = self.a(t0 + i * stag)
            if al <= 0: continue
            r = role[i] if isinstance(role, list) else role
            text(self.d, x, y + i * lh - top, ln, f, self.c(r, al), tr=1, align=align)
        return y + (len(lines) - 1) * lh + ch
    def para(self, s, y, size, t0, role="mut", fname=INTER, maxw=CW, lead=1.34, align="l", x=None):
        f = F(fname, size); lines = wrap(f, s, maxw); al = self.a(t0)
        x = (M if align == "l" else W / 2) if x is None else x
        for i, ln in enumerate(lines):
            if al > 0: text(self.d, x, y + i * int(size * lead), ln, f, self.c(role, al), align=align)
        return y + len(lines) * int(size * lead)
    def mono(self, s, x, y, size, t0, role="dim", tr=2, align="l", fname=MONO):
        al = self.a(t0)
        if al > 0: text(self.d, x, y, s, F(fname, size), self.c(role, al), tr=tr, align=align)
    def box(self, x0, y0, x1, y1, t0, fill="panel", edge="edge", r=18, w=2):
        al = self.a(t0)
        if al <= 0: return
        self.d.rounded_rectangle([x0, y0, x1, y1], radius=r, fill=self.c(fill, al),
                                 outline=self.c(edge, al) if edge else None, width=w)
    def rule(self, x0, y, x1, t0, role="acc", w=6):
        al = self.a(t0)
        if al > 0: self.d.rectangle([x0, y, x1, y + w - 1], fill=self.c(role, al))
    def chip(self, s, x, y, t0, size=24, fill="acc", tcol="bg"):
        al = self.a(t0)
        if al <= 0: return
        f = F(MONO_B, size); w = tw(f, s, 2) + 40
        self.d.rounded_rectangle([x, y, x + w, y + size + 26], radius=(size + 26) // 2, fill=self.c(fill, al))
        text(self.d, x + 20, y + 11, s, f, self.c(tcol, al) if tcol != "bg" else mix(self.c(fill, al), self.T["bg"], 1.0), tr=2)
        return w

# ---------------------------------------------------------------- scenes
# Each scene: (start, end, theme, act label, demo flag, vo lines, draw fn)
def s1(c):
    c.mono("A QUICK QUESTION", M, 520, 26, 0.1)
    yb = c.head(["SIGNED IT", "WITHOUT", "READING IT?"], 600, 210, 0.25, role=["fg", "fg", "acc"])
    c.para("Your supplier's terms. The bit nobody reads.", yb + 70, 44, 1.5, role="mut", fname=SERIF_I)

def s2(c):
    c.mono("SUPPLIER TERMS · PAGE 7 OF 9", M, 420, 26, 0.1)
    c.box(M, 480, W - M, 1060, 0.2)
    c.mono("11.  LIMITATION OF LIABILITY", M + 48, 530, 28, 0.35, role="dim")
    c.para("11.3  Our total liability under this agreement shall not exceed the charges paid by you "
           "in the three months before the claim arose.", 600, 46, 0.5, role="fg", maxw=CW - 96, x=M + 48, lead=1.32)
    c.rule(M + 48, 990, M + 360, 1.6, w=8)
    c.mono("THE LIABILITY CAP", M + 48, 1012, 26, 1.7, role="acc")
    c.head(["IT CAPS WHAT", "THEY'LL PAY YOU."], 1170, 120, 2.2)

def s3(c):
    c.mono("IF IT ALL GOES WRONG", M, 440, 26, 0.1)
    c.mono("THEIR CAP", M, 520, 30, 0.2, role="mut")
    c.head(["£3,900"], 570, 250, 0.35)
    c.mono("YOUR LOSS", M, 900, 30, 1.6, role="mut")
    c.head(["£58,400"], 950, 250, 1.75, role="acc")
    c.para("Fifteen times what they'd pay out.", 1290, 44, 2.8, role="mut", fname=SERIF_I)

def split(c, t0, left, right, y0=600, rowh=120, lt="HARLOW BRIDGE", rt="CALDEW", tstag=0.5, sub=None):
    mid = W // 2
    c.box(M, y0, mid - 14, y0 + 110 + rowh * len(left), t0)
    c.box(mid + 14, y0, W - M, y0 + 110 + rowh * len(right), t0)
    c.mono(lt, M + 34, y0 + 36, 26, t0 + 0.1, role="fg", fname=MONO_B)
    c.mono(rt, mid + 48, y0 + 36, 26, t0 + 0.1, role="fg", fname=MONO_B)
    for i, (l, r) in enumerate(zip(left, right)):
        tt = t0 + 0.4 + i * tstag
        y = y0 + 110 + i * rowh
        for (s, x, role) in ((l, M + 34, "mut"), (r, mid + 48, "fg")):
            c.para(s, y, 36, tt, role=role, maxw=mid - M - 80, x=x, lead=1.25)

def s4(c):
    c.mono("LET'S RUN IT TWICE", M, 380, 26, 0.1)
    c.head(["TWO FIRMS.", "SAME SUPPLIER.", "SAME TERMS."], 440, 150, 0.2)
    split(c, 1.4, ["Joinery workshop, Midlands", "Bought the same machine"],
          ["Fabrication firm, North East", "Bought the same machine"], y0=1010, rowh=110)

def s5(c):
    c.mono("SIX WEEKS LATER", M, 380, 26, 0.1)
    c.head(["IT PACKS UP.", "SAME LETTER", "TO BOTH."], 440, 160, 0.2, role=["fg", "acc", "acc"])
    c.box(M, 1020, W - M, 1340, 1.5)
    c.mono("FROM: MERETON SYSTEMS LTD", M + 44, 1060, 24, 1.6)
    c.para("“We refer you to clause 11.3. Our liability is limited to £3,900.”", 1120, 46, 1.8,
           role="fg", fname=SERIF_I, maxw=CW - 88, x=M + 44)

def s6(c):
    c.mono("WHAT THEY DID NEXT", M, 380, 26, 0.1)
    mid = W // 2
    c.box(M, 470, mid - 14, 1230, 0.2); c.box(mid + 14, 470, W - M, 1230, 0.2)
    c.mono("HARLOW BRIDGE", M + 34, 510, 26, 0.3, role="fg", fname=MONO_B)
    c.mono("CALDEW", mid + 48, 510, 26, 0.3, role="fg", fname=MONO_B)
    c.head(["TAKES", "THE", "£3,900."], 620, 150, 0.6, maxw=mid - M - 80, align="l")
    c.head(["PUSHES", "BACK."], 620, 150, 1.6, role="acc", maxw=mid - M - 80, x=mid + 48)
    c.para("Same clause. Different move.", 1300, 44, 2.6, role="mut", fname=SERIF_I)

def s7(c):
    c.mono("THE BIT MOST PEOPLE DON'T KNOW", M, 460, 26, 0.1)
    c.head(["A CAP ISN'T", "AUTOMATICALLY", "THE END OF IT."], 540, 170, 0.25, role=["fg", "fg", "acc"])

def law(c, kicker, lines, sub, src, roles=None):
    c.mono(kicker, M, 400, 26, 0.1)
    yb = c.head(lines, 470, 160, 0.25, role=roles or "fg")
    yb = c.para(sub, yb + 60, 46, 1.3, role="mut")
    c.rule(M, yb + 40, M + 120, 1.9, w=4)
    c.mono(src, M, yb + 64, 24, 2.0)

def s8(c):
    law(c, "ON THEIR STANDARD TERMS", ["IT HAS TO BE", "REASONABLE."],
        "And it's the supplier who has to prove that. Not you.",
        "UNFAIR CONTRACT TERMS ACT 1977 · s.3 · s.11(5)", ["fg", "acc"])

def s9(c):
    law(c, "AND HERE'S THE KICKER", ["JUDGED ON THE", "DAY YOU SIGNED."],
        "Not on the day it broke. What did everyone know back then?",
        "UCTA 1977 · s.11(1)", ["fg", "acc"])

def s10(c):
    c.mono("WHAT COURTS TEND TO LOOK AT", M, 400, 26, 0.1)
    c.head(["WHO HAD", "THE CLOUT?"], 460, 160, 0.2, role=["fg", "acc"])
    items = ["Who had more bargaining power", "Could you have gone elsewhere?",
             "Did you know the clause was there?", "How you've dealt with each other before"]
    y = 860
    for i, s in enumerate(items):
        tt = 0.9 + i * 0.55
        c.box(M, y, W - M, y + 112, tt, r=14)
        c.mono(f"0{i + 1}", M + 32, y + 38, 28, tt + 0.1, role="acc", fname=MONO_B)
        c.para(s, y + 32, 40, tt + 0.1, role="fg", x=M + 110, maxw=CW - 140)
        y += 132
    c.mono("UCTA 1977 · s.11 & SCHEDULE 2 FACTORS", M, y + 24, 24, 3.2)

def s11(c):
    c.mono("TO BE FAIR", M, 460, 26, 0.1)
    c.head(["LOADS OF CAPS", "ARE FAIR.", "AND THEY HOLD."], 540, 160, 0.25)
    c.mono("GENERAL POSITION — OUTCOMES TURN ON THE FACTS", M, 1100, 24, 1.4, role="acc")

def s12(c):
    c.head(["BUT YOU CAN", "ONLY ARGUE", "WHAT YOU", "CAN SHOW."], 480, 170, 0.15, role=["fg", "fg", "acc", "acc"])

def s13(c):
    c.mono("WHAT EACH ONE COULD SHOW", M, 360, 26, 0.1)
    c.head(["THE PAPER", "TRAIL."], 410, 150, 0.2)
    split(c, 0.9, ["Terms agreed on a phone call", "Quote lost in someone's inbox", "No idea which version"],
          ["Signed terms, version 4.2", "Emails saying what it was for", "11 past orders, all dated"],
          y0=760, rowh=150, tstag=0.75)

def s14(c):
    c.head(["SAME CLAUSE.", "SAME SUPPLIER."], 500, 160, 0.15)
    c.head(["ONLY ONE HAD", "A CASE TO MAKE."], 900, 160, 1.4, role="acc")

def s15(c):
    c.mono("AND IF IT ENDS UP IN COURT", M, 440, 26, 0.1)
    c.head(["41 WEEKS"], 520, 260, 0.3, role="acc")
    c.para("Typical wait for a small claim to get to trial.", 860, 46, 1.2, role="fg")
    c.para("Nobody wants to be there. Which is the point.", 1010, 44, 2.2, role="mut", fname=SERIF_I)
    c.mono("SOURCE: MINISTRY OF JUSTICE, APR–JUN 2026 (MEDIAN)", M, 1160, 22, 2.6)

def win(c, t0, title, y0, y1):
    c.box(M, y0, W - M, y1, t0, r=20)
    al = c.a(t0)
    if al > 0:
        c.d.rounded_rectangle([M, y0, W - M, y0 + 70], radius=20, fill=c.c("edge", al * 0.7))
        c.d.rectangle([M, y0 + 50, W - M, y0 + 70], fill=c.c("edge", al * 0.7))
        for k in range(3):
            c.d.ellipse([M + 28 + k * 30, y0 + 26, M + 46 + k * 30, y0 + 44], fill=c.c("dim", al))
        text(c.d, M + 140, y0 + 22, title, F(MONO, 24), c.c("fg", al), tr=2)

def s16(c):
    c.mono("THAT'S WHAT DOGETLAWYER IS FOR", M, 330, 26, 0.1, role="acc")
    win(c, 0.3, "LIABILITY CAPS · ALL SUPPLIERS", 400, 1060)
    rows = [("Mereton Systems Ltd", "£3,900", "3 months' charges"),
            ("Brayfield Plant Hire", "£25,000", "fixed sum"),
            ("Ivelet Logistics Ltd", "Price paid", "per consignment")]
    y = 520
    for i, (n, v, b) in enumerate(rows):
        tt = 0.8 + i * 0.5
        c.para(n, y, 40, tt, role="fg", x=M + 40)
        c.para(v, y, 40, tt, role="acc", fname=INTER_B, x=W - M - 40 - tw(F(INTER_B, 40), v))
        c.mono(b.upper(), M + 40, y + 62, 22, tt, role="dim")
        if i < 2: c.rule(M + 40, y + 120, W - M - 40, tt, role="line", w=2)
        y += 170
    c.para("Every supplier. The cap buried in their terms, pulled out where you can see it.",
           1110, 42, 2.2, role="mut", fname=SERIF_I)

def s17(c):
    c.mono("OPEN ONE UP", M, 330, 26, 0.1, role="acc")
    win(c, 0.2, "MERETON SYSTEMS LTD · CONTRACT", 400, 1180)
    rows = [("TERMS", "Version 4.2 — attached"), ("SENT", "14 May 2026, 09:12"),
            ("SIGNED", "16 May 2026"), ("CLAUSE 11.3", "Liability cap — flagged"),
            ("PAST ORDERS", "11, all on these terms")]
    y = 510
    for i, (k, v) in enumerate(rows):
        tt = 0.6 + i * 0.45
        c.mono(k, M + 40, y + 8, 24, tt)
        c.para(v, y, 40, tt, role="acc" if k.startswith("CLAUSE") else "fg", x=M + 330, maxw=CW - 380)
        if i < len(rows) - 1: c.rule(M + 40, y + 108, W - M - 40, tt, role="line", w=2)
        y += 128
    c.head(["YOUR PAPER TRAIL,", "SORTED."], 1250, 110, 3.0, role=["fg", "acc"])

def s18(c):
    c.mono("DO ONE THING THIS WEEK", M, 440, 26, 0.1)
    c.head(["FIND THE CAP", "IN YOUR 3", "BIGGEST", "CONTRACTS."], 520, 165, 0.25, role=["fg", "acc", "acc", "acc"])

def s19(c):
    c.head(["DOGETLAWYER"], 560, 120, 0.1, role="acc", align="c")
    c.head(["KNOW WHAT YOUR", "CONTRACTS CAP."], 760, 140, 0.4, align="c")
    c.para("Every supplier. Every limit. One place.", 1110, 44, 0.9, role="mut", align="c", fname=SERIF_I)
    c.para("dogetlawyer.com", 1210, 40, 1.1, role="fg", fname=INTER_SB, align="c")
    c.para("Contract management software for UK small businesses — not a substitute for legal advice.",
           1340, 30, 1.4, role="mut", align="c", maxw=CW - 40)
    c.para("All names, figures and documents shown are fictional examples.", 1430, 26, 1.5, role="dim", align="c")

A1, A2, A3, A4, A5, A6 = ("01 — THE SMALL PRINT", "02 — TWO FIRMS", "03 — WHAT THE LAW SAYS",
                          "04 — WHO COULD SHOW IT", "05 — THE RECORD", "06 — YOUR MOVE")
SCENES = [
    (0.0, 4.6, DARK, A1, False, ["Signed a supplier's terms without reading the small print?",
                                  "Yeah. Most of us have."], s1),
    (4.6, 10.4, DARK, A1, True, ["Somewhere in there is a line like this.",
                                  "It caps what they'll pay you if it all goes wrong."], s2),
    (10.4, 15.6, DARK, A1, True, ["Here, that's three thousand nine hundred quid.",
                                   "Your loss? Fifty-eight grand."], s3),
    (15.6, 21.6, LIGHT, A2, True, ["So let's run it twice.",
                                    "Two firms. Same supplier, same machine, same terms."], s4),
    (21.6, 27.4, LIGHT, A2, True, ["Six weeks in, it packs up. Both lose a whole batch.",
                                    "Both get the exact same letter."], s5),
    (27.4, 32.6, LIGHT, A2, True, ["One shrugs and takes the three thousand nine hundred.",
                                    "The other pushes back."], s6),
    (32.6, 37.2, DARK, A3, False, ["Here's the bit most people don't know.",
                                    "A cap like that isn't automatically the end of it."], s7),
    (37.2, 43.6, DARK, A3, False, ["On their standard terms, it has to be reasonable.",
                                    "And it's the supplier who has to prove that. Not you."], s8),
    (43.6, 49.2, DARK, A3, False, ["And reasonable is judged on what everyone knew when you signed.",
                                    "Not on the day it broke."], s9),
    (49.2, 56.4, DARK, A3, False, ["Courts look at who had the clout, and whether you could've gone elsewhere.",
                                    "Whether you knew the clause was there. And how you've dealt before."], s10),
    (56.4, 60.6, DARK, A3, False, ["Mind you, loads of caps are perfectly fair.", "They hold up."], s11),
    (60.6, 64.4, DARK, A3, False, ["But you can only argue what you can actually show."], s12),
    (64.4, 72.8, LIGHT, A4, True, ["So, what could each of them show?",
                                    "One had a phone call and a quote lost in someone's inbox.",
                                    "The other had the signed terms, the emails, and eleven past orders."], s13),
    (72.8, 77.6, LIGHT, A4, False, ["Same clause. Same supplier.", "Only one had a case to make."], s14),
    (77.6, 83.0, LIGHT, A4, False, ["And honestly? Nobody wants this in court.",
                                     "A small claim takes around forty-one weeks to reach trial."], s15),
    (83.0, 89.4, DARK, A5, True, ["That's what Dogetlawyer's for.",
                                   "Every supplier, and the cap buried in their terms, where you can see it."], s16),
    (89.4, 95.6, DARK, A5, True, ["Open one up: which version you signed, when, and the clause flagged.",
                                   "Your paper trail, sorted."], s17),
    (95.6, 100.6, LIGHT, A6, False, ["Do one thing this week.",
                                      "Find the liability cap in your three biggest supplier contracts."], s18),
    (100.6, 105.0, DARK, A6, False, ["Send this to whoever signs your supplier terms."], s19),
]

# ---------------------------------------------------------------- captions
def caption_at(si, u):
    a, b, _, _, _, vo, _ = SCENES[si]
    dur = b - a - 0.5
    tot = sum(len(s) for s in vo)
    t = 0.2
    for s in vo:
        d = dur * len(s) / tot
        if t <= u < t + d: return s, cl((u - t) / 0.2) * cl((t + d - u) / 0.2)
        t += d
    return None, 0

def draw_caption(d, T, s, al):
    if not s or al <= 0: return
    f = F(INTER_SB, 44)
    lines = wrap(f, s, CW - 60)
    y0 = 1560 - (len(lines) - 1) * 30
    for i, ln in enumerate(lines):
        text(d, W / 2, y0 + i * 60, ln, f, mix(T["bg"], T["fg"], al), align="c")

# ---------------------------------------------------------------- base
def build_bg(T):
    im = Image.new("RGB", (W, H), T["bg"]); d = ImageDraw.Draw(im)
    ln = mix(T["bg"], T["fg"], 0.045); ln2 = mix(T["bg"], T["fg"], 0.08)
    d.rectangle([W // 2, 0, W // 2 + 1, H], fill=ln2)
    for x in (M, W - M): d.rectangle([x, 0, x, H], fill=ln)
    for y in range(240, H, 96): d.rectangle([0, y, W, y], fill=ln)
    return im

BG = {id(DARK): build_bg(DARK), id(LIGHT): build_bg(LIGHT)}
rng = np.random.default_rng(5)
GRAIN = []
for _ in range(8):
    g = rng.normal(0, 1, (H // 4, W // 4)).astype(np.float32)
    g = np.array(Image.fromarray(((g * 40) + 128).clip(0, 255).astype(np.uint8)).resize((W, H), Image.BICUBIC),
                 dtype=np.float32) - 128
    GRAIN.append((g * 0.10)[..., None])

def chrome(d, T, act, demo, sidx):
    f = F(MONO_B, 24)
    text(d, M, 96, "DOGETLAWYER", f, T["acc"], tr=3)
    text(d, W - M, 96, "CASE FILE № 05", F(MONO, 24), T["dim"], tr=3, align="r")
    fc = F(MONO_B, 22); w = tw(fc, act, 2) + 44
    d.rounded_rectangle([M, 150, M + w, 198], radius=24, fill=T["acc"])
    text(d, M + 22, 161, act, fc, T["bg"], tr=2)
    d.rectangle([M, 1490, W - M, 1491], fill=T["line"])
    if demo:
        text(d, M, 1820, "FICTIONAL DEMO EXAMPLE", F(MONO, 22), T["dim"], tr=2)
    text(d, W - M, 1820, "dogetlawyer.com", F(MONO, 22), T["dim"], tr=1, align="r")

def render_scene(si, t):
    a, b, T, act, demo, vo, fn = SCENES[si]
    im = BG[id(T)].copy()
    c = Ctx(im, T, t - a)
    fn(c)
    chrome(c.d, T, act, demo, si)
    s, al = caption_at(si, t - a)
    draw_caption(c.d, T, s, al)
    return im

def scene_index(t):
    si = 0
    for k, sc in enumerate(SCENES):
        if t >= sc[0]: si = k
    return si

def frame(i):
    t = i / FPS
    si = scene_index(t); a, b = SCENES[si][0], SCENES[si][1]
    im = render_scene(si, t)
    if si + 1 < len(SCENES) and t > b - XF / 2:
        im = Image.blend(im, render_scene(si + 1, t), eio((t - (b - XF / 2)) / XF))
    elif si > 0 and t < a + XF / 2:
        im = Image.blend(render_scene(si - 1, t), im, eio((t - (a - XF / 2)) / XF))
    arr = np.asarray(im, dtype=np.float32) + GRAIN[i % len(GRAIN)]
    return arr.clip(0, 255).astype(np.uint8)

if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "preview":
        os.makedirs(os.path.join(HERE, "pv"), exist_ok=True)
        for ts in sys.argv[2:]:
            i = int(round(float(ts) * FPS))
            Image.fromarray(frame(i)).save(os.path.join(HERE, "pv", f"t{float(ts):06.2f}.png"))
    elif mode == "chunk":
        import subprocess
        s, e, out = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                              "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium",
                              "-crf", "14", "-pix_fmt", "yuv420p", "-g", "60", out], stdin=subprocess.PIPE)
        for i in range(s, e):
            p.stdin.write(frame(i).tobytes())
            if (i - s) % 150 == 0: print(out, i, flush=True)
        p.stdin.close(); p.wait(); print("DONE", out, flush=True)
