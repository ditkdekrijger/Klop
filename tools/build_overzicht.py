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

DATA = {k: [{'f': PFX + x['file'], 't': clean(x['title'])} for x in v] for k, v in {'recap': recap, 'old': recap_old, 'brandbook': M['brandbook'], 'merk': M['merkuitingen'], 'ds': M['ds']}.items()}
N = {'bb': len(M['brandbook']), 'mu': len(M['merkuitingen']), 'ds': len(M['ds']), 'rc': len(recap)}

page = open(os.path.join(ROOT, 'tools/overzicht.template.html')).read()
for k, v in {
    '{{SITE}}': SITE, '{{PFX}}': PFX, '{{RECAP_MAIN}}': PFX + recap[0]['file'],
    '{{RECAP_STRIP}}': flat(recap, 'recap', 'strip'), '{{RECAP_OLD}}': flat(recap_old, 'old'),
    '{{BRANDBOOK}}': grid(M['brandbook'], bb_deel, 'brandbook'), '{{MERK}}': grid(M['merkuitingen'], mu_groep, 'merk'),
    '{{SWATCHES}}': sw, '{{TYPE}}': typ, '{{SPACING}}': toklist('spacing'), '{{RADIUS}}': toklist('radius'), '{{LAYOUT}}': toklist('layout'),
    '{{ICONS}}': icons, '{{COMPS}}': comps, '{{DATA}}': json.dumps(DATA, ensure_ascii=False),
    '{{N_BB}}': str(N['bb']), '{{N_MU}}': str(N['mu']), '{{N_DS}}': str(N['ds']), '{{N_RC}}': str(N['rc']), '{{N_IC}}': str(icons.count('class="ic"')),
    '{{CODE}}': open(os.path.join(ROOT, 'tools/code_sectie.html')).read(),
}.items():
    page = page.replace(k, v)
open(OUT, 'w').write(page)
print('geschreven', OUT, len(page))
