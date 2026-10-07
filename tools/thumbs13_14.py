"""Catchier thumbnails v2 for Case Files 13 and 14: 2–3 huge words, one hero object, red glow, arrow, reaction emoji,
matching the video's first frame. Usage: python3 thumbs13_14.py 13|14"""
import sys, os
B = os.path.dirname(os.path.abspath(__file__)); O = '/home/user/DGL_private/thumbnails/'
case = sys.argv[1]; sys.path.insert(0, os.path.join(B, f'c{case}')); sys.path.insert(0, B)
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
r = __import__(f'render{case}'); import engine3 as E
F = lambda n, s: ImageFont.truetype(os.path.join(E.FD, n + '.ttf'), s)
def fit(name, s, maxw, size):
    while F(name, size).getlength(s) > maxw: size -= 4
    return F(name, size)
WH = (255, 255, 255); YEL = (255, 216, 77); RED = (255, 59, 48); INK = (26, 26, 26); PAPER = (251, 250, 247); GREY = (119, 115, 108)
EMOJI = '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf'

def base(W, H, glow_xy, top=(14, 14, 20), glow=(150, 20, 24)):
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    gx, gy = glow_xy; d = np.sqrt(((x - gx) / (W * 0.55)) ** 2 + ((y - gy) / (H * 0.55)) ** 2)
    g = np.clip(1 - d, 0, 1)[..., None] ** 1.6
    a = np.array(top, np.float32) * (1 - g) + np.array(glow, np.float32) * g
    a += np.random.default_rng(3).normal(0, 5, (H, W))[..., None]
    return Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert('RGBA')

def bigtext(im, xy, s, font, fill, stroke=0, glow=None, shadow=True, anchor='la'):
    if shadow:
        sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).text((xy[0] + 8, xy[1] + 12), s, font=font, fill=(0, 0, 0, 200), anchor=anchor)
        im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
    if glow:
        gl = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(gl).text(xy, s, font=font, fill=glow + (255,), anchor=anchor)
        im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(22)))
    ImageDraw.Draw(im).text(xy, s, font=font, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=(0, 0, 0))

def emoji(ch, size):
    f = ImageFont.truetype(EMOJI, 109); im = Image.new('RGBA', (136, 128), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((0, 0), ch, font=f, embedded_color=True)
    return im.resize((size, int(size * 128 / 136)), Image.LANCZOS)

def arrow(im, p0, p1, w=22, col=RED):
    d = ImageDraw.Draw(im); d.line([p0, p1], fill=col, width=w)
    v = np.array(p1, float) - np.array(p0, float); v /= np.linalg.norm(v); n = np.array([-v[1], v[0]])
    tip = np.array(p1, float) + v * w * 1.6
    d.polygon([tuple(tip), tuple(np.array(p1) + n * w * 1.6), tuple(np.array(p1) - n * w * 1.6)], fill=col)

def paste_shadow(im, card, xy):
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); a = card.split()[3].point(lambda v: int(v * 0.6))
    blk = Image.new('RGBA', card.size, (0, 0, 0, 255)); blk.putalpha(a); sh.paste(blk, (xy[0] + 14, xy[1] + 20), blk)
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14))); im.alpha_composite(card, xy)

def stamp(word, size, ang, f):
    w = int(f.getlength(word) + size * 0.8); h = int(size * 1.4)
    s = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(s)
    d.rounded_rectangle([4, 4, w - 5, h - 5], radius=int(size * 0.16), outline=RED, width=max(6, size // 9))
    d.text((w / 2, h / 2), word, font=f, fill=RED, anchor='mm')
    return s.rotate(ang, expand=True, resample=Image.BICUBIC)

def message_card(w):
    k = w / 600; h = int(300 * k); im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=int(24 * k), fill=PAPER)
    d.ellipse([24 * k, 24 * k, 104 * k, 104 * k], fill=(201, 162, 39))
    d.text((64 * k, 64 * k), "MG", font=F(E.BODY_B, int(30 * k)), fill=PAPER, anchor='mm')
    d.text((124 * k, 26 * k), "Mr Grant · Hartley Hotels", font=F(E.BODY_B, int(30 * k)), fill=INK)
    d.rounded_rectangle([124 * k, 70 * k, 380 * k, 106 * k], radius=int(18 * k), fill=(255, 176, 32))
    d.text((138 * k, 74 * k), "VIP · £24K A YEAR", font=F(E.MONO_B, int(20 * k)), fill=INK)
    d.rounded_rectangle([24 * k, 130 * k, w - 24 * k, h - 24 * k], radius=int(20 * k), fill=(236, 234, 229))
    d.text((48 * k, 150 * k), "“Send the pretty one", font=F(E.BODY_B, int(36 * k)), fill=INK)
    d.text((48 * k, 200 * k), "again next time.”", font=F(E.BODY_B, int(36 * k)), fill=INK)
    return im.rotate(-5, expand=True, resample=Image.BICUBIC)

def cal_card(w, top, big, sub=None):
    h = int(w * 1.05); im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=int(w * 0.07), fill=PAPER)
    d.rounded_rectangle([0, 0, w - 1, int(h * 0.28)], radius=int(w * 0.07), fill=RED); d.rectangle([0, int(h * 0.18), w - 1, int(h * 0.28)], fill=RED)
    d.text((w / 2, h * 0.14), top, font=F(E.MONO_B, int(w * 0.09)), fill=PAPER, anchor='mm')
    d.text((w / 2, h * 0.64), big, font=F(E.HEAD, int(w * 0.5)), fill=INK, anchor='mm')
    return im.rotate(6, expand=True, resample=Image.BICUBIC)

def diary_card(w):
    k = w / 600; h = int(330 * k); im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=int(24 * k), fill=PAPER)
    d.text((26 * k, 20 * k), "DIARY · PEOPLE", font=F(E.MONO_B, int(22 * k)), fill=GREY)
    for i, dd in enumerate(["4 Aug", "3 Sep", "5 Oct"]):
        y = (70 + i * 80) * k; t = "Probation review: Sam"; f = F(E.BODY_B, int(32 * k))
        d.text((26 * k, y), dd, font=F(E.MONO, int(24 * k)), fill=GREY); d.text((140 * k, y - 4 * k), t, font=f, fill=INK)
        d.line([(140 * k, y + 16 * k), (140 * k + f.getlength(t), y + 16 * k)], fill=RED, width=max(3, int(5 * k)))
    st = stamp("POSTPONED", int(70 * k), 10, F(E.HEAD, int(70 * k))); im.alpha_composite(st, (int(w - st.width - 10 * k), int(h - st.height - 6 * k)))
    return im.rotate(-5, expand=True, resample=Image.BICUBIC)

def make13(W, H, vert):
    im = base(W, H, (W * 0.75, H * 0.6) if not vert else (W * 0.5, H * 0.6), glow=(140, 70, 10))
    if not vert:
        bigtext(im, (50, 30), "CUSTOMER", F(E.HEAD, 120), WH)
        bigtext(im, (50, 170), "CROSSED", F(E.HEAD, 120), WH)
        bigtext(im, (50, 310), "THE LINE?", F(E.HEAD, 120), YEL, glow=(255, 170, 0))
        d = ImageDraw.Draw(im); d.rounded_rectangle([50, 480, 650, 570], radius=14, fill=RED)
        d.text((350, 525), "NOW IT’S ON YOU", font=F(E.HEAD, 58), fill=WH, anchor='mm')
        c = message_card(470); paste_shadow(im, c, (W - c.width - 10, 20))
        cc = cal_card(200, "OCT 2026", "30"); paste_shadow(im, cc, (W - cc.width - 60, 400))
        e = emoji("😳", 150); im.alpha_composite(e, (W - 470, 450))
        ImageDraw.Draw(im).text((52, 640), "NEW DUTY FROM 30 OCTOBER 2026", font=F(E.MONO_B, 28), fill=WH)
    else:
        for i, t in enumerate(["CUSTOMER", "CROSSED"]): bigtext(im, (60, 100 + i * 180), t, fit(E.HEAD, "CUSTOMER", 960, 170), WH)
        bigtext(im, (60, 460), "THE LINE?", fit(E.HEAD, "THE LINE?", 960, 190), YEL, glow=(255, 170, 0))
        d = ImageDraw.Draw(im); d.rounded_rectangle([60, 720, W - 60, 840], radius=18, fill=RED)
        d.text((W / 2, 780), "NOW IT’S ON YOU", font=F(E.HEAD, 84), fill=WH, anchor='mm')
        c = message_card(820); paste_shadow(im, c, ((W - c.width) // 2, 920))
        cc = cal_card(300, "OCT 2026", "30"); paste_shadow(im, cc, (W - cc.width - 60, 1360))
        e = emoji("😳", 220); im.alpha_composite(e, (100, 1420))
    return im.convert('RGB')

def make14(W, H, vert):
    im = base(W, H, (W * 0.3, H * 0.45) if not vert else (W * 0.5, H * 0.3), glow=(130, 90, 10))
    if not vert:
        bigtext(im, (40, -20), "6 MONTHS", F(E.HEAD, 330), YEL, glow=(255, 170, 0))
        d = ImageDraw.Draw(im); d.rounded_rectangle([44, 380, 560, 470], radius=14, fill=RED)
        d.text((302, 425), "NOT 2 YEARS", font=F(E.HEAD, 76), fill=WH, anchor='mm')
        c = diary_card(470); paste_shadow(im, c, (W - c.width - 10, 330))
        e = emoji("⏰", 160); im.alpha_composite(e, (W - 200, 130))
        bigtext(im, (44, 510), "UNFAIR DISMISSAL", F(E.HEAD, 92), WH)
        ImageDraw.Draw(im).text((48, 640), "FROM 1 JANUARY 2027 · ENGLAND, SCOTLAND & WALES", font=F(E.MONO_B, 26), fill=WH)
    else:
        bigtext(im, (60, 60), "6", F(E.HEAD, 520), YEL, glow=(255, 170, 0))
        bigtext(im, (60, 560), "MONTHS", fit(E.HEAD, "MONTHS", 960, 380), YEL, glow=(255, 170, 0))
        e = emoji("⏰", 260); im.alpha_composite(e, (W - 360, 180))
        d = ImageDraw.Draw(im); d.rounded_rectangle([60, 960, W - 60, 1080], radius=18, fill=RED)
        d.text((W / 2, 1020), "NOT 2 YEARS", font=F(E.HEAD, 100), fill=WH, anchor='mm')
        c = diary_card(860); paste_shadow(im, c, ((W - c.width) // 2, 1140))
        bigtext(im, (W // 2, 1700), "UNFAIR DISMISSAL · 1 JAN 2027", F(E.HEAD, 80), WH, anchor='mm')
    return im.convert('RGB')

mk = make13 if case == '13' else make14
mk(1280, 720, False).save(O + f'case-{case}_thumbnail_1280x720.png')
mk(1080, 1920, True).save(O + f'case-{case}_cover_1080x1920.png'); print('ok', case)
