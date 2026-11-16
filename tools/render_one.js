// Rendert één .dc.html-board naar JPG. Gebruik: node tools/render_one.js <set> <bestand.dc.html> <uit.jpg>
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const [set,file,out]=process.argv.slice(2);const ROOT=path.resolve(__dirname,'..');const dir=path.join(ROOT,'bron',set);
let s=fs.readFileSync(path.join(dir,'project',file),'utf8');const helmet=(s.match(/<helmet>([\s\S]*?)<\/helmet>/)||[,''])[1];
let body=(s.match(/<x-dc>([\s\S]*?)<\/x-dc>/)||[,''])[1].replace(/<helmet>[\s\S]*?<\/helmet>/,'');const blobs=fs.readdirSync(path.join(dir,'blob'));
body=body.replace(/\/_blob\/([0-9a-f]{32})/g,(m,id)=>{const f=blobs.find(x=>x.startsWith(id));return f?'file://'+path.join(dir,'blob',f):m});
const tmp=path.join(dir,'_one.html');fs.writeFileSync(tmp,'<!doctype html><html><head><meta charset="utf-8">'+helmet+'<style>html,body{margin:0;width:1600px;height:900px;overflow:hidden}</style></head><body>'+body+'</body></html>');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1600,height:900}});await p.goto('file://'+tmp);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);await p.screenshot({path:out,type:'jpeg',quality:80});fs.unlinkSync(tmp);await b.close()})();
