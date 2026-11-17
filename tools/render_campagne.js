// Rendert tools/campagne_digitaal.html naar overzicht/ov/merkuitingen/m26g-campagne-digitaal.jpg (1600x900) en de 2x-versie in overzicht/hd.
const {chromium}=require('playwright');const path=require('path');const fs=require('fs');
const R=path.resolve(__dirname,'..');
let h=fs.readFileSync(path.join(__dirname,'campagne_digitaal.html'),'utf8').replace(/\{\{B\}\}/g,'file://'+path.join(R,'bron/campagne')).replace(/\{\{O\}\}/g,'file://'+path.join(R,'overzicht/ov'));
const t=path.join(R,'bron/campagne/_r.html');fs.writeFileSync(t,h);
(async()=>{const b=await chromium.launch();
for(const [dpr,out] of [[1,'overzicht/ov/merkuitingen/m26g-campagne-digitaal.jpg'],[2,'overzicht/hd/merkuitingen/m26g-campagne-digitaal.jpg']]){
 const p=await b.newPage({viewport:{width:1600,height:900},deviceScaleFactor:dpr});await p.goto('file://'+t,{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);
 fs.mkdirSync(path.dirname(path.join(R,out)),{recursive:true});await p.screenshot({path:path.join(R,out),type:'jpeg',quality:dpr==2?80:82});await p.close()}
fs.unlinkSync(t);await b.close();console.log('ok')})();
