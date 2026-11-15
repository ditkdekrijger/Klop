"""Patch: Maxima-configurator bewaren in Mijn Klop (na tools/patch_maxima.py).

- De configurator (iframe) stuurt {type:'mx:save', ...} naar de site; de site zet hem in
  Mijn Klop > Configuraties (S.cfgs) en bevestigt met {type:'mx:saved'}.
  Alleen berichten van dezelfde oorsprong en uit een Maxima-iframe worden aangenomen.
- Een bewaarde configuratie krijgt een link: #/stel-samen/<model>?c=...&ral=...
- pCfgMx geeft c, ral en stap uit de hash door aan de iframe, zodat die link de samenstelling herstelt.

Gebruik: python3 tools/patch_maxima_bewaren.py site/index.html   (eenmalig)
"""
import sys

p = sys.argv[1]
s = open(p, encoding='utf-8').read()
if 'var MXC=' not in s:
    raise SystemExit('eerst tools/patch_maxima.py toepassen')
if "'mx:save'" in s:
    raise SystemExit('al gepatcht')


def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit('anchor count %d != %d for: %s' % (n, count, old[:80]))
    s = s.replace(old, new)


# 1. Hash-query (c, ral, stap) doorgeven aan de iframe
rep("function mxSrc(slug){",
    "function mxQs(){var q=(location.hash.split('?')[1]||''),o=[];q.split('&').forEach(function(kv){var k=kv.split('=')[0];"
    "if(/^(c|ral|stap)$/.test(k)&&/^[a-z]+=[0-9a-z.,~%-]*$/i.test(kv))o.push(kv)});return o.length?'&'+o.join('&'):''}"
    "function mxSrc(slug){")
rep("src=mxSrc(n?slug:'');", "src=mxSrc(n?slug:'')+(n?mxQs():'');")

# 2. Berichten uit de configurator aannemen en in Mijn Klop bewaren
rep("var MXC='../maxima-configurator/public/';",
    "var MXC='../maxima-configurator/public/';"
    "window.addEventListener('message',function(e){var d=e.data;if(e.origin!==location.origin||!d||d.type!=='mx:save')return;"
    "var fr=[].slice.call(document.querySelectorAll('.mxf iframe')).filter(function(f){return f.contentWindow===e.source})[0];if(!fr)return;"
    "var slug=String(d.slug||'').replace(/[^a-z0-9-]/g,'');if(!MXN[slug])return;"
    "var qs=String(d.qs||'').replace(/[^0-9a-z.,~%=&-]/gi,'').slice(0,1500);"
    "S.cfgs.push({naam:MXN[slug],kleur:String(d.kleur||'').slice(0,80),motor:String(d.motor||'').slice(0,80),"
    "tot:Math.max(0,Math.round(+d.tot||0)),href:'#/stel-samen/'+slug+(qs?'?'+qs:'')});save('cfgs');"
    "toast('Configuratie bewaard in Mijn Klop.',1);e.source.postMessage({type:'mx:saved'},e.origin)});")

# 3. Mijn Klop: bewaarde Maxima-configuratie is klikbaar
rep("'<li><div><b>'+esc(c.naam)+'</b>",
    "'<li><div><b>'+(c.href?'<a class=\"wv\" href=\"'+esc(c.href)+'\">'+esc(c.naam)+'</a>':esc(c.naam))+'</b>",
    count=2)

open(p, 'w', encoding='utf-8').write(s)
print('ok: bewaren in Mijn Klop gekoppeld')
