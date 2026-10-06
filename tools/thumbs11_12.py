"""Thumbnails (1280x720) + vertical covers (1080x1920) for Case Files 11 and 12. Usage: python3 thumbs11_12.py 11|12"""
import sys, os
B = os.path.dirname(os.path.abspath(__file__)); O = '/home/user/DGL_private/thumbnails/'
case = sys.argv[1]; sys.path.insert(0, os.path.join(B, f'c{case}')); sys.path.insert(0, B)
from PIL import Image, ImageDraw, ImageFont
import numpy as np
r = __import__(f'render{case}'); import engine3 as E
F = lambda n, s: ImageFont.truetype(os.path.join(E.FD, n + '.ttf'), s)
T = E.STH[0]; WH = (255, 255, 255); ACC = T['acc']; PAPER = (251, 250, 247); INK = (26, 26, 26); GREY = (119, 115, 108)
def grain(im):
    a = np.asarray(im).astype(np.float32); a += np.random.default_rng(4).normal(0, 6, a.shape[:2])[..., None]
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))
def bgimg(w, h): return r.bg(T) if w == 1080 else r.bg(T).crop((0, 600, 1080, 1208)).resize((w, h))
def fit(name, s, maxw, size):
    while F(name, size).getlength(s) > maxw: size -= 4
    return F(name, size)

def email_card(w):
    h = int(w * 0.56); im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); k = w / 600
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=int(24 * k), fill=PAPER + (255,))
    d.text((30 * k, 30 * k), "To:", font=F(E.MONO_B, int(26 * k)), fill=GREY)
    d.text((90 * k, 26 * k), "Sarah Bentley", font=F(E.BODY_B, int(34 * k)), fill=INK)
    d.rounded_rectangle([80 * k, 16 * k, w - 24 * k, 76 * k], radius=int(10 * k), outline=(229, 50, 45), width=max(3, int(5 * k)))
    d.text((30 * k, 110 * k), "Subject: Signed contract", font=F(E.BODY, int(28 * k)), fill=INK)
    d.rounded_rectangle([30 * k, 170 * k, 400 * k, 230 * k], radius=int(12 * k), fill=(239, 236, 230))
    d.text((50 * k, 184 * k), "Contract_signed.pdf", font=F(E.MONO_B, int(24 * k)), fill=INK)
    d.rounded_rectangle([w - 190 * k, h - 80 * k, w - 30 * k, h - 24 * k], radius=int(28 * k), fill=(47, 124, 246))
    d.text((w - 110 * k, h - 52 * k), "SENT", font=F(E.BODY_B, int(28 * k)), fill=WH, anchor="mm")
    return im.rotate(4, expand=True, resample=Image.BICUBIC)

def chat_card(w):
    h = int(w * 0.62); im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); k = w / 600
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=int(28 * k), fill=(24, 24, 28, 255))
    def bub(y, msg, right):
        f = F(E.BODY_B, int(36 * k)); bw = f.getlength(msg) + 56 * k; x0 = w - 24 * k - bw if right else 24 * k
        d.rounded_rectangle([x0, y, x0 + bw, y + 76 * k], radius=int(38 * k), fill=(47, 124, 246) if right else (236, 234, 229))
        d.text((x0 + 28 * k, y + 18 * k), msg, font=f, fill=WH if right else INK)
    bub(30 * k, "Still not paid…", True); bub(130 * k, "Just sue them.", False)
    d.text((24 * k, 240 * k), "41 WEEKS", font=F(E.HEAD, int(110 * k)), fill=ACC)
    return im.rotate(-4, expand=True, resample=Image.BICUBIC)

def make(W, H, vert):
    im = bgimg(W, H); d = ImageDraw.Draw(im)
    if case == '11':
        if not vert:
            f1 = fit(E.HEAD, "SENT IT TO", 720, 110)
            d.text((56, 60), "SENT IT TO", font=f1, fill=WH)
            d.text((56, 200), "THE WRONG", font=f1, fill=WH)
            d.text((56, 370), "SARAH?", font=fit(E.HEAD, "SARAH?", 720, 170), fill=ACC)
            c = email_card(430); im.paste(c, (W - c.width - 20, 230), c)
            d.text((60, 660), "DATA BREACH · UK SMALL BUSINESS", font=F(E.MONO_B, 28), fill=WH)
        else:
            for i, t in enumerate(["SENT IT", "TO THE", "WRONG"]): d.text((70, 150 + i * 200), t, font=fit(E.HEAD, "SENT IT", 940, 190), fill=WH)
            d.text((70, 760), "SARAH?", font=fit(E.HEAD, "SARAH?", 940, 260), fill=ACC)
            c = email_card(860); im.paste(c, ((W - c.width) // 2, 1180), c)
    else:
        if not vert:
            f1 = fit(E.HEAD, "“JUST SUE", 740, 190)
            d.text((56, 40), "“JUST SUE", font=f1, fill=WH)
            d.text((56, 230), "THEM.”", font=f1, fill=WH)
            d.text((56, 440), "HOW LONG?", font=fit(E.HEAD, "HOW LONG?", 740, 170), fill=ACC)
            c = chat_card(420); im.paste(c, (W - c.width - 20, 180), c)
            d.text((60, 660), "SMALL CLAIMS · ENGLAND & WALES", font=F(E.MONO_B, 28), fill=WH)
        else:
            for i, t in enumerate(["“JUST SUE", "THEM.”"]): d.text((70, 160 + i * 250), t, font=fit(E.HEAD, "“JUST SUE", 940, 280), fill=WH)
            d.text((70, 700), "HOW LONG?", font=fit(E.HEAD, "HOW LONG?", 940, 260), fill=ACC)
            c = chat_card(860); im.paste(c, ((W - c.width) // 2, 1100), c)
    return grain(im)
make(1280, 720, False).save(O + f'case-{case}_thumbnail_1280x720.png')
make(1080, 1920, True).save(O + f'case-{case}_cover_1080x1920.png'); print('ok', case)
