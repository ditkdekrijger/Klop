// Mockups uit de aangeleverde site-schermen (bron/site-screens), in laptop en telefoon.
const {chromium}=require('playwright');const path=require('path');const fs=require('fs');
const ROOT=path.resolve(__dirname,'..');const SRC=path.join(ROOT,'overzicht/ov/pitch/site');const OUT=path.join(ROOT,'overzicht/ov/pitch');
const SETS=[['mock-home','home-hero','m-home'],['mock-plp','collectie','m-collectie'],['mock-pdp','pdp','m-pdp'],['mock-keuzehulp','home-zoeker',null],['mock-premium','home-premium',null],
 ['mock-proto-modellen','../proto/modellen-d','../proto/modellen-m'],['mock-proto-kussens','../proto/kussens-d','../proto/kussens-m'],['mock-proto-3d','../proto/3d-d','../proto/motor-m'],['mock-proto-overzicht','../proto/overzicht-d','../proto/overzicht-m']];
// proto-schermen: node tools/proto_shots.js
(async()=>{const b=await chromium.launch();const f=await b.newPage({viewport:{width:2400,height:1500}});
for(const [n,dk,mb] of SETS){const u=x=>'file://'+path.join(SRC,x+'.jpg');
 const html=`<!doctype html><html><head><style>html,body{margin:0;width:2400px;height:1500px;background:linear-gradient(160deg,#F5F7F8 0%,#DDE3E8 100%);overflow:hidden}
 .lap{position:absolute;left:${mb?150:250}px;top:120px;width:1900px}
 .scr{background:#0B1930;border-radius:34px 34px 0 0;padding:26px 26px 30px;box-shadow:0 60px 120px -50px rgba(11,25,48,.55)}
 .scr div{height:1130px;border-radius:8px;background:url(${u(dk)}) top center/cover #fff}
 .base{height:34px;background:linear-gradient(#C9D1D8,#AAB3BD);border-radius:0 0 26px 26px;margin:0 -70px;position:relative}
 .base:after{content:"";position:absolute;left:50%;top:0;width:260px;height:14px;margin-left:-130px;background:#98A3AE;border-radius:0 0 14px 14px}
 .ph{position:absolute;right:120px;bottom:70px;width:470px;height:960px;background:#0B1930;border-radius:70px;padding:18px;box-shadow:0 60px 120px -40px rgba(11,25,48,.6)}
 .ph div{width:100%;height:100%;border-radius:54px;background:url(${mb?u(mb):''}) top center/cover #fff}
 </style></head><body><div class="lap"><div class="scr"><div></div></div><div class="base"></div></div>${mb?'<div class="ph"><div></div></div>':''}</body></html>`;
 const t=path.join(ROOT,'tools/pitch/_f2.html');fs.writeFileSync(t,html);await f.goto('file://'+t);await f.waitForTimeout(300);await f.screenshot({path:path.join(OUT,n+'.jpg'),type:'jpeg',quality:82});console.log('ok',n)}
await b.close()})();
