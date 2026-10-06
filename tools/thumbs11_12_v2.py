"""Catchier thumbnails v2 for Case Files 11 and 12: 2–3 huge words, one hero object, red glow, arrow, reaction emoji,
matching the video's first frame. Usage: python3 thumbs11_12_v2.py 11|12"""
import sys, os
B = os.path.dirname(os.path.abspath(__file__)); O = '/home/user/DGL_private/thumbnails/'
case = sys.argv[1]; sys.path.insert(0, os.path.join(B, f'c{case}')); sys.path.insert(0, B)
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
r = __import__(f'render{case}'); import engine3 as E
F = lambda n, s: ImageFont.truetype(os.path.join(E.FD, n + '.ttf'), s)
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

def email_card(w):
    k = w / 600; h = int(330 * k); im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=int(24 * k), fill=PAPER)
    d.text((30 * k, 34 * k), "To:", font=F(E.MONO_B, int(28 * k)), fill=GREY)
    d.text((95 * k, 28 * k), "Sarah Bentley", font=F(E.BODY_B, int(40 * k)), fill=INK)
    d.ellipse([78 * k, 6 * k, 420 * k, 98 * k], outline=RED, width=max(5, int(7 * k)))
    d.text((30 * k, 130 * k), "Subject: Signed contract", font=F(E.BODY, int(30 * k)), fill=INK)
    d.rounded_rectangle([30 * k, 196 * k, 380 * k, 256 * k], radius=int(12 * k), fill=(239, 236, 230))
    d.text((50 * k, 210 * k), "Bank_details.pdf", font=F(E.MONO_B, int(26 * k)), fill=INK)
    st = stamp("SENT", int(90 * k), 12, F(E.HEAD, int(90 * k))); im.alpha_composite(st, (int(w - st.width - 16 * k), int(h - st.height - 6 * k)))
    return im.rotate(-5, expand=True, resample=Image.BICUBIC)

def invoice_card(w):
    k = w / 600; h = int(360 * k); im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=int(24 * k), fill=PAPER)
    d.text((34 * k, 30 * k), "INVOICE #0412", font=F(E.MONO_B, int(28 * k)), fill=GREY)
    d.text((34 * k, 80 * k), "£8,400", font=F(E.HEAD, int(130 * k)), fill=INK)
    d.text((34 * k, 290 * k), "94 days overdue", font=F(E.BODY_B, int(34 * k)), fill=RED)
    st = stamp("UNPAID", int(80 * k), 10, F(E.HEAD, int(80 * k))); im.alpha_composite(st, (int(w - st.width - 14 * k), int(205 * k)))
    return im.rotate(6, expand=True, resample=Image.BICUBIC)

def timer_box(text_, size):
    f = F(E.MONO_B, size); w = int(f.getlength(text_) + size * 0.7); h = int(size * 1.4)
    im = Image.new('RGBA', (w + 80, h + 80), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.text((40 + size * 0.35, 40 + size * 0.13), text_, font=f, fill=RED + (255,))
    glow = im.filter(ImageFilter.GaussianBlur(18))
    out = Image.new('RGBA', im.size, (0, 0, 0, 0)); od = ImageDraw.Draw(out)
    od.rounded_rectangle([40, 40, 40 + w, 40 + h], radius=int(size * 0.2), fill=(10, 8, 10, 235), outline=RED + (255,), width=max(5, size // 14))
    out.alpha_composite(glow); out.alpha_composite(glow); od = ImageDraw.Draw(out)
    od.text((40 + size * 0.35, 40 + size * 0.13), text_, font=f, fill=RED + (255,))
    return out

def make11(W, H, vert):
    im = base(W, H, (W * 0.5, H * 0.78) if vert else (W * 0.78, H * 0.75))
    if not vert:
        bigtext(im, (50, 30), "WRONG", F(E.HEAD, 165), WH)
        bigtext(im, (50, 210), "EMAIL.", F(E.HEAD, 165), YEL, glow=(255, 170, 0))
        c = email_card(470); paste_shadow(im, c, (W - c.width - 10, 20))
        t = timer_box("71:59:58", 110); im.alpha_composite(t, (10, H - t.height + 10))
        ImageDraw.Draw(im).text((W - 40, H - 60), "THE CLOCK IS TICKING", font=F(E.MONO_B, 34), fill=WH, anchor='rm')
        e = emoji("😱", 170); im.alpha_composite(e, (W - 230, 330))
        arrow(im, (900, 600), (760, 610))
    else:
        bigtext(im, (60, 120), "WRONG", F(E.HEAD, 215), WH)
        bigtext(im, (60, 370), "EMAIL.", F(E.HEAD, 215), YEL, glow=(255, 170, 0))
        c = email_card(900); paste_shadow(im, c, ((W - c.width) // 2, 720))
        e = emoji("😱", 220); im.alpha_composite(e, (W - 280, 640))
        t = timer_box("71:59:58", 150); im.alpha_composite(t, ((W - t.width) // 2, 1300))
        ImageDraw.Draw(im).text((W / 2, 1620), "THE CLOCK IS TICKING", font=F(E.MONO_B, 46), fill=WH, anchor='mm')
    return im.convert('RGB')

def make12(W, H, vert):
    im = base(W, H, (W * 0.3, H * 0.4) if not vert else (W * 0.5, H * 0.35), glow=(120, 14, 22))
    f41 = F(E.HEAD, 300 if not vert else 430)
    if not vert:
        bigtext(im, (40, -10), "41 WEEKS", f41, YEL, glow=(255, 160, 0))
        d = ImageDraw.Draw(im); d.rounded_rectangle([40, 360, 700, 450], radius=14, fill=RED)
        d.text((370, 405), "JUST TO GET TO COURT", font=F(E.HEAD, 64), fill=WH, anchor='mm')
        c = invoice_card(430); paste_shadow(im, c, (W - c.width - 20, 330))
        e = emoji("🤯", 170); im.alpha_composite(e, (W - 220, 150))
        bigtext(im, (40, 500), "“JUST SUE THEM”?", F(E.HEAD, 96), WH)
    else:
        bigtext(im, (60, 80), "41", f41, YEL, glow=(255, 160, 0))
        bigtext(im, (60, 470), "WEEKS", F(E.HEAD, 300), YEL, glow=(255, 160, 0))
        e = emoji("🤯", 260); im.alpha_composite(e, (W - 330, 170))
        d = ImageDraw.Draw(im); d.rounded_rectangle([60, 860, W - 60, 980], radius=18, fill=RED)
        d.text((W / 2, 920), "JUST TO GET TO COURT", font=F(E.HEAD, 92), fill=WH, anchor='mm')
        c = invoice_card(860); paste_shadow(im, c, ((W - c.width) // 2, 1080))
        bigtext(im, (W // 2, 1760), "“JUST SUE THEM”?", F(E.HEAD, 120), WH, anchor='mm')
    return im.convert('RGB')

mk = make11 if case == '11' else make12
mk(1280, 720, False).save(O + f'case-{case}_thumbnail_1280x720.png')
mk(1080, 1920, True).save(O + f'case-{case}_cover_1080x1920.png'); print('ok', case)
