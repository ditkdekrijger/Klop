// Rendert de sheets (recap, brandbook, merkuitingen) op 2x resolutie naar overzicht/hd/<set>/ voor schermvullende weergave.
// Gebruik: node tools/render_hd.js [set ...]   (standaard alle drie). Recap b04 krijgt ook de lichte variant.
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const ROOT=path.resolve(__dirname,'..');const OUT=path.join(ROOT,'overzicht/hd');
const sets0=process.argv.slice(2).length?process.argv.slice(2):['recap','brandbook','merkuitingen'];
function plain(src,blobDir){
  let s=fs.readFileSync(src,'utf8');
  const helmet=(s.match(/<helmet>([\s\S]*?)<\/helmet>/)||[,''])[1];
  let body=(s.match(/<x-dc>([\s\S]*?)<\/x-dc>/)||[,''])[1].replace(/<helmet>[\s\S]*?<\/helmet>/,'');
  const blobs=fs.readdirSync(blobDir);
  body=body.replace(/\/_blob\/([0-9a-f]{32})/g,(m,id)=>{const f=blobs.find(x=>x.startsWith(id));return f?'file://'+path.join(blobDir,f):m});
  return '<!doctype html><html><head><meta charset="utf-8">'+helmet+'<style>html,body{margin:0;width:1600px;height:900px;overflow:hidden}</style></head><body>'+body+'</body></html>';
}
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1600,height:900},deviceScaleFactor:2});let n=0;
for(const set of sets0){const dir=path.join(ROOT,'bron',set);if(!fs.existsSync(path.join(dir,'project/canvas.json')))continue;const c=JSON.parse(fs.readFileSync(path.join(dir,'project/canvas.json')));
  const files=[...c.order];if(set==='recap'&&fs.existsSync(path.join(dir,'project/b04-licht.dc.html')))files.push('b04-licht.dc.html');
  fs.mkdirSync(path.join(OUT,set),{recursive:true});
  for(const f of files){const tmp=path.join(dir,'_hd.html');fs.writeFileSync(tmp,plain(path.join(dir,'project',f),path.join(dir,'blob')));
    await p.goto('file://'+tmp);await p.waitForLoadState('networkidle').catch(()=>{});await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(200);
    await p.screenshot({path:path.join(OUT,set,f.replace('.dc.html','')+'.jpg'),type:'jpeg',quality:80});fs.unlinkSync(tmp);n++}}
// pitchbeelden (siteschermen en mockups) zijn al groot genoeg: ongewijzigd kopiëren
const PS=path.join(ROOT,'overzicht/ov/pitch');for(const sub of ['','site','proto']){const d=path.join(PS,sub);fs.mkdirSync(path.join(OUT,'pitch',sub),{recursive:true});
  for(const f of fs.readdirSync(d))if(/\.jpg$/.test(f)&&!/-lang\.jpg$/.test(f)){fs.copyFileSync(path.join(d,f),path.join(OUT,'pitch',sub,f));n++}}
await b.close();console.log('hd',n)})();
