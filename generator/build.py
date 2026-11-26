#!/usr/bin/env python3
"""Generator for the Detail Pros Orlando Inc. redesign demo (RGWebD).
Facts: /workspace/detailpros/notes.md (old site detailprosorlando.com, Facebook page, Google Business Profile).
Run: python3 process.py (once) && python3 build.py  -> writes ../detailpros-site"""
import json, shutil, html
from pathlib import Path
from PIL import Image
GEN=Path(__file__).parent; OUT=Path('/workspace/detailpros-site')
REPO='detailprosorlando'; BASE=f'https://rgwebd.github.io/{REPO}/'
NAME='Detail Pros Orlando Inc.'
PHONE='407-456-0031'; TEL='tel:+14074560031'; EMAIL='detailprosorlandoinc@gmail.com'
SMS_BODY="Hi Detail Pros! I'd like to book a mobile detail. Vehicle: "
SMS='sms:+14074560031?&body='+SMS_BODY.replace(' ','%20').replace("'",'%27').replace('!','%21').replace(':','%3A')
FB='https://www.facebook.com/p/Detail-Pros-Orlando-Inc-100091688833386/'
GMAPS='https://www.google.com/maps/place/?q=place_id:ChIJybDPJlnRWkIROPiOTczLTPM'
OLD='https://detailprosorlando.com/'
e=html.escape

# ---------------- assets ----------------
OUT.mkdir(parents=True,exist_ok=True)
for p in OUT.iterdir():
    if p.name in ('.git',): continue
    shutil.rmtree(p) if p.is_dir() else p.unlink()
A=OUT/'assets'; shutil.copytree(GEN/'assets'/'img',A/'img'); (A/'brand').mkdir()
for f in ['logo-720.webp','logo-360.webp','logo-160.webp','badge-640.webp','badge-256.webp','logo-512.png','fav-32.png','fav-16.png','fav-192.png','fav-512.png']: shutil.copy(GEN/'assets/brand'/f,A/'brand'/f)
shutil.copy(GEN/'assets/brand/favicon.ico',OUT/'favicon.ico'); shutil.copy(GEN/'assets/brand/fav-180.png',OUT/'apple-touch-icon.png')
shutil.copy(GEN/'src/styles.css',A/'styles.css'); shutil.copy(GEN/'src/script.js',A/'script.js')
G=OUT/'generator'; G.mkdir(); (G/'src').mkdir()
for f in ['build.py','process.py','qa.py','shots.py','README.md']:
    if (GEN/f).exists(): shutil.copy(GEN/f,G/f)
for f in ['styles.css','script.js']: shutil.copy(GEN/'src'/f,G/'src'/f)
# OG image: hero photo + logo
og=Image.open(GEN/'assets/img/w19-1600.webp').convert('RGB').resize((1200,900)).crop((0,150,1200,780))
dk=Image.new('RGB',og.size,(5,7,10)); m=Image.linear_gradient('L').rotate(90).resize(og.size)
og=Image.composite(og,dk,m.point(lambda v:int(40+v*.75)))
lg=Image.open(GEN/'assets/brand/logo-cut-1167.png').convert('RGBA').resize((440,440),Image.LANCZOS)
og=og.convert('RGBA'); og.alpha_composite(lg,(50,95)); og.convert('RGB').save(A/'og-image.jpg',quality=86)

def dims(n,w=1600): return Image.open(A/'img'/f'{n}-{w}.webp').size
def pic(n,alt=None,cls='',sizes='(max-width:1000px) 100vw, 50vw',eager=False,attrs=''):
    alt=PH[n] if alt is None else alt
    w,h=dims(n); w8,_=dims(n,800)
    ld='fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<img src="assets/img/{n}-1600.webp" srcset="assets/img/{n}-800.webp {w8}w, assets/img/{n}-1600.webp {w}w" sizes="{sizes}" '
            f'width="{w}" height="{h}" alt="{e(alt)}" {ld} decoding="async"{(" class=\""+cls+"\"") if cls else ""} {attrs}>')

PH={ # every photo checked by eye; plates / registration numbers / house number blurred in process.py
'w19':'Black Ford F-250 with mirror-gloss paint reflecting the trees, the Detail Pros mobile setup parked behind it',
'w18':'Black Mercedes-Benz convertible gleaming on a paver driveway','w21':'Black Ford F-250 Platinum with deep gloss on the hood and doors',
'w03':'Black Audi SUV side profile with the street mirrored in its doors','w31':'Black Audi A8 sedan freshly detailed',
'w30':'Close-up of a black Audi’s glossy doors and polished trim','w16':'Red Corvette coupe with polished paint and chrome wheels',
'w20':'Black Corvette with gloss black wheels and red brake calipers','w25':'Red Alfa Romeo Giulia shining on a brick driveway',
'w17':'Red Ford F-150 FX4 bed and tail light after a detail','g02':'Blue Ford Super Duty front fender wet with fresh wash water',
'g04':'Tan Hyundai Santa Cruz pickup with dressed tires','w29':'Grey Tesla Model 3 side panels after a hand wash',
'w28':'Grey Tesla Model 3 with hoses and detailing gear on the driveway','g05':'Close-up of deep red paint and a polished body line',
'w08':'Blue and black Yamaha wake boat on its trailer after a detail','w09':'Yamaha outboard motor cleaned and polished',
'w10':'Center-console boat with a polished hull on its trailer','w11':'White deck boat hull polished on the trailer',
'w12':'Clean white boat deck, seating and helm','w14':'Center-console fishing boat with a glossy black and white hull',
'w04':'Close-up of a polished white boat hull and chrome rub rail','w23':'Black Entegra luxury motorhome with a mirror finish',
'w24':'Copper and black swoosh graphics on a motorhome, freshly polished','w22':'Ladders set up beside a luxury motorhome during a detail',
'w26':'Blue and black Accolade motorhome after a detail','w27':'Super C motorhome with a clean grey cab',
'w05':'Champagne cruiser motorcycle with polished chrome','w06':'Candy red Harley-Davidson touring bike after a detail',
'w07':'Kawasaki sport bike with a mirror-chrome tank','w13':'Blue Harley-Davidson with polished chrome exhaust and engine',
'w15':'Purple Honda cruiser with chrome pipes',
}
CAT={'auto':['w19','w18','w21','w03','w31','w30','w16','w20','w25','w17','g02','g04','w29','w28','g05'],
     'boat':['w08','w09','w10','w11','w12','w14','w04'],'rv':['w23','w24','w22','w26','w27'],'moto':['w06','w05','w07','w13','w15']}

IC={
'phone':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>',
'chat':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12a8 8 0 0 1-11.8 7L3 21l2-6.2A8 8 0 1 1 21 12z"/></svg>',
'mail':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>',
'arrow':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
'left':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M15 6l-6 6 6 6"/></svg>',
'right':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg>',
'x':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>',
'cal':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="17" rx="2"/><path d="M3 9h18M8 2v4M16 2v4"/></svg>',
'g':'<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#4285F4" d="M22.5 12.3c0-.8-.1-1.5-.2-2.2H12v4.2h5.9a5 5 0 0 1-2.2 3.3v2.7h3.5c2.1-1.9 3.3-4.7 3.3-8z"/><path fill="#34A853" d="M12 23c3 0 5.5-1 7.3-2.7l-3.5-2.7c-1 .7-2.3 1.1-3.8 1.1-2.9 0-5.4-2-6.3-4.7H2.1v2.8A11 11 0 0 0 12 23z"/><path fill="#FBBC05" d="M5.7 14a6.6 6.6 0 0 1 0-4.2V7H2.1a11 11 0 0 0 0 9.9z"/><path fill="#EA4335" d="M12 5.4c1.6 0 3.1.6 4.3 1.7l3.1-3.1A11 11 0 0 0 2.1 7l3.6 2.8C6.6 7.3 9.1 5.4 12 5.4z"/></svg>',
'fb':'<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#1877F2" d="M24 12a12 12 0 1 0-13.9 11.9v-8.4H7.1V12h3V9.4c0-3 1.8-4.7 4.5-4.7 1.3 0 2.7.2 2.7.2v3h-1.5c-1.5 0-2 .9-2 1.9V12h3.4l-.5 3.5h-2.9v8.4A12 12 0 0 0 24 12z"/></svg>',
'web':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/></svg>',
}
def btn_call(cls='pri',lbl=None): return f'<a class="btn mag {cls}" href="{TEL}">{IC["phone"]}<span>{lbl or "Call "+PHONE}</span></a>'
def btn_text(cls='gh',lbl='Text to book'): return f'<a class="btn mag {cls}" href="{SMS}">{IC["chat"]}<span>{lbl}</span></a>'
def stars(r): return f'<span class="stars5" role="img" aria-label="{r} out of 5 stars"><i style="--w:{r/5*100:.1f}%"></i></span>'

# ---------------- reviews (word for word) ----------------
GREV=[('Charlotte Weinreich','a week ago','super honest and good workers. I was worried about damage to a usb port in my vehicle after their service and they were willing to fix it for me. It\'s very rare to find a company with integrity like that. The pricing was very affordable for the service too and they were pretty quick.'),
      ('Amanda','a month ago','Arrived on time. I did have an issue, but they made it right! :)')]
OREV=[('Sophia Akel','They did a fantastic job on my boyfriend’s F-250. It was filthy inside and out, with mud caked everywhere. The truck looked and smelled brand new when they finished! SO impressed by their work and they are super communicative and personable as well. We’ve already booked them to detail my SUV as well. Highly recommend their services to anyone looking for a well-priced, reliable, and talented detailer.'),
      ('Ben Mayo','These guys do great work right in your driveway. They did my boat and truck better than any of the places I’ve taken vehicles before.'),
      ('Cheina Ramos','I had an amazing experience with this cleaning service! My little brother had thrown up in my car, and I was understandably stressed about getting it cleaned up. I called them, and they came the very next day. They were incredibly fast, efficient, and paid great attention to detail. Every trace of the mess was gone, and my car looked spotless again. I couldn\'t be more impressed with their service, and I’ll definitely be recommending them to others!'),
      ('mwmagin','They came right to me and did an excellent job. Quick, attention to detail, and fairly priced.'),
      ('Elizabeth Gross','They did a great job on my interior, it was dirty. It looks brand new. Very affordable and professional. Very satisfied'),
      ('Carmen Treffiletti','The crew was amazing! Cars were spotless and looked brand new.'),
      ('Darnell Lindsey','Great customer service and great detailed. Would highly recommend.'),
      ('Lisa P','Akeem is amazing and keeps my Genesis looking good!'),
      ('Uday Desai','Good service and great people')]
FBC=('Laurie Boston Shackelford','about a year ago','Cameron did a FANTASTIC job on our Jeep!!! We will definitely use him again for summer detailing.')

# ---------------- prices (current published menu on detailprosorlando.com) ----------------
SIZES=[('Coupes & light trucks','coupe'),('Sedans','sedan'),('2-door trucks & small SUVs','suv'),('Full-size SUVs & large trucks','truck')]
SIG=['169.95','179.95','189.95','219.95']; ULT=['199.95','219.95','239.95','279.95']
INC_INT=['Interior vacuumed, personal items bagged','Mats and seats steam cleaned & extracted','Carpets shampooed','Door panels, steering wheel & shifter','Visors, windows & headliner','Leather / vinyl cleaned & conditioned','Steam disinfect & sanitize','Trunk, dash, console & instrument panel']
INC_SIG=['Hand wash','Liquid carnauba wax','Tires, wheels & wheel wells','Interior vacuumed, trunk included','Dash, console & cup holders','Carpet, seats, mats & upholstery steam cleaned','Interior sanitizing','Trim conditioned','Bug & tar removal','Wheels & chrome polished','Door jambs & gas compartment','Exhaust tips','Air freshener']
INC_ULT=['Hand wash with pH-balanced soap','Clay bar & paint decontamination','Carnauba wax (ceramic wax +$30)','Hand dried','Wheels & chrome polished','Interior vacuum','Carpet, seats, mats & upholstery steam cleaned','Interior sanitized','Leather cleaned & conditioned','Wheel wells & trim conditioned','Bug & tar removal','Windows','Gas compartment','Trunk / cargo vacuumed','Rims & tires dressed','Door & trunk jambs','Exhaust tips polished','Air freshener']
ADD=[('Rain-X treatment','16'),('Child stroller cleaning','25'),('Pet hair removal','30'),('Interior sanitizing','30'),('Ceramic wax','30'),('Headlight restoration','69')]

SVCS=[ # (id, title, verbatim line from their site, extras)
('auto','Auto detailing','high speed buffing, polishing and waxing, light scratch removal.',['Hand wash & clay bar','Three-step paint process','Scratch removal','Headlight restoration','Steam-cleaned interiors','Pet hair & sanitizing']),
('boat','Boat detailing','high speed buffing, polishing, waxing engine cleaning, and vinyl cleaning.',['Hull buffing & polishing','Wax','Engine cleaning','Vinyl cleaning']),
('rv','RV detailing','Keep your RV, Mobile Home, 5th Wheel and Travel Trailer looking fantastic.',['Motorhomes','5th wheels','Travel trailers','Mobile homes']),
('moto','Motorcycle detailing','experience in detailing Harley\'s, Victory, Sport Bikes, and customs bikes.',['Harley-Davidson','Victory','Sport bikes','Custom bikes']),
]
CITIES=['Orlando','Lake Nona','Winter Park','Windermere','Celebration','Kissimmee','Saint Cloud','Altamonte Springs','Lake Mary','Sanford']

# ---------------- schema ----------------
BID=BASE+'#business'
def biz(full=True):
    b={"@context":"https://schema.org","@type":"AutoWash","@id":BID,"name":NAME,"url":BASE,
       "description":"Mobile auto, boat, RV and motorcycle detailing that comes to your home or office in the Orlando area, seven days a week.",
       "telephone":"+1-407-456-0031","email":EMAIL,"logo":BASE+"assets/brand/logo-512.png","image":[BASE+"assets/og-image.jpg",BASE+"assets/img/w19-1600.webp"],
       "address":{"@type":"PostalAddress","addressLocality":"Orlando","addressRegion":"FL","addressCountry":"US"},
       "areaServed":[{"@type":"AdministrativeArea","name":f"{c} County, FL"} for c in ['Orange','Seminole','Lake','Osceola']]+[{"@type":"City","name":c+", FL"} for c in CITIES],
       "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],"opens":"08:00","closes":"20:00"}],
       "sameAs":[FB,GMAPS],"knowsLanguage":["en","es"],"paymentAccepted":"Credit card, debit card, NFC mobile payments",
       "foundingDate":"2004","founder":{"@type":"Person","name":"Thomas Kerney","jobTitle":"Founder and President"},
       "priceRange":"$16–$279.95"}
    if full:
        b["aggregateRating"]={"@type":"AggregateRating","ratingValue":"5.0","reviewCount":"2","bestRating":"5"}
        b["review"]=[{"@type":"Review","author":{"@type":"Person","name":n},"reviewRating":{"@type":"Rating","ratingValue":"5","bestRating":"5"},"reviewBody":t,"publisher":{"@type":"Organization","name":"Google"}} for n,a,t in GREV]
        b["hasOfferCatalog"]={"@type":"OfferCatalog","name":"Detailing services","itemListElement":[{"@type":"Offer","itemOffered":{"@type":"Service","name":s[1]}} for s in SVCS]}
    return b
def crumbs_ld(name,file): return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":BASE},{"@type":"ListItem","position":2,"name":name,"item":BASE+file}]}
def ld(*objs): return ''.join(f'<script type="application/ld+json">{json.dumps(o,ensure_ascii=False)}</script>' for o in objs)

NAV=[('index.html','Home'),('services.html','Services'),('pricing.html','Pricing'),('gallery.html','Gallery'),('reviews.html','Reviews'),('about.html','About'),('contact.html','Contact')]
FONTS='<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Unbounded:wght@600;700;800;900&family=Yellowtail&display=swap" rel="stylesheet">'

def head(file,title,desc,img='assets/og-image.jpg',extra=''):
    url=BASE+('' if file=='index.html' else file)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{url}">
<meta name="theme-color" content="#05070a"><meta property="og:type" content="website"><meta property="og:site_name" content="{NAME}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}{img}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}"><meta name="twitter:image" content="{BASE}{img}">
<link rel="icon" href="favicon.ico" sizes="any"><link rel="icon" type="image/png" sizes="32x32" href="assets/brand/fav-32.png"><link rel="apple-touch-icon" href="apple-touch-icon.png">
{FONTS}<link rel="stylesheet" href="assets/styles.css">{extra}</head>'''

def header(cur):
    links=''.join(f'<a href="{f}"{" aria-current=page" if f==cur else ""}>{n}</a>' for f,n in NAV)
    mlinks=''.join(f'<a class="ml" href="{f}"{" aria-current=page" if f==cur else ""}>{n}</a>' for f,n in NAV)
    return f'''<a class="skip" href="#main">Skip to content</a><div class="prog" aria-hidden="true"></div>
<header class="hdr"><div class="hdr-in"><a class="brand" href="index.html" aria-label="{NAME} home"><img src="assets/brand/logo-160.webp" width="160" height="160" alt="Detail Pros Orlando Inc. emblem"><span><b>DETAIL PROS</b><i>Orlando</i></span></a>
<nav class="nav" aria-label="Main">{links}</nav><div class="ctas"><a class="btn sm gh" href="{TEL}">{IC["phone"]}<span>{PHONE}</span></a><a class="btn sm pri" href="contact.html#quote">{IC["cal"]}<span>Book</span></a></div>
<button class="burger" aria-label="Menu" aria-expanded="false" aria-controls="mnav"><span></span><span></span><span></span></button></div></header>
<div class="mnav" id="mnav">{mlinks}<div class="ctas">{btn_call()}{btn_text()}</div></div>'''

def footer():
    links=''.join(f'<li><a href="{f}">{n}</a></li>' for f,n in NAV)
    return f'''<footer class="ft"><div class="hex" aria-hidden="true"></div><div class="wrap"><div class="ft-g">
<div><img class="lg" src="assets/brand/logo-360.webp" width="360" height="360" alt="Detail Pros Orlando Inc. logo" loading="lazy"><p><b>{NAME}</b><br>Mobile auto, boat, RV &amp; motorcycle detailing. We come to your home or office, seven days a week.</p></div>
<div><h4>Pages</h4><ul>{links}</ul></div>
<div><h4>Service area</h4><p>Orange, Seminole, Lake &amp; Osceola counties, Florida. Mobile service, no shop visit needed.</p><p>English &amp; Español</p></div>
<div><h4>Contact</h4><ul><li><a href="{TEL}">{PHONE}</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li>Open 7 days · 8 AM–8 PM</li><li>By appointment</li><li><a href="{FB}" rel="noopener" target="_blank">Facebook</a> · <a href="{GMAPS}" rel="noopener" target="_blank">Google</a></li></ul></div>
</div><div class="ft-b"><span>© <span data-yr>2026</span> {NAME} All rights reserved.</span><span>Design preview by <a href="https://github.com/RGWebD" rel="noopener">RGWebD</a></span></div></div></footer>
<div class="mbar" aria-label="Quick contact">{btn_call('pri','Call')}{btn_text('gold','Text to book')}</div>
<div class="demo" role="note">Design preview by RGWebD <button type="button" aria-label="Dismiss preview note">{IC["x"]}</button></div>
<script>document.querySelectorAll('[data-yr]').forEach(function(s){{s.textContent=new Date().getFullYear()}})</script>
<script src="assets/script.js" defer></script>'''

def page(file,title,desc,body,schema,cur=None,extra_head=''):
    html_=head(file,title,desc,extra=extra_head)+'<body>'+header(cur or file)+f'<main id="main">{body}</main>'+footer()+ld(*schema)+'</body></html>'
    (OUT/file).write_text(html_,encoding='utf-8')

def phero(file,label,h1,lead,img,ctas=True):
    c=f'<div class="ctas" style="display:flex;flex-wrap:wrap;gap:12px;margin-top:26px">{btn_call()}{btn_text()}</div>' if ctas else ''
    return f'''<section class="ph"><div class="hex" aria-hidden="true"></div><div class="wrap"><div><ol class="crumbs"><li><a href="index.html">Home</a></li><li aria-current="page">{label}</li></ol>
<h1 class="split-t">{h1}</h1><p class="lead" data-r style="--d:.2s">{lead}</p>{c}</div>
<div class="phf" data-r="zoom">{pic(img,eager=True)}</div></div></section>'''

def cta_band(title='Ready when your ride is.',sub='Call, text or email and we will set a time at your home or office. Seven days a week.'):
    return f'''<section class="sec" style="padding-top:0"><div class="wrap"><div class="cta" data-r="zoom"><canvas class="beads" data-n="55" aria-hidden="true"></canvas><span class="ghost" aria-hidden="true">SHINE</span>
<p class="eb">Book your detail</p><h2>{title}</h2><p class="lead">{sub}</p><a class="big chrome" href="{TEL}">{PHONE}</a>
<div class="ctas">{btn_call('pri xl','Call now')}{btn_text('gold xl','Text to book')}<a class="btn gh xl" href="mailto:{EMAIL}?subject=Mobile%20detail%20request">{IC["mail"]}<span>Email us</span></a></div></div></div></section>'''

def rv_slide(n,t,meta,src):
    return f'<figure class="rvw-s"><q>{e(t)}</q><figcaption class="rvw-m"><b>{e(n)}</b>{stars(5)}<span>{meta}</span>{src}</figcaption></figure>'
GSRC=f'<span class="src">{IC["g"]}Google review</span>'
OSRC='<span class="src">As published on their previous website</span>'
def reviews_carousel(items):
    return f'''<div class="rvw" data-r><div class="rvw-vp"><div class="rvw-tr">{"".join(items)}</div></div>
<div class="rvw-nav"><button class="ar pv" type="button" aria-label="Previous review">{IC["left"]}</button><button class="ar nx" type="button" aria-label="Next review">{IC["right"]}</button><div class="rvw-dots"></div></div></div>'''

WAVE='<svg width="0" height="0" style="position:absolute" aria-hidden="true"><clipPath id="wave" clipPathUnits="objectBoundingBox"><path d="M.1,0 C.02,.18 .13,.34 .05,.52 C-.02,.68 .1,.84 .04,1 L1,1 L1,0 Z"/></clipPath></svg>'

# =============== HOME ===============
def home():
    hs=[('47%','40%','Mirror gloss','That’s the neighborhood reflected in the doors.'),
        ('76%','42%','Glass & trim','Windows streak-free, trim conditioned.'),
        ('50%','72%','Running boards','Steps, rockers and jambs wiped down too.'),
        ('83%','79%','Tires & wheels','Wheels cleaned, tires dressed.')]
    pins=''.join(f'<div class="hs" style="--x:{x};--y:{y}"><button type="button" aria-expanded="false" aria-label="{t}">+</button><span class="lbl" role="tooltip"><b>{t}</b>{d}</span></div>' for x,y,t,d in hs)
    ride_imgs={'auto':'w31','boat':'w08','rv':'w23','moto':'w06'}
    tabs=''.join(f'<button role="tab" id="t-{s[0]}" aria-controls="p-{s[0]}" aria-selected="false" tabindex="-1">{ {"auto":"Cars & trucks","boat":"Boats","rv":"RVs","moto":"Motorcycles"}[s[0]]}</button>' for s in SVCS)
    stage=''.join(pic(ride_imgs[s[0]],sizes='(max-width:1000px) 100vw, 55vw') for s in SVCS)
    panels=''.join(f'<div class="ride-pn" role="tabpanel" id="p-{s[0]}" aria-labelledby="t-{s[0]}" tabindex="0"{"" if i==0 else " hidden"}><h3>{s[1]}</h3><blockquote>“{e(s[2][0].upper()+s[2][1:])}”<cite>From their services page</cite></blockquote><ul class="tags">{"".join(f"<li>{e(x)}</li>" for x in s[3])}</ul><a class="btn gh" href="services.html#{s[0]}"><span>See {s[1].lower()}</span>{IC["arrow"]}</a></div>' for i,s in enumerate(SVCS))
    mq=['Hand wash','Clay bar','Carnauba wax','Ceramic wax upgrade','Steam-cleaned interiors','High-speed buffing','Scratch removal','Headlight restoration','Pet hair removal','Boats','RVs','Motorcycles']
    mqh=''.join(f'<span>{x}</span>' for x in mq)*2
    pk=f'''<div class="pks">
<article class="pk" data-r style="--d:0s"><h3>Premium Interior</h3><p class="mu">Steam-cleaned, shampooed and sanitized, top to bottom.</p><div class="pr"><small>Starting at</small><sup>$</sup>139.95</div><ul><li>Seats & mats steam extracted</li><li>Carpets shampooed</li><li>Leather & vinyl conditioned</li><li>Steam disinfect & sanitize</li></ul><a class="btn gh" href="pricing.html#interior"><span>What’s included</span>{IC["arrow"]}</a></article>
<article class="pk feat" data-r style="--d:.1s"><span class="bd">Inside + out</span><h3>Signature Detail</h3><p class="mu">Hand wash, carnauba wax and a full steam-cleaned interior.</p><div class="pr"><small>Starting at</small><sup>$</sup>169.95</div><ul><li>Hand wash & carnauba wax</li><li>Interior steam cleaned & sanitized</li><li>Wheels & chrome polished</li><li>Bug & tar removal</li></ul><a class="btn pri" href="pricing.html#signature"><span>Price my vehicle</span>{IC["arrow"]}</a></article>
<article class="pk" data-r style="--d:.2s"><h3>Ultimate Detail</h3><p class="mu">Clay bar decontamination plus every inside-and-out step.</p><div class="pr"><small>Starting at</small><sup>$</sup>199.95</div><ul><li>pH-balanced hand wash</li><li>Clay bar & paint decontamination</li><li>Leather cleaned & conditioned</li><li>Rims & tires dressed</li></ul><a class="btn gh" href="pricing.html#ultimate"><span>What’s included</span>{IC["arrow"]}</a></article></div>'''
    rv=[rv_slide(n,t,a,GSRC) for n,a,t in GREV]+[rv_slide(n,t,'',OSRC) for n,t in OREV[:3]]
    body=f'''<div id="foam" aria-hidden="true"><div class="fm"></div><div class="fl"><img src="assets/brand/logo-360.webp" width="360" height="360" alt=""></div><div class="blade"></div></div>
{WAVE}<section class="hero"><div class="hero-ph"><div class="fit">{pic('w19',eager=True,sizes='(max-width:760px) 100vw, 66vw')}<canvas class="beads" data-n="42" aria-hidden="true"></canvas></div><div class="fit pinsl">{pins}</div></div>
<div class="hero-cp"><div><p class="eb">Mobile detailing · Orlando, FL · Since 2004</p>
<h1><span class="sheen">Showroom shine</span><span class="scr">in your driveway</span><span class="sheen">Orlando.</span></h1>
<p class="lead">Cars, trucks, boats, RVs and motorcycles, hand-detailed at your home or office, seven days a week.</p>
<div class="ctas">{btn_call('pri xl')}{btn_text('gh xl')}</div>
<div class="chips"><span class="chip" data-open><span class="dot"></span><span class="t">Open 7 days · 8 AM–8 PM</span></span><span class="chip"><span class="st" aria-hidden="true">★★★★★</span>Rated 5.0 on Google</span><span class="chip">Orange · Seminole · Lake · Osceola</span></div></div></div></section>
<div class="mq" aria-label="Services"><div class="mq-t">{mqh}</div></div>

<section class="sec"><div class="hex" aria-hidden="true"></div><div class="wrap"><div class="ttl"><div><p class="eb">Pick your ride</p><h2 class="split-t">Four ways to shine.</h2></div><p>One mobile crew for everything in the driveway, from the daily driver to the boat and the motorhome.</p></div>
<div class="ride"><div class="ride-stage" data-r>{stage}</div><div><div class="ride-tabs" role="tablist" aria-label="Vehicle type"><span class="ride-ind" aria-hidden="true"></span>{tabs}</div>{panels}</div></div></div></section>

<section class="vanb"><div class="wrap"><div><p class="eb">We come to you</p><h2 class="split-t">Your driveway. Your schedule.</h2><p class="lead">Book a time, keep your day. The Detail Pros van pulls up and the work happens right where your vehicle is parked.</p>
<div class="cnty"><span><b>Orange</b> County</span><span><b>Seminole</b> County</span><span><b>Lake</b> County</span><span><b>Osceola</b> County</span></div></div>
<div class="stats" style="grid-template-columns:1fr 1fr"><div class="stat" data-r><div class="odo" data-v="2004"></div><p>Detailing Florida vehicles since 2004</p><small>From their site</small></div><div class="stat" data-r style="--d:.1s"><div class="odo" data-v="7"></div><p>Days a week, by appointment</p></div><div class="stat" data-r style="--d:.2s"><div class="odo" data-v="4"></div><p>Vehicle types: auto, boat, RV & motorcycle</p></div><div class="stat" data-r style="--d:.3s"><div class="bigv">$16</div><p>Add-ons start at $16 (Rain-X)</p></div></div></div>
<div class="vroad" aria-hidden="true"><div class="van"><div class="spray"></div><img src="assets/img/van-1000.webp" width="1000" height="400" alt="" loading="lazy"></div></div></section>

<section class="sec"><div class="wrap pol"><div><p class="eb">Try it</p><h2 class="split-t">Polish it yourself.</h2><p class="lead">Drag across the photo to wipe away the haze and see the gloss underneath. It’s a finished Detail Pros job, so the shine is real.</p>
<div class="pol-meter" aria-live="polite"><div class="bar"><i></i></div><b>0%</b></div><div class="ctas"><button class="btn pri" type="button" data-pol="all">Polish it all</button><button class="btn gh" type="button" data-pol="reset">Re-haze</button></div>
<p class="note" style="margin-top:16px">Interactive effect: the haze is simulated over one finished photo. This is not a real before/after.</p></div>
<div class="pol-st" data-r>{pic('w20',sizes='(max-width:1000px) 100vw, 55vw')}<canvas aria-label="Drag to polish the hazed photo" role="img"></canvas><span class="tag">Drag to polish</span></div></div></section>

<section class="sec" style="padding-top:0"><div class="wrap"><div class="ttl"><div><p class="eb">Packages</p><h2 class="split-t">Starting-at pricing, posted.</h2></div><p>From their current published menu. Final price depends on vehicle size and condition.</p></div>{pk}</div></section>

<section class="sec" style="padding-top:0"><div class="wrap"><div class="ttl"><div><p class="eb">What customers say</p><h2 class="split-t">Honest work, made right.</h2></div><p><a class="lk" href="reviews.html">Read every review</a></p></div>{reviews_carousel(rv)}</div></section>

<section class="sec" style="padding-top:0"><div class="wrap"><div class="tz">
<a class="tzc" href="gallery.html" data-r>{pic('w24',sizes='(max-width:760px) 100vw, 33vw')}<div class="tx"><small>Gallery</small><h3>32 real jobs</h3><span>See the work {IC["arrow"]}</span></div></a>
<a class="tzc" href="about.html" data-r style="--d:.1s">{pic('w18',sizes='(max-width:760px) 100vw, 33vw')}<div class="tx"><small>About</small><h3>Since 2004</h3><span>Meet Detail Pros {IC["arrow"]}</span></div></a>
<a class="tzc" href="contact.html" data-r style="--d:.2s">{pic('w14',sizes='(max-width:760px) 100vw, 33vw')}<div class="tx"><small>Book</small><h3>Get a quote</h3><span>Call, text or email {IC["arrow"]}</span></div></a></div></div></section>
{cta_band()}'''
    page('index.html','Detail Pros Orlando Inc. | Mobile Auto, Boat & RV Detailing in Orlando, FL',
         'Mobile car, truck, boat, RV and motorcycle detailing at your home or office in Orlando and Orange, Seminole, Lake & Osceola counties. Since 2004. Call 407-456-0031.',
         body,[biz(True)])

# =============== SERVICES ===============
def services():
    imgs={'auto':['w16','w30','w25'],'boat':['w14','w09','w12'],'rv':['w27','w22','w26'],'moto':['w13','w15','w07']}
    extra={'auto':'Packages run from the quick Premium Wax to the clay-bar Ultimate Detail, priced by vehicle size. Ceramic wax is available as an upgrade.',
           'boat':'Boats are detailed right on the trailer at your place. Boat pricing is quoted by phone.',
           'rv':'From Super Cs to full-size luxury coaches, every RV gets the same hands-on care. RV pricing is quoted by phone.',
           'moto':'Chrome, paint and engine cases cleaned and brought back up. Motorcycle pricing is quoted by phone.'}
    secs=''
    for i,s in enumerate(SVCS):
        a,b,c=imgs[s[0]]
        fr='<span class="from">Packages from $99.95</span>' if s[0]=='auto' else '<span class="from">Call for a quote</span>'
        secs+=f'''<section class="svc{' flip' if i%2 else ''}" id="{s[0]}"><div class="svc-ph" data-r="{'right' if i%2 else 'left'}"><figure>{pic(a,sizes='(max-width:1000px) 60vw, 30vw')}</figure><figure>{pic(b,sizes='(max-width:1000px) 40vw, 20vw')}</figure><figure>{pic(c,sizes='(max-width:1000px) 40vw, 20vw')}</figure></div>
<div data-r><span class="num">0{i+1}</span><h2>{s[1]}</h2>{fr}<p class="lead" style="margin-top:18px">“{e(s[2][0].upper()+s[2][1:])}”</p><p class="mu">{extra[s[0]]}</p><ul class="tags">{"".join(f"<li>{e(x)}</li>" for x in s[3])}</ul><div style="display:flex;flex-wrap:wrap;gap:10px">{btn_call('pri')}{'<a class="btn gh" href="pricing.html">See prices</a>' if s[0]=='auto' else btn_text()}</div></div></section>'''
    adds=''.join(f'<div class="ad" data-r style="--d:{i*.05:.2f}s"><b>{n}</b><span>${p}</span></div>' for i,(n,p) in enumerate(ADD))
    steps=[('Call, text or email','Tell us the vehicle, the package you want and where it’s parked. Appointment required.'),
           ('Pick a day and time','Seven days a week. Home, office or wherever the vehicle sits.'),
           ('We pull up and get to work','The Detail Pros crew arrives with the gear and gets started right there.'),
           ('Walk around and enjoy the shine','Look it over together before we roll out.')]
    tl=''.join(f'<div class="tl-step"><h3>{i+1}. {t}</h3><p>{d}</p></div>' for i,(t,d) in enumerate(steps))
    body=phero('services.html','Services','Detailing for the <span class="cy">whole</span> driveway.','Auto, boat, RV and motorcycle detailing, done mobile across the Orlando area. High-speed buffing, three-step paint processes, scratch removal, headlight restoration and steam-cleaned interiors.','w03')+f'''
<div class="wrap">{secs}</div>
<section class="sec"><div class="wrap"><div class="ttl"><div><p class="eb">Add-ons</p><h2 class="split-t">Extras, priced up front.</h2></div><p>Add any of these to a package. Prices from their current published menu.</p></div><div class="addons">{adds}</div>
<p class="pnote">Going green? Ask about eco-friendly options. Detail Pros mentions IGL products, which are soybean-based, and IGL ceramic coatings are quoted on request.</p></div></section>
<section class="sec" style="padding-top:0"><div class="wrap split"><div><p class="eb">How it works</p><h2 class="split-t">Four steps to a fresh finish.</h2><p class="lead">No shop drop-off, no waiting room. You book it, we bring the detail to you.</p></div><div class="tl"><span class="tl-fill" aria-hidden="true"></span>{tl}</div></div></section>
{cta_band('Tell us what needs a shine.')}'''
    page('services.html','Mobile Detailing Services | Auto, Boat, RV & Motorcycle | Detail Pros Orlando',
         'Mobile auto, boat, RV and motorcycle detailing in Orlando: buffing, polishing, waxing, scratch removal, headlight restoration, steam-cleaned interiors. Add-ons from $16.',
         body,[biz(False),crumbs_ld('Services','services.html'),
               {"@context":"https://schema.org","@type":"ItemList","name":"Detailing services","itemListElement":[{"@type":"ListItem","position":i+1,"item":{"@type":"Service","name":s[1],"description":s[2],"provider":{"@id":BID},"areaServed":"Orange, Seminole, Lake and Osceola counties, FL"}} for i,s in enumerate(SVCS)]}])

# =============== PRICING ===============
CARS={ # simple side-profile silhouettes
'coupe':'M4 26h6a6 6 0 0 1 12 0h34a6 6 0 0 1 12 0h6v-6l-8-3-12-8H30l-12 8-12 2z',
'sedan':'M3 26h7a6 6 0 0 1 12 0h34a6 6 0 0 1 12 0h7v-7l-6-2-10-8H28l-11 8-12 2z',
'suv':'M3 26h7a6 6 0 0 1 12 0h34a6 6 0 0 1 12 0h7V12l-6-1-4-6H22l-8 7-10 2z',
'truck':'M2 26h8a6 6 0 0 1 12 0h34a6 6 0 0 1 12 0h8V16H48V6H30l-8 9-18 2z'}
def pricing():
    szb=''.join(f'<button role="tab" aria-selected="{"true" if i==0 else "false"}" tabindex="{0 if i==0 else -1}" data-l="{e(n)}"><svg viewBox="0 0 80 32" aria-hidden="true"><path d="{CARS[k]}" fill="currentColor"/></svg>{e(n)}</button>' for i,(n,k) in enumerate(SIZES))
    P=json.dumps({'p-sig':SIG,'p-ult':ULT})
    li=lambda L:''.join(f'<li>{e(x)}</li>' for x in L)
    body=phero('pricing.html','Pricing','Prices that <span class="cy">shine</span> too.','Starting-at prices from Detail Pros’ current published menu. Pick your vehicle size to see Signature and Ultimate pricing.','w17')+f'''
<section class="sec" style="padding-top:20px"><div class="wrap"><p class="eb">Choose your vehicle</p><h2 class="split-t" style="font-size:clamp(28px,3.4vw,46px)">What are we detailing?</h2>
<div class="sizes" role="tablist" aria-label="Vehicle size" data-p='{P}'>{szb}</div>
<div class="pks">
<article class="pk" id="interior" data-r><h3>Premium Interior</h3><p class="mu">Every surface inside, steam cleaned.</p><div class="pr"><small>Starting at · price may vary by size and condition</small><sup>$</sup>139.95</div><ul>{li(INC_INT[:4])}</ul><details class="pkd"><summary>Everything included</summary><ul>{li(INC_INT)}</ul></details><a class="btn gh" href="{TEL}" style="margin-top:22px">{IC["phone"]}<span>Book Premium Interior</span></a></article>
<article class="pk feat" id="signature" data-r style="--d:.1s"><span class="bd">Inside + out</span><h3>Signature Detail</h3><p class="mu">For: <span data-sizelabel>{SIZES[0][0]}</span></p><div class="pr"><small>Starting at</small><sup>$</sup><span class="odo" id="p-sig" data-v="{SIG[0]}"></span></div><ul>{li(INC_SIG[:4])}</ul><details class="pkd"><summary>Everything included</summary><ul>{li(INC_SIG)}</ul></details><a class="btn pri" href="{TEL}" style="margin-top:22px">{IC["phone"]}<span>Book Signature</span></a></article>
<article class="pk" id="ultimate" data-r style="--d:.2s"><h3>Ultimate Detail</h3><p class="mu">Clay bar, decon and the full interior.</p><div class="pr"><small>Starting at</small><sup>$</sup><span class="odo" id="p-ult" data-v="{ULT[0]}"></span></div><ul>{li(INC_ULT[:4])}</ul><details class="pkd"><summary>Everything included</summary><ul>{li(INC_ULT)}</ul></details><a class="btn gh" href="{TEL}" style="margin-top:22px">{IC["phone"]}<span>Book Ultimate</span></a></article></div>
<p class="pnote">Prices are “starting at” and come from Detail Pros’ current published menu. Final pricing depends on the size and condition of the vehicle. Boat, RV and motorcycle details are quoted by phone.</p></div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><div class="ttl"><div><p class="eb">Quick services</p><h2 class="split-t">Wash &amp; wax menu.</h2></div></div>
<div class="pks" style="grid-template-columns:repeat(2,1fr)">
<article class="pk" data-r><h3>Premium Wax</h3><div class="pr"><sup>$</sup>99.95</div><ul><li>Superior hand wash</li><li>Liquid carnauba wax</li><li>Upgrade to ceramic wax for an additional $40</li></ul><a class="btn gh" href="{TEL}">{IC["phone"]}<span>Book Premium Wax</span></a></article>
<article class="pk" data-r style="--d:.1s"><h3>Interior Detail</h3><div class="pr"><sup>$</sup>99.95</div><ul><li>Superior hand wash plus</li><li>Liquid carnauba or ceramic wax</li><li>Vehicle hand dried</li></ul><a class="btn gh" href="{TEL}">{IC["phone"]}<span>Book Interior Detail</span></a></article></div>
<h3 style="margin-top:56px">Add-ons</h3><div class="addons">{''.join(f'<div class="ad"><b>{n}</b><span>${p}</span></div>' for n,p in ADD)}</div></div></section>
{cta_band('Get your exact price.','Every vehicle is a little different. Call or text with the year, make and model and we will quote it.')}'''
    offers=[("Premium Interior Detailing","139.95"),("Premium Wax","99.95"),("Interior Detail","99.95")]+[(f"Signature Detail – {SIZES[i][0]}",SIG[i]) for i in range(4)]+[(f"Ultimate Detail – {SIZES[i][0]}",ULT[i]) for i in range(4)]+[(n,p) for n,p in ADD]
    cat={"@context":"https://schema.org","@type":"OfferCatalog","name":"Detail Pros Orlando price menu","url":BASE+"pricing.html","itemListElement":[{"@type":"Offer","itemOffered":{"@type":"Service","name":n,"provider":{"@id":BID}},"priceSpecification":{"@type":"PriceSpecification","price":p,"priceCurrency":"USD","minPrice":p},"priceCurrency":"USD","price":p} for n,p in offers]}
    page('pricing.html','Detailing Prices | Signature, Ultimate & Interior Packages | Detail Pros Orlando',
         'Mobile detailing prices in Orlando: Premium Interior from $139.95, Signature Detail from $169.95, Ultimate Detail from $199.95, add-ons from $16. Call 407-456-0031.',
         body,[biz(False),crumbs_ld('Pricing','pricing.html'),cat])

# =============== GALLERY ===============
def gallery():
    order=[]; 
    for k in ['auto','boat','rv','moto']: order+= [(n,k) for n in CAT[k]]
    # interleave for a nicer mix
    mix=[]; L={k:[n for n in CAT[k]] for k in CAT}
    while any(L.values()):
        for k in ['auto','boat','auto','rv','moto']:
            if L[k]: mix.append((L[k].pop(0),k))
    items=''.join(f'<button class="gi" type="button" data-c="{k}" data-full="assets/img/{n}-1600.webp" aria-label="Open photo: {e(PH[n])}">{pic(n,sizes="(max-width:760px) 50vw, 33vw").replace(f"assets/img/{n}-1600.webp\" srcset","assets/img/"+n+"-800.webp\" srcset")}<span class="cap">{e(PH[n])}</span></button>' for n,k in mix)
    fl=''.join(f'<button type="button" data-f="{k}" aria-pressed="{"true" if k=="all" else "false"}">{l}</button>' for k,l in [('all','All'),('auto','Cars & trucks'),('boat','Boats'),('rv','RVs'),('moto','Motorcycles')])
    body=f'''<section class="ph" style="padding-bottom:30px"><div class="hex" aria-hidden="true"></div><div class="wrap" style="grid-template-columns:1fr"><div><ol class="crumbs"><li><a href="index.html">Home</a></li><li aria-current="page">Gallery</li></ol>
<h1 class="split-t">The <span class="cy">gloss</span> gallery.</h1><p class="lead" data-r>32 finished jobs from Detail Pros’ own photos: daily drivers, sports cars, wake boats, luxury motorhomes and touring bikes. Tap any photo to see it full size.</p></div></div></section>
<section style="padding-bottom:40px"><div class="wrap" data-lbscope><div class="gf" role="group" aria-label="Filter photos">{fl}</div><div class="gal">{items}</div></div></section>
<div class="glb" hidden role="dialog" aria-modal="true" aria-label="Photo viewer"><figure style="margin:0"><img alt=""><p></p></figure><button class="x" type="button" aria-label="Close">{IC["x"]}</button><button class="pv" type="button" aria-label="Previous photo">{IC["left"]}</button><button class="nx" type="button" aria-label="Next photo">{IC["right"]}</button></div>
{cta_band('Your ride, next in the gallery.')}'''
    page('gallery.html','Detailing Gallery | Cars, Boats, RVs & Motorcycles | Detail Pros Orlando',
         'Photos of real mobile detailing jobs by Detail Pros Orlando: cars, trucks, boats, motorhomes and motorcycles across Orange, Seminole, Lake and Osceola counties.',
         body,[biz(False),crumbs_ld('Gallery','gallery.html'),{"@context":"https://schema.org","@type":"ImageGallery","name":"Detail Pros Orlando gallery","image":[BASE+f"assets/img/{n}-1600.webp" for n,_ in mix]}])

# =============== REVIEWS ===============
def reviews():
    g=''.join(f'<figure class="rvw-s" data-r style="margin:0 0 16px"><q>{e(t)}</q><figcaption class="rvw-m"><b>{e(n)}</b>{stars(5)}<span>{a}</span>{GSRC}</figcaption></figure>' for n,a,t in GREV)
    o=''.join(f'<figure class="rvw-s" data-r style="margin:0;padding:28px"><q style="font-size:17px">{e(t)}</q><figcaption class="rvw-m"><b>{e(n)}</b>{stars(5)}</figcaption></figure>' for n,t in OREV)
    body=phero('reviews.html','Reviews','People who <span class="cy">love</span> the shine.','Two five-star Google reviews so far, plus the testimonials Detail Pros published on its previous website.','w25',ctas=False)+f'''
<section class="sec" style="padding-top:20px"><div class="wrap"><div class="ttl"><div><p class="eb">On Google</p><h2 class="split-t">What Google reviewers say.</h2></div><p><a class="btn gh" href="{GMAPS}" target="_blank" rel="noopener">{IC["g"]}<span>See them on Google</span></a></p></div>{g}</div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><div class="ttl"><div><p class="eb">From their previous website</p><h2 class="split-t">Earlier testimonials.</h2></div><p>As published on Detail Pros’ previous website (shown there as Google reviews). Shown word for word.</p></div>
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,340px),1fr));gap:16px">{o}
<figure class="rvw-s" data-r style="margin:0;padding:28px"><q style="font-size:17px">{e(FBC[2])}</q><figcaption class="rvw-m"><b>{e(FBC[0])}</b><span>{FBC[1]}</span><span class="src">{IC["fb"]}Facebook comment</span></figcaption></figure></div></div></section>
{cta_band('Be the next five-star review.')}'''
    page('reviews.html','Reviews | Detail Pros Orlando Inc. Mobile Detailing',
         'Read Google reviews and customer testimonials for Detail Pros Orlando Inc., the mobile auto, boat, RV and motorcycle detailing company serving the Orlando area.',
         body,[biz(True),crumbs_ld('Reviews','reviews.html')])

# =============== ABOUT ===============
def about():
    why=[('Professionally trained technicians','Their crew is trained in buffing, polishing and interior work.'),('Satisfaction guarantee','If something isn’t right, they make it right. Both Google reviewers say exactly that.'),('Environmentally conscious','Ask about eco-friendly options, including soybean-based IGL products.'),
         ('Convenient & flexible','Home or office, seven days a week, by appointment.'),('Premium products','Quality products and equipment tested on every type of vehicle.'),('English & Español','The team serves customers in English and Spanish.')]
    w=''.join(f'<div data-r style="--d:{i*.06:.2f}s"><h3>{t}</h3><p>{d}</p></div>' for i,(t,d) in enumerate(why))
    radar_ct=[('Seminole','50%','13%',1),('Lake','15%','42%',1),('Orange','58%','56%',1),('Osceola','50%','88%',1),
              ('Sanford','72%','20%',0),('Lake Mary','40%','24%',0),('Altamonte Springs','34%','33%',0),('Winter Park','70%','38%',0),('Windermere','24%','58%',0),('Lake Nona','76%','66%',0),('Celebration','30%','72%',0),('Kissimmee','52%','76%',0),('Saint Cloud','78%','80%',0)]
    rc=''.join(f'<span class="ct{" co" if c else ""}" style="--x:{x};--y:{y}">{n}{" Co." if c else ""}</span>' for n,x,y,c in radar_ct)
    body=phero('about.html','About','Florida detailing <span class="cy">since 2004.</span>','Detail Pros Orlando Inc. is a mobile detailing company for cars, boats, RVs and motorcycles, founded by Thomas Kerney.','w24')+f'''
<section class="sec" style="padding-top:20px"><div class="wrap split"><div data-r><p class="eb">Our story</p><h2 class="split-t">Passionate about vehicles of all types.</h2>
<p class="lead">“Detail Pros Orlando Founder and President, Thomas Kerney, along with all of his exceptionally trained staff, are extremely passionate about vehicles of all types, resulting in a beautifully finished product after every detail assignment.”<span class="fchip">From their site</span></p>
<p>They use premium-quality products and equipment tested for reliability on every kind of vehicle, and offer high-speed buffing and polishing, three-step paint processes, scratch removal and headlight restoration. Plenty of loyal customers book only with them, and new clients keep coming from referrals.</p></div>
<figure class="polaroid" data-r="zoom">{pic('w28',sizes='(max-width:1000px) 90vw, 45vw')}<figcaption>Right in your driveway</figcaption></figure></div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><div class="ttl"><div><p class="eb">Why Detail Pros</p><h2 class="split-t">What they promise.</h2></div><p>In their own words, from the “Why choose us” section of their site.</p></div><div class="why">{w}</div></div></section>
<section class="sec" style="padding-top:0"><div class="wrap split"><div><p class="eb">Service area</p><h2 class="split-t">Four counties. We come to you.</h2><p class="lead">Serving Orange, Seminole, Lake and Osceola counties. Not sure if you’re in range? Call and ask.</p><ul class="cities">{''.join(f'<li>{c}</li>' for c in CITIES)}</ul>
<div class="vanpic" data-r><img src="assets/img/van-1000.webp" width="1000" height="400" alt="The white Detail Pros Orlando mobile detailing van" loading="lazy"></div></div>
<div data-r="zoom"><div class="radar" role="img" aria-label="Stylized service area graphic showing Orange, Seminole, Lake and Osceola counties around Orlando"><span class="rg" style="--i:12%"></span><span class="rg" style="--i:25%"></span><span class="rg" style="--i:38%"></span><span class="sw"></span><span class="ctr"></span>{rc}</div><p class="radar-cap">Stylized graphic, not to scale.</p></div></div></section>
{cta_band()}'''
    page('about.html','About Detail Pros Orlando Inc. | Mobile Detailing Since 2004',
         'Detail Pros Orlando Inc., founded by Thomas Kerney, has offered mobile auto, boat, RV and motorcycle detailing in Florida since 2004, serving Orange, Seminole, Lake and Osceola counties.',
         body,[biz(False),crumbs_ld('About','about.html')])

# =============== CONTACT ===============
FAQ=[('Do you come to me?','Yes. Detail Pros is fully mobile. They come to your home or office seven days a week across Orange, Seminole, Lake and Osceola counties.'),
     ('What can you detail?','Cars, trucks and SUVs, boats, RVs (motorhomes, 5th wheels, travel trailers and mobile homes) and motorcycles, including Harleys, Victory, sport bikes and customs.'),
     ('How much does a detail cost?','From their current published menu: Premium Interior from $139.95, Signature Detail from $169.95 and Ultimate Detail from $199.95, depending on vehicle size. Premium Wax is $99.95 and add-ons start at $16. Boats, RVs and motorcycles are quoted by phone.'),
     ('How do I book?',f'Call or text {PHONE}, or email {EMAIL}. Appointments are required. There is no online booking system, so a quick call is the fastest way.'),
     ('What are your hours?','Their Google listing shows 8 AM to 8 PM, seven days a week. Call to confirm a time.'),
     ('What payment do you accept?','Credit cards, debit cards and NFC mobile payments, per their Google listing.'),
     ('Do you offer ceramic?','Ceramic wax is available as a $30 add-on, or as a $40 upgrade on the Premium Wax. Ask about IGL ceramic coating options, which are quoted on request.'),
     ('¿Hablan español?','Sí. The team serves customers in English and Spanish.')]
def contact():
    days=['Mon','Tue','Wed','Thu','Fri','Sat','Sun']; full=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    hrs=''.join(f'<li data-d="{d}"><span>{f}</span><span>8 AM – 8 PM</span></li>' for d,f in zip(days,full))
    fq=''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q,a in FAQ)
    opts=''.join(f'<option>{x}</option>' for x in ['Not sure yet','Premium Interior','Signature Detail','Ultimate Detail','Premium Wax','Interior Detail','Boat detail','RV detail','Motorcycle detail'])
    kinds=''.join(f'<option>{x}</option>' for x in ['Car / sedan','Coupe or light truck','2-door truck / small SUV','Full-size SUV / large truck','Boat','RV','Motorcycle'])
    body=phero('contact.html','Contact','Let’s get you <span class="cy">booked.</span>','Call, text or email. Appointments are required, and the crew comes to you seven days a week.','g02',ctas=False)+f'''
<section class="sec" style="padding-top:20px"><div class="wrap"><div class="cards3">
<a class="cc" href="{TEL}" data-r>{IC["phone"]}<small>Call</small><b>{PHONE}</b></a>
<a class="cc" href="{SMS}" data-r style="--d:.1s">{IC["chat"]}<small>Text</small><b>{PHONE}</b></a>
<a class="cc" href="mailto:{EMAIL}?subject=Mobile%20detail%20request" data-r style="--d:.2s">{IC["mail"]}<small>Email</small><b>{EMAIL}</b></a></div></div></section>
<section class="sec" id="quote" style="padding-top:0"><div class="wrap split" style="align-items:start"><div><p class="eb">Quote request</p><h2 class="split-t">Tell us about your ride.</h2><p class="lead">Fill this in and it opens a ready-to-send email or text to Detail Pros. Nothing is stored on this site.</p>
<div style="margin-top:30px"><span class="chip" data-open><span class="dot"></span><span class="t">Open 7 days · 8 AM–8 PM</span></span></div>
<h3 style="margin-top:34px">Hours</h3><ul class="hrs">{hrs}</ul><p class="note" style="margin-top:12px">Hours as listed on Google. By appointment only.</p></div>
<form class="form" id="quote-form" data-r><label>Name<input name="name" autocomplete="name" required></label><label>Phone<input name="phone" type="tel" autocomplete="tel" required></label>
<label>Vehicle (year, make, model)<input name="vehicle" placeholder="2021 Ford F-250"></label><label>Type<select name="kind">{kinds}</select></label>
<label>Service<select name="service">{opts}</select></label><label>Preferred day / time<input name="when" placeholder="Saturday morning"></label>
<label class="full">City or area<input name="city" placeholder="Winter Park"></label><label class="full">Notes<textarea name="notes" rows="4" placeholder="Pet hair, stains, oxidation, anything we should know"></textarea></label>
<div class="ctas full"><button class="btn pri" type="submit">{IC["mail"]}<span>Send by email</span></button><button class="btn gold" type="button" id="quote-sms">{IC["chat"]}<span>Send by text</span></button>{btn_call('gh','Or just call')}</div></form></div></section>
<section class="sec" style="padding-top:0"><div class="wrap split" style="align-items:start"><div><p class="eb">FAQ</p><h2 class="split-t">Good questions.</h2><p class="lead">Straight answers from what Detail Pros publishes.</p></div><div class="faq">{fq}</div></div></section>'''
    faq_ld={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]}
    page('contact.html','Contact & Book | Detail Pros Orlando Inc. | 407-456-0031',
         'Book mobile detailing in Orlando: call or text 407-456-0031 or email detailprosorlandoinc@gmail.com. Open 7 days, 8 AM–8 PM. Serving Orange, Seminole, Lake & Osceola counties.',
         body,[biz(False),crumbs_ld('Contact','contact.html'),faq_ld])

def notfound():
    body=f'''<section class="ph" style="min-height:80vh;display:grid;align-items:center"><div class="wrap" style="grid-template-columns:1fr;text-align:center"><div><p class="eb" style="justify-content:center">Error 404</p><h1><span class="sheen">Missed a spot.</span></h1><p class="lead" style="margin:0 auto 28px">That page isn’t here, but the shine is. Head back home or give us a call.</p><div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap"><a class="btn pri" href="/{REPO}/">Back to home</a>{btn_call('gh')}</div></div></div></section>'''
    h=head('404.html','Page not found | Detail Pros Orlando','This page could not be found.').replace('href="assets/',f'href="/{REPO}/assets/').replace('href="favicon',f'href="/{REPO}/favicon').replace('href="apple',f'href="/{REPO}/apple')
    hd=header('').replace('href="assets/',f'href="/{REPO}/assets/').replace('src="assets/',f'src="/{REPO}/assets/')
    for f,_ in NAV: hd=hd.replace(f'href="{f}"',f'href="/{REPO}/{f}"')
    ft=footer().replace('src="assets/',f'src="/{REPO}/assets/')
    for f,_ in NAV: ft=ft.replace(f'href="{f}"',f'href="/{REPO}/{f}"')
    hd=hd.replace(f'href="contact.html#quote"',f'href="/{REPO}/contact.html#quote"')
    (OUT/'404.html').write_text(h.replace('<link rel="canonical"','<meta name="robots" content="noindex"><link rel="canonical"')+'<body>'+hd+f'<main id="main">{body}</main>'+ft+'</body></html>',encoding='utf-8')

def seo():
    pages=[f for f,_ in NAV]
    (OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{BASE}{"" if f=="index.html" else f}</loc><changefreq>monthly</changefreq><priority>{"1.0" if f=="index.html" else "0.8"}</priority></url>' for f in pages)+'</urlset>\n')
    (OUT/'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n')
    adds='; '.join(f'{n} ${p}' for n,p in ADD)
    (OUT/'llms.txt').write_text(f'''# {NAME}
> Mobile auto, boat, RV and motorcycle detailing in the Orlando, Florida area. The crew comes to your home or office, seven days a week. In business since 2004 (stated on their own site). Founder and President: Thomas Kerney.

## Contact
- Phone / text: {PHONE}
- Email: {EMAIL}
- Hours: 8 AM–8 PM daily per their Google listing; appointment required. No online booking: call, text or email.
- Service area: Orange, Seminole, Lake and Osceola counties, FL (Orlando, Lake Nona, Winter Park, Windermere, Celebration, Kissimmee, Saint Cloud, Altamonte Springs, Lake Mary, Sanford). Mobile service-area business, no storefront.
- Languages: English, Spanish
- Payments: credit cards, debit cards, NFC mobile payments
- Facebook: {FB}

## Services
- Auto detailing: high-speed buffing, polishing and waxing, light scratch removal, three-step paint process, headlight restoration, steam-cleaned interiors
- Boat detailing: buffing, polishing, waxing, engine cleaning, vinyl cleaning
- RV detailing: motorhomes, 5th wheels, travel trailers, mobile homes
- Motorcycle detailing: Harley-Davidson, Victory, sport bikes, custom bikes

## Prices (starting at, from their current published menu; vary by size and condition)
- Premium Interior Detailing: from $139.95
- Signature Detail: $169.95 coupes & light trucks / $179.95 sedans / $189.95 2-door trucks & small SUVs / $219.95 full-size SUVs & large trucks
- Ultimate Detail: $199.95 / $219.95 / $239.95 / $279.95 (same size order)
- Premium Wax: $99.95 (ceramic wax upgrade +$40). Interior Detail: $99.95
- Add-ons: {adds}
- Boats, RVs and motorcycles: quoted by phone

## Reviews
- Google: 5.0 from 2 reviews (Charlotte Weinreich, Amanda).

## Pages
- Home: {BASE}
- Services: {BASE}services.html
- Pricing: {BASE}pricing.html
- Gallery: {BASE}gallery.html
- Reviews: {BASE}reviews.html
- About: {BASE}about.html
- Contact & FAQ: {BASE}contact.html
''')
    (OUT/'.nojekyll').write_text('')
    (OUT/'README.md').write_text(f'# {NAME} – redesign demo\n\nDesign preview by RGWebD. Live: {BASE}\n\nStatic site generated by `generator/build.py` (photos processed by `generator/process.py`).\n')

home(); services(); pricing(); gallery(); reviews(); about(); contact(); notfound(); seo()
print('built',sorted(p.name for p in OUT.glob('*.html')))
