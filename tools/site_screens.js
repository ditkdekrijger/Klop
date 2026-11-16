// Echte screenshots van de site voor de merkuitingen (M23-reeks). Gebruik: node tools/site_screens.js (server op :8765 vanuit de repo-root)
const {chromium}=require('playwright');const path=require('path');
const ROOT=path.resolve(__dirname,'..');const B='http://localhost:8765/site/index.html#';
const SHOTS=[
 ['6c4fea34ea52bbcd627114aef245b497','/',null],
 ['28bc06e0425882d67d5f020e067aefa0','/boot/2',null],
 ['274a0c0eb7037c8112863cca3cd1d58e','/stel-samen/14',async p=>{}],
 ['12f20bee831ad348e963fb6a919e4935','/stel-samen/14',async p=>{await p.click('[data-a=cstep][data-i="3"]');}],
 ['ed79f5ee7b07ed163985598df8f3f4b7','/klop-premium-service',null],
];
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1440,height:1380},deviceScaleFactor:1.3});
for(const [id,u,act] of SHOTS){await p.goto(B+u);await p.waitForTimeout(1600);if(act){await act(p);await p.waitForTimeout(600)}
 await p.evaluate(()=>{document.querySelectorAll('.rv').forEach(e=>e.classList.add('in'));const m=document.getElementById('mbar');if(m)m.style.display='none';const w=document.getElementById('wa');if(w)w.style.display='none'});await p.waitForTimeout(500);
 await p.screenshot({path:path.join(ROOT,'bron/merkuitingen/blob',id+'.jpg'),type:'jpeg',quality:85});console.log('ok',u)}
await b.close()})();
