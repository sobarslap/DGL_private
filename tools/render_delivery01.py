"""Dogetlawyer Delivery 01 - Matter & Assurance and Upload & Go (PREVIEW) for UK legal professionals. 3-minute Short.
Follows the boss's master script (02_THREE_MINUTE_MASTER_SCRIPT.md) scene by scene; each scene is split into 4-9 s cuts.
Retention format (engine v3): hook on frame 0, slide-up entrances, slow punch-in, sound-off captions. Runtime 179.5 s.
Type: Spectral ExtraBold / Figtree / Red Hat Mono / Newsreader italic. Colour per section, not per scene.
Usage: python3 render_d01.py info | preview T... | chunk START END OUT.mp4
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, ".."))
import numpy as np
from PIL import Image
import engine3 as E
from engine3 import M, W, H, CW, F, tw, text, wrap, tick, cross, win
from multitheme import gradient, hexc, mix
import dhelp as D
from dhelp import PAPER, INK, GREY, RULE, RED, HIL, card, ptext, chip, arrow

SECTIONS = [
 ("The draft · oxblood & ink",   "#4A1020", "#120A10", "#FFFFFF", "#FFC2A6", "#8BF0BC"),
 ("The workflow · deep navy",    "#0E2448", "#071228", "#FFFFFF", "#7FD3FF", "#8BF0BC"),
 ("The law · forest & ink",      "#0F3A2C", "#06130E", "#FFFFFF", "#E9D27A", "#9BF0C0"),
 ("Controls · slate & lilac",    "#2A2E40", "#0C0D14", "#FFFFFF", "#C9B8FF", "#8BF0BC"),
]
#        h1 h2 h3 4a 4b 5a 5b 5c 5d 6a 6b 7a 7b 7c 8a 8b 9a 9b 10a 10b 11a 11b 11c 12a 12b 12c 13 14
MAP = [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 3, 3, 2, 2, 2, 0, 0, 0, 0, 0]

def bg(T):
    im = gradient(T, W, H); a = np.asarray(im, dtype=np.float32)
    line = np.array(T["fg"], np.float32); k = 0.035
    for x in range(M - 30, W, 120):                    # faint dot grid, like ruled legal paper
        for y in range(270, H - 120, 120): a[y:y + 3, x:x + 3] = a[y:y + 3, x:x + 3] * (1 - k * 4) + line * k * 4
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))

E.configure(os.path.join(HERE, "f"),
            ("Spectral_800ExtraBold", "Figtree_500Medium", "Figtree_700Bold", "RedHatMono_400Regular", "RedHatMono_700Bold",
             "Newsreader_500Medium_Italic", "Figtree_800ExtraBold"),
            "MATTER & ASSURANCE", SECTIONS, MAP, bg)
E.LHK = 1.42
D.install("MATTER & ASSURANCE")
X0, X1 = M, W - M

# ---------------------------------------------------------------- hook
def h1(c):
    card(c, X0, 300, X1, 820, 0.0)
    ptext(c, "INBOX · TODAY 17:40", X0 + 40, 330, 24, 0.0, fn=E.MONO_B, col=GREY)
    c.d.ellipse([X1 - 70, 334, X1 - 46, 358], fill=RED)
    ptext(c, "Harbour Studio Ltd (client)", X0 + 40, 385, 40, 0.0, fn=E.BODY_B)
    ptext(c, "RE: Services agreement - revised draft v2", X0 + 40, 445, 32, 0.0)
    c.d.rectangle([X0 + 40, 505, X1 - 40, 507], fill=RULE)
    ptext(c, "“Can I sign this today?”", X0 + 40, 535, 58, 0.0, fn=E.SERIF)
    c.d.rounded_rectangle([X0 + 40, 650, X0 + 520, 720], radius=14, fill=hexc("#EFEBE3"))
    ptext(c, "Services_Agreement_v2.docx", X0 + 64, 670, 26, 0.0, fn=E.MONO_B)
    ptext(c, "Fictional client and documents", X0 + 40, 755, 24, 0.0, col=GREY)
    c.head(["CAN THEY SIGN?"], 900, 150, 0.0, role="acc")
    c.mono("IT’S FIVE FORTY. A REVISED AGREEMENT JUST LANDED.", M, 1110, 26, 0.0, role="mut", fn=E.MONO_B)

def h2(c):
    c.head(["WHICH CLAUSE", "CHANGED?"], 290, 120, 0.0, role=["fg", "acc"], stag=0.1)
    for i, (tag, body, extra) in enumerate([("VERSION A · CLAUSE 8.2", "The Supplier’s aggregate liability under or in connection with this agreement is limited to £10,000.", None),
                                            ("VERSION B · CLAUSE 8.2", "The Supplier’s aggregate liability under or in connection with this agreement is limited to £10,000,", "subject to clause 8.3.")]):
        y0 = 600 + i * 420; t0 = 0.2 + i * 0.5
        card(c, X0, y0, X1, y0 + 380, t0)
        ptext(c, tag, X0 + 40, y0 + 30, 24, t0, fn=E.MONO_B, col=GREY)
        yb = ptext(c, body, X0 + 40, y0 + 80, 36, t0, maxw=CW - 80)
        if extra:
            al = c.a(t0 + 0.6)
            if al > 0:
                f = F(E.BODY_B, 36); c.d.rectangle([X0 + 34, yb + 2, X0 + 50 + tw(f, extra), yb + 50], fill=c.c(HIL, al))
                text(c.d, X0 + 40, yb + 4, extra, f, c.c(INK, al))
                chip(c, "CHANGED", X1 - 200, y0 + 22, t0 + 0.6, size=22, fill=RED, tcol=(255, 255, 255))

def h3(c):
    qs = [("1", "WHICH CLAUSE CHANGED?"), ("2", "WHO CHECKED IT?"), ("3", "WHAT EVIDENCE SUPPORTS", "THE ANSWER?")]
    y = 330
    for i, q in enumerate(qs):
        t0 = 0.0 + i * 0.35; al = c.a(t0)
        if al > 0:
            c.d.ellipse([M, y, M + 90, y + 90], outline=c.c("acc", al), width=5)
            text(c.d, M + 45, y + 12, q[0], F(E.HEAD, 56), c.c("acc", al), align="c")
        yy = c.head(list(q[1:]), y + 8, 74, t0, x=M + 130, maxw=CW - 130)
        y = yy + 110
    c.para("We’ll answer it with the fictional draft at the end of this video.", y + 20, 42, 1.4, role="mut", fn=E.SERIF)

# ---------------------------------------------------------------- the product
def s4a(c):
    c.mono("HERE’S WHAT WE’RE BUILDING", M, 330, 28, 0.0, role="acc", fn=E.MONO_B)
    c.head(["MATTER &", "ASSURANCE"], 400, 170, 0.1, stag=0.12)
    c.head(["+ UPLOAD & GO"], 830, 120, 0.6, role="acc")
    c.para("A legal matter and assurance workflow from Dogetlawyer. Not mergers and acquisitions.", 1040, 42, 1.0, role="mut")

def s4b(c):
    c.head(["PREVIEW."], 320, 230, 0.0, role="acc")
    rows = [("STATUS", "Product preview: proposed screens"), ("FIRST PILOT", "Solicitor firms"), ("JURISDICTION", "England and Wales")]
    y = 680
    for i, (k, v) in enumerate(rows):
        t0 = 0.4 + i * 0.4
        c.box(M, y, W - M, y + 170, t0, r=22)
        c.mono(k, M + 40, y + 30, 26, t0, role="acc", fn=E.MONO_B)
        c.para(v, y + 78, 46, t0, role="fg", fn=E.BODY_B, x=M + 40, maxw=CW - 80)
        y += 200

def step(n, title, ui):
    def fn(c):
        c.pill(f"STEP {n} OF 4", M, 290, 0.0, size=26)
        c.head(title, 380, 130, 0.1, role="fg")
        ui(c)
    return fn

def ui_matter(c):
    win(c, 0.3, "UPLOAD & GO · SELECT MATTER", 600, 1380)
    ms = [("Harbour Studio Ltd", "Services agreement · Commercial", True), ("Kestrel Foods Ltd", "Supply terms · Commercial", False), ("Northgate Lettings", "NDA · Commercial", False)]
    y = 700
    for i, (n, sub, sel) in enumerate(ms):
        t0 = 0.6 + i * 0.25; al = c.a(t0)
        if al <= 0: continue
        if sel: c.d.rounded_rectangle([M + 30, y - 20, W - M - 30, y + 170], radius=18, outline=c.c("acc", al), width=5)
        c.para(n, y, 46, t0, role="fg", fn=E.BODY_B, x=M + 60)
        c.para(sub, y + 70, 34, t0, role="mut", x=M + 60)
        if sel: tick(c, W - M - 130, y + 30, 60, t0 + 0.3)
        y += 220

def ui_upload(c):
    win(c, 0.3, "UPLOAD & GO · UPLOAD", 600, 1380)
    al = c.a(0.6)
    if al > 0:
        c.d.rounded_rectangle([M + 60, 720, W - M - 60, 1080], radius=22, outline=c.c("edge", al), width=4)
        c.para("Services_Agreement_v2.docx", 790, 44, 0.6, role="fg", fn=E.BODY_B, x=M + 100)
        c.para("Revised draft · 14 pages", 860, 34, 0.6, role="mut", x=M + 100)
        p = E.cl((c.u - 0.8) / 2.0)
        c.d.rounded_rectangle([M + 100, 960, W - M - 100, 990], radius=15, fill=c.c("panel", al))
        c.d.rounded_rectangle([M + 100, 960, M + 100 + int((CW - 200) * max(p, 0.03)), 990], radius=15, fill=c.c("acc", al))
    if c.u > 2.8: c.mono("UPLOADED TO THE RIGHT MATTER", M + 100, 1140, 28, 2.8, role="ok", fn=E.MONO_B)

def ui_confirm(c):
    win(c, 0.3, "UPLOAD & GO · CONFIRM", 600, 1380)
    rows = [("MATTER", "Harbour Studio Ltd"), ("DOCUMENT TYPE", "Commercial contract"), ("JURISDICTION", "England and Wales")]
    y = 710
    for i, (k, v) in enumerate(rows):
        t0 = 0.6 + i * 0.4
        c.mono(k, M + 60, y, 24, t0, role="dim", fn=E.MONO_B)
        c.para(v, y + 40, 46, t0, role="fg", fn=E.BODY_B, x=M + 60)
        tick(c, W - M - 130, y + 30, 54, t0 + 0.3)
        y += 210

def ui_review(c):
    win(c, 0.3, "UPLOAD & GO · CHOOSE ONE REVIEW", 600, 1400)
    opts = [("Liability", True), ("Missing information", False), ("Termination", False)]
    y = 700
    for i, (o, sel) in enumerate(opts):
        t0 = 0.5 + i * 0.2; al = c.a(t0)
        if al <= 0: continue
        c.d.ellipse([M + 60, y + 4, M + 110, y + 54], outline=c.c("fg", al), width=4)
        if sel: c.d.ellipse([M + 74, y + 18, M + 96, y + 40], fill=c.c("acc", al))
        c.para(o, y, 46, t0, role="fg" if sel else "mut", fn=E.BODY_B, x=M + 140)
        y += 90
    al = c.a(1.6)
    if al > 0:
        c.d.rounded_rectangle([M + 40, 1010, W - M - 40, 1360], radius=20, fill=c.c("panel", al), outline=c.c("acc", al), width=3)
    c.mono("DEMO ESTIMATE · NOT A PRICE", M + 80, 1040, 24, 1.6, role="acc", fn=E.MONO_B)
    c.para("Scope: liability clauses in this document", 1095, 38, 1.6, role="fg", x=M + 80, maxw=CW - 160)
    c.para("Estimated usage shown before the review starts", 1200, 38, 1.9, role="fg", fn=E.BODY_B, x=M + 80, maxw=CW - 160)

def s6a(c):
    c.mono("THE INTENDED RESULT", M, 300, 28, 0.0, role="acc", fn=E.MONO_B)
    c.head(["A DRAFT FINDING"], 360, 130, 0.0)
    card(c, X0, 560, X1, 1420, 0.3, bar=hexc("#2F6FD6"))
    chip(c, "DRAFT FINDING · FOR REVIEW", X0 + 50, 590, 0.3, size=22, fill=hexc("#2F6FD6"), tcol=(255, 255, 255))
    ptext(c, "A fee is payable if the customer ends the agreement early in breach.", X0 + 50, 670, 38, 0.4, fn=E.BODY_B, maxw=CW - 100)
    rows = [("DOCUMENT ANCHOR", "Clause 12.1 · page 6", INK), ("LEGAL SOURCE", "[2015] UKSC 67 · para 32", INK), ("MISSING INFORMATION", "Schedule 2 (fees) not uploaded", RED)]
    y = 860
    for i, (k, v, col) in enumerate(rows):
        t0 = 0.9 + i * 0.5
        ptext(c, k, X0 + 50, y, 22, t0, fn=E.MONO_B, col=GREY)
        ptext(c, v, X0 + 50, y + 36, 40, t0, fn=E.BODY_B, col=col)
        y += 170

def s6b(c):
    c.mono("THEN THE PROFESSIONAL", M, 330, 28, 0.0, role="acc", fn=E.MONO_B)
    items = ["INSPECT THE SOURCE.", "QUESTION THE FINDING.", "DECIDE WHAT NEEDS ATTENTION."]
    y = 420
    for i, it in enumerate(items):
        t0 = 0.1 + i * 0.6
        tick(c, M, y + 10, 70, t0)
        y = c.head(wrap(F(E.HEAD, 92), it, CW - 120), y, 92, t0, x=M + 120, maxw=CW - 120) + 90
    c.para("You make the call. The software prepares; it doesn’t decide.", y + 30, 44, 2.0, role="mut", fn=E.SERIF)

# ---------------------------------------------------------------- the law
def s7a(c):
    c.mono("A REAL CONTRACT-LAW EXAMPLE", M, 330, 28, 0.0, role="acc", fn=E.MONO_B)
    c.head(["A PAYMENT", "TRIGGERED", "BY BREACH."], 400, 190, 0.1, role=["fg", "fg", "acc"], stag=0.12)
    c.para("Say the contract makes the customer pay a set sum if they break it. Is that a penalty?", 1060, 44, 0.9, role="mut")

def cite(c, y0, names, cit, t0, h=420):
    card(c, X0, y0, X1, y0 + h, t0, bar=hexc("#B8860B"))
    ptext(c, "REAL AUTHORITY", X0 + 50, y0 + 34, 22, t0, fn=E.MONO_B, col=hexc("#8A6A10"))
    yb = ptext(c, names, X0 + 50, y0 + 80, 44, t0, fn=E.SERIF, maxw=CW - 100, lead=1.2)
    ptext(c, cit, X0 + 50, yb + 20, 30, t0, fn=E.MONO_B)

def s7b(c):
    cite(c, 290, "Cavendish Square Holding BV v Makdessi; ParkingEye Ltd v Beavis", "[2015] UKSC 67 · paras 13 and 32", 0.0, h=360)
    qs = [("1", "Is it a secondary obligation, triggered by the breach?"),
          ("2", "If so, weigh the detriment against the innocent party’s legitimate interest.")]
    y = 720
    for i, (n, q) in enumerate(qs):
        t0 = 0.8 + i * 1.6; al = c.a(t0)
        if al > 0:
            c.d.ellipse([M, y, M + 80, y + 80], fill=c.c("acc", al)); text(c.d, M + 40, y + 10, n, F(E.HEAD, 50), c.c("bg", al), align="c")
        y = c.para(q, y + 6, 48, t0, role="fg", fn=E.BODY_B, x=M + 110, maxw=CW - 110) + 70

def s7c(c):
    c.head(["CALLING IT", "A PENALTY", "IS NOT", "ENOUGH."], 330, 200, 0.0, role=["fg", "fg", "fg", "acc"], stag=0.12)
    c.mono("SOURCE: CASELAW.NATIONALARCHIVES.GOV.UK/UKSC/2015/67", M, 1240, 22, 0.8)
    c.para("General legal information on how to approach the question, not a result for any contract.", 1290, 34, 1.0, role="mut", maxw=CW)

# ---------------------------------------------------------------- finding to work
def s8a(c):
    c.mono("FROM FINDING TO WORK", M, 300, 28, 0.0, role="acc", fn=E.MONO_B)
    steps = [("FINDING", "Clause 12.1 · fee on early exit"), ("ASSIGNED TASK", "J. Patel (associate) · checked due date: Thu"), ("PROFESSIONAL REVIEW", "S. Okoro (partner) · decision recorded")]
    y = 370
    for i, (k, v) in enumerate(steps):
        t0 = 0.1 + i * 0.9
        c.box(M, y, W - M, y + 230, t0, r=22, fill="panel", edge="acc", w=3)
        c.mono(k, M + 40, y + 34, 28, t0, role="acc", fn=E.MONO_B)
        c.para(v, y + 90, 44, t0, role="fg", fn=E.BODY_B, x=M + 40, maxw=CW - 80)
        if i < 2: arrow(c, (W / 2, y + 240), (W / 2, y + 320), t0 + 0.5, w=10)
        y += 340

def s8b(c):
    c.head(["FOLLOW THE MATTER", "THROUGH TO DELIVERY."], 300, 104, 0.0, role=["fg", "acc"], stag=0.1)
    tiles = ["Existing documents", "Contract management", "Billing"]
    y = 600
    for i, t in enumerate(tiles):
        t0 = 0.5 + i * 0.45
        c.box(M, y, W - M, y + 200, t0, r=22)
        c.para(t, y + 40, 52, t0, role="fg", fn=E.BODY_B, x=M + 40)
        c.mono("INTEGRATION PLANNED", M + 40, y + 128, 24, t0, role="acc", fn=E.MONO_B)
        y += 240

def s9a(c):
    c.mono("THE REASON TO LOOK AT DOGETLAWYER", M, 300, 28, 0.0, role="acc", fn=E.MONO_B)
    parts = ["MATTER CONTEXT", "DOCUMENT EVIDENCE", "PROFESSIONAL CONTROL"]
    y = 400
    for i, p in enumerate(parts):
        t0 = 0.2 + i * 0.6
        if i: c.head(["+"], y - 30, 90, t0, role="acc", align="c")
        if i: y += 80
        c.box(M, y, W - M, y + 190, t0, r=24, fill="panel", edge="edge")
        c.head([p], y + 50, 88, t0, align="c")
        y += 230
    c.head(["TOGETHER."], y + 30, 150, 2.0, role="acc", align="c")

def s9b(c):
    c.mono("WHO IT’S FOR, HONESTLY", M, 300, 28, 0.0, role="acc", fn=E.MONO_B)
    cards = [("SOLICITOR FIRMS · ENGLAND & WALES", "Your firm’s own work can enter the intended pilot.", "INTENDED PILOT", "ok"),
             ("BARRISTERS & CHAMBERS", "Workflows for counsel and chambers.", "SEPARATE PLANNED EDITION", "acc")]
    y = 380
    for i, (h, b, tag, r) in enumerate(cards):
        t0 = 0.2 + i * 1.2
        c.box(M, y, W - M, y + 440, t0, r=24)
        c.mono(h, M + 40, y + 40, 26, t0, role="dim", fn=E.MONO_B)
        c.para(b, y + 100, 52, t0, role="fg", fn=E.BODY_B, x=M + 40, maxw=CW - 80)
        chip(c, tag, M + 40, y + 340, t0 + 0.3, size=26, fill=c.T[r])
        y += 500

# ---------------------------------------------------------------- confidentiality
def s10a(c):
    c.pill("PROPOSED CONTROLS · NOT A CERTIFICATION", M, 290, 0.0, size=24)
    c.head(["THE DESIGN", "CALLS FOR:"], 390, 140, 0.1, role=["fg", "acc"])
    items = ["Matter-based access", "An approval record", "Clear data-handling terms", "No silent switch to another AI provider"]
    y = 760
    for i, it in enumerate(items):
        t0 = 0.8 + i * 0.6
        tick(c, M, y + 6, 50, t0)
        y = c.para(it, y, 50, t0, role="fg", fn=E.BODY_B, x=M + 90, maxw=CW - 90) + 50

def s10b(c):
    c.mono("BEFORE CLIENT USE", M, 330, 30, 0.0, role="acc", fn=E.MONO_B)
    c.head(["CHECK THE", "ACTUAL", "SAFEGUARDS."], 400, 200, 0.1, role=["fg", "fg", "acc"], stag=0.12)
    c.para("Confidentiality and privilege still need your attention. Your practice assesses the service.", 1060, 46, 1.0, role="mut", fn=E.SERIF)

# ---------------------------------------------------------------- the court example
def s11a(c):
    c.mono("A REAL COURT EXAMPLE", M, 300, 28, 0.0, role="acc", fn=E.MONO_B)
    cite(c, 370, "R (Ayinde) v London Borough of Haringey; Al-Haroun v Qatar National Bank QPSC", "[2025] EWHC 1383 (Admin) · paras 7–8", 0.1, h=470)
    c.head(["VERIFY AI-ASSISTED", "RESEARCH AGAINST", "AUTHORITATIVE SOURCES."], 920, 84, 1.0, role=["fg", "fg", "acc"], stag=0.12)

def s11b(c):
    c.head(["A PLAUSIBLE", "CITATION", "NEEDS CHECKING."], 330, 160, 0.0, role=["fg", "fg", "acc"], stag=0.12)
    card(c, X0, 960, X1, 1180, 0.8)
    ptext(c, "Checked against the official judgment?", X0 + 50, 1000, 38, 0.8, fn=E.BODY_B, maxw=CW - 200)
    ptext(c, "Source · paragraph · still good law", X0 + 50, 1100, 28, 0.8, fn=E.MONO_B, col=GREY)

def s11c(c):
    c.mono("SEPARATE CARD · REGULATORS", M, 300, 28, 0.0, role="acc", fn=E.MONO_B)
    c.head(["SRA AND BSB:"], 380, 140, 0.1)
    c.head(["RESPONSIBILITY", "STAYS WITH YOU."], 600, 140, 0.4, role=["fg", "acc"], stag=0.12)
    c.para("SRA AI warning notice (Aug 2026) · BSB AI guidance (May 2026). Neither approves or certifies Dogetlawyer.", 980, 38, 1.0, role="mut", maxw=CW)

# ---------------------------------------------------------------- the answer
def clause(c, y0, num, body, t0, hil=False):
    card(c, X0, y0, X1, y0 + 250, t0, bar=RED if hil else None)
    ptext(c, f"VERSION B · CLAUSE {num}", X0 + 50, y0 + 28, 22, t0, fn=E.MONO_B, col=RED if hil else GREY)
    ptext(c, body, X0 + 50, y0 + 74, 36, t0, fn=E.BODY_B if hil else E.BODY, maxw=CW - 100)

def s12a(c):
    c.mono("BACK TO THAT AGREEMENT", M, 290, 28, 0.0, role="acc", fn=E.MONO_B)
    clause(c, 350, "8.2", "Liability is limited to £10,000, subject to clause 8.3.", 0.0)
    clause(c, 630, "8.3", "The limit in clause 8.2 does not apply to the indemnity in clause 9.", 0.6, hil=True)
    c.head(["THE CAP MAY NOT", "COVER THE INDEMNITY."], 960, 104, 1.6, role=["fg", "acc"], stag=0.12)

def s12b(c):
    c.mono("THE REVIEW SHOULD FLAG IT", M, 300, 28, 0.0, role="acc", fn=E.MONO_B)
    card(c, X0, 370, X1, 1130, 0.1, bar=hexc("#2F6FD6"))
    chip(c, "DRAFT FINDING · CL. 8.2 + 8.3 + 9", X0 + 50, 400, 0.1, size=22, fill=hexc("#2F6FD6"), tcol=(255, 255, 255))
    ptext(c, "The latest wording puts the clause 9 indemnity outside the £10,000 cap.", X0 + 50, 480, 42, 0.3, fn=E.BODY_B, maxw=CW - 100)
    ptext(c, "Read the indemnity’s scope with the liability clauses and the complete agreement. This extract alone isn’t enough to advise.", X0 + 50, 700, 34, 0.8, maxw=CW - 100)
    chip(c, "PROFESSIONAL ASSESSMENT REQUIRED", X0 + 50, 1020, 1.0, size=24, fill=RED, tcol=(255, 255, 255))

def s12c(c):
    c.mono("THE VALUABLE RESULT", M, 300, 28, 0.0, role="acc", fn=E.MONO_B)
    card(c, X0, 370, X1, 960, 0.1)
    ptext(c, "REVIEW RECORD", X0 + 50, 400, 22, 0.1, fn=E.MONO_B, col=GREY)
    rows = [("Version reviewed", "v2 · complete agreement"), ("Reviewer", "S. Okoro (partner)"), ("Decision", "Request amendment")]
    y = 460
    for i, (k, v) in enumerate(rows):
        t0 = 0.3 + i * 0.4
        ptext(c, k, X0 + 50, y, 28, t0, col=GREY)
        ptext(c, v, X0 + 50, y + 40, 42, t0, fn=E.BODY_B, col=RED if i == 2 else INK)
        y += 160
    c.head(["EXPLAINED. REVIEWED.", "TRACEABLE."], 1030, 110, 1.6, role=["fg", "acc"], stag=0.12)

def s13(c):
    c.mono("ONE NEXT STEP", M, 300, 28, 0.0, role="acc", fn=E.MONO_B)
    c.head(["REQUEST A", "DEMO."], 360, 220, 0.0, role=["fg", "acc"], stag=0.12)
    c.para("dogetlawyer.com", 870, 64, 0.4, role="fg", fn=E.BODY_B)
    c.pill("CHANNEL PROFILE LINK", M, 970, 0.6, size=28)
    items = ["Bring a fictional or approved redacted example", "See which workflows are available for your practice", "No client documents in the comments, please"]
    y = 1090
    for i, it in enumerate(items):
        t0 = 1.0 + i * 0.5
        tick(c, M, y + 4, 40, t0)
        y = c.para(it, y, 38, t0, role="fg", x=M + 70, maxw=CW - 70) + 20

def s14(c):
    c.head(["DOGETLAWYER"], 520, 130, 0.0, role="acc", align="c")
    c.head(["MATTER & ASSURANCE · PREVIEW"], 700, 52, 0.0, role="mut", align="c")
    c.para("This is general legal information, not legal advice.", 860, 64, 0.0, role="fg", fn=E.SERIF, align="c", maxw=CW - 40)
    c.para("dogetlawyer.com", 1110, 46, 0.0, role="fg", fn=E.BODY_B, align="c")
    c.para("Fictional client and documents. Dogetlawyer is a technology platform; professionals remain responsible for their work.", 1200, 30, 0.0, role="dim", align="c", maxw=CW - 40)

SCENES = [
    # 00:00-00:12 The urgent revised agreement
    (3.6, "CAN THEY SIGN?", "F", ["It’s five forty. A revised agreement lands. The client asks, “Can I sign?”"], h1),
    (4.2, "CAN THEY SIGN?", "F", ["Which clause changed,"], h2),
    (4.2, "CAN THEY SIGN?", "", ["who checked it, and what evidence supports the answer?"], h3),
    # 00:12-00:26 Name the product and its status
    (6.6, "THE PRODUCT", "P", ["Here’s the Matter & Assurance workflow we’re building at Dogetlawyer, with Upload & Go."], s4a),
    (7.4, "THE PRODUCT", "P", ["This is a preview, starting with an England and Wales solicitor-firm pilot."], s4b),
    # 00:26-00:43 Show the intake
    (3.4, "UPLOAD & GO", "PF", ["Open the right matter."], step(1, ["SELECT THE MATTER."], ui_matter)),
    (3.4, "UPLOAD & GO", "PF", ["Upload the document."], step(2, ["UPLOAD."], ui_upload)),
    (4.2, "UPLOAD & GO", "PF", ["Confirm the document type and jurisdiction."], step(3, ["CONFIRM."], ui_confirm)),
    (6.0, "UPLOAD & GO", "PF", ["Choose one review, such as liability or missing information.", "The design shows scope and estimated usage before the review starts."], step(4, ["CHOOSE ONE REVIEW."], ui_review)),
    # 00:43-01:00 Show what the professional inspects
    (8.6, "THE FINDING", "PF", ["The intended result is a draft finding tied to the exact clause or page, with supporting authority and gaps clearly marked."], s6a),
    (8.4, "THE FINDING", "P", ["You can inspect the source, question the finding and decide what needs attention."], s6b),
    # 01:00-01:19 Use a real contract authority
    (4.4, "THE LAW", "A", ["Take a payment triggered by breach."], s7a),
    (9.6, "THE LAW", "A", ["Cavendish and ParkingEye show why you check whether it is a secondary obligation,", "then assess the detriment against the innocent party’s legitimate interest."], s7b),
    (5.0, "THE LAW", "A", ["Calling it a penalty is not enough."], s7c),
    # 01:19-01:36 Turn a finding into work
    (8.6, "FINDING TO WORK", "PF", ["The design then connects findings to assigned tasks, checked dates and reviewer decisions."], s8a),
    (8.4, "FINDING TO WORK", "P", ["It aims to connect with existing documents, contract management and billing, so the team can follow the matter through to delivery."], s8b),
    # 01:36-01:54 Explain the difference and the audience
    (9.0, "WHY DOGETLAWYER", "P", ["That connected workflow is the reason to look at Dogetlawyer: matter context, document evidence and professional control together."], s9a),
    (9.0, "WHO IT’S FOR", "P", ["Your firm’s own work can enter the intended pilot.", "Barrister and chambers workflows are a separate planned edition."], s9b),
    # 01:54-02:12 Explain the confidentiality design
    (9.4, "CONFIDENTIALITY", "P", ["The design calls for matter-based access, an approval record, clear data-handling terms and no silent switch to another AI provider."], s10a),
    (8.6, "CONFIDENTIALITY", "", ["Before client use, your practice must check the actual safeguards.", "Confidentiality and privilege still need your attention."], s10b),
    # 02:12-02:29 Use a real court example
    (8.4, "THE COURTS", "A", ["Ayinde and Al-Haroun in 2025 explain why lawyers must verify AI-assisted legal research against authoritative sources."], s11a),
    (4.0, "THE COURTS", "A", ["A plausible citation needs checking."], s11b),
    (4.6, "THE REGULATORS", "", ["The SRA and BSB also keep responsibility for professional work with you."], s11c),
    # 02:29-02:44 Resolve the opening question
    (5.6, "THE ANSWER", "F", ["Back to that agreement. The fictional draft has a liability cap, but an indemnity sits outside it."], s12a),
    (4.6, "THE ANSWER", "PF", ["The review should flag the interaction for you."], s12b),
    (4.8, "THE ANSWER", "PF", ["The valuable result is an explained, reviewed decision the team can trace."], s12c),
    # 02:44-02:55 Give one commercial next step
    (11.0, "NEXT STEP", "P", ["Visit Dogetlawyer dot com and request a Matter & Assurance demo.", "Bring a fictional or approved redacted example.", "See which workflows are available for your practice."], s13),
    # 02:55-03:00 Close with the legal information notice
    (4.5, "DOGETLAWYER", "P", ["This is general legal information, not legal advice."], s14),
]
E.build(SCENES)
if __name__ == "__main__": E.main(HERE, os.path.join(HERE, "..", "vo_d01.json"))
