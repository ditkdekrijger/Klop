"""Bouwt de publiceerbare versie van het overzicht in een map (standaard: dist/).
Beelden gebundeld in ov.js (één bestand), site als site.html met de configurator onder mx/.
Gebruik: python3 tools/pack_overzicht.py [OUTDIR]"""
import os, sys, json, base64, io, shutil, subprocess
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'dist')
os.makedirs(OUT, exist_ok=True)
subprocess.check_call([sys.executable, os.path.join(ROOT, 'tools/build_overzicht.py'), 'site.html', os.path.join(OUT, 'index.html'), 'ov/'])
# beelden bundelen
OV = {}
PAGE = open(os.path.join(OUT, 'index.html')).read()
src = os.path.join(ROOT, 'overzicht')
for d, _, ff in os.walk(os.path.join(src, 'ov')):
    for f in ff:
        p = os.path.join(d, f); rel = os.path.relpath(p, src)
        if rel not in PAGE: continue  # alleen beelden die het overzicht gebruikt
        if f.endswith('.png'):
            OV[rel] = 'data:image/png;base64,' + base64.b64encode(open(p, 'rb').read()).decode(); continue
        im = Image.open(p).convert('RGB')
        W = 800 if rel.startswith(('ov/pitch/site/', 'ov/pitch/proto/')) else 1200  # schermen: klein in de galerij, scherp via hd/
        if im.width > W: im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
        b = io.BytesIO(); im.save(b, 'JPEG', quality=72, optimize=True, progressive=True)
        OV[rel] = 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
open(os.path.join(OUT, 'ov.js'), 'w').write('window.OV=' + json.dumps(OV) + ';')
# index: beelden pas laden na ov.js
h = open(os.path.join(OUT, 'index.html')).read()
h = h.replace(' src="ov/', ' data-ov="ov/')
h = h.replace("style=\"background-image:url('ov/cover-showroom.jpg')\"", 'data-bg="ov/cover-showroom.jpg"')
assert h.count('deck(0);\n</script>') == 1
h = h.replace('deck(0);\n</script>', '''</script><script src="ov.js"></script><script>(function(){function R(p){return(window.OV&&OV[p])||p}
document.querySelectorAll('img[data-ov]').forEach(function(i){i.src=R(i.dataset.ov)});
document.querySelectorAll('[data-bg]').forEach(function(e){e.style.backgroundImage='url('+R(e.dataset.bg)+')'});
for(var k in D)D[k].forEach(function(x){x.o=x.f;x.f=R(x.f)});deck(0)})();</script>''')
open(os.path.join(OUT, 'index.html'), 'w').write(h)
# site met configurator
s = open(os.path.join(ROOT, 'site/index.html')).read()
assert s.count("var MXC='../maxima-configurator/public/';") == 1
open(os.path.join(OUT, 'site.html'), 'w').write(s.replace("var MXC='../maxima-configurator/public/';", "var MXC='mx/';"))
shutil.rmtree(os.path.join(OUT, 'mx'), ignore_errors=True)
pub = os.path.join(ROOT, 'maxima-configurator/public')
os.makedirs(os.path.join(OUT, 'mx'))
shutil.copy(os.path.join(pub, 'index.html'), os.path.join(OUT, 'mx', 'index.html'))
for x in ('assets', 'data'):
    shutil.copytree(os.path.join(pub, x), os.path.join(OUT, 'mx', x))
shutil.copy(os.path.join(ROOT, 'overzicht/powermarketing.html'), os.path.join(OUT, 'powermarketing.html'))
print('klaar:', OUT)

# scherpe (2x) beelden voor schermvullende weergave: gebundeld in kleine pakketjes hd/cN.js (de site gebruikt al veel losse bestanden),
# die pas laden zodra een sheet schermvullend opent
PAGE = open(os.path.join(OUT, 'index.html')).read(); HDC = {}; chunk = []; size = 0; n = 0
HDB = os.path.join(ROOT, 'overzicht/hd'); shutil.rmtree(os.path.join(OUT, 'hd'), ignore_errors=True); os.makedirs(os.path.join(OUT, 'hd'))
def flush():
    global chunk, size, n
    if not chunk: return
    open(os.path.join(OUT, 'hd', 'c%d.js' % n), 'w').write('(function(H){' + ''.join('H[%s]=%s;' % (json.dumps(r), json.dumps(u)) for r, u in chunk) + '})(window.HDX||(window.HDX={}));')
    chunk = []; size = 0; n += 1
for sub in ['recap', 'brandbook', 'merkuitingen', 'pitch']:
    for d, _, ff in sorted(os.walk(os.path.join(HDB, sub))):
        for f in sorted(ff):
            rel = os.path.relpath(os.path.join(d, f), HDB)
            if 'ov/' + rel not in PAGE: continue
            u = 'data:image/jpeg;base64,' + base64.b64encode(open(os.path.join(d, f), 'rb').read()).decode()
            HDC[rel] = n; chunk.append((rel, u)); size += len(u)
            if size > 3_500_000: flush()
flush()
PAGE = PAGE.replace('var HDC=null,', 'var HDC=' + json.dumps(HDC) + ',', 1); open(os.path.join(OUT, 'index.html'), 'w').write(PAGE)
print('hd', len(HDC), 'beelden in', n, 'pakketjes')
