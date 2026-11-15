# Klop Watersport

Herpositionering "Vaar je vrijheid." Alles op één plek.

| Map | Inhoud |
|---|---|
| `overzicht/index.html` | **Het ene overzichtsbestand**: recap, brandbook, designsysteem, merkuitingen en de website |
| `site/index.html` | De klikbare website (213 boten), met de showroom centraal op de homepage |
| `bron/` | Ruwe bronbestanden uit de ontwerpen: recap, brandbook, merkuitingen (boards + beeld) en designsysteem (tokens, iconen, logo's, componenten) |
| `tools/` | Scripts om alles opnieuw te bouwen |
| `maxima-configurator/` | Maxima-configurator 2.0 voor alle 32 modellen, gekoppeld aan de site (zie de README in die map) |

## Opnieuw bouwen

```bash
node tools/render_boards.js          # boards en componenten naar overzicht/ov/
python3 tools/build_overzicht.py     # overzicht/index.html
# site/index.html opnieuw opbouwen vanaf de originele site, in deze volgorde:
python3 tools/patch_showroom.py site/index.html   # showroom-uitbreiding
python3 tools/patch_maxima.py site/index.html     # Maxima-configurator 2.0 koppelen
python3 tools/patch_mobile.py site/index.html     # mobiele UX
```

Lokaal bekijken: `python3 -m http.server` in de root en open `/overzicht/`.
