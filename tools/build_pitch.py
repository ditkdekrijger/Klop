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
# Aangeleverde siteschermen (ontwerpoverzicht 16 november 2026). pdp-premium staat er bewust niet in: blauwe achtergrond achter Klop Premium Service.
SITE = [('home', 'home-hero', 'Homepage: opening, Vaar je vrijheid.'), ('home', 'home-zoeker', 'Wat voor vaarder ben je? Drie keuzes en een teller'),
 ('home', 'home-vrij', 'Vrijheid is geen boot'), ('home', 'home-premium', 'Wij regelen het gedoe. Jij vaart.'),
 ('home', 'home-showroom', '4.000 m² aan het water'), ('home', 'home-voorraad', 'Op voorraad bij Klop'), ('home', 'home-tijdlijn', 'Sinds 1966 aan de Rivierdijk'),
 ('home', 'm-home', 'Homepage op de telefoon'),
 ('aanbod', 'megamenu', 'Megamenu Boten'), ('aanbod', 'collectie', 'Alle boten'), ('aanbod', 'collectie-lijst', 'Filters en horizontale bootkaarten'),
 ('aanbod', 'soort', 'Soortpagina'), ('aanbod', 'pdp', 'Bootpagina: galerij en koopkolom'), ('aanbod', 'pdp-prijsinzicht', 'Prijsinzicht: zo verhoudt deze boot zich'),
 ('aanbod', 'm-collectie', 'Bootkaart op de telefoon'), ('aanbod', 'm-pdp', 'Bootpagina op de telefoon'),
 ('pag', 'showroom', 'Showroom: een boot koop je niet van een foto'), ('pag', 'premium-service', 'Klop Premium Service™: na de aankoop begint het pas'), ('pag', 'over-klop', 'Over Klop')]
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
    site = [dict(file='pitch/site/%s.jpg' % f, title=t, g=g) for g, f, t in SITE]
    def sg(g): return '<div class="grid sitegrid">' + ''.join(th('site', i, x) for i, x in enumerate(site) if x['g'] == g) + '</div>'
    code = open(os.path.join(ROOT, 'tools/code_sectie.html')).read()
    code = code[code.index('<div class="cx">'): code.rindex('</div></section>')]
    data = {k: [{'f': pfx + x['file'], 't': clean(x['title'])} for x in v] for k, v in {'recap': recap, 'brandbook': M['brandbook'], 'merk': M['merkuitingen'], 'site': site}.items()}
    page = open(os.path.join(ROOT, 'tools/pitch.template.html')).read()
    for k, v in {'{{CSS}}': CSS, '{{RECAP_STRIP}}': strip, '{{BB_GRID}}': bb, '{{MU_GRID}}': mu, '{{CODE_BODY}}': code,
                 '{{DATA}}': json.dumps(data, ensure_ascii=False), '{{HD}}': json.dumps(hd_list()), '{{HDP}}': hdp, '{{N_BB}}': str(len(M['brandbook'])), '{{N_MU}}': str(len(M['merkuitingen'])), '{{SITE_HOME}}': sg('home'), '{{SITE_AANBOD}}': sg('aanbod'), '{{SITE_PAG}}': sg('pag')}.items():
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
        im = Image.open(p).convert('RGB'); w = 1200 if '-lang' in rel else (1600 if ('pitch/mock' in rel or 'pitch/site/' in rel) else 1280)
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
