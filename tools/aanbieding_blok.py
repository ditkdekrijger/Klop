# Genereert pitch-blok 11 (aanbieding 2027) uit de onderwerpen en hun plek op de Powermarketing-grid en zet het in tools/pitch.template.html.
# Let op: voegt ook CSS toe; draai het op een template waarin blok 11 nog de vorige versie heeft.
import html
e = html.escape
AREAS = ['Marketing & content', 'Sales', 'CODE', 'Change']
PHASES = ['Bereik', 'Kliks', 'Leads', 'Sales']
CELLS = [['Displaycampagnes, SEO', 'Direct mail, events', 'Sites, platforms', 'Merk- & productpositionering'],
         ['Klikcampagnes, UI/UX', 'Salespitch, lead-inzichten', 'Landingspages, CRO', 'Processen & structuur'],
         ['Leadcampagnes, -magnets', 'Follow-up, (bel-)scripts', 'Configurators, pijplijn', 'Leiderschap & management'],
         ['Retargetingcampagnes, datamanagement', 'Pitch, salestechniek', 'Dashboards, automations', 'Businessmodel & waardepropositie']]
# onderwerp: naam, grid-cellen (fase, gebied), planning dec..q4
TOP = [
 ('Merk Klop', [(0, 3), (0, 0), (2, 0)], ['Merkfeiten vast, fotodag gepland', 'Fotodag, drukwerk, campagne Voorjaarsklaar', 'Campagne online en buiten, proefvaardagen', 'Zomercontent, tussenmeting', 'Campagne Winterklaar, plan 2028']),
 ('Nieuwe site in WordPress', [(0, 2), (1, 2), (1, 0)], ['Thema op het designsysteem, redirectkaart', 'Bouw en livegang eind maart', 'Configurator op de site, Mijn Klop', 'Conversie verbeteren', 'Beheer en wensen 2028']),
 ('SEO en GEO', [(0, 0), (0, 2)], ['Nulmeting en vragenkaart', 'Techniek in het thema, soortpagina’s', 'Vraag-en-antwoordcontent, reviews, links', 'Vast contentritme, maandrapport', 'Wintercontent, jaarrapport']),
 ('CRM', [(2, 2), (2, 1), (3, 2)], ['Inventarisatie en datamodel', 'Alle leads in één bak, klantkaart, offertes', 'Klop Premium Service™ in het CRM', 'Mijn Klop gekoppeld, dashboards', 'Automations; ERP en CAD in overleg']),
 ('Maxima-identiteit aanscherpen', [(0, 3), (3, 3)], ['Analyse, aanspreekvorm gelijk', 'Merkregels Maxima, configurator in stijl', 'Modelpagina’s, brochure, beurs', 'Content per model', 'Evaluatie, modeljaar 2028']),
]
cellmap = {}
for n, (name, cells, _) in enumerate(TOP, 1):
    for c in cells: cellmap.setdefault(c, []).append(n)

def grid(cls):
    h = '<div class="%s"><div class="pgc pgh"></div>' % cls + ''.join('<div class="pgc pgh">%s</div>' % e(a) for a in AREAS)
    for r, ph in enumerate(PHASES):
        h += '<div class="pgc pgp">%s</div>' % ph
        for c in range(4):
            ns = cellmap.get((r, c), [])
            h += '<div class="pgc%s"><span>%s</span>%s</div>' % (' on' if ns else '', e(CELLS[r][c]), ''.join('<i>%d</i>' % n for n in ns) if ns else '')
    return h + '</div>'

legend = '<ol class="pg-leg">' + ''.join('<li><i>%d</i>%s</li>' % (n, e(t[0])) for n, t in enumerate(TOP, 1)) + '</ol>'
rows = ''
for n, (name, cells, plan) in enumerate(TOP, 1):
    chips = ''.join('<span title="%s · %s">%s</span>' % (e(AREAS[c]), PHASES[r], e(CELLS[r][c])) for r, c in cells)
    rows += '<tr><th><i>%d</i>%s<div class="chips">%s</div></th>%s</tr>\n' % (n, e(name), chips, ''.join('<td%s>%s</td>' % (' class="pdec"' if k == 0 else '', e(t)) for k, t in enumerate(plan)))

ART = '''<article class="blk" data-n="11" data-t="Aanbieding 2027"><div class="sl"><div class="sl-t"><span class="kick">11 · Aanbieding</span><h2>Extra inzet in 2027, met een start in december.</h2><p class="lead">Vijf onderwerpen, geplot op de Powermarketing-grid. Zo zie je in één oogopslag welke werkgebieden en fases van JUST.LEAD extra aangaan.</p>''' + legend + '''</div><div class="sl-v">''' + grid('pgrid') + '''</div><a class="sl-more" href="#" data-more="1">Verdieping ↓</a></div><div class="det">

<h3 class="gh">Planning per onderwerp</h3>
<div class="plan-wrap"><table class="plan plan2"><colgroup><col class="c0"><col><col><col><col><col></colgroup>
<thead><tr><th></th><th class="pdec">December 2026<small>start</small></th><th>Q1 2027<small>jan · feb · mrt</small></th><th>Q2 2027<small>apr · mei · jun</small></th><th>Q3 2027<small>jul · aug · sep</small></th><th>Q4 2027<small>okt · nov · dec</small></th></tr></thead>
<tbody>
''' + rows + '''</tbody></table></div>
<p class="cap" style="margin-top:10px">Het zwaartepunt ligt voor het vaarseizoen: in Q1 staan de nieuwe site, de fotodag en de basis van het CRM. Per kwartaal sturen we samen bij.</p>

<h3 class="gh" style="margin-top:34px">Zo werken we</h3>
<div class="pts"><div><small>Eén team</small><b>JUST.LEAD</b><p>Marketing &amp; content, CODE en Change werken als één team, met één aanspreekpunt voor Klop.</p></div><div><small>December</small><b>Meteen beginnen</b><p>Startsessie, merkfeiten, thema, nulmeting en datamodel, zodat we in januari direct bouwen.</p></div><div><small>Ritme</small><b>Elke maand een rapport</b><p>Wat er is gedaan, wat het oplevert en wat er volgt, langs de grid.</p></div><div><small>Nodig van Klop</small><b>Tijd en toegang</b><p>Een vast moment per twee weken, de fotodag, en toegang tot de systemen.</p></div></div>
</div></article>
'''

CSS = '''.pgrid{display:grid;grid-template-columns:64px repeat(4,minmax(0,1fr));gap:6px;width:100%}
.pgc{position:relative;min-height:74px;border-radius:12px;background:#fff;box-shadow:inset 0 0 0 1px var(--line);padding:9px 10px;font-size:11.5px;line-height:1.3;color:var(--mut)}
.pgc.pgh{min-height:0;background:var(--nacht);color:#fff;box-shadow:none;font-size:11px;font-weight:600;padding:9px 10px}.pgc.pgh:first-child{background:none}
.pgc.pgp{background:none;box-shadow:none;font-size:11px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--nacht);padding:9px 0;writing-mode:horizontal-tb}
.pgc.on{background:#FFF1CF;box-shadow:inset 0 0 0 1.5px #EFA91F;color:var(--nacht)}
.pgc i,.pg-leg i,.plan2 tbody th i{display:inline-grid;place-items:center;width:20px;height:20px;border-radius:50%;background:var(--nacht);color:#fff;font-style:normal;font-size:11px;font-weight:700;margin:6px 4px 0 0}
.pgc span{display:block}
.pg-leg{list-style:none;margin:18px 0 0;padding:0;display:grid;gap:6px}.pg-leg li{display:flex;align-items:center;gap:8px;font-size:15px;color:var(--nacht)}.pg-leg i{margin:0}
.plan2 col.c0{width:210px}.plan2 tbody th{font-size:15px}.plan2 tbody th i{margin:0 6px 0 0;vertical-align:-3px}
.plan2 .chips{display:flex;flex-wrap:wrap;gap:4px;margin-top:8px}.plan2 .chips span{font-size:10px;font-weight:600;letter-spacing:.04em;background:#FFF1CF;color:var(--nacht);border-radius:999px;padding:3px 7px}
.plan2 td{font-size:13.5px;color:var(--nacht)}
@media(max-width:700px){.pgrid{grid-template-columns:48px repeat(4,minmax(0,1fr));gap:4px}.pgc{min-height:58px;font-size:9.5px;padding:6px}.pgc.pgh{font-size:9px;padding:6px}}
'''

R = '/home/user/Klop/tools/'
p = R + 'pitch.template.html'; s = open(p).read()
a = s.index('<article class="blk" data-n="11"'); b = s.index('</article>', a) + len('</article>\n')
s = s[:a] + ART + s[b:]
i = s.index('</style></head>'); s = s[:i] + CSS + s[i:]
old = 'Merk, site, SEO en GEO, CRM en Maxima: de planning vanaf december, in dagen per kwartaal.'
assert old in s; s = s.replace(old, 'Merk, site, SEO en GEO, CRM en Maxima: de planning vanaf december, geplot op de Powermarketing-grid.')
open(p, 'w').write(s); print('ok')
