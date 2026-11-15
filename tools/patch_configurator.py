"""Patch: configurator afgemaakt en ingebouwd in de site.

Toepassen na patch_showroom.py en patch_maxima.py, vóór patch_mobile.py.

Maxima (alle Maxima-modellen, eigen huisstijl):
- #/stel-samen/maxima[-<model>] is een schermvullende configuratorpagina: smalle Klop-balk, de Maxima-configurator
  eronder over de rest van het scherm. Geen voet, geen actiebalk, geen pagina-in-pagina meer.
- De configurator meldt zijn stand (model, keuzes, totaal) aan de site. De adresbalk volgt mee, zodat een
  samenstelling deelbaar en terug te openen is: #/stel-samen/maxima-760-nieuw?c=...&ral=...&stap=...
- "Bewaar in Mijn Klop" en een offerteaanvraag komen in Mijn Klop > Configuraties, met een link terug.

Andere merken (algemene configurator):
- Alle boten met configurator (niet meer de eerste 60), Maxima-boten springen naar de Maxima-configurator.
- Opties per soort boot: sloep, elektrische sloep, open boot of RIB, sportboot, cruiser of yacht.
- Samenstelling in de adresbalk (#/stel-samen/<id>?k=..&m=..&i=..&o=..&h=..), bewaren en offerte naar Mijn Klop.
"""
import sys
p = sys.argv[1]
s = open(p, encoding='utf-8').read()
if 'function cfgStore(' in s:
    raise SystemExit('al gepatcht')
if 'var MXC=' not in s:
    raise SystemExit('eerst patch_maxima.py toepassen')

def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit('anchor count %d != %d for: %s' % (n, count, old[:100]))
    s = s.replace(old, new)

CSS = r"""
/* ===== Configurator ===== */
html.pg-cfg #foot,html.pg-cfg .mbar,html.pg-cfg #wa,html.pg-cfg .wa,html.pg-cfg .sprog{display:none!important}
html.pg-cfg body{padding-bottom:0!important;overflow:hidden}
.mxapp{padding-top:var(--nav);background:#fff}
.mxbar{border-bottom:1px solid var(--mist);background:#fff}
.mxbar .wrap{display:flex;align-items:center;gap:clamp(10px,2vw,24px);min-height:56px;padding-top:6px;padding-bottom:6px}
.mxbar .mxback{display:inline-flex;align-items:center;gap:8px;text-decoration:none;font-size:14.5px;color:var(--staal);white-space:nowrap}
.mxbar .mxback:hover{color:var(--nacht)}
.mxbar .mxback svg{width:16px;height:10px;fill:none;stroke:currentColor;stroke-width:1.3}
.mxbar .mxt{flex:1;min-width:0;display:flex;align-items:baseline;gap:10px;font-size:15px;white-space:nowrap;overflow:hidden}
.mxbar .mxt b{font-weight:500}.mxbar .mxt span{color:var(--staal);overflow:hidden;text-overflow:ellipsis}
.mxbar .mxsave{display:inline-flex;align-items:center;gap:8px;min-height:38px;padding:0 16px;border-radius:999px;border:1px solid var(--nacht);font-size:14px;font-weight:500;white-space:nowrap;transition:background .3s,color .3s,opacity .3s}
.mxbar .mxsave:hover:not([disabled]){background:var(--nacht);color:#fff}
.mxbar .mxsave[disabled]{opacity:.35;cursor:default}
.mxbar .mxsave svg{width:16px;height:16px;fill:none;stroke:currentColor;stroke-width:1.4}
.mxapp iframe{display:block;width:100%;height:calc(100svh - 160px);border:0;background:#f6f4f1}
.cfgmx{display:inline-flex;align-items:center;gap:6px;font-size:12px;letter-spacing:.04em;font-weight:500;color:var(--nacht);background:var(--mist);border-radius:999px;padding:2px 10px;margin-left:8px;vertical-align:middle}
.mkc a{color:inherit;text-decoration:none}.mkc .act{display:flex;gap:14px;align-items:center;margin-top:6px;font-size:14px}
.mkc .act a{text-decoration:underline;text-underline-offset:3px}.mkc .act button{font-size:14px;color:var(--staal);text-decoration:underline;text-underline-offset:3px}
@media(max-width:760px){.mxbar .mxback span,.mxbar .mxt b{display:none}.mxbar .mxsave span{display:none}.mxbar .mxsave{padding:0 12px}}
"""
i = s.find('</style>')
s = s[:i] + CSS + s[i:]

# ---------- 1. Maxima: schermvullende configuratorpagina ----------
start = s.index("function pCfgMx(slug){")
end = s.index("</section>'}", start) + len("</section>'}")
s = s[:start] + r"""function pCfgMx(slug){if(slug&&!MXN[slug]){var c=Object.keys(MXN).filter(function(k){return k.indexOf(slug+'-')===0});slug=c.filter(function(k){return!/elektr|electr/.test(k)})[0]||c[0]||''}
var n=slug&&MXN[slug],qs=new URLSearchParams(dec().split('?')[1]||''),q=[];if(n)q.push('model='+encodeURIComponent(slug));['c','ral','stap'].forEach(function(k){if(qs.get(k))q.push(k+'='+encodeURIComponent(qs.get(k)))});q.push('embed=1');MXS=null;
return'<section class="mxapp"><div class="mxbar"><div class="wrap"><a class="mxback" href="#/stel-samen"><svg viewBox="0 0 20 12"><path d="M20 6H2M6 1 1 6l5 5"/></svg><span>Stel samen</span></a><span class="mxt"><b>Maxima Boats</b><span id="mxname">'+(n?mxEsc(n):'Kies een model')+'</span></span><button class="mxsave" id="mxsave" data-a="mxsave"'+(n?'':' disabled')+'><svg viewBox="0 0 24 24"><path d="M6 3h12v18l-6-4-6 4z"/></svg><span>Bewaar in Mijn Klop</span></button></div></div><iframe id="mxf" src="'+MXC+'?'+q.join('&')+'" title="'+(n?mxEsc(n):'Maxima')+' configurator" allow="clipboard-write"></iframe></section>'}
var MXS=null;
function mxFit(){var f=document.getElementById('mxf');if(!f)return;f.style.height=Math.max(420,innerHeight-f.getBoundingClientRect().top-(window.scrollY||0))+'px'}
addEventListener('resize',mxFit);
function mxPick(re){if(!MXS||!MXS.picks)return'';var x=MXS.picks.filter(function(p){return re.test(p[0])})[0];return x?x[2]:''}
function cfgStore(o,st){var ex=-1;S.cfgs.forEach(function(c,i){if(c.url&&c.url.split('?')[0]===o.url.split('?')[0])ex=i});o.st=st;o.d=Date.now();if(ex>-1)S.cfgs[ex]=o;else S.cfgs.push(o);save('cfgs')}
function mxStore(st){if(!MXS)return;var q=[];if(MXS.c)q.push('c='+MXS.c);if(MXS.ral)q.push('ral='+MXS.ral);cfgStore({naam:MXS.name,kleur:mxPick(/romp/)||'Maxima Boats',motor:mxPick(/motor/)||(MXS.complete?'Compleet':'Nog niet compleet'),tot:MXS.total,url:'/stel-samen/'+MXS.slug+(q.length?'?'+q.join('&'):''),mx:1},st)}
addEventListener('message',function(e){var d=e.data,f=document.getElementById('mxf');if(!d||d.source!=='klop-mx'||!f||e.source!==f.contentWindow)return;
if(d.type==='overview'){MXS=null;$('#mxname').textContent='Kies een model';$('#mxsave').disabled=true;curH=enc('/stel-samen/maxima');try{history.replaceState(null,'','#'+curH)}catch(x){}}
else if(d.type==='state'){var first=!MXS||MXS.slug!==d.slug;MXS=d;$('#mxname').textContent=d.name+' · '+eur(d.total);$('#mxsave').disabled=false;var q=[];if(d.c)q.push('c='+d.c);if(d.ral)q.push('ral='+d.ral);if(d.stap)q.push('stap='+d.stap);curH=enc('/stel-samen/'+d.slug+(q.length?'?'+q.join('&'):''));try{history.replaceState(null,'','#'+curH)}catch(x){}if(first)document.title='Stel je '+d.name+' samen | Klop Watersport'}
else if(d.type==='quote'){mxStore('Offerte aangevraagd');toast('Je aanvraag staat ook in Mijn Klop bij Configuraties.',1)}});""" + s[end:]

# html-klasse + passende hoogte voor de configuratorpagina
rep("function afterRender(path){srInit();", "function afterRender(path){srInit();document.documentElement.classList.toggle('pg-cfg',/^\\/stel-samen\\/maxima/.test(path)||(/^\\/stel-samen\\/\\d+$/.test(path)&&!!MXMAP[path.split('/')[2]]));setTimeout(mxFit,0);")

# ---------- 2. Algemene configurator ----------
# alle boten met configurator
rep("function cfgList(){return BOATS.filter(function(b){return b.cfg&&b.prijs&&b.staat==='Nieuw'}).slice(0,60)}",
    "function cfgList(){return BOATS.filter(function(b){return b.cfg&&b.prijs&&b.staat==='Nieuw'})}")
# opties per soort boot (prijzen zijn een indicatie, zoals al op de pagina staat)
OPTS = r"""
var OPTT={
sloep:{motor:[['Standaard motor','Zoals in de basisprijs',0],['Krachtiger motor','Meer vermogen voor groter water',4200],['Elektrisch (E-propulsion)','Stil en onderhoudsarm',9800]],intr:[['Standaard','Praktisch en onderhoudsarm',0,'#C9CED3'],['Teakvloer','Teak look in de kuip',2400,'#B98B52'],['Foam vloer','Comfortabel en slipvrij',1800,'#7A8794']],opties:[['Boegschroef',2200],['Buiskap',1450],['Bluetooth audio met speakers',890],['Kussenset luxe stof',1250],['Tafel met teak blad',690],['Kuipverlichting',540],['Koellade',780],['Zonnedek-kussens voor',950]]},
elek:{motor:[['Standaard elektromotor','Zoals in de basisprijs',0],['Groter accupakket','Langer varen op één lading',6500],['Krachtiger elektromotor','Meer reserve op stroming',4800]],intr:[['Standaard','Praktisch en onderhoudsarm',0,'#C9CED3'],['Teakvloer','Teak look in de kuip',2400,'#B98B52'],['Foam vloer','Comfortabel en slipvrij',1800,'#7A8794']],opties:[['Snellader',1900],['Walstroomaansluiting',640],['Buiskap',1450],['Bluetooth audio met speakers',890],['Kussenset luxe stof',1250],['Tafel met teak blad',690],['Kuipverlichting',540],['Boegschroef',2200]]},
open:{motor:[['Standaard motor','Zoals in de basisprijs',0],['Krachtiger motor','Meer vermogen',4200],['Topmotorisering','Maximaal toegestaan vermogen',8900]],intr:[['Standaard','Praktisch en onderhoudsarm',0,'#C9CED3'],['Foam vloer','Comfortabel en slipvrij',1800,'#7A8794'],['Teakvloer','Teak look',2400,'#B98B52']],opties:[['Bimini',1150],['T-top',3400],['Kussenset zonnedek',950],['Bluetooth audio met speakers',890],['Fishfinder met GPS',1290],['Ski-paal',420],['Afdekhoes',690],['Kuipverlichting',540]]},
rib:{motor:[['Standaard motor','Zoals in de basisprijs',0],['Krachtiger motor','Meer vermogen',4200],['Topmotorisering','Maximaal toegestaan vermogen',8900]],intr:[['Standaard','Praktisch en onderhoudsarm',0,'#C9CED3'],['Foam vloer','Comfortabel en slipvrij',1800,'#7A8794'],['Teakvloer','Teak look',2400,'#B98B52']],opties:[['Bimini',1150],['T-top',3400],['Zitkussen consolebank',690],['Bluetooth audio met speakers',890],['Fishfinder met GPS',1290],['Ski-paal',420],['Afdekhoes',690],['Navigatieverlichting LED',380]]},
cab:{motor:[['Standaard motorisering','Zoals in de basisprijs',0],['Krachtiger motorisering','Meer vermogen en reserve',9800],['Dubbele motorisering','Meer vermogen en zekerheid',24500]],intr:[['Standaard','Zoals in de basisprijs',0,'#C9CED3'],['Teakvloer kuip','Teak look in de kuip',3900,'#B98B52'],['Luxe interieur','Leder en extra afwerking',6200,'#7A8794']],opties:[['Boegschroef',3200],['Walstroom met lader',1450],['Koelkast',1180],['Navigatie met plotter',2950],['Bluetooth audio met speakers',890],['Ankerlier',2100],['Kuipverlichting',540],['Warmwaterboiler',1350]]}};
function optKey(b){var t=b&&b.type;if(t==='Elektrische sloep')return'elek';if(t==='Sloep')return'sloep';if(t==='RIB')return'rib';if(t==='Sportcruiser'||t==='Yacht'||t==='Kajuitboot')return'cab';return'open'}
function OF(){var o=OPTT[optKey(boat(C.cid))];return{kleur:OPT.kleur,motor:o.motor,intr:o.intr,opties:o.opties}}
function cfgQ(){return'k='+C.kleur+'&m='+C.motor+'&i='+C.intr+'&h='+C.haven+(C.opt.length?'&o='+C.opt.join('.'):'')}
function cfgSync(){if(dec().indexOf('/stel-samen')!==0)return;curH=enc('/stel-samen/'+C.cid+'?'+cfgQ());try{history.replaceState(null,'','#'+curH)}catch(x){}}
function cfgSave(st){var b=boat(C.cid),o=OF();if(!b)return;cfgStore({naam:b.naam,kleur:'Romp '+o.kleur[C.kleur][0].toLowerCase(),motor:o.motor[C.motor][0],tot:ctot(),url:'/stel-samen/'+C.cid+'?'+cfgQ()},st)}
"""
rep("function ctot(){var b=boat(C.cid);if(!b)return 0;var t=b.prijs+OPT.motor[C.motor][2]+OPT.kleur[C.kleur][2]+OPT.intr[C.intr][2];C.opt.forEach(function(i){t+=OPT.opties[i][1]});return t}",
    OPTS + "function ctot(){var b=boat(C.cid);if(!b)return 0;var O=OF(),t=b.prijs+O.motor[C.motor][2]+O.kleur[C.kleur][2]+O.intr[C.intr][2];C.opt.forEach(function(i){if(O.opties[i])t+=O.opties[i][1]});return t}")

# cfgRender: opties uit OF() i.p.v. vaste OPT
i = s.index('function cfgRender(){')
j = s.index('/* ---------- Klop Premium Service ---------- */', i)
body = s[i:j]
body = body.replace('function cfgRender(){var b=boat(C.cid),s=C.stap,body=\'\';', 'function cfgRender(){var b=boat(C.cid),s=C.stap,body=\'\',OPT=OF();cfgSync();', 1)
# bootkeuze: label bij Maxima-boten
body = body.replace("'<button class=\"opt'+(x.id===C.cid?' on':'')+'\" data-a=\"cboot\" data-id=\"'+x.id+'\"><span><b>'+esc(x.naam)+'</b>",
                    "'<button class=\"opt'+(x.id===C.cid?' on':'')+'\" data-a=\"cboot\" data-id=\"'+x.id+'\"><span><b>'+esc(x.naam)+(MXMAP[x.id]?'<i class=\"cfgmx\">Maxima-configurator</i>':'')+'</b>", 1)
assert 'OPT=OF()' in body and 'cfgmx' in body
s = s[:i] + body + s[j:]

# pCfg: samenstelling uit de adresbalk terugzetten
rep("function pCfg(id){var l=cfgList();if(id&&boat(id))C.cid=+id;if(!C.cid||!boat(C.cid)){C.cid=(l[0]||BOATS[0]).id}",
    "function pCfg(id){var l=cfgList();if(id&&boat(id)){if(+id!==C.cid){C.motor=0;C.intr=0;C.opt=[]}C.cid=+id}if(!C.cid||!boat(C.cid)){C.cid=(l[0]||BOATS[0]).id}"
    "var qs=new URLSearchParams(dec().split('?')[1]||'');if(qs.has('k')){var O=OF(),nm=function(k,n){var v=parseInt(qs.get(k),10);return v>=0&&v<n?v:0};C.kleur=nm('k',O.kleur.length);C.motor=nm('m',O.motor.length);C.intr=nm('i',O.intr.length);C.haven=qs.get('h')==='eigen'?'eigen':'klop';C.opt=(qs.get('o')||'').split('.').filter(function(x){return x!==''&&+x<O.opties.length}).map(Number)}")

# handlers
rep("else if(a==='cboot'){C.cid=id;cfgRender()}",
    "else if(a==='cboot'){if(MXMAP[id]){go('#/stel-samen/'+MXMAP[id]);return}if(id!==C.cid){C.motor=0;C.intr=0;C.opt=[]}C.cid=id;cfgRender()}")
rep("else if(a==='csave'){var b2=boat(C.cid);S.cfgs.push({naam:b2.naam,kleur:OPT.kleur[C.kleur][0],motor:OPT.motor[C.motor][0],tot:ctot()});save('cfgs');toast('Configuratie bewaard in Mijn Klop.',1)}",
    "else if(a==='csave'){cfgSave('Bewaard');toast('Configuratie bewaard in Mijn Klop.',1)}\n"
    "else if(a==='mxsave'){mxStore('Bewaard');toast('Configuratie bewaard in Mijn Klop.',1)}\n"
    "else if(a==='cfgdel'){S.cfgs.splice(+t.dataset.i,1);save('cfgs');lastPath='';route()}")
rep("else if(f.id==='bf'||f.id==='cf'||f.id==='of'){",
    "else if(f.id==='bf'||f.id==='cf'||f.id==='of'){if(f.id==='of')cfgSave('Offerte aangevraagd');")

# Mijn Klop: configuraties met status, link terug en verwijderen
rep("'<li><div><b>'+esc(c.naam)+'</b><small>'+esc(c.kleur)+' · '+esc(c.motor)+'</small></div><b>'+eur(c.tot)+'</b></li>'",
    "'<li class=\"mkc\"><div><b>'+(c.url?'<a href=\"#'+esc(c.url)+'\">'+esc(c.naam)+'</a>':esc(c.naam))+'</b><small>'+esc(c.kleur)+' · '+esc(c.motor)+(c.st?' · '+esc(c.st):'')+'</small>'+'<div class=\"act\">'+(c.url?'<a href=\"#'+esc(c.url)+'\">Verder samenstellen</a>':'')+'<button data-a=\"cfgdel\" data-i=\"'+i+'\">Verwijder</button></div></div><b>'+eur(c.tot)+'</b></li>'", 2)
rep("S.cfgs.map(function(c){return'<li class=\"mkc\">", "S.cfgs.map(function(c,i){return'<li class=\"mkc\">", 2)

open(p, 'w', encoding='utf-8').write(s)
print('ok: configurator afgemaakt')
