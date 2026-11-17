"""Bouwt de pitch (versie 2): pitch/index.html, en met --dist een publiceerbare map met gebundelde beelden.
Gebruik: python3 tools/build_pitch.py [--dist MAP]"""
import os, re, sys, json, html, base64, io, shutil
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
e = html.escape
M = json.load(open(os.path.join(ROOT, 'overzicht/manifest.json')))
tpl_over = open(os.path.join(ROOT, 'tools/overzicht.template.html')).read()
CSS = tpl_over[tpl_over.index('<style>') + 7: tpl_over.index('</style>')]
def clean(t):
    t = re.sub(r'^(B?\d+[a-z]?\s+)+', '', t); return re.sub(r'^M\d+[a-z]?\s+', '', t)
SCHERMEN = json.load(open(os.path.join(ROOT, 'tools/schermen.json')))['schermen']
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
def hd_list():
    """Relatieve paden van de scherpe (2x) beelden in overzicht/hd (gemaakt met tools/render_hd.js)."""
    base = os.path.join(ROOT, 'overzicht/hd'); out = []
    for d, _, ff in os.walk(base):
        out += [os.path.relpath(os.path.join(d, f), base) for f in ff if f.endswith('.jpg')]
    return sorted(out)
def build(pfx, hdp='hd/'):
    recap = [dict(x) for x in M['recap'] if re.match(r'recap/b\d+\.jpg$', x['file'])]
    for x in recap:
        if x['file'] == 'recap/b04.jpg': x['file'] = 'recap/b04-licht.jpg'
    def th(set_, i, x): return '<button class="th" data-set="%s" data-i="%d"><img loading="lazy" src="%s%s" alt=""><span>%s</span></button>' % (set_, i, pfx, x['file'], e(clean(x['title'])))
    strip = '<div class="strip">' + ''.join(th('recap', i, x) for i, x in enumerate(recap)) + '</div>'
    bb = '<div class="grid">' + ''.join(th('brandbook', i, x) for i, x in enumerate(M['brandbook'])) + '</div>'
    mu = '<div class="grid">' + ''.join(th('merk', i, x) for i, x in enumerate(M['merkuitingen'])) + '</div>'
    site = SCHERMEN
    def sg(g): return '<div class="grid sitegrid">' + ''.join(th('site', i, x) for i, x in enumerate(site) if x['g'] == g) + '</div>'
    code = open(os.path.join(ROOT, 'tools/code_sectie.html')).read()
    code = code[code.index('<div class="cx">'): code.rindex('</div></section>')]
    data = {k: [{'f': pfx + x['file'], 't': clean(x['title'])} for x in v] for k, v in {'recap': recap, 'brandbook': M['brandbook'], 'site': site, 'mutop': [next(x for x in M['merkuitingen'] if x['file'] == f) for f in MU_TOP] + [{'file': MU_CAMP[0], 'title': MU_CAMP[1]}]}.items()}
    page = open(os.path.join(ROOT, 'tools/pitch.template.html')).read()
    for k, v in {'{{CSS}}': CSS, '{{RECAP_STRIP}}': strip, '{{BB_GRID}}': bb, '{{MU_GRID}}': mu, '{{CODE_BODY}}': code,
                 '{{DATA}}': json.dumps(data, ensure_ascii=False), '{{HD}}': json.dumps(hd_list()), '{{HDP}}': hdp, '{{N_BB}}': str(len(M['brandbook'])), '{{N_MU}}': str(len(M['merkuitingen'])), '{{MU_OVERZICHT}}': mu_overzicht(pfx), '{{SITE_HOME}}': sg('home'), '{{SITE_AANBOD}}': sg('aanbod'), '{{SITE_PAG}}': sg('pag'), '{{PROTO}}': sg('proto')}.items():
        page = page.replace(k, v)
    page = page.replace('{{PFX}}', pfx)
    assert '{{' not in page, re.findall(r'\{\{\w+\}\}', page)
    return page
os.makedirs(os.path.join(ROOT, 'pitch'), exist_ok=True)
open(os.path.join(ROOT, 'pitch/index.html'), 'w').write(build('../overzicht/ov/', '../overzicht/hd/').replace('data-src="powermarketing.html"', 'data-src="../overzicht/powermarketing.html"'))
print('geschreven pitch/index.html')
if '--dist' in sys.argv:
    from PIL import Image
    OUT = sys.argv[sys.argv.index('--dist') + 1]; os.makedirs(OUT, exist_ok=True)
    page = build('ov/')
    used = sorted(set(re.findall(r'ov/([\w./-]+\.(?:jpg|png))', page)))
    OV = {}
    for rel in used:
        p = os.path.join(ROOT, 'overzicht/ov', rel)
        if rel.endswith('.png'): OV['ov/' + rel] = 'data:image/png;base64,' + base64.b64encode(open(p, 'rb').read()).decode(); continue
        im = Image.open(p).convert('RGB'); w = 2400 if rel == 'opening.jpg' else 1200 if '-lang' in rel else (1600 if ('pitch/mock' in rel or 'pitch/site/' in rel or 'pitch/proto/' in rel) else 1280)
        if im.width > w: im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        b = io.BytesIO(); im.save(b, 'JPEG', quality=70, optimize=True, progressive=True)
        OV['ov/' + rel] = 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
    open(os.path.join(OUT, 'ov.js'), 'w').write('window.OV=' + json.dumps(OV) + ';')
    page = page.replace(' src="ov/', ' data-ov="ov/')
    page = re.sub(r"style=\"background-image:url\('ov/([^']+)'\)", r'data-bg="ov/\1" style="', page)
    page = re.sub(r"style=\"background-image:url\('ov/([^']+)'\);", r'data-bg="ov/\1" style="', page)
    page = page.replace('deck(0);\n</script>', '''</script><script src="ov.js"></script><script>(function(){function R(p){return(window.OV&&OV[p])||p}
document.querySelectorAll('img[data-ov]').forEach(function(i){i.src=R(i.dataset.ov)});
document.querySelectorAll('[data-bg]').forEach(function(e){e.style.backgroundImage='url('+R(e.dataset.bg)+')'});
for(var k in D)D[k].forEach(function(x){x.o=x.f;x.f=R(x.f)});deck(0)})();</script>''')
    open(os.path.join(OUT, 'index.html'), 'w').write(page)
    shutil.copy(os.path.join(ROOT, 'overzicht/powermarketing.html'), os.path.join(OUT, 'powermarketing.html'))
    n = 0
    for rel in hd_list():
        if 'ov/' + rel in page:
            os.makedirs(os.path.dirname(os.path.join(OUT, 'hd', rel)), exist_ok=True); shutil.copy(os.path.join(ROOT, 'overzicht/hd', rel), os.path.join(OUT, 'hd', rel)); n += 1
    print('hd', n, 'beelden')
    print('dist', OUT, len(used), 'beelden', round(os.path.getsize(os.path.join(OUT, 'ov.js')) / 1e6, 1), 'MB')
