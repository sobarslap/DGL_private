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
VO=json.load(open(B+'vo.json'))
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
    for (a,b,lab,vo),os_ in zip(VO[cfg['vk']],cfg['onscreen']):
        rows.append([P(f'{ts(a)}–{ts(b)}',cell),P(X(lab.capitalize()),cell),P(X(os_),cell),P(X(' '.join(vo)),cell)])
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

C5=dict(vk='c5',accent=PLUM,kicker='CASE FILE № 05 · VERSION 4 (SEO)',title='Limitation of liability clause: 4 myths',
 sub='“This one line just cost a firm £54,500.”',file='videos/dogetlawyer_case-file-05_v4_1080x1920.mp4',
 format='Myth-buster: money-first hook → 4 myths (MYTH stamp, strike-through, TRUTH) → recap → product → 60-second challenge → comment prompt → link in bio',
 look='Plum #241528 / blush #F2E8EC, rose accent, green TRUTH stamps, yellow highlighter. Anton headlines, Inter body, JetBrains Mono labels.',
 topic='Liability caps in supplier terms and conditions, and the Unfair Contract Terms Act 1977 reasonableness test.',
 t1='Limitation of Liability Clause: 4 Myths UK Businesses Believe 🇬🇧', t2='This Supplier T&Cs Clause Cost a UK Firm £54,500 (Liability Cap Explained)',
 hook='“This one line just cost a firm fifty-four grand. It’s a limitation of liability clause. Their machine broke, they lost fifty-eight thousand. The supplier said: we’ll pay three nine.” (On screen: THIS ONE LINE + the clause in yellow highlighter → COST A FIRM £54,500.)',
 onscreen=['THIS ONE LINE + highlighted clause “Our total liability shall not exceed £3,900.” → COST A FIRM £54,500.',
  'LIMITATION OF LIABILITY CLAUSE · £54,500 counts up · Their loss £58,400 · Supplier offered £3,900','ONE’S PROBABLY IN YOUR SUPPLIER T&Cs RIGHT NOW.',
  '4 MYTHS ABOUT THE SMALL PRINT','MYTH #1 stamp · “IT’S IN THE CONTRACT, SO I’M STUCK WITH IT.” (struck through)',
  'THE TRUTH · IT HAS TO PASS THE REASONABLENESS TEST. · UCTA 1977 s.3, s.11(5)','MYTH #2 · “IT’S JUDGED ON THE DAY IT BROKE.”',
  'THE TRUTH · IT’S JUDGED ON THE DAY YOU SIGNED. · UCTA 1977 s.11(1)','MYTH #3 · “A LIABILITY CAP IS NEVER ENFORCEABLE.”',
  'THE TRUTH · PLENTY ARE FAIR AND ENFORCEABLE. · Schedule 2 factors · outcomes turn on the facts','MYTH #4 · “KEEPING RECORDS IS JUST ADMIN.”',
  'THE TRUTH · IT’S YOUR EVIDENCE. · Without vs With (phone call, lost quote vs signed terms v4.2, emails, 11 orders)',
  'RECAP: 4 myths struck through → THE DIFFERENCE? THE PAPER TRAIL.','Product: LIABILITY CAPS · ALL SUPPLIERS → EVERY CAP, IN ONE PLACE.',
  'Product: contract record (v4.2, sent/signed dates, clause 11.3 flagged, 11 orders) → YOUR PAPER TRAIL, SORTED.',
  '60-SECOND CHALLENGE · OPEN YOUR BIGGEST SUPPLIER CONTRACT. · Search: liability','WHICH MYTH DID YOU BELIEVE? 1 · 2 · 3 · 4',
  'DOGETLAWYER · KNOW WHAT YOUR CONTRACTS CAP. · dogetlawyer.com · LINK IN BIO · fine print'],
 delivery='Delivery: fast and punchy for the hook, then a “myth / truth” rhythm with a beat on each strike-through. Friendly, a bit cheeky, never preachy. About 160 words per minute.',
 desc=['This one line in your supplier’s terms and conditions cost a firm £54,500. It’s called a <b>limitation of liability clause</b>, and most UK small businesses believe at least one of these 4 myths about it. 🇬🇧',
  '❌ “It’s in the contract, so I’m stuck with it.”<br/>✅ Under the <b>Unfair Contract Terms Act 1977</b>, a cap in a supplier’s standard terms has to pass the <b>reasonableness test</b>, and the supplier has to prove it.',
  '❌ “It’s judged on the day it broke.”<br/>✅ It’s judged on what you both knew when you signed.',
  '❌ “A liability cap is never enforceable.”<br/>✅ Plenty are fair and enforceable.',
  '❌ “Keeping records is just admin.”<br/>✅ It’s your evidence.',
  '👉 Check your contracts at dogetlawyer.com (link in bio)',
  '0:00 The £54,500 clause · 0:14 Myth 1 · 0:26 Myth 2 · 0:38 Myth 3 · 0:50 Myth 4 · 1:09 How to keep track · 1:25 Your 60-second challenge',
  '<font size="8">Sources: Unfair Contract Terms Act 1977, ss.3, 11 and Schedule 2 (legislation.gov.uk). General position only; outcomes turn on the facts. All names and figures shown are fictional examples. Dogetlawyer is contract management software for UK small businesses, not a substitute for legal advice.</font>'],
 tags='limitation of liability clause, liability cap, unfair contract terms act, UCTA 1977, reasonableness test, supplier terms and conditions, B2B contract UK, small business UK, contract law UK, exclusion clause, unlimited liability, supplier contract, small print, Ltd company',
 hash='#smallbusinessuk #contractlaw #ukbusiness #limitationofliability #smallprint #businesstips', pin='Which myth did you believe: 1, 2, 3 or 4? 👇',
 kw=[('limitation of liability clause','Spoken + on screen in the first 5 seconds; title; description; tags'),('Unfair Contract Terms Act','Spoken + on screen (Myth 1); description'),
  ('reasonableness test','On-screen headline (Myth 1 truth); spoken; description'),('enforceable','Myth 3 and its truth; spoken and on screen'),
  ('supplier terms and conditions / T&Cs','Spoken + on screen (0:07); title alternative'),('standard terms','Spoken (Myth 1)'),('small print / small business UK','On screen; hashtags; tags')],
 src=['UCTA 1977 s.3 (standard terms), s.11(1) (judged at the time of contracting), s.11(5) (burden on the party relying on the clause), Schedule 2 (factors courts use as guidance). General position only; on screen: “outcomes turn on the facts”.',
  'Myth 3’s truth says plenty of caps are fair and enforceable, so the video doesn’t imply every cap can be beaten.',
  'No unverified statistics. The £54,500 example (£58,400 loss − £3,900 cap) and all names are fictional and labelled “FICTIONAL DEMO EXAMPLE”.',
  'No prices, plans or offers. No promise of recovering money. Closing card: “Contract management software for UK small businesses — not a substitute for legal advice.”'])

C6=dict(vk='c6',accent=SCA,kicker='CASE FILE № 06 · VERSION 2 (SEO)',title='Personal guarantees: Ltd company directors',
 sub='“Limited company director? So your house is safe… right?”',file='videos/dogetlawyer_case-file-06_v2_1080x1920.mp4',
 format='Chat-message story → credit form page 4 → what a personal guarantee means (GOV.UK) → 5-point “check before you sign” checklist with ticks → product → “save this” → link in bio',
 look='Court black #121213 / ivory #F4EFE6 / scarlet #E0313F, green ticks, halftone dot background, scarlet edge strip. Archivo Black headlines, Space Grotesk body, IBM Plex Mono labels, Instrument Serif italic asides.',
 topic='Personal guarantees signed by company directors on supplier credit forms, leases and loans.',
 t1='Ltd Company Director? A Personal Guarantee Could Put Your House at Risk 🇬🇧', t2='Personal Guarantee Explained: Can a Supplier Take a Director’s House? (UK)',
 hook='“Limited company director? So your house is safe, right? Not if you’ve signed a personal guarantee.” (On screen: LTD COMPANY DIRECTOR? → SO WHY CAN THEY COME AFTER YOUR HOUSE?)',
 onscreen=['LTD COMPANY DIRECTOR? · “So your house is safe… right?”','SO WHY CAN THEY COME AFTER YOUR HOUSE? · “If you’ve signed a personal guarantee.”',
  'Chat bubbles: “Hiya! Just need a quick signature on the credit account form” · “No worries, signing now” → form page 4 with PERSONAL GUARANTEE box',
  'PERSONAL GUARANTEE. · If the company can’t pay, you do. Personally.','YOUR LTD PROTECTION? GONE. · Your home / Your car / Your savings · Source: GOV.UK Insolvency Service',
  'IT ONLY HAS TO BE IN WRITING AND SIGNED. · Statute of Frauds 1677 s.4','BEFORE YOU SIGN ANYTHING, CHECK THESE 5.',
  'CHECK 1 OF 5 · SEARCH FOR “GUARANTEE”. · tick','CHECK 2 OF 5 · IS THERE A LIMIT? · tick','CHECK 3 OF 5 · HOW DO YOU GET OUT? · tick',
  'CHECK 4 OF 5 · WHO ELSE IS SIGNING? · tick','CHECK 5 OF 5 · GET IT CHECKED FIRST. · tick',
  'IT’S EASY TO FORGET YOU EVER SIGNED IT. UNTIL THE LETTER TURNS UP.','Product: GUARANTEES · ALL CONTRACTS (Halden Timber unlimited · Tannery Lane capped £15,000 · Brookfield none)',
  'SO YOU ALWAYS KNOW WHAT YOU’VE PUT ON THE LINE.','SAVE THIS FOR NEXT TIME SOMEONE SAYS “JUST A QUICK SIGNATURE.”',
  'DOGETLAWYER · KNOW WHAT YOU’VE SIGNED. · dogetlawyer.com · LINK IN BIO · fine print'],
 delivery='Delivery: chatty and slightly alarmed on the viewer’s behalf for the first 30 seconds, then calm and practical through the checklist. A beat after “Personally.” About 165 words per minute.',
 desc=['<b>Limited company director?</b> If you’ve signed a <b>personal guarantee</b>, your company’s protection doesn’t cover that debt, and GOV.UK’s own guidance says your <b>home, car and savings</b> could be used to pay it. 🇬🇧',
  'Suppliers, landlords and lenders ask for personal guarantees all the time, often on a “quick” credit account form. Before you sign, check these 5:',
  '1️⃣ Search for “guarantee” and “indemnity”<br/>2️⃣ Is there a limit, or is it unlimited?<br/>3️⃣ How do you get out? (Some carry on after you leave the company)<br/>4️⃣ Who else is signing? (joint and several)<br/>5️⃣ If your home’s on the line, get advice before you sign',
  '👉 Check what you’ve signed at dogetlawyer.com (link in bio)',
  '0:00 Ltd company director? · 0:07 The “quick signature” · 0:14 What a personal guarantee is · 0:33 The 5 checks · 1:22 Never lose track of one',
  '<font size="8">Sources: GOV.UK, Insolvency Service, “Director information hub: Personal guarantees”; Statute of Frauds 1677, s.4. General position in England &amp; Wales. All names and figures shown are fictional examples. Dogetlawyer is contract management software for UK small businesses, not a substitute for legal advice.</font>'],
 tags='personal guarantee, director personal guarantee, personal guarantee UK, limited company director, Ltd company, personal guarantee house, company debt, personally liable, joint and several, credit account, supplier credit form, company insolvency, small business UK, director responsibilities',
 hash='#smallbusinessuk #companydirector #ltdcompany #personalguarantee #ukbusiness #businesstips', pin='Have you ever been asked to sign a personal guarantee? Yes / No 👇',
 kw=[('Ltd company director / director','First words of the video; title; description; tags'),('personal guarantee','Spoken by 0:04; on screen 0:04, 0:14, 1:27; title; tags'),
  ('home, car and savings','On-screen list + spoken, cited to GOV.UK (0:20)'),('suppliers, landlords and lenders','Spoken (0:14); description'),
  ('company debt / personally liable','Spoken (0:14–0:27); tags'),('joint and several','Check 4; description'),('leave the company','Check 3 (“some carry on after you leave”)')],
 src=['GOV.UK, Insolvency Service, “Director information hub: Personal guarantees” (published 23 Dec 2025, updated 20 May 2026): personal assets “such as your home, car, savings and investments could be used to settle that company debt”; lenders, landlords and suppliers request them; joint and several liability.',
  'Statute of Frauds 1677, s.4: a guarantee must be in writing and signed. General position in England & Wales.',
  'Check 5 tells viewers to speak to a solicitor before signing if their home is at risk, so the video doesn’t replace advice. The product is shown holding guarantees a person has recorded (not detecting them automatically).',
  'No statistics. All names and figures are fictional and labelled. No prices, plans or offers. Standard fine print on the closing card.'])

def cover(story):
    story.append(Spacer(1,6*mm))
    story.append(P('DOGETLAWYER · CONTENT FOR REVIEW',S('ck',fontName='Mono',fontSize=10,textColor=SCA)))
    story.append(P('Case Files 05 &amp; 06',S('ct',fontName='Head',fontSize=34,leading=40)))
    story.append(P('Scripts, descriptions, thumbnails and SEO: ready to post',S('cs',fontSize=14,leading=19,textColor=MUT)))
    story.append(Spacer(1,12))
    story.append(P('Prepared 3 October 2026',small)); story.append(Spacer(1,16))
    story.append(P('What changed after the last round of feedback',h2))
    for t in ['<b>Hooks:</b> new, eye-catching openers with a money or personal stake in the first 2 seconds (“This one line just cost a firm £54,500”, “Ltd company director? So your house is safe… right?”).',
              '<b>Language:</b> conversational British English used UK-wide (“fifty-four grand”, “on the hook”, “who had the clout”, “just a quick signature”). No regional slang.',
              '<b>SEO:</b> researched UK search phrases are spoken and shown in the first 5 seconds and used in titles, descriptions and tags: “limitation of liability clause”, “reasonableness test”, “enforceable”, “Ltd company director”, “personal guarantee”, “home, car and savings”.',
              '<b>Conversion:</b> both videos end with “dogetlawyer.com, link in bio” plus a LINK IN BIO button; Case 05 adds a comment prompt and a 60-second challenge; Case 06 adds “save this”.',
              '<b>Format &amp; look:</b> each video uses a different format, palette and font family. Case 05: myth-buster, plum/rose, Anton. Case 06: chat story + 5-point checklist, black/scarlet, Archivo Black.',
              '<b>Compliance:</b> no prices or offers, no claims of certification or money recovery, legal points hedged as “general position”, fictional demo data labelled, standard fine print on every closing card.']:
        story.append(P('• '+t)); story.append(Spacer(1,3))
    story.append(P('Before posting (both videos)',h2))
    for t in ['Record the voiceover (clean reads on the script pages) or generate it, and drop it onto the silent audio track.',
              'Set <b>dogetlawyer.com</b> as the link in bio on YouTube, Instagram and TikTok; the videos send people there.',
              'Upload the matching thumbnail / vertical cover, paste the title, description, tags and pinned comment.',
              'Judge results on <b>average % viewed after 24 hours</b> (the auto-renewal video got 5.6%; the boss’s example got 57.3%).']:
        story.append(P('□ '+t)); story.append(Spacer(1,3))
    story.append(P('Files',h2))
    story.append(tbl([[P('<b>Item</b>',cell),P('<b>File (repo: sobarslap/DGL_private, branch claude/beautiful-lamport-e2idkm)</b>',cell)],
      [P('Case 05 video',cell),P('videos/dogetlawyer_case-file-05_v4_1080x1920.mp4',mono)],[P('Case 06 video',cell),P('videos/dogetlawyer_case-file-06_v2_1080x1920.mp4',mono)],
      [P('Thumbnails',cell),P('thumbnails/case-05_thumbnail_1280x720.png · case-05_cover_1080x1920.png · case-06_thumbnail_1280x720.png · case-06_cover_1080x1920.png',mono)],
      [P('Keyword research',cell),P('scripts/seo-keywords_case-05-06.md',mono)]],[35*mm,137*mm]))
    story.append(PageBreak())

def foot(c,doc):
    c.saveState(); c.setFont('Mono',7); c.setFillColor(MUT)
    c.drawString(18*mm,10*mm,'Dogetlawyer · Case Files 05 & 06 · internal review'); c.drawRightString(A4[0]-18*mm,10*mm,f'Page {doc.page}'); c.restoreState()
doc=BaseDocTemplate(R+'Dogetlawyer_Case-05-06_Scripts-Descriptions-Thumbnails.pdf',pagesize=A4,leftMargin=18*mm,rightMargin=18*mm,topMargin=16*mm,bottomMargin=18*mm,
                    title='Dogetlawyer Case Files 05 & 06: scripts, descriptions, thumbnails',author='Dogetlawyer content team')
doc.addPageTemplates([PageTemplate(id='p',frames=[Frame(doc.leftMargin,doc.bottomMargin,doc.width,doc.height)],onPage=foot)])
story=[]; cover(story); case(story,'case-05',C5); case(story,'case-06',C6); story.pop()
doc.build(story); print('ok')
