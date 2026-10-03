"""Dogetlawyer Case File 06 - personal guarantees. Chat hook + 5-point checklist.
Palette: court black & scarlet / ivory. Type: Archivo Black, Space Grotesk, IBM Plex Mono, Instrument Serif.
Usage: python3 render6.py preview T...   |   python3 render6.py chunk START END OUT.mp4
"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__)); FD = os.path.join(HERE, "f")
W, H, FPS, DUR, M = 1080, 1920, 30, 105.0, 84
CW = W - 2 * M; XF = 0.30

def hexc(h): h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
def mix(a, b, t): return tuple(int(round(x + (y - x) * t)) for x, y in zip(a, b))
def cl(x): return 0.0 if x < 0 else (1.0 if x > 1 else x)
def eio(x): x = cl(x); return x * x * (3 - 2 * x)

def theme(bg, fg, acc):
    return dict(bg=bg, fg=fg, acc=acc, mut=mix(bg, fg, 0.66), dim=mix(bg, fg, 0.45),
                line=mix(bg, fg, 0.12), panel=mix(bg, fg, 0.07), edge=mix(bg, fg, 0.22))
DARK = theme(hexc("#121213"), hexc("#F4EFE6"), hexc("#E0313F"))
LIGHT = theme(hexc("#F4EFE6"), hexc("#141414"), hexc("#B5182A"))
OK_G = hexc("#1F8A5B")

_fc = {}
def F(n, s):
    if (n, s) not in _fc: _fc[(n, s)] = ImageFont.truetype(os.path.join(FD, n + ".ttf"), s)
    return _fc[(n, s)]
HEAD = "ArchivoBlack_400Regular"; BODY = "SpaceGrotesk_500Medium"; BODY_B = "SpaceGrotesk_700Bold"
MONO = "IBMPlexMono_500Medium"; MONO_B = "IBMPlexMono_700Bold"; SERIF = "InstrumentSerif_400Regular_Italic"
CAP = "SpaceGrotesk_600SemiBold"

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
    def c(s, role, al):
        return mix(s.T["bg"], s.T[role] if isinstance(role, str) else role, al)
    def head(s, lines, y, size, t0, role="fg", gap=0.12, align="l", maxw=CW, stag=0.2, x=None):
        f = F(HEAD, size)
        while max(tw(f, ln) for ln in lines) > maxw and size > 36: size -= 4; f = F(HEAD, size)
        bb = f.getbbox("H"); top, ch = bb[1], bb[3] - bb[1]; lh = int(ch * (1 + gap) + size * 0.12)
        x = (M if align == "l" else W / 2) if x is None else x
        for i, ln in enumerate(lines):
            al = s.a(t0 + i * stag)
            if al > 0:
                r = role[i] if isinstance(role, list) else role
                text(s.d, x, y + i * lh - top, ln, f, s.c(r, al), align=align)
        return y + (len(lines) - 1) * lh + ch
    def para(s, t, y, size, t0, role="mut", fn=BODY, maxw=CW, lead=1.3, align="l", x=None):
        f = F(fn, size); ls = wrap(f, t, maxw); al = s.a(t0)
        x = (M if align == "l" else W / 2) if x is None else x
        for i, ln in enumerate(ls):
            if al > 0: text(s.d, x, y + i * int(size * lead), ln, f, s.c(role, al), align=align)
        return y + len(ls) * int(size * lead)
    def mono(s, t, x, y, size, t0, role="dim", tr=2, align="l", fn=MONO):
        al = s.a(t0)
        if al > 0: text(s.d, x, y, t, F(fn, size), s.c(role, al), tr=tr, align=align)
    def box(s, x0, y0, x1, y1, t0, fill="panel", edge="edge", r=18, w=2):
        al = s.a(t0)
        if al > 0: s.d.rounded_rectangle([x0, y0, x1, y1], radius=r, fill=s.c(fill, al),
                                          outline=s.c(edge, al) if edge else None, width=w)
    def rule(s, x0, y, x1, t0, role="acc", w=6):
        al = s.a(t0)
        if al > 0: s.d.rectangle([x0, y, x1, y + w - 1], fill=s.c(role, al))

# ------------------------------------------------------------------ scenes
def s1(c):
    c.mono("QUICK ONE", M, 560, 28, 0.0)
    c.head(["LTD COMPANY", "DIRECTOR?"], 630, 150, 0.1)
    c.para("So your house is safe… right?", 1000, 52, 1.3, role="mut", fn=SERIF)

def s2(c):
    yb = c.head(["SO WHY CAN", "THEY COME", "AFTER", "YOUR HOUSE?"], 470, 160, 0.0, role=["fg", "fg", "fg", "acc"])
    c.para("If you’ve signed a personal guarantee.", yb + 60, 50, 1.2, role="mut", fn=SERIF)

def bubble(c, s, y, t0, me=False, size=38):
    al = c.a(t0, 0.3)
    if al <= 0: return y
    f = F(BODY, size); ls = wrap(f, s, 640)
    w = max(tw(f, l) for l in ls) + 64; h = len(ls) * int(size * 1.3) + 44
    x0 = W - M - w if me else M
    fill = c.T["acc"] if me else c.T["panel"]
    c.d.rounded_rectangle([x0, y, x0 + w, y + h], radius=34, fill=c.c(fill, al),
                          outline=None if me else c.c("edge", al), width=2)
    for i, l in enumerate(ls):
        text(c.d, x0 + 32, y + 20 + i * int(size * 1.3), l, f, c.c(c.T["bg"] if me else "fg", al))
    return y + h + 24

def s3(c):
    c.mono("NEW SUPPLIER · ACCOUNTS TEAM", M, 330, 24, 0.0)
    y = 400
    y = bubble(c, "Hiya! Just need a quick signature on the credit account form", y, 0.2)
    y = bubble(c, "Then we can get your first order out today", y, 1.0)
    y = bubble(c, "No worries, signing now", y, 2.0, me=True)
    al = c.a(3.4)
    if al > 0:
        y0 = 1000
        c.box(M, y0, W - M, y0 + 400, 3.4, fill="fg", edge=None, r=10)
        ink = mix(c.T["bg"], hexc("#141414"), 1.0)
        dd = c.d
        text(dd, M + 40, y0 + 34, "CREDIT ACCOUNT APPLICATION · PAGE 4 OF 4", F(MONO, 22), mix(c.c("fg", al), hexc("#6b6b6b"), al), tr=1)
        dd.rectangle([M + 36, y0 + 90, W - M - 36, y0 + 260], outline=c.c("acc", al), width=4)
        text(dd, M + 60, y0 + 108, "PERSONAL GUARANTEE", F(MONO_B, 28), c.c("acc", al), tr=2)
        for i, l in enumerate(wrap(F(BODY, 30), "I personally guarantee payment of all sums due from the company, now or in the future.", CW - 140)):
            text(dd, M + 60, y0 + 156 + i * 40, l, F(BODY, 30), mix(c.c("fg", al), hexc("#141414"), al))
        text(dd, M + 40, y0 + 310, "Signed: ____________________", F(BODY, 30), mix(c.c("fg", al), hexc("#141414"), al))

def s4(c):
    c.mono("THAT BOX HAS A NAME", M, 470, 26, 0.0)
    yb = c.head(["PERSONAL", "GUARANTEE."], 540, 170, 0.15, role=["fg", "acc"])
    c.para("If the company can't pay, you do. Personally.", yb + 70, 50, 1.2, role="fg")

def s5(c):
    c.mono("FOR THAT DEBT", M, 430, 26, 0.0)
    c.head(["YOUR LTD", "PROTECTION?", "GONE."], 500, 160, 0.15, role=["fg", "fg", "acc"])
    items = ["Your home", "Your car", "Your savings"]
    y = 1080
    for i, s in enumerate(items):
        tt = 1.4 + i * 0.5; al = c.a(tt)
        if al > 0:
            c.d.rectangle([M, y + 18, M + 26, y + 44], fill=c.c("acc", al))
            text(c.d, M + 52, y, s, F(BODY_B, 50), c.c("fg", al))
        y += 84
    c.mono("SOURCE: GOV.UK · INSOLVENCY SERVICE · DIRECTOR INFORMATION HUB", M, y + 20, 21, 2.6, tr=1)

def s6(c):
    c.mono("HERE'S THE KICKER", M, 450, 26, 0.0)
    yb = c.head(["IT ONLY HAS", "TO BE IN WRITING", "AND SIGNED."], 520, 130, 0.15, role=["fg", "fg", "acc"])
    yb = c.para("Which is exactly what that little form is.", yb + 60, 48, 1.4, role="mut", fn=SERIF)
    c.mono("STATUTE OF FRAUDS 1677 · s.4 · GENERAL POSITION", M, yb + 50, 21, 2.0)

def s7(c):
    c.head(["BEFORE YOU", "SIGN ANYTHING,", "CHECK THESE 5."], 560, 150, 0.0, role=["fg", "fg", "acc"])

def check(n, head, sub, extra=None):
    def fn(c):
        f = F(HEAD, 300); al = c.a(0.0)
        text(c.d, W - M, 1060, f"0{n}", f, c.c("line", al), align="r")
        c.mono(f"CHECK {n} OF 5", M, 440, 26, 0.05, role="acc", fn=MONO_B)
        yb = c.head(head, 510, 140, 0.15)
        yb = c.para(sub, yb + 60, 46, 0.9, role="mut")
        # tick box
        bx, by = M, yb + 70; al = c.a(2.4)
        if al > 0:
            c.d.rounded_rectangle([bx, by, bx + 80, by + 80], radius=12, outline=c.c(OK_G, al), width=6)
            p = eio((c.u - 2.5) / 0.4)
            if p > 0:
                pts = [(bx + 18, by + 42), (bx + 34, by + 60), (bx + 64, by + 22)]
                c.d.line(pts[:2] if p < 0.5 else pts, fill=c.c(OK_G, al), width=10, joint="curve")
            text(c.d, bx + 110, by + 18, "Checked", F(BODY_B, 40), c.c(OK_G, al))
        if extra: extra(c, by + 150)
    return fn

def s13(c):
    c.mono("THE WORST PART?", M, 470, 26, 0.0)
    c.head(["IT'S EASY TO", "FORGET YOU", "EVER SIGNED IT."], 540, 140, 0.15)
    c.head(["UNTIL THE LETTER", "TURNS UP."], 1050, 120, 1.6, role="acc")

def win(c, t0, title, y0, y1):
    c.box(M, y0, W - M, y1, t0, r=20); al = c.a(t0)
    if al > 0:
        c.d.rounded_rectangle([M, y0, W - M, y0 + 70], radius=20, fill=c.c("edge", al * 0.8))
        c.d.rectangle([M, y0 + 50, W - M, y0 + 70], fill=c.c("edge", al * 0.8))
        for k in range(3): c.d.ellipse([M + 28 + k * 30, y0 + 26, M + 46 + k * 30, y0 + 44], fill=c.c("dim", al))
        text(c.d, M + 140, y0 + 20, title, F(MONO, 24), c.c("fg", al), tr=1)

def s14(c):
    c.mono("THAT'S WHERE DOGETLAWYER COMES IN", M, 330, 26, 0.0, role="acc")
    win(c, 0.2, "GUARANTEES · ALL CONTRACTS", 400, 1170)
    rows = [("Halden Timber Supplies", "Unlimited", "Signed by J. Morley · 3 Feb 2025", "acc"),
            ("Tannery Lane Leasing", "Capped £15,000", "Ends on 3 months' notice", "fg"),
            ("Brookfield Fuels Ltd", "None", "No guarantee on file", "dim")]
    y = 520
    for i, (n, v, b, r) in enumerate(rows):
        tt = 0.7 + i * 0.5
        c.para(n, y, 40, tt, role="fg", fn=BODY_B, x=M + 40)
        c.para(v, y, 38, tt, role=r, fn=BODY_B, x=W - M - 40 - tw(F(BODY_B, 38), v))
        c.mono(b, M + 40, y + 62, 23, tt, tr=1)
        if i < 2: c.rule(M + 40, y + 130, W - M - 40, tt, role="line", w=2)
        y += 190
    c.para("Every guarantee on record: who signed it, and whether there's a limit.", 1220, 42, 2.2, role="mut", fn=SERIF)

def s15(c):
    c.head(["SO YOU ALWAYS", "KNOW WHAT", "YOU'VE PUT", "ON THE LINE."], 520, 150, 0.0, role=["fg", "fg", "fg", "acc"])

def s16(c):
    c.mono("SAVE THIS FOR NEXT TIME SOMEONE SAYS", M, 500, 24, 0.0)
    c.head(["“JUST A QUICK", "SIGNATURE.”"], 570, 150, 0.2, role="acc")
    c.para("And send it to whoever signs for your business.", 1000, 46, 1.2, role="mut", fn=SERIF)

def close(c):
    c.head(["DOGETLAWYER"], 560, 110, 0.1, role="acc", align="c")
    c.head(["KNOW WHAT", "YOU'VE SIGNED."], 760, 130, 0.4, align="c")
    c.para("Every contract. Every personal guarantee. One place.", 1040, 40, 0.9, role="mut", align="c", fn=SERIF)
    al = c.a(0.8)
    if al > 0:
        f = F(MONO_B, 30); w = tw(f, "LINK IN BIO", 3) + 60
        c.d.rectangle([W / 2 - w / 2, 1190, W / 2 + w / 2, 1250], fill=c.c("acc", al))
        text(c.d, W / 2, 1203, "LINK IN BIO", f, c.c("bg", al) if False else mix(c.c("acc", al), c.T["bg"], 1.0), tr=3, align="c")
    c.para("dogetlawyer.com", 1120, 44, 0.9, role="fg", fn=BODY_B, align="c")
    c.para("Contract management software for UK small businesses — not a substitute for legal advice.",
           1300, 30, 1.4, role="mut", align="c", maxw=CW - 40)
    c.para("All names, figures and documents shown are fictional examples.", 1400, 26, 1.5, role="dim", align="c")

LBL_H, LBL_P, LBL_C, LBL_F, LBL_E = "THE QUICK SIGNATURE", "WHAT YOU SIGNED", "5 CHECKS", "THE FIX", "SAVE THIS"
SC = [
    (0.0, 3.4, DARK, LBL_H, None, False, ["Limited company director? So your house is safe, right?"], s1),
    (3.4, 7.0, DARK, LBL_H, None, False, ["Not if you’ve signed a personal guarantee."], s2),
    (7.0, 14.6, DARK, LBL_H, None, True, ["It usually starts like this. A friendly message, a credit account form.",
                                         "Just sign at the bottom. And on page four, there's a box."], s3),
    (14.6, 20.6, DARK, LBL_P, None, False, ["It's a personal guarantee. Suppliers, landlords and lenders ask for them all the time.", "If your company can't pay that debt, you’re on the hook. Personally."], s4),
    (20.6, 27.4, DARK, LBL_P, None, False, ["That limited company protection you were counting on? For that debt, it's gone.",
                                           "The government's own guidance says your home, car and savings could be used to pay it."], s5),
    (27.4, 33.4, LIGHT, LBL_P, None, False, ["And here's the kicker. A guarantee only has to be in writing and signed.",
                                            "Which is exactly what that little form is."], s6),
    (33.4, 37.0, LIGHT, LBL_C, 0, False, ["So before you sign anything, check these five things."], s7),
    (37.0, 46.0, DARK, LBL_C, 1, False, ["One. Search the whole thing for guarantee, and indemnity.", "Every page. The small print too."],
     check(1, ["SEARCH FOR", "“GUARANTEE”."], "And “indemnity”. Ctrl+F the whole document, small print included.")),
    (46.0, 55.0, LIGHT, LBL_C, 2, False, ["Two. Is there a limit?", "An unlimited guarantee covers every penny the company owes them. You can ask for a cap."],
     check(2, ["IS THERE", "A LIMIT?"], "Unlimited means every penny the company owes. You can ask for a cap.")),
    (55.0, 64.0, DARK, LBL_C, 3, False, ["Three. How do you get out of it? Can you end it with notice?", "Some guarantees carry on even after you leave the company."],
     check(3, ["HOW DO YOU", "GET OUT?"], "Can you end it with notice? Some carry on even after you leave the company.")),
    (64.0, 73.0, LIGHT, LBL_C, 4, False, ["Four. Who else is signing?", "If it's joint and several, each of you could be chased for the full amount."],
     check(4, ["WHO ELSE IS", "SIGNING?"], "If it's “joint and several”, each of you could be chased for the full amount.")),
    (73.0, 82.0, DARK, LBL_C, 5, False, ["And five. If your home's on the line, get proper advice before you sign.", "Not after."],
     check(5, ["GET IT CHECKED", "FIRST."], "If you're putting your home on the line, speak to a solicitor before you sign. Not after.")),
    (82.0, 87.0, DARK, LBL_F, None, False, ["The worst part? It's easy to forget you ever signed one.", "Until the letter turns up."], s13),
    (87.0, 95.0, DARK, LBL_F, None, True, ["That's where Dogetlawyer comes in. Every contract in one place,",
                                          "and every personal guarantee on record, with who signed it and whether there's a limit."], s14),
    (95.0, 99.0, LIGHT, LBL_F, None, False, ["So you always know what you've put on the line."], s15),
    (99.0, 101.8, LIGHT, LBL_E, None, False, ["Save this for the next time someone says, just a quick signature."], s16),
    (101.8, 105.0, DARK, "DOGETLAWYER", None, False, ["Check what you’ve signed at dogetlawyer.com. Link in bio."], close),
]

def build_bg(T, light):
    im = Image.new("RGB", (W, H), T["bg"]); d = ImageDraw.Draw(im)
    for yy in range(0, H, 36):
        for xx in range(0, W, 36):
            # halftone: dots grow toward bottom-right
            k = cl(((xx / W) * 0.6 + (yy / H) * 0.8) - 0.55)
            r = 1 + 6 * k
            if k > 0: d.ellipse([xx - r, yy - r, xx + r, yy + r], fill=mix(T["bg"], T["acc"], 0.10 if light else 0.16))
    d.rectangle([0, 0, 10, H], fill=T["acc"])
    return im
BG = {id(DARK): build_bg(DARK, False), id(LIGHT): build_bg(LIGHT, True)}
rng = np.random.default_rng(6); GRAIN = []
for _ in range(8):
    g = rng.normal(0, 1, (H // 4, W // 4)).astype(np.float32)
    g = np.array(Image.fromarray(((g * 40) + 128).clip(0, 255).astype(np.uint8)).resize((W, H), Image.BICUBIC), dtype=np.float32) - 128
    GRAIN.append((g * 0.09)[..., None])

def caption_at(si, u):
    a, b = SC[si][0], SC[si][1]; vo = SC[si][6]; dur = b - a - 0.4; tot = sum(len(s) for s in vo); t = 0.15
    for s in vo:
        d = dur * len(s) / tot
        if t <= u < t + d: return s, cl((u - t) / 0.15) * cl((t + d - u) / 0.15)
        t += d
    return None, 0

def chrome(d, T, label, prog, demo):
    text(d, M, 96, "DOGETLAWYER", F(MONO_B, 26), T["acc"], tr=3)
    text(d, W - M, 96, "CASE FILE № 06", F(MONO, 24), T["dim"], tr=2, align="r")
    f = F(MONO_B, 22); w = tw(f, label, 2) + 40
    d.rectangle([M, 150, M + w, 196], fill=T["fg"]); text(d, M + 20, 160, label, f, T["bg"], tr=2)
    if prog is not None:
        for k in range(5):
            x = W - M - (5 - k) * 56 + 8
            d.rectangle([x, 164, x + 44, 182], fill=T["acc"] if k < prog else T["edge"])
    d.rectangle([M, 1490, W - M, 1491], fill=T["line"])
    if demo: text(d, M, 1820, "FICTIONAL DEMO EXAMPLE", F(MONO, 22), T["dim"], tr=2)
    text(d, W - M, 1820, "dogetlawyer.com", F(MONO, 22), T["dim"], tr=1, align="r")

def draw_caption(d, T, s, al):
    if not s or al <= 0: return
    f = F(CAP, 44); ls = wrap(f, s, CW - 60); y0 = 1560 - (len(ls) - 1) * 30
    for i, l in enumerate(ls): text(d, W / 2, y0 + i * 60, l, f, mix(T["bg"], T["fg"], al), align="c")

def render_scene(si, t):
    a, b, T, label, prog, demo, vo, fn = SC[si]
    im = BG[id(T)].copy(); c = Ctx(im, T, t - a); fn(c)
    chrome(c.d, T, label, prog, demo); s, al = caption_at(si, t - a); draw_caption(c.d, T, s, al)
    return im

def frame(i):
    t = i / FPS; si = max(k for k, s in enumerate(SC) if t >= s[0]); a, b = SC[si][0], SC[si][1]
    im = render_scene(si, t)
    if si + 1 < len(SC) and t > b - XF / 2: im = Image.blend(im, render_scene(si + 1, t), eio((t - (b - XF / 2)) / XF))
    elif si > 0 and t < a + XF / 2: im = Image.blend(render_scene(si - 1, t), im, eio((t - (a - XF / 2)) / XF))
    return (np.asarray(im, dtype=np.float32) + GRAIN[i % 8]).clip(0, 255).astype(np.uint8)

if __name__ == "__main__":
    if sys.argv[1] == "preview":
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
