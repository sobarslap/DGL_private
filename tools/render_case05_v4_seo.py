"""Case 05 v3 - myth-buster format, money-first hook. Reuses helpers from render.py."""
import os, sys
import numpy as np
from PIL import Image, ImageDraw
import render_case05_v2 as R
from render_case05_v2 import (Ctx, F, text, tw, wrap, mix, cl, eio, hexc, W, H, FPS, M, CW, XF,
                    ANTON, INTER, INTER_SB, INTER_B, MONO, MONO_B, SERIF_I, DARK, LIGHT, GRAIN, win)

DUR = 105.0
GREEN = hexc("#1E7B57"); GREEN_D = hexc("#5FD3A0")
YEL = hexc("#F2D04B"); INK = hexc("#1A1014")

def stamp(c, s, cx, cy, size, t0, col, ang=-8):
    al = c.a(t0, 0.3)
    if al <= 0: return
    f = F(ANTON, size); w = int(tw(f, s, 2) + 60); h = int(size * 1.35)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([3, 3, w - 4, h - 4], radius=14, outline=col + (255,), width=7)
    bb = f.getbbox("H")
    text(d, w / 2, (h - (bb[3] - bb[1])) / 2 - bb[1], s, f, col + (255,), tr=2, align="c")
    im = im.rotate(ang, expand=True, resample=Image.BICUBIC)
    a = np.asarray(im).astype(np.float32); a[..., 3] *= al
    im = Image.fromarray(a.astype(np.uint8))
    c.im.paste(im, (int(cx - im.width / 2), int(cy - im.height / 2)), im)

def strike(c, x0, x1, y, t0, dur=0.5, col=None):
    p = eio((c.u - t0) / dur)
    if p <= 0: return
    c.d.rectangle([x0, y - 6, x0 + (x1 - x0) * p, y + 6], fill=col or c.T["acc"])

def quote(c, s, y, t0, size=128, strike_t=None):
    f = F(ANTON, size)
    lines = wrap(f, s, CW)
    bb = f.getbbox("H"); top, ch = bb[1], bb[3] - bb[1]; lh = int(ch * 1.2)
    for i, ln in enumerate(lines):
        al = c.a(t0 + i * 0.18)
        if al <= 0: continue
        text(c.d, M, y + i * lh - top, ln, f, c.c("fg", al), tr=1)
        if strike_t is not None:
            strike(c, M - 10, M + tw(f, ln, 1) + 10, y + i * lh + ch // 2, strike_t + i * 0.25)
    return y + (len(lines) - 1) * lh + ch

def count(c, v0, v1, t0, dur):
    return v0 + (v1 - v0) * eio((c.u - t0) / dur)

# ------------------------------------------------------------------ scenes
def h1(c):
    yb = c.head(["THIS ONE", "LINE"], 380, 230, 0.0)
    al = c.a(0.6)
    if al > 0:
        y = yb + 90; f = F(INTER_SB, 46)
        lines = wrap(f, "“Our total liability shall not exceed £3,900.”", CW - 60)
        for i, ln in enumerate(lines):
            w = tw(f, ln)
            c.d.rectangle([M - 10, y + i * 70 - 6, M + w + 14, y + i * 70 + 58], fill=mix(c.T["bg"], YEL, al))
            text(c.d, M, y + i * 70, ln, f, mix(c.T["bg"], INK, al))
    c.head(["COST A FIRM", "£54,500."], 1050, 150, 1.4, role=["fg", "acc"])

def h2(c):
    c.mono("LIMITATION OF LIABILITY CLAUSE", M, 400, 28, 0.0, role="acc", fname=MONO_B)
    c.mono("THE GAP BETWEEN THEIR LOSS AND THE CAP", M, 450, 22, 0.1, role="mut")
    v = int(count(c, 0, 54500, 0.0, 1.6) / 100) * 100
    c.head([f"£{v:,}"], 500, 260, 0.0, role="acc")
    rows = [("THEIR LOSS", "£58,400"), ("WHAT THE SUPPLIER OFFERED", "£3,900")]
    y = 900
    for i, (k, val) in enumerate(rows):
        tt = 1.2 + i * 0.5
        c.box(M, y, W - M, y + 120, tt, r=14)
        c.mono(k, M + 36, y + 46, 26, tt + 0.05)
        c.para(val, y + 34, 46, tt + 0.05, role="fg", fname=INTER_B, x=W - M - 36 - tw(F(INTER_B, 46), val))
        y += 140

def h3(c):
    c.head(["ONE’S PROBABLY", "IN YOUR", "SUPPLIER T&Cs", "RIGHT NOW."], 470, 170, 0.0,
           role=["fg", "fg", "acc", "acc"])

def h4(c):
    c.mono("LET'S CLEAR THIS UP", M, 470, 26, 0.0)
    c.head(["4 MYTHS", "ABOUT THE", "SMALL PRINT"], 540, 200, 0.15, role=["acc", "fg", "fg"])
    c.para("that leave UK businesses out of pocket.", 1190, 46, 1.2, role="mut", fname=SERIF_I)

def myth(n, q):
    def fn(c):
        stamp(c, f"MYTH #{n}", W - M - 190, 470, 84, 0.0, c.T["acc"], ang=-9)
        c.mono("WHAT PEOPLE THINK", M, 640, 26, 0.2)
        quote(c, q, 720, 0.35, size=130, strike_t=2.9)
    return fn

def truth(head, sub, src, roles=None):
    def fn(c):
        stamp(c, "THE TRUTH", W - M - 210, 470, 76, 0.0, GREEN, ang=7)
        yb = c.head(head, 640, 150, 0.3, role=roles or "fg")
        yb = c.para(sub, yb + 60, 46, 1.4, role="mut")
        c.rule(M, yb + 40, M + 120, 2.0, role=GREEN, w=5)
        c.mono(src, M, yb + 66, 23, 2.1)
    return fn

def t4(c):
    stamp(c, "THE TRUTH", W - M - 210, 430, 76, 0.0, GREEN, ang=7)
    c.head(["IT'S YOUR", "EVIDENCE."], 560, 160, 0.3, role=["fg", GREEN])
    mid = W // 2; y0 = 920
    c.box(M, y0, mid - 14, y0 + 470, 1.3); c.box(mid + 14, y0, W - M, y0 + 470, 1.3)
    c.mono("WITHOUT", M + 34, y0 + 34, 26, 1.4, role="acc", fname=MONO_B)
    c.mono("WITH", mid + 48, y0 + 34, 26, 1.4, role=GREEN, fname=MONO_B)
    L = ["Terms agreed on a call", "Quote lost in an inbox", "No idea which version"]
    Rr = ["Signed terms, v4.2", "Emails saying what it was for", "11 past orders, dated"]
    for i in range(3):
        tt = 2.0 + i * 0.9
        c.para(L[i], y0 + 110 + i * 120, 36, tt, role="mut", x=M + 34, maxw=mid - M - 80, lead=1.22)
        c.para(Rr[i], y0 + 110 + i * 120, 36, tt + 0.3, role="fg", x=mid + 48, maxw=mid - M - 80, lead=1.22)

def recap(c):
    c.mono("SO, TO RECAP", M, 360, 26, 0.0)
    items = ["“I'm stuck with it.”", "“Judged when it broke.”", "“Never enforceable.”", "“Records are just admin.”"]
    y = 440; f = F(ANTON, 84)
    for i, s in enumerate(items):
        al = c.a(0.15 + i * 0.25)
        if al > 0:
            text(c.d, M, y, s, f, c.c("mut", al), tr=1)
            strike(c, M - 6, M + tw(f, s, 1) + 6, y + 70, 0.4 + i * 0.25, 0.35)
        y += 140
    c.head(["THE DIFFERENCE?", "THE PAPER TRAIL."], 1030, 140, 1.8, role=["fg", "acc"])

def p1(c):
    c.mono("THAT'S WHAT DOGETLAWYER IS FOR", M, 330, 26, 0.0, role="acc")
    win(c, 0.2, "LIABILITY CAPS · ALL SUPPLIERS", 400, 1060)
    rows = [("Mereton Systems Ltd", "£3,900", "3 months' charges"), ("Brayfield Plant Hire", "£25,000", "fixed sum"),
            ("Ivelet Logistics Ltd", "Price paid", "per consignment")]
    y = 520
    for i, (n, v, b) in enumerate(rows):
        tt = 0.7 + i * 0.45
        c.para(n, y, 40, tt, role="fg", x=M + 40)
        c.para(v, y, 40, tt, role="acc", fname=INTER_B, x=W - M - 40 - tw(F(INTER_B, 40), v))
        c.mono(b.upper(), M + 40, y + 62, 22, tt)
        if i < 2: c.rule(M + 40, y + 120, W - M - 40, tt, role="line", w=2)
        y += 170
    c.head(["EVERY CAP,", "IN ONE PLACE."], 1130, 120, 2.2, role=["fg", "acc"])

def p2(c):
    c.mono("OPEN ONE UP", M, 330, 26, 0.0, role="acc")
    win(c, 0.2, "MERETON SYSTEMS LTD · CONTRACT", 400, 1180)
    rows = [("TERMS", "Version 4.2 — attached"), ("SENT", "14 May 2026, 09:12"), ("SIGNED", "16 May 2026"),
            ("CLAUSE 11.3", "Liability cap — flagged"), ("PAST ORDERS", "11, all on these terms")]
    y = 510
    for i, (k, v) in enumerate(rows):
        tt = 0.5 + i * 0.4
        c.mono(k, M + 40, y + 8, 24, tt)
        c.para(v, y, 40, tt, role="acc" if k.startswith("CLAUSE") else "fg", x=M + 330, maxw=CW - 380)
        if i < len(rows) - 1: c.rule(M + 40, y + 108, W - M - 40, tt, role="line", w=2)
        y += 128
    c.head(["YOUR PAPER TRAIL,", "SORTED."], 1250, 110, 2.8, role=["fg", "acc"])

def ch(c):
    stamp(c, "60-SECOND CHALLENGE", W / 2, 470, 70, 0.0, c.T["acc"], ang=-4)
    c.head(["OPEN YOUR", "BIGGEST SUPPLIER", "CONTRACT."], 640, 150, 0.4)
    al = c.a(1.8)
    if al > 0:
        y = 1150; c.box(M, y, W - M, y + 120, 1.8, r=60)
        text(c.d, M + 50, y + 34, "Search:  liability", F(INTER_SB, 46), c.c("fg", al))
    c.para("You might be surprised.", 1320, 44, 2.6, role="mut", fname=SERIF_I)

def cm(c):
    c.head(["WHICH MYTH", "DID YOU", "BELIEVE?"], 480, 190, 0.0, role=["fg", "fg", "acc"])
    al = c.a(1.0)
    for i in range(4):
        tt = 1.0 + i * 0.2; a = c.a(tt)
        if a <= 0: continue
        x = M + i * 230
        c.d.rounded_rectangle([x, 1060, x + 190, 1250], radius=24, fill=c.c("panel", a), outline=c.c("acc", a), width=4)
        text(c.d, x + 95, 1085, str(i + 1), F(ANTON, 120), c.c("acc", a), align="c")
    c.para("Drop the number in the comments.", 1320, 44, 1.9, role="mut", fname=SERIF_I)

def close(c):
    c.head(["DOGETLAWYER"], 560, 120, 0.1, role="acc", align="c")
    c.head(["KNOW WHAT YOUR", "CONTRACTS CAP."], 760, 140, 0.4, align="c")
    c.para("Every liability cap. Every supplier. One place.", 1090, 40, 0.9, role="mut", align="c", fname=SERIF_I)
    c.para("dogetlawyer.com", 1170, 44, 0.9, role="fg", fname=INTER_SB, align="c")
    c.chip_bio = True
    al = c.a(0.8)
    if al > 0:
        f = F(MONO_B, 30); w = tw(f, "LINK IN BIO", 3) + 60
        c.d.rounded_rectangle([W / 2 - w / 2, 1240, W / 2 + w / 2, 1300], radius=30, fill=c.c("acc", al))
        text(c.d, W / 2, 1254, "LINK IN BIO", f, c.T["bg"], tr=3, align="c")
    c.para("Contract management software for UK small businesses — not a substitute for legal advice.",
           1340, 30, 1.4, role="mut", align="c", maxw=CW - 40)
    c.para("All names, figures and documents shown are fictional examples.", 1430, 26, 1.5, role="dim", align="c")

# (start, end, theme, label, progress 0-4 or None, demo, vo, fn)
SC = [
    (0.0, 3.6, DARK, "WATCH THIS", None, True, ["This one line just cost a firm fifty-four grand."], h1),
    (3.6, 7.6, DARK, "WATCH THIS", None, True, ["It's a limitation of liability clause. Their machine broke, they lost fifty-eight thousand.",
                                                 "The supplier said: we'll pay three nine."], h2),
    (7.6, 11.0, DARK, "WATCH THIS", None, False, ["And one's probably in your supplier terms and conditions right now."], h3),
    (11.0, 14.6, DARK, "4 MYTHS", 0, False, ["So let's bust four myths that leave businesses out of pocket."], h4),
    (14.6, 19.2, DARK, "MYTH 1 OF 4", 1, False, ["Myth one. It's in the contract, so I'm stuck with it."],
     myth(1, "“IT'S IN THE CONTRACT, SO I'M STUCK WITH IT.”")),
    (19.2, 26.6, LIGHT, "MYTH 1 OF 4", 1, False, ["Not quite. Under the Unfair Contract Terms Act, if it's on their standard terms,",
                                                   "the cap has to pass the reasonableness test. And it's on them to prove it. Not you."],
     truth(["IT HAS TO PASS THE", "REASONABLENESS TEST."], "On their standard terms. And the supplier has to prove it — not you.",
           "UNFAIR CONTRACT TERMS ACT 1977 · s.3 · s.11(5)", ["fg", GREEN])),
    (26.6, 31.2, DARK, "MYTH 2 OF 4", 2, False, ["Myth two. It's judged on the day it all went wrong."],
     myth(2, "“IT'S JUDGED ON THE DAY IT BROKE.”")),
    (31.2, 38.6, LIGHT, "MYTH 2 OF 4", 2, False, ["Nope. It's judged on what you both knew when you signed.",
                                                   "So what was said back then really matters."],
     truth(["IT'S JUDGED ON", "THE DAY YOU SIGNED."], "What did you both know back then? What was it for?",
           "UCTA 1977 · s.11(1)", ["fg", GREEN])),
    (38.6, 43.2, DARK, "MYTH 3 OF 4", 3, False, ["Myth three. A liability cap is never enforceable."],
     myth(3, "“A LIABILITY CAP IS NEVER ENFORCEABLE.”")),
    (43.2, 50.8, LIGHT, "MYTH 3 OF 4", 3, False, ["Wrong. Plenty are perfectly fair, and enforceable.",
                                                   "Courts weigh things like who had the clout, and whether you knew the clause was there."],
     truth(["PLENTY ARE FAIR", "AND ENFORCEABLE."],
           "Courts weigh things like bargaining power, your other options, and whether you knew the clause was there.",
           "UCTA 1977 · SCHEDULE 2 FACTORS · OUTCOMES TURN ON THE FACTS", ["fg", GREEN])),
    (50.8, 55.4, DARK, "MYTH 4 OF 4", 4, False, ["Myth four. Keeping records is just admin."],
     myth(4, "“KEEPING RECORDS IS JUST ADMIN.”")),
    (55.4, 64.2, LIGHT, "MYTH 4 OF 4", 4, True, ["It's your evidence. One firm had a phone call and a lost quote.",
                                                  "The other had the signed terms, the emails and eleven past orders.",
                                                  "Guess who had a case to make."], t4),
    (64.2, 69.2, DARK, "RECAP", 4, False, ["Same clause. Same supplier. The difference was the paper trail."], recap),
    (69.2, 77.2, DARK, "THE FIX", None, True, ["That's what Dogetlawyer's for.",
                                                "Every supplier, and the cap buried in their terms, pulled out where you can see it."], p1),
    (77.2, 85.0, DARK, "THE FIX", None, True, ["Open one up: the version you signed, when it was sent,",
                                                "the clause flagged, and every order on those terms."], p2),
    (85.0, 93.0, LIGHT, "YOUR TURN", None, False, ["Here's your sixty-second challenge.",
                                                    "Open your biggest supplier contract and search for the word liability.",
                                                    "You might be surprised."], ch),
    (93.0, 99.0, LIGHT, "YOUR TURN", None, False, ["Which myth did you believe?", "Drop the number in the comments."], cm),
    (99.0, 105.0, DARK, "DOGETLAWYER", None, False, ["Check your contracts at dogetlawyer.com. Link in bio."], close),
]

def caption_at(si, u):
    a, b = SC[si][0], SC[si][1]; vo = SC[si][6]
    dur = b - a - 0.4; tot = sum(len(s) for s in vo); t = 0.15
    for s in vo:
        d = dur * len(s) / tot
        if t <= u < t + d: return s, cl((u - t) / 0.15) * cl((t + d - u) / 0.15)
        t += d
    return None, 0

def chrome(d, T, label, prog, demo):
    text(d, M, 96, "DOGETLAWYER", F(MONO_B, 24), T["acc"], tr=3)
    text(d, W - M, 96, "CASE FILE № 05", F(MONO, 24), T["dim"], tr=3, align="r")
    fc = F(MONO_B, 22); w = tw(fc, label, 2) + 44
    d.rounded_rectangle([M, 150, M + w, 198], radius=24, fill=T["acc"])
    text(d, M + 22, 161, label, fc, T["bg"], tr=2)
    if prog is not None:
        for k in range(4):
            x = W - M - (4 - k) * 70 + 10
            d.rounded_rectangle([x, 166, x + 56, 182], radius=8, fill=T["acc"] if k < prog else T["edge"])
    d.rectangle([M, 1490, W - M, 1491], fill=T["line"])
    if demo: text(d, M, 1820, "FICTIONAL DEMO EXAMPLE", F(MONO, 22), T["dim"], tr=2)
    text(d, W - M, 1820, "dogetlawyer.com", F(MONO, 22), T["dim"], tr=1, align="r")

def render_scene(si, t):
    a, b, T, label, prog, demo, vo, fn = SC[si]
    im = R.BG[id(T)].copy()
    c = Ctx(im, T, t - a); c.im = im
    fn(c)
    chrome(c.d, T, label, prog, demo)
    s, al = caption_at(si, t - a)
    R.draw_caption(c.d, T, s, al)
    return im

def frame(i):
    t = i / FPS
    si = max(k for k, s in enumerate(SC) if t >= s[0]); a, b = SC[si][0], SC[si][1]
    im = render_scene(si, t)
    if si + 1 < len(SC) and t > b - XF / 2:
        im = Image.blend(im, render_scene(si + 1, t), eio((t - (b - XF / 2)) / XF))
    elif si > 0 and t < a + XF / 2:
        im = Image.blend(render_scene(si - 1, t), im, eio((t - (a - XF / 2)) / XF))
    arr = np.asarray(im, dtype=np.float32) + GRAIN[i % len(GRAIN)]
    return arr.clip(0, 255).astype(np.uint8)

if __name__ == "__main__":
    HERE = os.path.dirname(os.path.abspath(__file__))
    if sys.argv[1] == "preview":
        os.makedirs(os.path.join(HERE, "pv4"), exist_ok=True)
        for ts in sys.argv[2:]:
            Image.fromarray(frame(int(round(float(ts) * FPS)))).save(os.path.join(HERE, "pv4", f"t{float(ts):06.2f}.png"))
    else:
        import subprocess
        s, e, out = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                              "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "14",
                              "-pix_fmt", "yuv420p", "-g", "60", out], stdin=subprocess.PIPE)
        for i in range(s, e):
            p.stdin.write(frame(i).tobytes())
        p.stdin.close(); p.wait(); print("DONE", out, flush=True)
