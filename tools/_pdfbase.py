import json
from xml.sax.saxutils import escape as X
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
                                Image, PageBreak, KeepTogether)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
B='/tmp/claude-0/-home-user-DGL-private/f3f04cd2-c6be-58d9-99ed-c95e44436400/scratchpad/'
R='/home/user/DGL_private/'
for n,f in [('In','Inter_400Regular'),('InM','Inter_500Medium'),('InSB','Inter_600SemiBold'),('InB','Inter_700Bold'),('InI','Inter_400Regular_Italic')]:
    pdfmetrics.registerFont(TTFont(n,B+'c5/f/'+f+'.ttf'))
pdfmetrics.registerFont(TTFont('Mono',B+'c6/f/IBMPlexMono_500Medium.ttf'))
pdfmetrics.registerFont(TTFont('Head',B+'c6/f/ArchivoBlack_400Regular.ttf'))
INK=colors.HexColor('#1A1A1A'); MUT=colors.HexColor('#5A5A5A'); LINE=colors.HexColor('#DDDDDD')
PLUM=colors.HexColor('#7A2F55'); SCA=colors.HexColor('#C21F30'); PALE=colors.HexColor('#F6F3EE')
S=lambda name,**k: ParagraphStyle(name,**{**dict(fontName='In',fontSize=9.6,leading=13.6,textColor=INK),**k})
body=S('b'); small=S('s',fontSize=8.2,leading=11,textColor=MUT); mono=S('m',fontName='Mono',fontSize=7.6,leading=10,textColor=MUT)
h1=S('h1',fontName='Head',fontSize=22,leading=26,spaceAfter=4); h2=S('h2',fontName='InB',fontSize=13,leading=17,spaceBefore=12,spaceAfter=6)
h3=S('h3',fontName='InSB',fontSize=10.5,leading=14,spaceBefore=8,spaceAfter=4)
cell=S('c',fontSize=8.4,leading=11.2); cellb=S('cb',fontName='InSB',fontSize=8.4,leading=11.2)
quote=S('q',fontName='In',fontSize=10,leading=15,leftIndent=10,borderPadding=(8,8,8,8),backColor=PALE)
EMO={' 🇬🇧':'',"🇬🇧":'','❌ ':'<font color="#C21F30"><b>MYTH:</b></font> ','✅ ':'<font color="#1F8A5B"><b>TRUTH:</b></font> ','👉 ':'→ ',' 👇':'','1️⃣ ':'1. ','2️⃣ ':'2. ','3️⃣ ':'3. ','4️⃣ ':'4. ','5️⃣ ':'5. ','☐ ':'□ ',' ✗':' (✗)',' ✓':' (✓)'}
def clean(t):
    for k,v in EMO.items(): t=t.replace(k,v)
    return t
P=lambda t,st=body: Paragraph(clean(t),st)

def tbl(rows,widths,head=True,accent=INK):
    if head: rows=[[Paragraph(c.getPlainText(),S('hh',fontName='InSB',fontSize=8.4,leading=11.2,textColor=colors.white)) for c in rows[0]]]+rows[1:]
    t=Table(rows,colWidths=widths,repeatRows=1 if head else 0)
    st=[('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,-1),0.4,LINE),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),('LEFTPADDING',(0,0),(-1,-1),4)]
    if head: st+= [('BACKGROUND',(0,0),(-1,0),accent),('TEXTCOLOR',(0,0),(-1,0),colors.white)]
    t.setStyle(TableStyle(st)); return t
def ts(x): x=int(round(x)); return f"{x//60}:{x%60:02d}"

def case(story, key, cfg):
    acc=cfg['accent']
    story.append(P(cfg['kicker'],S('k',fontName='Mono',fontSize=8.5,textColor=acc)))
    story.append(P(X(cfg['title']),h1))
    story.append(P(X(cfg['sub']),S('sub',fontSize=10.5,leading=14,textColor=MUT)))
    story.append(Spacer(1,8))
    story.append(tbl([[P('<b>Video file</b>',cell),P(X(cfg['file']),cell)],[P('<b>Spec</b>',cell),P('1:45 (105 s) · 1080×1920 vertical · 30 fps · captions burned in · silent audio track ready for voiceover',cell)],
                      [P('<b>Format</b>',cell),P(X(cfg['format']),cell)],[P('<b>Look</b>',cell),P(X(cfg['look']),cell)],[P('<b>Topic</b>',cell),P(X(cfg['topic']),cell)]],[32*mm,140*mm],head=False))
    story.append(P('Thumbnails',h2))
    story.append(Table([[Image(R+f'thumbnails/{key}_thumbnail_1280x720.png',width=118*mm,height=66.4*mm),
                         Image(R+f'thumbnails/{key}_cover_1080x1920.png',width=37.3*mm,height=66.4*mm)]],colWidths=[122*mm,45*mm]))
    story.append(P(f'Left: YouTube thumbnail 1280×720 (thumbnails/{key}_thumbnail_1280x720.png). Right: vertical cover for Shorts / Reels / TikTok 1080×1920 (thumbnails/{key}_cover_1080x1920.png).',small))
    story.append(P('Titles',h2))
    story.append(P('<b>Recommended:</b> '+X(cfg['t1']))); story.append(P('<b>Alternative:</b> '+X(cfg['t2']))); story.append(P('Add the UK flag emoji at the end of the title when posting.',small))
    story.append(P('Hook (first 3–7 seconds)',h2)); story.append(P(X(cfg['hook']),quote))
    story.append(PageBreak())
    story.append(P('Script: scene by scene',h2))
    rows=[[P('<b>Time</b>',cell),P('<b>Section</b>',cell),P('<b>On screen</b>',cell),P('<b>Voiceover</b>',cell)]]
    for (a,b,lab,vo),os_,thn in zip(cfg['sc'],cfg['onscreen'],cfg['th']):
        rows.append([P(f'{ts(a)}–{ts(b)}',cell),P(X(lab.capitalize())+'<br/><font color="#888888" size="7">'+X(thn)+'</font>',cell),P(X(os_),cell),P(X(' '.join(vo)),cell)])
    story.append(tbl(rows,[19*mm,25*mm,58*mm,70*mm],accent=acc))
    story.append(P('Voiceover: clean read for the voice artist',h2))
    story.append(P(X(cfg['delivery']),small)); story.append(Spacer(1,4))
    story.append(P(X(' '.join(' '.join(v) for *_,v in cfg['sc'])),quote))
    story.append(PageBreak())
    story.append(P('Description (YouTube / Shorts; trim for Instagram & TikTok)',h2))
    for para in cfg['desc']: story.append(P(para)); story.append(Spacer(1,3))
    story.append(P('Tags',h3)); story.append(P(X(cfg['tags']),cell))
    story.append(P('Hashtags',h3)); story.append(P(X(cfg['hash']),cell))
    story.append(P('Pinned comment',h3)); story.append(P(X(cfg['pin'])+' <font color="#5A5A5A">(add a pointing-down emoji when posting)</font>'))
    story.append(P('SEO keywords used (and where)',h2))
    story.append(tbl([[P('<b>Keyword</b>',cell),P('<b>Where it appears</b>',cell)]]+[[P(X(k),cellb),P(X(v),cell)] for k,v in cfg['kw']],[55*mm,117*mm],accent=acc))
    story.append(P('Sources & compliance',h2))
    for s_ in cfg['src']: story.append(P('• '+X(s_),cell))
    story.append(PageBreak())

