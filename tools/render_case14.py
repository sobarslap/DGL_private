"""Dogetlawyer Case File 14 - "Probation review: postponed. Again." Unfair dismissal after 6 months from 1 Jan 2027 (Short 06).
Retention format (engine v3): hook on frame 0 (diary with POSTPONED stamps), the answer by ~7 s, quick cuts, sound-off captions. ~1:15.
Type: League Gothic / Work Sans / Overpass Mono / Literata italic. Colour per section.
Usage: python3 render14.py info | preview T... | chunk START END OUT.mp4
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, ".."))
import numpy as np
from PIL import Image, ImageDraw
import engine3 as E
from engine3 import M, W, H, CW, F, tw, text, wrap, tick, cross, win, close_card
from multitheme import gradient, hexc, mix

SECTIONS = [
 ("Hook · navy & steel",       "#0F1C30", "#26323F", "#FFFFFF", "#FFCF3F", "#7CFFB2"),
 ("The change · burnt umber",  "#3C1B0C", "#140A06", "#FFFFFF", "#FF9966", "#8BF0BC"),
 ("3 things · teal slate",     "#0A3036", "#0B1518", "#FFFFFF", "#8BF0E0", "#8BF0E0"),
 ("Key dates · deep indigo",   "#1E1A4E", "#0C0A22", "#FFFFFF", "#B7A6FF", "#8BF0BC"),
]
MAP = [0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 0, 0]
PAPER = hexc("#FBFAF7"); INK = hexc("#1A1A1A"); GREY = hexc("#77736C"); RED = hexc("#FF3B30")

def bg(T):
    im = gradient(T, W, H); a = np.asarray(im, dtype=np.float32)
    # faint ruled diary lines
    line = np.array(T["fg"], np.float32); k = 0.03
    for y in range(260, H, 96): a[y:y + 2, :] = a[y:y + 2, :] * (1 - k) + line * k
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))

E.configure(os.path.join(HERE, "f"),
            ("LeagueGothic_400Regular", "WorkSans_500Medium", "WorkSans_800ExtraBold", "OverpassMono_400Regular", "OverpassMono_600SemiBold",
             "Literata_500Medium_Italic", "WorkSans_700Bold"),
            "CASE FILE 14", SECTIONS, MAP, bg)
E.LHK = 1.08

_ST = {}
def stamp(word, size, ang):
    k = (word, size, ang)
    if k not in _ST:
        f = F(E.HEAD, size); w = int(tw(f, word) + size * 0.7); h = int(size * 1.25)
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle([4, 4, w - 5, h - 5], radius=int(size * 0.14), outline=RED + (255,), width=max(6, size // 11))
        d.text((w / 2, h / 2), word, font=f, fill=RED + (255,), anchor="mm")
        _ST[k] = im.rotate(ang, expand=True, resample=Image.BICUBIC)
    return _ST[k]

def diary(c, y0, n_stamps=3):
    c.d.rounded_rectangle([M, y0, W - M, y0 + 470], radius=24, fill=PAPER)
    text(c.d, M + 36, y0 + 26, "DIARY · PEOPLE", F(E.MONO_B, 24), GREY)
    rows = [("Tue 4 Aug", "Probation review: Sam"), ("Thu 3 Sep", "Probation review: Sam"), ("Mon 5 Oct", "Probation review: Sam")]
    for i, (d_, t_) in enumerate(rows):
        y = y0 + 80 + i * 126
        text(c.d, M + 36, y + 20, d_, F(E.MONO, 28), GREY)
        text(c.d, M + 250, y + 14, t_, F(E.BODY_B, 38), INK)
        c.d.line([(M + 250, y + 40), (M + 250 + tw(F(E.BODY_B, 38), t_), y + 40)], fill=RED, width=5)
        if i < 2: c.d.rectangle([M + 30, y + 104, W - M - 30, y + 105], fill=hexc("#E2DED6"))
    st = stamp("POSTPONED AGAIN", 70, 8); c.im.paste(st, (W - M - st.width - 10, y0 + 300), st)

def strike_years(c, y, t0=0.0, size=260):
    """'2 YEARS' struck out, then a drawn arrow, then '6 MONTHS' (fonts lack the arrow glyph)."""
    al = c.a(t0)
    if al <= 0: return
    f = F(E.HEAD, size); s1 = "2 YEARS"
    text(c.d, M, y, s1, f, c.c("dim", al)); w1 = tw(f, s1)
    c.d.line([(M - 10, y + size * 0.55), (M + w1 + 10, y + size * 0.45)], fill=c.c(RED, al), width=14)
    ax = M + w1 + 40; ay = y + size * 0.5
    c.d.line([(ax, ay), (ax + 90, ay)], fill=c.c("fg", al), width=12)
    c.d.polygon([(ax + 90, ay - 28), (ax + 130, ay), (ax + 90, ay + 28)], fill=c.c("fg", al))
    a2 = c.a(t0 + 0.4)
    if a2 > 0: text(c.d, M, y + size * 1.02, "6 MONTHS.", F(E.HEAD, int(size * 1.2)), c.c("acc", a2))

# ---------------------------------------------------------------- scenes
def h1(c):
    diary(c, 330)
    c.head(["PROBATION REVIEW:"], 870, 170, 0.0)
    c.head(["POSTPONED. AGAIN."], 1060, 170, 0.0, role="acc")

def h2(c):
    c.mono("FROM 1 JANUARY 2027 · UNFAIR DISMISSAL", M, 320, 28, 0.0, role="acc", fn=E.MONO_B)
    c.head(["THEY CAN CLAIM AFTER"], 380, 140, 0.0)
    strike_years(c, 560, 0.2)

def h3(c):
    c.head(["AND YOUR", "PROBATION", "CLAUSE WON’T", "CHANGE THAT."], 400, 200, 0.0, role=["fg", "fg", "fg", "acc"], stag=0.12)

def s4(c):
    c.mono("THE GOVERNMENT’S OWN WORDS", M, 320, 26, 0.0, role="acc", fn=E.MONO_B)
    al = c.a(0.2)
    if al > 0:
        y0 = 390
        c.d.rounded_rectangle([M, y0, W - M, y0 + 400], radius=24, fill=c.c(PAPER, al))
        c.d.rectangle([M, y0, M + 14, y0 + 400], fill=c.c("acc", al))
        y = y0 + 50
        for l in wrap(F(E.SERIF, 50), "“the qualifying period for protection against ‘ordinary’ unfair dismissal will be reduced from 2 years to 6 months”", CW - 100):
            text(c.d, M + 56, y, l, F(E.SERIF, 50), c.c(INK, al)); y += 68
    c.mono("SOURCE: BUSINESS.GOV.UK · UNFAIR DISMISSAL RIGHTS", M, 830, 22, 0.6)
    c.mono("FOR DISMISSALS FROM 1 JANUARY 2027 · ENGLAND, SCOTLAND & WALES", M, 866, 22, 0.6)
    c.head(["FROM 1 JAN 2027."], 960, 150, 1.4, role="acc")

def s5(c):
    c.mono("IT COUNTS STAFF YOU ALREADY HAVE", M, 330, 28, 0.0)
    c.head(["STARTED BY", "1 JULY 2026?"], 400, 200, 0.1, role=["fg", "acc"], stag=0.12)
    c.para("They’ll already have six months’ service when the change lands on 1 January.", 860, 46, 0.8, role="mut")
    # mini timeline
    al = c.a(1.4)
    if al > 0:
        y = 1150; x0, x1 = M + 20, W - M - 20
        c.d.line([(x0, y), (x1, y)], fill=c.c("edge", al), width=6)
        for x, lab, col in [(x0, "1 JUL 2026", "fg"), ((x0 + x1) / 2, "6 MONTHS", "dim"), (x1, "1 JAN 2027", "acc")]:
            c.d.ellipse([x - 16, y - 16, x + 16, y + 16], fill=c.c(col, al))
            text(c.d, x, y + 36, lab, F(E.MONO_B, 26), c.c(col, al), align="c" if x not in (x0, x1) else ("l" if x == x0 else "r"))

def s6(c):
    c.mono("AND FROM 1 JANUARY", M, 420, 30, 0.0)
    c.head(["NO CAP ON", "COMPENSATION."], 490, 200, 0.1, role=["fg", "acc"], stag=0.12)
    c.para("The government is uncapping compensatory awards for unfair dismissal.", 900, 44, 0.8, role="mut", fn=E.SERIF)

def s7(c):
    c.head(["THAT REVIEW", "YOU KEEP", "MOVING?"], 400, 230, 0.0, role=["fg", "fg", "acc"], stag=0.12)
    c.head(["IT MATTERS NOW."], 1100, 150, 0.8, role="fg")

def s8(c):
    c.mono("BEFORE 1 JANUARY", M, 480, 32, 0.0)
    c.head(["3 THINGS", "TO DO."], 550, 300, 0.1, role=["fg", "acc"], stag=0.2)

def step(n, title, sub, items):
    def fn(c):
        c.pill(f"{n} OF 3", M, 300, 0.0, size=28)
        yb = c.head(title, 410, 170, 0.1, role=["fg"] * (len(title) - 1) + ["acc"], stag=0.12)
        yb = c.para(sub, yb + 50, 44, 0.5, role="mut")
        y = yb + 60
        for i, it in enumerate(items):
            tt = 1.1 + i * 0.5
            tick(c, M, y + 6, 46, tt)
            c.para(it, y, 46, tt, role="fg", fn=E.BODY_B, x=M + 80, maxw=CW - 80)
            y += 100
    return fn

def s12(c):
    c.mono("THAT’S WHERE DOGETLAWYER HELPS", M, 300, 26, 0.0, role="acc", fn=E.MONO_B)
    win(c, 0.2, "EMPLOYMENT CONTRACTS · KEY DATES", 370, 1220)
    rows = [("Sam Patel", "Probation ends 14 Jan 2027", "Review task: P. Hale · due 7 Jan", "acc"),
            ("Aisha Khan", "Probation ends 30 Nov 2026", "Review done 24 Nov · outcome recorded", "ok"),
            ("Tom Reid", "Probation ends 3 Mar 2027", "Review task: J. Okafor · due 24 Feb", "acc")]
    y = 480
    for i, (n, d_, task, r) in enumerate(rows):
        tt = 0.6 + i * 0.4
        c.para(n, y, 44, tt, role="fg", fn=E.BODY_B, x=M + 40)
        c.para(d_, y + 62, 34, tt, role="fg", x=M + 40)
        c.para(task, y + 110, 30, tt, role=r, fn=E.BODY_B, x=M + 40)
        al = c.a(tt)
        if i < 2 and al > 0: c.d.rectangle([M + 40, y + 180, W - M - 40, y + 181], fill=c.c("line", al))
        y += 230
    c.para("Every probation end date, with a task and a name against it.", 1270, 42, 2.0, role="mut", fn=E.SERIF)

def s13(c):
    c.mono("BE HONEST", M, 420, 32, 0.0)
    c.head(["HOW MANY TIMES", "HAVE YOU MOVED", "A PROBATION REVIEW?"], 490, 150, 0.1, role=["fg", "fg", "acc"], stag=0.12)
    for i, n in enumerate(["0", "1", "2", "3+"]):
        tt = 1.0 + i * 0.15; a = c.a(tt)
        if a <= 0: continue
        x = M + i * 230
        c.d.rounded_rectangle([x, 1060, x + 190, 1230], radius=24, fill=c.c("panel", a), outline=c.c("acc", a), width=4)
        f = F(E.HEAD, 120); text(c.d, x + 95, 1145 - (f.getbbox(n)[1] + f.getbbox(n)[3]) / 2, n, f, c.c("acc", a), align="c")
    c.mono("COMMENT YOURS", M, 1270, 26, 1.6)

def close(c):
    close_card(c, ["STOP POSTPONING.", "6 MONTHS COMES FAST."], "Every key date. One place.")

SCENES = [
    (3.0, "POSTPONED", True, ["You've postponed Sam's probation review. Again."], h1),
    (3.6, "POSTPONED", False, ["From the first of January, staff can claim unfair dismissal after six months. Not two years."], h2),
    (3.6, "POSTPONED", False, ["And a probation clause in their contract won't change that."], h3),
    (6.6, "THE CHANGE", False, ["That's the government's own wording.", "The qualifying period drops from two years to six months, for dismissals from the first of January."], s4),
    (6.4, "THE CHANGE", False, ["And it counts staff you've already got.", "Anyone who started by the first of July this year will already have six months' service."], s5),
    (5.4, "THE CHANGE", False, ["And the cap on compensation for unfair dismissal is being removed too."], s6),
    (4.4, "THE CHANGE", False, ["So that review you keep moving? It really matters now."], s7),
    (3.0, "3 THINGS", False, ["Here's what to do."], s8),
    (7.0, "STEP 1", False, ["One. Put every probation end date in the diary,", "with a named owner and a reminder well before month six."],
     step(1, ["DIARISE EVERY", "END DATE."], "With a named owner and an early reminder.", ["Probation end date", "Who’s doing the review", "A reminder before month 6"])),
    (7.0, "STEP 2", False, ["Two. Actually hold the review, and write it down.", "What was discussed, what was agreed, and the outcome."],
     step(2, ["HOLD IT.", "WRITE IT DOWN."], "Then you can show what happened.", ["What was discussed", "What was agreed", "The outcome, dated"])),
    (6.8, "STEP 3", False, ["Three. Check what the contract says.", "How long probation is, whether it can be extended, and the notice period."],
     step(3, ["CHECK THE", "CONTRACT."], "What did you actually agree?", ["Probation length", "Whether it can be extended", "Notice period"])),
    (8.6, "KEY DATES", True, ["Dogetlawyer keeps every contract in one place,", "with key dates like probation end dates, and a task with a name against each one."], s12),
    (4.4, "YOUR TURN", False, ["Be honest. How many times have you moved a probation review? Comment it."], s13),
    (5.4, "DOGETLAWYER", False, ["Stop postponing. Six months comes round fast. Dogetlawyer dot com, link in bio."], close),
]
E.build(SCENES)
if __name__ == "__main__": E.main(HERE, os.path.join(HERE, "..", "vo14.json"))
