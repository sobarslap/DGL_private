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
VO=json.load(open(B+'vo7.json')); THN=VO['th']
INK=colors.HexColor('#1A1A1A'); MUT=colors.HexColor('#5A5A5A'); LINE=colors.HexColor('#DDDDDD')
PLUM=colors.HexColor('#7A2F55'); SCA=colors.HexColor('#C21F30'); PALE=colors.HexColor('#F6F3EE')
S=lambda name,**k: ParagraphStyle(name,**{**dict(fontName='In',fontSize=9.6,leading=13.6,textColor=INK),**k})
body=S('b'); small=S('s',fontSize=8.2,leading=11,textColor=MUT); mono=S('m',fontName='Mono',fontSize=7.6,leading=10,textColor=MUT)
h1=S('h1',fontName='Head',fontSize=22,leading=26,spaceAfter=4); h2=S('h2',fontName='InB',fontSize=13,leading=17,spaceBefore=12,spaceAfter=6)
h3=S('h3',fontName='InSB',fontSize=10.5,leading=14,spaceBefore=8,spaceAfter=4)
cell=S('c',fontSize=8.4,leading=11.2); cellb=S('cb',fontName='InSB',fontSize=8.4,leading=11.2)
quote=S('q',fontName='In',fontSize=10,leading=15,leftIndent=10,borderPadding=(8,8,8,8),backColor=PALE)
EMO={' 🇬🇧':'',"🇬🇧":'','❌ ':'<font color="#C21F30"><b>MYTH:</b></font> ','✅ ':'<font color="#1F8A5B"><b>TRUTH:</b></font> ','👉 ':'→ ',' 👇':'','1️⃣ ':'1. ','2️⃣ ':'2. ','3️⃣ ':'3. ','4️⃣ ':'4. ','5️⃣ ':'5. ','☐ ':'□ '}
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

ORANGE=colors.HexColor('#5A2A8C')
C7=dict(vk='c7',accent=ORANGE,kicker='CASE FILE 07 · TIMELINE FORMAT · MULTI-COLOUR SCENES',title='“We’re updating our terms and conditions”',
 sub='The supplier email nobody reads, and what it can quietly change.',file='videos/dogetlawyer_case-file-07_1080x1920.mp4',
 format='Timeline: hook → “let’s run the clock” → Day 1 / Day 2 / Day 30 / Day 31–90 / Day 91 / Day 92 → the law (variation clause; silence vs carrying on) → what to do on Day 1 (3 steps) → product → comment prompt → link in bio',
 look='Every scene has its own colour combination, per the brief: scene 1 purple & black, scene 2 grey & red, scene 3 sky blue, then emerald & navy, charcoal & orange, pink & plum, navy & gold, mint & forest, repeating. Text colour is set per scene for contrast. Oswald headlines, Manrope body, Space Mono labels, Lora italic asides, faint diagonal pinstripes, progress bar along the top.',
 topic='Suppliers changing their terms by email (“continued use means you accept”), variation clauses, and acceptance by conduct.',
 t1='“We’re Updating Our Terms and Conditions” — Read This Before You Archive It 🇬🇧', t2='Can a Supplier Change the Terms of a Contract? UK Small Business Guide 🇬🇧',
 hook='“Got an email saying, we’re updating our terms and conditions? Course you didn’t read it. Nobody does. But that email might have just put your prices up eighteen percent.” (On screen: “WE’RE UPDATING OUR TERMS AND CONDITIONS.” → PUT YOUR PRICES UP 18%.)',
 onscreen=['NEW EMAIL · “WE’RE UPDATING OUR TERMS AND CONDITIONS.” · You didn’t read it. Nobody does.','PUT YOUR PRICES UP 18%. (fictional example)',
  'LET’S RUN THE CLOCK · HOW A “QUICK UPDATE” PLAYS OUT.','DAY 1 · email: “Important: changes to our terms and conditions… Continued use of our services means you accept the new terms.” (highlighted)',
  'DAY 2 · YOU ARCHIVE IT.','DAY 30 · WHAT QUIETLY CHANGED: prices reviewed every quarter · notice 60 → 90 days · liability cap halved',
  'DAY 31–90 · YOU KEEP ORDERING.','DAY 91 · invoice: last quarter £4,000 → this quarter £4,720 · +18%','DAY 92 · THEY SEND YOU… THE EMAIL FROM DAY ONE.',
  'CAN A SUPPLIER JUST CHANGE THE TERMS ON YOU?','USUALLY… ONLY IF THE CONTRACT LETS THEM. · look for a “variation clause”',
  'SAYING NOTHING ISN’T ALWAYS AGREEING… …BUT CARRYING ON CAN BE. · general position, England & Wales',
  'REWIND TO DAY 1. DO THIS: 01 Don’t archive it · 02 Disagree? Say so in writing · 03 Diary the start date',
  'Product: TERMS CHANGES · ALL SUPPLIERS (Harrow Print new terms 1 Nov · Kestrel version 3 on file · Norbury no change)','SO DAY ONE NEVER SLIPS PAST YOU.',
  'HAD ONE OF THESE EMAILS THIS YEAR? · COMMENT “TERMS” BELOW','DOGETLAWYER · KNOW WHEN YOUR TERMS CHANGE. · dogetlawyer.com · LINK IN BIO · fine print'],
 delivery='Delivery: chatty and a bit knowing at the start, then a ticking-clock rhythm through the Day 1 / Day 30 / Day 91 beats, calm and practical for the three steps. About 160 words per minute.',
 desc=['Got an email saying <b>“we’re updating our terms and conditions”</b>? Course you didn’t read it. But it might have just put your prices up, lengthened your notice period or cut what they’ll pay if things go wrong. 🇬🇧',
  'Can a supplier just <b>change the terms of a contract</b>? Usually only if the contract lets them, via a <b>variation clause</b>. Saying nothing isn’t always agreeing, but carrying on ordering after the new terms start can count as accepting them.',
  'What to do on Day 1:<br/>1️⃣ Don’t archive it: read what’s changing (price, notice period, liability)<br/>2️⃣ Don’t agree? Say so in writing before the start date<br/>3️⃣ Diary the start date, with a name against it',
  '👉 Check what you’ve agreed to at dogetlawyer.com (link in bio)',
  '0:00 The email nobody reads · 0:11 Day 1 → Day 92 · 0:48 Can they change the terms? · 1:07 What to do on Day 1 · 1:20 Keeping track · 1:37 Your turn',
  '<font size="8">General position in England &amp; Wales; outcomes turn on the facts and the wording of your contract. All names and figures shown are fictional examples. Dogetlawyer is contract management software for UK small businesses, not a substitute for legal advice.</font>'],
 tags='updating our terms and conditions, supplier changed terms, can a supplier change the terms of a contract, variation clause, variation of contract UK, change of terms notice, continued use means acceptance, supplier price increase, notice period, terms of business, small business UK, B2B contract, contract law UK, supplier contract',
 hash='#smallbusinessuk #ukbusiness #termsandconditions #contractlaw #smallprint #businesstips', pin='Had a “we’re updating our terms” email this year? Comment TERMS 👇',
 kw=[('updating our terms and conditions','First words of the video (VO + on screen); title; description; tags'),('change the terms (of a contract)','Spoken + on-screen question (0:48); title alternative'),
  ('variation clause','Spoken + on screen (law scene); description; tags'),('continued use means you accept','On the Day 1 email (highlighted) and spoken'),
  ('price increase / prices up 18%','Hook (0:04) and Day 91 invoice'),('notice period','Day 30 and Day 1 steps'),('terms of business / small business UK','Email copy, description, tags')],
 src=['General contract-law position in England & Wales: a party can usually only vary a contract unilaterally if the contract allows it (a variation clause, often with notice requirements); silence alone is not generally acceptance, but continuing to perform/order after notice of new terms can amount to acceptance by conduct. Hedged on screen: “general position, England & Wales · outcomes turn on the facts”.',
  'Supporting UK guidance reviewed: Harper James (“It should not be assumed that continued use will always amount to acceptance”), Sprintlaw (variation needs consent and compliance with any variation clause), LexisNexis (variation clauses must be clear and properly invoked; notice requirements).',
  'All names, invoices and the 18% figure are fictional and labelled; no statistics. No prices or offers; the product is shown holding saved versions of terms (no email/inbox sync). Standard fine print on the closing card.'])
def cover(story):
    story.append(Spacer(1,6*mm))
    story.append(P('DOGETLAWYER · CONTENT FOR REVIEW',S('ck',fontName='Mono',fontSize=10,textColor=SCA)))
    story.append(P('Case File 07',S('ct',fontName='Head',fontSize=34,leading=40)))
    story.append(P('“We’re updating our terms”: script, description, thumbnails and SEO',S('cs',fontSize=14,leading=19,textColor=MUT)))
    story.append(Spacer(1,8)); story.append(P('Prepared 4 October 2026',small)); story.append(Spacer(1,12))
    story.append(P('How this follows the brief',h2))
    for t in ['<b>Multi-colour slides:</b> every scene has its own background combination: scene 1 purple &amp; black, scene 2 grey &amp; red, scene 3 sky blue, then emerald &amp; navy, charcoal &amp; orange, pink &amp; plum, navy &amp; gold and mint &amp; forest, repeating. The scene table shows the colour for each.',
              '<b>New hook:</b> the supplier email everyone gets and nobody reads, then “that email might have just put your prices up 18%”.',
              '<b>New format:</b> a timeline (Day 1 → Day 92) with a progress bar along the top; the only one of the four formats not used yet.',
              '<b>New fonts:</b> Oswald, Manrope, Space Mono and Lora italic (not used in Cases 01–06).',
              '<b>Language &amp; SEO:</b> conversational British English; researched search phrases (“updating our terms and conditions”, “change the terms of a contract”, “variation clause”, “continued use means acceptance”) spoken and shown early and used in the title, description and tags.',
              '<b>Conversion:</b> “comment TERMS below” prompt plus “dogetlawyer.com, link in bio” with a LINK IN BIO button.',
              '<b>Compliance:</b> no prices or offers, legal points hedged as “general position”, all names/figures fictional and labelled, standard fine print on the closing card.']:
        story.append(P('• '+t)); story.append(Spacer(1,3))
    story.append(P('Before posting',h2))
    for t in ['Record the voiceover (clean read on page 4) and drop it onto the silent audio track.','Make sure dogetlawyer.com is the link in bio.',
              'Upload the thumbnail / vertical cover and paste the title, description, tags and pinned comment.','Check average % viewed after 24 hours.']:
        story.append(P('□ '+t)); story.append(Spacer(1,3))
    story.append(P('Files',h2))
    story.append(tbl([[P('<b>Item</b>',cell),P('<b>File (repo: sobarslap/DGL_private)</b>',cell)],
      [P('Video',cell),P('videos/dogetlawyer_case-file-07_1080x1920.mp4 (1:45, 1080×1920, silent track for VO)',mono)],
      [P('Thumbnails',cell),P('thumbnails/case-07_thumbnail_1280x720.png · thumbnails/case-07_cover_1080x1920.png',mono)]],[35*mm,137*mm]))
    story.append(PageBreak())

def foot(c,doc):
    c.saveState(); c.setFont('Mono',7); c.setFillColor(MUT)
    c.drawString(18*mm,10*mm,'Dogetlawyer · Case File 07 · internal review'); c.drawRightString(A4[0]-18*mm,10*mm,f'Page {doc.page}'); c.restoreState()
doc=BaseDocTemplate(R+'deliverables/Dogetlawyer_Case-07_Script-Description-Thumbnails.pdf',pagesize=A4,leftMargin=18*mm,rightMargin=18*mm,topMargin=16*mm,bottomMargin=18*mm,
                    title='Dogetlawyer Case File 07: script, description, thumbnails',author='Dogetlawyer content team')
doc.addPageTemplates([PageTemplate(id='p',frames=[Frame(doc.leftMargin,doc.bottomMargin,doc.width,doc.height)],onPage=foot)])
story=[]; cover(story); case(story,'case-07',C7); story.pop()
doc.build(story); print('ok')
