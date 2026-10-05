"""Thumbnails (1280x720) + vertical covers (1080x1920) for Case Files 09 and 10. Usage: python3 thumbs9_10.py 9|10"""
import sys, os
B = os.path.dirname(os.path.abspath(__file__)); O = '/home/user/DGL_private/thumbnails/'
case = sys.argv[1]; sys.path.insert(0, os.path.join(B, f'c{case}')); sys.path.insert(0, B)
from PIL import Image, ImageDraw, ImageFont
import numpy as np
r = __import__(f'render{case}'); import engine as E
F = lambda n, s: ImageFont.truetype(os.path.join(E.FD, n + '.ttf'), s)
T = E.STH[0]; WH = (255, 255, 255); ACC = T['acc']
def grain(im):
    a = np.asarray(im).astype(np.float32); a += np.random.default_rng(4).normal(0, 6, a.shape[:2])[..., None]
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))
def bgimg(w, h): return r.bg(T).resize((w, h)) if w == 1080 else r.bg(T).crop((0, 600, 1080, 1208)).resize((w, h))
def fit(name, s, maxw, size):
    while F(name, size).getlength(s) > maxw: size -= 4
    return F(name, size)

def bank_card(w):   # case 09: little bank-balance card
    h = int(w * 0.62); im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=26, fill=(251, 250, 247, 255))
    d.text((40, 34), "AVAILABLE BALANCE", font=F(E.MONO_B, int(h * 0.09)), fill=(110, 110, 110, 255))
    d.text((40, int(h * 0.24)), "£600.00", font=F(E.HEAD, int(h * 0.42)), fill=(194, 31, 48, 255))
    d.text((40, int(h * 0.76)), "Sales this month: £20,000", font=F(E.BODY_B, int(h * 0.09)), fill=(26, 26, 26, 255))
    return im.rotate(4, expand=True, resample=Image.BICUBIC)

def files_card(w):  # case 10: stacked file names
    names = ["FINAL.docx", "FINAL2.docx", "FINAL_ACTUALLY_FINAL.docx"]; h = int(w * 0.62)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=26, fill=(251, 250, 247, 255))
    rh = (h - 60) // 3
    for i, n in enumerate(names):
        y = 30 + i * rh; hot = i == 2
        d.rounded_rectangle([24, y, w - 24, y + rh - 16], radius=14, fill=(255, 224, 138, 255) if hot else (236, 233, 226, 255))
        f = F(E.MONO_B, int(rh * 0.36))
        while f.getlength(n) > w - 100: f = F(E.MONO_B, f.size - 2)
        d.text((50, y + (rh - 16) / 2), n, font=f, fill=(26, 26, 26, 255), anchor="lm")
    return im.rotate(-4, expand=True, resample=Image.BICUBIC)

def make(W, H, vert):
    im = bgimg(W, H); d = ImageDraw.Draw(im)
    if case == '9':
        if not vert:
            d.text((56, 50), "£20,000 IN SALES.", font=fit(E.HEAD, "£20,000 IN SALES.", 720, 150), fill=WH)
            d.text((56, 240), "£600 IN", font=F(E.HEAD, 190), fill=ACC); d.text((56, 430), "THE BANK?", font=F(E.HEAD, 190), fill=ACC)
            c = bank_card(440); im.paste(c, (W - c.width - 24, 120), c)
            d.text((60, 660), "PAYMENT TERMS · UK SMALL BUSINESS", font=F(E.MONO_B, 28), fill=WH)
        else:
            for i, t in enumerate(["£20,000", "IN SALES."]): d.text((70, 150 + i * 230), t, font=F(E.HEAD, 260), fill=WH)
            for i, t in enumerate(["£600 IN", "THE BANK?"]): d.text((70, 680 + i * 250), t, font=fit(E.HEAD, "THE BANK?", 930, 280), fill=ACC)
            c = bank_card(760); im.paste(c, ((W - c.width) // 2, 1300), c)
    else:
        if not vert:
            d.text((56, 50), "WHICH ONE", font=F(E.HEAD, 120), fill=WH)
            d.text((56, 210), "DID YOU", font=F(E.HEAD, 120), fill=WH)
            d.text((56, 400), "SIGN?", font=F(E.HEAD, 190), fill=ACC)
            c = files_card(470); im.paste(c, (W - c.width - 20, 250), c)
            d.text((60, 660), "CONTRACT VERSIONS · UK SMALL BUSINESS", font=F(E.MONO_B, 28), fill=WH)
        else:
            for i, t in enumerate(["WHICH ONE", "DID YOU"]): d.text((70, 170 + i * 220), t, font=fit(E.HEAD, "WHICH ONE", 940, 200), fill=WH)
            d.text((70, 640), "SIGN?", font=F(E.HEAD, 330), fill=ACC)
            c = files_card(860); im.paste(c, ((W - c.width) // 2, 1150), c)
    return grain(im)
make(1280, 720, False).save(O + f'case-{int(case):02d}_thumbnail_1280x720.png')
make(1080, 1920, True).save(O + f'case-{int(case):02d}_cover_1080x1920.png'); print('ok', case)
