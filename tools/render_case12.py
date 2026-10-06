"""Dogetlawyer Case File 12 - "Just sue them." How long does that take? (Short 15, Late payment).
Retention format (engine v3): hook on frame 0, the answer (41 weeks) by ~7 s, quick cuts, sound-off captions. ~1:16.
Type: Barlow Condensed Black / Rubik / Azeret Mono / Spectral italic. Colour per section.
Usage: python3 render12.py info | preview T... | chunk START END OUT.mp4
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, ".."))
import numpy as np
from PIL import Image
import engine3 as E
from engine3 import M, W, H, CW, F, tw, text, wrap, tick, cross, win, close_card
from multitheme import gradient, hexc, mix

SECTIONS = [
 ("Hook · oxblood & black",       "#4E0D14", "#0D0A0B", "#FFFFFF", "#FFD84D", "#8BF0BC"),
 ("The wait · slate navy",        "#1A2640", "#0A0F1E", "#FFFFFF", "#FF8A66", "#8BF0BC"),
 ("What helps · olive & charcoal", "#27310F", "#111411", "#FFFFFF", "#DDFF66", "#DDFF66"),
 ("Be ready · deep indigo",       "#211C52", "#0C0A22", "#FFFFFF", "#7FE3FF", "#8BF0BC"),
]
MAP = [0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 0, 0]
PAPER = hexc("#FBFAF7"); INK = hexc("#1A1A1A"); GREY = hexc("#77736C")

def bg(T):
    im = gradient(T, W, H); a = np.asarray(im, dtype=np.float32)
    # faint diagonal hatching at very low contrast
    y, x = np.mgrid[0:H, 0:W]
    m = (((x + y) // 6) % 14 == 0)[..., None]
    a = np.where(m, a * 0.965 + np.array(T["fg"], np.float32) * 0.035, a)
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))

E.configure(os.path.join(HERE, "f"),
            ("BarlowCondensed_900Black", "Rubik_500Medium", "Rubik_800ExtraBold", "AzeretMono_400Regular", "AzeretMono_600SemiBold",
             "Spectral_500Medium_Italic", "Rubik_700Bold"),
            "CASE FILE 12", SECTIONS, MAP, bg)
E.LHK = 1.16

def bubble(c, y, msg, t0, right=False, who=""):
    al = c.a(t0)
    if al <= 0: return
    f = F(E.BODY_B, 46); w = min(CW - 120, tw(f, msg) + 70); x0 = W - M - w if right else M
    c.d.rounded_rectangle([x0, y + c.off(t0), x0 + w, y + 110 + c.off(t0)], radius=40, fill=c.c(hexc("#2F7CF6") if right else hexc("#ECEAE5"), al))
    text(c.d, x0 + 35, y + 28 + c.off(t0), msg, f, c.c(hexc("#FFFFFF") if right else INK, al))
    if who: text(c.d, x0 + (w - 10 if right else 10), y - 40, who, F(E.MONO, 24), c.c("dim", al), align="r" if right else "l")

# ---------------------------------------------------------------- scenes
def s1(c):
    bubble(c, 360, "Customer still hasn’t paid 😩".replace(" 😩", ""), 0.0, right=True, who="YOU")
    bubble(c, 560, "Just sue them.", 0.0, who="EVERYONE")
    c.head(["“JUST SUE", "THEM.”"], 800, 280, 0.0, role=["fg", "acc"])

def s2(c):
    c.mono("EASY TO SAY", M, 460, 32, 0.0)
    c.head(["HOW LONG", "DOES THAT", "TAKE?"], 520, 270, 0.1, role=["fg", "fg", "acc"], stag=0.15)

def s3(c):
    c.mono("TYPICAL WAIT · SMALL CLAIM TO TRIAL", M, 380, 28, 0.0, role="acc", fn=E.MONO_B)
    c.head(["41"], 440, 560, 0.1, role="acc")
    c.head(["WEEKS."], 1000, 230, 0.4)

def s4(c):
    c.mono("THE GOVERNMENT’S OWN FIGURE", M, 330, 28, 0.0, role="acc", fn=E.MONO_B)
    al = c.a(0.2)
    if al > 0:
        y0 = 400
        c.d.rounded_rectangle([M, y0, W - M, y0 + 480], radius=24, fill=c.c(PAPER, al))
        c.d.rectangle([M, y0, M + 14, y0 + 480], fill=c.c("acc", al))
        y = y0 + 50
        for l in wrap(F(E.SERIF, 52), "“In April to June 2026, it took a median time of 41.0 weeks between a small claim being issued and the claim going to trial.”", CW - 100):
            text(c.d, M + 56, y, l, F(E.SERIF, 52), c.c(INK, al)); y += 68
    c.mono("SOURCE: MINISTRY OF JUSTICE · CIVIL JUSTICE", M, 930, 24, 0.6)
    c.mono("STATISTICS QUARTERLY, APRIL TO JUNE 2026", M, 968, 24, 0.6)
    c.para("Cases that ended at a trial. England & Wales.", 1040, 36, 0.9, role="mut")

def s5(c):
    c.mono("THAT’S", M, 330, 32, 0.0)
    c.head(["OVER 9", "MONTHS."], 390, 260, 0.1, role=["acc", "fg"], stag=0.15)
    months = ["OCT", "NOV", "DEC", "JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL"]
    for i, m in enumerate(months):
        tt = 0.8 + i * 0.12; al = c.a(tt)
        if al <= 0: continue
        r, k = divmod(i, 5); x = M + k * (CW / 5); y = 960 + r * 150
        c.d.rounded_rectangle([x + 4, y, x + CW / 5 - 4, y + 120], radius=16, fill=c.c("panel" if i < 9 else "acc", al), outline=c.c("edge", al), width=2)
        text(c.d, x + CW / 10, y + 34, m, F(E.MONO_B, 34), c.c("bg" if i == 9 else "fg", al), align="c")
    c.mono("OF CHASING, WAITING, AND PAYING YOUR OWN BILLS", M, 1290, 22, 2.2)

def s6(c):
    c.mono("AND EVEN IF YOU WIN", M, 380, 32, 0.0)
    c.head(["A JUDGMENT", "ISN’T CASH", "IN THE BANK."], 450, 230, 0.1, role=["fg", "fg", "acc"], stag=0.15)
    c.para("Getting paid can be a whole other step.", 1180, 46, 1.4, role="mut", fn=E.SERIF)

def s7(c):
    c.head(["SO COURT", "ISN’T A QUICK", "CASH FIX."], 470, 260, 0.0, role=["fg", "fg", "acc"], stag=0.15)

def step(n, title, sub, extra=None):
    def fn(c):
        c.pill(f"{n} OF 3", M, 300, 0.0, size=28)
        yb = c.head(title, 410, 210, 0.1, role=["fg"] * (len(title) - 1) + ["acc"], stag=0.15)
        yb = c.para(sub, yb + 50, 46, 0.6, role="mut")
        if extra: extra(c, yb + 60)
    return fn

def x_agreed(c, y):
    for i, n in enumerate(["The signed contract", "The payment terms", "Proof you delivered"]):
        tt = 1.2 + i * 0.5
        tick(c, M, y + i * 104 + 8, 48, tt)
        c.para(n, y + i * 104, 50, tt, role="fg", fn=E.BODY_B, x=M + 84)

def x_letter(c, y):
    al = c.a(1.2)
    if al > 0:
        c.d.rounded_rectangle([M, y, W - M, y + 330], radius=20, fill=c.c(PAPER, al))
        text(c.d, M + 40, y + 34, "LETTER BEFORE CLAIM", F(E.MONO_B, 28), c.c(GREY, al), tr=2)
        for i, l in enumerate(["What’s owed and why", "What you want them to do", "A clear deadline to reply"]):
            text(c.d, M + 40, y + 100 + i * 66, "— " + l, F(E.BODY, 40), c.c(INK, al))
    c.mono("PRACTICE DIRECTION – PRE-ACTION CONDUCT AND PROTOCOLS", M, y + 360, 22, 1.6)

def x_med(c, y):
    al = c.a(1.0)
    if al > 0:
        c.d.rounded_rectangle([M, y, W - M, y + 280], radius=20, fill=c.c(PAPER, al))
        c.d.rectangle([M, y, M + 14, y + 280], fill=c.c("acc", al))
        yy = y + 40
        for l in wrap(F(E.SERIF, 42), "“Mediation is being fully integrated as a key step in the court process for small civil claims valued up to £10,000.”", CW - 100):
            text(c.d, M + 56, yy, l, F(E.SERIF, 42), c.c(INK, al)); yy += 56
    c.mono("SOURCE: MINISTRY OF JUSTICE · CIVIL JUSTICE STATISTICS", M, y + 310, 22, 1.4)

def s12(c):
    c.mono("THE BEST TIME TO PREPARE FOR ALL THIS?", M, 460, 28, 0.0)
    c.head(["BEFORE", "YOU SIGN."], 530, 300, 0.1, role=["fg", "acc"], stag=0.2)

def s13(c):
    c.mono("THAT’S WHERE DOGETLAWYER HELPS", M, 300, 26, 0.0, role="acc", fn=E.MONO_B)
    win(c, 0.2, "BRIGHTWELL RETAIL · SUPPLY AGREEMENT", 370, 1200)
    rows = [("SIGNED VERSION", "v3 · signed 2 Jun 2026"), ("PAYMENT TERMS", "30 days from invoice"), ("KEY DATE", "Delivered 14 Aug 2026"),
            ("OWNER", "J. Okafor")]
    y = 480
    for i, (k, v) in enumerate(rows):
        tt = 0.6 + i * 0.4
        c.mono(k, M + 40, y, 24, tt, tr=2)
        c.para(v, y + 40, 46, tt, role="fg", fn=E.BODY_B, x=M + 40)
        al = c.a(tt)
        if i < 3 and al > 0: c.d.rectangle([M + 40, y + 140, W - M - 40, y + 141], fill=c.c("line", al))
        y += 170
    c.para("So if it ever comes to it, you’re ready.", 1240, 44, 2.4, role="mut", fn=E.SERIF)

def s14(c):
    c.mono("YOUR TURN", M, 420, 32, 0.0)
    c.head(["LONGEST YOU’VE", "WAITED TO", "GET PAID?"], 490, 200, 0.1, role=["fg", "fg", "acc"], stag=0.15)
    for i, n in enumerate(["30", "60", "90", "90+"]):
        tt = 1.0 + i * 0.15; a = c.a(tt)
        if a <= 0: continue
        x = M + i * 230
        c.d.rounded_rectangle([x, 1080, x + 190, 1250], radius=24, fill=c.c("panel", a), outline=c.c("acc", a), width=4)
        f = F(E.HEAD, 110); text(c.d, x + 95, 1165 - (f.getbbox(n)[1] + f.getbbox(n)[3]) / 2, n, f, c.c("acc", a), align="c")
    c.mono("DAYS · COMMENT YOURS", M, 1290, 26, 1.6)

def close(c):
    close_card(c, ["BEFORE “JUST SUE", "THEM”… KNOW WHAT", "YOU SIGNED."], "Every contract. Every key date. One place.")

# ---------------------------------------------------------------- v2 hook: unpaid invoice + racing week counter from frame 0
RED = hexc("#FF3B30")
_ST = {}
def stamp(word, size, ang):
    k = (word, size, ang)
    if k not in _ST:
        from PIL import ImageDraw
        f = F(E.HEAD, size); w = int(tw(f, word) + size * 0.8); h = int(size * 1.4)
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle([4, 4, w - 5, h - 5], radius=int(size * 0.16), outline=RED + (255,), width=max(6, size // 10))
        d.text((w / 2, h / 2), word, font=f, fill=RED + (255,), anchor="mm")
        _ST[k] = im.rotate(ang, expand=True, resample=Image.BICUBIC)
    return _ST[k]

def invoice(c, y0):
    c.d.rounded_rectangle([M, y0, W - M, y0 + 400], radius=22, fill=PAPER)
    text(c.d, M + 40, y0 + 36, "INVOICE #0412", F(E.MONO_B, 30), GREY, tr=2)
    text(c.d, M + 40, y0 + 90, "£8,400", F(E.HEAD, 170), INK)
    text(c.d, M + 40, y0 + 300, "Due: 30 days · now 94 days overdue", F(E.BODY_B, 34), RED)
    st = stamp("UNPAID", 110, 10); c.im.paste(st, (W - M - st.width + 10, y0 + 150), st)

def weeks_bar(c, n, y):
    c.d.rounded_rectangle([M, y, W - M, y + 44], radius=22, fill=c.c("panel", 1))
    c.d.rounded_rectangle([M, y, M + max(44, int(CW * n / 41)), y + 44], radius=22, fill=c.c("acc", 1))
    text(c.d, M, y + 64, f"WEEK {n} OF 41", F(E.MONO_B, 34), c.c("acc", 1), tr=2)
    text(c.d, W - M, y + 64, "…STILL WAITING", F(E.MONO, 28), c.c("dim", 1), tr=1, align="r")

def h1(c):
    invoice(c, 330)
    c.head(["JUST SUE", "THEM?"], 830, 300, 0.0, role=["fg", "acc"])

def h2(c):
    n = max(1, min(41, 1 + int(40 * E.cl((c.u - 0.2) / 2.6))))
    c.mono("SO YOU TAKE THEM TO COURT", M, 320, 30, 0.0)
    c.head(["SEE YOU IN"], 380, 170, 0.0)
    c.head(["41 WEEKS."], 580, 300, 0.0, role="acc")
    weeks_bar(c, n, 960)
    c.mono("TYPICAL WAIT · SMALL CLAIM TO TRIAL · MoJ, APR–JUN 2026", M, 1130, 22, 0.4)

def h3(c):
    c.mono("STICK AROUND", M, 440, 32, 0.0)
    c.head(["THERE’S A", "SMARTER", "MOVE."], 500, 270, 0.0, role=["fg", "fg", "acc"], stag=0.12)
    c.para("And it starts before anything goes wrong.", 1240, 44, 0.8, role="mut", fn=E.SERIF)

SCENES = [
    (3.0, "JUST SUE THEM", True, ["Your customer owes you eight grand. Just sue them, right?"], h1),
    (3.6, "JUST SUE THEM", False, ["So you go to court. Typical wait to get to a trial? Forty-one weeks."], h2),
    (3.6, "JUST SUE THEM", False, ["Stick around. There's a smarter move, and it starts before anything goes wrong."], h3),
    (6.6, "THE WAIT", False, ["That's the government's own figure, for April to June this year,", "for cases that went all the way to a trial."], s4),
    (5.0, "THE WAIT", False, ["That's over nine months.", "Of chasing, waiting, and paying your own bills in the meantime."], s5),
    (5.8, "THE WAIT", False, ["And even if you win, a judgment isn't cash in the bank.", "Getting paid can be a whole other step."], s6),
    (3.4, "THE WAIT", False, ["So court isn't a quick cash fix."], s7),
    (7.2, "WHAT HELPS", False, ["Here's what actually helps. One. Know exactly what was agreed.", "The signed contract, the payment terms, and proof you delivered."],
     step(1, ["KNOW WHAT", "WAS AGREED."], "Before anything else, have it in writing.", x_agreed)),
    (7.2, "WHAT HELPS", False, ["Two. Send a letter before claim.", "Courts expect you to try and sort it out before you go to court."],
     step(2, ["LETTER", "BEFORE CLAIM."], "Courts expect you to try to settle first.", x_letter)),
    (6.6, "WHAT HELPS", False, ["Three. Expect mediation.", "It's now a key step for small claims up to ten thousand pounds."],
     step(3, ["EXPECT", "MEDIATION."], "For small claims up to £10,000.", x_med)),
    (3.8, "WHAT HELPS", False, ["And the best time to prepare for all this? Before you sign."], s12),
    (9.2, "BE READY", True, ["That's where Dogetlawyer helps. Every contract in one place,", "with the signed version, the payment terms and the key dates on record.",
                            "So if it ever comes to it, you're ready."], s13),
    (4.4, "YOUR TURN", False, ["What's the longest you've waited to get paid? Comment it."], s14),
    (6.0, "DOGETLAWYER", False, ["So before you say just sue them, know what you signed. Dogetlawyer dot com, link in bio."], close),
]
E.build(SCENES)
if __name__ == "__main__": E.main(HERE, os.path.join(HERE, "..", "vo12.json"))
