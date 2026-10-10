"""Dogetlawyer Delivery 02 - Business Intelligence for UK SMEs (PREVIEW). 3-minute Short.
Follows the boss's master script (02_THREE_MINUTE_MASTER_SCRIPT.md) scene by scene; each scene is split into 4-9 s cuts.
All figures are the pack's fictional fixtures (FICTIONAL_DEMO_RECORDS.csv / FICTIONAL_CASH_SCENARIOS.csv).
Palette per the pack: navy, cream and teal, one palette per section. Runtime 179.5 s.
Type: Barlow Condensed ExtraBold / Plus Jakarta Sans / Azeret Mono / Crimson Pro italic.
Usage: python3 render_d02.py info | preview T... | chunk START END OUT.mp4
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, ".."))
import numpy as np
from PIL import Image
import engine3 as E
from engine3 import M, W, H, CW, F, tw, text, wrap, tick, cross, win
from multitheme import gradient, hexc, mix
import dhelp as D
from dhelp import PAPER, INK, GREY, RULE, card, ptext, chip, arrow

SECTIONS = [
 ("Friday · cream & navy",     "#F8F3E9", "#E9DFCB", "#14284B", "#0F766E", "#0F766E"),
 ("BI workflow · deep navy",   "#16305A", "#0A1530", "#F8F3E9", "#5EEAD4", "#86EFAC"),
 ("The money · deep teal",     "#0F5E59", "#082A30", "#FFFFFF", "#FFD38A", "#A7F3D0"),
 ("Why Dogetlawyer · mint",    "#EEF6F3", "#CFE6E0", "#14284B", "#0F766E", "#0F766E"),
]
#        h1 h2 h3 4a 4b 5a 5b 6a 6b 6c 7a 7b 8a 8b 9a 9b 10a 10b 11a 11b 12a 12b 13 14
MAP = [0, 0, 0, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 3, 3, 3, 3, 2, 2, 0, 0, 0, 0]
GAP = hexc("#C2410C"); NAVY = hexc("#14284B"); TEAL = hexc("#0F766E")

def bg(T):
    im = gradient(T, W, H); a = np.asarray(im, dtype=np.float32)
    line = np.array(T["fg"], np.float32); k = 0.025
    for y in range(300, H - 100, 110): a[y:y + 2, :] = a[y:y + 2, :] * (1 - k) + line * k     # ledger lines
    a[:, M - 40:M - 38] = a[:, M - 40:M - 38] * (1 - k * 2) + line * k * 2
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))

E.configure(os.path.join(HERE, "f"),
            ("BarlowCondensed_800ExtraBold", "PlusJakartaSans_500Medium", "PlusJakartaSans_800ExtraBold", "AzeretMono_400Regular", "AzeretMono_700Bold",
             "CrimsonPro_500Medium_Italic", "PlusJakartaSans_700Bold"),
            "BI FOR UK SMEs", SECTIONS, MAP, bg)
E.LHK = 1.16
D.install("BI FOR UK SMEs")
X0, X1 = M, W - M

def money_row(c, y, label, amt, sub, t0, col="fg", h=170):
    c.box(M, y, W - M, y + h, t0, r=22)
    c.mono(label, M + 36, y + 28, 24, t0, role="dim", fn=E.MONO_B)
    c.para(sub, y + 80, 34, t0, role="mut", x=M + 36, maxw=CW * 0.55)
    al = c.a(t0)
    if al > 0: text(c.d, W - M - 36, y + 34, amt, F(E.HEAD, 110), c.c(col, al), align="r")

# ---------------------------------------------------------------- hook
def chart(c, x0, y0, w, h, t0):
    al = c.a(t0)
    if al <= 0: return
    vals = [3, 4, 3.6, 5, 5.6, 6.8]; bw = w / len(vals) * 0.62
    for i, v in enumerate(vals):
        x = x0 + i * w / len(vals); bh = h * v / 7
        c.d.rounded_rectangle([x, y0 + h - bh, x + bw, y0 + h], radius=8, fill=c.c("acc" if i == 5 else "edge", al))
    arrow(c, (x0 + 10, y0 + h * 0.75), (x0 + w - 20, y0 + 10), t0, role="acc", w=10)

def h1(c):
    c.mono("SALES THIS QUARTER", M, 300, 26, 0.0, role="dim", fn=E.MONO_B)
    chart(c, M, 350, 420, 300, 0.0)
    c.head(["SALES:", "UP."], 330, 160, 0.0, x=W / 2 + 60, maxw=W / 2 - 150, role=["fg", "acc"])
    card(c, X0, 720, X1, 1180, 0.0)
    ptext(c, "FRIDAY 9 OCTOBER · DUE", X0 + 40, 750, 24, 0.0, fn=E.MONO_B, col=GREY)
    for i, (k, v) in enumerate([("Wages", "£10,000"), ("Supplier", "£4,000"), ("Rent", "£3,000")]):
        y = 810 + i * 90
        ptext(c, k, X0 + 40, y, 42, 0.0, fn=E.BODY_B, col=NAVY)
        al = c.a(0.0); text(c.d, X1 - 40, y, v, F(E.BODY_B, 42), c.c(NAVY, al), align="r")
    c.d.rectangle([X0 + 40, 1088, X1 - 40, 1090], fill=RULE)
    ptext(c, "Total due", X0 + 40, 1105, 40, 0.0, col=GREY); text(c.d, X1 - 40, 1100, "£17,000", F(E.HEAD, 60), GAP, align="r")
    c.head(["SO WHY THE FRIDAY DREAD?"], 1240, 92, 0.0, role="fg")

def h2(c):
    c.mono("ONE EXPECTED PAYMENT", M, 300, 28, 0.0, role="acc", fn=E.MONO_B)
    card(c, X0 + 60, 380, X1 - 60, 820, 0.0, bar=TEAL)
    ptext(c, "INVOICE 1042 · FICTIONAL", X0 + 110, 410, 24, 0.0, fn=E.MONO_B, col=GREY)
    al = c.a(0.0); text(c.d, X0 + 110, 460, "£8,000", F(E.HEAD, 190), c.c(NAVY, al))
    ptext(c, "Due Mon 5 Oct · not yet paid", X0 + 110, 700, 38, 0.0, fn=E.BODY_B, col=GAP)
    c.head(["CAN CHANGE", "THE ANSWER."], 900, 170, 0.3, role=["fg", "acc"], stag=0.12)

def h3(c):
    c.head(["CAN YOU", "COVER", "FRIDAY?"], 330, 270, 0.0, role=["fg", "fg", "acc"], stag=0.1)
    c.para("Let’s work through one simple, fictional example. The answer comes at the end.", 1180, 44, 0.6, role="mut", fn=E.SERIF)

# ---------------------------------------------------------------- BI in ordinary words
def s4a(c):
    c.mono("IN ORDINARY WORDS", M, 320, 28, 0.0, role="acc", fn=E.MONO_B)
    c.head(["BUSINESS", "INTELLIGENCE"], 380, 200, 0.1, stag=0.12)
    c.head(["MEANS:"], 790, 110, 0.6, role="acc")
    c.para("Using your business records to decide what needs attention.", 940, 60, 1.0, role="fg", fn=E.BODY_B)

def s4b(c):
    c.mono("WHAT WE’RE BUILDING", M, 320, 28, 0.0, role="acc", fn=E.MONO_B)
    c.head(["DOGETLAWYER BI"], 380, 180, 0.1)
    c.head(["FOR UK SMEs"], 590, 140, 0.3, role="acc")
    rows = [("STATUS", "Product preview"), ("FOR", "Agencies, consultancies, IT services"), ("SCREENS", "Proposed, labelled Preview")]
    y = 820
    for i, (k, v) in enumerate(rows):
        t0 = 0.8 + i * 0.4
        c.box(M, y, W - M, y + 160, t0, r=22)
        c.mono(k, M + 36, y + 28, 24, t0, role="acc", fn=E.MONO_B)
        c.para(v, y + 74, 44, t0, role="fg", fn=E.BODY_B, x=M + 36, maxw=CW - 72)
        y += 190

# ---------------------------------------------------------------- the fictional agency
def s5a(c):
    c.mono("A SMALL AGENCY · WED 7 OCT, 10AM", M, 300, 26, 0.0, role="acc", fn=E.MONO_B)
    money_row(c, 380, "AVAILABLE NOW", "£12,000", "Cash in the business account", 0.2, h=230)
    money_row(c, 650, "DUE BY FRIDAY", "£17,000", "Wages, a supplier and rent", 1.6, col=GAP if False else "acc", h=230)
    al = c.a(1.6)
    c.para("Only £12,000 is cash today.", 960, 50, 2.4, role="fg", fn=E.BODY_B)

def s5b(c):
    c.mono("TWO MORE FIGURES", M, 300, 26, 0.0, role="acc", fn=E.MONO_B)
    money_row(c, 380, "INVOICE · OVERDUE", "£8,000", "Due Mon 5 Oct, not paid yet", 0.2, h=230)
    money_row(c, 650, "COMPLETED WORK", "£3,000", "Needs a billing check first", 1.6, h=230)
    c.para("Four figures. Not one pot of money.", 960, 50, 2.6, role="fg", fn=E.BODY_B)

def s6a(c):
    c.head(["THOSE", "FIGURES TELL", "DIFFERENT", "STORIES."], 330, 220, 0.0, role=["fg", "fg", "fg", "acc"], stag=0.1)

def s6b(c):
    rows = [("AVAILABLE CASH", "£12,000", "In the bank now", 0.1), ("MONEY TO COLLECT", "£8,000", "Invoice issued, not yet paid", 1.6),
            ("WORK TO CHECK", "£3,000", "Check it before you bill it", 3.6)]
    y = 300
    for k, v, s, t0 in rows:
        money_row(c, y, k, v, s, t0, h=250); y += 290
    c.mono("THREE DIFFERENT MONEY STATES", M, y + 10, 26, 4.4, role="acc", fn=E.MONO_B)

def s6c(c):
    c.head(["TREATING", "THEM ALL", "AS CASH"], 330, 220, 0.0, stag=0.1)
    c.head(["CAN MISLEAD YOU."], 1000, 150, 0.6, role="acc")

# ---------------------------------------------------------------- evidence
def s7a(c):
    c.mono("THE RECORDS, WITH THEIR DATES", M, 290, 26, 0.0, role="acc", fn=E.MONO_B)
    win(c, 0.1, "DOGETLAWYER BI · INVOICE 1042", 350, 1420)
    recs = [("INVOICE", "£8,000 · issued 21 Sep · due 5 Oct", "Checked 7 Oct, 09:58"),
            ("PAYMENT RECORD", "No matching receipt found", "Checked 7 Oct, 09:58"),
            ("DELIVERY EVIDENCE", "Client sign-off email · 18 Sep", "Checked 7 Oct, 09:59")]
    y = 460
    for i, (k, v, d_) in enumerate(recs):
        t0 = 0.6 + i * 0.9
        c.mono(k, M + 40, y, 24, t0, role="acc", fn=E.MONO_B)
        c.para(v, y + 42, 42, t0, role="fg", fn=E.BODY_B, x=M + 40, maxw=CW - 80)
        c.mono(d_.upper(), M + 40, y + 160, 22, t0, role="dim")
        al = c.a(t0)
        if i < 2 and al > 0: c.d.rectangle([M + 40, y + 220, W - M - 40, y + 221], fill=c.c("line", al))
        y += 300

def s7b(c):
    c.head(["MISSING", "OR OLD?"], 300, 230, 0.0, role=["fg", "acc"], stag=0.1)
    card(c, X0, 820, X1, 1180, 0.5, bar=GAP)
    ptext(c, "DATA WARNING", X0 + 50, 850, 24, 0.5, fn=E.MONO_B, col=GAP)
    ptext(c, "Bank feed last updated 3 days ago. Receipts after Sun 4 Oct may be missing.", X0 + 50, 900, 40, 0.5, fn=E.BODY_B, col=NAVY, maxw=CW - 100)
    c.head(["IT SHOULD SAY SO."], 1240, 100, 1.2, role="fg")

def s8a(c):
    c.mono("GIVE THE ISSUE AN OWNER", M, 290, 26, 0.0, role="acc", fn=E.MONO_B)
    tasks = [("FINANCE · PRIYA", "Check the payment for invoice 1042", "Due Thu 8 Oct"),
             ("PROJECT LEAD · DAN", "Confirm what of the £3,000 work can be billed", "Due Thu 8 Oct")]
    y = 360
    for i, (who, what, due) in enumerate(tasks):
        t0 = 0.2 + i * 1.6
        c.box(M, y, W - M, y + 420, t0, r=24, fill="panel", edge="acc", w=3)
        c.mono(who, M + 40, y + 36, 26, t0, role="acc", fn=E.MONO_B)
        c.para(what, y + 100, 52, t0, role="fg", fn=E.BODY_B, x=M + 40, maxw=CW - 80)
        c.mono(due.upper(), M + 40, y + 340, 24, t0, role="dim")
        y += 470

def s8b(c):
    c.mono("PROPOSED ACTION", M, 290, 26, 0.0, role="acc", fn=E.MONO_B)
    card(c, X0, 350, X1, 900, 0.1)
    ptext(c, "Polite payment reminder · invoice 1042", X0 + 50, 390, 40, 0.1, fn=E.BODY_B, col=NAVY, maxw=CW - 100)
    ptext(c, "Sent through your existing billing tool, only after you approve it.", X0 + 50, 520, 34, 0.3, col=GREY, maxw=CW - 100)
    al = c.a(0.8)
    if al > 0:
        c.d.rounded_rectangle([X0 + 50, 720, X0 + 380, 820], radius=50, fill=c.c(TEAL, al))
        text(c.d, X0 + 215, 745, "APPROVE", F(E.MONO_B, 34), c.c((255, 255, 255), al), align="c")
        c.d.rounded_rectangle([X0 + 410, 720, X0 + 700, 820], radius=50, outline=c.c(NAVY, al), width=4)
        text(c.d, X0 + 555, 745, "EDIT", F(E.MONO_B, 34), c.c(NAVY, al), align="c")
    c.head(["YOU KEEP", "CONTROL."], 1000, 190, 1.4, role=["fg", "acc"], stag=0.12)

# ---------------------------------------------------------------- wider uses
def s9(items, t0s):
    def fn(c):
        c.pill("PLANNED CHECKS", M, 290, 0.0, size=26)
        c.head(["BEYOND CASH"], 380, 130, 0.0)
        y = 580
        for (k, v), t0 in zip(items, t0s):
            card(c, X0, y, X1, y + 380, t0, bar=TEAL)
            ptext(c, k, X0 + 50, y + 36, 26, t0, fn=E.MONO_B, col=TEAL)
            ptext(c, v, X0 + 50, y + 90, 46, t0, fn=E.BODY_B, col=NAVY, maxw=CW - 100)
            y += 420
    return fn
s9a = s9([("RENEWALS NEEDING ATTENTION", "Hosting contract renews 30 Nov. Notice is needed by 31 Oct."),
          ("CUSTOMERS YOU DEPEND ON", "One customer paid 46% of receipts, April to September.")], [0.4, 2.6])
s9b = s9([("JOBS WITH LITTLE MARGIN", "Job 214: included costs leave about 6%. Some costs missing."),
          ("DATED MARKET CONTEXT", "Outside news shown with its source and date, kept apart from your records.")], [0.2, 2.8])

def s10a(c):
    c.mono("THE REASON TO LOOK AT DOGETLAWYER", M, 300, 26, 0.0, role="acc", fn=E.MONO_B)
    parts = ["RECORDS", "EVIDENCE", "FOLLOW-UP WORK"]
    y = 380
    for i, p in enumerate(parts):
        t0 = 0.2 + i * 0.8
        c.box(M + 80, y, W - M - 80, y + 200, t0, r=26, fill="panel", edge="acc", w=4)
        c.head([p], y + 46, 110, t0, align="c")
        if i < 2: arrow(c, (W / 2, y + 210), (W / 2, y + 290), t0 + 0.4, w=12)
        y += 300
    c.head(["CONNECTED."], y + 20, 150, 2.6, role="acc", align="c")

def s10b(c):
    c.mono("REUSES TOOLS YOU ALREADY RUN", M, 290, 26, 0.0, role="acc", fn=E.MONO_B)
    tiles = ["Accounting", "Billing", "Customers", "Projects", "Contracts"]
    for i, t in enumerate(tiles):
        t0 = 0.2 + i * 0.3; col = i % 2; row = i // 2
        x = M + col * (CW // 2 + 10); y = 360 + row * 200; w = CW // 2 - 10
        if i == 4: x, w = M, CW
        c.box(x, y, x + w, y + 170, t0, r=22)
        c.para(t, y + 30, 48, t0, role="fg", fn=E.BODY_B, x=x + 32)
        c.mono("INTEGRATION PLANNED", x + 32, y + 110, 20, t0, role="acc", fn=E.MONO_B)
    c.head(["SEE THE NEXT ACTION.", "TRACK THE OUTCOME."], 1000, 110, 1.8, role=["fg", "acc"], stag=0.15)

# ---------------------------------------------------------------- check the assumption
def s11a(c):
    c.mono("BEFORE YOU CHASE THAT INVOICE", M, 300, 26, 0.0, role="acc", fn=E.MONO_B)
    c.head(["IS A RECEIPT", "ALREADY THERE,", "UNMATCHED?"], 370, 180, 0.1, role=["fg", "fg", "acc"], stag=0.12)
    c.para("Check receipts, allocations, credits and disputes first. Then chase.", 1000, 46, 1.2, role="mut", fn=E.SERIF)

def s11b(c):
    c.mono("THEN TEST BOTH PAYMENT DATES", M, 300, 26, 0.0, role="acc", fn=E.MONO_B)
    for i, (k, s) in enumerate([("PAID BEFORE FRIDAY", "£8,000 lands in time"), ("PAID AFTER FRIDAY", "£8,000 lands too late")]):
        t0 = 0.3 + i * 0.8; x = M + i * (CW // 2 + 12); w = CW // 2 - 12
        c.box(x, 380, x + w, 900, t0, r=24, fill="panel", edge="acc", w=3)
        c.para(k, 420, 44, t0, role="acc", fn=E.HEAD, x=x + 30, maxw=w - 60)
        c.para(s, 560, 36, t0, role="fg", fn=E.BODY_B, x=x + 30, maxw=w - 60)
        al = c.a(t0)
        if al > 0: text(c.d, x + w / 2, 700, "?", F(E.HEAD, 150), c.c("fg", al), align="c")
    c.para("Money that arrives after Friday can’t pay Friday’s bills. A forecast is only as good as its assumptions.", 980, 44, 1.8, role="fg", fn=E.BODY_B)

# ---------------------------------------------------------------- the answer
def scen(c, x, y, w, tag, line, res, sub, col, t0):
    card(c, x, y, x + w, y + 520, t0, bar=col)
    ptext(c, tag, x + 44, y + 34, 24, t0, fn=E.MONO_B, col=col)
    ptext(c, line, x + 44, y + 90, 40, t0, fn=E.MONO_B, col=NAVY)
    al = c.a(t0 + 0.3)
    if al > 0: text(c.d, x + 44, y + 210, res, F(E.HEAD, 170), c.c(col, al))
    ptext(c, sub, x + 44, y + 420, 40, t0 + 0.3, fn=E.BODY_B, col=NAVY)

def s12a(c):
    c.mono("HERE’S THE ANSWER · TWO SCENARIOS", M, 290, 26, 0.0, role="acc", fn=E.MONO_B)
    scen(c, X0, 350, CW, "A · £8,000 ARRIVES BEFORE THE BILLS", "£12,000 + £8,000 − £17,000", "£3,000", "remains", TEAL, 0.0)
    scen(c, X0, 900, CW, "B · IT ARRIVES AFTER FRIDAY", "£12,000 + £0 − £17,000", "£5,000", "gap on Friday", GAP, 3.0)

def s12b(c):
    c.head(["CONFIRM THE", "TIMING. TALK TO", "YOUR ACCOUNTANT", "EARLY."], 300, 170, 0.0, role=["fg", "fg", "fg", "acc"], stag=0.1)
    c.para("Scenarios, not a promise of collection. The £3,000 of work awaiting a billing check is in neither.", 1080, 40, 1.0, role="mut", maxw=CW)

def s13(c):
    c.mono("ONE NEXT STEP", M, 300, 28, 0.0, role="acc", fn=E.MONO_B)
    c.head(["REQUEST A", "UK SME BI DEMO."], 360, 180, 0.0, role=["fg", "acc"], stag=0.12)
    c.para("dogetlawyer.com", 800, 64, 0.4, role="fg", fn=E.BODY_B)
    c.pill("CHANNEL PROFILE LINK", M, 900, 0.6, size=28)
    items = ["Use a fictional or approved redacted example", "Check which workflows are available now", "No financial records in the comments, please"]
    y = 1030
    for i, it in enumerate(items):
        t0 = 1.0 + i * 0.5
        tick(c, M, y + 4, 40, t0)
        y = c.para(it, y, 38, t0, role="fg", x=M + 70, maxw=CW - 70) + 24

def s14(c):
    c.head(["DOGETLAWYER"], 520, 170, 0.0, role="acc", align="c")
    c.head(["BUSINESS INTELLIGENCE · PREVIEW"], 740, 64, 0.0, role="mut", align="c")
    c.para("Illustrative figures. Check your business records before acting.", 880, 60, 0.0, role="fg", fn=E.SERIF, align="c", maxw=CW - 40)
    c.para("dogetlawyer.com", 1110, 46, 0.0, role="fg", fn=E.BODY_B, align="c")
    c.para("General business information. All figures and names are fictional.", 1200, 30, 0.0, role="dim", align="c", maxw=CW - 40)

SCENES = [
    # 00:00-00:12 The Friday cash question
    (4.0, "CAN YOU COVER FRIDAY?", "F", ["Your sales look healthy. So why are you worried about Friday’s bills?"], h1),
    (3.8, "CAN YOU COVER FRIDAY?", "F", ["One expected payment can change the answer."], h2),
    (4.2, "CAN YOU COVER FRIDAY?", "", ["Let’s work through a simple example."], h3),
    # 00:12-00:27 Explain BI in ordinary words
    (7.6, "WHAT IS BI?", "", ["Business Intelligence means using your business records to decide what needs attention."], s4a),
    (7.4, "WHAT IS BI?", "P", ["Here’s the Dogetlawyer BI workflow we’re building for UK SMEs. This is a product preview."], s4b),
    # 00:27-00:44 Introduce the fictional business
    (8.4, "THE EXAMPLE", "F", ["Imagine a small agency. It has twelve thousand pounds available and seventeen thousand due by Friday."], s5a),
    (8.6, "THE EXAMPLE", "F", ["An eight-thousand-pound invoice is overdue. Another three thousand of completed work needs a billing check."], s5b),
    # 00:44-01:01 Keep the money states separate
    (3.4, "THE MONEY", "F", ["Those figures tell different stories."], s6a),
    (9.4, "THE MONEY", "F", ["Cash is available now. An invoice is money you expect to collect.", "Completed work may still need checking before you bill it."], s6b),
    (4.2, "THE MONEY", "", ["Treating them all as cash can mislead you."], s6c),
    # 01:01-01:19 Show the evidence and the next step
    (10.0, "THE EVIDENCE", "PF", ["The BI design brings the relevant records together and shows their dates.", "You inspect the invoice, payment record and delivery evidence."], s7a),
    (8.0, "THE EVIDENCE", "PF", ["If information is missing or old, the result should say so."], s7b),
    # 01:19-01:36 Turn a finding into work
    (9.4, "NEXT ACTION", "PF", ["Then give the issue an owner. Ask finance to check the payment, and the project lead to confirm what can be billed."], s8a),
    (7.6, "NEXT ACTION", "PF", ["Approved actions go through the existing billing or task tools. You keep control."], s8b),
    # 01:36-01:53 Explain the wider everyday uses
    (8.6, "EVERYDAY USES", "PF", ["Beyond cash, the design can highlight renewals needing attention, customers you depend on heavily,"], s9a),
    (8.4, "EVERYDAY USES", "PF", ["and jobs where included costs leave little margin. External market information should have a source and date, too."], s9b),
    # 01:53-02:12 Explain the reason to choose Dogetlawyer
    (9.0, "WHY DOGETLAWYER", "P", ["The reason to look at Dogetlawyer is that connection between records, evidence and follow-up work."], s10a),
    (10.0, "WHY DOGETLAWYER", "P", ["The design reuses existing accounting, billing, customer, project and contract tools.", "Your team should see the next action and track its outcome."], s10b),
    # 02:12-02:29 Check the payment assumption
    (7.0, "CHECK FIRST", "F", ["Before chasing that invoice, check whether a receipt is already recorded but unmatched."], s11a),
    (10.0, "CHECK FIRST", "F", ["Then test both payment dates. Expected money arriving after Friday cannot cover bills due on Friday.", "A forecast depends on its assumptions."], s11b),
    # 02:29-02:44 Resolve the Friday question
    (9.4, "THE ANSWER", "F", ["Here’s the answer. If the eight thousand arrives before those bills, three thousand remains.", "If it arrives later, Friday has a five-thousand-pound gap."], s12a),
    (5.6, "THE ANSWER", "F", ["Confirm payment timing and discuss the gap with your accountant early."], s12b),
    # 02:44-02:55 Invite a relevant demonstration
    (11.0, "NEXT STEP", "P", ["Request a UK SME BI demo at Dogetlawyer dot com.", "Use the channel profile link, and a fictional or approved redacted example.", "Check the workflows currently available."], s13),
    # 02:55-03:00 Close with the example notice
    (4.5, "DOGETLAWYER", "P", ["Illustrative figures. Check your business records before acting."], s14),
]
E.build(SCENES)
if __name__ == "__main__": E.main(HERE, os.path.join(HERE, "..", "vo_d02.json"))
