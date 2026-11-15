/*
 * Maxima configurator 2.0 (Klop Watersport)
 * Vanilla JS, geen build-stap. Data: data/models.json + data/<slug>.json (scripts/curate.py).
 *
 * URL-schema
 *   ?                         overzicht van alle modellen
 *   ?model=maxima-550         configurator voor dat model   (?p=1785 = Maxima product-id, werkt ook)
 *   &c=41651.41680.46034      gekozen opties als originele Maxima-optie-id's (compatibel met 1.0-links)
 *   &ral=rompkleur~7016       RAL-codes per groep
 *   &stap=3                   open stap (1-based; "overzicht" voor de laatste)
 *   &embed=1                  zonder eigen kop/voet (iframe in de Klop-site)
 */
(() => {
  'use strict';

  const CFG = Object.assign({
    dataPath: 'data/', endpoint: 'api/offerte.php', dealer: 'Klop Watersport',
    email: 'verkoop@klopwatersport.nl', phone: '+31184612227', phoneLabel: '0184 - 61 22 27',
    whatsapp: '31633180500', address: '',
  }, window.MX_CONFIG || {});

  const app = document.getElementById('app');
  const EMBED = document.documentElement.classList.contains('is-embed');
  // Koppeling met de Klop-site: in embed-modus meldt de configurator zijn stand aan de omringende pagina.
  const PARENT = EMBED && window.parent !== window ? window.parent : null;
  const tell = (type, data) => { if (PARENT) { try { PARENT.postMessage(Object.assign({ source: 'klop-mx', type }, data || {}), '*'); } catch { /* geen ouder */ } } };
  const VIEW_LABELS = { side: 'Zijkant', back: 'Achter', front: 'Voor' };
  const STORE_KEY = 'mx-config-v2';
  const SWATCH_GROUPS = new Set(['rompkleur', 'binnenkant', 'waterlijn', 'kabelaring', 'kussenset', 'buiskap']);

  // ---------- helpers ----------
  const money = (n, opts = {}) => {
    const v = Number(n || 0);
    const dec = Number.isInteger(v) ? 0 : 2;
    return (opts.sign ? '+ ' : '') + '€ ' + v.toLocaleString('nl-NL', { minimumFractionDigits: dec, maximumFractionDigits: dec });
  };
  const optPrice = (p) => (p ? money(p, { sign: true }) : 'Inbegrepen');
  const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const store = {
    all() { try { return JSON.parse(localStorage.getItem(STORE_KEY) || '{}'); } catch { return {}; } },
    get(k) { return this.all()[k]; },
    set(k, v) { try { const a = this.all(); if (v == null) delete a[k]; else a[k] = v; localStorage.setItem(STORE_KEY, JSON.stringify(a)); } catch { /* geen opslag */ } },
  };
  const jsonCache = new Map();
  const getJSON = (url) => {
    if (!jsonCache.has(url)) jsonCache.set(url, fetch(url).then((r) => { if (!r.ok) throw new Error(`${url}: ${r.status}`); return r.json(); }));
    return jsonCache.get(url);
  };
  const imgCache = new Map();
  const loadImg = (src) => {
    if (!imgCache.has(src)) {
      imgCache.set(src, new Promise((res) => {
        const i = new Image();
        i.onload = () => (i.decode ? i.decode().catch(() => {}) : Promise.resolve()).then(() => res(i));
        i.onerror = () => res(null);
        i.src = src;
      }));
    }
    return imgCache.get(src);
  };
  const isElectric = (m) => /elektris|electris/i.test(m.name);
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;

  document.querySelectorAll('[data-dealer]').forEach((el) => { el.textContent = CFG.dealer; });
  document.querySelectorAll('[data-phone-link]').forEach((a) => { a.href = 'tel:' + CFG.phone; });
  document.querySelectorAll('[data-phone-label]').forEach((el) => { el.textContent = CFG.phoneLabel; });
  document.querySelectorAll('[data-address]').forEach((el) => { if (CFG.address) el.textContent = CFG.address; });

  // ---------- routing ----------
  function route() {
    const q = new URLSearchParams(location.search);
    getJSON(CFG.dataPath + 'models.json').then((models) => {
      const slug = q.get('model');
      const pid = q.get('p');
      const meta = slug ? models.find((m) => m.slug === slug) : pid ? models.find((m) => String(m.id) === pid) : null;
      if (meta) return renderConfigurator(meta, q);
      return renderOverview(models);
    }).catch((err) => {
      console.error(err);
      app.innerHTML = `<div class="wrap app__error"><h1>De configurator kon niet geladen worden</h1>
        <p>Probeer het later opnieuw of bel ons op <a href="tel:${esc(CFG.phone)}">${esc(CFG.phoneLabel)}</a>.</p></div>`;
    });
  }
  function navigate(params) {
    const q = new URLSearchParams(params);
    if (EMBED) q.set('embed', '1');
    history.pushState(null, '', q.toString() ? '?' + q : location.pathname);
    window.scrollTo(0, 0);
    route();
  }
  window.addEventListener('popstate', route);
  document.addEventListener('click', (e) => {
    const a = e.target.closest('[data-nav="overview"]');
    if (a && !e.metaKey && !e.ctrlKey) { e.preventDefault(); navigate({}); }
  });

  // =====================================================================
  // Overzicht
  // =====================================================================
  function renderOverview(models) {
    document.title = 'Stel je Maxima samen | ' + CFG.dealer;
    tell('overview');
    const st = { q: '', drive: 'all', sort: 'price-asc' };
    const len = (m) => parseFloat(String(m.specs?.Lengte || '0').replace(',', '.')) || 0;

    app.innerHTML = `
      <section class="ov-hero">
        <div class="wrap">
          <p class="eyebrow">Maxima Boats configurator</p>
          <h1>Stel je Maxima samen.</h1>
          <p class="ov-hero__lead">Kies een model en bepaal stap voor stap romp, kussens, buiskap, motor en opties. Je ziet direct hoe je boot eruitziet en wat hij kost.</p>
        </div>
      </section>
      <section class="wrap ov">
        <div class="ov-bar">
          <label class="ov-search"><span class="sr-only">Zoek een model</span>
            <input type="search" placeholder="Zoek een model, bijv. 650" data-f="q"></label>
          <div class="chips" role="group" aria-label="Aandrijving">
            <button type="button" class="chip is-on" data-drive="all" aria-pressed="true">Alle</button>
            <button type="button" class="chip" data-drive="fuel" aria-pressed="false">Brandstof</button>
            <button type="button" class="chip" data-drive="electric" aria-pressed="false">Elektrisch</button>
          </div>
          <label class="ov-sort"><span class="sr-only">Sorteren</span>
            <select data-f="sort">
              <option value="price-asc">Prijs oplopend</option>
              <option value="price-desc">Prijs aflopend</option>
              <option value="length">Lengte</option>
              <option value="name">Naam</option>
            </select></label>
        </div>
        <p class="ov-count" data-count aria-live="polite"></p>
        <div class="ov-grid" data-grid></div>
      </section>`;

    const grid = app.querySelector('[data-grid]');
    const draw = () => {
      let list = models.filter((m) => m.name.toLowerCase().includes(st.q.trim().toLowerCase()));
      if (st.drive === 'electric') list = list.filter(isElectric);
      if (st.drive === 'fuel') list = list.filter((m) => !isElectric(m));
      const sorters = {
        'price-asc': (a, b) => a.basePrice - b.basePrice,
        'price-desc': (a, b) => b.basePrice - a.basePrice,
        length: (a, b) => len(a) - len(b) || a.basePrice - b.basePrice,
        name: (a, b) => a.name.localeCompare(b.name, 'nl', { numeric: true }),
      };
      list.sort(sorters[st.sort]);
      app.querySelector('[data-count]').textContent = `${list.length} ${list.length === 1 ? 'model' : 'modellen'}`;
      const saved = store.all();
      grid.innerHTML = list.length ? list.map((m) => `
        <a class="mcard" href="?model=${esc(m.slug)}" data-slug="${esc(m.slug)}">
          <span class="mcard__img">${m.image ? `<img src="${esc(m.image)}" alt="" loading="lazy">` : ''}
            ${isElectric(m) ? '<span class="mcard__tag">Elektrisch</span>' : ''}
            ${saved[m.slug]?.c ? '<span class="mcard__tag mcard__tag--saved">Jouw samenstelling</span>' : ''}</span>
          <span class="mcard__body">
            <span class="mcard__name">${esc(m.name)}</span>
            <span class="mcard__specs">
              ${m.specs?.Lengte ? `<span>${esc(m.specs.Lengte)}</span>` : ''}
              ${m.specs?.['Aantal personen'] ? `<span>${esc(m.specs['Aantal personen'])} personen</span>` : ''}
              ${m.specs?.['Zichtbaarheid motor'] ? `<span>${esc(m.specs['Zichtbaarheid motor'])}</span>` : ''}
            </span>
            <span class="mcard__foot"><span class="mcard__price"><small>Vanaf</small>${money(m.basePrice)}</span>
              <span class="mcard__go">Stel samen <span aria-hidden="true">→</span></span></span>
          </span>
        </a>`).join('') : '<p class="ov-empty">Geen modellen gevonden.</p>';
    };
    app.querySelector('[data-f="q"]').addEventListener('input', (e) => { st.q = e.target.value; draw(); });
    app.querySelector('[data-f="sort"]').addEventListener('change', (e) => { st.sort = e.target.value; draw(); });
    app.querySelectorAll('[data-drive]').forEach((b) => b.addEventListener('click', () => {
      app.querySelectorAll('[data-drive]').forEach((x) => { const on = x === b; x.classList.toggle('is-on', on); x.setAttribute('aria-pressed', String(on)); });
      st.drive = b.dataset.drive; draw();
    }));
    grid.addEventListener('click', (e) => {
      const card = e.target.closest('[data-slug]');
      if (!card || e.metaKey || e.ctrlKey) return;
      e.preventDefault();
      const saved = store.get(card.dataset.slug) || {};
      navigate(Object.assign({ model: card.dataset.slug }, saved.c ? { c: saved.c } : {}, saved.ral ? { ral: saved.ral } : {}));
    });
    draw();
  }

  // =====================================================================
  // Configurator
  // =====================================================================
  async function renderConfigurator(meta, q) {
    app.innerHTML = `<div class="app__loading"><span class="spinner"></span> ${esc(meta.name)} laden…</div>`;
    const model = await getJSON(CFG.dataPath + meta.slug + '.json');
    document.title = `Stel je ${model.name} samen | ${CFG.dealer}`;

    // ----- index: groepen en optie-id's -----
    const groups = [];             // alle groepen in volgorde, met .section
    const gByKey = new Map();
    const idIndex = new Map();     // Maxima-optie-id -> { g, o, stitch }
    model.sections.forEach((s, si) => s.groups.forEach((g) => {
      g.sectionIndex = si;
      groups.push(g); gByKey.set(g.key, g);
      if (g.type === 'stitch') return;
      g.options.forEach((o) => {
        idIndex.set(String(o.id), { g, o, stitch: false });
        if (o.stitch) idIndex.set(String(o.stitch.id), { g, o, stitch: true });
      });
    }));
    const isSingle = (g) => g.type === 'single' || g.type === 'one' || g.type === 'stitch';
    const stitchGroup = gByKey.get('stiksel');

    // ----- selectie -----
    const sel = new Map();         // key -> string (single) of Set (many)
    const ral = new Map();         // key -> RAL-code
    groups.forEach((g) => sel.set(g.key, isSingle(g) ? null : new Set()));
    if (stitchGroup) sel.set('stiksel', 'glad');

    const saved = store.get(model.slug) || {};
    const codes = q.has('c') ? q.get('c') : (saved.c || '');
    String(codes).split('.').filter(Boolean).forEach((id) => {
      const hit = idIndex.get(id);
      if (!hit) return;
      if (isSingle(hit.g)) sel.set(hit.g.key, String(hit.o.id));
      else sel.get(hit.g.key).add(String(hit.o.id));
      if (hit.stitch && stitchGroup) sel.set('stiksel', 'ruitjes');
    });
    String(q.has('ral') ? q.get('ral') : (saved.ral || '')).split(',').filter(Boolean).forEach((pair) => {
      const [k, v] = pair.split('~');
      if (gByKey.has(k) && v) ral.set(k, decodeURIComponent(v).slice(0, 40));
    });

    const optOf = (g, id) => g.options.find((o) => String(o.id) === String(id));
    const chosenOpts = (g) => {
      const v = sel.get(g.key);
      if (v == null) return [];
      return (v instanceof Set ? [...v] : [v]).map((id) => optOf(g, id)).filter(Boolean);
    };
    const ruitjes = () => stitchGroup && sel.get('stiksel') === 'ruitjes';

    /** Alles wat meetelt: per gekozen optie de echte Maxima-optie, prijs en weergavenaam. */
    function resolved() {
      const out = [];
      groups.forEach((g) => {
        if (g.type === 'stitch') return;
        chosenOpts(g).forEach((o) => {
          const useStitch = g.key === 'kussenset' && o.stitch && ruitjes();
          const r = {
            group: g, opt: o,
            id: useStitch ? o.stitch.id : o.id,
            price: useStitch ? o.stitch.price : o.price,
            layerId: useStitch ? (o.stitch.layerId || o.layerId) : o.layerId,
            name: o.name + (useStitch ? ', ruitjesstiksel' : ''),
            raw: useStitch ? `${o.raw} ruitjes` : o.raw,
          };
          if (o.ral && ral.get(g.key)) { r.ral = ral.get(g.key); r.name += ` (RAL ${r.ral})`; }
          out.push(r);
        });
      });
      return out;
    }
    const optionsTotal = () => resolved().reduce((a, r) => a + r.price, 0);
    const fixedTotal = model.fixedCosts.reduce((a, c) => a + c.price, 0);
    const total = () => model.basePrice + fixedTotal + optionsTotal();
    const groupDone = (g) => (isSingle(g) ? sel.get(g.key) != null : true);
    const ralMissing = (g) => chosenOpts(g).some((o) => o.ral) && !ral.get(g.key);
    const missing = () => groups.filter((g) => (g.required && !groupDone(g)) || ralMissing(g));
    const sectionDone = (s) => s.groups.every((g) => (!g.required || groupDone(g)) && !ralMissing(g));

    // ----- stappen -----
    const steps = [...model.sections.map((s, i) => ({ type: 'section', s, i })), { type: 'overview' }];
    const stepParam = q.get('stap');
    let step = stepParam === 'overzicht' ? steps.length - 1 : Math.min(Math.max(parseInt(stepParam || '1', 10) - 1 || 0, 0), steps.length - 1);

    const hasLayers = model.views.length > 0 && model.layers.length > 0;
    let view = model.defaultView || model.views[0];

    // ----- skelet -----
    app.innerHTML = `
      <div class="cx" data-cx>
        <div class="cx-top">
          <div class="wrap cx-top__in">
            <div class="cx-top__id">
              <a class="cx-back" href="?" data-nav="overview">← Alle boten</a>
              <h1 class="cx-title">${esc(model.name)}</h1>
            </div>
            <div class="cx-top__price">
              <button type="button" class="cx-total" data-open-spec aria-haspopup="dialog">
                <small>Totaalprijs</small><strong data-total></strong>
              </button>
              <button type="button" class="btn btn--gold" data-goto-overview>Offerte aanvragen</button>
            </div>
          </div>
        </div>

        <div class="wrap cx-body">
          <section class="cx-stage" aria-label="Voorbeeld">
            <div class="stage ${hasLayers ? '' : 'stage--photo'}" data-stage>
              ${hasLayers ? '' : `<img class="stage__photo" src="${esc(model.image)}" alt="${esc(model.name)}">`}
              <span class="stage__loader" data-loader aria-hidden="true"><span class="spinner"></span></span>
            </div>
            ${hasLayers ? `<div class="stage__views" role="tablist" aria-label="Aanzicht">${model.views.map((v) =>
              `<button type="button" role="tab" class="vtab" data-view="${esc(v)}" aria-selected="${v === view}">${esc(VIEW_LABELS[v] || v)}</button>`).join('')}</div>` : ''}
            <p class="stage__note">${hasLayers ? 'Impressie. Je boot kan in werkelijkheid afwijken.' : 'Foto ter impressie. Voor dit model is nog geen samenstelbeeld beschikbaar.'}</p>
            <button type="button" class="cx-help" data-open-help>Hulp nodig bij het samenstellen?</button>
          </section>

          <section class="cx-panel" aria-label="Samenstellen">
            <nav class="stepnav" aria-label="Stappen"><ol data-stepnav></ol></nav>
            <div class="cx-step" data-step tabindex="-1"></div>
          </section>
        </div>

        <div class="cx-mbar">
          <button type="button" class="cx-mbar__total" data-open-spec><small>Totaal</small><strong data-total></strong></button>
          <button type="button" class="btn btn--gold" data-mnext></button>
        </div>
      </div>

      <dialog class="modal" data-spec aria-labelledby="spec-t">
        <div class="modal__head"><h2 id="spec-t">Prijsopbouw</h2><button type="button" class="modal__x" data-close aria-label="Sluiten">×</button></div>
        <div class="modal__body" data-spec-body></div>
      </dialog>
      <dialog class="modal" data-help aria-labelledby="help-t">
        <div class="modal__head"><h2 id="help-t">Hulp bij samenstellen</h2><button type="button" class="modal__x" data-close aria-label="Sluiten">×</button></div>
        <form class="modal__body" data-help-form novalidate>
          <p class="muted">Liever persoonlijk advies? Laat je gegevens achter, dan neemt een adviseur van ${esc(CFG.dealer)} contact met je op.
            Bellen kan ook: <a href="tel:${esc(CFG.phone)}">${esc(CFG.phoneLabel)}</a>, of <a href="https://wa.me/${esc(CFG.whatsapp)}" target="_blank" rel="noopener">stuur een WhatsApp</a>.</p>
          <div class="fgrid">
            ${field('name', 'Naam', true, 'text', 'full')}
            ${field('phone', 'Telefoonnummer', true, 'tel')}
            ${field('email', 'E-mailadres', true, 'email')}
            <label class="field full"><span>Opmerking <em>optioneel</em></span><textarea name="remarks" rows="3"></textarea></label>
            <label class="hp" aria-hidden="true">Laat leeg<input name="website" tabindex="-1" autocomplete="off"></label>
          </div>
          <p class="fmsg" data-fmsg role="status" hidden></p>
          <div class="factions"><button type="submit" class="btn btn--ink">Verstuur</button></div>
        </form>
      </dialog>
      <dialog class="modal modal--zoom" data-zoom aria-labelledby="zoom-t">
        <div class="modal__head"><h2 id="zoom-t" data-zoom-title></h2><button type="button" class="modal__x" data-close aria-label="Sluiten">×</button></div>
        <img data-zoom-img alt="">
      </dialog>
      <div class="print" data-print aria-hidden="true"></div>`;

    const $ = (s) => app.querySelector(s);
    const $$ = (s) => [...app.querySelectorAll(s)];
    const stepEl = $('[data-step]');

    // ----- beeld -----
    const stage = $('[data-stage]');
    const loader = $('[data-loader]');
    const layerEls = {};
    const layerSrc = (v, layer, id) => `${model.imageBase}${v}/${layer}/${id}.png`;
    const fullSrc = (v) => `${model.imageBase}${v}/full.png`;
    if (hasLayers) {
      ['full', ...model.layers].forEach((name) => {   // full.png is de basis, opties liggen erop
        const img = document.createElement('img');
        img.className = 'stage__layer';
        img.alt = name === 'full' ? model.name : '';
        img.hidden = true;
        stage.insertBefore(img, loader);
        layerEls[name] = img;
      });
    }
    function layerChoices() {
      const out = {};
      resolved().forEach((r) => { if (r.opt.layer && r.layerId) out[r.opt.layer] = r.layerId; });
      return out;
    }
    let drawToken = 0;
    async function drawStage() {
      if (!hasLayers) return;
      const token = ++drawToken;
      const ch = layerChoices();
      const jobs = [['full', fullSrc(view)], ...model.layers.map((l) => [l, ch[l] ? layerSrc(view, l, ch[l]) : null])];
      loader.classList.add('is-on');
      const imgs = await Promise.all(jobs.map(([, src]) => (src ? loadImg(src) : null)));
      if (token !== drawToken) return;
      jobs.forEach(([name, src], i) => {
        const el = layerEls[name];
        if (src && imgs[i]) { el.src = src; el.hidden = false; } else { el.hidden = true; }
      });
      loader.classList.remove('is-on');
    }
    function warmLayers(sectionIdx) {
      if (!hasLayers) return;
      const idle = window.requestIdleCallback || ((fn) => setTimeout(fn, 300));
      idle(() => model.sections[sectionIdx]?.groups.forEach((g) => g.options.forEach((o) => {
        if (o.layer && o.layerId) loadImg(layerSrc(view, o.layer, o.layerId));
      })));
    }
    $$('[data-view]').forEach((b) => b.addEventListener('click', () => {
      view = b.dataset.view;
      $$('[data-view]').forEach((x) => x.setAttribute('aria-selected', String(x === b)));
      drawStage();
    }));

    // ----- stapnavigatie -----
    function drawStepNav() {
      $('[data-stepnav]').innerHTML = steps.map((st, i) => {
        const done = st.type === 'section' ? sectionDone(st.s) : missing().length === 0;
        const label = st.type === 'section' ? st.s.title : 'Overzicht';
        return `<li><button type="button" data-go="${i}" class="${i === step ? 'is-on' : ''} ${done && st.type === 'section' ? 'is-done' : ''}" ${i === step ? 'aria-current="step"' : ''}>
          <span class="stepnav__n">${st.type === 'section' ? i + 1 : '✓'}</span><span>${esc(label)}</span></button></li>`;
      }).join('');
      const cur = $('[data-stepnav] .is-on');
      if (cur) cur.scrollIntoView({ block: 'nearest', inline: 'center', behavior: reduceMotion ? 'auto' : 'smooth' });
    }
    function groupTag(g) {
      if (g.required) return '<span class="gtag gtag--req">verplicht</span>';
      if (g.type === 'one') return '<span class="gtag">optioneel, kies er één</span>';
      return '<span class="gtag">meerdere mogelijk</span>';
    }

    function renderSection(s, i) {
      const next = steps[i + 1];
      return `
        <p class="cx-step__count">Stap ${i + 1} van ${model.sections.length}</p>
        <h2 class="cx-step__title">${esc(s.title)}</h2>
        <p class="cx-step__intro">${esc(s.intro)}</p>
        ${s.groups.map((g) => renderGroup(g)).join('')}
        <div class="cx-step__nav">
          ${i > 0 ? `<button type="button" class="btn btn--line" data-go="${i - 1}">← Vorige</button>` : '<span></span>'}
          <button type="button" class="btn btn--ink" data-go="${i + 1}">${next.type === 'overview' ? 'Naar overzicht' : 'Volgende: ' + esc(next.s.title)} →</button>
        </div>`;
    }

    function renderGroup(g) {
      const type = g.type === 'many' ? 'checkbox' : 'radio';
      const name = 'g-' + g.key;
      const cur = sel.get(g.key);
      const isOn = (o) => (cur instanceof Set ? cur.has(String(o.id)) : String(cur) === String(o.id));
      const hasImg = g.options.some((o) => o.image);
      const swatch = SWATCH_GROUPS.has(g.key) && !hasImg;
      const opts = g.options.map((o) => {
        let price = optPrice(o.price);
        if (g.type === 'stitch' && o.id === 'ruitjes') price = o.priceFrom != null ? 'vanaf ' + money(o.priceFrom, { sign: true }) : optPrice(o.price);
        return `
          <label class="opt ${hasImg ? 'opt--img' : ''}">
            <input type="${type}" name="${name}" value="${esc(o.id)}" ${isOn(o) ? 'checked' : ''} data-g="${esc(g.key)}">
            ${hasImg ? `<span class="opt__img">${o.image ? `<img src="${esc(o.image)}" alt="" loading="lazy">
              <button type="button" class="opt__zoom" data-zoom-src="${esc(o.image)}" data-zoom-name="${esc(o.name)}" aria-label="Foto van ${esc(o.name)} vergroten">⤢</button>` : ''}</span>` : ''}
            ${swatch ? `<span class="opt__sw" style="${swatchCss(g.key, o.name)}"></span>` : ''}
            <span class="opt__txt"><span class="opt__name">${esc(o.name)}</span>${o.sub ? `<span class="opt__sub">${esc(o.sub)}</span>` : ''}<span class="opt__price">${price}</span></span>
            <span class="opt__mark" aria-hidden="true"></span>
          </label>`;
      }).join('');
      const none = g.type === 'one' ? `
          <label class="opt opt--none">
            <input type="radio" name="${name}" value="" ${cur == null ? 'checked' : ''} data-g="${esc(g.key)}">
            <span class="opt__txt"><span class="opt__name">Geen</span></span><span class="opt__mark" aria-hidden="true"></span>
          </label>` : '';
      const needsRal = chosenOpts(g).some((o) => o.ral);
      return `
        <fieldset class="grp ${ralMissing(g) ? 'has-warn' : ''}" data-grp="${esc(g.key)}">
          <legend class="grp__head"><span class="grp__title">${esc(g.title)}</span>${groupTag(g)}</legend>
          ${g.hint ? `<p class="grp__hint">${esc(g.hint)}</p>` : ''}
          <div class="opts ${hasImg ? 'opts--img' : ''}">${none}${opts}</div>
          ${needsRal ? `<label class="ral"><span>RAL-code <em>verplicht</em></span>
            <input type="text" inputmode="numeric" maxlength="40" placeholder="bijv. 7016" value="${esc(ral.get(g.key) || '')}" data-ral="${esc(g.key)}" aria-describedby="ral-${esc(g.key)}">
            <small id="ral-${esc(g.key)}">Het voorbeeld toont wit. Wij spuiten de kleur die je opgeeft.</small></label>` : ''}
        </fieldset>`;
    }

    function renderOverviewStep() {
      const miss = missing();
      const rs = resolved();
      const optCount = rs.length;
      return `
        <p class="cx-step__count">Overzicht</p>
        <h2 class="cx-step__title">Jouw ${esc(model.name)}</h2>
        <p class="cx-step__intro">Controleer je keuzes en vraag een vrijblijvende offerte aan.</p>
        ${miss.length ? `<div class="warn" role="alert"><b>Nog niet compleet.</b> Kies nog:
          <ul>${miss.map((g) => `<li><button type="button" class="lnk" data-go="${g.sectionIndex}" data-focus="${esc(g.key)}">${esc(g.title)}${ralMissing(g) && groupDone(g) ? ' (RAL-code)' : ''}</button></li>`).join('')}</ul></div>` : ''}
        <div class="sum">
          ${model.sections.map((s, si) => {
            const rows = s.groups.filter((g) => g.type !== 'stitch').map((g) => {
              const items = rs.filter((r) => r.group === g);
              if (!items.length && !g.required) return '';
              return `<div class="sum__row"><span class="sum__g">${esc(g.title)}</span>
                <span class="sum__v">${items.length ? items.map((r) => `<span>${esc(r.name)}<b>${r.price ? money(r.price) : ''}</b></span>`).join('') : '<span class="sum__miss">Nog niet gekozen</span>'}</span></div>`;
            }).join('');
            return `<section class="sum__sec"><header><h3>${esc(s.title)}</h3><button type="button" class="lnk" data-go="${si}">Wijzig</button></header>
              ${rows || '<p class="sum__none">Geen keuzes</p>'}</section>`;
          }).join('')}
        </div>
        <dl class="price">
          <div><dt>Basisprijs ${esc(model.name)}</dt><dd>${money(model.basePrice)}</dd></div>
          <div><dt>Opties (${optCount})</dt><dd>${money(optionsTotal())}</dd></div>
          ${model.fixedCosts.map((c) => `<div><dt>${esc(c.label)}</dt><dd>${money(c.price)}</dd></div>`).join('')}
          <div class="price__total"><dt>Totaal</dt><dd>${money(total())}</dd></div>
        </dl>
        <div class="tools">
          <button type="button" class="btn btn--line" data-print-btn>Print of bewaar als pdf</button>
          <button type="button" class="btn btn--line" data-share>Kopieer link</button>
          <button type="button" class="lnk" data-reset>Opnieuw beginnen</button>
        </div>

        <form class="quote" data-quote novalidate>
          <h3>Offerte aanvragen</h3>
          <p class="muted">Vrijblijvend. ${esc(CFG.dealer)} neemt binnen twee werkdagen contact met je op.</p>
          <div class="fgrid">
            ${field('firstname', 'Voornaam', true)}
            ${field('lastname', 'Achternaam', true)}
            ${field('email', 'E-mailadres', true, 'email')}
            ${field('phone', 'Telefoonnummer', true, 'tel')}
            ${field('street', 'Straat')}
            ${field('housenumber', 'Huisnummer')}
            ${field('zipcode', 'Postcode')}
            ${field('city', 'Plaats', true)}
            <label class="field full"><span>Land</span><select name="country">${['Nederland', 'België', 'Duitsland', 'Frankrijk', 'Luxemburg', 'Oostenrijk', 'Zwitserland', 'Spanje', 'Italië', 'Verenigd Koninkrijk', 'Anders'].map((c) => `<option>${c}</option>`).join('')}</select></label>
            <label class="field full"><span>Opmerking <em>optioneel</em></span><textarea name="remarks" rows="3"></textarea></label>
            <label class="hp" aria-hidden="true">Laat leeg<input name="website" tabindex="-1" autocomplete="off"></label>
            <label class="check full"><input type="checkbox" name="agree" required><span>Ik vind het goed dat ${esc(CFG.dealer)} contact met me opneemt over deze aanvraag.</span></label>
          </div>
          <p class="fmsg" data-fmsg role="status" hidden></p>
          <div class="factions"><button type="submit" class="btn btn--gold">Offerte aanvragen</button></div>
          ${miss.length ? '<p class="muted small">Maak eerst je samenstelling compleet.</p>' : ''}
        </form>`;
    }

    function drawStep(focus) {
      const st = steps[step];
      stepEl.innerHTML = st.type === 'section' ? renderSection(st.s, st.i) : renderOverviewStep();
      stepEl.dataset.kind = st.type;
      drawStepNav();
      updateBars();
      if (st.type === 'section') { warmLayers(st.i); warmLayers(st.i + 1); }
      if (focus) {
        const target = typeof focus === 'string' ? stepEl.querySelector(`[data-grp="${CSS.escape(focus)}"]`) : stepEl;
        (target || stepEl).scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'start' });
        stepEl.focus({ preventScroll: true });
      }
    }

    function goTo(i, focus = true) {
      step = Math.max(0, Math.min(steps.length - 1, i));
      drawStep(focus);
      persist();
    }

    function updateBars() {
      $$('[data-total]').forEach((el) => { el.textContent = money(total()); });
      const mnext = $('[data-mnext]');
      if (steps[step].type === 'overview') { mnext.textContent = 'Offerte aanvragen'; mnext.dataset.target = 'quote'; }
      else { mnext.textContent = steps[step + 1].type === 'overview' ? 'Naar overzicht' : 'Volgende'; mnext.dataset.target = String(step + 1); }
    }

    // ----- opslaan + URL -----
    function encodeC() { return resolved().map((r) => r.id).join('.'); }
    function encodeRal() { return [...ral].filter(([k, v]) => v && chosenOpts(gByKey.get(k)).some((o) => o.ral)).map(([k, v]) => `${k}~${encodeURIComponent(v)}`).join(','); }
    function persist() {
      const qq = new URLSearchParams();
      qq.set('model', model.slug);
      const c = encodeC(); if (c) qq.set('c', c);
      const r = encodeRal(); if (r) qq.set('ral', r);
      qq.set('stap', steps[step].type === 'overview' ? 'overzicht' : String(step + 1));
      if (EMBED) qq.set('embed', '1');
      history.replaceState(null, '', '?' + qq);
      store.set(model.slug, c || r ? { c, ral: r } : null);
      tell('state', {
        slug: model.slug, name: model.name, total: total(), c, ral: r, stap: qq.get('stap'),
        complete: missing().length === 0,
        picks: resolved().map((x) => [x.group.key, x.group.title, x.name]),
      });
    }

    // ----- interactie -----
    stepEl.addEventListener('change', (e) => {
      const inp = e.target;
      if (!inp.dataset.g) return;
      const g = gByKey.get(inp.dataset.g);
      if (g.type === 'many') {
        const set = sel.get(g.key);
        if (inp.checked) set.add(inp.value); else set.delete(inp.value);
      } else {
        sel.set(g.key, inp.value === '' ? null : inp.value);
      }
      // RAL-veld tonen/verbergen zonder de hele stap opnieuw te tekenen
      const fs = inp.closest('.grp');
      const hadRal = !!fs.querySelector('[data-ral]');
      const needsRal = chosenOpts(g).some((o) => o.ral);
      if (hadRal !== needsRal) {
        fs.outerHTML = renderGroup(g);
        if (needsRal) stepEl.querySelector(`[data-ral="${CSS.escape(g.key)}"]`)?.focus();
      }
      drawStepNav();
      updateBars();
      drawStage();
      persist();
    });
    stepEl.addEventListener('input', (e) => {
      const k = e.target.dataset.ral;
      if (!k) return;
      ral.set(k, e.target.value.trim());
      e.target.closest('.grp').classList.toggle('has-warn', !e.target.value.trim());
      drawStepNav();
      persist();
    });
    app.addEventListener('click', (e) => {
      const go = e.target.closest('[data-go]');
      if (go) { goTo(+go.dataset.go, go.dataset.focus || true); return; }
      const z = e.target.closest('[data-zoom-src]');
      if (z) {
        e.preventDefault();
        $('[data-zoom-img]').src = z.dataset.zoomSrc;
        $('[data-zoom-img]').alt = z.dataset.zoomName;
        $('[data-zoom-title]').textContent = z.dataset.zoomName;
        $('[data-zoom]').showModal();
        return;
      }
      if (e.target.closest('[data-open-spec]')) { $('[data-spec-body]').innerHTML = specTable(); $('[data-spec]').showModal(); return; }
      if (e.target.closest('[data-open-help]')) { $('[data-help]').showModal(); return; }
      if (e.target.closest('[data-goto-overview]')) { goToQuote(); return; }
      const mn = e.target.closest('[data-mnext]');
      if (mn) { if (mn.dataset.target === 'quote') focusQuote(); else goTo(+mn.dataset.target); return; }
      if (e.target.closest('[data-print-btn]')) { printSheet(); return; }
      if (e.target.closest('[data-share]')) { share(e.target.closest('[data-share]')); return; }
      if (e.target.closest('[data-reset]')) {
        if (!confirm('Alle keuzes voor deze boot wissen?')) return;
        groups.forEach((g) => sel.set(g.key, isSingle(g) ? null : new Set()));
        if (stitchGroup) sel.set('stiksel', 'glad');
        ral.clear();
        drawStage();
        goTo(0);
      }
    });
    function goToQuote() { if (steps[step].type !== 'overview') goTo(steps.length - 1, false); focusQuote(); }
    function focusQuote() {
      const f = $('[data-quote]');
      if (!f) return;
      f.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'start' });
      setTimeout(() => f.querySelector('input[name="firstname"]').focus({ preventScroll: true }), reduceMotion ? 0 : 450);
    }

    $$('dialog').forEach((d) => d.addEventListener('click', (e) => { if (e.target === d || e.target.closest('[data-close]')) d.close(); }));

    function specTable() {
      const rs = resolved();
      return `<table class="spec"><tbody>
        <tr><th>Basisprijs ${esc(model.name)}</th><td>${money(model.basePrice)}</td></tr>
        ${rs.map((r) => `<tr><th><small>${esc(r.group.title)}</small>${esc(r.name)}</th><td>${money(r.price)}</td></tr>`).join('')}
        ${model.fixedCosts.map((c) => `<tr><th>${esc(c.label)}</th><td>${money(c.price)}</td></tr>`).join('')}
        </tbody><tfoot><tr><th>Totaal</th><td>${money(total())}</td></tr></tfoot></table>
        ${missing().length ? `<p class="muted small">Nog niet compleet: ${missing().map((g) => esc(g.title.toLowerCase())).join(', ')}.</p>` : ''}`;
    }

    async function share(btn) {
      const url = location.href.replace(/([?&])embed=1&?/, '$1').replace(/[?&]$/, '');
      try { await navigator.clipboard.writeText(url); btn.textContent = 'Link gekopieerd'; }
      catch { prompt('Kopieer deze link:', url); }
      setTimeout(() => { btn.textContent = 'Kopieer link'; }, 2500);
    }

    async function printSheet() {
      const sheet = $('[data-print]');
      let boat = '';
      if (hasLayers) {
        const ch = layerChoices();
        const srcs = [fullSrc(view), ...model.layers.filter((l) => ch[l]).map((l) => layerSrc(view, l, ch[l]))];
        boat = `<div class="print__boat">${srcs.map((s) => `<img src="${esc(s)}" alt="">`).join('')}</div>`;
      } else if (model.image) boat = `<div class="print__boat"><img src="${esc(model.image)}" alt=""></div>`;
      sheet.innerHTML = `
        <header class="print__head"><img src="assets/maxima-logo-wit.svg" alt="Maxima Boats"><div><h1>${esc(model.name)}</h1>
          <p>Samenstelling van ${new Date().toLocaleDateString('nl-NL', { day: 'numeric', month: 'long', year: 'numeric' })} · via ${esc(CFG.dealer)}</p></div></header>
        ${boat}${specTable()}
        <p class="print__foot">${esc(CFG.dealer)} · ${esc(CFG.address)} · ${esc(CFG.phoneLabel)} · ${esc(CFG.email)}<br>
          Deze samenstelling is een indicatie; aan de prijzen kunnen geen rechten worden ontleend.<br>${esc(location.href.replace(/([?&])embed=1&?/, '$1'))}</p>`;
      await Promise.all([...sheet.querySelectorAll('img')].map((i) => (i.complete ? null : new Promise((r) => { i.onload = i.onerror = r; }))));
      window.print();
    }

    // ----- formulieren -----
    function payload(form, type) {
      const data = Object.fromEntries(new FormData(form).entries());
      return {
        type, model: model.name, modelId: model.id,
        configUrl: location.href.replace(/([?&])embed=1&?/, '$1').replace(/[?&]$/, ''),
        options: resolved().map((r) => ({ step: r.group.title, name: r.name, maximaName: r.raw, maximaId: r.id, price: r.price, ral: r.ral || null })),
        basePrice: model.basePrice, fixedCosts: model.fixedCosts, total: total(),
        complete: missing().length === 0,
        contact: data,
      };
    }
    function mailto(p) {
      const head = `${p.type === 'help' ? 'Hulpaanvraag' : 'Offerteaanvraag'} ${p.model}`;
      const lines = [
        ...Object.entries(p.contact).filter(([k, v]) => v && !['website', 'agree'].includes(k)).map(([k, v]) => `${k}: ${v}`), '',
        `Basisprijs: ${money(p.basePrice)}`,
        ...p.options.map((o) => `${o.step}: ${o.name} (${money(o.price)})`),
        ...p.fixedCosts.map((c) => `${c.label}: ${money(c.price)}`),
        `Totaal: ${money(p.total)}`, '', p.configUrl,
      ];
      location.href = `mailto:${CFG.email}?subject=${encodeURIComponent(head)}&body=${encodeURIComponent(lines.join('\n'))}`;
    }
    async function submit(form, type, precheck) {
      const msg = form.querySelector('[data-fmsg]');
      msg.hidden = true; msg.className = 'fmsg';
      form.querySelectorAll('.is-bad').forEach((x) => x.classList.remove('is-bad'));
      const bad = [...form.querySelectorAll('[required]')].filter((i) => (i.type === 'checkbox' ? !i.checked
        : !i.value.trim() || (i.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(i.value.trim()))));
      bad.forEach((i) => { i.closest('.field, .check')?.classList.add('is-bad'); i.setAttribute('aria-invalid', 'true'); });
      const pre = precheck ? precheck() : null;
      if (pre || bad.length) {
        msg.textContent = pre || 'Vul de gemarkeerde velden in.';
        msg.hidden = false; msg.classList.add('is-err');
        if (!pre) bad[0].focus();
        return;
      }
      const btn = form.querySelector('[type="submit"]');
      btn.disabled = true;
      const p = payload(form, type);
      try {
        const r = await fetch(CFG.endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(p) });
        const res = await r.json().catch(() => ({}));
        if (!r.ok || res.ok === false) throw new Error(res.error || String(r.status));
        tell(type, { payload: p });
        form.reset();
        msg.textContent = type === 'help' ? 'Bedankt. We nemen zo snel mogelijk contact met je op.'
          : `Bedankt voor je aanvraag. ${CFG.dealer} stuurt je zo snel mogelijk een offerte.`;
        msg.hidden = false; msg.classList.add('is-ok');
      } catch (err) {
        console.warn('Endpoint niet bereikbaar, mailto als terugval', err);
        tell(type, { payload: p });
        mailto(p);
        msg.textContent = `Je e-mailprogramma opent met je aanvraag. Lukt dat niet? Mail naar ${CFG.email} of bel ${CFG.phoneLabel}.`;
        msg.hidden = false; msg.classList.add('is-ok');
      } finally {
        btn.disabled = false;
      }
    }
    app.addEventListener('submit', (e) => {
      if (e.target.matches('[data-quote]')) {
        e.preventDefault();
        submit(e.target, 'quote', () => {
          const miss = missing();
          if (!miss.length) return null;
          const first = miss[0];
          setTimeout(() => goTo(first.sectionIndex, first.key), 900);
          return `Kies eerst nog: ${miss.map((g) => g.title.toLowerCase()).join(', ')}. We brengen je erheen.`;
        });
      } else if (e.target.matches('[data-help-form]')) {
        e.preventDefault();
        submit(e.target, 'help');
      }
    });

    // ----- start -----
    drawStep(false);
    drawStage();
    persist();
  }

  function field(name, label, required = false, type = 'text', cls = '') {
    const ac = { firstname: 'given-name', lastname: 'family-name', email: 'email', phone: 'tel', street: 'address-line1',
      housenumber: 'address-line2', zipcode: 'postal-code', city: 'address-level2', name: 'name' }[name] || 'off';
    return `<label class="field ${cls}"><span>${esc(label)}${required ? '' : ' <em>optioneel</em>'}</span>
      <input name="${name}" type="${type}" autocomplete="${ac}" ${required ? 'required aria-required="true"' : ''}></label>`;
  }

  // Kleurvlak bij kleurkeuzes zonder foto, afgeleid uit de naam.
  function swatchCss(group, name) {
    const n = name.toLowerCase();
    if (/^geen/.test(n)) return 'background:repeating-linear-gradient(45deg,#fff 0 4px,#e6e5e2 4px 8px)';
    if (/ral/.test(n)) return 'background:conic-gradient(#c0392b,#e9b44c,#2a9d8f,#2b4f81,#7a6750,#c0392b)';
    const map = [
      [/donkerblauw|navy/, '#1d2a48'], [/blauw/, '#3a6599'],
      [/donkergrijs|antraciet|charcoal|carbon|negro/, '#44464c'], [/zilver/, '#c3c6cb'], [/lichtgrijs/, '#d3d5d7'], [/grijs|mineral|vision/, '#8a8d92'],
      [/zwart/, '#1b1b1f'], [/wit|white/, '#ffffff'], [/oranje|sunset/, '#e07a3a'],
      [/cognac|bruin|naturel/, '#8a5a32'], [/otono/, '#9a7b5c'], [/seashell|neutra|tweed/, '#d8ccb6'],
    ];
    const hit = map.find(([re]) => re.test(n));
    return 'background:' + (hit ? hit[1] : '#e6e5e2');
  }

  route();
})();
