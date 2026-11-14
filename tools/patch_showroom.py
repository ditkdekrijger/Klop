"""Patch: meer oog voor de showroom op de homepage + rijkere showroompagina."""
import sys
p = sys.argv[1]
s = open(p, encoding='utf-8').read()

def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit('anchor count %d != %d for: %s' % (n, count, old[:80]))
    s = s.replace(old, new)

CSS = r"""
/* ===== Showroom (home + pagina) ===== */
.hsr{display:inline-flex;align-items:center;gap:14px;margin-top:26px;border-radius:999px;color:#fff;text-decoration:none;font-size:15px;padding:10px 16px 10px 12px;border:1px solid rgba(255,255,255,.28);background:rgba(11,25,48,.35);backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px);transition:border-color .4s var(--ez),background .4s var(--ez)}
.hsr i{width:9px;height:9px;border-radius:50%;background:#fff;box-shadow:0 0 0 0 rgba(255,255,255,.6);animation:hsrp 2.4s var(--ez) infinite}
.hsr b{font-weight:500;border-left:1px solid rgba(255,255,255,.28);padding-left:14px}
.hsr:hover{border-color:#fff;background:rgba(11,25,48,.6)}
@keyframes hsrp{0%{box-shadow:0 0 0 0 rgba(255,255,255,.5)}70%{box-shadow:0 0 0 10px rgba(255,255,255,0)}100%{box-shadow:0 0 0 0 rgba(255,255,255,0)}}
.srh{position:relative;overflow:hidden}
.srh-h{display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);gap:clamp(28px,5vw,88px);align-items:end;margin-bottom:clamp(32px,4vw,56px)}
.srh-h h2{margin-top:16px}.srh-h h2 span{color:var(--chroom)}
.srtour{position:relative}
.srtour-v{position:relative;aspect-ratio:16/8;overflow:hidden;border-radius:6px;background:var(--diep)}
.srtour-v .im{position:absolute;inset:0;background-size:cover;background-position:50% 50%;opacity:0;transform:scale(1.06);transition:opacity 1.1s var(--ez),transform 7s linear}
.srtour-v .im.on{opacity:1;transform:scale(1)}
.srtour-v:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(11,25,48,0) 30%,rgba(11,25,48,.78) 100%);pointer-events:none}
.srtour-c{position:absolute;left:clamp(18px,3vw,40px);bottom:clamp(18px,3vw,36px);right:clamp(18px,3vw,40px);z-index:2;color:#fff;display:grid;gap:6px;max-width:620px}
.srtour-c small{font-size:13px;letter-spacing:.12em;color:var(--olie);font-weight:500}
.srtour-c b{font-family:var(--f-d);font-weight:300;font-size:clamp(28px,3.4vw,48px);letter-spacing:-.035em;line-height:1.02}
.srtour-c span{font-size:clamp(15px,1.3vw,18px);color:var(--mist);line-height:1.5}
.srtour-s{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:0 clamp(10px,1.6vw,24px);margin-top:18px}
.srtour-s button{text-align:left;padding:14px 0 6px;font-size:15px;color:var(--staal);display:grid;gap:4px;transition:color .3s}
.srtour-s button small{font-size:12px;letter-spacing:.1em;opacity:.8}
.srtour-s button i{display:block;height:2px;background:var(--mist);position:relative;overflow:hidden;margin-bottom:8px}
.srtour-s button i em{position:absolute;inset:0;background:var(--nacht);transform:scaleX(0);transform-origin:left}
.srtour-s button.on{color:var(--nacht)}
.srtour-s button.on i em{transform:scaleX(1)}
.srtour.run .srtour-s button.on i em{transform:scaleX(0);animation:srp 6s linear forwards}
@keyframes srp{to{transform:scaleX(1)}}
.srtour-s button:hover{color:var(--nacht)}
.dark .srtour-s button{color:var(--chroom)}.dark .srtour-s button i{background:rgba(255,255,255,.16)}.dark .srtour-s button i em{background:var(--olie)}
.dark .srtour-s button.on,.dark .srtour-s button:hover{color:#fff}
.srh-f{display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);gap:clamp(28px,5vw,88px);margin-top:clamp(44px,5vw,72px);padding-top:clamp(28px,3vw,40px);border-top:1px solid rgba(255,255,255,.14)}
.srh-f small{display:block;font-size:14px;color:var(--chroom);margin-bottom:16px}
.srh-ty{display:flex;flex-wrap:wrap;gap:10px}
.srh-ty a{display:inline-flex;align-items:center;gap:12px;text-decoration:none;padding:8px 8px 8px 18px;border-radius:999px;border:1px solid rgba(255,255,255,.22);font-size:15px;color:#fff;transition:border-color .3s,background .3s}
.srh-ty a b{font-family:var(--f-d);font-weight:400;font-size:15px;min-width:28px;height:28px;padding:0 6px;display:inline-grid;place-items:center;border-radius:999px;background:rgba(255,255,255,.1)}
.srh-ty a:hover{border-color:var(--olie);background:rgba(239,169,31,.08)}
.srh-ty.lt a{color:var(--nacht);border-color:rgba(11,25,48,.18);background:#fff}.srh-ty.lt a b{background:var(--gel)}
.srh-ty.lt a:hover{border-color:var(--nacht)}
.srh-ad b{display:block;font-family:var(--f-d);font-weight:300;font-size:clamp(28px,2.6vw,38px);letter-spacing:-.03em;line-height:1.05}
.srh-ad span{display:block;color:var(--mist);margin-top:6px}
.srh .btn:not(.solid){--bd:rgba(255,255,255,.4);color:#fff;--dv:rgba(255,255,255,.28)}
.srh .btn:not(.solid):before{background:#fff}.srh .btn:not(.solid):hover{color:var(--nacht);--dv:rgba(11,25,48,.22)}
.srs{margin-top:8px}
.srs>div{border-top:1px solid var(--nacht);padding-top:18px}
.srs small{font-size:13px;letter-spacing:.1em;color:var(--staal)}
.srs h3{margin:10px 0 10px}
.srv{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(20px,2.4vw,32px);margin-top:clamp(28px,3vw,44px)}
@media(max-width:900px){.srh-h,.srh-f{grid-template-columns:1fr}.srtour-v{aspect-ratio:4/3}.srtour-s{display:flex;overflow-x:auto;scrollbar-width:none;gap:18px}.srtour-s::-webkit-scrollbar{display:none}.srtour-s button{flex:0 0 42%}.srv{grid-template-columns:1fr}}
@media(max-width:560px){.hsr b{display:none}.srtour-s button{flex-basis:62%}}
@media(prefers-reduced-motion:reduce){.hsr i{animation:none}.srtour-v .im{transition:opacity .2s}.srtour.run .srtour-s button.on i em{animation:none;transform:scaleX(1)}}
"""

i = s.find('</style>')
s = s[:i] + CSS + s[i:]

JS = r"""
/* ---------- showroom: rondleiding en voorraad ---------- */
var SR=[['g12','De showroom','Nieuwe en gebruikte boten onder één dak, achter glas aan het water. Stap aan boord en neem de tijd.'],['g08','De hal','Ruimte om rond te lopen, in te stappen en de boten van dichtbij te bekijken. Ook bij slecht weer.'],['g06','De werkplaats','Eigen monteurs, eigen werkplaats. Hier wordt je boot afgeleverd, onderhouden en klaargemaakt voor het seizoen.'],['g07','De servicehaven','Vanaf onze eigen steiger direct het water op. Zo vaar je de boot eerst zelf, voordat je beslist.'],['g11','Aan de rivier','Buitendijks aan de Rivierdijk in Hardinxveld-Giessendam, met het water voor de deur.']];
var SRI=0,SRT=null;
function srVoorraad(){var c={};BOATS.forEach(function(b){if(b.voorraad)c[b.type]=(c[b.type]||0)+1});return TYPES.filter(function(t){return c[t[0]]}).map(function(t){return'<a href="#/boten/'+slug(t[0])+'"><span>'+t[1]+'</span><b>'+c[t[0]]+'</b></a>'}).join('')}
function srTour(){return'<div class="srtour rv" id="srt"><div class="srtour-v">'+SR.map(function(x,i){return'<div class="im i-'+x[0]+(i?'':' on')+'" role="img" aria-label="'+esc(x[1])+'"></div>'}).join('')+'<div class="srtour-c" aria-live="polite"><small id="srn">01 / 0'+SR.length+'</small><b id="srh">'+SR[0][1]+'</b><span id="srp">'+SR[0][2]+'</span></div></div><div class="srtour-s" role="tablist" aria-label="Rondleiding door de showroom">'+SR.map(function(x,i){return'<button data-a="srt" data-i="'+i+'" role="tab" aria-selected="'+(!i)+'"'+(i?'':' class="on"')+'><i><em></em></i><small>0'+(i+1)+'</small>'+x[1]+'</button>'}).join('')+'</div></div>'}
function srGo(i,user){var r=document.getElementById('srt');if(!r)return;SRI=i;$$('#srt .srtour-v .im').forEach(function(e,j){e.classList.toggle('on',j===i)});$$('#srt .srtour-s button').forEach(function(b,j){b.classList.toggle('on',j===i);b.setAttribute('aria-selected',j===i)});$('#srn').textContent='0'+(i+1)+' / 0'+SR.length;$('#srh').textContent=SR[i][1];$('#srp').textContent=SR[i][2];if(user){r.classList.add('man');r.classList.remove('run');clearTimeout(SRT)}else srPlay()}
function srPlay(){clearTimeout(SRT);var r=document.getElementById('srt');if(!r||r.classList.contains('man')||REDUCED0)return;r.classList.remove('run');void r.offsetWidth;r.classList.add('run');SRT=setTimeout(function(){if(document.getElementById('srt')===r)srGo((SRI+1)%SR.length)},6000)}
function srInit(){SRI=0;clearTimeout(SRT);if(document.getElementById('srt'))srPlay()}
function showroomHome(){var n=BOATS.filter(function(b){return b.voorraad}).length;
return'<section class="srh dark" id="showroom"><div class="wrap sec"><div class="srh-h"><div>'+lbl('De showroom')+'<h2>4.000 m² aan het water.<br><span>Kom kijken, voelen en varen.</span></h2></div><p class="lead">Een boot koop je niet van een foto. In onze showroom aan de Rivierdijk stap je aan boord, voel je het hout en vaar je vanaf onze eigen steiger meteen het water op. Een Vrijheidsvaarder loopt met je mee.</p></div>'+srTour()+'<div class="srh-f"><div><small>Nu in de showroom · '+n+' boten op voorraad</small><div class="srh-ty">'+srVoorraad()+'</div></div><div class="srh-ad"><small>Bezoekadres</small><b>'+CONTACT.adres+'</b><span>'+CONTACT.plaats+'</span><div class="btns" style="margin-top:24px">'+btn('Plan je bezoek','#/bezoek','solid')+btn('Meer over de showroom','#/showroom')+'</div></div></div></div></section>'}
"""

# 1. JS helpers voor pHome
rep('\nfunction pHome(){', JS + '\nfunction pHome(){')
# 2. Showroom-sectie op de homepage, direct na merkenband en voor de voorraad
rep("+'<section class=\"sec\"><div class=\"wrap\"><div class=\"head\"><div>'+lbl('Direct varen')",
    "+showroomHome()\n+'<section class=\"sec\"><div class=\"wrap\"><div class=\"head\"><div>'+lbl('Direct varen')")
# 3. Hero: showroom-link
rep("btn('<span class=\"pe\"></span>Klop Premium Service™','#/klop-premium-service','prem')+'</div></div><div class=\"scroll\">",
    "btn('<span class=\"pe\"></span>Klop Premium Service™','#/klop-premium-service','prem')+'</div><a class=\"hsr\" href=\"#/#showroom\"><i></i><span>4.000 m² showroom aan de Rivierdijk</span><b>Kom kijken</b></a></div><div class=\"scroll\">")
# 4. Klik-handler
rep("else if(a==='hs'){", "else if(a==='srt'){srGo(+t.dataset.i,1)}\nelse if(a==='hs'){")
# 5. afterRender
rep('function afterRender(path){', 'function afterRender(path){srInit();')
# 6. Showroompagina
i = s.find('\nfunction pShow(){')
j = s.find('\n', i + 5)
NEW_SHOW = r"""
function pShow(){var vo=BOATS.filter(function(b){return b.voorraad&&b.prijs}).slice(0,6),n=BOATS.filter(function(b){return b.voorraad}).length;return'<section class="phead"><div class="wrap">'+lbl('Showroom')+'<h1>Kom langs aan de Rivierdijk.</h1><p class="lead">4.000 m² showroom aan het water, met werkplaats en servicehaven ernaast. Eén afspraak en een Vrijheidsvaarder staat voor je klaar.</p><div class="btns" style="margin-top:30px">'+btn('Plan een bezoek of proefvaart','#/bezoek','solid')+btn('Contact en route','#/contact')+'</div></div></section>'
+'<section class="sec tight" style="padding-top:0"><div class="wrap">'+srTour()+'<div class="cols3 srs" style="margin-top:clamp(48px,6vw,88px)"><div><small>01</small><h3>Kijken en voelen</h3><p class="mut">Stap aan boord, zit achter het stuur en vergelijk de boten naast elkaar. Zonder haast.</p></div><div><small>02</small><h3>Proefvaren</h3><p class="mut">Vanaf onze eigen steiger direct het water op. Jij vaart, wij varen mee.</p></div><div><small>03</small><h3>Werkplaats en service</h3><p class="mut">Zie waar je boot wordt onderhouden en ontmoet de mensen van Klop Premium Service™.</p></div></div></div></section>'
+'<section class="sec" style="background:var(--mist)"><div class="wrap"><div class="head"><div>'+lbl('Nu in de showroom')+'<h2>'+n+' boten op voorraad.</h2></div><a class="tlink" href="#/boten">Alle boten</a></div><div class="srh-ty lt">'+srVoorraad()+'</div><div class="srv">'+vo.map(function(b,i){return card(b,i)}).join('')+'</div></div></section>'
+'<section class="sec tight"><div class="wrap"><div class="two-col" style="align-items:start"><div><h3>Adres</h3><p style="margin:10px 0 24px">'+CONTACT.adres+'<br>'+CONTACT.plaats+'</p><h3>Contact</h3><p style="margin-top:10px"><a class="tlink" href="tel:+31184612227">'+CONTACT.tel+'</a><br><a class="tlink" href="'+CONTACT.wal+'">WhatsApp '+CONTACT.wa+'</a><br><a class="tlink" href="mailto:'+CONTACT.mail+'">'+CONTACT.mail+'</a></p></div><div>'+ph('g11','','De showroom aan de dijk')+'</div></div></div></section>'}"""
s = s[:i] + NEW_SHOW + s[j:]

open(p, 'w', encoding='utf-8').write(s)
print('ok')
