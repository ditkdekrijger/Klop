// Openingsplaat met titel: export/klop-openingsplaat-titel.jpg (3200x1800), op basis van export/klop-openingsplaat.jpg.
const {chromium}=require('playwright');const path=require('path');const fs=require('fs');
const R=path.resolve(__dirname,'..');const bg='file://'+path.join(R,'export/klop-openingsplaat.jpg');const logo='file://'+path.join(R,'overzicht/ov/klop-logo-wit.png');
const html=`<!doctype html><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Funnel+Display:wght@300..800&family=Funnel+Sans:wght@300..800&display=swap" rel="stylesheet">
<style>html,body{margin:0;width:1600px;height:900px;overflow:hidden}body{background:url(${bg}) center/cover;font-family:'Funnel Sans',Arial,sans-serif;color:#fff;position:relative}
.logo{position:absolute;left:96px;top:72px;height:86px}
.k{position:absolute;left:96px;top:356px;font-size:15px;font-weight:600;letter-spacing:.18em;text-transform:uppercase;color:#EFA91F}
h1{position:absolute;left:92px;top:388px;margin:0;font-family:'Funnel Display',Arial,sans-serif;font-weight:300;font-size:108px;line-height:.98;letter-spacing:-.03em}
.line{position:absolute;left:96px;right:96px;bottom:92px;height:1px;background:rgba(255,255,255,.35)}
.f{position:absolute;left:96px;bottom:52px;font-size:14px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:rgba(255,255,255,.8)}
.f2{position:absolute;right:96px;bottom:52px;font-size:14px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:rgba(255,255,255,.8)}</style>
<img class="logo" src="${logo}"><div class="k">Vrijheidsvaarders sinds 1966</div><h1>Klop<br>merkstrategie-<br>traject</h1>
<div class="line"></div><div class="f">Recap · Brandbook · Merkuitingen · Powermarketing · Website · Code</div><div class="f2">November 2026</div>`;
(async()=>{const t=path.join(R,'export/_plaat.html');fs.writeFileSync(t,html);const b=await chromium.launch();const p=await b.newPage({viewport:{width:1600,height:900},deviceScaleFactor:2});
await p.goto('file://'+t,{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(400);
await p.screenshot({path:path.join(R,'export/klop-openingsplaat-titel.jpg'),type:'jpeg',quality:92});fs.unlinkSync(t);await b.close();console.log('ok')})();
