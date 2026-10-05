"""Boss-review PDFs for Case Files 09 and 10 (script, description, thumbnails, SEO). Usage: python3 tools/mkpdf9_10.py"""
import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_pdfbase.py')).read())
for k in ('9', '10'):
    VOJ = json.load(open(R + f'scripts/vo{k}.json'))
    globals()[f'SC{k}'] = [tuple(x) for x in VOJ['sc']]; globals()[f'TH{k}'] = VOJ['th']
short = lambda n: n.split(' · ')[1] if ' · ' in n else n

C9 = dict(sc=SC9, th=[short(t) for t in TH9], accent=colors.HexColor('#0E4634'),
 kicker='CASE FILE 09 · CASH CALENDAR + 4-LINE CHECK · COLOUR BY SECTION', title='£20,000 in sales. £600 in the bank.',
 sub='“The diary’s full. So why is Friday still stressful?” Payment terms and cash flow (Short 10, Business health)',
 file='videos/dogetlawyer_case-file-09_1080x1920.mp4',
 format='Hook (sales vs bank balance) → cash calendar (money out on days 7, 14 and 28; customer pays on day 60) → “4 lines that decide when you get paid” → what GOV.UK says → ask for terms that match your bills → product → comment prompt → link in bio',
 look='Colour changes once per section (5 changes): forest & black (hook), burgundy & charcoal (the gap), petrol blue (the 4 lines), plum & ink (the fix), back to forest for the close. Dark, calm grounds with a faint calendar grid; bright colour only on key words. Big Shoulders Display headlines, Plus Jakarta Sans body, Red Hat Mono labels, Newsreader italic asides.',
 topic='Payment terms in your contracts decide when cash actually arrives: terms, when the clock starts, deposits/stage payments, and the default if nothing is agreed.',
 t1='£20,000 in Sales, £600 in the Bank? It Might Be Your Payment Terms 🇬🇧', t2='Busy but Broke? 4 Contract Lines That Decide When You Get Paid (UK) 🇬🇧',
 hook='“Twenty grand in sales this month. Six hundred quid actually in the bank. The diary’s full. So why is Friday still stressful?” (On screen: £20,000 IN SALES. → £600. → SO WHY IS FRIDAY STILL STRESSFUL? → IT’S THE TIMING.)',
 onscreen=['THIS MONTH · £20,000 IN SALES.', 'IN THE BANK · £600. · Available. Right now.', 'THE DIARY’S FULL. SO WHY IS FRIDAY STILL STRESSFUL?',
  'IT’S THE TIMING. · And the timing is written in your contracts.', 'Calendar: OUT on day 7 (supplier), 14 (rent), 28 (wages) · MONEY IN: customer pays on day 60. Not this month.',
  'YOU PAY IN 14 DAYS · THEY PAY IN 60 DAYS (bars) · That gap is where Friday gets stressful.', '4 LINES THAT DECIDE WHEN YOU GET PAID.',
  'LINE 1 OF 4 · THE PAYMENT TERMS. · 30 days? 60 days? 90 days?', 'LINE 2 OF 4 · WHEN THE CLOCK STARTS. · “60 days end of month” · Invoice on the 2nd? That can be nearly 90 days.',
  'LINE 3 OF 4 · DEPOSITS & STAGE PAYMENTS. · Up front? At milestones? All at the end?',
  'LINE 4 OF 4 · NOTHING AGREED? · GOV.UK quote: late 30 days after the invoice or delivery (if later) · Late Payment of Commercial Debts (Interest) Act 1998',
  'OVER 60 DAYS? IT MUST BE FAIR TO BOTH. · GOV.UK quote', 'ASK FOR TERMS THAT MATCH YOUR BILLS. · ✓ Shorter payment terms ✓ A deposit up front ✓ Stage payments',
  'Product: PAYMENT TERMS · ALL CONTRACTS (Money in: Brightwell Retail 60 days end of month; Corran Events 30 days + 25% deposit · Money out: Ashby Packaging 14 days; Unit 4, Mill Lane lease monthly on the 1st)',
  'SO PAYDAY ISN’T A SURPRISE.', 'WHAT TERMS DO YOUR CUSTOMERS GET? 14 · 30 · 60 · 90', 'DOGETLAWYER · KNOW WHEN YOU’RE PAID. · dogetlawyer.com · LINK IN BIO · fine print'],
 delivery='Delivery: chatty and a bit exasperated for the hook (“twenty grand… six hundred quid”), slower and clear through the calendar, then brisk and practical for the four lines. About 155 words per minute.',
 desc=['Busy month, but nothing in the bank? 🇬🇧 Often it’s not your sales, it’s the <b>payment terms</b> in your contracts. If you pay suppliers in 14 days but customers pay you in 60, that gap is where <b>cash flow</b> gets tight.',
  'Check these 4 lines in your contracts:<br/>1️⃣ The payment terms (30, 60, 90 days?)<br/>2️⃣ When the clock starts (“60 days end of month” can mean nearly 90)<br/>3️⃣ Deposits and stage payments<br/>4️⃣ What happens if no payment date is agreed',
  '👉 Keep every contract’s payment terms in one place at dogetlawyer.com (link in bio)',
  '0:00 £20,000 in sales, £600 in the bank · 0:17 The cash gap · 0:32 4 lines to check · 1:01 What GOV.UK says · 1:17 Before you sign · 1:21 Keeping track · 1:35 Your turn',
  '<font size="8">Source: GOV.UK, “Late commercial payments: charging interest and debt recovery” (when a payment becomes late); Late Payment of Commercial Debts (Interest) Act 1998. General position in England &amp; Wales; outcomes turn on the facts and the contract. All names and figures shown are fictional examples. Dogetlawyer is contract management software for UK small businesses, not a substitute for legal advice.</font>'],
 tags='payment terms, cash flow, cash flow problems small business, 30 day payment terms, 60 day payment terms, end of month payment terms, late payment UK, invoice payment terms, deposit, stage payments, small business UK, business health',
 hash='#smallbusinessuk #cashflow #paymentterms #invoice #ukbusiness #latepayment #businesstips', pin='What terms do your customers get: 14, 30, 60 or 90 days? 👇',
 kw=[('payment terms', 'Spoken at 0:12 and 0:32; Line 1; title; description'), ('cash flow', 'Description, tags, alt title'), ('30 / 60 / 90 days', 'Line 1 chips; comment prompt'),
     ('end of month', 'Line 2'), ('late payment / GOV.UK', 'Line 4 quote; sources'), ('deposit / stage payments', 'Line 3; the fix')],
 src=['GOV.UK, “Late commercial payments: charging interest and debt recovery”, quoted verbatim: with no agreed date, payment is late 30 days after the customer gets the invoice or you deliver (if later); terms over 60 days for business transactions must be fair to both businesses. Late Payment of Commercial Debts (Interest) Act 1998.',
      'Short 10 rule held: no claim that Dogetlawyer recovers money, chases invoices or manages cash. It is shown holding payment terms on record only. “Ask for terms that match your bills” is a commercial tip, not legal advice.',
      'No statistics; no prices or offers; demo scene labelled FICTIONAL DEMO EXAMPLE; standard fine print on the closing card.'])

C10 = dict(sc=SC10, th=[short(t) for t in TH10], accent=colors.HexColor('#C2551A'),
 kicker='CASE FILE 10 · SPOT-THE-DIFFERENCE GAME · COLOUR BY SECTION', title='FINAL. FINAL2. FINAL_ACTUALLY_FINAL.',
 sub='“Which one did you sign?” Contract versions and the signed copy (Short 11, Which final?)',
 file='videos/dogetlawyer_case-file-10_1080x1920.mp4',
 format='Hook (file names stacking up) → “Which one did you sign?” → spot-the-difference game, 3 rounds with a 3-second countdown (payment 30 → 60 days; notice 1 → 3 months; liability cap shrinks) → entire agreement clause → e-signatures usually count → 3 checks → product → comment prompt → link in bio',
 look='Colour changes once per section (5 changes): charcoal & ember (hook), deep navy & teal (the game), aubergine (the law), bottle green (the fix), back to charcoal & ember for the close. Dark, calm grounds with a soft glow; clauses shown on white “paper” cards with the change highlighted. Bricolage Grotesque headlines, Outfit body, Fira Code labels, Libre Baskerville for documents and italic asides.',
 topic='Version confusion: small changes between drafts can change the deal, the signed version is usually what counts, so check changes and keep the signed copy.',
 t1='FINAL, FINAL2, FINAL_ACTUALLY_FINAL: Which Contract Did You Sign? 🇬🇧', t2='Spot the Difference: 3 Contract Changes Nobody Tells You About (UK) 🇬🇧',
 hook='“Final. Final two. Final, actually final. Quick question. Which one did you actually sign? Everyone’s got the contract. Not everyone’s got the same one.” (On screen: Contract_FINAL.docx / FINAL2 / FINAL_ACTUALLY_FINAL → WHICH ONE DID YOU SIGN?)',
 onscreen=['SHARED DRIVE · Contract_FINAL.docx / Contract_FINAL2.docx / Contract_FINAL_ACTUALLY_FINAL.docx · FINAL. FINAL2. FINAL_ACTUALLY_FINAL.',
  'WHICH ONE DID YOU SIGN?', 'EVERYONE HAS THE CONTRACT. NOT EVERYONE HAS THE SAME ONE.', 'SPOT THE DIFFERENCE. · Three rounds. Three seconds each. Go.',
  'ROUND 1 OF 3 · Version 3 vs Version 4 payment clause · 3-2-1 · highlight 30 → 60 · 30 BECAME 60.',
  'ROUND 2 OF 3 · notice clause · highlight one month’s → three months’ · 1 MONTH BECAME 3.',
  'ROUND 3 OF 3 · liability clause · highlight “under this agreement” → “in the last three months” · THE CAP SHRANK.',
  'ONE WORD. ONE NUMBER. DIFFERENT DEAL.', 'THE SIGNED ONE IS USUALLY THE DEAL. · “12. Entire agreement” clause card (typical wording, fictional example)',
  'IT USUALLY COUNTS. · Law Commission quote on electronic signatures (2019, England & Wales)', '3 QUICK CHECKS.',
  '01 Ask what’s changed · 02 Read the one you’re signing · 03 Save the signed copy (each ticks)',
  'Product: SIGNED VERSIONS · ALL CONTRACTS (Ellison Freight v4 · 12 Aug 2026; Marlow Studio v2 · 3 Jun 2026; Pell & Hart Supplies: not signed yet, draft v3) · So nobody’s working from FINAL2.',
  'ONE CONTRACT. ONE VERSION.', 'MOST “FINALS” YOU’VE SEEN ON ONE FILE? 2 · 3 · 4 · 5+', 'DOGETLAWYER · KNOW WHICH ONE YOU SIGNED. · dogetlawyer.com · LINK IN BIO · fine print'],
 delivery='Delivery: playful for the file names, game-show energy for the three rounds (leave the 3-second countdown silent before each answer), then calm and clear for the law and the checks. About 155 words per minute.',
 desc=['Contract_FINAL. Contract_FINAL2. Contract_FINAL_ACTUALLY_FINAL. 🇬🇧 Which one did you actually sign?',
  'Play spot the difference: one word or one number between versions can change the whole deal: payment terms, notice periods, liability caps. And many contracts have an <b>entire agreement clause</b>, so the <b>signed version</b> is usually what counts, not what you agreed in an email. An <b>electronic signature</b> usually counts too.',
  'Before you sign, 3 checks:<br/>1️⃣ Ask what’s changed since the last version, in writing<br/>2️⃣ Read the version you’re signing, not the one you remember<br/>3️⃣ Save the signed copy, dated, where everyone can find it',
  '👉 Keep the signed version of every contract in one place at dogetlawyer.com (link in bio)',
  '0:00 Which one did you sign? · 0:12 Spot the difference · 0:49 The entire agreement clause · 0:59 E-signatures · 1:06 3 checks · 1:22 Keeping track · 1:35 Your turn',
  '<font size="8">Source: Law Commission, “Electronic execution of documents” (2019): an electronic signature is capable in law of being used to execute a document, provided the signer intends to authenticate it and any formalities are met. General position in England &amp; Wales; outcomes turn on the facts and the contract. All names and documents shown are fictional examples. Dogetlawyer is contract management software for UK small businesses, not a substitute for legal advice.</font>'],
 tags='which version of the contract, signed contract, contract versions, final version contract, entire agreement clause, electronic signature UK, e-signature legal UK, contract changes, redline, contract management, small business UK',
 hash='#smallbusinessuk #contracts #contractmanagement #ukbusiness #esignature #businesstips', pin='Be honest: most “finals” you’ve seen on one file? 2, 3, 4 or 5+? 👇',
 kw=[('signed version / which one did you sign', 'Hook (0:04); product; title'), ('contract versions / final version', 'Hook file names; title'),
     ('spot the difference / contract changes', '0:12–0:49; alt title'), ('entire agreement clause', '0:49 scene; description'), ('electronic signature', '0:59 scene; description; tags')],
 src=['Law Commission, “Electronic execution of documents” (2019), Statement of the law, quoted verbatim with its conditions (intention to authenticate; formalities satisfied). Entire agreement clause explained in general terms, hedged as “usually”; the clause card is labelled typical wording, fictional example.',
      'Product shown holding the signed version and signing date on record (consistent with the contract register in Case 01). No claim that it detects or compares changes automatically.',
      'No statistics; no prices or offers; demo scenes labelled FICTIONAL DEMO EXAMPLE; standard fine print on the closing card.'])

def cover(story, n, cfg, bullets):
    story.append(Spacer(1, 6 * mm))
    story.append(P('DOGETLAWYER · CONTENT FOR REVIEW', S('ck', fontName='Mono', fontSize=10, textColor=SCA)))
    story.append(P(f'Case File {n}', S('ct', fontName='Head', fontSize=34, leading=40)))
    story.append(P(X(cfg['title']) + ': script, description, thumbnails and SEO', S('cs', fontSize=14, leading=19, textColor=MUT)))
    story.append(Spacer(1, 8)); story.append(P('Prepared 5 October 2026', small)); story.append(Spacer(1, 12))
    story.append(P('How this follows the brief', h2))
    for t in bullets: story.append(P('• ' + t)); story.append(Spacer(1, 3))
    story.append(P('Before posting', h2))
    for t in ['Record the voiceover (clean read on page 4) and drop it onto the silent audio track.', 'Make sure dogetlawyer.com is the link in bio.',
              'Upload the thumbnail / vertical cover and paste the title, description, tags and pinned comment.', 'Check average % viewed after 24 hours.']:
        story.append(P('□ ' + t)); story.append(Spacer(1, 3))
    story.append(P('Files', h2))
    story.append(tbl([[P('<b>Item</b>', cell), P('<b>File (repo: sobarslap/DGL_private)</b>', cell)],
      [P('Video', cell), P(cfg['file'] + ' (1:45, 1080×1920, silent track for VO)', mono)],
      [P('Thumbnails', cell), P(f'thumbnails/case-{n}_thumbnail_1280x720.png · thumbnails/case-{n}_cover_1080x1920.png', mono)]], [35 * mm, 137 * mm]))
    story.append(PageBreak())

COMMON = ['<b>Multi-colour, calm:</b> per the latest feedback, the colour changes once per section (5 changes), not every scene, on dark backgrounds, so the text stays the focus. The scene table shows the colour for each scene.',
          '<b>Language &amp; SEO:</b> conversational British English used UK-wide; researched phrases spoken and shown early and used in the title, description and tags.',
          '<b>Conversion:</b> a comment prompt with numbered answers plus “dogetlawyer.com, link in bio” with a LINK IN BIO button.',
          '<b>Compliance:</b> no prices or offers, no statistics, legal points hedged as “general position”, all names/figures fictional and labelled, standard fine print on the closing card.']
B9 = ['<b>New hook:</b> “£20,000 in sales. £600 in the bank. So why is Friday still stressful?”: a money contrast every small business owner recognises.',
      '<b>New format:</b> a cash calendar (money out vs money in), then a 4-line checklist of the contract terms that decide when you get paid.',
      '<b>New fonts:</b> Big Shoulders Display, Plus Jakarta Sans, Red Hat Mono and Newsreader italic (not used in Cases 01–08).',
      '<b>Authority:</b> two direct quotes from GOV.UK on when a business payment becomes late.'] + COMMON
B10 = ['<b>New hook:</b> “FINAL. FINAL2. FINAL_ACTUALLY_FINAL. Which one did you sign?”: the file-naming chaos everyone has seen.',
       '<b>New format:</b> an interactive spot-the-difference game: 3 rounds, a 3-second countdown, then the change is highlighted. Viewers play along, which keeps them watching.',
       '<b>New fonts:</b> Bricolage Grotesque, Outfit, Fira Code and Libre Baskerville (not used in Cases 01–09).',
       '<b>Authority:</b> a direct quote from the Law Commission on electronic signatures.'] + COMMON

for n, cfg, bl, cname in [('09', C9, B9, '£20,000 in sales. £600 in the bank'), ('10', C10, B10, 'Which final did you sign')]:
    def foot(c, doc, n=n):
        c.saveState(); c.setFont('Mono', 7); c.setFillColor(MUT)
        c.drawString(18 * mm, 10 * mm, f'Dogetlawyer · Case File {n} · internal review'); c.drawRightString(A4[0] - 18 * mm, 10 * mm, f'Page {doc.page}'); c.restoreState()
    out = R + f'deliverables/Dogetlawyer_Case-{n}_Script-Description-Thumbnails.pdf'
    doc = BaseDocTemplate(out, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm, bottomMargin=18 * mm,
                          title=f'Dogetlawyer Case File {n}: script, description, thumbnails', author='Dogetlawyer content team')
    doc.addPageTemplates([PageTemplate(id='p', frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height)], onPage=foot)])
    story = []; cover(story, n, cfg, bl); case(story, f'case-{n}', cfg); story.pop()
    doc.build(story); print('ok', out)
