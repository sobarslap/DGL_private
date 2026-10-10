"""Catchy thumbnails (1280x720) + vertical covers (1080x1920) for Delivery 01 and 02, matching each video's first frame.
Usage: python3 thumbs_d.py 01|02"""
import sys, os
B = os.path.dirname(os.path.abspath(__file__)); O = '/home/user/DGL_private/thumbnails/'
which = sys.argv[1]
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
FD = os.path.join(B, 'd1/f' if which == '01' else 'd2/f')
F = lambda n, s: ImageFont.truetype(os.path.join(FD, n + '.ttf'), s)
if which == '01': HEAD, BODY, BODY_B, MONO_B, SERIF = 'Spectral_800ExtraBold', 'Figtree_500Medium', 'Figtree_700Bold', 'RedHatMono_700Bold', 'Newsreader_500Medium_Italic'
else: HEAD, BODY, BODY_B, MONO_B, SERIF = 'BarlowCondensed_800ExtraBold', 'PlusJakartaSans_500Medium', 'PlusJakartaSans_800ExtraBold', 'AzeretMono_700Bold', 'CrimsonPro_500Medium_Italic'
WH = (255, 255, 255); RED = (230, 45, 40); INK = (26, 26, 26); PAPER = (251, 250, 247); GREY = (111, 106, 98); HIL = (255, 224, 138)
ACC = (255, 194, 166) if which == '01' else (94, 234, 212)
EMOJI = '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf'

def base(W, H, glow_xy, top, glow):
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    gx, gy = glow_xy; d = np.sqrt(((x - gx) / (W * 0.55)) ** 2 + ((y - gy) / (H * 0.55)) ** 2)
    g = np.clip(1 - d, 0, 1)[..., None] ** 1.6
    a = np.array(top, np.float32) * (1 - g) + np.array(glow, np.float32) * g
    a += np.random.default_rng(3).normal(0, 5, (H, W))[..., None]
    return Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert('RGBA')
def bigtext(im, xy, s, font, fill, glow=None, anchor='la'):
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).text((xy[0] + 8, xy[1] + 12), s, font=font, fill=(0, 0, 0, 200), anchor=anchor)
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
    if glow:
        gl = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(gl).text(xy, s, font=font, fill=glow + (255,), anchor=anchor)
        im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(22)))
    ImageDraw.Draw(im).text(xy, s, font=font, fill=fill, anchor=anchor)
def emoji(ch, size):
    f = ImageFont.truetype(EMOJI, 109); im = Image.new('RGBA', (136, 128), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((0, 0), ch, font=f, embedded_color=True)
    return im.resize((size, int(size * 128 / 136)), Image.LANCZOS)
def paste_shadow(im, card, xy):
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); a = card.split()[3].point(lambda v: int(v * 0.6))
    blk = Image.new('RGBA', card.size, (0, 0, 0, 255)); blk.putalpha(a); sh.paste(blk, (xy[0] + 14, xy[1] + 20), blk)
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14))); im.alpha_composite(card, xy)
def stamp(word, size, ang):
    f = F(HEAD, size); w = int(f.getlength(word) + size * 0.8); h = int(size * 1.4)
    s = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(s)
    d.rounded_rectangle([4, 4, w - 5, h - 5], radius=int(size * 0.16), outline=RED, width=max(6, size // 9))
    d.text((w / 2, h / 2), word, font=f, fill=RED, anchor='mm')
    return s.rotate(ang, expand=True, resample=Image.BICUBIC)
def banner(im, box, s, size):
    d = ImageDraw.Draw(im); d.rounded_rectangle(box, radius=16, fill=RED)
    while F(HEAD, size).getlength(s) > box[2] - box[0] - 50: size -= 2
    d.text(((box[0] + box[2]) / 2, (box[1] + box[3]) / 2), s, font=F(HEAD, size), fill=WH, anchor='mm')
def preview(im, x, y, size):
    d = ImageDraw.Draw(im); f = F(MONO_B, size); w = f.getlength("PREVIEW") + size * 1.4
    d.rounded_rectangle([x, y, x + w, y + size * 1.8], radius=int(size * 0.9), fill=ACC)
    d.text((x + w / 2, y + size * 0.9), "PREVIEW", font=f, fill=(20, 20, 30), anchor='mm')

def clause_card(w):
    k = w / 600; h = int(380 * k); im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=int(24 * k), fill=PAPER)
    d.text((30 * k, 28 * k), "REVISED DRAFT v2 · CLAUSE 8.2", font=F(MONO_B, int(22 * k)), fill=GREY)
    d.text((30 * k, 80 * k), "Liability is limited to", font=F(BODY, int(34 * k)), fill=INK)
    d.text((30 * k, 128 * k), "£10,000,", font=F(BODY_B, int(56 * k)), fill=INK)
    d.rectangle([24 * k, 210 * k, 440 * k, 268 * k], fill=HIL)
    d.text((30 * k, 214 * k), "subject to clause 8.3.", font=F(BODY_B, int(38 * k)), fill=INK)
    d.text((30 * k, 310 * k), "Fictional example", font=F(BODY, int(22 * k)), fill=GREY)
    st = stamp("CHANGED", int(56 * k), 10); im.alpha_composite(st, (int(w - st.width - 12 * k), int(h - st.height - 14 * k)))
    return im.rotate(-4, expand=True, resample=Image.BICUBIC)

def bills_card(w):
    k = w / 600; h = int(420 * k); im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=int(24 * k), fill=PAPER)
    d.text((30 * k, 26 * k), "FRIDAY · DUE", font=F(MONO_B, int(24 * k)), fill=GREY)
    for i, (a, b) in enumerate([("Wages", "£10,000"), ("Supplier", "£4,000"), ("Rent", "£3,000")]):
        y = (76 + i * 58) * k
        d.text((30 * k, y), a, font=F(BODY_B, int(36 * k)), fill=INK); d.text((w - 30 * k, y), b, font=F(BODY_B, int(36 * k)), fill=INK, anchor='ra')
    d.text((30 * k, 270 * k), "£17,000", font=F(HEAD, int(110 * k)), fill=RED)
    d.text((w - 30 * k, 380 * k), "Fictional example", font=F(BODY, int(20 * k)), fill=GREY, anchor='rs')
    st = stamp("DUE", int(70 * k), -8); im.alpha_composite(st, (int(w - st.width - 16 * k), int(250 * k)))
    return im.rotate(5, expand=True, resample=Image.BICUBIC)

def make01(W, H, vert):
    im = base(W, H, (W * 0.75, H * 0.6) if not vert else (W * 0.5, H * 0.6), (16, 10, 14), (120, 18, 36))
    if not vert:
        bigtext(im, (46, 30), "CAN THEY", F(HEAD, 120), WH)
        bigtext(im, (46, 180), "SIGN?", F(HEAD, 190), ACC, glow=(255, 120, 80))
        banner(im, [46, 450, 680, 540], "ONE CLAUSE CHANGED", 58)
        c = clause_card(500); paste_shadow(im, c, (W - c.width - 10, 150))
        e = emoji("😬", 150); im.alpha_composite(e, (W - 190, 10))
        ImageDraw.Draw(im).text((50, 600), "MATTER & ASSURANCE · UK LAW FIRMS", font=F(MONO_B, 30), fill=WH)
        preview(im, 50, 650, 22)
    else:
        bigtext(im, (60, 130), "CAN THEY", F(HEAD, 170), WH)
        bigtext(im, (60, 350), "SIGN?", F(HEAD, 235), ACC, glow=(255, 120, 80))
        e = emoji("😬", 190); im.alpha_composite(e, (W - 230, 440))
        banner(im, [60, 720, W - 60, 840], "ONE CLAUSE CHANGED", 82)
        c = clause_card(880); paste_shadow(im, c, ((W - c.width) // 2, 930))
        ImageDraw.Draw(im).text((W / 2, 1640), "MATTER & ASSURANCE · UK LAW FIRMS", font=F(MONO_B, 38), fill=WH, anchor='mm')
        preview(im, W / 2 - 90, 1700, 34)
    return im.convert('RGB')

def make02(W, H, vert):
    im = base(W, H, (W * 0.3, H * 0.4) if not vert else (W * 0.5, H * 0.3), (8, 16, 32), (14, 110, 100))
    if not vert:
        bigtext(im, (46, 10), "CAN YOU COVER", F(HEAD, 140), WH)
        bigtext(im, (46, 165), "FRIDAY?", F(HEAD, 225), ACC, glow=(40, 220, 190))
        banner(im, [46, 470, 600, 560], "SALES UP. CASH TIGHT?", 64)
        c = bills_card(460); paste_shadow(im, c, (W - c.width - 20, 200))
        e = emoji("😰", 150); im.alpha_composite(e, (W - 200, 20))
        ImageDraw.Draw(im).text((50, 610), "BUSINESS INTELLIGENCE · UK SMEs", font=F(MONO_B, 30), fill=WH)
        preview(im, 50, 660, 22)
    else:
        bigtext(im, (60, 100), "CAN YOU", F(HEAD, 220), WH)
        bigtext(im, (60, 330), "COVER", F(HEAD, 220), WH)
        bigtext(im, (60, 560), "FRIDAY?", F(HEAD, 300), ACC, glow=(40, 220, 190))
        e = emoji("😰", 230); im.alpha_composite(e, (W - 300, 360))
        banner(im, [60, 920, W - 60, 1040], "SALES UP. CASH TIGHT?", 92)
        c = bills_card(800); paste_shadow(im, c, ((W - c.width) // 2, 1100))
        ImageDraw.Draw(im).text((W / 2, 1760), "BUSINESS INTELLIGENCE · UK SMEs", font=F(MONO_B, 38), fill=WH, anchor='mm')
        preview(im, W / 2 - 90, 1810, 30)
    return im.convert('RGB')

mk = make01 if which == '01' else make02
mk(1280, 720, False).save(O + f'delivery-{which}_thumbnail_1280x720.png')
mk(1080, 1920, True).save(O + f'delivery-{which}_cover_1080x1920.png'); print('ok', which)
