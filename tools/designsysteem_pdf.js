// Maakt export/klop-designsysteem.pdf uit de sectie Designsysteem van het overzicht (overzicht/index.html).
// Gebruik: node tools/designsysteem_pdf.js
const {chromium}=require('playwright');const path=require('path');
const R=path.resolve(__dirname,'..');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1440,height:900}});
await p.goto('file://'+path.join(R,'overzicht/index.html'),{waitUntil:'networkidle'});
await p.emulateMedia({media:'screen',colorScheme:'light'});
await p.evaluate(async()=>{
  document.documentElement.setAttribute('data-theme','light');
  document.querySelectorAll('img[loading="lazy"]').forEach(i=>i.loading='eager');
  document.querySelectorAll('.rv').forEach(x=>x.classList.add('in'));
  document.querySelectorAll('body > *').forEach(el=>{if(!el.contains(document.getElementById('designsysteem')))el.style.display='none'});
  document.querySelectorAll('section').forEach(s=>{if(s.id!=='designsysteem')s.style.display='none'});
  const st=document.createElement('style');st.textContent='header,#nav,.bar,footer,.lb{display:none!important}#designsysteem{padding-top:40px!important}*{animation:none!important;transition:none!important}.cp,.th,figure,.ty,.sw,.ic,.tk3>div,.logos,.rules li{break-inside:avoid}#designsysteem .wrap{padding-left:56px;padding-right:56px}#designsysteem .ty{padding-top:8px!important;padding-bottom:8px!important}';
  document.head.appendChild(st);
  const hs=[...document.querySelectorAll('#designsysteem h3')];
  hs.forEach(h=>{const t=h.textContent.trim();if(/^(Typografie|Logo|Componenten|Spelregels)/.test(t)){h.style.breakBefore='page';h.style.marginTop='0';h.style.paddingTop='40px';h.style.borderTop='0'}});
  const tk=document.querySelector('#designsysteem .tk3');if(tk){tk.style.marginTop='36px'}
  await Promise.all([...document.images].filter(i=>!i.complete).map(i=>new Promise(r=>{i.onload=i.onerror=r})));
  await document.fonts.ready;});
await p.waitForTimeout(800);
const h=await p.evaluate(()=>document.documentElement.scrollHeight);
await p.pdf({path:path.join(R,'export/klop-designsysteem.pdf'),width:'1440px',height:'1018px',printBackground:true,margin:{top:'0',bottom:'0',left:'0',right:'0'}});
await b.close();console.log('ok, hoogte',h)})();
