"""Dogetlawyer Case File 10 - "FINAL. FINAL2. FINAL_ACTUALLY_FINAL." Which version did you sign? (Short 11).
Format: spot-the-difference game (3 rounds) + 3 checks. Colour per section (calm, dark grounds).
Type: Bricolage Grotesque ExtraBold / Outfit / Fira Code / Libre Baskerville (documents + italic asides).
Usage: python3 render10.py info | preview T... | chunk START END OUT.mp4
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, ".."))
import numpy as np
from PIL import Image
import engine as E
from engine import M, W, H, CW, F, tw, text, wrap, tick, cross, win, close_card
from multitheme import gradient, hexc, mix

SECTIONS = [
 ("Hook · charcoal & ember",     "#232129", "#3E1A08", "#FFFFFF", "#FF8A3D", "#8BF0BC"),
 ("Game · deep navy & teal",     "#081B36", "#0B3A3E", "#FFFFFF", "#5CF2D6", "#8BF0BC"),
 ("The law · aubergine",         "#341043", "#12081D", "#FFFFFF", "#FFC94D", "#8BF0BC"),
 ("The fix · bottle green",      "#0F3A2B", "#141E26", "#FFFFFF", "#B6FF6B", "#B6FF6B"),
]
MAP = [0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 3, 3, 3, 3, 0, 0]
PAPER = hexc("#FBFAF7"); INK = hexc("#1A1A1A"); GREY = hexc("#77736C"); HL = hexc("#FFE08A")
DOC = "LibreBaskerville_400Regular"; DOC_B = "LibreBaskerville_700Bold"

def bg(T):
    im = gradient(T, W, H); a = np.asarray(im, dtype=np.float32)
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    g = np.exp(-(((x - W * 0.85) / (W * 0.6)) ** 2 + ((y - H * 0.12) / (H * 0.35)) ** 2))[..., None]
    a = a + (np.array(T["acc"], np.float32) - a) * g * 0.10      # soft glow, top right
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))

E.configure(os.path.join(HERE, "f"),
            ("BricolageGrotesque_800ExtraBold", "Outfit_500Medium", "Outfit_800ExtraBold", "FiraCode_400Regular", "FiraCode_600SemiBold",
             "LibreBaskerville_400Regular_Italic", "Outfit_700Bold"),
            "CASE FILE 10", SECTIONS, MAP, bg)
E.LHK = 1.34

# ---------------------------------------------------------------- helpers
def file_row(c, y, name, t0, hot=False):
    al = c.a(t0)
    if al <= 0: return
    c.d.rounded_rectangle([M, y, W - M, y + 120], radius=18, fill=c.c("panel", al), outline=c.c("acc" if hot else "edge", al), width=3 if hot else 2)
    # document icon
    c.d.rounded_rectangle([M + 30, y + 22, M + 92, y + 98], radius=6, fill=c.c(PAPER, al))
    for k in range(3): c.d.rectangle([M + 42, y + 44 + k * 14, M + 80, y + 48 + k * 14], fill=c.c(GREY, al))
    f = F(E.MONO_B, 36)
    while tw(f, name) > CW - 160: f = F(E.MONO_B, f.size - 2)
    text(c.d, M + 120, y + 38, name, f, c.c("acc" if hot else "fg", al))

def clause(c, y, label, words, hl, t0, t_hl, hcol=HL):
    """Paper card with a clause; words in hl get highlighted from t_hl."""
    al = c.a(t0)
    if al <= 0: return y
    f = F(DOC, 40); maxw = CW - 90; lines = [[]]; cur = 0
    for i, w_ in enumerate(words):
        ww = tw(f, w_ + " ")
        if cur + ww > maxw and lines[-1]: lines.append([]); cur = 0
        lines[-1].append((i, w_)); cur += ww
    h = 90 + len(lines) * 58 + 30
    c.d.rounded_rectangle([M, y, W - M, y + h], radius=20, fill=c.c(PAPER, al))
    text(c.d, M + 40, y + 28, label, F(E.MONO_B, 24), c.c(GREY, al), tr=2)
    hal = c.a(t_hl, 0.3)
    yy = y + 84
    for ln in lines:
        x = M + 44
        for i, w_ in ln:
            wd = tw(f, w_)
            if i in hl and hal > 0:
                c.d.rounded_rectangle([x - 6, yy - 4, x + wd + 6, yy + 50], radius=6, fill=c.c(mix(PAPER, hcol, hal), al))
            text(c.d, x, yy, w_, F(DOC_B, 40) if (i in hl and hal > 0.5) else f, c.c(INK, al))
            x += tw(f, w_ + " ")
        yy += 58
    return y + h

def round_(n, a_words, b_words, hl, verdict, sub):
    def fn(c):
        c.pill(f"ROUND {n} OF 3", M, 290, 0.0, size=28)
        c.mono("SPOT THE DIFFERENCE", W - M, 302, 24, 0.0, align="r")
        y = clause(c, 400, "VERSION 3 · SENT TUESDAY", a_words, hl, 0.2, 4.4)
        y = clause(c, y + 30, "VERSION 4 · SENT THURSDAY", b_words, hl, 0.5, 4.4)
        # countdown 3-2-1 (fades only)
        for k, num in enumerate("321"):
            t0 = 1.4 + k * 1.0; al = min(c.a(t0, 0.2), 1 - c.a(t0 + 0.8, 0.2))
            if al > 0: text(c.d, W / 2, y + 40, num, F(E.HEAD, 200), c.c("acc", al), align="c")
        c.head([verdict], y + 70, 110, 4.6, role="acc", maxw=CW)
        c.para(sub, y + 220, 40, 5.0, role="mut", fn=E.SERIF)
    return fn

# ---------------------------------------------------------------- scenes
def s1(c):
    c.mono("SHARED DRIVE · CONTRACTS", M, 420, 26, 0.0)
    for i, n in enumerate(["Contract_FINAL.docx", "Contract_FINAL2.docx", "Contract_FINAL_ACTUALLY_FINAL.docx"]):
        file_row(c, 480 + i * 150, n, 0.2 + i * 0.9, hot=(i == 2))
    c.head(["FINAL.", "FINAL2.", "FINAL_ACTUALLY", "_FINAL."], 980, 120, 0.4, role=["fg", "fg", "acc", "acc"], stag=0.9)

def s2(c):
    c.mono("QUICK QUESTION", M, 520, 30, 0.0)
    c.head(["WHICH ONE", "DID YOU", "SIGN?"], 590, 220, 0.15, role=["fg", "fg", "acc"])

def s3(c):
    c.head(["EVERYONE", "HAS THE", "CONTRACT."], 400, 170, 0.0)
    c.head(["NOT EVERYONE", "HAS THE", "SAME ONE."], 900, 150, 1.4, role=["fg", "fg", "acc"])

def s4(c):
    c.mono("LET’S PLAY", M, 460, 30, 0.0)
    c.head(["SPOT THE", "DIFFERENCE."], 530, 170, 0.15, role=["fg", "acc"])
    c.para("Three rounds. Three seconds each. Go.", 960, 48, 1.2, role="mut", fn=E.SERIF)

def s8(c):
    c.mono("NOBODY SENT YOU A LIST OF CHANGES", M, 440, 28, 0.0)
    c.head(["ONE WORD.", "ONE NUMBER.", "DIFFERENT", "DEAL."], 510, 190, 0.15, role=["fg", "fg", "fg", "acc"])

def s9(c):
    c.mono("THE CATCH", M, 330, 30, 0.0)
    yb = c.head(["THE SIGNED", "ONE IS", "USUALLY", "THE DEAL."], 400, 170, 0.15, role=["fg", "fg", "fg", "acc"])
    al = c.a(1.6)
    if al > 0:
        y0 = yb + 70
        c.d.rounded_rectangle([M, y0, W - M, y0 + 300], radius=20, fill=c.c(PAPER, al))
        text(c.d, M + 40, y0 + 30, "12. ENTIRE AGREEMENT", F(E.MONO_B, 26), c.c(GREY, al), tr=2)
        yy = y0 + 84
        for l in wrap(F(DOC, 36), "This agreement is the entire agreement between the parties and supersedes all previous drafts, discussions and correspondence.", CW - 90):
            text(c.d, M + 44, yy, l, F(DOC, 36), c.c(INK, al)); yy += 52
    c.mono("TYPICAL WORDING · FICTIONAL EXAMPLE", M, yb + 400, 22, 1.8)

def s10(c):
    c.mono("AND CLICKING “SIGN” ON A SCREEN?", M, 340, 28, 0.0)
    c.head(["IT USUALLY", "COUNTS."], 410, 200, 0.15, role=["fg", "acc"])
    al = c.a(1.2)
    if al > 0:
        y0 = 860
        c.d.rounded_rectangle([M, y0, W - M, y0 + 330], radius=24, fill=c.c(PAPER, al))
        c.d.rectangle([M, y0, M + 14, y0 + 330], fill=c.c("acc", al))
        yy = y0 + 46
        for l in wrap(F(E.SERIF, 44), "“An electronic signature is capable in law of being used to execute a document (including a deed) provided that …”", CW - 100):
            text(c.d, M + 56, yy, l, F(E.SERIF, 44), c.c(INK, al)); yy += 62
    c.mono("SOURCE: LAW COMMISSION · ELECTRONIC EXECUTION", M, 1220, 24, 1.4, role="acc", fn=E.MONO_B)
    c.mono("OF DOCUMENTS (2019) · ENGLAND & WALES", M, 1260, 24, 1.4, role="acc", fn=E.MONO_B)
    c.para("…the signer intends to authenticate it and any formalities are met.", 1310, 32, 1.6, role="mut")

def s11(c):
    c.mono("BEFORE YOU SIGN", M, 500, 30, 0.0)
    c.head(["3 QUICK", "CHECKS."], 570, 260, 0.15, role=["fg", "acc"])

def s12(c):
    c.mono("BEFORE YOU SIGN", M, 330, 28, 0.0)
    steps = [("Ask what’s changed", "Since the last version. In writing."),
             ("Read the one you’re signing", "Not the one you remember."),
             ("Save the signed copy", "Dated, where everyone can find it.")]
    y = 420
    for i, (h, s) in enumerate(steps):
        tt = 0.3 + i * 2.6
        al = c.a(tt)
        if al > 0:
            text(c.d, M, y - 10, f"0{i + 1}", F(E.HEAD, 120), c.c("acc", al))
        c.para(h, y + 150, 56, tt, role="fg", fn=E.BODY_B)
        c.para(s, y + 225, 40, tt + 0.2, role="mut")
        y += 330
    tick(c, W - M - 90, 440, 70, 1.0); tick(c, W - M - 90, 770, 70, 3.6); tick(c, W - M - 90, 1100, 70, 6.2)

def s13(c):
    c.mono("THAT’S WHAT DOGETLAWYER IS FOR", M, 330, 26, 0.0, role="acc", fn=E.MONO_B)
    win(c, 0.2, "SIGNED VERSIONS · ALL CONTRACTS", 400, 1200)
    rows = [("Ellison Freight", "SIGNED VERSION", "v4 · 12 Aug 2026", "ok"),
            ("Marlow Studio", "SIGNED VERSION", "v2 · 3 Jun 2026", "ok"),
            ("Pell & Hart Supplies", "NOT SIGNED YET", "Draft v3", "acc")]
    y = 520
    for i, (n, lab, v, r) in enumerate(rows):
        tt = 0.7 + i * 0.5
        c.para(n, y, 42, tt, role="fg", fn=E.BODY_B, x=M + 40)
        c.mono(lab, M + 40, y + 66, 22, tt, tr=2)
        c.para(v, y + 58, 36, tt, role=r, fn=E.BODY_B, x=W - M - 40 - tw(F(E.BODY_B, 36), v))
        al = c.a(tt)
        if i < 2 and al > 0: c.d.rectangle([M + 40, y + 140, W - M - 40, y + 141], fill=c.c("line", al))
        y += 200
    c.para("So nobody’s working from FINAL2.", 1250, 46, 2.2, role="mut", fn=E.SERIF)

def s14(c):
    c.head(["ONE", "CONTRACT.", "ONE", "VERSION."], 470, 220, 0.0, role=["fg", "fg", "fg", "acc"])

def s15(c):
    c.mono("BE HONEST", M, 480, 30, 0.0)
    c.head(["MOST “FINALS”", "YOU’VE SEEN", "ON ONE FILE?"], 550, 150, 0.15, role=["fg", "fg", "acc"])
    for i, n in enumerate(["2", "3", "4", "5+"]):
        tt = 1.2 + i * 0.2; a = c.a(tt)
        if a <= 0: continue
        x = M + i * 230
        c.d.rounded_rectangle([x, 1060, x + 190, 1240], radius=24, fill=c.c("panel", a), outline=c.c("acc", a), width=4)
        f = F(E.HEAD, 110)
        text(c.d, x + 95, 1150 - (f.getbbox(n)[1] + f.getbbox(n)[3]) / 2, n, f, c.c("acc", a), align="c")
    c.mono("COMMENT THE NUMBER", M, 1280, 26, 2.0)

def close(c):
    close_card(c, ["KNOW WHICH", "ONE YOU", "SIGNED."], "Every contract. The signed version. One place.")

W_ = str.split
SCENES = [
    (3.8, "THE FILES", False, ["Final. Final two. Final, actually final."], s1),
    (4.0, "THE FILES", False, ["Quick question. Which one did you actually sign?"], s2),
    (4.6, "THE FILES", False, ["Everyone's got the contract. Not everyone's got the same one."], s3),
    (4.2, "THE GAME", False, ["Let's play spot the difference. Three seconds each."], s4),
    (8.8, "ROUND 1", True, ["Round one. Version three, and version four. Spotted it?", "Thirty days became sixty. That's a month longer to get paid."],
     round_(1, W_("The Customer shall pay each invoice within 30 days of the invoice date."),
               W_("The Customer shall pay each invoice within 60 days of the invoice date."), {7}, "30 BECAME 60.", "A month longer to get paid.")),
    (8.8, "ROUND 2", True, ["Round two. Look closely.", "One month's notice became three. That's two extra months you're locked in."],
     round_(2, W_("Either party may end this agreement by giving one month's written notice."),
               W_("Either party may end this agreement by giving three months' written notice."), {8, 9}, "1 MONTH BECAME 3.", "Two extra months locked in.")),
    (8.8, "ROUND 3", True, ["Round three. The cap on what they'd pay if it goes wrong.", "Now it's only the last three months' fees."],
     round_(3, W_("Our total liability is limited to the fees paid under this agreement."),
               W_("Our total liability is limited to the fees paid in the last three months."), {9, 10, 11, 12, 13}, "THE CAP SHRANK.", "Only the last three months’ fees.")),
    (6.0, "THE GAME", False, ["One word. One number. A different deal.", "And nobody sent you a list of changes."], s8),
    (9.6, "THE CATCH", False, ["Here's the catch. Lots of contracts have an entire agreement clause. It says the signed document is the whole deal.",
                               "So what you agreed in an email may not count."], s9),
    (7.4, "THE CATCH", False, ["And clicking sign on a screen usually counts too.", "The Law Commission says an electronic signature can be used to sign a document."], s10),
    (5.2, "3 CHECKS", False, ["So before you sign, three quick checks."], s11),
    (10.4, "3 CHECKS", False, ["One. Ask what's changed since the last version, in writing.", "Two. Read the version you're signing, not the one you remember.",
                               "Three. Save the signed copy, dated, where everyone can find it."], s12),
    (9.2, "THE FIX", True, ["That's what Dogetlawyer is for. Every contract in one place,", "with the signed version on record, and the date it was signed. So nobody's working from final two."], s13),
    (3.8, "THE FIX", False, ["One contract. One version."], s14),
    (5.0, "YOUR TURN", False, ["Be honest. What's the most finals you've seen on one file? Comment the number."], s15),
    (5.4, "DOGETLAWYER", False, ["Keep track of what you signed at dogetlawyer.com. Link in bio."], close),
]
E.build(SCENES)
if __name__ == "__main__": E.main(HERE, os.path.join(HERE, "..", "vo10.json"))
