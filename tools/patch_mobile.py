"""Patch: mobiele UX. Toepassen na patch_showroom.py."""
import sys
p = sys.argv[1]
s = open(p, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: raise SystemExit('anchor %d != %d: %s' % (n, count, old[:90]))
    s = s.replace(old, new)

CSS = r"""
/* ===== Mobiel ===== */
.hscroll{scrollbar-width:none}.hscroll::-webkit-scrollbar{display:none}
@media(max-width:760px){
/* algemeen: ruimte voor de actiebalk onderin */
body{padding-bottom:calc(66px + env(safe-area-inset-bottom))}
.mbar{padding-bottom:env(safe-area-inset-bottom)}
html.pg-boot .mbar{display:none!important}
html.pg-boot body{padding-bottom:calc(76px + env(safe-area-inset-bottom))}
.sec{padding:56px 0}.sec.tight{padding:40px 0}
.head{margin-bottom:24px}
h2{font-size:clamp(30px,8.4vw,40px)}
.lead{font-size:17px}
/* horizontale scrollrijen */
.hscroll{display:flex!important;overflow-x:auto;scroll-snap-type:x mandatory;gap:12px!important;margin:0 calc(var(--pad)*-1);padding:0 var(--pad) 6px;scroll-padding:0 var(--pad)}
.hscroll>*{flex:0 0 82%;scroll-snap-align:start;min-width:0}
/* hero */
.hero{min-height:92svh}
.hero .in{padding-top:calc(var(--nav) + 40px);padding-bottom:40px}
.hero .bg:after{background:linear-gradient(180deg,rgba(11,25,48,.55) 0%,rgba(11,25,48,.15) 30%,rgba(11,25,48,.55) 60%,rgba(11,25,48,.92) 100%)}
.hero .lbl{font-size:13px}
.hero .sub{font-size:17px;margin:18px 0 24px}
.hero .btns{display:grid;grid-template-columns:1fr;gap:10px}
.hero .btns .btn{width:100%}
.hsr{display:flex;width:100%;justify-content:center;margin-top:12px;font-size:14px}
.hero .scroll{display:none}
/* vaardersvinder: elke vraag als één veegrij */
.finder .chips{display:flex!important;flex-wrap:nowrap!important;overflow-x:auto;gap:8px;scrollbar-width:none;scroll-snap-type:x proximity;padding-bottom:4px}
.finder .chips::-webkit-scrollbar{display:none}
.finder .chip.tile{flex:0 0 auto;min-width:112px;scroll-snap-align:start}
/* bewijs */
.bewijs>div{padding:22px 12px 22px 0!important}.bewijs>div+div{padding-left:16px!important}
.bewijs b{font-size:38px}.bewijs small{font-size:14px;margin-top:6px}
/* showroom */
.srh .sec{padding-top:56px;padding-bottom:56px}
.srh-h{gap:16px;margin-bottom:24px}
.srtour-v{aspect-ratio:4/5!important;border-radius:14px}
.srtour-c b{font-size:30px}
.srtour-s button{flex:0 0 46%!important;scroll-snap-align:start}
.srtour-s{scroll-snap-type:x mandatory}
.srh-f{gap:28px;margin-top:32px}
.srh-ty{flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none;margin:0 calc(var(--pad)*-1);padding:0 var(--pad) 4px}
.srh-ty::-webkit-scrollbar{display:none}.srh-ty a{flex:0 0 auto}
.srh-ad .btns{display:grid;grid-template-columns:1fr;gap:10px}.srh-ad .btn{width:100%}
.srtour .swipe{display:block}
/* merken compact */
.merken{grid-template-columns:repeat(3,1fr)!important}
.merken a{min-height:84px!important;padding:14px 10px!important;gap:6px!important;justify-content:center}
.merken small{display:none}
.merken .bmw{min-height:28px!important;margin:0!important}.merken .bmw .bm{max-height:26px!important}
.merken .mfill{grid-column:1/-1;min-height:0!important;padding:20px!important}
.merken .mfill small{display:block}
/* bootpagina */
#snav2 .sp,#snav2 .mut{display:none!important}
#snav2 .wrap{flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none}
#snav2 a{white-space:nowrap}
.mcta{display:flex!important;padding:10px var(--pad) calc(10px + env(safe-area-inset-bottom))}
.mcta b{font-size:20px;font-family:var(--f-d);font-weight:400;display:block;line-height:1.1}
.mcta small{display:block;font-size:13px;max-width:52vw;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.zg-t{display:flex!important;overflow-x:auto;scroll-snap-type:x mandatory;gap:12px;margin:0 calc(var(--pad)*-1);padding:0 var(--pad) 6px;scrollbar-width:none}
.zg-t::-webkit-scrollbar{display:none}
.zg-t .zt{flex:0 0 78%;scroll-snap-align:start;min-width:0}
.dna4{display:flex!important;overflow-x:auto;scroll-snap-type:x mandatory;gap:12px;scrollbar-width:none;margin:0 calc(var(--pad)*-1);padding:0 var(--pad) 6px}
.dna4::-webkit-scrollbar{display:none}.dna4>*{flex:0 0 78%;scroll-snap-align:start}
/* aanbodlijst */
.lc-ph{aspect-ratio:16/10!important;height:auto!important;min-height:0!important}
.lc h3{white-space:normal!important;overflow:visible!important}
.lc-sp{display:grid!important;grid-template-columns:1fr 1fr;gap:10px 12px!important;overflow:visible!important}
.lc-sp li{min-width:0}
.srt{margin-left:calc(var(--pad)*-1);margin-right:calc(var(--pad)*-1);padding-left:var(--pad);padding-right:var(--pad)}
/* footer korter */
footer .wrap{row-gap:28px}
/* correcties */
.lay,.lay>*,#lst,#lst>*{min-width:0;max-width:100%}.lc{width:100%;max-width:100%}
.srh-f>*,.srh-h>*{min-width:0}
.merken a{overflow:hidden}.merken .bmw{max-width:100%;overflow:hidden;font-size:13px!important;white-space:nowrap;text-overflow:ellipsis}
.zg-g{grid-template-columns:1fr!important}.zg-g>*{min-width:0}
.lc{display:flex!important;flex-direction:column;grid-template-columns:none!important}.lc>*{min-width:0;max-width:100%}
.lc-ph{position:relative;display:block;width:100%;max-height:230px}
.lc h3,.lc h3 *{white-space:normal!important;text-overflow:clip!important}
.lc-sp li{overflow:hidden}.lc-sp b{font-size:15px}
.lc-p{display:flex!important;flex-direction:column!important;align-items:stretch!important;gap:14px;text-align:left!important}
.lc-pr{text-align:left!important}.lc-pr b{font-size:30px}
.lc-ac{display:grid!important;grid-template-columns:auto 1fr;gap:10px 14px;align-items:center}
.lc-ac>.btn{grid-column:1/-1;width:100%}.lc-ac>a:not(.btn){justify-self:end}
}
"""
i = s.find('</style>')
s = s[:i] + CSS + s[i:]

# html-klasse per pagina (bootpagina verbergt de algemene actiebalk)
rep('function afterRender(path){srInit();', "function afterRender(path){srInit();document.documentElement.classList.toggle('pg-boot',path.indexOf('/boot/')===0);")
# vegen door de showroom-rondleiding
rep("function srInit(){SRI=0;clearTimeout(SRT);if(document.getElementById('srt'))srPlay()}",
    "function srInit(){SRI=0;clearTimeout(SRT);var r=document.getElementById('srt');if(!r)return;srPlay();var v=r.querySelector('.srtour-v'),x0=null,y0=0;v.addEventListener('touchstart',function(e){x0=e.touches[0].clientX;y0=e.touches[0].clientY},{passive:true});v.addEventListener('touchend',function(e){if(x0===null)return;var dx=e.changedTouches[0].clientX-x0,dy=e.changedTouches[0].clientY-y0;x0=null;if(Math.abs(dx)>40&&Math.abs(dx)>Math.abs(dy))srGo((SRI+(dx<0?1:-1)+SR.length)%SR.length,1)},{passive:true})}")
# voorraad op showroompagina als veegrij
rep('<div class="srv">', '<div class="srv hscroll">')
# routes op home als veegrij
rep("<div class=\"cols3\">'+ROUTES.slice(0,3)", "<div class=\"cols3 hscroll\">'+ROUTES.slice(0,3)")
open(p, 'w', encoding='utf-8').write(s)
print('ok')
