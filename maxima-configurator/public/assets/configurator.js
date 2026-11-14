/*
 * Klop Watersport — Maxima configurator
 * Vanilla JS, geen build-stap. Data komt uit data/models.json + data/<slug>.json
 * (gegenereerd door scripts/scrape_maxima.py).
 *
 * URL-schema:
 *   ?                       → overzicht van alle modellen
 *   ?model=maxima-550       → configurator voor dat model
 *   ?p=1785                 → idem, op basis van het Maxima product-id (compatibel met oude links)
 *   &c=41651.41680.46034    → gekozen opties (deelbare link)
 */
(() => {
  'use strict';

  const CFG = Object.assign({
    dataPath: 'data/',
    endpoint: 'api/offerte.php',
    email: 'verkoop@klopwatersport.nl',
    phone: '+31184612227',
    phoneLabel: '+31 (0)184 - 61 22 27',
    whatsapp: '31633180500',
    backUrl: null,
  }, window.KLOP_CONFIG || {});

  const app = document.getElementById('app');
  const VIEW_LABELS = { side: 'Zijkant', back: 'Achterkant', front: 'Voorkant' };
  const STORAGE_KEY = 'klop-maxima-config';

  // ---------- helpers ----------
  const fmt = (n) => '€ ' + Number(n || 0).toLocaleString('nl-NL', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  const fmtShort = (n) => '€ ' + Number(n || 0).toLocaleString('nl-NL', { maximumFractionDigits: 0 });
  const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const stripStepVerb = (t) => t.replace(/^Kies\s+/i, '').replace(/^\w/, (c) => c.toUpperCase());
  const h = (html) => { const t = document.createElement('template'); t.innerHTML = html.trim(); return t.content.firstElementChild; };
  const store = {
    get() { try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}'); } catch { return {}; } },
    set(v) { try { localStorage.setItem(STORAGE_KEY, JSON.stringify(v)); } catch { /* geen opslag beschikbaar */ } },
  };
  const cache = new Map();
  const getJSON = (url) => {
    if (!cache.has(url)) cache.set(url, fetch(url).then((r) => { if (!r.ok) throw new Error(r.status); return r.json(); }));
    return cache.get(url);
  };
  const preloaded = new Map();
  const preload = (src) => {
    if (!preloaded.has(src)) {
      preloaded.set(src, new Promise((res) => { const i = new Image(); i.onload = () => res(true); i.onerror = () => res(false); i.src = src; }));
    }
    return preloaded.get(src);
  };

  const isElectric = (m) => /elektris|electris/i.test(m.name);

  // ---------- routing ----------
  function route() {
    const q = new URLSearchParams(location.search);
    const slug = q.get('model');
    const pid = q.get('p');
    getJSON(CFG.dataPath + 'models.json').then((models) => {
      const model = slug ? models.find((m) => m.slug === slug) : pid ? models.find((m) => String(m.id) === pid) : null;
      if (model) return renderConfigurator(model, q.get('c'));
      return renderOverview(models);
    }).catch((err) => {
      console.error(err);
      app.innerHTML = '<div class="app__error wrap"><h1>De configurator kon niet geladen worden</h1><p>Probeer het later opnieuw of neem contact met ons op.</p></div>';
    });
  }
  function navigate(params) {
    const q = new URLSearchParams(params);
    history.pushState(null, '', q.toString() ? '?' + q : location.pathname);
    window.scrollTo(0, 0);
    route();
  }
  window.addEventListener('popstate', route);
  document.addEventListener('click', (e) => {
    const a = e.target.closest('[data-nav="overview"]');
    if (a) { e.preventDefault(); navigate({}); }
  });
  document.querySelectorAll('[data-phone-link]').forEach((a) => { a.href = 'tel:' + CFG.phone; });
  document.querySelectorAll('[data-phone-label]').forEach((el) => { el.textContent = CFG.phoneLabel; });

  // ---------- overzicht ----------
  function renderOverview(models) {
    document.title = 'Maxima configurator | Klop Watersport';
    const state = { q: '', drive: 'all', sort: 'price-asc' };

    app.innerHTML = `
      <section class="hero">
        <div class="wrap">
          <span class="eyebrow">Maxima Boats bij Klop Watersport</span>
          <h1>Stel je eigen Maxima samen</h1>
          <p>Kies een model, bepaal kleuren, buiskap, kussens, motor en opties en zie direct je prijs. Vraag daarna vrijblijvend een offerte aan.</p>
        </div>
      </section>
      <section class="wrap overview">
        <div class="filters" role="search">
          <label class="field field--search">
            <span class="sr-only">Zoek model</span>
            <input type="search" placeholder="Zoek model, bijv. 650" data-f="q">
          </label>
          <div class="seg" role="group" aria-label="Aandrijving">
            <button type="button" class="seg__btn is-active" data-drive="all">Alle</button>
            <button type="button" class="seg__btn" data-drive="fuel">Brandstof</button>
            <button type="button" class="seg__btn" data-drive="electric">Elektrisch</button>
          </div>
          <label class="field field--select">
            <span class="sr-only">Sorteren</span>
            <select data-f="sort">
              <option value="price-asc">Prijs oplopend</option>
              <option value="price-desc">Prijs aflopend</option>
              <option value="name">Naam</option>
              <option value="length">Lengte</option>
            </select>
          </label>
        </div>
        <p class="overview__count" data-count></p>
        <div class="grid" data-grid></div>
      </section>`;

    const grid = app.querySelector('[data-grid]');
    const count = app.querySelector('[data-count]');
    const len = (m) => parseFloat((m.specs?.Lengte || '0').replace(',', '.')) || 0;

    const draw = () => {
      let list = models.filter((m) => m.name.toLowerCase().includes(state.q.toLowerCase()));
      if (state.drive === 'electric') list = list.filter(isElectric);
      if (state.drive === 'fuel') list = list.filter((m) => !isElectric(m));
      const sorters = {
        'price-asc': (a, b) => a.basePrice - b.basePrice,
        'price-desc': (a, b) => b.basePrice - a.basePrice,
        name: (a, b) => a.name.localeCompare(b.name, 'nl', { numeric: true }),
        length: (a, b) => len(a) - len(b),
      };
      list.sort(sorters[state.sort]);
      count.textContent = `${list.length} ${list.length === 1 ? 'model' : 'modellen'}`;
      grid.innerHTML = list.length ? list.map((m) => `
        <a class="card" href="?model=${esc(m.slug)}" data-slug="${esc(m.slug)}">
          <span class="card__img">
            ${m.image ? `<img src="${esc(m.image)}" alt="${esc(m.name)}" loading="lazy">` : ''}
            ${isElectric(m) ? '<span class="badge">Elektrisch</span>' : ''}
          </span>
          <span class="card__body">
            <span class="card__title">${esc(m.name)}</span>
            <span class="card__specs">
              ${m.specs?.Lengte ? `<span><b>Lengte</b>${esc(m.specs.Lengte)}</span>` : ''}
              ${m.specs?.['Aantal personen'] ? `<span><b>Personen</b>${esc(m.specs['Aantal personen'])}</span>` : ''}
            </span>
            <span class="card__foot">
              <span class="card__price"><small>vanaf</small>${fmtShort(m.basePrice)}</span>
              <span class="btn btn--small">Configureer</span>
            </span>
          </span>
        </a>`).join('') : '<p class="empty">Geen modellen gevonden.</p>';
    };

    app.querySelector('[data-f="q"]').addEventListener('input', (e) => { state.q = e.target.value; draw(); });
    app.querySelector('[data-f="sort"]').addEventListener('change', (e) => { state.sort = e.target.value; draw(); });
    app.querySelectorAll('[data-drive]').forEach((b) => b.addEventListener('click', () => {
      app.querySelectorAll('[data-drive]').forEach((x) => x.classList.toggle('is-active', x === b));
      state.drive = b.dataset.drive; draw();
    }));
    grid.addEventListener('click', (e) => {
      const card = e.target.closest('[data-slug]');
      if (!card || e.metaKey || e.ctrlKey) return;
      e.preventDefault();
      navigate({ model: card.dataset.slug });
    });
    draw();
  }

  // ---------- configurator ----------
  async function renderConfigurator(meta, encoded) {
    app.innerHTML = '<div class="app__loading"><span class="spinner"></span> ' + esc(meta.name) + ' laden…</div>';
    const model = await getJSON(CFG.dataPath + meta.slug + '.json');
    document.title = `Configureer ${model.name} | Klop Watersport`;

    // optie-index
    const optIndex = new Map();
    model.steps.forEach((s, si) => s.options.forEach((o) => optIndex.set(String(o.id), { step: si, opt: o })));

    // selectie: per stap een Set van optie-id's
    const sel = model.steps.map(() => new Set());
    const restore = encoded ?? store.get()[model.slug] ?? '';
    String(restore).split('.').filter(Boolean).forEach((id) => {
      const hit = optIndex.get(id);
      if (!hit) return;
      if (model.steps[hit.step].type === 'single') sel[hit.step].clear();
      sel[hit.step].add(id);
    });

    const hasLayers = model.views.length > 0 && model.layers.length > 0;
    let view = model.defaultView || model.views[0];
    let openStep = sel.findIndex((s, i) => !s.size && !model.steps[i].optional);
    if (openStep < 0) openStep = 0;

    app.innerHTML = `
      <div class="cfg">
        <div class="cfg__bar wrap">
          <a href="?" data-nav="overview" class="back">← Alle modellen</a>
          <h1 class="cfg__title">Configureer <span>${esc(model.name)}</span></h1>
        </div>
        <div class="cfg__layout wrap">
          <section class="cfg__stage" aria-label="Voorbeeld van je boot">
            <div class="stage">
              <div class="stage__img ${hasLayers ? '' : 'stage__img--photo'}" data-stage>
                ${hasLayers ? '' : `<img src="${esc(model.image)}" alt="${esc(model.name)}">`}
                <span class="stage__loader" data-loader><span class="spinner"></span></span>
              </div>
              ${hasLayers ? `<div class="stage__views" role="tablist" aria-label="Aanzicht">
                ${model.views.map((v) => `<button type="button" role="tab" class="view-btn" data-view="${esc(v)}" aria-selected="${v === view}">
                  <span class="view-btn__img" data-thumb="${esc(v)}"></span><span>${esc(VIEW_LABELS[v] || v)}</span></button>`).join('')}
              </div>` : ''}
              <p class="stage__note">Let op: deze afbeelding dient enkel als impressie. Je werkelijke boot kan afwijken.</p>
            </div>
            <div class="total-card">
              <div class="total-card__row">
                <span>Totaalprijs</span>
                <strong data-total></strong>
              </div>
              <button type="button" class="link" data-open-spec>Bekijk prijsspecificatie</button>
              <div class="total-card__actions">
                <button type="button" class="btn" data-goto-quote>Offerte aanvragen</button>
                <button type="button" class="btn btn--ghost" data-open-help>Hulp bij samenstellen</button>
              </div>
            </div>
          </section>

          <section class="cfg__steps" aria-label="Samenstellen">
            <div class="steps__tools">
              <span data-progress></span>
              <span><button type="button" class="link" data-expand>Alles uitklappen</button> · <button type="button" class="link" data-collapse>Alles inklappen</button></span>
            </div>
            <ol class="steps" data-steps></ol>
            <form class="step step--form is-open" data-quote novalidate>
              <div class="step__head step__head--static"><span class="step__num">${model.steps.length + 1}</span><span class="step__title">Je gegevens &amp; offerte</span></div>
              <div class="step__body">
                <p class="muted">Vul je gegevens in en ontvang een vrijblijvende offerte voor deze configuratie. Velden met * zijn verplicht.</p>
                <div class="form-grid">
                  ${field('firstname', 'Voornaam', true)}
                  ${field('lastname', 'Achternaam', true)}
                  ${field('email', 'E-mail', true, 'email')}
                  ${field('phone', 'Telefoonnummer', true, 'tel')}
                  ${field('street', 'Straat')}
                  ${field('housenumber', 'Huisnummer')}
                  ${field('zipcode', 'Postcode')}
                  ${field('city', 'Plaats', true)}
                  <label class="field field--full"><span>Land</span>
                    <select name="country">${['Nederland', 'België', 'Duitsland', 'Frankrijk', 'Luxemburg', 'Verenigd Koninkrijk', 'Overig'].map((c) => `<option>${c}</option>`).join('')}</select>
                  </label>
                  <label class="field field--full"><span>Opmerking</span><textarea name="remarks" rows="3"></textarea></label>
                  <label class="hp" aria-hidden="true">Laat leeg<input name="website" tabindex="-1" autocomplete="off"></label>
                  <label class="check field--full"><input type="checkbox" name="agree" required> <span>Ik ga ermee akkoord dat Klop Watersport contact met mij opneemt over deze aanvraag.</span></label>
                </div>
                <p class="form-msg" data-form-msg role="alert" hidden></p>
                <div class="form-actions">
                  <button type="submit" class="btn">Offerte aanvragen</button>
                  <button type="button" class="btn btn--ghost" data-print>Download PDF</button>
                  <button type="button" class="btn btn--ghost" data-share>Link kopiëren</button>
                </div>
              </div>
            </form>
          </section>
        </div>

        <div class="mobile-bar">
          <button type="button" class="mobile-bar__total" data-open-spec><small>Totaalprijs</small><strong data-total></strong></button>
          <button type="button" class="btn btn--small" data-goto-quote>Offerte</button>
        </div>
      </div>

      <dialog class="modal" data-spec>
        <div class="modal__head"><h2>Prijsspecificatie</h2><button type="button" class="modal__close" data-close aria-label="Sluiten">×</button></div>
        <div class="modal__body" data-spec-body></div>
      </dialog>
      <dialog class="modal" data-help>
        <div class="modal__head"><h2>Hulp bij samenstellen</h2><button type="button" class="modal__close" data-close aria-label="Sluiten">×</button></div>
        <form class="modal__body" data-help-form novalidate>
          <p class="muted">Liever persoonlijk advies? Laat je gegevens achter en een van onze adviseurs neemt contact met je op. Je kunt ook bellen naar <a href="tel:${esc(CFG.phone)}">${esc(CFG.phoneLabel)}</a> of <a href="https://wa.me/${esc(CFG.whatsapp)}" target="_blank" rel="noopener">WhatsAppen</a>.</p>
          <div class="form-grid">
            ${field('name', 'Naam', true)}
            ${field('phone', 'Telefoonnummer', true, 'tel')}
            ${field('email', 'E-mail', true, 'email', 'field--full')}
            <label class="field field--full"><span>Opmerking</span><textarea name="remarks" rows="3"></textarea></label>
            <label class="hp" aria-hidden="true">Laat leeg<input name="website" tabindex="-1" autocomplete="off"></label>
          </div>
          <p class="form-msg" data-form-msg role="alert" hidden></p>
          <div class="form-actions"><button type="submit" class="btn">Verzenden</button></div>
        </form>
      </dialog>
      <dialog class="modal modal--img" data-zoom>
        <div class="modal__head"><h2 data-zoom-title></h2><button type="button" class="modal__close" data-close aria-label="Sluiten">×</button></div>
        <img data-zoom-img alt="">
      </dialog>
      <div class="print-sheet" data-print-sheet></div>`;

    const $ = (s) => app.querySelector(s);
    const $$ = (s) => [...app.querySelectorAll(s)];
    const stepsEl = $('[data-steps]');

    // ----- stappen renderen -----
    stepsEl.innerHTML = model.steps.map((s, si) => `
      <li class="step" data-step="${si}">
        <button type="button" class="step__head" aria-expanded="false" aria-controls="step-body-${si}">
          <span class="step__num">${si + 1}</span>
          <span class="step__main">
            <span class="step__title">${esc(stripStepVerb(s.title))}${s.optional ? ' <em>optioneel</em>' : ''}</span>
            <span class="step__chosen" data-chosen></span>
          </span>
          <span class="step__check" aria-hidden="true">✓</span>
          <span class="step__chev" aria-hidden="true"></span>
        </button>
        <div class="step__body" id="step-body-${si}">
          <div class="options ${s.options.some((o) => o.image) ? 'options--img' : ''}" role="${s.type === 'single' ? 'radiogroup' : 'group'}" aria-label="${esc(s.title)}">
            ${s.options.map((o) => `
              <label class="opt ${o.image ? 'opt--img' : ''}">
                <input type="${s.type === 'single' ? 'radio' : 'checkbox'}" name="step-${si}" value="${o.id}">
                ${o.image ? `<span class="opt__img"><img src="${esc(o.image)}" alt="" loading="lazy"><button type="button" class="opt__zoom" data-zoom-src="${esc(o.image)}" data-zoom-name="${esc(o.name)}" aria-label="Vergroot afbeelding van ${esc(o.name)}">⤢</button></span>` : `<span class="opt__swatch" style="${swatchStyle(o.name)}"></span>`}
                <span class="opt__text">
                  <span class="opt__name">${esc(o.name)}</span>
                  ${o.description ? `<span class="opt__desc">${esc(o.description)}</span>` : ''}
                  <span class="opt__price">${o.price ? '+ ' + fmt(o.price) : 'Inbegrepen'}</span>
                </span>
                <span class="opt__tick" aria-hidden="true"></span>
              </label>`).join('')}
          </div>
          <div class="step__nav">
            ${s.type === 'multi' ? '<button type="button" class="link" data-clear>Geen opties</button>' : '<span></span>'}
            <button type="button" class="btn btn--small" data-next>Verder ↓</button>
          </div>
        </div>
      </li>`).join('');

    // ----- boot-lagen -----
    const stage = $('[data-stage]');
    const loader = $('[data-loader]');
    let layerImgs = {};
    const layerSrc = (v, o) => `${model.imageBase}${v}/${o.layer}/${o.layerId}.png`;
    const fullSrc = (v) => `${model.imageBase}${v}/full.png`;

    function chosenLayerOptions() {
      const out = {};
      sel.forEach((set) => set.forEach((id) => {
        const { opt } = optIndex.get(id);
        if (opt.layer && opt.layerId && model.layers.includes(opt.layer)) out[opt.layer] = opt;
      }));
      return out;
    }

    function buildStage() {
      if (!hasLayers) return;
      stage.querySelectorAll('img').forEach((i) => i.remove());
      layerImgs = {};
      // full.png is de basis (onderste laag); de gekozen opties liggen erbovenop.
      ['full', ...model.layers].forEach((name) => {
        const img = document.createElement('img');
        img.alt = name === 'full' ? model.name : '';
        img.className = 'layer layer--' + name;
        img.hidden = name !== 'full';
        stage.insertBefore(img, loader);
        layerImgs[name] = img;
      });
    }

    let stageToken = 0;
    async function drawStage() {
      if (!hasLayers) return;
      const token = ++stageToken;
      const chosen = chosenLayerOptions();
      const jobs = [['full', fullSrc(view)], ...model.layers.map((l) => [l, chosen[l] ? layerSrc(view, chosen[l]) : null])];
      loader.classList.add('is-on');
      const results = await Promise.all(jobs.map(([, src]) => (src ? preload(src) : Promise.resolve(false))));
      // Decoderen voor het wisselen voorkomt flikkeren tussen lagen.
      await Promise.all(jobs.map(([, src], i) => {
        if (!src || !results[i]) return null;
        const probe = new Image();
        probe.src = src;
        return probe.decode().catch(() => null);
      }));
      if (token !== stageToken) return;
      jobs.forEach(([name, src], i) => {
        const img = layerImgs[name];
        if (src && results[i]) { img.src = src; img.hidden = false; } else if (name !== 'full') { img.hidden = true; }
      });
      loader.classList.remove('is-on');
      drawThumbs(chosen);
    }

    // Thumbnails: alle lagen samenvoegen op een canvas (een bitmap per aanzicht).
    // Lichter dan 8 gestapelde 1000x1000 PNG's per knop en altijd volledig getekend.
    let thumbToken = 0;
    function drawThumbs(chosen) {
      const token = ++thumbToken;
      $$('[data-thumb]').forEach((el) => {
        const v = el.dataset.thumb;
        const srcs = [fullSrc(v), ...model.layers.filter((l) => chosen[l]).map((l) => layerSrc(v, chosen[l]))];
        const imgs = srcs.map((src) => { const img = new Image(); img.src = src; return img; });
        Promise.all(imgs.map((img) => img.decode().then(() => img, () => null))).then((ok) => {
          if (token !== thumbToken) return;
          const dpr = Math.min(window.devicePixelRatio || 1, 2);
          const w = Math.max(1, Math.round(el.clientWidth * dpr));
          const hgt = Math.max(1, Math.round(el.clientHeight * dpr));
          const canvas = document.createElement('canvas');
          canvas.width = w; canvas.height = hgt;
          const ctx = canvas.getContext('2d');
          ok.filter(Boolean).forEach((img) => {
            // object-fit: cover
            const scale = Math.max(w / img.naturalWidth, hgt / img.naturalHeight);
            const sw = w / scale, sh = hgt / scale;
            ctx.drawImage(img, (img.naturalWidth - sw) / 2, (img.naturalHeight - sh) / 2, sw, sh, 0, 0, w, hgt);
          });
          el.replaceChildren(canvas);
        });
      });
    }

    function preloadAll() {
      if (!hasLayers) return;
      const idle = window.requestIdleCallback || ((fn) => setTimeout(fn, 400));
      idle(() => {
        model.views.forEach((v) => preload(fullSrc(v)));
        model.steps.forEach((s) => s.options.forEach((o) => { if (o.layer && o.layerId && model.layers.includes(o.layer)) preload(layerSrc(view, o)); }));
      });
    }

    $$('[data-view]').forEach((b) => b.addEventListener('click', () => {
      view = b.dataset.view;
      $$('[data-view]').forEach((x) => x.setAttribute('aria-selected', String(x === b)));
      drawStage();
    }));

    // ----- prijs & samenvatting -----
    function chosenList() {
      const out = [];
      sel.forEach((set, si) => set.forEach((id) => out.push({ step: model.steps[si].title, ...optIndex.get(id).opt })));
      return out;
    }
    function total() {
      return model.basePrice + model.fixedCosts.reduce((a, c) => a + c.price, 0) + chosenList().reduce((a, o) => a + o.price, 0);
    }
    function encode() { return sel.flatMap((s) => [...s]).join('.'); }

    function specHTML() {
      const rows = chosenList();
      return `
        <table class="spec">
          <tbody>
            <tr><th>Basisprijs ${esc(model.name)}</th><td>${fmt(model.basePrice)}</td></tr>
            ${rows.map((o) => `<tr><th><small>${esc(stripStepVerb(o.step))}</small>${esc(o.name)}</th><td>${fmt(o.price)}</td></tr>`).join('')}
            ${model.fixedCosts.map((c) => `<tr><th>${esc(c.label)}</th><td>${fmt(c.price)}</td></tr>`).join('')}
          </tbody>
          <tfoot><tr><th>Totaalprijs</th><td>${fmt(total())}</td></tr></tfoot>
        </table>`;
    }

    function update() {
      // stappen bijwerken
      model.steps.forEach((s, si) => {
        const li = stepsEl.children[si];
        const names = [...sel[si]].map((id) => optIndex.get(id).opt.name);
        li.classList.toggle('is-done', names.length > 0);
        li.querySelector('[data-chosen]').textContent = names.length ? names.join(', ') : (s.optional ? 'Geen keuze' : 'Nog niet gekozen');
        li.querySelectorAll('input').forEach((inp) => { inp.checked = sel[si].has(inp.value); });
      });
      const required = model.steps.filter((s) => !s.optional).length;
      const done = model.steps.filter((s, i) => !s.optional && sel[i].size).length;
      $('[data-progress]').textContent = `${done} van ${required} verplichte keuzes gemaakt`;
      $$('[data-total]').forEach((el) => { el.textContent = fmt(total()); });

      // deelbare URL + opslag
      const q = new URLSearchParams(location.search);
      q.delete('p'); q.set('model', model.slug);
      const c = encode();
      if (c) q.set('c', c); else q.delete('c');
      history.replaceState(null, '', '?' + q);
      const saved = store.get(); saved[model.slug] = c; store.set(saved);
    }

    function setOpen(si, scroll) {
      openStep = si;
      [...stepsEl.children].forEach((li, i) => {
        const on = i === si;
        li.classList.toggle('is-open', on);
        li.querySelector('.step__head').setAttribute('aria-expanded', String(on));
      });
      if (scroll && si >= 0) {
        const li = stepsEl.children[si] || $('[data-quote]');
        requestAnimationFrame(() => li.scrollIntoView({ behavior: 'smooth', block: 'start' }));
      }
    }

    stepsEl.addEventListener('click', (e) => {
      const head = e.target.closest('.step__head');
      if (head) { const si = +head.closest('.step').dataset.step; setOpen(openStep === si ? -1 : si, false); return; }
      const next = e.target.closest('[data-next]');
      if (next) {
        const si = +next.closest('.step').dataset.step;
        if (si + 1 < model.steps.length) setOpen(si + 1, true);
        else { setOpen(-1, false); $('[data-quote]').scrollIntoView({ behavior: 'smooth', block: 'start' }); }
        return;
      }
      const clr = e.target.closest('[data-clear]');
      if (clr) { sel[+clr.closest('.step').dataset.step].clear(); update(); return; }
      const z = e.target.closest('[data-zoom-src]');
      if (z) {
        e.preventDefault();
        $('[data-zoom-img]').src = z.dataset.zoomSrc;
        $('[data-zoom-title]').textContent = z.dataset.zoomName;
        $('[data-zoom]').showModal();
      }
    });
    stepsEl.addEventListener('change', (e) => {
      const inp = e.target;
      const si = +inp.closest('.step').dataset.step;
      if (inp.type === 'radio') { sel[si].clear(); sel[si].add(inp.value); }
      else if (inp.checked) sel[si].add(inp.value);
      else sel[si].delete(inp.value);
      update();
      drawStage();
    });

    $('[data-expand]').addEventListener('click', () => $$('.steps .step').forEach((li) => li.classList.add('is-open')));
    $('[data-collapse]').addEventListener('click', () => setOpen(-1, false));

    // ----- modals -----
    $$('dialog').forEach((d) => {
      d.addEventListener('click', (e) => { if (e.target === d || e.target.closest('[data-close]')) d.close(); });
    });
    $$('[data-open-spec]').forEach((b) => b.addEventListener('click', () => {
      $('[data-spec-body]').innerHTML = specHTML();
      $('[data-spec]').showModal();
    }));
    $('[data-open-help]').addEventListener('click', () => $('[data-help]').showModal());
    $$('[data-goto-quote]').forEach((b) => b.addEventListener('click', () => {
      $('[data-quote]').scrollIntoView({ behavior: 'smooth', block: 'start' });
      setTimeout(() => $('[data-quote] input[name="firstname"]').focus({ preventScroll: true }), 500);
    }));

    // ----- delen / printen -----
    $('[data-share]').addEventListener('click', async (e) => {
      const btn = e.currentTarget;
      try { await navigator.clipboard.writeText(location.href); btn.textContent = 'Link gekopieerd ✓'; }
      catch { prompt('Kopieer deze link:', location.href); }
      setTimeout(() => { btn.textContent = 'Link kopiëren'; }, 2500);
    });
    $('[data-print]').addEventListener('click', () => {
      const sheet = $('[data-print-sheet]');
      const stageClone = stage.cloneNode(true);
      stageClone.querySelector('[data-loader]')?.remove();
      sheet.innerHTML = `
        <div class="print-sheet__head"><img src="assets/klop-logo.svg" alt="Klop Watersport"><div><h1>${esc(model.name)}</h1><p>Configuratie d.d. ${new Date().toLocaleDateString('nl-NL')}</p></div></div>
        <div class="print-sheet__boat"></div>
        ${specHTML()}
        <p class="print-sheet__foot">Klop Watersport · Rivierdijk 27a, 3372 BE Hardinxveld-Giessendam · ${esc(CFG.phoneLabel)} · ${esc(CFG.email)}<br>
        Deze configuratie is een indicatie; aan deze prijsopgave kunnen geen rechten worden ontleend. Bekijk online: ${esc(location.href)}</p>`;
      sheet.querySelector('.print-sheet__boat').appendChild(stageClone);
      window.print();
    });

    // ----- formulieren -----
    function payload(form, type) {
      const data = Object.fromEntries(new FormData(form).entries());
      return {
        type,
        model: model.name,
        modelId: model.id,
        configUrl: location.href,
        options: chosenList().map((o) => ({ step: stripStepVerb(o.step), name: o.name, price: o.price })),
        basePrice: model.basePrice,
        fixedCosts: model.fixedCosts,
        total: total(),
        contact: data,
      };
    }
    function mailtoFallback(p) {
      const lines = [
        `${p.type === 'help' ? 'Hulpaanvraag' : 'Offerteaanvraag'} ${p.model}`, '',
        ...Object.entries(p.contact).filter(([k, v]) => v && !['website', 'agree'].includes(k)).map(([k, v]) => `${k}: ${v}`), '',
        `Basisprijs: ${fmt(p.basePrice)}`,
        ...p.options.map((o) => `${o.step}: ${o.name} (${fmt(o.price)})`),
        ...p.fixedCosts.map((c) => `${c.label}: ${fmt(c.price)}`),
        `Totaal: ${fmt(p.total)}`, '', p.configUrl,
      ];
      location.href = `mailto:${CFG.email}?subject=${encodeURIComponent(lines[0])}&body=${encodeURIComponent(lines.slice(2).join('\n'))}`;
    }
    async function send(form, type, validate) {
      const msg = form.querySelector('[data-form-msg]');
      msg.hidden = true; msg.className = 'form-msg';
      form.querySelectorAll('.is-invalid').forEach((x) => x.classList.remove('is-invalid'));
      const bad = [...form.querySelectorAll('[required]')].filter((i) => (i.type === 'checkbox' ? !i.checked : !i.value.trim() || (i.type === 'email' && !/^\S+@\S+\.\S+$/.test(i.value))));
      bad.forEach((i) => i.closest('.field, .check')?.classList.add('is-invalid'));
      const extra = validate ? validate() : null;
      if (bad.length || extra) {
        msg.textContent = extra || 'Controleer de gemarkeerde velden.';
        msg.hidden = false; msg.classList.add('is-error');
        (bad[0] || msg).focus?.();
        return;
      }
      const btn = form.querySelector('[type="submit"]');
      btn.disabled = true;
      const p = payload(form, type);
      try {
        const r = await fetch(CFG.endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(p) });
        const res = await r.json().catch(() => ({}));
        if (!r.ok || res.ok === false) throw new Error(res.error || r.status);
        form.reset();
        msg.textContent = type === 'help'
          ? 'Bedankt! We nemen zo snel mogelijk contact met je op.'
          : 'Bedankt voor je aanvraag! Je ontvangt zo snel mogelijk een offerte van ons.';
        msg.hidden = false; msg.classList.add('is-ok');
      } catch (err) {
        console.warn('Endpoint niet bereikbaar, mailto-fallback', err);
        mailtoFallback(p);
        msg.textContent = `Je e-mailprogramma wordt geopend met je aanvraag. Lukt dat niet? Mail naar ${CFG.email} of bel ${CFG.phoneLabel}.`;
        msg.hidden = false; msg.classList.add('is-ok');
      } finally {
        btn.disabled = false;
      }
    }
    $('[data-quote]').addEventListener('submit', (e) => {
      e.preventDefault();
      send(e.target, 'quote', () => {
        const missing = model.steps.findIndex((s, i) => !s.optional && !sel[i].size);
        if (missing < 0) return null;
        setOpen(missing, true);
        return `Maak eerst een keuze bij stap ${missing + 1}: ${stripStepVerb(model.steps[missing].title).toLowerCase()}.`;
      });
    });
    $('[data-help-form]').addEventListener('submit', (e) => { e.preventDefault(); send(e.target, 'help'); });

    // ----- start -----
    buildStage();
    update();
    setOpen(openStep, false);
    drawStage();
    preloadAll();
  }

  function field(name, label, required = false, type = 'text', cls = '') {
    return `<label class="field ${cls}"><span>${esc(label)}${required ? ' *' : ''}</span><input name="${name}" type="${type}" ${required ? 'required' : ''} autocomplete="${({ firstname: 'given-name', lastname: 'family-name', email: 'email', phone: 'tel', street: 'address-line1', zipcode: 'postal-code', city: 'address-level2', name: 'name' })[name] || 'off'}"></label>`;
  }

  // Kleurvlakje bij kleuropties zonder foto, afgeleid uit de optienaam.
  function swatchStyle(name) {
    const n = name.toLowerCase();
    const map = [
      [/ral|eigen kleur/, 'conic-gradient(#e63946,#f4a261,#2a9d8f,#264653,#e63946)'],
      [/geen/, 'repeating-linear-gradient(45deg,#fff 0 4px,#d9dee5 4px 8px)'],
      [/donker ?blauw|navy|marine/, '#1d2b4f'], [/blauw/, '#3d6fa8'],
      [/donker ?grijs|antraciet|charcoal|carbon/, '#4a4f55'], [/zilver/, '#c3c7cc'], [/lichtgrijs|licht grijs/, '#cfd3d6'], [/agaat/, '#8f9496'], [/grijs/, '#8a8f94'],
      [/zwart|negro/, '#1b1b1b'], [/creme|crème|off.?white|ivoor/, '#f1ead8'], [/wit|white/, '#ffffff'],
      [/oranje/, '#f28c28'], [/rood/, '#c0392b'], [/groen|olijf/, '#4f6b3a'], [/cognac|bruin|naturel|teak/, '#8a5a32'], [/sunset/, '#d9774a'],
      [/beige|sand|seashell|neutra|otono|tweed|mineral/, '#d9ccb4'],
    ];
    const hit = map.find(([re]) => re.test(n));
    return 'background:' + (hit ? hit[1] : '#e4e9ef');
  }

  route();
})();
