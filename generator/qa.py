"""Playwright QA for the Detail Pros Orlando demo. usage: python3 qa.py [base_url]  (default: local server)"""
import asyncio,sys,json,functools,threading,http.server,socketserver,re
from playwright.async_api import async_playwright
PAGES=['index','services','pricing','gallery','reviews','about','contact']
BASE=sys.argv[1] if len(sys.argv)>1 else None
if not BASE:
    class Q(http.server.SimpleHTTPRequestHandler):
        def log_message(self,*a):pass
    socketserver.TCPServer.allow_reuse_address=True
    srv=socketserver.ThreadingTCPServer(('127.0.0.1',8962),functools.partial(Q,directory='/workspace/detailpros-site'));threading.Thread(target=srv.serve_forever,daemon=True).start()
    BASE='http://127.0.0.1:8962/'
fails=[]
def F(m): fails.append(m); print('FAIL',m,flush=True)
JS=r"""async()=>{
 const H=document.body.scrollHeight;for(let y=0;y<H;y+=400){scrollTo(0,y);await new Promise(r=>setTimeout(r,70))}
 await new Promise(r=>setTimeout(r,2600));
 const imgs=[...document.images];
 const broken=imgs.filter(i=>i.getAttribute('src')&&(!i.complete||i.naturalWidth===0)).map(i=>i.getAttribute('src'));
 const hidden=[...document.querySelectorAll('[data-r],.split-t')].filter(e=>{const s=getComputedStyle(e);return e.offsetParent!==null&&(+s.opacity<.5)}).map(e=>e.className||e.tagName).slice(0,5);
 const counters=[...document.querySelectorAll('.odo')].filter(o=>o.offsetParent!==null).map(o=>{const got=[...o.children].map(c=>c.classList.contains('col')?String(Math.round(-new DOMMatrix(getComputedStyle(c).transform).m42/parseFloat(getComputedStyle(o).fontSize))):(c.classList.contains('fx')?c.textContent:'')).join('');return [o.dataset.v,got]});
 const base=imgs.filter(i=>!/brand\/|van-/.test(i.getAttribute('src')||'')&&i.closest('.glb')===null).map(i=>(i.getAttribute('src')||'').replace(/^.*\//,'').replace(/-\d+\.webp$/,''));
 const ld=[...document.querySelectorAll('script[type="application/ld+json"]')].map(s=>s.textContent);
 return {ow:document.documentElement.scrollWidth,vw:innerWidth,broken,hidden,counters,imgs:base,ld,h1:document.querySelectorAll('h1').length,title:document.title,
   ring:[...document.querySelectorAll('body *')].some(e=>{const s=getComputedStyle(e);return s.position==='fixed'&&s.pointerEvents==='none'&&s.borderRadius==='50%'&&e.offsetWidth<80&&e.offsetWidth>8}),
   wide:[...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();return r.right>innerWidth+1&&r.width>0&&getComputedStyle(e).position!=='fixed'&&!e.closest('.mq,.rvw-tr,.vroad,.radar,.hero-ph')}).slice(0,4).map(e=>e.tagName+'.'+e.className)}
}"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        for w,h in [(1440,900),(390,844)]:
            for rm in ['no-preference','reduce']:
                ctx=await b.new_context(viewport={'width':w,'height':h},reduced_motion=rm)
                await ctx.add_init_script("sessionStorage.setItem('dpFoam','1')")
                for n in PAGES:
                    pg=await ctx.new_page(); errs=[]
                    pg.on('console',lambda m,errs=errs: m.type=='error' and errs.append(m.text))
                    pg.on('pageerror',lambda ex,errs=errs: errs.append(str(ex)))
                    resp=await pg.goto(BASE+n+'.html',wait_until='load',timeout=60000)
                    res=await pg.evaluate(JS); tag=f'{n}@{w}/{rm}'
                    if resp.status!=200: F(f'{tag} status {resp.status}')
                    if res['ow']>res['vw']: F(f'{tag} overflow {res["ow"]}>{res["vw"]} {res["wide"]}')
                    if res['broken']: F(f'{tag} broken {res["broken"]}')
                    if res['hidden']: F(f'{tag} hidden {res["hidden"]}')
                    for want,got in res['counters']:
                        if want!=got: F(f'{tag} counter {want}!={got}')
                    if res['h1']!=1: F(f'{tag} h1 {res["h1"]}')
                    if res['ring']: F(f'{tag} cursor ring?')
                    if errs: F(f'{tag} console {errs[:3]}')
                    for s in res['ld']:
                        try: json.loads(s)
                        except Exception as ex: F(f'{tag} bad json-ld {ex}')
                    dup=sorted({x for x in res['imgs'] if res['imgs'].count(x)>1})
                    if dup: F(f'{tag} duplicate photos {dup}')
                    if w==390 and rm=='no-preference':
                        await pg.evaluate('scrollTo(0,0)'); await pg.wait_for_timeout(300)
                        await pg.click('.burger'); await pg.wait_for_timeout(500)
                        if await pg.evaluate("getComputedStyle(document.querySelector('.mnav')).visibility")!='visible': F(f'{tag} menu not opening')
                        await pg.click('.burger'); await pg.wait_for_timeout(400)
                    if n=='pricing' and rm=='no-preference':
                        await pg.click('.sizes button:nth-child(4)'); await pg.wait_for_timeout(2600)
                        r=await pg.evaluate(JS)
                        if ['219.95','219.95'] not in r['counters'] or ['279.95','279.95'] not in r['counters']: F(f'{tag} size switch counters {r["counters"]}')
                    if n=='index' and rm=='no-preference':
                        await pg.click('#t-boat'); await pg.wait_for_timeout(400)
                        if await pg.evaluate("document.getElementById('p-boat').hidden"): F(f'{tag} ride tab')
                        await pg.evaluate('scrollTo(0,0)'); await pg.wait_for_timeout(300)
                        try:
                            await pg.click('.hs button >> nth=0',timeout=4000); await pg.wait_for_timeout(300)
                            if not await pg.evaluate("document.querySelector('.hs').classList.contains('on')"): F(f'{tag} hotspot not toggling')
                            lb=await pg.evaluate("(()=>{const r=document.querySelector('.hs.on .lbl').getBoundingClientRect();return [r.left,r.right]})()")
                            if lb[0]<0 or lb[1]>w: F(f'{tag} hotspot label off-screen {lb}')
                        except Exception as ex: F(f'{tag} hotspot click blocked {str(ex)[:80]}')
                    if n=='gallery' and rm=='no-preference':
                        await pg.click('.gi >> nth=2'); await pg.wait_for_timeout(500)
                        ok=await pg.evaluate("(()=>{const i=document.querySelector('.glb img');return !document.querySelector('.glb').hidden&&i.complete&&i.naturalWidth>0})()")
                        if not ok: F(f'{tag} lightbox')
                        await pg.keyboard.press('ArrowRight'); await pg.keyboard.press('Escape')
                    if w==1440 and rm=='no-preference': print(n,'ok',len(res['imgs']),'imgs |',res['title'][:80],flush=True)
                    await pg.close()
                await ctx.close()
        await b.close()
asyncio.run(main())
print('FAILS',len(fails))
