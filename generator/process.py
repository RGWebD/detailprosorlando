"""Photo + logo processing for the Detail Pros Orlando demo (RGWebD).
Reads /workspace/detailpros/photos, writes assets/img/*.webp and assets/brand/*."""
from PIL import Image, ImageFilter, ImageDraw, ImageOps, ImageFont
from pathlib import Path
SRC=Path('/workspace/detailpros'); G=Path(__file__).parent; A=G/'assets'
(A/'img').mkdir(parents=True,exist_ok=True); (A/'brand').mkdir(parents=True,exist_ok=True)
# key: (crop l,t,r,b as fractions, [blur boxes as fractions])
P={
'w19':((0,0,1,1),[(.935,.15,1,.2)]),
'w18':((.25,.07,1,1),[]),
'w21':((0,0,1,1),[(.035,.66,.13,.81)]),
'w03':((0,0,1,1),[]),'w31':((0,0,1,1),[]),'w30':((0,0,1,1),[]),
'w16':((0,.14,1,1),[]),'w20':((0,0,1,1),[]),'w25':((0,0,1,1),[]),'w17':((0,0,1,1),[]),
'g02':((0,0,1,1),[]),'g04':((0,0,1,1),[]),'w29':((0,0,1,1),[]),
'w28':((0,0,1,1),[(.52,.3,.63,.5)]),'g05':((0,0,1,1),[]),
'w08':((0,0,1,1),[(.395,.37,.535,.45)]),'w09':((0,0,1,1),[]),'w10':((0,0,1,1),[(.44,.31,.72,.44)]),
'w11':((0,0,1,1),[]),'w12':((0,0,1,.8),[]),'w14':((0,0,1,1),[]),'w04':((0,0,1,1),[(.6,.33,1,.7)]),
'w23':((0,0,1,1),[]),'w24':((0,0,1,1),[]),'w22':((0,0,1,1),[]),'w26':((0,0,1,.74),[]),'w27':((0,0,1,1),[]),
'w05':((0,0,1,1),[]),'w06':((0,0,1,1),[]),'w07':((0,0,1,1),[]),'w13':((0,0,1,1),[]),'w15':((0,0,1,1),[]),
}
def blur(im,box,r=30,feather=18):
    W,H=im.size; b=(box[0]*W,box[1]*H,box[2]*W,box[3]*H)
    m=Image.new('L',im.size,0); ImageDraw.Draw(m).rounded_rectangle(b,radius=20,fill=255); m=m.filter(ImageFilter.GaussianBlur(feather))
    return Image.composite(im.filter(ImageFilter.GaussianBlur(r)),im,m)
def save(im,k,widths=(800,1600),q=80):
    for w in widths:
        x=im.copy()
        if x.width>w: x=x.resize((w,round(x.height*w/x.width)),Image.LANCZOS)
        x.save(A/'img'/f'{k}-{w}.webp',quality=q,method=6)
for k,(c,bl) in P.items():
    im=ImageOps.exif_transpose(Image.open(SRC/'photos'/f'{k}.jpg')).convert('RGB')
    for b in bl: im=blur(im,b,r=(48 if k=='w04' else 30))
    W,H=im.size; im=im.crop((round(c[0]*W),round(c[1]*H),round(c[2]*W),round(c[3]*H)))
    save(im,k)
# their van (already a cut-out PNG on their old site)
from PIL import ImageChops
van=Image.open(SRC/'photos/w32.png').convert('RGBA'); vp=van.load()
# paint out the photographer's shadow on the rear quarter panel (cream fill, keeps dark seams/badges)
m=Image.new('L',van.size,0);mp=m.load();keep=Image.new('L',van.size,0);kp=keep.load()
for y in range(255,348):
    for x in range(855,978):
        r,g,b,a=vp[x,y]; L=(r+g+b)/3
        if a>200 and b>=r-12 and 100<L<238: mp[x,y]=255
        if a>200 and L>=95: kp[x,y]=255
m=ImageChops.multiply(m.filter(ImageFilter.MaxFilter(7)),keep).filter(ImageFilter.GaussianBlur(1.2))
al=van.split()[3]; van=Image.composite(Image.new('RGBA',van.size,(247,225,192,255)),van,m); van.putalpha(al)
van=van.crop(van.getbbox())
van.save(A/'img'/'van-1000.webp',quality=86,method=6); van.resize((600,round(van.height*600/van.width)),Image.LANCZOS).save(A/'img'/'van-600.webp',quality=86,method=6)
# ---- logo: soft-key the black background (for dark backgrounds only) ----
lg=Image.open(SRC/'logo_fb.jpg').convert('RGB'); W,H=lg.size
px=lg.load(); a=Image.new('L',lg.size); ap=a.load()
for y in range(H):
    for x in range(W):
        r,g,b=px[x,y]; m=max(r,g,b); ap[x,y]=max(0,min(255,int((m-14)*255/60)))
cut=lg.convert('RGBA'); cut.putalpha(a)
# un-premultiply against black so edges don't go grey
cut=Image.merge('RGBA',[*[ch.point(lambda v:v) for ch in cut.split()[:3]],a])
cut.save(A/'brand'/'logo-cut-1167.png')
for s in (720,360,160): cut.resize((s,s),Image.LANCZOS).save(A/'brand'/f'logo-{s}.webp',quality=92)
cut.resize((512,512),Image.LANCZOS).save(A/'brand'/'logo-512.png')
# badge on black disc (works on any background): disc slightly larger, chrome ring
S=1300; bd=Image.new('RGBA',(S,S),(0,0,0,0)); d=ImageDraw.Draw(bd)
d.ellipse((0,0,S-1,S-1),fill=(205,212,222,255)); d.ellipse((14,14,S-15,S-15),fill=(6,8,11,255))
bd.alpha_composite(lg.convert('RGBA').resize((1150,1150),Image.LANCZOS),(75,75))
m=Image.new('L',(S*2,S*2),0); ImageDraw.Draw(m).ellipse((28,28,S*2-29,S*2-29),fill=255); m=m.resize((S,S),Image.LANCZOS)
inner=Image.new('L',(S,S),0); ImageDraw.Draw(inner).ellipse((14,14,S-15,S-15),fill=255)
ring=Image.new('RGBA',(S,S),(205,212,222,255)); ring.alpha_composite(Image.composite(bd,Image.new('RGBA',(S,S),(6,8,11,255)),inner))
ring.putalpha(Image.composite(Image.new('L',(S,S),255),Image.new('L',(S,S),0),m))
for s in (640,256): ring.resize((s,s),Image.LANCZOS).save(A/'brand'/f'badge-{s}.webp',quality=92)
ring.resize((1024,1024),Image.LANCZOS).save(A/'brand'/'badge-1024.png')
# ---- favicon: bold "DP" + gold drop on gloss black, cyan ring (32px legible) ----
def fav(s):
    k=8; im=Image.new('RGBA',(s*k,s*k),(0,0,0,0)); d=ImageDraw.Draw(im); S2=s*k
    d.rounded_rectangle((0,0,S2-1,S2-1),radius=int(S2*.24),fill=(7,9,13,255))
    d.rounded_rectangle((S2*.05,S2*.05,S2*.95,S2*.95),radius=int(S2*.2),outline=(25,211,255,255),width=max(2,int(S2*.06)))
    f=ImageFont.truetype(str(G/'fonts/Unbounded.ttf'),int(S2*.46)); f.set_variation_by_axes([900])
    t='DP'; bb=d.textbbox((0,0),t,font=f); tw=bb[2]-bb[0]; th=bb[3]-bb[1]
    d.text(((S2-tw)/2-bb[0],(S2-th)/2-bb[1]-S2*.04),t,font=f,fill=(240,246,250,255))
    # gold drop under letters
    cx,cy,r=S2*.5,S2*.78,S2*.065
    d.ellipse((cx-r,cy-r,cx+r,cy+r),fill=(245,197,24,255)); d.polygon([(cx-r*.9,cy-r*.35),(cx+r*.9,cy-r*.35),(cx,cy-r*2.2)],fill=(245,197,24,255))
    return im.resize((s,s),Image.LANCZOS)
for s in (16,32,48,180,192,512): fav(s).save(A/'brand'/f'fav-{s}.png')
fav(256).save(A/'brand'/'favicon.ico',sizes=[(16,16),(32,32),(48,48)])
print('ok')
