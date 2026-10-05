"""Dogetlawyer Case File 09 - "£20,000 in sales. £600 in the bank." Payment terms and cash timing (Short 10, business health).
Format: cash calendar + "4 lines that decide when you get paid". Colour per section (calm, dark grounds).
Type: Big Shoulders Display / Plus Jakarta Sans / Red Hat Mono / Newsreader italic.
Usage: python3 render9.py info | preview T... | chunk START END OUT.mp4
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, ".."))
import numpy as np
from PIL import Image, ImageDraw
import engine as E
from engine import M, W, H, CW, F, tw, text, wrap, tick, cross, win, close_card
from multitheme import gradient, hexc, mix

SECTIONS = [
 ("Hook · forest & black",       "#0E4634", "#04120D", "#FFFFFF", "#FFD84D", "#7CFFB2"),
 ("The gap · burgundy & charcoal","#56122A", "#18171C", "#FFFFFF", "#FF9F6B", "#8BF0BC"),
 ("The 4 lines · petrol blue",   "#0B3F59", "#061B29", "#FFFFFF", "#FFD84D", "#8BF0BC"),
 ("The fix · plum & ink",        "#3E1655", "#100A1C", "#FFFFFF", "#7FE3FF", "#8BF0BC"),
]
MAP = [0, 0, 0, 0, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 0, 0]

def bg(T):
    im = gradient(T, W, H); a = np.asarray(im, dtype=np.float32)
    # faint 7-column "calendar" grid, very low contrast so it never competes with text
    line = np.array(T["fg"], np.float32); k = 0.035
    for i in range(1, 7):
        x = int(i * W / 7); a[:, x:x + 2] = a[:, x:x + 2] * (1 - k) + line * k
    for y in range(0, H, int(W / 7)):
        a[y:y + 2, :] = a[y:y + 2, :] * (1 - k) + line * k
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))

E.configure(os.path.join(HERE, "f"),
            ("BigShouldersDisplay_900Black", "PlusJakartaSans_600SemiBold", "PlusJakartaSans_800ExtraBold",
             "RedHatMono_400Regular", "RedHatMono_600SemiBold", "Newsreader_500Medium_Italic", "PlusJakartaSans_700Bold"),
            "CASE FILE 09", SECTIONS, MAP, bg)

# ---------------------------------------------------------------- scenes
def s1(c):
    c.mono("THIS MONTH", M, 520, 30, 0.0)
    c.head(["£20,000", "IN SALES."], 590, 300, 0.1, role=["acc", "fg"])

def s2(c):
    c.mono("IN THE BANK", M, 520, 30, 0.0)
    c.head(["£600."], 590, 420, 0.1, role="acc")
    c.para("Available. Right now.", 1080, 50, 0.8, role="mut", fn=E.SERIF)

def s3(c):
    yb = c.head(["THE DIARY’S", "FULL."], 420, 200, 0.0)
    c.head(["SO WHY IS", "FRIDAY STILL", "STRESSFUL?"], yb + 110, 170, 0.8, role=["fg", "fg", "acc"])

def s4(c):
    c.mono("OFTEN IT’S NOT THE SALES", M, 470, 30, 0.0)
    c.head(["IT’S THE", "TIMING."], 540, 290, 0.15, role=["fg", "acc"])
    c.para("And the timing is written in your contracts.", 1150, 48, 1.4, role="mut", fn=E.SERIF)

def s5(c):
    c.mono("YOUR MONTH · MONEY IN vs MONEY OUT", M, 290, 26, 0.0, role="acc", fn=E.MONO_B)
    x0, y0, cw, chh = M, 360, CW / 7, 128
    al = c.a(0.1)
    if al > 0:
        for k, dname in enumerate("MTWTFSS"):
            text(c.d, x0 + k * cw + cw / 2, y0, dname, F(E.MONO_B, 24), c.c("dim", al), align="c")
        for dnum in range(1, 31):
            r, k = divmod(dnum - 1, 7); x = x0 + k * cw; y = y0 + 44 + r * chh
            c.d.rounded_rectangle([x + 4, y, x + cw - 4, y + chh - 8], radius=10, fill=c.c("panel", al))
            text(c.d, x + 14, y + 8, str(dnum), F(E.MONO, 22), c.c("dim", al))
    outs = [(7, "SUPPLIER", 1.0), (14, "RENT", 2.0), (28, "WAGES", 3.0)]
    for dnum, lab, tt in outs:
        a2 = c.a(tt)
        if a2 <= 0: continue
        r, k = divmod(dnum - 1, 7); x = x0 + k * cw; y = y0 + 44 + r * chh
        c.d.rounded_rectangle([x + 4, y, x + cw - 4, y + chh - 8], radius=10, fill=c.c("acc", a2))
        text(c.d, x + 14, y + 8, str(dnum), F(E.MONO_B, 22), c.c("bg", a2))
        text(c.d, x + cw / 2, y + 62, "OUT", F(E.HEAD, 40), c.c("bg", a2), align="c")
        lx = M + [0, 300, 560][[7, 14, 28].index(dnum)]
        text(c.d, lx, y0 + 44 + 5 * chh + 20, f"{dnum} · {lab}", F(E.MONO_B, 28), c.c("acc", a2), tr=1)
    a3 = c.a(4.6)
    if a3 > 0:
        y = y0 + 44 + 5 * chh + 90
        c.d.rounded_rectangle([M, y, W - M, y + 130], radius=20, outline=c.c("ok", a3), width=4)
        text(c.d, M + 32, y + 24, "MONEY IN:", F(E.MONO_B, 28), c.c("ok", a3), tr=2)
        text(c.d, M + 32, y + 66, "customer pays on day 60. Not this month.", F(E.BODY_B, 34), c.c("fg", a3))

def s6(c):
    c.mono("THE GAP", M, 380, 30, 0.0)
    rows = [("YOU PAY IN", "14 DAYS", 14, "acc", 0.2), ("THEY PAY IN", "60 DAYS", 60, "ok", 1.2)]
    y = 460
    for lab, big, days, role, tt in rows:
        al = c.a(tt)
        if al > 0:
            text(c.d, M, y, lab, F(E.MONO_B, 30), c.c("dim", al), tr=2)
            text(c.d, M, y + 40, big, F(E.HEAD, 170), c.c(role, al))
            bw = int(CW * days / 60)
            c.d.rounded_rectangle([M, y + 250, M + bw, y + 290], radius=20, fill=c.c(role, al))
        y += 390
    c.para("That gap is where Friday gets stressful.", 1270, 46, 2.4, role="fg", fn=E.SERIF)

def s7(c):
    c.mono("CHECK YOUR CONTRACTS FOR", M, 430, 30, 0.0)
    c.head(["4 LINES", "THAT DECIDE", "WHEN YOU", "GET PAID."], 500, 200, 0.15, role=["acc", "fg", "fg", "fg"])

def line(n, title, sub, chips, note=None, src=None):
    def fn(c):
        c.pill(f"LINE {n} OF 4", M, 300, 0.0, size=28)
        yb = c.head(title, 420, 190, 0.15, role=["fg"] * (len(title) - 1) + ["acc"])
        yb = c.para(sub, yb + 50, 44, 0.6, role="mut")
        y = yb + 40
        for i, ch in enumerate(chips):
            tt = 1.4 + i * 0.5; al = c.a(tt)
            if al <= 0: continue
            f = F(E.BODY_B, 38); bw = min(CW, tw(f, ch) + 60)
            c.d.rounded_rectangle([M, y, M + bw, y + 84], radius=18, fill=c.c("panel", al), outline=c.c("edge", al), width=2)
            text(c.d, M + 30, y + 20, ch, f, c.c("fg", al))
            y += 104
        if note: c.para(note, y + 20, 40, 1.4 + len(chips) * 0.5, role="acc", fn=E.SERIF)
        if src: c.mono(src, M, 1420, 22, 0.6)
    return fn

def s11(c):
    c.pill("LINE 4 OF 4", M, 300, 0.0, size=28)
    c.head(["NOTHING", "AGREED?"], 410, 190, 0.15, role=["fg", "acc"])
    al = c.a(0.8)
    if al > 0:
        y0 = 800
        c.d.rounded_rectangle([M, y0, W - M, y0 + 340], radius=24, fill=c.c(hexc("#FBFAF7"), al))
        c.d.rectangle([M, y0, M + 14, y0 + 340], fill=c.c("acc", al))
        y = y0 + 44
        for l in wrap(F(E.SERIF, 44), "“If you do not agree a payment date, the law says the payment is late 30 days after either: the customer gets the invoice; you deliver the goods or provide the service (if this is later).”", CW - 100):
            text(c.d, M + 56, y, l, F(E.SERIF, 44), c.c(hexc("#1A1A1A"), al)); y += 60
    c.mono("SOURCE: GOV.UK · LATE COMMERCIAL PAYMENTS", M, 1180, 24, 1.2, role="acc", fn=E.MONO_B)
    c.mono("Late Payment of Commercial Debts (Interest) Act 1998", M, 1222, 22, 1.2)

def s12(c):
    c.mono("AND FOR BUSINESS DEALS", M, 400, 30, 0.0)
    c.head(["OVER 60 DAYS?", "IT MUST BE", "FAIR TO BOTH."], 470, 190, 0.15, role=["acc", "fg", "fg"])
    c.para("“You can agree a longer period than 60 days for business transactions – but it must be fair to both businesses.”", 1060, 40, 1.2, role="mut", fn=E.SERIF)
    c.mono("SOURCE: GOV.UK · GENERAL POSITION, ENGLAND & WALES", M, 1330, 22, 1.4)

def s13(c):
    c.mono("BEFORE YOU SIGN THE NEXT ONE", M, 380, 30, 0.0)
    c.head(["ASK FOR", "TERMS THAT", "MATCH YOUR", "BILLS."], 450, 180, 0.15, role=["fg", "fg", "fg", "acc"])
    items = ["Shorter payment terms", "A deposit up front", "Stage payments"]
    y = 1150
    for i, s in enumerate(items):
        tt = 1.6 + i * 0.5
        tick(c, M, y + 6, 44, tt)
        c.para(s, y, 42, tt, role="fg", fn=E.BODY_B, x=M + 76)
        y += 76

def s14(c):
    c.mono("THAT’S WHERE DOGETLAWYER HELPS", M, 300, 26, 0.0, role="acc", fn=E.MONO_B)
    win(c, 0.2, "PAYMENT TERMS · ALL CONTRACTS", 360, 1240)
    groups = [("MONEY IN", [("Brightwell Retail", "60 days, end of month", "acc"), ("Corran Events", "30 days · 25% deposit", "ok")]),
              ("MONEY OUT", [("Ashby Packaging", "14 days from invoice", "fg"), ("Unit 4, Mill Lane (lease)", "Monthly, on the 1st", "fg")])]
    y = 470; tt = 0.6
    for g, rows in groups:
        c.mono(g, M + 40, y, 24, tt, role="dim", fn=E.MONO_B); y += 50
        for n, term, r in rows:
            c.para(n, y, 38, tt, role="fg", fn=E.BODY_B, x=M + 40)
            c.para(term, y + 54, 32, tt, role=r, fn=E.BODY_B, x=M + 40)
            al = c.a(tt)
            if al > 0: c.d.rectangle([M + 40, y + 120, W - M - 40, y + 121], fill=c.c("line", al))
            y += 150; tt += 0.4
        y += 20
    c.para("Who pays you, when. And when you pay them.", 1290, 44, 2.4, role="mut", fn=E.SERIF)

def s15(c):
    c.head(["SO PAYDAY", "ISN’T A", "SURPRISE."], 560, 230, 0.0, role=["fg", "fg", "acc"])

def s16(c):
    c.mono("YOUR TURN", M, 480, 30, 0.0)
    c.head(["WHAT TERMS", "DO YOUR", "CUSTOMERS GET?"], 550, 180, 0.15, role=["fg", "fg", "acc"])
    for i, n in enumerate(["14", "30", "60", "90"]):
        tt = 1.2 + i * 0.2; a = c.a(tt)
        if a <= 0: continue
        x = M + i * 230
        c.d.rounded_rectangle([x, 1110, x + 190, 1290], radius=24, fill=c.c("panel", a), outline=c.c("acc", a), width=4)
        text(c.d, x + 95, 1130, n, F(E.HEAD, 130), c.c("acc", a), align="c")
    c.mono("DAYS · COMMENT YOURS", M, 1320, 26, 2.0)

def close(c):
    close_card(c, ["KNOW WHEN", "YOU’RE PAID."], "Every contract. Every payment term. One place.")

SCENES = [
    (3.6, "THE MONTH", False, ["Twenty grand in sales this month."], s1),
    (3.8, "THE MONTH", False, ["Six hundred quid actually in the bank."], s2),
    (4.4, "THE MONTH", False, ["The diary's full. So why is Friday still stressful?"], s3),
    (5.4, "THE MONTH", False, ["Often it's not the sales. It's the timing.", "And the timing is written in your contracts."], s4),
    (9.0, "THE GAP", False, ["Here's how it happens. Your supplier wants paying in fourteen days. Rent and wages don't wait.",
                             "But your biggest customer pays in sixty days. The money's earned. It's just not here yet."], s5),
    (6.0, "THE GAP", False, ["You pay in fourteen days. They pay in sixty.", "That gap is where Friday gets stressful."], s6),
    (5.0, "4 LINES", False, ["So check these four lines in your contracts. They decide when you actually get paid."], s7),
    (8.0, "LINE 1", False, ["One. The payment terms. Thirty days? Sixty? Ninety?", "Know the number for every customer, and every supplier."],
     line(1, ["THE PAYMENT", "TERMS."], "How many days do they actually get?", ["30 days?", "60 days?", "90 days?"])),
    (8.4, "LINE 2", False, ["Two. When the clock starts. From the invoice? From delivery?", "And sixty days end of month can mean nearly ninety."],
     line(2, ["WHEN THE", "CLOCK STARTS."], "From the invoice? From delivery? Month end?", ["“60 days end of month”"], note="Invoice on the 2nd? That can be nearly 90 days.")),
    (7.6, "LINE 3", False, ["Three. Deposits and stage payments.", "Is any money due up front, or at milestones? Or does it all land at the end?"],
     line(3, ["DEPOSITS &", "STAGE PAYMENTS."], "Is anything paid before the work’s finished?", ["Up front?", "At milestones?", "All at the end?"])),
    (9.0, "LINE 4", False, ["Four. What if no payment date's agreed at all?", "GOV.UK says the payment's late thirty days after the invoice, or after you deliver, if that's later."], s11),
    (6.4, "LINE 4", False, ["And for business deals, terms over sixty days are allowed. But they have to be fair to both sides."], s12),
    (4.8, "THE FIX", False, ["Before you sign the next one, ask for terms that match your own bills."], s13),
    (9.0, "THE FIX", True, ["That's where Dogetlawyer helps. Every contract in one place, with the payment terms on record.",
                            "Who pays you, when. And when you pay them."], s14),
    (4.2, "THE FIX", False, ["So payday's never a surprise."], s15),
    (5.0, "YOUR TURN", False, ["What terms do your customers get? Comment fourteen, thirty, sixty or ninety."], s16),
    (5.4, "DOGETLAWYER", False, ["Check your terms at dogetlawyer.com. Link in bio."], close),
]
E.build(SCENES)
if __name__ == "__main__": E.main(HERE, os.path.join(HERE, "..", "vo9.json"))
