# Klop Watersport — Maxima configurator

Eigen herbouw van de Maxima Boats-configurator die nu als iframe van maximaboats.nl op
[klopwatersport.nl/boot-configureren](https://www.klopwatersport.nl/boot-configureren/?id=97) staat,
in de huisstijl van Klop Watersport.

## Wat zit erin

| Onderdeel | Bestand |
|---|---|
| Pagina (overzicht + configurator) | `public/index.html` |
| Logica (vanilla JS, geen build) | `public/assets/configurator.js` |
| Styling | `public/assets/configurator.css` |
| Offerte- en hulpaanvragen mailen | `public/api/offerte.php` |
| Modeldata (32 modellen) | `public/data/*.json` |
| Data synchroniseren met Maxima | `scripts/scrape_maxima.py` |

### Functies
- Overzicht van alle Maxima-modellen met zoeken, filter (brandstof/elektrisch) en sorteren.
- Configurator per model: stappen (accordeon) met kleurvlakjes, optiefoto's met zoom, enkel- en meerkeuze.
- Live bootvoorbeeld uit gelaagde afbeeldingen, met zij-, achter- en vooraanzicht.
- Live totaalprijs plus een prijsspecificatie (basisprijs, opties en afleverkosten).
- Deelbare link (`?model=maxima-550&c=…`). De configuratie wordt ook lokaal onthouden.
- Offerteaanvraag (controleert of alle verplichte stappen gekozen zijn), hulpaanvraag, PDF via printen.
- Mobiel: vaste balk onderin met totaalprijs en offerteknop.
- Spamfilter (honeypot) en rate limit op het PHP-endpoint. Als het endpoint niet bereikbaar is, opent de mailclient van de bezoeker.

## Lokaal draaien

```bash
cd public
php -S localhost:8000      # of: python3 -m http.server 8000 (dan zonder mail-endpoint)
```

Open daarna http://localhost:8000/ of http://localhost:8000/?model=maxima-550.

## Integratie op klopwatersport.nl

1. Zet de map `public/` op de server, bijvoorbeeld als `/maxima-configurator/`.
2. Stel in `public/index.html` (`window.KLOP_CONFIG`) en `public/api/offerte.php` (`TO_EMAIL`, `FROM_EMAIL`) de juiste adressen in.
3. Vervang op `/boot-configureren/` de iframe naar maximaboats.nl door een link of iframe naar
   `/maxima-configurator/?p=<maxima-product-id>`. Het oude product-id uit de huidige iframe-URL
   werkt direct (bijv. Maxima 550: `?p=1785`). Een slug mag ook: `?model=maxima-550`.

## Data bijwerken

Prijzen, opties en afbeeldingspaden komen van de dealerconfigurator van Maxima (dealer-hash van Klop).
Draai het script opnieuw als Maxima iets wijzigt:

```bash
pip install beautifulsoup4
python3 scripts/scrape_maxima.py
```

Het script stopt zonder bestanden te overschrijven als een model geen stappen oplevert
(bijv. door de bot-check van maximaboats.nl).

## Aandachtspunten
- **Afbeeldingen** (bootlagen, optiefoto's, modelfoto's) worden direct vanaf maximaboats.nl geladen.
  Stem met Maxima af of dat mag, of host ze zelf.
- De Maxima 800 sport heeft bij Maxima geen gelaagde afbeeldingen. Daar toont de configurator de modelfoto.
- Prijzen zijn een indicatie, overgenomen van de Maxima-configurator.
