# Maxima configurator 2.0

Configurator voor alle 32 Maxima-modellen, voor Klop Watersport als dealer. Vervangt de iframe naar
maximaboats.nl op klopwatersport.nl. Op de nieuwe site (`site/`) vervangt hij ook de Mustang-iframe,
die alleen de Maxima 760 had.

De configurator gebruikt de Maxima-huisstijl (inkt `#1a1a23`, goud `#aa9882`, Karla en Playfair Display).
Het designsysteem van Klop zegt namelijk: *"Maxima Boats is een apart merk en krijgt geen Klop-opmaak."*
Klop staat als dealer in de kop en de voet. Aanvragen gaan naar Klop.

## Wat is er nieuw ten opzichte van 1.0

| | 1.0 | 2.0 |
|---|---|---|
| Stappen | 11 tot 13 lange lijsten zoals bij Maxima | 7 tot 9 stappen met subgroepen (bijv. Exterieur: Deluxe pakket, Voordek, Besturing, Dek, Beveiliging) |
| Keuzes die elkaar uitsluiten | konden samen aangevinkt worden (twee Deluxe pakketten, twee tafels) | "optioneel, kies er één" met een Geen-optie |
| Kussensets | 14 opties (7 stoffen × glad/ruitjes) | 7 stoffen plus een aparte keuze "Stiksel" |
| RAL-kleur | alleen de meerprijs | invoerveld voor de RAL-code, verplicht bij die keuze |
| Namen | "Rompkleur donker blauw", "30 Honda LRTU" | "Donkerblauw", "Honda 30 pk LRTU", met toelichting eronder |
| Afronden | formulier onderaan | overzichtsstap met alle keuzes, "Wijzig" per sectie, ontbrekende keuzes, prijsopbouw, pdf, link en offerte |
| Huisstijl | oude klopwatersport.nl-stijl | Maxima-huisstijl |
| Site-integratie | geen | `?embed=1` en `tools/patch_maxima.py` |

Links uit 1.0 (`?model=…&c=…`) blijven werken, ook met ruitjeskussens.

## Nieuw in 2.1

- **Voorproefje:** met de muis of het toetsenbord op een kleur, kap of kussenset zie je die direct op de boot, nog voordat je kiest.
- **Afhankelijkheden** (uit `curate.py`, alleen waar de optienaam ze noemt):
  - *Hard:* "Blindering buiskap" en "Uitritsbaar voorraam buiskap" kunnen alleen met een buiskap. Zonder buiskap zijn ze uitgeschakeld met uitleg. Kies je later "Geen buiskap", dan verdwijnen ze en zegt een melding dat.
  - *Zacht:* Garmin-uitbreidingen (audio, tweede scherm, radar, stuurautomaat) krijgen een waarschuwing zonder Garmin-display, ook in het overzicht.
- **Prijsfeedback:** het totaal telt op en af en laat kort het verschil zien (bijv. "+ € 550").
- **Jouw keuzes:** onder het bootbeeld (desktop) alle keuzes met prijs en een voortgangsbalk voor de verplichte keuzes.
- **Groot beeld:** de knop "Groot" toont de boot schermvullend, met alle drie de aanzichten.
- **Berichten aan de site alleen naar de eigen oorsprong:** de configurator meldt zijn stand en aanvragen (met contactgegevens) alleen aan `parentOrigin` (standaard dezelfde oorsprong), niet aan elke pagina die hem inbouwt.
- **Stuur naar een adviseur:** opent WhatsApp met de samenstelling, het totaal en de link. De bezoeker verstuurt het bericht zelf.

## Mappen

| Pad | Inhoud |
|---|---|
| `public/index.html` | De pagina (overzicht en configurator) |
| `public/assets/configurator.js` | Logica, vanilla JS zonder build-stap |
| `public/assets/configurator.css` | Styling |
| `public/api/offerte.php` | Mailt offerte- en hulpaanvragen naar de verkoop |
| `public/data/*.json` | Ingedeelde modeldata (gemaakt door `curate.py`) |
| `bron/*.json` | Ruwe data van Maxima (gemaakt door `scrape_maxima.py`) |
| `scripts/scrape_maxima.py` | Haalt prijzen, opties en beeldlagen op bij de dealerconfigurator van Maxima |
| `scripts/curate.py` | Deelt de ruwe data in: secties, groepen, namen, stiksel, RAL |

## Lokaal draaien

```bash
cd maxima-configurator/public
php -S localhost:8000          # met mail-endpoint
# of: python3 -m http.server 8000  (zonder endpoint; dan opent de mailclient van de bezoeker)
```

Open http://localhost:8000/ of http://localhost:8000/?model=maxima-760-nieuw.

## URL's

| URL | Wat |
|---|---|
| `?` | Overzicht van alle modellen |
| `?model=maxima-550` | Configurator voor dat model |
| `?p=1785` | Idem, via het Maxima-product-id uit de oude iframe-links |
| `&c=41651.41680…` | Gekozen opties (originele Maxima-optie-id's) |
| `&ral=rompkleur~7016` | RAL-code per groep |
| `&stap=3`, `&stap=overzicht` | Open stap |
| `&embed=1` | Zonder eigen kop en voet, voor een iframe |

De samenstelling wordt per model ook in de browser onthouden.

## Data bijwerken

```bash
pip install beautifulsoup4
python3 maxima-configurator/scripts/scrape_maxima.py   # ruwe data naar bron/
python3 maxima-configurator/scripts/curate.py          # ingedeelde data naar public/data/
```

`curate.py` meldt opties die geen regel raken. Die komen onder "Overig" en horen een regel in `RULES`
te krijgen. Het script controleert niet zelf of er opties verloren gaan. Dat is wel nagelopen: alle
Maxima-optie-id's uit `bron/` komen terug in `public/data/`.

## Koppeling met de nieuwe site

`python3 tools/patch_maxima.py site/index.html` (vanuit de root; is al toegepast):

- `#/stel-samen/maxima` toont het overzicht van alle Maxima-modellen.
- `#/stel-samen/maxima-<model>` toont de configurator voor dat model. De oude link `#/stel-samen/maxima-760` blijft werken.
- "Stel samen" bij 22 Maxima-boten gaat direct naar het juiste model. De Maxima 485 en 730i zitten niet in de Maxima-configurator en houden de algemene configurator.
- De iframe laadt `../maxima-configurator/public/?model=…&embed=1`. Pas `MXC` in het script aan als de configurator elders gehost wordt.

Daarna `python3 tools/patch_configurator.py site/index.html`:

- De Maxima-pagina is schermvullend: een smalle Klop-balk met model en totaal, de configurator eronder. Geen dubbele kop, geen voet, geen actiebalk.
- In embed-modus stuurt de configurator berichten naar de site (`postMessage`, `source: 'klop-mx'`): `overview`, `state` (model, keuzes, totaal, compleet) en `quote`/`help` bij een aanvraag.
- De site zet de samenstelling in de adresbalk (`#/stel-samen/maxima-760-nieuw?c=…&ral=…&stap=…`), zodat hij deelbaar is en terug te openen.
- "Bewaar in Mijn Klop" en offerteaanvragen komen in Mijn Klop > Configuraties, met "Verder samenstellen".

## Aandachtspunten

- **Afbeeldingen** (bootlagen, optiefoto's, modelfoto's) komen direct van maximaboats.nl. Stem met Maxima af of dat mag, of host ze zelf.
- **3D:** de Mustang-versie van de 760 heeft een 3D-model. Daarvoor zijn per model 3D-bestanden nodig. Deze versie gebruikt de 2D-beeldlagen van Maxima, met zij-, achter- en vooraanzicht.
- **Maxima 800 sport** heeft bij Maxima geen beeldlagen. Daar toont de configurator de modelfoto.
- **Prijzen** zijn overgenomen van de dealerconfigurator van Maxima en zijn een indicatie.
- **Exclusiviteit** ("kies er één") is afgeleid uit de optienamen. Controleer bij twijfel met Maxima of combinaties toch mogelijk zijn (bijv. GPS-dieptemeter plus Glass cockpit).
