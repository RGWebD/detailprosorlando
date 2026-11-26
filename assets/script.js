/* Detail Pros Orlando – RGWebD. No libraries. */
(()=>{
const d=document,root=d.documentElement,RM=matchMedia('(prefers-reduced-motion: reduce)').matches;
root.classList.add('js');
const $=(s,c=d)=>c.querySelector(s),$$=(s,c=d)=>[...c.querySelectorAll(s)];
/* foam intro (home only, once per session) */
const foam=$('#foam');
if(foam){let seen=false;try{seen=sessionStorage.getItem('dpFoam')}catch(e){}
 if(seen||RM){foam.remove()}else{try{sessionStorage.setItem('dpFoam','1')}catch(e){}
  const end=()=>{if(!foam.isConnected)return;foam.classList.add('done');setTimeout(()=>foam.remove(),300)};
  setTimeout(end,1900);foam.addEventListener('click',end);d.addEventListener('keydown',e=>{if(e.key==='Escape')end()},{once:true})}}
/* header + progress + mobile bar */
const hdr=$('.hdr'),prog=$('.prog'),mbar=$('.mbar');
const onS=()=>{const y=scrollY,h=root.scrollHeight-innerHeight;hdr&&hdr.classList.toggle('sc',y>30);prog&&(prog.style.transform=`scaleX(${h>0?y/h:0})`);mbar&&mbar.classList.toggle('show',y>innerHeight*.55)};
addEventListener('scroll',onS,{passive:true});onS();
/* mobile menu */
const bg=$('.burger'),mn=$('.mnav');
if(bg&&mn){const set=o=>{bg.setAttribute('aria-expanded',o);mn.classList.toggle('open',o);d.body.style.overflow=o?'hidden':'';mn.inert=!o};set(false);
 bg.addEventListener('click',()=>set(bg.getAttribute('aria-expanded')!=='true'));
 d.addEventListener('keydown',e=>{if(e.key==='Escape'&&mn.classList.contains('open')){set(false);bg.focus()}});
 $$('a',mn).forEach(a=>a.addEventListener('click',()=>set(false)))}
/* demo pill */
const dm=$('.demo');if(dm){try{if(sessionStorage.getItem('dpDemo'))dm.remove()}catch(e){}$('button',dm)?.addEventListener('click',()=>{dm.remove();try{sessionStorage.setItem('dpDemo','1')}catch(e){}})}
/* split text */
$$('.split-t').forEach(el=>{let i=0;const walk=n=>{[...n.childNodes].forEach(c=>{if(c.nodeType===3){const f=d.createDocumentFragment();c.textContent.split(/(\s+)/).forEach(t=>{if(!t)return;if(/^\s+$/.test(t)){f.append(t);return}const w=d.createElement('span');w.className='w';const s=d.createElement('span');s.textContent=t;s.style.setProperty('--i',i++);w.append(s);f.append(w)});c.replaceWith(f)}else if(c.nodeType===1&&c.tagName!=='BR')walk(c)})};walk(el)});
/* reveals */
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{rootMargin:'0px 0px -8% 0px',threshold:.08});
$$('[data-r],.split-t').forEach(el=>RM?el.classList.add('in'):io.observe(el));
/* live open badge (America/New_York, 8 AM–8 PM daily per Google listing) */
const OPEN=8*60,CLOSE=20*60;
const nowNY=()=>{const p=new Intl.DateTimeFormat('en-US',{timeZone:'America/New_York',hour:'numeric',minute:'numeric',weekday:'short',hour12:false}).formatToParts(new Date());const g=t=>p.find(x=>x.type===t).value;return{wd:g('weekday'),m:(+g('hour')%24)*60+ +g('minute')}};
const n=nowNY();const isOpen=n.m>=OPEN&&n.m<CLOSE;
$$('[data-open]').forEach(el=>{el.classList.add(isOpen?'open':'closed');const t=$('.t',el);if(t)t.textContent=isOpen?'Open now · until 8 PM':(n.m<OPEN?'Opens today at 8 AM':'Opens tomorrow at 8 AM')});
$$('.hrs li').forEach(li=>{if(li.dataset.d===n.wd)li.classList.add('td')});
/* odometers */
const odo=el=>{const v=el.dataset.v;el.innerHTML='';[...v].forEach(ch=>{if(/\d/.test(ch)){const c=d.createElement('span');c.className='col';c.setAttribute('aria-hidden','true');for(let k=0;k<=9;k++){const s=d.createElement('span');s.textContent=k;c.append(s)}c.dataset.t=ch;el.append(c)}else{const s=d.createElement('span');s.className='fx';s.setAttribute('aria-hidden','true');s.textContent=ch;el.append(s)}});const sr=d.createElement('span');sr.className='sr';sr.textContent=v;el.append(sr)};
const roll=el=>$$('.col',el).forEach((c,i)=>{c.style.transitionDelay=(i*.08)+'s';c.style.transform=`translateY(-${c.dataset.t}em)`});
const oio=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){roll(e.target);oio.unobserve(e.target)}}),{threshold:.3});
$$('.odo').forEach(el=>{odo(el);if(RM)roll(el);else oio.observe(el)});
window.__odo={odo,roll};
/* tilt cards */
if(!RM&&matchMedia('(hover:hover)').matches)$$('.pk').forEach(c=>{c.addEventListener('pointermove',e=>{const r=c.getBoundingClientRect(),x=(e.clientX-r.left)/r.width,y=(e.clientY-r.top)/r.height;c.style.transform=`rotateY(${(x-.5)*8}deg) rotateX(${(.5-y)*8}deg)`;c.style.setProperty('--mx',x*100+'%');c.style.setProperty('--my',y*100+'%')});c.addEventListener('pointerleave',()=>{c.style.transform=''})});
/* magnetic buttons */
if(!RM&&matchMedia('(hover:hover)').matches)$$('.btn.mag').forEach(b=>{b.addEventListener('pointermove',e=>{const r=b.getBoundingClientRect();b.style.transform=`translate(${(e.clientX-r.left-r.width/2)*.18}px,${(e.clientY-r.top-r.height/2)*.25}px)`});b.addEventListener('pointerleave',()=>b.style.transform='')});
/* water beads canvas */
$$('canvas.beads').forEach(cv=>{const ctx=cv.getContext('2d');let W,H,B=[],vis=true,raf;const dense=+(cv.dataset.n||70);
 const mk=()=>{const r=Math.random()<.12?6+Math.random()*7:1.6+Math.random()*4.2;return{x:Math.random()*W,y:Math.random()*H,r,vy:r>6&&Math.random()<.6?.15+Math.random()*.5:0,tr:[]}};
 const size=()=>{const dpr=Math.min(devicePixelRatio||1,2),rc=cv.getBoundingClientRect();W=rc.width;H=rc.height;cv.width=W*dpr;cv.height=H*dpr;ctx.setTransform(dpr,0,0,dpr,0,0);const want=Math.round(dense*(W*H)/(1440*900));B=Array.from({length:Math.max(18,Math.min(want,160))},mk)};
 const bead=b=>{const {x,y,r}=b;ctx.save();ctx.beginPath();ctx.ellipse(x,y,r,r*.92,0,0,7);const g=ctx.createRadialGradient(x-r*.3,y-r*.35,r*.1,x,y,r);g.addColorStop(0,'rgba(255,255,255,.55)');g.addColorStop(.35,'rgba(170,230,255,.10)');g.addColorStop(.85,'rgba(0,10,20,.22)');g.addColorStop(1,'rgba(160,225,255,.55)');ctx.fillStyle=g;ctx.fill();
  ctx.beginPath();ctx.ellipse(x-r*.32,y-r*.38,r*.28,r*.18,-.6,0,7);ctx.fillStyle='rgba(255,255,255,.9)';ctx.fill();
  ctx.beginPath();ctx.arc(x+r*.25,y+r*.45,r*.18,0,7);ctx.fillStyle='rgba(120,220,255,.35)';ctx.fill();ctx.restore()};
 const draw=()=>{ctx.clearRect(0,0,W,H);B.forEach(b=>{if(b.vy){b.tr.push([b.x,b.y]);if(b.tr.length>40)b.tr.shift();ctx.beginPath();b.tr.forEach((p,i)=>i?ctx.lineTo(p[0],p[1]):ctx.moveTo(p[0],p[1]));ctx.strokeStyle='rgba(180,235,255,.10)';ctx.lineWidth=b.r*.9;ctx.lineCap='round';ctx.stroke();b.y+=b.vy;b.x+=Math.sin(b.y*.03)*.12;if(b.y>H+20){Object.assign(b,mk(),{y:-10,tr:[]})}}bead(b)})};
 const loop=()=>{draw();if(vis)raf=requestAnimationFrame(loop)};
 size();addEventListener('resize',()=>{size();if(RM)draw()});
 if(RM){draw();return}
 new IntersectionObserver(es=>{vis=es[0].isIntersecting;cancelAnimationFrame(raf);if(vis)loop()}).observe(cv)});
/* hotspots */
const fitHs=()=>$$('.hs').forEach(h=>{h.classList.remove('rev');const l=$('.lbl',h),r=l.getBoundingClientRect();const box=(h.closest('.hero-ph')||d.body).getBoundingClientRect();if(r.right>Math.min(innerWidth,box.right)-8)h.classList.add('rev')});
$$('.hs').forEach(h=>{const b=$('button',h);b.addEventListener('click',()=>{const on=!h.classList.contains('on');$$('.hs').forEach(x=>{x.classList.remove('on');$('button',x).setAttribute('aria-expanded','false')});h.classList.toggle('on',on);b.setAttribute('aria-expanded',on)})});
addEventListener('load',fitHs);addEventListener('resize',fitHs);fitHs();
/* ride switcher */
$$('.ride').forEach(rd=>{const tabs=$$('[role=tab]',rd),ind=$('.ride-ind',rd),st=$('.ride-stage',rd);
 const sel=(i,f)=>{tabs.forEach((t,k)=>{const on=k===i;t.setAttribute('aria-selected',on);t.tabIndex=on?0:-1;$('#'+t.getAttribute('aria-controls')).hidden=!on;$$('img',st)[k].classList.toggle('on',on)});const t=tabs[i];ind.style.width=t.offsetWidth+'px';ind.style.transform=`translateX(${t.offsetLeft}px)`;if(f)tabs[i].focus();st.classList.remove('flash');void st.offsetWidth;st.classList.add('flash')};
 tabs.forEach((t,i)=>{t.addEventListener('click',()=>sel(i));t.addEventListener('keydown',e=>{const k={ArrowRight:1,ArrowLeft:-1}[e.key];if(k){e.preventDefault();sel((i+k+tabs.length)%tabs.length,1)}if(e.key==='Home'){e.preventDefault();sel(0,1)}if(e.key==='End'){e.preventDefault();sel(tabs.length-1,1)}})});
 sel(0);addEventListener('resize',()=>sel(tabs.findIndex(t=>t.getAttribute('aria-selected')==='true')));addEventListener('load',()=>sel(tabs.findIndex(t=>t.getAttribute('aria-selected')==='true')))});
/* van band */
$$('.vanb').forEach(v=>{const sp=$('.spray',v);if(sp){for(let i=0;i<18;i++){const s=d.createElement('i');s.style.left=(70+Math.random()*30)+'%';s.style.top=(30+Math.random()*60)+'%';s.style.setProperty('--dx',-(40+Math.random()*140)+'px');s.style.setProperty('--dy',(Math.random()*60-40)+'px');s.style.animationDelay=(.6+Math.random()*1.4)+'s';sp.append(s)}}
 if(RM){v.classList.add('in');return}
 new IntersectionObserver((es,o)=>{if(es[0].isIntersecting){v.classList.add('in','go');setTimeout(()=>v.classList.remove('go'),2600);o.disconnect()}},{threshold:.35}).observe(v)});
/* polish canvas */
$$('.pol-st').forEach(st=>{const img=$('img',st),cv=$('canvas',st),ctx=cv.getContext('2d'),hz=d.createElement('canvas'),hx=hz.getContext('2d');const meter=$('.pol-meter'),bar=meter&&$('.bar i',meter),pct=meter&&$('b',meter);let W,H,down=false,last=null,demoed=false;
 const haze=()=>{const r=st.getBoundingClientRect(),dpr=Math.min(devicePixelRatio||1,2);W=r.width;H=r.height;cv.width=hz.width=W*dpr;cv.height=hz.height=H*dpr;ctx.setTransform(1,0,0,1,0,0);hx.setTransform(dpr,0,0,dpr,0,0);
  hx.globalCompositeOperation='source-over';hx.clearRect(0,0,W,H);hx.fillStyle='rgba(196,190,178,.62)';hx.fillRect(0,0,W,H);
  let seed=7;const rnd=()=>(seed=(seed*16807)%2147483647)/2147483647;
  for(let i=0;i<260;i++){const x=rnd()*W,y=rnd()*H,rr=20+rnd()*170;hx.beginPath();hx.arc(x,y,rr,rnd()*6,rnd()*6+1.2);hx.strokeStyle=`rgba(255,255,255,${.06+rnd()*.12})`;hx.lineWidth=.7+rnd()*1.1;hx.stroke()}
  for(let i=0;i<90;i++){const x=rnd()*W,y=rnd()*H,rr=2+rnd()*7;hx.beginPath();hx.arc(x,y,rr,0,7);hx.strokeStyle='rgba(255,255,255,.22)';hx.lineWidth=1;hx.stroke()}
  for(let i=0;i<700;i++){hx.fillStyle=`rgba(90,80,60,${rnd()*.25})`;hx.fillRect(rnd()*W,rnd()*H,1.4,1.4)}
  render();update()};
 const render=()=>{ctx.clearRect(0,0,cv.width,cv.height);ctx.drawImage(hz,0,0)};
 const brush=(x,y)=>{const R=Math.max(34,W*.06);hx.globalCompositeOperation='destination-out';const g=hx.createRadialGradient(x,y,0,x,y,R);g.addColorStop(0,'rgba(0,0,0,.95)');g.addColorStop(.6,'rgba(0,0,0,.6)');g.addColorStop(1,'rgba(0,0,0,0)');hx.fillStyle=g;hx.beginPath();hx.arc(x,y,R,0,7);hx.fill()};
 const line=(a,b)=>{const dx=b[0]-a[0],dy=b[1]-a[1],n=Math.max(1,Math.hypot(dx,dy)/8);for(let i=0;i<=n;i++)brush(a[0]+dx*i/n,a[1]+dy*i/n);render()};
 let ut;const update=()=>{clearTimeout(ut);ut=setTimeout(()=>{if(!meter)return;const s=8,c=d.createElement('canvas');c.width=W/s|0;c.height=H/s|0;const x=c.getContext('2d');x.drawImage(hz,0,0,c.width,c.height);const p=x.getImageData(0,0,c.width,c.height).data;let t=0;for(let i=3;i<p.length;i+=4)t+=p[i];const v=Math.round(100-t/(p.length/4)/(255*.62)*100);const q=Math.max(0,Math.min(100,v));bar.style.width=q+'%';pct.textContent=q+'%'},60)};
 const pos=e=>{const r=cv.getBoundingClientRect();return[e.clientX-r.left,e.clientY-r.top]};
 cv.addEventListener('pointerdown',e=>{down=true;last=pos(e);cv.setPointerCapture(e.pointerId);brush(...last);render()});
 cv.addEventListener('pointermove',e=>{if(!down)return;const p=pos(e);line(last,p);last=p;update()});
 ['pointerup','pointercancel'].forEach(t=>cv.addEventListener(t,()=>{down=false;update()}));
 const anim=(pts,ms,done)=>{if(RM){for(let i=1;i<pts.length;i++)line(pts[i-1],pts[i]);update();done&&done();return}const t0=performance.now();let k=0;const step=t=>{const f=Math.min(1,(t-t0)/ms),to=Math.floor(f*(pts.length-1));while(k<to){line(pts[k],pts[k+1]);k++}update();if(f<1)requestAnimationFrame(step);else done&&done()};requestAnimationFrame(step)};
 const demo=()=>{const pts=[];for(let i=0;i<=60;i++){const t=i/60;pts.push([W*(.12+.76*t),H*(.5+Math.sin(t*Math.PI*2)*.2)])}anim(pts,1600)};
 const all=()=>{const pts=[];const rows=Math.ceil(H/(Math.max(34,W*.06)*1.2));for(let r=0;r<=rows;r++){const y=r*H/rows;pts.push(r%2?[W+20,y]:[-20,y],r%2?[-20,y]:[W+20,y])}anim(pts,1400)};
 $('[data-pol=all]')?.addEventListener('click',all);$('[data-pol=reset]')?.addEventListener('click',haze);
 const go=()=>{haze();new IntersectionObserver((es,o)=>{if(es[0].isIntersecting&&!demoed){demoed=true;setTimeout(demo,350);o.disconnect()}},{threshold:.5}).observe(st)};
 if(img.complete)go();else img.addEventListener('load',go);
 let rt;addEventListener('resize',()=>{clearTimeout(rt);rt=setTimeout(haze,200)})});
/* timeline fill */
$$('.tl').forEach(tl=>{const f=$('.tl-fill',tl),steps=$$('.tl-step',tl);const up=()=>{const r=tl.getBoundingClientRect(),mid=innerHeight*.62,h=Math.max(0,Math.min(r.height-12,mid-r.top));f.style.height=h+'px';steps.forEach(s=>{if(s.getBoundingClientRect().top<mid)s.classList.add('lit')})};
 if(RM){f.style.height='calc(100% - 12px)';steps.forEach(s=>s.classList.add('lit'));return}addEventListener('scroll',up,{passive:true});up()});
/* size selector (pricing) */
$$('.sizes').forEach(sz=>{const bt=$$('[role=tab]',sz);const P=JSON.parse(sz.dataset.p);
 const sel=(i,f)=>{bt.forEach((b,k)=>{b.setAttribute('aria-selected',k===i);b.tabIndex=k===i?0:-1});if(f)bt[i].focus();Object.entries(P).forEach(([id,arr])=>{const el=d.getElementById(id);if(!el)return;el.dataset.v=arr[i];window.__odo.odo(el);requestAnimationFrame(()=>requestAnimationFrame(()=>window.__odo.roll(el)))});const lab=$('[data-sizelabel]');if(lab)lab.textContent=bt[i].dataset.l};
 bt.forEach((b,i)=>{b.addEventListener('click',()=>sel(i));b.addEventListener('keydown',e=>{const k={ArrowRight:1,ArrowLeft:-1,ArrowDown:1,ArrowUp:-1}[e.key];if(k){e.preventDefault();sel((i+k+bt.length)%bt.length,1)}})})});
/* reviews carousel */
$$('.rvw').forEach(c=>{const tr=$('.rvw-tr',c),sl=$$('.rvw-s',c),dots=$('.rvw-dots',c);let i=0,t,paused=false;
 sl.forEach((s,k)=>{const b=d.createElement('button');b.type='button';b.setAttribute('aria-label','Show review '+(k+1));b.addEventListener('click',()=>go(k));dots.append(b)});
 const go=k=>{i=(k+sl.length)%sl.length;tr.style.transform=`translateX(-${i*100}%)`;sl.forEach((s,j)=>{s.setAttribute('aria-hidden',j!==i);s.inert=j!==i});$$('button',dots).forEach((b,j)=>b.setAttribute('aria-current',j===i))};
 $('.pv',c)?.addEventListener('click',()=>go(i-1));$('.nx',c)?.addEventListener('click',()=>go(i+1));
 c.addEventListener('mouseenter',()=>paused=true);c.addEventListener('mouseleave',()=>paused=false);c.addEventListener('focusin',()=>paused=true);c.addEventListener('focusout',()=>paused=false);
 let sx=null;tr.addEventListener('pointerdown',e=>sx=e.clientX);tr.addEventListener('pointerup',e=>{if(sx!==null&&Math.abs(e.clientX-sx)>40)go(i+(e.clientX<sx?1:-1));sx=null});
 go(0);if(!RM)t=setInterval(()=>{if(!paused&&!d.hidden)go(i+1)},6500)});
/* gallery filter + lightbox */
const gal=$('.gal');
if(gal){const fb=$$('.gf button');fb.forEach(b=>b.addEventListener('click',()=>{fb.forEach(x=>x.setAttribute('aria-pressed',x===b));const c=b.dataset.f;$$('.gi',gal).forEach(g=>g.classList.toggle('hide',c!=='all'&&g.dataset.c!==c))}))}
const lb=$('.glb');
if(lb){const im=$('img',lb),cap=$('p',lb);let list=[],i=0,opener=null;
 const show=k=>{i=(k+list.length)%list.length;const g=list[i];im.src=g.dataset.full;im.alt=$('img',g).alt;cap.textContent=$('img',g).alt+'  ·  '+(i+1)+' / '+list.length};
 const open=g=>{list=$$('.gi',g.closest('[data-lbscope]')||d).filter(x=>!x.classList.contains('hide'));opener=g;lb.hidden=false;d.body.style.overflow='hidden';show(list.indexOf(g));$('.x',lb).focus()};
 const close=()=>{lb.hidden=true;d.body.style.overflow='';im.removeAttribute('src');opener&&opener.focus()};
 $$('.gi').forEach(g=>g.addEventListener('click',()=>open(g)));
 $('.x',lb).addEventListener('click',close);$('.pv',lb).addEventListener('click',()=>show(i-1));$('.nx',lb).addEventListener('click',()=>show(i+1));
 lb.addEventListener('click',e=>{if(e.target===lb)close()});
 d.addEventListener('keydown',e=>{if(lb.hidden)return;if(e.key==='Escape')close();if(e.key==='ArrowRight')show(i+1);if(e.key==='ArrowLeft')show(i-1);if(e.key==='Tab'){const f=$$('button',lb);const a=f.indexOf(d.activeElement);e.preventDefault();f[(a+(e.shiftKey?-1:1)+f.length)%f.length].focus()}});
 let sx=null;lb.addEventListener('pointerdown',e=>sx=e.clientX);lb.addEventListener('pointerup',e=>{if(sx!==null&&Math.abs(e.clientX-sx)>50)show(i+(e.clientX<sx?1:-1));sx=null})}
/* quote form -> pre-filled email or text (nothing is submitted anywhere) */
const qf=$('#quote-form');
if(qf){const body=()=>{const f=new FormData(qf);return `Hi Detail Pros, I'd like a quote.\nName: ${f.get('name')||''}\nPhone: ${f.get('phone')||''}\nVehicle: ${f.get('vehicle')||''} (${f.get('kind')||''})\nService: ${f.get('service')||''}\nPreferred day/time: ${f.get('when')||''}\nArea / city: ${f.get('city')||''}\nNotes: ${f.get('notes')||''}`};
 qf.addEventListener('submit',e=>{e.preventDefault();location.href='mailto:detailprosorlandoinc@gmail.com?subject='+encodeURIComponent('Detailing quote request')+'&body='+encodeURIComponent(body())});
 $('#quote-sms')?.addEventListener('click',()=>{const ios=/iPad|iPhone|iPod|Macintosh/.test(navigator.userAgent)&&'ontouchend' in d;location.href='sms:+14074560031'+(ios?'&':'?')+'body='+encodeURIComponent(body())})}
})();
