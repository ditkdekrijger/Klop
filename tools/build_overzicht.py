"""Bouwt overzicht/index.html: recap, brandbook, designsysteem, merkuitingen en website in één bestand.
Gebruik: python3 tools/build_overzicht.py [SITE_URL] [OUT] [IMGPREFIX]"""
import json, os, sys, html, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = sys.argv[1] if len(sys.argv) > 1 else '../site/index.html'
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, 'overzicht/index.html')
PFX = sys.argv[3] if len(sys.argv) > 3 else 'ov/'
M = json.load(open(os.path.join(ROOT, 'overzicht/manifest.json')))
T = json.load(open(os.path.join(ROOT, 'bron/designsysteem/project/tokens.json')))
ICDIR = os.path.join(ROOT, 'bron/designsysteem/project/assets/Icons')
e = html.escape

def clean(t):
    t = re.sub(r'^(B?\d+[a-z]?\s+)+', '', t)          # "06 05 Het brandbook" -> "Het brandbook"
    t = re.sub(r'^M\d+[a-z]?\s+', '', t)
    return t

# ---------- recap: deck B is de definitieve versie ----------
recap = [x for x in M['recap'] if re.match(r'recap/b\d+', x['file'])]
recap_old = [x for x in M['recap'] if x not in recap]

# ---------- brandbook in delen ----------
BB_DELEN = [('Opening', '01'), ('Deel 1 · Kern', '04'), ('Deel 2 · Positionering', '09'), ('Deel 3 · Identiteit', '14'), ('Deel 4 · Basiselementen', '21'), ('Deel 5 · Toepassingen', '33')]
def bb_deel(f):
    n = os.path.basename(f)
    num = '01' if n.startswith('Main') else n[:2]
    d = BB_DELEN[0][0]
    for name, start in BB_DELEN:
        if num >= start: d = name
    return d

MU_GROEP = [('Het merk', lambda n: n.startswith(('Main', '02', '03', '04'))),
            ('Klant en service', lambda n: re.match(r'm0\d', n)),
            ('Locatie, haven en evenement', lambda n: re.match(r'm(1\d|2[0-2])', n)),
            ('Online', lambda n: n.startswith('m23')),
            ('Campagne', lambda n: n.startswith('m26')),
            ('Post, papier en onderweg', lambda n: re.match(r'm2[4578]', n)),
            ('Vervolg', lambda n: n.startswith('33'))]
def mu_groep(f):
    n = os.path.basename(f)
    for g, fn in MU_GROEP:
        if fn(n): return g
    return 'Overig'

def grid(items, groupfn, setname):
    out, cur = [], None
    for i, x in enumerate(items):
        g = groupfn(x['file'])
        if g != cur:
            if cur is not None: out.append('</div>')
            out.append('<h3 class="gh">%s</h3><div class="grid">' % e(g)); cur = g
        out.append('<button class="th" data-set="%s" data-i="%d"><img loading="lazy" src="%s%s" alt=""><span>%s</span></button>' % (setname, i, PFX, x['file'], e(clean(x['title']))))
    out.append('</div>')
    return ''.join(out)

def flat(items, setname, cls='grid'):
    return '<div class="%s">' % cls + ''.join('<button class="th" data-set="%s" data-i="%d"><img loading="lazy" src="%s%s" alt=""><span>%s</span></button>' % (setname, i, PFX, x['file'], e(clean(x['title']))) for i, x in enumerate(items)) + '</div>'

# ---------- designsysteem ----------
cols = T['color']['tokens']
merk = [c for c in cols if c['name'] in ('gelcoat', 'nachtblauw', 'oliegoed', 'diep', 'mist', 'chroom', 'staal', 'wit')]
sw = ''.join('<div class="sw"><i style="background:%s"></i><b>%s</b><code>%s</code><p>%s</p></div>' % (c['value']['light'], e(c['name'].capitalize()), c['value']['light'], e(c.get('usage', ''))) for c in merk)
typ = ''
for g in T['type']['groups']:
    fam = T['type']['families'][g['family']]
    for st in g['styles']:
        size = st['fontSize']; shown = 'min(%s,9vw)' % size
        sample = 'Vaar je vrijheid.' if g['family'] == 'display' else 'Wij regelen het gedoe. Jij vaart.'
        typ += '<div class="ty"><div class="tm"><b>%s</b><span>%s · %s · %s</span><p>%s</p></div><div class="ts" style="font-family:%s;font-size:%s;font-weight:%s;letter-spacing:%s;line-height:%s">%s</div></div>' % (
            st['name'], size, st['fontWeight'], st.get('letterSpacing', '0'), e(st.get('usage', '')), e(fam, quote=True), shown, st['fontWeight'], st.get('letterSpacing', '0'), st['lineHeight'], sample)
def toklist(key):
    return ''.join('<tr><td><code>%s</code></td><td>%s</td><td>%s</td></tr>' % (t['name'], t['value'], e(t.get('usage', ''))) for t in T[key]['tokens'])
icons = ''
for f in sorted(os.listdir(ICDIR)):
    if f.endswith('.svg'):
        svg = open(os.path.join(ICDIR, f)).read()
        svg = re.sub(r'<\?xml[^>]*>', '', svg)
        icons += '<div class="ic">%s<span>%s</span></div>' % (svg, f[:-4])
comps = ''
for i, c in enumerate(M['ds']):
    rd = re.sub(r'^#.*\n', '', c['readme']).strip()
    rd = e(re.sub(r'[`*_]', '', rd))[:340]
    comps += '<figure class="cp"><button class="th" data-set="ds" data-i="%d"><img src="%s%s" alt=""></button><figcaption><b>%s</b><small>%s</small><p>%s</p></figcaption></figure>' % (i, PFX, c['file'], e(c['title']), e(c['group']), rd)

BEELD = [{'f': x['f'].replace('{{PFX}}', PFX), 't': x['t']} for x in json.load(open(os.path.join(ROOT, 'tools/beeld_data.json')))]
def hd_list():
    """Relatieve paden van de scherpe (2x) beelden in overzicht/hd (gemaakt met tools/render_hd.js)."""
    base = os.path.join(ROOT, 'overzicht/hd'); out = []
    for d, _, ff in os.walk(base):
        out += [os.path.relpath(os.path.join(d, f), base) for f in ff if f.endswith('.jpg')]
    return sorted(out)

MU_CAMP = ('merkuitingen/m26g-campagne-digitaal.jpg', 'Campagne: digitaal, voorbeeld')
MU_TOP = ['merkuitingen/m08-het-gele-label.jpg', 'merkuitingen/m18-overdracht.jpg', 'merkuitingen/m16-oliegoed.jpg', 'merkuitingen/m13-servicehaven.jpg', 'merkuitingen/m26-campagne.jpg']
def mu_overzicht(pfx):
    t = {x['file']: x['title'] for x in M['merkuitingen']}
    top = '<div class="mutop">' + ''.join('<button class="th" data-set="mutop" data-i="%d"><img loading="lazy" src="%s%s" alt=""><span>%s</span></button>' % (i, pfx, f, html.escape(clean(t[f]))) for i, f in enumerate(MU_TOP)) + '</div>'
    camp = '<div class="mucamp"><button class="th" data-set="mutop" data-i="%d"><img loading="lazy" src="%s%s" alt="Voorbeeld digitale campagne"><span>%s</span></button></div>' % (len(MU_TOP), pfx, MU_CAMP[0], MU_CAMP[1])
    return open(os.path.join(ROOT, 'tools/mu_overzicht.html')).read().replace('{{MU_TOP}}', top).replace('{{MU_CAMP}}', camp)
def mu_data(pfx):
    t = {x['file']: x['title'] for x in M['merkuitingen']}
    return [{'f': pfx + f, 't': clean(t[f])} for f in MU_TOP] + [{'f': pfx + MU_CAMP[0], 't': MU_CAMP[1]}]
DATA = {k: [{'f': PFX + x['file'], 't': clean(x['title'])} for x in v] for k, v in {'recap': recap, 'old': recap_old, 'brandbook': M['brandbook'], 'ds': M['ds']}.items()}
N = {'bb': len(M['brandbook']), 'mu': len(M['merkuitingen']), 'ds': len(M['ds']), 'rc': len(recap)}

DATA['mutop'] = mu_data(PFX)
SCHERMEN = json.load(open(os.path.join(ROOT, 'tools/schermen.json')))['schermen']
DATA['site'] = [{'f': PFX + x['file'], 't': x['title']} for x in SCHERMEN]
def sg(g): return '<div class="grid sitegrid">' + ''.join('<button class="th" data-set="site" data-i="%d"><img loading="lazy" src="%s%s" alt=""><span>%s</span></button>' % (i, PFX, x['file'], e(x['title'])) for i, x in enumerate(SCHERMEN) if x['g'] == g) + '</div>'
page = open(os.path.join(ROOT, 'tools/overzicht.template.html')).read()
page = page.replace('{{CFG}}', open(os.path.join(ROOT, 'tools/configurator_sectie.html')).read())
page = page.replace('{{MU_OVERZICHT}}', mu_overzicht(PFX))
for k, g in {'{{SITE_HOME}}': 'home', '{{SITE_AANBOD}}': 'aanbod', '{{SITE_PAG}}': 'pag', '{{PROTO}}': 'proto'}.items(): page = page.replace(k, sg(g))
page = page.replace('{{BEELD}}', open(os.path.join(ROOT, 'tools/beeld_sectie.html')).read())
for k, v in {
    '{{SITE}}': SITE, '{{PFX}}': PFX, '{{RECAP_MAIN}}': PFX + recap[0]['file'],
    '{{RECAP_STRIP}}': flat(recap, 'recap', 'strip'), '{{RECAP_OLD}}': flat(recap_old, 'old'),
    '{{BRANDBOOK}}': grid(M['brandbook'], bb_deel, 'brandbook'), '{{MERK}}': grid(M['merkuitingen'], mu_groep, 'merk'),
    '{{SWATCHES}}': sw, '{{TYPE}}': typ, '{{SPACING}}': toklist('spacing'), '{{RADIUS}}': toklist('radius'), '{{LAYOUT}}': toklist('layout'),
    '{{HD}}': json.dumps(hd_list()), '{{HDP}}': 'hd/', '{{ICONS}}': icons, '{{COMPS}}': comps, '{{DATA}}': json.dumps(DATA, ensure_ascii=False),
    '{{N_BB}}': str(N['bb']), '{{N_MU}}': str(N['mu']), '{{N_DS}}': str(N['ds']), '{{N_RC}}': str(N['rc']), '{{N_IC}}': str(icons.count('class="ic"')),
    '{{CODE}}': open(os.path.join(ROOT, 'tools/code_sectie.html')).read(),
    '{{PM}}': open(os.path.join(ROOT, 'tools/powermarketing_sectie.html')).read(),
}.items():
    page = page.replace(k, v)
open(OUT, 'w').write(page)
print('geschreven', OUT, len(page))
