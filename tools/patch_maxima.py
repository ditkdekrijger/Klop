"""Patch: Maxima-configurator 2.0 in de site.

- #/stel-samen/maxima            -> overzicht van alle Maxima-modellen (configurator in iframe)
- #/stel-samen/maxima-<model>    -> configurator voor dat model (was alleen maxima-760, via maxima.mustang.dev)
- #/stel-samen/<boot-id>         -> voor Maxima-boten de Maxima-configurator in plaats van de algemene
- "Stel samen" op de bootpagina van een Maxima-boot gaat direct naar het juiste model

De configurator zelf staat in maxima-configurator/public/ (eigen Maxima-huisstijl; het
designsysteem zegt dat Maxima geen Klop-opmaak krijgt). Pas MXC aan als hij elders gehost wordt.

Gebruik: python3 tools/patch_maxima.py site/index.html   (eenmalig; stopt als het al gepatcht is)
"""
import json
import sys

p = sys.argv[1]
s = open(p, encoding='utf-8').read()
if 'var MXC=' in s:
    raise SystemExit('al gepatcht')


def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit('anchor count %d != %d for: %s' % (n, count, old[:80]))
    s = s.replace(old, new)


# Boot-id op de site -> model in de configurator (maxima-configurator/public/data/<slug>.json).
# Maxima 485 en 730i zitten niet in de dealerconfigurator van Maxima en houden de algemene configurator.
MXMAP = {
    85: 'maxima-35-nieuw', 87: 'maxima-37-cabin', 92: 'maxima-490', 94: 'maxima-550',
    95: 'maxima-580-sport-lounge-nieuw', 96: 'maxima-600-nieuw', 100: 'maxima-620-retro-mc',
    103: 'maxima-630-nieuw', 109: 'maxima-640', 111: 'maxima-650-flying-lounge',
    114: 'maxima-680-sport-lounge', 117: 'maxima-700-sport', 119: 'maxima-720-retro', 124: 'maxima-730',
    129: 'maxima-740', 131: 'maxima-750-flying-lounge', 135: 'maxima-760-nieuw', 136: 'maxima-800-cabin',
    137: 'maxima-800-sport', 139: 'maxima-820-retro', 142: 'maxima-840', 145: 'maxima-920-cabin',
}
models = json.load(open('maxima-configurator/public/data/models.json', encoding='utf-8'))
names = {m['slug']: m['name'] for m in models}
missing = sorted(set(MXMAP.values()) - set(names))
if missing:
    raise SystemExit('onbekende modellen in MXMAP: %s' % missing)

# 1. Basis-URL, koppeltabel en helpers (vervangt de vaste Mustang-URL voor de 760)
rep("var MXU='https://maxima.mustang.dev/configurator/maxima-760-nieuw';",
    "var MXC='../maxima-configurator/public/';"
    "var MXMAP=" + json.dumps({str(k): v for k, v in MXMAP.items()}, separators=(',', ':')) + ";"
    "var MXN=" + json.dumps(names, ensure_ascii=False, separators=(',', ':')) + ";"
    "function mxHref(b){return MXMAP[b.id]?'#/stel-samen/'+MXMAP[b.id]:'#/stel-samen/'+b.id}"
    "function mxEsc(t){return String(t).replace(/[&<>\"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;'}[c]})}"
    "function mxSrc(slug){return MXC+'?'+(slug?'model='+encodeURIComponent(slug)+'&':'')+'embed=1'}")

# 2. Pagina: elk Maxima-model (of het overzicht) in de iframe
old_fn_start = "function pCfgMx(){return'"
i = s.index(old_fn_start)
j = s.index("</section>'}", i) + len("</section>'}")
if s.count(old_fn_start) != 1:
    raise SystemExit('pCfgMx niet uniek')
s = s[:i] + (
    "function pCfgMx(slug){if(slug&&!MXN[slug]){var c=Object.keys(MXN).filter(function(k){return k.indexOf(slug+'-')===0});"
    "slug=c.filter(function(k){return!/elektr|electr/.test(k)})[0]||c[0]||''}"
    "var n=slug&&MXN[slug],src=mxSrc(n?slug:'');"
    "return'<section class=\"phead\" style=\"padding-bottom:0\"><div class=\"wrap\"><div class=\"cfgh\"><div>'+lbl('Stel samen · Maxima Boats')"
    "+'<h1 style=\"font-size:clamp(36px,5vw,72px)\">'+(n?mxEsc(n)+'.':'Stel je Maxima samen.')+'</h1>"
    "<p class=\"lead\" style=\"margin-top:14px\">'+(n?'Stel je '+mxEsc(n)+' stap voor stap samen en vraag direct een offerte aan.':'Kies een Maxima-model en stel hem stap voor stap samen.')+'</p></div>"
    "<a class=\"tlink\" href=\"#/stel-samen\">Andere boot samenstellen</a></div></div></section>"
    "<section style=\"padding:28px 0 0\"><div class=\"wrap\"><div class=\"mxf\"><iframe src=\"'+src+'\" title=\"'+(n?mxEsc(n):'Maxima')+' configurator\" loading=\"lazy\" allow=\"clipboard-write\"></iframe></div>"
    "<p class=\"note\" style=\"margin-top:14px\">Zie je de configurator niet? <a class=\"tlink\" href=\"'+src.replace('&embed=1','').replace('?embed=1','')+'\" target=\"_blank\" rel=\"noopener\">Open hem in een nieuw tabblad</a>.</p></div></section>'}"
) + s[j:]
# 3. Routes: alle Maxima-modellen, en Maxima-boot-id's naar de Maxima-configurator
rep("[/^\\/stel-samen\\/maxima-760$/,pCfgMx]",
    "[/^\\/stel-samen\\/maxima(?:-([a-z0-9-]+))?$/,function(r){return pCfgMx(r?'maxima-'+r:'')}]")
rep("[/^\\/stel-samen\\/?(\\d*)$/,pCfg]",
    "[/^\\/stel-samen\\/?(\\d*)$/,function(id){return MXMAP[id]?pCfgMx(MXMAP[id]):pCfg(id)}]")
rep("if(path==='/stel-samen'||/^\\/stel-samen\\/\\d+$/.test(path)){C.stap=0;cfgRender()}",
    "if(path==='/stel-samen'||(/^\\/stel-samen\\/\\d+$/.test(path)&&!MXMAP[path.split('/')[2]])){C.stap=0;cfgRender()}")

# 4. "Stel samen" op de bootpagina
rep("(b.cfg?'<a class=\"btn\" href=\"#/stel-samen/'+b.id+'\">Stel samen</a>'",
    "(b.cfg?'<a class=\"btn\" href=\"'+mxHref(b)+'\">Stel samen</a>'")

# 5. Banner op de algemene configurator: alle Maxima-modellen in plaats van alleen de 760
rep('<a class="mxb" href="#/stel-samen/maxima-760"><span><b>Maxima 760 NIEUW</b> stel hem direct samen met de live configurator</span><i>Open</i></a>',
    '<a class="mxb" href="#/stel-samen/maxima"><span><b>Maxima Boats</b> stel elk Maxima-model samen met de live configurator</span><i>Open</i></a>')

open(p, 'w', encoding='utf-8').write(s)
print('ok: Maxima-configurator 2.0 gekoppeld (%d boten)' % len(MXMAP))
