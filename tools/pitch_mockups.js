// Mockups voor de pitch: screenshots van de site, in een laptop- en telefoonframe. Server op :8765 vanuit de repo-root.
const {chromium}=require('playwright');const path=require('path');const fs=require('fs');
const ROOT=path.resolve(__dirname,'..');const OUT=path.join(ROOT,'overzicht/ov/pitch');const TMP=path.join(ROOT,'tools/pitch/shots');fs.mkdirSync(TMP,{recursive:true});
const B='http://localhost:8765/site/index.html#';
async function prep(p){await p.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=600){scrollTo(0,y);await new Promise(r=>setTimeout(r,30))}scrollTo(0,0);
 document.querySelectorAll('.rv,.spoor,.ev').forEach(e=>e.classList.add('in'));['mbar','wa','sprog'].forEach(i=>{const e=document.getElementById(i);if(e)e.style.display='none'});document.querySelectorAll('.wa').forEach(e=>e.style.display='none')});await p.waitForTimeout(700)}
(async()=>{const b=await chromium.launch();
const d=await b.newPage({viewport:{width:1440,height:900},deviceScaleFactor:1.5});
const m=await b.newPage({viewport:{width:390,height:844},deviceScaleFactor:2,isMobile:true,hasTouch:true});
const shot=async(pg,u,name,opt={})=>{await pg.goto(B+u);await pg.waitForTimeout(opt.wait||1500);if(opt.act)await opt.act(pg);await prep(pg);
 if(opt.el){const el=await pg.$(opt.el);await el.scrollIntoViewIfNeeded();await pg.waitForTimeout(400);await el.screenshot({path:path.join(TMP,name)})}
 else if(opt.full){await pg.screenshot({path:path.join(TMP,name),fullPage:true,clip:{x:0,y:0,width:pg.viewportSize().width,height:opt.full}})}
 else{if(opt.yel){await pg.evaluate(sel=>{const e=document.querySelector(sel);scrollTo(0,e.getBoundingClientRect().top+scrollY-110)},opt.yel);await pg.waitForTimeout(3000)}if(opt.y){await pg.evaluate(y=>scrollTo(0,y),opt.y);await pg.waitForTimeout(500)}await pg.screenshot({path:path.join(TMP,name)})}};
await shot(d,'/','home-d.png');await shot(d,'/','home-lang.png',{full:5200});
await shot(d,'/boot/2','pdp-d.png');await shot(d,'/boot/2','pdp-lang.png',{full:3600});
await shot(d,'/boten','plp-d.png');await shot(d,'/boten','plp-lang.png',{full:3000});
await shot(d,'/','finder-d.png',{yel:'section.finder'});
await shot(d,'/stel-samen/maxima-760-nieuw','cfg-mx-d.png',{wait:4500});
await shot(d,'/stel-samen/maxima-760-nieuw?stap=overzicht','cfg-ov-d.png',{wait:5000});
await shot(d,'/stel-samen/14','cfg-alg-d.png',{act:async p=>{await p.click('[data-a=cstep][data-i="2"]');await p.waitForTimeout(400)}});
await shot(m,'/','home-m.png',{y:0});await shot(m,'/boot/2','pdp-m.png');await shot(m,'/boten','plp-m.png',{y:520});
await shot(m,'/','finder-m.png',{el:'section.finder'});await shot(m,'/stel-samen/maxima-760-nieuw','cfg-m.png',{wait:4500});
// samenstellen in frames
const f=await b.newPage({viewport:{width:2400,height:1500}});
const SETS=[['mock-home','home-d.png','home-m.png'],['mock-pdp','pdp-d.png','pdp-m.png'],['mock-plp','plp-d.png','plp-m.png'],['mock-keuzehulp','finder-d.png','finder-m.png'],['mock-configurator','cfg-mx-d.png','cfg-m.png'],['mock-configurator-alg','cfg-alg-d.png',null],['mock-configurator-overzicht','cfg-ov-d.png',null],['mock-proto','proto-760-d.png','proto-760-m.png']];
for(const [n,dk,mb] of SETS){const u=x=>'file://'+path.join(TMP,x);
 const html=`<!doctype html><html><head><style>html,body{margin:0;width:2400px;height:1500px;background:linear-gradient(160deg,#F5F7F8 0%,#DDE3E8 100%);overflow:hidden;font-family:sans-serif}
 .lap{position:absolute;left:150px;top:120px;width:1900px}
 .scr{background:#0B1930;border-radius:34px 34px 0 0;padding:26px 26px 30px;box-shadow:0 60px 120px -50px rgba(11,25,48,.55)}
 .scr div{height:1130px;border-radius:8px;background:url(${u(dk)}) top center/cover #fff}
 .base{height:34px;background:linear-gradient(#C9D1D8,#AAB3BD);border-radius:0 0 26px 26px;margin:0 -70px;position:relative}
 .base:after{content:"";position:absolute;left:50%;top:0;width:260px;height:14px;margin-left:-130px;background:#98A3AE;border-radius:0 0 14px 14px}
 .ph{position:absolute;right:120px;bottom:70px;width:470px;height:960px;background:#0B1930;border-radius:70px;padding:18px;box-shadow:0 60px 120px -40px rgba(11,25,48,.6)}
 .ph div{width:100%;height:100%;border-radius:54px;background:url(${mb?u(mb):''}) top center/cover #fff}
 </style></head><body><div class="lap"><div class="scr"><div></div></div><div class="base"></div></div>${mb?'<div class="ph"><div></div></div>':''}</body></html>`;
 fs.writeFileSync(path.join(TMP,'_f.html'),html);await f.goto('file://'+path.join(TMP,'_f.html'));await f.waitForTimeout(300);await f.screenshot({path:path.join(OUT,n+'.jpg'),type:'jpeg',quality:82});console.log('ok',n)}
// lange schermen voor de fullscreen-weergave
const sharp=null;for(const n of ['home-lang','pdp-lang','plp-lang']){fs.copyFileSync(path.join(TMP,n+'.png'),path.join(TMP,n+'.copy.png'))}
await b.close()})();
