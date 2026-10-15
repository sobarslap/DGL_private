"""Turn a case script .md into a styled A4 PDF (same look as the boss-review PDFs).
Usage: python3 tools/md2pdf.py scripts/case-13_....md OUT.pdf [thumbnail.png] [cover.png]"""
import os, re, sys
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_pdfbase.py')).read())
src, out = sys.argv[1], sys.argv[2]; imgs = sys.argv[3:]
EMO.update({'🇬🇧': '', ' 👇': '', '👇': '', '😳': 'a shocked-face emoji', '⏰': 'an alarm-clock emoji'})
def inline(t):
    t = X(t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'(?<![\w*])_(.+?)_(?!\w)', r'<i>\1</i>', t)
    t = re.sub(r'`(.+?)`', r'<font name="Mono" size="8">\1</font>', t)
    return clean(t)
Pi = lambda t, st=body: Paragraph(inline(t), st)
lines = open(src, encoding='utf-8').read().split('\n')
story = []; i = 0; acc = PLUM; W = A4[0] - 36 * mm
bullet = S('bl', leftIndent=12, bulletIndent=2)
def put_images():
    row = []
    for p in imgs:
        im = Image(p); r = im.imageHeight / im.imageWidth
        w = 112 * mm if im.imageWidth > im.imageHeight else 40 * mm
        im.drawWidth, im.drawHeight = w, w * r; row.append(im)
    if row:
        t = Table([row], colWidths=[r_.drawWidth + 6 * mm for r_ in row]); t.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP')]))
        story.extend([Spacer(1, 4), t, Spacer(1, 6)])
done_img = False
while i < len(lines):
    l = lines[i]
    if l.startswith('# '): story += [Pi(l[2:], h1)]
    elif l.startswith('## '):
        story.append(Pi(l[3:], h2))
        if not done_img and 'thumbnail' in l.lower(): put_images(); done_img = True
    elif l.startswith('### '): story.append(Pi(l[4:], h3))
    elif l.startswith('|'):
        rows = []
        while i < len(lines) and lines[i].startswith('|'):
            cells = [c.strip() for c in lines[i].strip().strip('|').split('|')]
            if not all(re.fullmatch(r':?-+:?', c) for c in cells): rows.append(cells)
            i += 1
        n = len(rows[0]); lens = [max(len(r[k]) for r in rows) for k in range(n)]
        ws = [max(0.12, min(0.65, x / sum(lens))) for x in lens]; ws = [W * x / sum(ws) for x in ws]
        story.append(tbl([[Pi(c, cell) for c in r] for r in rows], ws, accent=acc)); continue
    elif l.startswith('>'):
        buf = []
        while i < len(lines) and lines[i].startswith('>'):
            buf.append(lines[i][1:].strip()); i += 1
        paras = '\n'.join(buf).split('\n\n')
        for p in paras:
            if p.strip(): story += [Spacer(1, 6), Paragraph(inline(p.strip()).replace('\n', '<br/>'), quote), Spacer(1, 6)]
        continue
    elif re.match(r'^\s*[-*] ', l): story.append(Paragraph(inline(re.sub(r'^\s*[-*] ', '', l)), bullet, bulletText='•'))
    elif l.strip():
        buf = [l]
        while i + 1 < len(lines) and lines[i + 1].strip() and not re.match(r'^(#|\||>|\s*[-*] )', lines[i + 1]): i += 1; buf.append(lines[i])
        story.append(Paragraph('<br/>'.join(inline(b.rstrip()) for b in buf), body))
    i += 1
if not done_img: put_images()
def foot(c, d):
    c.saveState(); c.setFont('Mono', 7); c.setFillColor(MUT)
    c.drawString(18 * mm, 10 * mm, 'DOGETLAWYER · ' + os.path.basename(src).replace('.md', '')); c.drawRightString(A4[0] - 18 * mm, 10 * mm, str(d.page)); c.restoreState()
doc = BaseDocTemplate(out, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm, bottomMargin=16 * mm)
doc.addPageTemplates([PageTemplate(frames=[Frame(18 * mm, 16 * mm, W, A4[1] - 32 * mm)], onPage=foot)])
doc.build(story); print('ok', out)
