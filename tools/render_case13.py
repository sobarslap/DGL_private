"""Dogetlawyer Case File 13 - "Your best customer. Your staff's worst day." Third-party harassment duty from 30 Oct 2026 (Short 05).
Retention format (engine v3): hook on frame 0 (customer message + VIP badge), the answer by ~10 s, quick cuts, sound-off captions. ~1:21.
Type: Epilogue ExtraBold / Albert Sans / Martian Mono / Gelasio italic. Colour per section.
Usage: python3 render13.py info | preview T... | chunk START END OUT.mp4
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, ".."))
import numpy as np
from PIL import Image, ImageDraw
import engine3 as E
from engine3 import M, W, H, CW, F, tw, text, wrap, tick, cross, win, close_card
from multitheme import gradient, hexc, mix

SECTIONS = [
 ("Hook · graphite & amber",  "#1C1814", "#3E2608", "#FFFFFF", "#FFB020", "#7CFFB2"),
 ("The law · deep plum",      "#2E0F31", "#120812", "#FFFFFF", "#FFD166", "#8BF0BC"),
 ("4 steps · deep forest",    "#0D2C23", "#0A1512", "#FFFFFF", "#7CFFB2", "#7CFFB2"),
 ("Keep track · ink blue",    "#0E1F3A", "#090F1C", "#FFFFFF", "#7FE3FF", "#8BF0BC"),
]
MAP = [0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 0, 0]
PAPER = hexc("#FBFAF7"); INK = hexc("#1A1A1A"); GREY = hexc("#77736C"); RED = hexc("#FF3B30")

def bg(T):
    im = gradient(T, W, H); a = np.asarray(im, dtype=np.float32)
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    g = np.exp(-(((x - W * 0.2) / (W * 0.7)) ** 2 + ((y - H * 0.15) / (H * 0.3)) ** 2))[..., None]
    a = a + (np.array(T["acc"], np.float32) - a) * g * 0.08
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))

E.configure(os.path.join(HERE, "f"),
            ("Epilogue_800ExtraBold", "AlbertSans_500Medium", "AlbertSans_800ExtraBold", "MartianMono_400Regular", "MartianMono_600SemiBold",
             "Gelasio_500Medium_Italic", "AlbertSans_700Bold"),
            "CASE FILE 13", SECTIONS, MAP, bg)
E.LHK = 1.24

def message(c, y0):
    """Customer message card with a VIP badge (fictional)."""
    c.d.rounded_rectangle([M, y0, W - M, y0 + 330], radius=26, fill=PAPER)
    c.d.ellipse([M + 30, y0 + 30, M + 120, y0 + 120], fill=hexc("#C9A227"))
    text(c.d, M + 75, y0 + 52, "MG", F(E.BODY_B, 34), PAPER, align="c")
    text(c.d, M + 145, y0 + 34, "Mr Grant · Hartley Hotels", F(E.BODY_B, 36), INK)
    c.d.rounded_rectangle([M + 145, y0 + 84, M + 470, y0 + 124], radius=20, fill=hexc("#FFB020"))
    text(c.d, M + 160, y0 + 90, "VIP · £24K A YEAR", F(E.MONO_B, 22), INK)
    c.d.rounded_rectangle([M + 30, y0 + 150, W - M - 30, y0 + 300], radius=22, fill=hexc("#ECEAE5"))
    yy = y0 + 172
    for l in wrap(F(E.BODY_B, 38), "“Send the pretty one again next time. You know the one.”", CW - 120):
        text(c.d, M + 60, yy, l, F(E.BODY_B, 38), INK); yy += 50

def calendar_page(c, x, y, w, t0=0.0):
    al = c.a(t0)
    if al <= 0: return
    h = int(w * 1.05)
    c.d.rounded_rectangle([x, y, x + w, y + h], radius=24, fill=c.c(PAPER, al))
    c.d.rounded_rectangle([x, y, x + w, y + h * 0.28], radius=24, fill=c.c(RED, al)); c.d.rectangle([x, y + h * 0.18, x + w, y + h * 0.28], fill=c.c(RED, al))
    text(c.d, x + w / 2, y + h * 0.06, "OCTOBER 2026", F(E.MONO_B, int(w * 0.075)), c.c(PAPER, al), align="c")
    text(c.d, x + w / 2, y + h * 0.33, "30", F(E.HEAD, int(w * 0.5)), c.c(INK, al), align="c")

# ---------------------------------------------------------------- scenes
def h1(c):
    message(c, 330)
    c.head(["YOUR BEST", "CUSTOMER."], 760, 170, 0.0)
    c.head(["YOUR STAFF’S", "WORST DAY."], 1080, 130, 0.0, role="acc")

def h2(c):
    calendar_page(c, M, 330, 380)
    c.head(["FROM", "30 OCT"], 360, 150, 0.0, role=["fg", "acc"], x=M + 430, maxw=CW - 430, stag=0.1)
    c.head(["THAT CAN BE", "ON YOU."], 820, 180, 0.2, role=["fg", "acc"], stag=0.12)
    c.para("New duty under the Employment Rights Act 2025. England, Scotland & Wales.", 1230, 36, 0.6, role="mut")

def h3(c):
    c.head(["NOT THEM."], 420, 230, 0.0, role="fg")
    c.head(["YOU."], 650, 420, 0.15, role="acc")
    c.para("If you didn’t take all reasonable steps to stop it.", 1150, 46, 0.6, role="mut", fn=E.SERIF)

def s4(c):
    c.mono("WHAT THE GOVERNMENT SAYS", M, 320, 26, 0.0, role="acc", fn=E.MONO_B)
    al = c.a(0.2)
    if al > 0:
        y0 = 390
        c.d.rounded_rectangle([M, y0, W - M, y0 + 440], radius=24, fill=c.c(PAPER, al))
        c.d.rectangle([M, y0, M + 14, y0 + 440], fill=c.c("acc", al))
        y = y0 + 50
        for l in wrap(F(E.SERIF, 52), "“Employers must not permit the harassment of their employees by third parties, for example, customers and clients.”", CW - 100):
            text(c.d, M + 56, y, l, F(E.SERIF, 52), c.c(INK, al)); y += 70
    c.mono("SOURCE: BUSINESS.GOV.UK · EMPLOYMENT CHANGES", M, 870, 22, 0.6)
    c.mono("FROM 30 OCTOBER 2026 · EMPLOYMENT RIGHTS ACT 2025", M, 906, 22, 0.6)
    c.head(["CUSTOMERS AND", "CLIENTS COUNT."], 1000, 110, 1.4, role="acc")

def s5(c):
    c.mono("A “THIRD PARTY” IS ANYONE WHO ISN’T YOU OR YOUR STAFF", M, 330, 22, 0.0)
    for i, w_ in enumerate(["CUSTOMERS", "CLIENTS", "SUPPLIERS", "CONTRACTORS"]):
        tt = 0.2 + i * 0.4; al = c.a(tt)
        if al <= 0: continue
        y = 410 + i * 200
        c.d.rounded_rectangle([M, y + c.off(tt), W - M, y + 170 + c.off(tt)], radius=24, fill=c.c("panel", al), outline=c.c("acc", al), width=3)
        text(c.d, M + 44, y + 40 + c.off(tt), w_, F(E.HEAD, 84), c.c("fg", al))

def s6(c):
    c.mono("AND IT’S NOT JUST SEXUAL HARASSMENT", M, 330, 26, 0.0)
    c.head(["ANY", "HARASSMENT", "LINKED TO:"], 390, 150, 0.1, role=["fg", "acc", "fg"], stag=0.12)
    chips = ["Age", "Disability", "Race", "Religion or belief", "Sex", "Sexual orientation", "Gender reassignment"]
    x, y = M, 900
    for i, ch in enumerate(chips):
        tt = 0.8 + i * 0.15; al = c.a(tt)
        f = F(E.BODY_B, 40); w_ = tw(f, ch) + 56
        if x + w_ > W - M: x = M; y += 96
        if al > 0:
            c.d.rounded_rectangle([x, y, x + w_, y + 76], radius=38, fill=c.c("panel", al), outline=c.c("edge", al), width=2)
            text(c.d, x + 28, y + 16, ch, f, c.c("fg", al))
        x += w_ + 16

def s7(c):
    c.mono("AND IF IT GOES WRONG", M, 420, 30, 0.0)
    c.head(["YOUR STAFF", "CAN TAKE YOU", "TO A TRIBUNAL."], 490, 160, 0.1, role=["fg", "fg", "acc"], stag=0.12)
    c.para("A new claim, against the employer. The EHRC can also act.", 1060, 42, 0.8, role="mut", fn=E.SERIF)

def s8(c):
    c.mono("BEFORE 30 OCTOBER", M, 480, 32, 0.0)
    c.head(["4 THINGS", "TO DO."], 550, 250, 0.1, role=["fg", "acc"], stag=0.2)

def step(n, title, sub, items):
    def fn(c):
        c.pill(f"{n} OF 4", M, 300, 0.0, size=28)
        yb = c.head(title, 410, 150, 0.1, role=["fg"] * (len(title) - 1) + ["acc"], stag=0.12)
        yb = c.para(sub, yb + 50, 44, 0.5, role="mut")
        y = yb + 60
        for i, it in enumerate(items):
            tt = 1.1 + i * 0.5
            tick(c, M, y + 6, 46, tt)
            c.para(it, y, 46, tt, role="fg", fn=E.BODY_B, x=M + 80, maxw=CW - 80)
            y += 100
    return fn

def s13(c):
    c.mono("KEEP TRACK OF EVERY CLIENT CONTRACT", M, 300, 26, 0.0, role="acc", fn=E.MONO_B)
    win(c, 0.2, "CLIENT CONTRACTS · CONDUCT TERMS", 370, 1220)
    rows = [("Hartley Hotels", "Next task: add conduct clause", "P. Hale · due 29 Oct", "acc"),
            ("Brightwell Retail", "Terms updated 2 Oct 2026", "Done", "ok"),
            ("Corran Events", "Next task: send updated terms", "J. Okafor · due 27 Oct", "acc")]
    y = 480
    for i, (n, task, who, r) in enumerate(rows):
        tt = 0.6 + i * 0.4
        c.para(n, y, 44, tt, role="fg", fn=E.BODY_B, x=M + 40)
        c.para(task, y + 62, 34, tt, role=r, fn=E.BODY_B, x=M + 40)
        c.mono(who.upper(), M + 40, y + 116, 22, tt, tr=1)
        al = c.a(tt)
        if i < 2 and al > 0: c.d.rectangle([M + 40, y + 180, W - M - 40, y + 181], fill=c.c("line", al))
        y += 230
    c.para("A task and an owner for every update, so nothing slips.", 1270, 42, 2.0, role="mut", fn=E.SERIF)

def s14(c):
    c.mono("BE HONEST", M, 420, 32, 0.0)
    c.head(["HAS A CUSTOMER", "EVER CROSSED", "THE LINE?"], 490, 140, 0.1, role=["fg", "fg", "acc"], stag=0.12)
    for i, n in enumerate(["YES", "NO"]):
        tt = 1.0 + i * 0.2; a = c.a(tt)
        if a <= 0: continue
        x = M + i * 470
        c.d.rounded_rectangle([x, 1000, x + 440, 1180], radius=28, fill=c.c("panel", a), outline=c.c("acc", a), width=4)
        text(c.d, x + 220, 1045, n, F(E.HEAD, 90), c.c("acc", a), align="c")
    c.mono("WITH YOUR TEAM · TELL US IN THE COMMENTS", M, 1220, 24, 1.6)

def close(c):
    close_card(c, ["YOUR STAFF.", "YOUR DUTY."], "From 30 October 2026.")

SCENES = [
    (3.0, "BEST CUSTOMER", True, ["Your best customer keeps making your staff uncomfortable."], h1),
    (3.4, "BEST CUSTOMER", False, ["From the thirtieth of October, that can be on you."], h2),
    (3.6, "BEST CUSTOMER", False, ["Not them. You. If you didn't take all reasonable steps to stop it."], h3),
    (6.6, "THE LAW", False, ["The new law says employers must not permit harassment of their staff by third parties.", "That means customers and clients."], s4),
    (5.6, "THE LAW", False, ["A third party is anyone who isn't you or your staff.", "Customers, clients, suppliers, contractors."], s5),
    (5.8, "THE LAW", False, ["And it's not just sexual harassment.", "It covers harassment linked to things like age, disability, race, religion, sex and sexual orientation."], s6),
    (5.0, "THE LAW", False, ["And your staff can bring a claim against you at an employment tribunal."], s7),
    (3.2, "4 STEPS", False, ["So here's what to do before the thirtieth."], s8),
    (6.8, "STEP 1", False, ["One. Put it in writing.", "A harassment policy that covers customers and clients, not just staff."],
     step(1, ["PUT IT IN", "WRITING."], "A policy that covers customers, not just staff.", ["Customers and clients named", "What counts as harassment", "What you’ll do about it"])),
    (6.6, "STEP 2", False, ["Two. Make it easy to report.", "More than one way to speak up, and act fast when someone does."],
     step(2, ["MAKE IT EASY", "TO REPORT."], "And act fast when someone does.", ["More than one way to report", "A named person to tell", "Written notes of what you did"])),
    (7.0, "STEP 3", False, ["Three. Put it in your client contracts and terms.", "Set out how your staff must be treated, and what happens if they're not."],
     step(3, ["PUT IT IN YOUR", "CONTRACTS."], "Your client terms can set the standard.", ["How your staff must be treated", "What happens if they’re not"])),
    (6.2, "STEP 4", False, ["Four. Train your team and managers on what to do when it happens."],
     step(4, ["TRAIN YOUR", "TEAM."], "Staff and managers know what to do.", ["Spot it", "Report it", "Deal with it"])),
    (8.0, "KEEP TRACK", True, ["Dogetlawyer keeps every client contract in one place,", "with a task and an owner for each update. So nothing slips before the deadline."], s13),
    (4.4, "YOUR TURN", False, ["Has a customer ever crossed the line with your team? Yes or no."], s14),
    (5.4, "DOGETLAWYER", False, ["Your best customer isn't worth your best staff. Dogetlawyer dot com, link in bio."], close),
]
E.build(SCENES)
if __name__ == "__main__": E.main(HERE, os.path.join(HERE, "..", "vo13.json"))
