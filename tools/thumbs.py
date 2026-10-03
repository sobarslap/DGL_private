from PIL import Image, ImageDraw, ImageFont
import numpy as np
B='/tmp/claude-0/-home-user-DGL-private/f3f04cd2-c6be-58d9-99ed-c95e44436400/scratchpad/'
O='/home/user/DGL_private/thumbnails/'
def F(p,s): return ImageFont.truetype(B+p+'.ttf',s)
def hx(h): return tuple(int(h[i:i+2],16) for i in (1,3,5))
def fit(fp, s, maxw, size):
    f=F(fp,size)
    while f.getlength(s)>maxw and size>20: size-=4; f=F(fp,size)
    return f
def grain(im, amt=7):
    a=np.asarray(im).astype(np.float32); a+=np.random.default_rng(1).normal(0,amt,a.shape[:2])[...,None]
    return Image.fromarray(a.clip(0,255).astype(np.uint8))
def card(w,h,lines,fill,ink,hl=None,font=None,label=None,lab_col=None,ang=-4,boxcol=None):
    im=Image.new('RGBA',(w,h),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.rounded_rectangle([0,0,w-1,h-1],radius=18,fill=fill+(255,))
    y=36
    while max(font.getlength(l) for l in lines)>w-90: font=ImageFont.truetype(font.path,font.size-2)
    if label:
        d.text((36,y),label,font=F('c6/f/IBMPlexMono_700Bold',26),fill=lab_col+(255,)); y+=62
    if boxcol: d.rectangle([24,y-14,w-24,y+len(lines)*58+14],outline=boxcol+(255,),width=5)
    for ln in lines:
        if hl:
            tw=font.getlength(ln); d.rectangle([30,y-4,40+tw,y+52],fill=hl+(255,))
        d.text((36,y),ln,font=font,fill=ink+(255,)); y+=58
    return im.rotate(ang,expand=True,resample=Image.BICUBIC)

# ---------------- Case 05
PLUM,BLUSH,ROSE,YEL,INK=hx('#241528'),hx('#F0E4E8'),hx('#E86A8A'),hx('#F2D04B'),hx('#1A1014')
def c5(W,H,vert=False):
    im=Image.new('RGB',(W,H),PLUM); d=ImageDraw.Draw(im)
    for x in range(0,W,96): d.line([(x,0),(x,H)],fill=(44,28,48))
    A='c5/f/Anton_400Regular'
    if not vert:
        d.text((60,46),"LIMITATION OF LIABILITY CLAUSE",font=F('c5/f/JetBrainsMono_700Bold',30),fill=ROSE)
        d.text((56,96),"THIS ONE LINE",font=F(A,120),fill=BLUSH)
        d.text((56,236),"COST A FIRM",font=F(A,120),fill=BLUSH)
        d.text((52,370),"£54,500",font=F(A,230),fill=ROSE)
        c=card(560,320,["“Our total liability","shall not exceed","£3,900.”"],(244,239,230),INK,hl=YEL,font=F('c5/f/Inter_600SemiBold',40),label="SUPPLIER T&Cs · CLAUSE 11.3",lab_col=(120,100,110),ang=-6)
        im.paste(c,(W-c.width-30,110),c)
        d.rounded_rectangle([W-470,H-118,W-50,H-46],radius=36,fill=ROSE)
        d.text((W-260,H-82),"4 MYTHS BUSTED",font=F(A,46),fill=PLUM,anchor="mm")
    else:
        d.text((70,180),"LIMITATION OF LIABILITY CLAUSE",font=F('c5/f/JetBrainsMono_700Bold',34),fill=ROSE)
        for i,t in enumerate(["THIS ONE","LINE COST","A FIRM"]): d.text((64,250+i*190),t,font=F(A,190),fill=BLUSH)
        d.text((60,820),"£54,500",font=F(A,300),fill=ROSE)
        c=card(800,280,["“Our total liability shall","not exceed £3,900.”"],(244,239,230),INK,hl=YEL,font=F('c5/f/Inter_600SemiBold',44),label="SUPPLIER T&Cs · CLAUSE 11.3",lab_col=(120,100,110),ang=-5)
        im.paste(c,((W-c.width)//2,1240),c)
        d.rounded_rectangle([200,1640,880,1740],radius=50,fill=ROSE)
        d.text((540,1690),"4 MYTHS BUSTED",font=F(A,64),fill=PLUM,anchor="mm")
    return grain(im)
c5(1280,720).save(O+'case-05_thumbnail_1280x720.png'); c5(1080,1920,True).save(O+'case-05_cover_1080x1920.png')

# ---------------- Case 06
BLK,IVO,SCA=hx('#121213'),hx('#F4EFE6'),hx('#E0313F')
def c6(W,H,vert=False):
    im=Image.new('RGB',(W,H),BLK); d=ImageDraw.Draw(im)
    for yy in range(0,H,28):
        for xx in range(0,W,28):
            k=max(0,(xx/W)*0.6+(yy/H)*0.8-0.55); r=1+5*k
            if k>0: d.ellipse([xx-r,yy-r,xx+r,yy+r],fill=(52,22,26))
    d.rectangle([0,0,14,H],fill=SCA)
    A='c6/f/ArchivoBlack_400Regular'
    form=lambda w,fs: card(w,int(fs*8.4),["I personally guarantee","all sums due from","the company."],IVO,(20,20,20),font=F('c6/f/SpaceGrotesk_500Medium',fs),label="PERSONAL GUARANTEE",lab_col=SCA,ang=5,boxcol=SCA)
    if not vert:
        d.text((60,60),"LTD COMPANY",font=F(A,84),fill=IVO)
        d.text((60,165),"DIRECTOR?",font=F(A,84),fill=IVO)
        d.text((60,320),"YOUR HOUSE",font=F(A,92),fill=SCA)
        d.text((60,432),"COULD BE",font=F(A,92),fill=SCA)
        d.text((60,544),"AT RISK.",font=F(A,92),fill=SCA)
        c=form(440,34); im.paste(c,(W-c.width-30,150),c)
        d.text((W-280,H-70),"CHECK PAGE 4 →",font=F('c6/f/IBMPlexMono_700Bold',30),fill=IVO,anchor="mm")
    else:
        d.text((80,200),"LTD COMPANY",font=F(A,120),fill=IVO)
        d.text((80,340),"DIRECTOR?",font=F(A,120),fill=IVO)
        for i,t in enumerate(["YOUR HOUSE","COULD BE","AT RISK."]): d.text((80,560+i*150),t,font=F(A,130),fill=SCA)
        c=form(760,52); im.paste(c,((W-c.width)//2,1080),c)
        d.text((540,1760),"CHECK BEFORE YOU SIGN",font=F('c6/f/IBMPlexMono_700Bold',40),fill=IVO,anchor="mm")
    return grain(im)
c6(1280,720).save(O+'case-06_thumbnail_1280x720.png'); c6(1080,1920,True).save(O+'case-06_cover_1080x1920.png')
print('ok')
