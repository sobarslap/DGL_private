import sys; sys.path.insert(0,'/tmp/claude-0/-home-user-DGL-private/f3f04cd2-c6be-58d9-99ed-c95e44436400/scratchpad/c8')
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import render8b as r  # v2: calmer section colours (hook = deep blue & magenta)
F=lambda n,s: ImageFont.truetype(r.FD+'/'+n+'.ttf',s); O='/home/user/DGL_private/thumbnails/'
def grain(im):
    a=np.asarray(im).astype(np.float32); a+=np.random.default_rng(4).normal(0,6,a.shape[:2])[...,None]; return Image.fromarray(a.clip(0,255).astype(np.uint8))
def logo_card(w,ang):
    h=int(w*0.72); im=Image.new('RGBA',(w,h),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.rounded_rectangle([0,0,w-1,h-1],radius=24,fill=(251,250,247,255))
    cx,cy=w//2,int(h*0.40); R=int(h*0.2)
    d.ellipse([cx-R,cy-R,cx+R,cy+R],fill=(36,51,224,255)); d.text((cx,cy),"YOUR\nLOGO",font=F('BebasNeue_400Regular',int(R*0.62)),fill=(255,255,255,255),anchor="mm",align="center")
    d.text((cx,int(h*0.78)),"© THE DESIGNER",font=F('DMSans_800ExtraBold',int(h*0.11)),fill=(209,15,112,255),anchor="mm")
    return im.rotate(ang,expand=True,resample=Image.BICUBIC)
def make(W,H,vert):
    im=r.gradient(r.THEMES[0],W,H); d=ImageDraw.Draw(im); Y=(255,225,77); WH=(255,255,255)
    if not vert:
        d.text((56,40),"YOU PAID £800",font=F('BebasNeue_400Regular',150),fill=WH)
        d.text((56,190),"FOR YOUR LOGO.",font=F('BebasNeue_400Regular',150),fill=WH)
        d.text((56,380),"DO YOU OWN IT?",font=F('BebasNeue_400Regular',190),fill=Y)
        c=logo_card(400,6); im.paste(c,(W-c.width-30,40),c)
        d.text((60,640),"COPYRIGHT · UK SMALL BUSINESS",font=F('DMMono_500Medium',30),fill=WH)
    else:
        for i,t in enumerate(["YOU PAID","£800 FOR","YOUR LOGO."]): d.text((70,150+i*190),t,font=F('BebasNeue_400Regular',220),fill=WH)
        d.text((70,760),"DO YOU",font=F('BebasNeue_400Regular',250),fill=Y); d.text((70,990),"OWN IT?",font=F('BebasNeue_400Regular',250),fill=Y)
        c=logo_card(700,-5); im.paste(c,((W-c.width)//2,1290),c)
    return grain(im)
make(1280,720,False).save(O+'case-08_thumbnail_1280x720.png'); make(1080,1920,True).save(O+'case-08_cover_1080x1920.png'); print('ok')
