"""Patch: versie 2. Klop Premium Service™ nooit op een blauwe achtergrond (bootpagina: blok 'Zonder gedoe' wordt licht).
Toepassen als laatste (na patch_bezoek.py)."""
import sys
p = sys.argv[1]
s = open(p, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: raise SystemExit('anchor %d != %d: %s' % (n, count, old[:90]))
    s = s.replace(old, new)
CSS = r"""
/* ===== v2: Premium Service op licht ===== */
.zg.zgl{background:var(--gel);color:var(--nacht);border-top:1px solid var(--mist);border-bottom:1px solid var(--mist)}
.zg.zgl h2{color:var(--nacht)}.zg.zgl .lead{color:var(--staal)}.zg.zgl .gk2{color:var(--nacht)}
.zg.zgl .zt{background:#fff;border:1px solid var(--mist);color:var(--nacht)}
.zg.zgl .zt p{color:var(--staal)}.zg.zgl .zt .zn{color:var(--staal)}.zg.zgl .zt .zi svg{stroke:var(--nacht)}
.zg.zgl .zt:hover{border-color:var(--nacht)}.zg.zgl .zg-n{color:var(--staal)}
.zg.zgl .tlink{color:var(--nacht)}
"""
i = s.find('</style>'); s = s[:i] + CSS + s[i:]
rep('<section class="zg dark" id="zondergedoe">', '<section class="zg zgl" id="zondergedoe">')
rep("btn('Lees de methodiek','#/klop-premium-service','wit')+'<a class=\"tlink\" href=\"#/bezoek/'+b.id+'\">Bespreek het bij een proefvaart</a>",
    "btn('Lees de methodiek','#/klop-premium-service','solid')+'<a class=\"tlink\" href=\"#/bezoek/'+b.id+'\">Bespreek het bij een proefvaart</a>")
open(p, 'w', encoding='utf-8').write(s)
print('ok: v2')
