// Schermen van het app-prototype van de Maxima-configurator (https://maxima.mustang.dev/) naar overzicht/ov/pitch/proto/.
const {chromium}=require('playwright');const path=require('path');const fs=require('fs');
const OUT=path.resolve(__dirname,'../overzicht/ov/pitch/proto');fs.mkdirSync(OUT,{recursive:true});
const U='https://maxima.mustang.dev/';
async function shot(p,n){await p.waitForTimeout(1800);await p.screenshot({path:path.join(OUT,n+'.png')});console.log('ok',n)}
(async()=>{const b=await chromium.launch();
for(const [suf,vp] of [['d',{width:1440,height:900,deviceScaleFactor:2}],['m',{width:390,height:844,deviceScaleFactor:2,isMobile:true,hasTouch:true}]]){
 const p=await b.newPage({viewport:{width:vp.width,height:vp.height},deviceScaleFactor:vp.deviceScaleFactor,isMobile:!!vp.isMobile,hasTouch:!!vp.hasTouch});
 await p.goto(U,{waitUntil:'networkidle',timeout:60000}).catch(()=>{});await shot(p,'modellen-'+suf);
 await p.goto(U+'configurator/maxima-760-nieuw',{waitUntil:'networkidle',timeout:60000}).catch(()=>{});await p.waitForTimeout(2500);
 await p.click('button:has-text("Donkerblauw")').catch(()=>{});await shot(p,'romp-'+suf);
 await p.click('button:has-text("Kuip & kussens")').catch(()=>{});await shot(p,'kussens-'+suf);
 await p.click('button:has-text("Motor")').catch(()=>{});await shot(p,'motor-'+suf);
 if(suf==='d'){await p.click('button:has-text("3D")').catch(()=>{});await p.waitForTimeout(5000);await shot(p,'3d-'+suf);await p.click('button:has-text("Foto")').catch(()=>{});}
 await p.click('button:has-text("Overzicht")').catch(()=>{});await shot(p,'overzicht-'+suf);
 await p.close()}
await b.close()})();
