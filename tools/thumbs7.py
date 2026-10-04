import sys; sys.path.insert(0,'/tmp/claude-0/-home-user-DGL-private/f3f04cd2-c6be-58d9-99ed-c95e44436400/scratchpad')
from PIL import Image, ImageDraw, ImageFont
from multitheme import THEMES, gradient, hexc
import numpy as np
B='/tmp/claude-0/-home-user-DGL-private/f3f04cd2-c6be-58d9-99ed-c95e44436400/scratchpad/c7/f/'; O='/home/user/DGL_private/thumbnails/'
F=lambda n,s: ImageFont.truetype(B+n+'.ttf',s)
def grain(im):
    a=np.asarray(im).astype(np.float32); a+=np.random.default_rng(3).normal(0,6,a.shape[:2])[...,None]; return Image.fromarray(a.clip(0,255).astype(np.uint8))
def email(w,fs,ang):
    w=int(max(F('Manrope_800ExtraBold',fs).getlength('Important: changes to our'),F('Manrope_600SemiBold',int(fs*0.8)).getlength('Continued use means you accept'))+70)
    h=int(fs*7.6); im=Image.new('RGBA',(w,h),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.rounded_rectangle([0,0,w-1,h-1],radius=20,fill=(251,250,247,255))
    d.text((30,24),"From: Your supplier",font=F('SpaceMono_400Regular',int(fs*0.6)),fill=(110,110,110,255))
    d.text((30,24+fs),"Important: changes to our",font=F('Manrope_800ExtraBold',fs),fill=(26,26,26,255))
    d.text((30,24+fs*2.2),"terms and conditions",font=F('Manrope_800ExtraBold',fs),fill=(26,26,26,255))
    y=int(24+fs*3.9); s="Continued use means you accept"
    tw=F('Manrope_600SemiBold',int(fs*0.8)).getlength(s); d.rectangle([24,y-4,40+tw,y+int(fs*1.05)],fill=(255,224,138,255))
    d.text((30,y),s,font=F('Manrope_600SemiBold',int(fs*0.8)),fill=(26,26,26,255))
    d.text((30,y+int(fs*1.25)),"the new terms.",font=F('Manrope_600SemiBold',int(fs*0.8)),fill=(26,26,26,255))
    return im.rotate(ang,expand=True,resample=Image.BICUBIC)
def make(W,H,vert):
    im=gradient(THEMES[0],W,H); d=ImageDraw.Draw(im)
    red=gradient(THEMES[1],W,H)
    if not vert:
        im.paste(red.crop((int(W*0.62),0,W,H)),(int(W*0.62),0)); d=ImageDraw.Draw(im)
        d.text((56,50),"“WE’RE UPDATING",font=F('Oswald_700Bold',96),fill=(255,255,255))
        d.text((56,170),"OUR TERMS”",font=F('Oswald_700Bold',96),fill=(255,255,255))
        d.text((56,330),"= PRICES",font=F('Oswald_700Bold',120),fill=hexc('#D9B8FF'))
        d.text((56,480),"UP 18%?",font=F('Oswald_700Bold',120),fill=hexc('#FFE08A'))
        e=email(0,30,6); im.paste(e,(W-e.width-14,170),e)
        d.text((W-260,H-70),"DON’T ARCHIVE IT",font=F('SpaceMono_700Bold',28),fill=(255,255,255),anchor="mm")
    else:
        im.paste(red.crop((0,int(H*0.55),W,H)),(0,int(H*0.55))); d=ImageDraw.Draw(im)
        d.text((70,170),"“WE’RE UPDATING",font=F('Oswald_700Bold',118),fill=(255,255,255))
        d.text((70,320),"OUR TERMS”",font=F('Oswald_700Bold',118),fill=(255,255,255))
        d.text((70,520),"= PRICES",font=F('Oswald_700Bold',170),fill=hexc('#D9B8FF'))
        d.text((70,730),"UP 18%?",font=F('Oswald_700Bold',170),fill=hexc('#FFE08A'))
        e=email(820,46,-4); im.paste(e,((W-e.width)//2,1130),e)
        d.text((540,1780),"DON’T ARCHIVE IT",font=F('SpaceMono_700Bold',44),fill=(255,255,255),anchor="mm")
    return grain(im)
make(1280,720,False).save(O+'case-07_thumbnail_1280x720.png'); make(1080,1920,True).save(O+'case-07_cover_1080x1920.png'); print('ok')
