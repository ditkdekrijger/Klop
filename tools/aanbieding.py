"""Aanbieding 2027: vijf onderwerpen, geplot op de Powermarketing-grid, met de planning december 2026 t/m Q4 2027.
Schrijft tools/aanbieding_sectie.html (sectie in het overzicht). Gebruik: python3 tools/aanbieding.py"""
import html, os
e = html.escape
AREAS = ['Marketing & content', 'Sales', 'CODE', 'Change']
PHASES = ['Bereik', 'Kliks', 'Leads', 'Sales']
CELLS = [['Displaycampagnes, SEO', 'Direct mail, events', 'Sites, platforms', 'Merk- & productpositionering'],
         ['Klikcampagnes, UI/UX', 'Salespitch, lead-inzichten', 'Landingspages, CRO', 'Processen & structuur'],
         ['Leadcampagnes, -magnets', 'Follow-up, (bel-)scripts', 'Configurators, pijplijn', 'Leiderschap & management'],
         ['Retargetingcampagnes, datamanagement', 'Pitch, salestechniek', 'Dashboards, automations', 'Businessmodel & waardepropositie']]
# onderwerp, gridblokken (fase, werkgebied), planning december, Q1, Q2, Q3, Q4
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

grid = '<div class="pgrid"><div class="pgc pgh"></div>' + ''.join('<div class="pgc pgh">%s</div>' % e(a) for a in AREAS)
for r, ph in enumerate(PHASES):
    grid += '<div class="pgc pgp">%s</div>' % ph
    for c in range(4):
        ns = cellmap.get((r, c), [])
        grid += '<div class="pgc%s"><span>%s</span>%s</div>' % (' on' if ns else '', e(CELLS[r][c]), ''.join('<i>%d</i>' % n for n in ns))
grid += '</div>'
legend = '<ol class="pg-leg">' + ''.join('<li><i>%d</i>%s</li>' % (n, e(t[0])) for n, t in enumerate(TOP, 1)) + '</ol>'
rows = ''
for n, (name, cells, plan) in enumerate(TOP, 1):
    chips = ''.join('<span title="%s · %s">%s</span>' % (e(AREAS[c]), PHASES[r], e(CELLS[r][c])) for r, c in cells)
    rows += '<tr><th><i>%d</i>%s<div class="chips">%s</div></th>%s</tr>\n' % (n, e(name), chips, ''.join('<td%s>%s</td>' % (' class="pdec"' if k == 0 else '', e(t)) for k, t in enumerate(plan)))

SECTIE = '''<section class="sec" id="aanbieding"><div class="wrap">
<div class="sh"><div><span class="kick">09 · Zo verder</span><h2>Aanbieding 2027</h2></div><p class="lead">Extra inzet in 2027, met een start in december. Vijf onderwerpen, geplot op de Powermarketing-grid: zo zie je welke werkgebieden en fases van JUST.LEAD extra aangaan.</p></div>
<div class="aanb">''' + legend + grid + '''</div>
<h3 class="gh">Planning per onderwerp</h3>
<div class="plan-wrap"><table class="plan plan2"><colgroup><col class="c0"><col><col><col><col><col></colgroup>
<thead><tr><th></th><th class="pdec">December 2026<small>start</small></th><th>Q1 2027<small>jan · feb · mrt</small></th><th>Q2 2027<small>apr · mei · jun</small></th><th>Q3 2027<small>jul · aug · sep</small></th><th>Q4 2027<small>okt · nov · dec</small></th></tr></thead>
<tbody>
''' + rows + '''</tbody></table></div>
<p class="note">Het zwaartepunt ligt voor het vaarseizoen: in Q1 staan de nieuwe site, de fotodag en de basis van het CRM. Per kwartaal sturen we samen bij.</p>
<h3 class="gh">Zo werken we</h3>
<div class="pts"><div><small>Eén team</small><b>JUST.LEAD</b><p>Marketing &amp; content, CODE en Change werken als één team, met één aanspreekpunt voor Klop.</p></div><div><small>December</small><b>Meteen beginnen</b><p>Startsessie, merkfeiten, thema, nulmeting en datamodel, zodat we in januari direct bouwen.</p></div><div><small>Ritme</small><b>Elke maand een rapport</b><p>Wat er is gedaan, wat het oplevert en wat er volgt, langs de grid.</p></div><div><small>Nodig van Klop</small><b>Tijd en toegang</b><p>Een vast moment per twee weken, de fotodag, en toegang tot de systemen.</p></div></div>
</div></section>
'''
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'aanbieding_sectie.html'), 'w').write(SECTIE)
print('geschreven tools/aanbieding_sectie.html')
