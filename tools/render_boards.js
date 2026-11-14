// Rendert de .dc.html-boards (recap, brandbook, merkuitingen) en de componentpreviews van het designsysteem naar JPG.
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const ROOT=path.resolve(__dirname,'..');const OUT=path.join(ROOT,'overzicht/img');
const SETS={recap:null,brandbook:null,merkuitingen:null};
function plain(src,blobDir){
  let s=fs.readFileSync(src,'utf8');
  const helmet=(s.match(/<helmet>([\s\S]*?)<\/helmet>/)||[,''])[1];
  let body=(s.match(/<x-dc>([\s\S]*?)<\/x-dc>/)||[,''])[1].replace(/<helmet>[\s\S]*?<\/helmet>/,'');
  const blobs=fs.readdirSync(blobDir);
  body=body.replace(/\/_blob\/([0-9a-f]{32})/g,(m,id)=>{const f=blobs.find(x=>x.startsWith(id));return f?'file://'+path.join(blobDir,f):m});
  return '<!doctype html><html><head><meta charset="utf-8">'+helmet+'<style>html,body{margin:0;width:1600px;height:900px;overflow:hidden}</style></head><body>'+body+'</body></html>';
}
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1600,height:900}});const manifest={};
for(const set of Object.keys(SETS)){const dir=path.join(ROOT,'bron',set);const c=JSON.parse(fs.readFileSync(path.join(dir,'project/canvas.json')));
  fs.mkdirSync(path.join(OUT,set),{recursive:true});manifest[set]=[];
  for(const f of c.order){const tmp=path.join(dir,'_render.html');fs.writeFileSync(tmp,plain(path.join(dir,'project',f),path.join(dir,'blob')));
    await p.goto('file://'+tmp);await p.waitForLoadState('networkidle').catch(()=>{});await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(150);
    const name=f.replace('.dc.html','')+'.jpg';await p.screenshot({path:path.join(OUT,set,name),type:'jpeg',quality:78});
    manifest[set].push({file:set+'/'+name,title:c.boards[f].title});fs.unlinkSync(tmp)}}
// designsysteem componenten
const ds=path.join(ROOT,'bron/designsysteem/project/components');fs.mkdirSync(path.join(OUT,'ds'),{recursive:true});manifest.ds=[];
const q=await b.newPage({viewport:{width:760,height:400},deviceScaleFactor:2});
for(const comp of fs.readdirSync(ds).sort()){const f=path.join(ds,comp,'preview.html');if(!fs.existsSync(f))continue;
  let h=fs.readFileSync(f,'utf8');const g=(h.match(/group="([^"]+)"/)||[,''])[1];
  h='<!doctype html><meta charset="utf-8"><style>:root{--surface:#F5F7F8;--ink:#0B1930}</style>'+h.replace(/src="\.\.\/\.\.\/assets/g,'src="file://'+path.join(ROOT,'bron/designsysteem/project/assets'));
  const tmp=path.join(ds,comp,'_r.html');fs.writeFileSync(tmp,h);await q.goto('file://'+tmp);await q.waitForLoadState('networkidle').catch(()=>{});await q.evaluate(()=>document.fonts.ready);
  const rm=fs.existsSync(path.join(ds,comp,'README.md'))?fs.readFileSync(path.join(ds,comp,'README.md'),'utf8'):'';
  await q.screenshot({path:path.join(OUT,'ds',comp+'.jpg'),type:'jpeg',quality:82,fullPage:true});fs.unlinkSync(tmp);manifest.ds.push({file:'ds/'+comp+'.jpg',title:comp,group:g,readme:rm})}
fs.writeFileSync(path.join(ROOT,'overzicht/manifest.json'),JSON.stringify(manifest,null,1));await b.close();console.log(Object.entries(manifest).map(([k,v])=>k+':'+v.length).join(' '))})();
