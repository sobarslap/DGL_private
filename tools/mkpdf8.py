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
VO=json.load(open(B+'vo8.json')); THN=VO['th']
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
    for (a,b,lab,vo),os_,thn in zip(VO[cfg['vk']],cfg['onscreen'],THN):
        rows.append([P(f'{ts(a)}–{ts(b)}',cell),P(X(lab.capitalize())+'<br/><font color="#888888" size="7">'+X(thn)+'</font>',cell),P(X(os_),cell),P(X(' '.join(vo)),cell)])
    story.append(tbl(rows,[19*mm,25*mm,58*mm,70*mm],accent=acc))
    story.append(P('Voiceover: clean read for the voice artist',h2))
    story.append(P(X(cfg['delivery']),small)); story.append(Spacer(1,4))
    story.append(P(X(' '.join(' '.join(v) for *_,v in VO[cfg['vk']])),quote))
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

ORANGE=colors.HexColor('#2433E0')
C7=dict(vk='c8',accent=ORANGE,kicker='CASE FILE 08 · QUIZ FORMAT · MULTI-COLOUR SCENES (NEW PALETTE SET)',title='Paid for it. Do you own the copyright?',
 sub='“You paid £800 for your logo. So why might it still belong to the designer?”',file='videos/dogetlawyer_case-file-08_1080x1920.mp4',
 format='Hook → “paying ≠ owning” → GOV.UK quote → “Who owns it?” quiz (logo, website, product photos, staff’s work) → permission vs ownership → why it bites → the fix (written assignment) → product → comment prompt → link in bio',
 look='Same structure as the brief (every scene its own colour combination) with a brand-new, brighter set: electric blue & hot pink, black & lime, sunshine yellow, teal & coral, magenta & navy, turquoise, violet & tangerine, cherry & cream, repeating. Bebas Neue headlines, DM Sans body, DM Mono labels, Fraunces italic asides; faint concentric rings in the background; progress bar along the top.',
 topic='Copyright in work you commission (logos, websites, photos): the creator owns it unless it’s assigned in writing.',
 t1='Paid for Your Logo? You Might Not Own It 🇬🇧 Copyright for UK Small Businesses', t2='Who Owns Your Logo, Website and Photos? (Copyright Quiz, UK) 🇬🇧',
 hook='“You paid eight hundred quid for your logo. So why might it still belong to the designer? Here’s the bit nobody tells you. Paying for it isn’t the same as owning it.” (On screen: YOU PAID £800 FOR YOUR LOGO. → SO WHY MIGHT IT STILL BELONG TO THE DESIGNER? → PAYING ≠ OWNING.)',
 onscreen=['YOU PAID £800 FOR YOUR LOGO.','SO WHY MIGHT IT STILL BELONG TO THE DESIGNER?','THE BIT NOBODY TELLS YOU · PAYING ≠ OWNING.',
  'GOV.UK / Intellectual Property Office quote on commissioned works → UNLESS IT’S IN WRITING.','QUICK QUIZ · WHO OWNS IT?',
  'Q1 YOUR LOGO (freelance designer) → THE DESIGNER ✗ · unless there’s a written assignment','Q2 YOUR WEBSITE (web agency) → THE AGENCY ✗ · or joint owners if your staff helped',
  'Q3 PRODUCT PHOTOS (freelance photographer) → THE PHOTOGRAPHER ✗ · unless there’s a written assignment','Q4 STAFF’S WORK (employee, as part of their job) → YOU ✓',
  'PERMISSION. NOT OWNERSHIP. · a limited licence','WHY IT BITES: 01 tweak or reuse it · 02 selling the business · 03 they reuse it → IT’S NOT YOURS TO DECIDE.',
  'THE FIX · GET IT IN WRITING. · copyright assignment, signed · final AND source files · kept with the invoice · CDPA 1988 s.90(3)',
  'ALREADY PAID WITHOUT ONE? IT’S NOT TOO LATE TO ASK.','Product: WHO OWNS WHAT · ALL SUPPLIERS (Kite & Co logo: assignment signed · Northgate website: no assignment on file · Fenwick photos: licence only)',
  'SO YOU KNOW WHAT’S ACTUALLY YOURS.','WHICH ONE SURPRISED YOU? 1 · 2 · 3 · 4','DOGETLAWYER · OWN WHAT YOU PAID FOR. · dogetlawyer.com · LINK IN BIO · fine print'],
 delivery='Delivery: friendly and slightly incredulous for the hook, quick-fire quiz-show rhythm for the four questions (a beat before each answer), then calm and practical for the fix. About 160 words per minute.',
 desc=['You paid £800 for your logo, so it’s yours, right? Not necessarily. 🇬🇧 Under UK law, when you <b>commission</b> a logo, website or photos from a freelancer or agency, the person who made it usually owns the <b>copyright</b>, unless it’s <b>assigned to you in writing</b>.',
  'Quick quiz: who owns your logo, your website, your product photos and your staff’s work? (Answers in the video.)',
  'Without a written assignment you may only have <b>permission</b> to use it, not ownership. That matters when you want to change it, sell your business, or stop them reusing it.',
  'The fix:<br/>1️⃣ Get a copyright assignment, in writing and signed<br/>2️⃣ Make sure it covers final files AND source files<br/>3️⃣ Keep it with the invoice',
  '👉 Check who owns what at dogetlawyer.com (link in bio)',
  '0:00 You paid £800 for your logo · 0:12 What GOV.UK says · 0:20 Quiz: who owns it? · 0:52 Permission vs ownership · 1:06 The fix · 1:21 Keeping track · 1:33 Your turn',
  '<font size="8">Sources: GOV.UK, Intellectual Property Office, “Ownership of copyright works”; Copyright, Designs and Patents Act 1988, ss.11 and 90(3). General position in the UK; outcomes turn on the facts and the contract. All names and figures shown are fictional examples. Dogetlawyer is contract management software for UK small businesses, not a substitute for legal advice.</font>'],
 tags='who owns the copyright, logo copyright UK, commissioned work copyright, copyright assignment, freelancer copyright, website copyright, photo copyright, intellectual property UK, IP ownership, copyright for small business, graphic designer copyright, CDPA 1988, small business UK, branding',
 hash='#smallbusinessuk #copyright #logodesign #intellectualproperty #ukbusiness #branding', pin='Which one surprised you: 1, 2, 3 or 4? 👇',
 kw=[('who owns the copyright','On-screen panel in every quiz question; spoken; tags'),('logo copyright','Hook (0:00–0:08), Q1, title, thumbnail'),
  ('commissioned work / commission','GOV.UK quote and VO (0:12); description'),('copyright assignment / in writing','The fix (1:06); GOV.UK quote; description'),
  ('website / photos / freelancer','Quiz Q2 and Q3; tags'),('permission vs ownership (licence)','0:52 scene; description'),('intellectual property','Description, tags, hashtags')],
 src=['GOV.UK (Intellectual Property Office), “Ownership of copyright works”: the creator owns commissioned work “and not you the commissioner, unless you otherwise agree it in writing”; courts may imply only a limited licence; joint ownership can arise; employers own employees’ work made in the course of employment. CDPA 1988 s.11 and s.90(3) (assignment must be in writing and signed). General position, hedged in the video. All names/figures fictional; no statistics; no prices or offers; standard fine print on the closing card.'])
def cover(story):
    story.append(Spacer(1,6*mm))
    story.append(P('DOGETLAWYER · CONTENT FOR REVIEW',S('ck',fontName='Mono',fontSize=10,textColor=SCA)))
    story.append(P('Case File 08',S('ct',fontName='Head',fontSize=34,leading=40)))
    story.append(P('“Paid for it. Own the copyright?”: script, description, thumbnails and SEO',S('cs',fontSize=14,leading=19,textColor=MUT)))
    story.append(Spacer(1,8)); story.append(P('Prepared 4 October 2026',small)); story.append(Spacer(1,12))
    story.append(P('How this follows the brief',h2))
    for t in ['<b>Multi-colour slides (same structure, new colours):</b> every scene has its own background combination, now a brighter set: electric blue &amp; hot pink, black &amp; lime, sunshine yellow, teal &amp; coral, magenta &amp; navy, turquoise, violet &amp; tangerine and cherry &amp; cream, repeating. The scene table shows the colour for each.',
              '<b>New hook:</b> “You paid £800 for your logo. So why might it still belong to the designer?”: money first, then a surprise.',
              '<b>New format:</b> a 4-question “Who owns it?” quiz with ✗ / ✓ reveals; viewers guess before each answer lands, which helps people keep watching.',
              '<b>New fonts:</b> Bebas Neue, DM Sans, DM Mono and Fraunces italic (not used in Cases 01–07).',
              '<b>Language &amp; SEO:</b> conversational British English (“eight hundred quid”, “it’s not too late to ask”); researched phrases (“who owns the copyright”, “logo copyright”, “commissioned work”, “copyright assignment”) spoken and shown early and used in the title, description and tags. Authority: a direct quote from GOV.UK’s Intellectual Property Office.',
              '<b>Conversion:</b> “Which one surprised you? Comment 1–4” prompt plus “dogetlawyer.com, link in bio” with a LINK IN BIO button.',
              '<b>Compliance:</b> no prices or offers, legal points hedged as “general position”, all names/figures fictional and labelled, standard fine print on the closing card.']:
        story.append(P('• '+t)); story.append(Spacer(1,3))
    story.append(P('Before posting',h2))
    for t in ['Record the voiceover (clean read on page 4) and drop it onto the silent audio track.','Make sure dogetlawyer.com is the link in bio.',
              'Upload the thumbnail / vertical cover and paste the title, description, tags and pinned comment.','Check average % viewed after 24 hours.']:
        story.append(P('□ '+t)); story.append(Spacer(1,3))
    story.append(P('Files',h2))
    story.append(tbl([[P('<b>Item</b>',cell),P('<b>File (repo: sobarslap/DGL_private)</b>',cell)],
      [P('Video',cell),P('videos/dogetlawyer_case-file-08_1080x1920.mp4 (1:45, 1080×1920, silent track for VO)',mono)],
      [P('Thumbnails',cell),P('thumbnails/case-08_thumbnail_1280x720.png · thumbnails/case-08_cover_1080x1920.png',mono)]],[35*mm,137*mm]))
    story.append(PageBreak())

def foot(c,doc):
    c.saveState(); c.setFont('Mono',7); c.setFillColor(MUT)
    c.drawString(18*mm,10*mm,'Dogetlawyer · Case File 08 · internal review'); c.drawRightString(A4[0]-18*mm,10*mm,f'Page {doc.page}'); c.restoreState()
doc=BaseDocTemplate(R+'deliverables/Dogetlawyer_Case-08_Script-Description-Thumbnails.pdf',pagesize=A4,leftMargin=18*mm,rightMargin=18*mm,topMargin=16*mm,bottomMargin=18*mm,
                    title='Dogetlawyer Case File 08: script, description, thumbnails',author='Dogetlawyer content team')
doc.addPageTemplates([PageTemplate(id='p',frames=[Frame(doc.leftMargin,doc.bottomMargin,doc.width,doc.height)],onPage=foot)])
story=[]; cover(story); case(story,'case-08',C7); story.pop()
doc.build(story); print('ok')
