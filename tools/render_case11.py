"""Dogetlawyer Case File 11 - "To the wrong Sarah." Emailing contracts full of personal data (Short 13, Data & privacy).
Retention format (engine v3): hook on frame 0, problem named by ~10 s, quick cuts, sound-off captions. ~1:17.
Type: Sora ExtraBold / Figtree / Spline Sans Mono / Crimson Pro italic. Colour per section.
Usage: python3 render11.py info | preview T... | chunk START END OUT.mp4
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, ".."))
import numpy as np
from PIL import Image
import engine3 as E
from engine3 import M, W, H, CW, F, tw, text, wrap, tick, cross, win, close_card
from multitheme import gradient, hexc, mix

SECTIONS = [
 ("Hook · graphite & cobalt",   "#16181F", "#0F2C70", "#FFFFFF", "#FF6B5C", "#7CFFB2"),
 ("The rule · teal ink",        "#06323A", "#0A171C", "#FFFFFF", "#FFD166", "#8BF0BC"),
 ("3 checks · midnight violet", "#2A1561", "#0F0B26", "#FFFFFF", "#9BE8FF", "#8BF0BC"),
]
MAP = [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 0, 0]
PAPER = hexc("#FBFAF7"); INK = hexc("#1A1A1A"); GREY = hexc("#77736C")

def bg(T):
    im = gradient(T, W, H); a = np.asarray(im, dtype=np.float32)
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    v = 1 - 0.28 * np.clip(((x - W / 2) / (W * 0.75)) ** 2 + ((y - H * 0.42) / (H * 0.62)) ** 2, 0, 1)   # soft vignette
    return Image.fromarray((a * v[..., None]).clip(0, 255).astype(np.uint8))

E.configure(os.path.join(HERE, "f"),
            ("Sora_800ExtraBold", "Figtree_500Medium", "Figtree_800ExtraBold", "SplineSansMono_400Regular", "SplineSansMono_600SemiBold",
             "CrimsonPro_500Medium_Italic", "Figtree_900Black"),
            "CASE FILE 11", SECTIONS, MAP, bg)
E.LHK = 1.30

def email(c, y0, t0, to_name, to_addr, wrong=False, t_wrong=99):
    al = c.a(t0)
    if al <= 0: return
    c.d.rounded_rectangle([M, y0, W - M, y0 + 330], radius=24, fill=c.c(PAPER, al))
    text(c.d, M + 40, y0 + 34, "To:", F(E.MONO_B, 30), c.c(GREY, al))
    text(c.d, M + 110, y0 + 30, to_name, F(E.BODY_B, 38), c.c(INK, al))
    text(c.d, M + 110, y0 + 80, to_addr, F(E.MONO, 28), c.c(GREY, al))
    wa = c.a(t_wrong)
    if wrong and wa > 0:
        c.d.rounded_rectangle([M + 100, y0 + 22, W - M - 30, y0 + 120], radius=12, outline=c.c(hexc("#E5322D"), wa), width=5)
    c.d.rectangle([M + 40, y0 + 140, W - M - 40, y0 + 142], fill=c.c(hexc("#DDDDDD"), al))
    text(c.d, M + 40, y0 + 166, "Subject: Signed contract, as discussed", F(E.BODY, 32), c.c(INK, al))
    c.d.rounded_rectangle([M + 40, y0 + 230, M + 520, y0 + 300], radius=14, fill=c.c(hexc("#EFECE6"), al))
    text(c.d, M + 64, y0 + 248, "Contract_signed.pdf", F(E.MONO_B, 28), c.c(INK, al))

# ---------------------------------------------------------------- scenes
def s1(c):
    email(c, 330, 0.0, "Sarah B…", "sarah.bentley@…", wrong=False)
    c.head(["SENT."], 760, 300, 0.0, role="acc")
    c.para("A signed contract. Gone.", 1130, 50, 0.0, role="mut", fn=E.SERIF)

def s2(c):
    email(c, 330, 0.0, "Sarah Bentley", "sarah.bentley@brightwell…", wrong=True, t_wrong=0.3)
    c.mono("YOU MEANT SARAH BENNETT", M, 700, 28, 0.3, role="acc", fn=E.MONO_B)
    c.head(["TO THE", "WRONG", "SARAH."], 770, 190, 0.2, role=["fg", "fg", "acc"], stag=0.15)

def s3(c):
    c.mono("WHAT WAS IN IT?", M, 330, 30, 0.0)
    items = ["Home address", "Bank details", "Signature", "Date of birth"]
    y = 410
    for i, it in enumerate(items):
        tt = 0.2 + i * 0.55; al = c.a(tt)
        if al <= 0: continue
        c.d.rounded_rectangle([M, y + c.off(tt), W - M, y + 170 + c.off(tt)], radius=22, fill=c.c("panel", al), outline=c.c("acc", al), width=3)
        text(c.d, M + 44, y + 42 + c.off(tt), it.upper(), F(E.HEAD, 72), c.c("fg", al))
        y += 200

def s4(c):
    c.mono("THAT’S A", M, 420, 32, 0.0)
    c.head(["PERSONAL", "DATA", "BREACH."], 480, 210, 0.1, role=["fg", "fg", "acc"], stag=0.15)
    c.para("And it’s easier to do than you think.", 1220, 46, 1.4, role="mut", fn=E.SERIF)

def s5(c):
    c.mono("THE UK’S DATA WATCHDOG USES THIS EXACT EXAMPLE", M, 320, 24, 0.0, role="acc", fn=E.MONO_B)
    al = c.a(0.2)
    if al > 0:
        y0 = 390
        c.d.rounded_rectangle([M, y0, W - M, y0 + 520], radius=24, fill=c.c(PAPER, al))
        c.d.rectangle([M, y0, M + 14, y0 + 520], fill=c.c("acc", al))
        y = y0 + 50
        q = "“If you think you’ve had a personal data breach – perhaps an email has been sent to the wrong person, a laptop was stolen from a car or you’ve lost files because of a flood – … we can help.”"
        for l in wrap(F(E.SERIF, 50), q, CW - 100):
            text(c.d, M + 56, y, l, F(E.SERIF, 50), c.c(INK, al)); y += 64
    c.mono("SOURCE: ICO · 72 HOURS – HOW TO RESPOND TO A", M, 950, 24, 0.6)
    c.mono("PERSONAL DATA BREACH (ADVICE FOR SMALL ORGANISATIONS)", M, 988, 24, 0.6)
    c.head(["“AN EMAIL SENT TO", "THE WRONG PERSON.”"], 1090, 76, 1.6, role="acc")

def s6(c):
    c.mono("IF IT’S LIKELY TO PUT PEOPLE AT RISK", M, 330, 28, 0.0)
    c.head(["72"], 390, 420, 0.1, role="acc")
    c.head(["HOURS."], 860, 170, 0.3)
    c.para("You may have to report it to the ICO, without undue delay and within 72 hours where feasible.", 1100, 40, 0.8, role="mut")

def s7(c):
    c.mono("AND YES", M, 520, 32, 0.0)
    c.head(["WEEKENDS", "COUNT."], 590, 220, 0.1, role=["fg", "acc"], stag=0.2)
    c.para("The clock runs from when you become aware of it.", 1110, 44, 0.8, role="mut", fn=E.SERIF)

def s8(c):
    c.mono("AND “PERSONAL DATA” ISN’T JUST BANK DETAILS", M, 330, 26, 0.0)
    words = [("NAMES", 0.2), ("ADDRESSES", 0.6), ("EMAILS", 1.0), ("SIGNATURES", 1.4), ("PHONE NUMBERS", 1.8)]
    y = 410
    for w_, tt in words:
        c.head([w_], y, 120, tt, role="fg"); y += 150
    c.para("Contracts are full of it.", 1200, 52, 2.6, role="acc", fn=E.SERIF)

def s9(c):
    c.mono("BEFORE YOU HIT SEND", M, 480, 32, 0.0)
    c.head(["3 QUICK", "CHECKS."], 550, 250, 0.1, role=["fg", "acc"], stag=0.2)

def check(n, title, sub, extra):
    def fn(c):
        c.pill(f"CHECK {n} OF 3", M, 300, 0.0, size=28)
        yb = c.head(title, 410, 160, 0.1, role=["fg"] * (len(title) - 1) + ["acc"], stag=0.15)
        yb = c.para(sub, yb + 50, 44, 0.6, role="mut")
        extra(c, yb + 50)
    return fn

def x_auto(c, y):
    rows = [("Sarah Bennett", "sarah.bennett@kitecodesign…", True), ("Sarah Bentley", "sarah.bentley@brightwell…", False)]
    for i, (n, a, ok) in enumerate(rows):
        tt = 1.2 + i * 0.4; al = c.a(tt)
        if al <= 0: continue
        yy = y + i * 150
        c.d.rounded_rectangle([M, yy, W - M, yy + 130], radius=18, fill=c.c(PAPER, al))
        text(c.d, M + 36, yy + 20, n, F(E.BODY_B, 38), c.c(INK, al)); text(c.d, M + 36, yy + 74, a, F(E.MONO, 26), c.c(GREY, al))
        (tick if ok else cross)(c, W - M - 100, yy + 34, 60, tt + 0.3, role="ok" if ok else hexc("#E5322D"))

def x_strip(c, y):
    rows = [("Signed contract", True), ("Passport copy", False), ("Full bank details", False)]
    for i, (n, keep) in enumerate(rows):
        tt = 1.2 + i * 0.5; al = c.a(tt)
        if al <= 0: continue
        yy = y + i * 120
        f = F(E.BODY_B, 46); text(c.d, M, yy, n, f, c.c("fg" if keep else "dim", al))
        if keep: tick(c, W - M - 80, yy, 56, tt + 0.2)
        else:
            sa = c.a(tt + 0.5)
            if sa > 0: c.d.rectangle([M - 6, yy + 30, M + tw(f, n) + 6, yy + 36], fill=c.c("acc", sa))

def x_log(c, y):
    for i, n in enumerate(["What happened", "Who it affected", "What you did about it"]):
        tt = 1.2 + i * 0.5
        tick(c, M, y + i * 100 + 6, 44, tt)
        c.para(n, y + i * 100, 46, tt, role="fg", fn=E.BODY_B, x=M + 76)
    c.mono("UK GDPR ART. 33(5): RECORD EVERY BREACH, REPORTED OR NOT", M, y + 330, 22, 2.8)

def s13(c):
    c.mono("FEWER ATTACHMENTS FLYING ABOUT", M, 300, 26, 0.0, role="acc", fn=E.MONO_B)
    win(c, 0.2, "ALL CONTRACTS · ONE PLACE", 370, 1180)
    rows = [("Brightwell Retail", "Supply agreement", "Owner: J. Okafor"), ("Kite & Co Design", "Design services", "Owner: S. Bennett"),
            ("Unit 4, Mill Lane", "Lease", "Owner: P. Hale")]
    y = 490
    for i, (n, typ, own) in enumerate(rows):
        tt = 0.6 + i * 0.4
        c.para(n, y, 42, tt, role="fg", fn=E.BODY_B, x=M + 40)
        c.mono(typ.upper(), M + 40, y + 64, 22, tt, tr=2)
        c.para(own, y + 56, 32, tt, role="acc", fn=E.BODY_B, x=W - M - 40 - tw(F(E.BODY_B, 32), own))
        al = c.a(tt)
        if i < 2 and al > 0: c.d.rectangle([M + 40, y + 140, W - M - 40, y + 141], fill=c.c("line", al))
        y += 210
    c.para("Every contract in one place, with someone responsible for each.", 1230, 42, 1.8, role="mut", fn=E.SERIF)

def s14(c):
    c.mono("BE HONEST", M, 420, 32, 0.0)
    c.head(["EVER SENT ONE", "TO THE WRONG", "PERSON?"], 490, 150, 0.1, role=["fg", "fg", "acc"], stag=0.15)
    for i, n in enumerate(["YES", "NO"]):
        tt = 1.0 + i * 0.2; a = c.a(tt)
        if a <= 0: continue
        x = M + i * 470
        c.d.rounded_rectangle([x, 1000, x + 440, 1180], radius=28, fill=c.c("panel", a), outline=c.c("acc", a), width=4)
        text(c.d, x + 220, 1040, n, F(E.HEAD, 96), c.c("acc", a), align="c")
    c.mono("TELL US IN THE COMMENTS", M, 1220, 26, 1.6)

def close(c):
    close_card(c, ["CHECK THE NAME.", "THEN HIT SEND."], "Every contract. One place.")

SCENES = [
    (2.8, "SENT", False, ["You just emailed a signed contract."], s1),
    (3.4, "SENT", False, ["To the wrong Sarah."], s2),
    (4.4, "SENT", False, ["Home address. Bank details. Signature. Date of birth."], s3),
    (4.6, "SENT", False, ["That's a personal data breach. And it's easier to do than you think."], s4),
    (7.0, "THE RULE", False, ["Even the ICO, the UK's data watchdog, uses this exact example.", "An email sent to the wrong person."], s5),
    (6.2, "THE RULE", False, ["If it's likely to put people at risk, you may have to report it to the ICO.", "Within seventy-two hours."], s6),
    (4.2, "THE RULE", False, ["And yes, weekends count. The clock starts when you find out."], s7),
    (5.8, "THE RULE", False, ["And personal data isn't just bank details.", "Names, addresses, emails, signatures. Contracts are full of it."], s8),
    (3.2, "3 CHECKS", False, ["So before you hit send, three quick checks."], s9),
    (6.6, "CHECK 1", True, ["One. Check the full email address.", "Not just the first name autocomplete gives you."],
     check(1, ["CHECK THE", "FULL ADDRESS."], "Not just the first name autocomplete picks.", x_auto)),
    (7.0, "CHECK 2", True, ["Two. Only send what's needed.", "Do they really need the passport copy and the bank details?"],
     check(2, ["ONLY SEND", "WHAT’S NEEDED."], "If they don’t need it, don’t attach it.", x_strip)),
    (6.8, "CHECK 3", False, ["Three. If it does go wrong, write it down.", "What happened, who it affected, and what you did about it."],
     check(3, ["WRITE IT", "DOWN."], "If it goes wrong, keep a record.", x_log)),
    (7.6, "ONE PLACE", True, ["And fewer attachments flying about helps too.", "Dogetlawyer keeps every contract in one place, with someone responsible for each one."], s13),
    (4.2, "YOUR TURN", False, ["Be honest. Ever sent one to the wrong person? Yes or no."], s14),
    (5.0, "DOGETLAWYER", False, ["Check the name. Then hit send. Dogetlawyer dot com, link in bio."], close),
]
E.build(SCENES)
if __name__ == "__main__": E.main(HERE, os.path.join(HERE, "..", "vo11.json"))
