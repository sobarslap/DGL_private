"""Shared multi-colour scene palettes (boss: slide 1 purple+black, slide 2 grey+red, slide 3 sky blue, others)."""
import numpy as np
from PIL import Image, ImageDraw
def hexc(h): h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))
def mix(a,b,t): return tuple(int(round(x+(y-x)*t)) for x,y in zip(a,b))
SPEC=[ # name, c1 (top-left), c2 (bottom-right), text, accent, ok-green
 ("Purple & black", "#5A2A8C","#0A0A0F","#FFFFFF","#D9B8FF","#7CE3A8"),
 ("Grey & red",     "#55595F","#A3172B","#FFFFFF","#FFE08A","#9BF0C0"),
 ("Sky blue",       "#B4E3FC","#5BB6EA","#0A2342","#B0123A","#0B6B3A"),
 ("Emerald & navy", "#0E5E57","#0B1D33","#F6F1E7","#FFC857","#8BE3B0"),
 ("Charcoal & orange","#2B2B30","#C4561A","#FFFFFF","#FFD08A","#9BF0C0"),
 ("Pink & plum",    "#FFDCEB","#F4A9C9","#3A0B3F","#A0115E","#0B6B3A"),
 ("Navy & gold",    "#1E2E5E","#0B1226","#FFFFFF","#F7B32B","#8BE3B0"),
 ("Mint & forest",  "#DDF5E8","#9ED9BB","#0E2E22","#B0123A","#0B6B3A"),
]
def theme(name,c1,c2,fg,acc,ok):
    c1,c2,fg,acc,ok=map(hexc,(c1,c2,fg,acc,ok)); bg=mix(c1,c2,0.5)
    return dict(name=name,g1=c1,g2=c2,bg=bg,fg=fg,acc=acc,ok=ok,mut=mix(bg,fg,0.70),dim=mix(bg,fg,0.52),
                line=mix(bg,fg,0.16),panel=mix(bg,fg,0.10),edge=mix(bg,fg,0.26),light=sum(bg)>380)
THEMES=[theme(*s) for s in SPEC]
def gradient(T,W,H):
    y,x=np.mgrid[0:H,0:W].astype(np.float32); t=np.clip((x/W)*0.35+(y/H)*0.65,0,1)[...,None]
    a=np.array(T["g1"],np.float32); b=np.array(T["g2"],np.float32)
    return Image.fromarray((a+(b-a)*t).astype(np.uint8))
