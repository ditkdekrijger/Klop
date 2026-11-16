# Powermarketing-grid (JUST.LEAD)

Interactieve grid voor de Klop-pitch: de vier werkgebieden van JUST.LEAD tegen de vier fases van de klantreis. Om over te nemen in Claude Design: plak dit hele bestand als context, of upload het meegeleverde `powermarketing.html` direct. De volledige, werkende code staat onderaan.

## Opbouw

- **Kolommen, de vier werkgebieden van JUST.LEAD:** Marketing & content, Sales, Code, Change. Change is gemarkeerd met een sterretje: die blokken zijn verplaatsbaar naar een andere fase.
- **Rijen, de vier fases (RACE):** Bereik (reach), Kliks (act), Leads (convert), Sales (engage). Bereik en Kliks zijn *pull*, Leads en Sales zijn *push*.
- **Per cel:** een label en een lijnicoon.
- **Per werkgebied:** een rij tools met logo's (Google, LinkedIn, Meta, TikTok, enzovoort; Code o.a. Claude Code, Codex, GitHub).

| Fase | Marketing & content | Sales | Code | Change* |
|---|---|---|---|---|
| **Bereik**<br>Verhoog je zichtbaarheid | Displaycampagnes, SEO | Direct mail, events | Sites, platforms | Merk- & productpositionering |
| **Kliks**<br>Boost je traffic & interactie | Klikcampagnes, UI/UX | Salespitch, lead-inzichten | Landingspages, CRO | Processen & structuur |
| **Leads**<br>Genereer aanvragen & deals | Leadcampagnes, -magnets | Follow-up, (bel-)scripts | Configurators, pijplijn | Leiderschap & management |
| **Sales**<br>Actieve follow-up top prospects | Retargetingcampagnes, datamanagement | Pitch, salestechniek | Dashboards, automations | Businessmodel & waardepropositie |

## Interactie

- Klik een blok aan om het te selecteren: er vertrekt een raketje en de teller ("wat gaat er aan") loopt op.
- Change-blokken sleep je naar een andere fase; de indeling wordt in de browser onthouden.
- Bij de start staan de blokken aan die voor Klop aangaan (instelbaar in `const selected` in de code).

## Stijl

- Lettertypes: Archivo (koppen, ook italic 800) en JetBrains Mono (labels), via Google Fonts.
- Lijniconen met `currentColor`, merklogo's in hun eigen kleur.
- Aanspreekvorm: je/jij.

## Volledige code (`powermarketing.html`)

````html
<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>POWERMARKETING grid</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:ital,wght@0,400;0,500;0,600;0,700;0,800;1,800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  :root {
    --ink: #0A0A0B;
    --ink-2: #3D3D41;
    --ink-3: #5A5A5E;
    --muted: #A9A9AE;
    --line: #D5D5D8;
    --chip-line: #C9C9CD;
    --accent: #FF5A1F;
    --bg: #FFFFFF;
  }
  * { box-sizing: border-box; }
  body { margin: 0; font-family: 'Archivo', system-ui, sans-serif; color: var(--ink); background: var(--bg); }
  .mono { font-family: 'JetBrains Mono', ui-monospace, monospace; }
  svg { display: block; }

  .page { width: 100%; max-width: 1440px; margin: 0 auto; padding: 64px 56px 56px; }

  /* Header */
  .intro { display: flex; flex-direction: column; gap: 18px; margin-bottom: 48px; max-width: 1120px; }
  .intro__meta { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
  .badge { background: var(--ink); color: #fff; border-radius: 999px; padding: 6px 14px; font-size: 13px; font-weight: 600; letter-spacing: .06em; }
  .intro__sub { font-size: 13px; color: var(--ink-3); }
  .intro h1 { margin: 0; font-size: clamp(34px, 5.6vw, 68px); line-height: 1.02; font-weight: 800; letter-spacing: -.035em; }
  .nowrap { white-space: nowrap; }
  .outline { font-style: italic; color: transparent; -webkit-text-stroke: 2px var(--ink); }
  .intro p { margin: 0; font-size: 20px; line-height: 1.5; color: var(--ink-2); max-width: 640px; }

  /* Grid */
  .scroller { overflow-x: auto; padding-bottom: 8px; }
  .board { min-width: 1120px; display: flex; flex-direction: column; gap: 14px; }
  .row { display: grid; grid-template-columns: 180px repeat(4, minmax(0, 1fr)); gap: 14px; }
  .row--head { align-items: center; }

  .col-head { display: flex; align-items: center; gap: 14px; padding: 0 4px; }
  .col-head h2 { margin: 0; font-size: 26px; font-weight: 700; letter-spacing: -.02em; line-height: 1.1; }
  .cell--movable { cursor: grab; touch-action: none; user-select: none; }
  .is-dragging, .is-dragging * { cursor: grabbing !important; user-select: none; }
  .cell.is-lifted { box-shadow: 0 14px 30px rgba(10, 10, 11, .18); border-color: var(--ink); position: relative; z-index: 2; transition: none; }
  .cell.is-target { outline: 2px dashed var(--ink); outline-offset: 3px; }
  .disc { border-radius: 999px; background: var(--accent); color: var(--ink); display: flex; align-items: center; justify-content: center; flex: none; }
  .disc--lg { width: 56px; height: 56px; }
  .disc--sm { width: 34px; height: 34px; }

  .phase { display: flex; flex-direction: column; justify-content: center; gap: 6px; padding-right: 12px; }
  .phase__title { display: flex; align-items: center; gap: 10px; }
  .phase h3 { margin: 0; font-size: 28px; font-weight: 700; letter-spacing: -.02em; }
  .phase__desc { font-size: 15px; line-height: 1.35; color: var(--ink-2); }
  .phase__stage { display: flex; align-items: center; gap: 8px; font-size: 13px; color: var(--ink-3); }

  .cell {
    appearance: none; font: inherit; color: var(--ink); text-align: left; cursor: pointer;
    background: var(--bg); border: 1px solid var(--line); border-radius: 18px; padding: 14px; height: 164px;
    display: flex; flex-direction: column; justify-content: space-between; align-items: flex-start; gap: 8px;
    transition: background .15s, border-color .15s;
  }
  .cell:hover { border-color: var(--ink); }
  .cell:focus-visible { outline: 3px solid var(--ink); outline-offset: 2px; }
  .cell[aria-pressed="true"] { background: var(--accent); border-color: var(--accent); }
  .cell[aria-pressed="true"]:hover { border-color: var(--ink); }
  .cell__top { display: flex; justify-content: space-between; align-items: flex-start; width: 100%; font-size: 13px; }
  .cell__rocket { color: var(--muted); transition: color .15s, transform .25s; }
  .cell[aria-pressed="true"] .cell__rocket { color: var(--ink); transform: translateY(-3px); }
  .cell__label { font-size: 18px; font-weight: 600; line-height: 1.25; letter-spacing: -.01em; }

  .footnote { text-align: right; font-size: 14px; color: var(--ink-3); }
  .rule { height: 1px; background: var(--line); margin: 10px 0 6px; }

  /* Tools */
  .tools-title { font-size: 15px; font-weight: 700; padding-top: 6px; }
  .chips { list-style: none; margin: 0; padding: 0; display: flex; flex-wrap: wrap; gap: 6px; align-content: flex-start; }
  .chip {
    display: inline-flex; align-items: center; gap: 6px;
    border: 1px solid var(--chip-line); border-radius: 999px; padding: 3px 10px 3px 3px;
    font-size: 13px; line-height: 1.3; color: var(--ink); background: var(--bg); white-space: nowrap;
  }
  .tool-icon {
    width: 20px; height: 20px; border-radius: 999px; background: #F2F2F3; color: var(--ink);
    display: inline-flex; align-items: center; justify-content: center; flex: none;
  }
  .tool-icon svg { width: 12px; height: 12px; }
  .chip .tool-icon[data-brand] { color: var(--brand); }
  .tool-icon--fill, .tool-icon--fit { overflow: hidden; }
  .tool-icon--fill img, .tool-icon--fill svg { width: 100%; height: 100%; object-fit: cover; }
  .tool-icon--fit { background: #fff; border: 1px solid #ECECEE; }
  .tool-icon--fit img { width: 14px; height: 14px; object-fit: contain; }

  .partners { display: flex; flex-wrap: wrap; align-items: center; gap: 8px; margin-top: 12px; font-size: 13px; color: #B9B9BE; }
  .partner { display: inline-flex; align-items: center; gap: 7px; border: 1px solid #3A3A3F; border-radius: 999px; padding: 5px 12px 5px 8px; color: #fff; font-size: 13px; font-weight: 500; }

  /* Footer */
  .bar {
    margin-top: 48px; background: var(--ink); color: #fff; border-radius: 22px; padding: 22px 28px;
    display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 16px;
  }
  .bar__text { font-size: 18px; font-weight: 500; }
  .bar__count { display: flex; align-items: center; gap: 12px; font-size: 16px; }
  .counter { background: var(--accent); color: var(--ink); border-radius: 999px; padding: 8px 18px; font-size: 18px; font-weight: 700; display: flex; align-items: center; gap: 8px; }

  @media (max-width: 720px) {
    .page { padding: 40px 16px; }
    .intro p { font-size: 17px; }
  }
  @media (prefers-reduced-motion: reduce) {
    .cell, .cell__rocket { transition: none; }
  }
</style>
</head>
<body>
<div class="page">
  <header class="intro">
    <div class="intro__meta">
      <span class="badge">POWERMARKETING™</span>
      <span class="mono intro__sub">opzet 1 · RACE-grid</span>
    </div>
    <h1>Vier werkgebieden, vier fases, één <span class="outline nowrap">Powermarketing&#8209;aanpak</span>.</h1>
    <p>Klik de blokken aan om per onderdeel een raket te lanceren en zo je marketingmix te bepalen.</p>
  </header>

  <div class="scroller">
    <div class="board">
      <div class="row row--head" id="col-heads"></div>
      <div class="row" id="grid"></div>
      <div class="footnote">*Change: onderwerpen over alle fases toepasbaar — sleep een blok naar een andere fase om te wisselen</div>
      <div class="rule"></div>
      <div class="row" id="tools"></div>
    </div>
  </div>

  <footer class="bar">
    <div>
      <div class="bar__text">Alle acties in POWERMARKETING™ zijn AI-powered én altijd gericht op maximale klantwaarde.</div>
      <div class="partners">
        <span>Gecertificeerd partner van</span>
        <span class="partner"><span data-icon="google" data-size="14"></span>Google</span>
        <span class="partner"><span data-icon="meta" data-size="14"></span>Meta</span>
        <span class="partner"><span data-icon="claude" data-size="14"></span>Claude</span>
      </div>
    </div>
    <div class="bar__count" aria-live="polite">
      <span class="counter"><span data-icon="rocket" data-size="20"></span><span id="count">0</span></span>
      <span><span id="count-label">raketten</span> gelanceerd</span>
    </div>
  </footer>
</div>

<script>
/* ---------- Iconen ---------- */

// Lijniconen (stroke) uit het ontwerp.
const LINE = {
  rocket: '<path d="M12 2c3 2 5 5.5 5 9.5 0 1.5-.4 3-1 4.5H8c-.6-1.5-1-3-1-4.5C7 7.5 9 4 12 2z"/><circle cx="12" cy="10" r="1.6"/><path d="M8 16l-3 3 1-4.2M16 16l3 3-1-4.2M10.5 19.5L12 22l1.5-2.5"/>',
  // Kolomiconen: zender, cadeau, </>, horizon.
  marketing: '<circle cx="5" cy="12" r="1.6" fill="currentColor"/><path d="M9 8.5a5 5 0 010 7M12.5 6a8.5 8.5 0 010 12M16 3.5a12 12 0 010 17"/>',
  sales: '<rect x="3.5" y="8.5" width="17" height="4" rx="1"/><path d="M5 12.5V20a1 1 0 001 1h12a1 1 0 001-1v-7.5M12 8.5V21"/><path d="M12 8.5C10.5 5 6.5 4 6.5 6.5S9.5 8.5 12 8.5zM12 8.5C13.5 5 17.5 4 17.5 6.5S14.5 8.5 12 8.5z"/>',
  code: '<path d="M8 7l-5 5 5 5M16 7l5 5-5 5M14 4l-4 16"/>',
  change: '<path d="M7 15a5 5 0 0110 0"/><path d="M2.5 15h19M6 18.5h12M9.5 22h5"/><path d="M12 4v2.5M5.3 7.3l1.8 1.8M18.7 7.3l-1.8 1.8"/>',
  // Fasegezichtjes: van slaperig (bereik) naar blij (sales).
  face1: '<circle cx="12" cy="12" r="9"/><path d="M7.5 10.5c.7.6 1.6.6 2.3 0M14.2 10.5c.7.6 1.6.6 2.3 0M9.5 15.5h5"/>',
  face2: '<circle cx="12" cy="12" r="9"/><circle cx="9" cy="10" r=".9" fill="currentColor"/><circle cx="15" cy="10" r=".9" fill="currentColor"/><path d="M9.5 15h5"/>',
  face3: '<circle cx="12" cy="12" r="9"/><circle cx="9" cy="10" r=".9" fill="currentColor"/><circle cx="15" cy="10" r=".9" fill="currentColor"/><path d="M9.5 14.5c1.5 1 3.5 1 5 0"/>',
  face4: '<circle cx="12" cy="12" r="9"/><circle cx="9" cy="9.5" r=".9" fill="currentColor"/><circle cx="15" cy="9.5" r=".9" fill="currentColor"/><path d="M7.5 13.5a4.5 4.5 0 009 0z"/>',
  eye: '<path d="M2 12s3.6-6.5 10-6.5S22 12 22 12s-3.6 6.5-10 6.5S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
  mail: '<rect x="3" y="5" width="18" height="14" rx="3"/><path d="M4 7.5l8 6 8-6"/>',
  browser: '<rect x="3" y="4" width="18" height="16" rx="3"/><path d="M3 9h18M6.5 6.5h.01M9.5 6.5h.01"/>',
  compass: '<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5l-2 5-5 2 2-5 5-2z"/>',
  cursor: '<path d="M9 9l11 4.2-4.6 1.8-1.8 4.6L9 9z"/><path d="M5.5 5.5L7 7M4 10h2M10 4v2M14.5 5.5L13 7"/>',
  chat: '<path d="M4 6a3 3 0 013-3h10a3 3 0 013 3v8a3 3 0 01-3 3h-6l-5 4v-4H7a3 3 0 01-3-3V6z"/><path d="M8 8h8M8 12h5"/>',
  bag: '<path d="M5 8h14l-1 12H6L5 8z"/><path d="M9 8V7a3 3 0 016 0v1"/>',
  org: '<rect x="3" y="3.5" width="6" height="5" rx="1.5"/><rect x="15" y="3.5" width="6" height="5" rx="1.5"/><rect x="9" y="15.5" width="6" height="5" rx="1.5"/><path d="M6 8.5v3h12v-3M12 11.5v4"/>',
  funnel: '<path d="M3 5h18l-7 8.5V20l-4-2v-4.5L3 5z"/>',
  phone: '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 005 5L15 13l5 2v4a2 2 0 01-2 2A16 16 0 013 6a2 2 0 012-2z"/>',
  sliders: '<path d="M4 7h9M17 7h3M4 17h3M11 17h9"/><circle cx="15" cy="7" r="2"/><circle cx="9" cy="17" r="2"/>',
  people: '<circle cx="9" cy="8" r="3.2"/><path d="M3 20a6 6 0 0112 0"/><circle cx="17" cy="9" r="2.5"/><path d="M17 14a5 5 0 014 5"/>',
  target: '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.2"/>',
  board: '<path d="M3 4h18M5 4v10a2 2 0 002 2h10a2 2 0 002-2V4"/><path d="M12 16v4M8 20h8M8.5 12l2.5-3 2 2 2.5-3.5"/>',
  bars: '<path d="M4 20h16"/><rect x="5" y="11" width="3.5" height="6" rx="1"/><rect x="10.3" y="6" width="3.5" height="11" rx="1"/><rect x="15.5" y="9" width="3.5" height="8" rx="1"/>',
  canvas: '<rect x="3" y="3" width="18" height="18" rx="3"/><path d="M3 9h18M10 9v12M10 15h11"/>',
  // Generieke iconen voor tools zonder vrij beschikbaar logo
};

// Aangeleverde logo's, ingebed als data-URI zodat de pagina één los bestand is.
const IMG = {
  emailoctopus: 'data:image/png;base64,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',
  leadinfo: 'data:image/png;base64,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',
  mailchimp: 'data:image/png;base64,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',
  pipedrive: 'data:image/png;base64,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',
};

// Nagetekende merktekens (volledige SVG, eigen kleuren).
const MARK = {
  strategyzer: '<svg viewBox="0 0 24 24" aria-hidden="true"><rect width="24" height="24" fill="#fff"/><path d="M12 5.2A6.8 6.8 0 1 0 18.8 12" fill="none" stroke="#0A0A0B" stroke-width="3.2"/><path d="M12.6 12.6h5.2v5.2h-5.2z" fill="#0A0A0B"/></svg>',
  covey: '<svg viewBox="0 0 24 24" aria-hidden="true"><rect width="24" height="24" fill="#fff"/><circle cx="12" cy="12" r="6" fill="none" stroke="#0A0A0B" stroke-width="2.6"/><path d="M12 1.5l1.3 9.2L12 12l-1.3-1.3zM12 22.5l-1.3-9.2L12 12l1.3 1.3zM1.5 12l9.2-1.3L12 12l-1.3 1.3zM22.5 12l-9.2 1.3L12 12l1.3-1.3z" fill="#0A0A0B"/><circle cx="12" cy="12" r="2.4" fill="#fff"/></svg>',
  lean: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5.2 17.6A8.6 8.6 0 1 1 9 20.3" fill="none" stroke="#1BA6DE" stroke-width="2.8" stroke-linecap="round"/></svg>',
  brandthechange: '<svg viewBox="0 0 24 24" aria-hidden="true"><rect width="24" height="24" fill="#FFF200"/><circle cx="12" cy="12" r="4.6" fill="#0A0A0B"/><g stroke="#0A0A0B" stroke-width="1.6" stroke-linecap="square"><path d="M12 3.2v2.3M12 18.5v2.3M3.2 12h2.3M18.5 12h2.3M5.8 5.8l1.6 1.6M16.6 16.6l1.6 1.6M5.8 18.2l1.6-1.6M16.6 7.4l1.6-1.6"/></g></svg>',
};

// Merklogo's (fill), bron: Simple Icons (CC0), simpleicons.org.
const LOGO = {
  google: 'M12.48 10.92v3.28h7.84c-.24 1.84-.853 3.187-1.787 4.133-1.147 1.147-2.933 2.4-6.053 2.4-4.827 0-8.6-3.893-8.6-8.72s3.773-8.72 8.6-8.72c2.6 0 4.507 1.027 5.907 2.347l2.307-2.307C18.747 1.44 16.133 0 12.48 0 5.867 0 .307 5.387.307 12s5.56 12 12.173 12c3.573 0 6.267-1.173 8.373-3.36 2.16-2.16 2.84-5.213 2.84-7.667 0-.76-.053-1.467-.173-2.053H12.48z',
  meta: 'M6.915 4.03c-1.968 0-3.683 1.28-4.871 3.113C.704 9.208 0 11.883 0 14.449c0 .706.07 1.369.21 1.973a6.624 6.624 0 0 0 .265.86 5.297 5.297 0 0 0 .371.761c.696 1.159 1.818 1.927 3.593 1.927 1.497 0 2.633-.671 3.965-2.444.76-1.012 1.144-1.626 2.663-4.32l.756-1.339.186-.325c.061.1.121.196.183.3l2.152 3.595c.724 1.21 1.665 2.556 2.47 3.314 1.046.987 1.992 1.22 3.06 1.22 1.075 0 1.876-.355 2.455-.843a3.743 3.743 0 0 0 .81-.973c.542-.939.861-2.127.861-3.745 0-2.72-.681-5.357-2.084-7.45-1.282-1.912-2.957-2.93-4.716-2.93-1.047 0-2.088.467-3.053 1.308-.652.57-1.257 1.29-1.82 2.05-.69-.875-1.335-1.547-1.958-2.056-1.182-.966-2.315-1.303-3.454-1.303zm10.16 2.053c1.147 0 2.188.758 2.992 1.999 1.132 1.748 1.647 4.195 1.647 6.4 0 1.548-.368 2.9-1.839 2.9-.58 0-1.027-.23-1.664-1.004-.496-.601-1.343-1.878-2.832-4.358l-.617-1.028a44.908 44.908 0 0 0-1.255-1.98c.07-.109.141-.224.211-.327 1.12-1.667 2.118-2.602 3.358-2.602zm-10.201.553c1.265 0 2.058.791 2.675 1.446.307.327.737.871 1.234 1.579l-1.02 1.566c-.757 1.163-1.882 3.017-2.837 4.338-1.191 1.649-1.81 1.817-2.486 1.817-.524 0-1.038-.237-1.383-.794-.263-.426-.464-1.13-.464-2.046 0-2.221.63-4.535 1.66-6.088.454-.687.964-1.226 1.533-1.533a2.264 2.264 0 0 1 1.088-.285z',
  tiktok: 'M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z',
  pinterest: 'M12.017 0C5.396 0 .029 5.367.029 11.987c0 5.079 3.158 9.417 7.618 11.162-.105-.949-.199-2.403.041-3.439.219-.937 1.406-5.957 1.406-5.957s-.359-.72-.359-1.781c0-1.663.967-2.911 2.168-2.911 1.024 0 1.518.769 1.518 1.688 0 1.029-.653 2.567-.992 3.992-.285 1.193.6 2.165 1.775 2.165 2.128 0 3.768-2.245 3.768-5.487 0-2.861-2.063-4.869-5.008-4.869-3.41 0-5.409 2.562-5.409 5.199 0 1.033.394 2.143.889 2.741.099.12.112.225.085.345-.09.375-.293 1.199-.334 1.363-.053.225-.172.271-.401.165-1.495-.69-2.433-2.878-2.433-4.646 0-3.776 2.748-7.252 7.92-7.252 4.158 0 7.392 2.967 7.392 6.923 0 4.135-2.607 7.462-6.233 7.462-1.214 0-2.354-.629-2.758-1.379l-.749 2.848c-.269 1.045-1.004 2.352-1.498 3.146 1.123.345 2.306.535 3.55.535 6.607 0 11.985-5.365 11.985-11.987C23.97 5.39 18.592.026 11.985.026L12.017 0z',
  snapchat: 'M12.206.793c.99 0 4.347.276 5.93 3.821.529 1.193.403 3.219.299 4.847l-.003.06c-.012.18-.022.345-.03.51.075.045.203.09.401.09.3-.016.659-.12 1.033-.301.165-.088.344-.104.464-.104.182 0 .359.029.509.09.45.149.734.479.734.838.015.449-.39.839-1.213 1.168-.089.029-.209.075-.344.119-.45.135-1.139.36-1.333.81-.09.224-.061.524.12.868l.015.015c.06.136 1.526 3.475 4.791 4.014.255.044.435.27.42.509 0 .075-.015.149-.045.225-.24.569-1.273.988-3.146 1.271-.059.091-.12.375-.164.57-.029.179-.074.36-.134.553-.076.271-.27.405-.555.405h-.03c-.135 0-.313-.031-.538-.074-.36-.075-.765-.135-1.273-.135-.3 0-.599.015-.913.074-.6.104-1.123.464-1.723.884-.853.599-1.826 1.288-3.294 1.288-.06 0-.119-.015-.18-.015h-.149c-1.468 0-2.427-.675-3.279-1.288-.599-.42-1.107-.779-1.707-.884-.314-.045-.629-.074-.928-.074-.54 0-.958.089-1.272.149-.211.043-.391.074-.54.074-.374 0-.523-.224-.583-.42-.061-.192-.09-.389-.135-.567-.046-.181-.105-.494-.166-.57-1.918-.222-2.95-.642-3.189-1.226-.031-.063-.052-.15-.055-.225-.015-.243.165-.465.42-.509 3.264-.54 4.73-3.879 4.791-4.02l.016-.029c.18-.345.224-.645.119-.869-.195-.434-.884-.658-1.332-.809-.121-.029-.24-.074-.346-.119-1.107-.435-1.257-.93-1.197-1.273.09-.479.674-.793 1.168-.793.146 0 .27.029.383.074.42.194.789.3 1.104.3.234 0 .384-.06.465-.105l-.046-.569c-.098-1.626-.225-3.651.307-4.837C7.392 1.077 10.739.807 11.727.807l.419-.015h.06z',
  notion: 'M4.459 4.208c.746.606 1.026.56 2.428.466l13.215-.793c.28 0 .047-.28-.046-.326L17.86 1.968c-.42-.326-.981-.7-2.055-.607L3.01 2.295c-.466.046-.56.28-.374.466zm.793 3.08v13.904c0 .747.373 1.027 1.214.98l14.523-.84c.841-.046.935-.56.935-1.167V6.354c0-.606-.233-.933-.748-.887l-15.177.887c-.56.047-.747.327-.747.933zm14.337.745c.093.42 0 .84-.42.888l-.7.14v10.264c-.608.327-1.168.514-1.635.514-.748 0-.935-.234-1.495-.933l-4.577-7.186v6.952L12.21 19s0 .84-1.168.84l-3.222.186c-.093-.186 0-.653.327-.746l.84-.233V9.854L7.822 9.76c-.094-.42.14-1.026.793-1.073l3.456-.233 4.764 7.279v-6.44l-1.215-.139c-.093-.514.28-.887.747-.933zM1.936 1.035l13.31-.98c1.634-.14 2.055-.047 3.082.7l4.249 2.986c.7.513.934.653.934 1.213v16.378c0 1.026-.373 1.634-1.68 1.726l-15.458.934c-.98.047-1.448-.093-1.962-.747l-3.129-4.06c-.56-.747-.793-1.306-.793-1.96V2.667c0-.839.374-1.54 1.447-1.632z',
  claude: 'm4.7144 15.9555 4.7174-2.6471.079-.2307-.079-.1275h-.2307l-.7893-.0486-2.6956-.0729-2.3375-.0971-2.2646-.1214-.5707-.1215-.5343-.7042.0546-.3522.4797-.3218.686.0608 1.5179.1032 2.2767.1578 1.6514.0972 2.4468.255h.3886l.0546-.1579-.1336-.0971-.1032-.0972L6.973 9.8356l-2.55-1.6879-1.3356-.9714-.7225-.4918-.3643-.4614-.1578-1.0078.6557-.7225.8803.0607.2246.0607.8925.686 1.9064 1.4754 2.4893 1.8336.3643.3035.1457-.1032.0182-.0728-.164-.2733-1.3539-2.4467-1.445-2.4893-.6435-1.032-.17-.6194c-.0607-.255-.1032-.4674-.1032-.7285L6.287.1335 6.6997 0l.9957.1336.419.3642.6192 1.4147 1.0018 2.2282 1.5543 3.0296.4553.8985.2429.8318.091.255h.1579v-.1457l.1275-1.706.2368-2.0947.2307-2.6957.0789-.7589.3764-.9107.7468-.4918.5828.2793.4797.686-.0668.4433-.2853 1.8517-.5586 2.9021-.3643 1.9429h.2125l.2429-.2429.9835-1.3053 1.6514-2.0643.7286-.8196.85-.9046.5464-.4311h1.0321l.759 1.1293-.34 1.1657-1.0625 1.3478-.8804 1.1414-1.2628 1.7-.7893 1.36.0729.1093.1882-.0183 2.8535-.607 1.5421-.2794 1.8396-.3157.8318.3886.091.3946-.3278.8075-1.967.4857-2.3072.4614-3.4364.8136-.0425.0304.0486.0607 1.5482.1457.6618.0364h1.621l3.0175.2247.7892.522.4736.6376-.079.4857-1.2142.6193-1.6393-.3886-3.825-.9107-1.3113-.3279h-.1822v.1093l1.0929 1.0686 2.0035 1.8092 2.5075 2.3314.1275.5768-.3218.4554-.34-.0486-2.2039-1.6575-.85-.7468-1.9246-1.621h-.1275v.17l.4432.6496 2.3436 3.5214.1214 1.0807-.17.3521-.6071.2125-.6679-.1214-1.3721-1.9246L14.38 17.959l-1.1414-1.9428-.1397.079-.674 7.2552-.3156.3703-.7286.2793-.6071-.4614-.3218-.7468.3218-1.4753.3886-1.9246.3157-1.53.2853-1.9004.17-.6314-.0121-.0425-.1397.0182-1.4328 1.9672-2.1796 2.9446-1.7243 1.8456-.4128.164-.7164-.3704.0667-.6618.4008-.5889 2.386-3.0357 1.4389-1.882.929-1.0868-.0062-.1579h-.0546l-6.3385 4.1164-1.1293.1457-.4857-.4554.0608-.7467.2307-.2429 1.9064-1.3114Z',
  github: 'M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12',
  shopify: 'M15.337 23.979l7.216-1.561s-2.604-17.613-2.625-17.73c-.018-.116-.114-.192-.211-.192s-1.929-.136-1.929-.136-1.275-1.274-1.439-1.411c-.045-.037-.075-.057-.121-.074l-.914 21.104h.023zM11.71 11.305s-.81-.424-1.774-.424c-1.447 0-1.504.906-1.504 1.141 0 1.232 3.24 1.715 3.24 4.629 0 2.295-1.44 3.76-3.406 3.76-2.354 0-3.54-1.465-3.54-1.465l.646-2.086s1.245 1.066 2.28 1.066c.675 0 .975-.545.975-.932 0-1.619-2.654-1.694-2.654-4.359-.034-2.237 1.571-4.416 4.827-4.416 1.257 0 1.875.361 1.875.361l-.945 2.715-.02.01zM11.17.83c.136 0 .271.038.405.135-.984.465-2.064 1.639-2.508 3.992-.656.213-1.293.405-1.889.578C7.697 3.75 8.951.84 11.17.84V.83zm1.235 2.949v.135c-.754.232-1.583.484-2.394.736.466-1.777 1.333-2.645 2.085-2.971.193.501.309 1.176.309 2.1zm.539-2.234c.694.074 1.141.867 1.429 1.755-.349.114-.735.231-1.158.366v-.252c0-.752-.096-1.371-.271-1.871v.002zm2.992 1.289c-.02 0-.06.021-.078.021s-.289.075-.714.21c-.423-1.233-1.176-2.37-2.508-2.37h-.115C12.135.209 11.669 0 11.265 0 8.159 0 6.675 3.877 6.21 5.846c-1.194.365-2.063.636-2.16.674-.675.213-.694.232-.772.87-.075.462-1.83 14.063-1.83 14.063L15.009 24l.927-21.166z',
  wordpress: 'M21.469 6.825c.84 1.537 1.318 3.3 1.318 5.175 0 3.979-2.156 7.456-5.363 9.325l3.295-9.527c.615-1.54.82-2.771.82-3.864 0-.405-.026-.78-.07-1.11m-7.981.105c.647-.03 1.232-.105 1.232-.105.582-.075.514-.93-.067-.899 0 0-1.755.135-2.88.135-1.064 0-2.85-.15-2.85-.15-.585-.03-.661.855-.075.885 0 0 .54.061 1.125.09l1.68 4.605-2.37 7.08L5.354 6.9c.649-.03 1.234-.1 1.234-.1.585-.075.516-.93-.065-.896 0 0-1.746.138-2.874.138-.2 0-.438-.008-.69-.015C4.911 3.15 8.235 1.215 12 1.215c2.809 0 5.365 1.072 7.286 2.833-.046-.003-.091-.009-.141-.009-1.06 0-1.812.923-1.812 1.914 0 .89.513 1.643 1.06 2.531.411.72.89 1.643.89 2.977 0 .915-.354 1.994-.821 3.479l-1.075 3.585-3.9-11.61.001.014zM12 22.784c-1.059 0-2.081-.153-3.048-.437l3.237-9.406 3.315 9.087c.024.053.05.101.078.149-1.12.393-2.325.609-3.582.609M1.211 12c0-1.564.336-3.05.935-4.39L7.29 21.709C3.694 19.96 1.212 16.271 1.211 12M12 0C5.385 0 0 5.385 0 12s5.385 12 12 12 12-5.385 12-12S18.615 0 12 0',
  laravel: 'M23.642 5.43a.364.364 0 01.014.1v5.149c0 .135-.073.26-.189.326l-4.323 2.49v4.934a.378.378 0 01-.188.326L9.93 23.949a.316.316 0 01-.066.027c-.008.002-.016.008-.024.01a.348.348 0 01-.192 0c-.011-.002-.02-.008-.03-.012-.02-.008-.042-.014-.062-.025L.533 18.755a.376.376 0 01-.189-.326V2.974c0-.033.005-.066.014-.098.003-.012.01-.02.014-.032a.369.369 0 01.023-.058c.004-.013.015-.022.023-.033l.033-.045c.012-.01.025-.018.037-.027.014-.012.027-.024.041-.034H.53L5.043.05a.375.375 0 01.375 0L9.93 2.647h.002c.015.01.027.021.04.033l.038.027c.013.014.02.03.033.045.008.011.02.021.025.033.01.02.017.038.024.058.003.011.01.021.013.032.01.031.014.064.014.098v9.652l3.76-2.164V5.527c0-.033.004-.066.013-.098.003-.01.01-.02.013-.032a.487.487 0 01.024-.059c.007-.012.018-.02.025-.033.012-.015.021-.03.033-.043.012-.012.025-.02.037-.028.014-.01.026-.023.041-.032h.001l4.513-2.598a.375.375 0 01.375 0l4.513 2.598c.016.01.027.021.042.031.012.01.025.018.036.028.013.014.022.03.034.044.008.012.019.021.024.033.011.02.018.04.024.06.006.01.012.021.015.032zm-.74 5.032V6.179l-1.578.908-2.182 1.256v4.283zm-4.51 7.75v-4.287l-2.147 1.225-6.126 3.498v4.325zM1.093 3.624v14.588l8.273 4.761v-4.325l-4.322-2.445-.002-.003H5.04c-.014-.01-.025-.021-.04-.031-.011-.01-.024-.018-.035-.027l-.001-.002c-.013-.012-.021-.025-.031-.04-.01-.011-.021-.022-.028-.036h-.002c-.008-.014-.013-.031-.02-.047-.006-.016-.014-.027-.018-.043a.49.49 0 01-.008-.057c-.002-.014-.006-.027-.006-.041V5.789l-2.18-1.257zM5.23.81L1.47 2.974l3.76 2.164 3.758-2.164zm1.956 13.505l2.182-1.256V3.624l-1.58.91-2.182 1.255v9.435zm11.581-10.95l-3.76 2.163 3.76 2.163 3.759-2.164zm-.376 4.978L16.21 7.087 14.63 6.18v4.283l2.182 1.256 1.58.908zm-8.65 9.654l5.514-3.148 2.756-1.572-3.757-2.163-4.323 2.489-3.941 2.27z',
  linkedin: 'M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z',
  adobe: 'M13.966 22.624l-1.69-4.281H8.122l3.892-9.144 5.662 13.425zM8.884 1.376H0v21.248zm15.116 0h-8.884L24 22.624Z',
  canva: 'M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zM6.962 7.68c.754 0 1.337.549 1.405 1.2.069.583-.171 1.097-.822 1.406-.343.171-.48.172-.549.069-.034-.069 0-.137.069-.206.617-.514.617-.926.548-1.508-.034-.378-.308-.618-.583-.618-1.2 0-2.914 2.674-2.674 4.629.103.754.549 1.646 1.509 1.646.308 0 .65-.103.96-.24.5-.264.799-.47 1.097-.8-.073-.885.704-2.046 1.851-2.046.515 0 .926.205.96.583.068.514-.377.582-.514.582s-.378-.034-.378-.17c-.034-.138.309-.07.275-.378-.035-.206-.24-.274-.446-.274-.72 0-1.131.994-1.029 1.611.035.275.172.549.447.549.205 0 .514-.31.617-.755.068-.308.343-.514.583-.514.102 0 .17.034.205.171v.138c-.034.137-.137.548-.102.651 0 .069.034.171.17.171.092 0 .436-.18.777-.459.117-.59.253-1.298.253-1.357.034-.24.137-.48.617-.48.103 0 .171.034.205.171v.138l-.136.617c.445-.583 1.097-.994 1.508-.994.172 0 .309.102.309.274 0 .103 0 .274-.069.446-.137.377-.309.96-.412 1.474 0 .137.035.274.207.274.171 0 .685-.206 1.096-.754l.007-.004c-.002-.068-.007-.134-.007-.202 0-.411.035-.754.104-.994.068-.274.411-.514.617-.514.103 0 .205.069.205.171 0 .035 0 .103-.034.137-.137.446-.24.857-.24 1.269 0 .24.034.582.102.788 0 .034.035.069.07.069.068 0 .548-.445.89-1.028-.308-.206-.48-.549-.48-.96 0-.72.446-1.097.858-1.097.343 0 .617.24.617.72 0 .308-.103.65-.274.96h.102a.77.77 0 0 0 .584-.24.293.293 0 0 1 .134-.117c.335-.425.83-.74 1.41-.74.48 0 .924.205.959.582.068.515-.378.618-.515.618l-.002-.002c-.138 0-.377-.035-.377-.172 0-.137.309-.068.274-.376-.034-.206-.24-.275-.446-.275-.686 0-1.13.891-1.028 1.611.034.275.171.583.445.583.206 0 .515-.308.652-.754.068-.274.343-.514.583-.514.103 0 .17.034.205.171 0 .069 0 .206-.137.652-.17.308-.171.48-.137.617.034.274.171.48.309.583.034.034.068.102.068.102 0 .069-.034.138-.137.138-.034 0-.068 0-.103-.035-.514-.205-.72-.548-.789-.891-.205.24-.445.377-.72.377-.445 0-.89-.411-.96-.926a1.609 1.609 0 0 1 .075-.649c-.203.13-.422.203-.623.203h-.17c-.447.652-.927 1.098-1.27 1.303a.896.896 0 0 1-.377.104c-.068 0-.171-.035-.205-.104-.095-.152-.156-.392-.193-.667-.481.527-1.145.805-1.453.805-.343 0-.548-.206-.582-.55v-.376c.102-.754.377-1.2.377-1.337a.074.074 0 0 0-.069-.07c-.24 0-1.028.824-1.166 1.373l-.103.445c-.068.309-.377.515-.582.515-.103 0-.172-.035-.206-.172v-.137l.046-.233c-.435.31-.87.508-1.075.508-.308 0-.48-.172-.514-.412-.206.274-.445.412-.754.412-.352 0-.696-.24-.862-.593-.244.275-.523.553-.852.764-.48.309-1.028.549-1.68.549-.582 0-1.097-.309-1.371-.583-.412-.377-.651-.96-.686-1.509-.205-1.68.823-3.84 2.4-4.8.378-.205.755-.343 1.132-.343zm9.77 3.291c-.104 0-.172.172-.172.343 0 .274.137.583.309.755a1.74 1.74 0 0 0 .102-.583c0-.343-.137-.515-.24-.515z',
  openai: 'M22.2819 9.8211a5.9847 5.9847 0 0 0-.5157-4.9108 6.0462 6.0462 0 0 0-6.5098-2.9A6.0651 6.0651 0 0 0 4.9807 4.1818a5.9847 5.9847 0 0 0-3.9977 2.9 6.0462 6.0462 0 0 0 .7427 7.0966 5.98 5.98 0 0 0 .511 4.9107 6.051 6.051 0 0 0 6.5146 2.9001A5.9847 5.9847 0 0 0 13.2599 24a6.0557 6.0557 0 0 0 5.7718-4.2058 5.9894 5.9894 0 0 0 3.9977-2.9001 6.0557 6.0557 0 0 0-.7475-7.0729zm-9.022 12.6081a4.4755 4.4755 0 0 1-2.8764-1.0408l.1419-.0804 4.7783-2.7582a.7948.7948 0 0 0 .3927-.6813v-6.7369l2.02 1.1686a.071.071 0 0 1 .038.052v5.5826a4.504 4.504 0 0 1-4.4945 4.4944zm-9.6607-4.1254a4.4708 4.4708 0 0 1-.5346-3.0137l.142.0852 4.783 2.7582a.7712.7712 0 0 0 .7806 0l5.8428-3.3685v2.3324a.0804.0804 0 0 1-.0332.0615L9.74 19.9502a4.4992 4.4992 0 0 1-6.1408-1.6464zM2.3408 7.8956a4.485 4.485 0 0 1 2.3655-1.9728V11.6a.7664.7664 0 0 0 .3879.6765l5.8144 3.3543-2.0201 1.1685a.0757.0757 0 0 1-.071 0l-4.8303-2.7865A4.504 4.504 0 0 1 2.3408 7.872zm16.5963 3.8558L13.1038 8.364 15.1192 7.2a.0757.0757 0 0 1 .071 0l4.8303 2.7913a4.4944 4.4944 0 0 1-.6765 8.1042v-5.6772a.79.79 0 0 0-.407-.667zm2.0107-3.0231l-.142-.0852-4.7735-2.7818a.7759.7759 0 0 0-.7854 0L9.409 9.2297V6.8974a.0662.0662 0 0 1 .0284-.0615l4.8303-2.7866a4.4992 4.4992 0 0 1 6.6802 4.66zM8.3065 12.863l-2.02-1.1638a.0804.0804 0 0 1-.038-.0567V6.0742a4.4992 4.4992 0 0 1 7.3757-3.4537l-.142.0805L8.704 5.459a.7948.7948 0 0 0-.3927.6813zm1.0976-2.3654l2.602-1.4998 2.6069 1.4998v2.9994l-2.5974 1.4997-2.6067-1.4997Z',
};

function icon(name, size = 24) {
  if (LOGO[name]) {
    return `<svg width="${size}" height="${size}" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="${LOGO[name]}"/></svg>`;
  }
  return `<svg width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${LINE[name]}</svg>`;
}

/* ---------- Data ---------- */

const AREAS = [
  { key: 'm', name: 'Marketing &amp; content', aria: 'Marketing en content', icon: 'marketing' },
  { key: 's', name: 'Sales',     icon: 'sales' },
  { key: 'c', name: 'Code',      icon: 'code' },
  { key: 'x', name: 'Change*',   icon: 'change', aria: 'Change', movable: true },
];

// Fases (rijen): Bereik, Kliks, Leads, Sales — met de RACE-fase als ondertitel.
const PHASES = [
  { stage: 'Bereik', face: 'face1', race: 'reach',   desc: 'Verhoog je zichtbaarheid',        flow: 'pull' },
  { stage: 'Kliks',  face: 'face2', race: 'act',     desc: 'Boost je traffic & interactie',   flow: 'pull' },
  { stage: 'Leads',  face: 'face3', race: 'convert', desc: 'Genereer aanvragen & deals',      flow: 'push' },
  { stage: 'Sales',  face: 'face4', race: 'engage',  desc: 'Actieve follow-up top prospects', flow: 'push' },
];

// CELLS[fase][gebied] = [label, icoon]
const CELLS = [
  [['Displaycampagnes, SEO', 'eye'], ['Direct mail, events', 'mail'], ['Sites, platforms', 'browser'], ['Merk- & productpositionering', 'compass']],
  [['Klikcampagnes, UI/UX', 'cursor'], ['Salespitch, lead-inzichten', 'chat'], ['Landingspages, CRO', 'bag'], ['Processen & structuur', 'org']],
  [['Leadcampagnes, -magnets', 'funnel'], ['Follow-up, (bel-)scripts', 'phone'], ['Configurators, pijplijn', 'sliders'], ['Leiderschap & management', 'people']],
  [['Retargetingcampagnes, datamanagement', 'target'], ['Pitch, salestechniek', 'board'], ['Dashboards, automations', 'bars'], ['Businessmodel & waardepropositie', 'canvas']],
];

// Tools per gebied: [icoon, naam, merkkleur of img-modus]. Lijnicoon zonder kleur = generiek (geen logo).
const TOOLS = [
  [
    ['google', 'Google', '#4285F4'],
    ['linkedin', 'LinkedIn', '#0A66C2'], ['meta', 'Meta', '#0467DF'], ['tiktok', 'TikTok', '#000000'],
    ['pinterest', 'Pinterest', '#BD081C'], ['snapchat', 'Snap', '#000000'],
    ['bars', 'SEO PowerSuite'], ['adobe', 'Adobe', '#FF0000'], ['canva', 'Canva', '#00C4CC'],
  ],
  [
    ['img:leadinfo', 'Leadinfo', 'fill'], ['img:mailchimp', 'Direct mail (Mailchimp)', 'fill'],
    ['notion', 'Notion', '#000000'], ['img:pipedrive', 'Pipedrive', 'fill'], ['img:emailoctopus', 'EmailOctopus'],
  ],
  [
    ['claude', 'Claude Code', '#D97757'], ['openai', 'Codex', '#000000'], ['github', 'GitHub', '#181717'],
    ['shopify', 'Shopify', '#7AB55C'], ['wordpress', 'WordPress', '#21759B'], ['laravel', 'Laravel', '#FF2D20'],
  ],
  [
    ['mark:strategyzer', 'Strategyzer'], ['mark:covey', 'Covey'], ['mark:lean', 'Lean'], ['mark:brandthechange', 'Brand the Change'],
  ],
];

// Standaard aangeklikte blokken.
const selected = new Set(['m1', 'c1', 'c2', 'x2', 'c3']);

/* ---------- Render ---------- */

// Icoon in een tool-chip. 'img:naam' = aangeleverd logo uit IMG (3e veld 'fill' of 'fit'),
// 'mark:naam' = nagetekend merkteken, anders lijnicoon of Simple Icons-logo in merkkleur.
function toolIcon(ic, extra) {
  if (ic.startsWith('img:')) {
    return `<span class="tool-icon tool-icon--${extra || 'fit'}"><img src="${IMG[ic.slice(4)]}" alt="" width="26" height="26"></span>`;
  }
  if (ic.startsWith('mark:')) {
    return `<span class="tool-icon tool-icon--fill">${MARK[ic.slice(5)]}</span>`;
  }
  return `<span class="tool-icon"${extra ? ` data-brand style="--brand:${extra}"` : ''}>${icon(ic, 16)}</span>`;
}

const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;');

// Change-blokken zijn over alle fases toepasbaar en dus verticaal te verwisselen.
// slots[rij] = index van het Change-onderwerp (rij in CELLS) dat in die fase staat.
const MOVABLE = AREAS.findIndex((a) => a.movable);
const SLOTS_KEY = 'powermarketing-change-slots';
let slots = [0, 1, 2, 3];
try {
  const saved = JSON.parse(localStorage.getItem(SLOTS_KEY));
  if (Array.isArray(saved) && saved.slice().sort().join() === '0,1,2,3') slots = saved;
} catch (e) { /* geen opslag beschikbaar */ }

function render() {
  document.getElementById('col-heads').innerHTML = '<div></div>' + AREAS.map((a) => `
  <div class="col-head"><div class="disc disc--lg">${icon(a.icon, 28)}</div><h2>${a.name}</h2></div>`).join('');

  let n = 0;
  document.getElementById('grid').innerHTML = PHASES.map((p, r) => `
  <div class="phase">
    <div class="phase__title"><span class="disc disc--sm">${icon(p.face, 22)}</span><h3>${p.stage}</h3></div>
    <div class="phase__desc">${esc(p.desc)}</div>
    <div class="phase__stage mono">${p.flow} · ${p.race}</div>
  </div>` + AREAS.map((a, c) => {
    const src = a.movable ? slots[r] : r;          // welk onderwerp staat hier
    const id = a.key + (src + 1);
    const [label, ic] = CELLS[src][c];
    n += 1;
    const extra = a.movable
      ? ` data-slot="${r}" title="Klik om te kiezen · sleep naar een andere fase om te wisselen (of Alt + ↑/↓)"`
      : '';
    return `
  <button type="button" class="cell${a.movable ? ' cell--movable' : ''}" data-id="${id}" aria-pressed="${selected.has(id)}"${extra}
          aria-label="${esc(`${a.aria || a.name}, ${p.stage}: ${label}`)}">
    <span class="cell__top"><span class="mono">${String(n).padStart(2, '0')}</span><span class="cell__rocket">${icon('rocket')}</span></span>
    <span>${icon(ic, 36)}</span>
    <span class="cell__label">${esc(label)}</span>
  </button>`;
  }).join('')).join('');

  document.getElementById('tools').innerHTML = '<div class="tools-title">Tools &amp; kanalen</div>' + AREAS.map((a, c) => `
  <ul class="chips">${TOOLS[c].map(([ic, name, brand]) => `
    <li class="chip">${toolIcon(ic, brand)}${esc(name)}</li>`).join('')}
  </ul>`).join('');

  updateCount();
}

// Verwissel de Change-onderwerpen van fase 'from' en fase 'to'.
function swapSlots(from, to) {
  if (to < 0 || to >= slots.length || from === to) return false;
  [slots[from], slots[to]] = [slots[to], slots[from]];
  try { localStorage.setItem(SLOTS_KEY, JSON.stringify(slots)); } catch (e) { /* negeren */ }
  render();
  return true;
}

document.querySelectorAll('[data-icon]').forEach((el) => {
  el.outerHTML = icon(el.dataset.icon, Number(el.dataset.size) || 24);
});

/* ---------- Interactie ---------- */

function updateCount() {
  const count = selected.size;
  document.getElementById('count').textContent = count;
  document.getElementById('count-label').textContent = count === 1 ? 'raket' : 'raketten';
}

document.getElementById('grid').addEventListener('click', (e) => {
  const cell = e.target.closest('.cell');
  if (!cell) return;
  const id = cell.dataset.id;
  selected.has(id) ? selected.delete(id) : selected.add(id);
  cell.setAttribute('aria-pressed', selected.has(id));
  updateCount();
});

// Verslepen: pak een Change-blok en sleep het naar een andere fase (muis en touch).
// Bij loslaten wisselen de twee blokken van plek.
let drag = null;
let suppressClick = false;
const grid = document.getElementById('grid');

function slotAt(y) {
  let best = 0;
  let dist = Infinity;
  grid.querySelectorAll('.cell--movable').forEach((el) => {
    // Het versleepte blok zelf telt mee op zijn oorspronkelijke plek (zonder verschuiving).
    const r = el === drag.el ? drag.home : el.getBoundingClientRect();
    const d = Math.abs(y - (r.top + r.height / 2));
    if (d < dist) { dist = d; best = Number(el.dataset.slot); }
  });
  return best;
}

grid.addEventListener('pointerdown', (e) => {
  const cell = e.target.closest('.cell--movable');
  if (!cell || e.button !== 0) return;
  drag = { el: cell, home: cell.getBoundingClientRect(), slot: Number(cell.dataset.slot), startY: e.clientY, target: null, active: false };
});

window.addEventListener('pointermove', (e) => {
  if (!drag) return;
  const dy = e.clientY - drag.startY;
  if (!drag.active) {
    if (Math.abs(dy) < 8) return;
    drag.active = true;
    document.body.classList.add('is-dragging');
    drag.el.classList.add('is-lifted');
  }
  e.preventDefault();
  drag.el.style.transform = `translateY(${dy}px) scale(1.02)`;
  const target = slotAt(e.clientY);
  grid.querySelectorAll('.is-target').forEach((el) => el.classList.remove('is-target'));
  drag.target = target !== drag.slot ? target : null;
  if (drag.target !== null) grid.querySelector(`.cell--movable[data-slot="${target}"]`).classList.add('is-target');
});

function endDrag() {
  if (!drag) return;
  const { active, slot, target, el } = drag;
  drag = null;
  document.body.classList.remove('is-dragging');
  el.classList.remove('is-lifted');
  el.style.transform = '';
  grid.querySelectorAll('.is-target').forEach((x) => x.classList.remove('is-target'));
  if (!active) return;
  suppressClick = true;
  setTimeout(() => { suppressClick = false; }, 0);
  if (target !== null) swapSlots(slot, target);
}
window.addEventListener('pointerup', endDrag);
window.addEventListener('pointercancel', endDrag);

// Na een sleepbeweging geen klik doorgeven (anders wisselt het blok van status).
document.addEventListener('click', (e) => {
  if (suppressClick) { e.stopPropagation(); e.preventDefault(); suppressClick = false; }
}, true);

// Toetsenbord: Alt + pijl omhoog/omlaag verwisselt met het blok erboven/eronder.
grid.addEventListener('keydown', (e) => {
  const cell = e.target.closest('.cell--movable');
  if (!cell || !e.altKey || (e.key !== 'ArrowUp' && e.key !== 'ArrowDown')) return;
  e.preventDefault();
  const from = Number(cell.dataset.slot);
  const id = cell.dataset.id;
  if (swapSlots(from, from + (e.key === 'ArrowUp' ? -1 : 1))) grid.querySelector(`[data-id="${id}"]`).focus();
});

render();
</script>
</body>
</html>

````
