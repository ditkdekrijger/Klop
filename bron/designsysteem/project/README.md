# Klop Watersport

Het designsysteem van Klop Watersport: vrijheidsvaarders sinds 1966. Gebouwd uit het brandbook en de recap.

## Merkverhaal (content fundamentals)

- **Hoofdpositionering:** "Vaar je vrijheid." Afzender: "Vrijheidsvaarders sinds 1966."
- **Keten:** Vaar je vrijheid, Zonder gedoe, Klop Premium Service™. De methodiek heet altijd *Klop Premium Service™* en is overal klikbaar naar de servicepagina.
- **Alinea-zin:** "Wij regelen het gedoe. Jij vaart." Als kop alleen in de Premium Service-strook en het blok Zonder gedoe.
- **Toon:** Nederlands, je-vorm (jij, je, jouw), kort en concreet. Nooit u, uw of uzelf. Geen gedachtestreepjes. Geen verzonnen reviews, cijfers of urgentie. Zodra het over boten gaat: praktisch en feitelijk, niet abstract ("Op voorraad bij Klop", "Stel zelf je maatwerk boot samen").
- Het team heet *Vrijheidsvaarders*. Routes heten *Vrijheidsroutes*. De klantomgeving heet *Mijn Klop*.
- Maxima Boats is een apart merk en krijgt geen Klop-opmaak.

## Visuele basis

- **Kleur:** Gelcoat (`gelcoat`) als ondergrond, Nachtblauw (`nachtblauw`) als tekst en donker vlak, Diep (`diep`) als tweede donker. Oliegoed (`oliegoed`) betekent "geregeld".
- **Type:** Funnel Display weight 300 voor koppen met negatieve letterspatiëring. Funnel Sans 400/500 voor tekst.
- **Vorm: Waterlijn.** Knoppen, chips, tegels en labels zijn pillen of hebben `radius-water` (22px, tegels 18px). Het kader in een foto volgt `radius-kader` (14px). Invoervelden houden een lijn onderaan.
- **Lijnen:** hairlines zijn waterlijnen (Vaarspoor). Tekstlinks, menu-items, footerlinks en bootnamen krijgen bij hover een golflijn die van links naar rechts verschijnt en dan langzaam meestroomt.
- **Beeld:** foto's krijgen het waterlijst-kader. Het kleurenlogo staat op een witte plaat bij foto's en donkere vlakken.
- **Beweging:** water vult knoppen van onderen, beeld zoomt langzaam, reveal op scroll, view-transitions tussen pagina's, header verbergt bij omlaag scrollen en keert terug bij omhoog. Geen bounce. Bij "beperk beweging" staat alles stil.

## Iconografie

Eigen set lijniconen op raster 48 x 48, lijn 1.25 px, ronde lijneinden. Eén inkt. Op geel of donker in een ronde icoonring.

## Componenten

Button, Icon, Label, Card (bootkaart), Fotokader, Vaarspoor, Nav, **PremiumStrook** (gele sectie met foto's), **Tegel** (vaardersvinder), **BootResultaat** (lijstkaart met filters en labels), **Vergelijken** (beste per rij), **Prijsinzicht** (plek in het type).

Toegevoegd met de laatste versie van de site:

- **MegaMenu**: uitklap onder de hoofdnavigatie met foto's en logo's in plaats van tekstlijsten.
- **MerkTegel**, **Categorietegel**, **MerkHero**: merkbeleving op merk- en bootpagina's. Elke categorie en subcategorie heeft een foto.
- **PdfModal**: e-mailadres achterlaten en de vergelijking als PDF bewaren.
- **MijnKlopHero**, **MijnKlopTegel**, **Voortgang**: de klantomgeving Mijn Klop.

## Navigatie

Volgorde: **Boten, Showroom, Klop Premium Service™, Over ons**. Onder Boten staan merken (logo op witte plaat) en soorten boten met foto. Merkpagina's openen met een MerkHero, daarna type-tegels, uitgelichte boten, galerij en slotbanner. Containerbreedte 1320px; overzichten met veel kolommen (boten, vergelijken) gebruiken 1560px (tokens `container`, `container-breed`).

## Vergelijken en PDF

Bovenaan de vergelijking: schakelaar "Alleen verschillen tonen", knop "Bewaar als PDF" en "Vergelijking wissen". Bewaar als PDF vraagt eerst een e-mailadres ("Laat je e-mailadres achter") (leadmoment, met toestemming voor contact door een adviseur) en opent daarna het printvenster. De print is A4 liggend met Klop-kop, datum en ontvanger. De preview verstuurt geen mail en zegt dat ook.

## Mijn Klop

Donkere zijbalk met tien onderdelen: Overzicht, Mijn boot (gegevens en logboek), Seizoenschecklist, Serviceplanner, Afspraken, Documenten, Klop Premium Service™, Favorieten (met vergelijking), Configuraties, Mijn aanspreekpunt. Invoer wordt bewaard. Documenten zonder inhoud staan als "Straks beschikbaar". Geen verzonnen cijfers of gegevens; alles wat nog niet bestaat is als voorbeeld gelabeld.

## Regels

1. Geel is zeldzaam. Per scherm één gele accent, met één uitzondering: de PremiumStrook is een volledige gele band, één keer per pagina. Op die pagina blijven andere gele accenten beperkt tot kleine markeringen.
2. Geel op Nachtblauw of Gelcoat, nooit gele tekst op wit. Op een gele band staat nachtblauw.
3. Tekst minimaal 17px (bijschriften en meta 15px), koppen weight 300.
4. Het kleurenlogo nooit direct op een foto.
5. Geen scherpe hoeken en geen rechte decoratieve lijnen.
6. Bootvergelijking toont alleen berekenbare feiten uit de eigen voorraad. Geen verzonnen scores of schaarste.
7. Klop Premium Service™ is altijd Oliegoed, in labels, knoppen en tegels.
8. Merklogo's staan altijd in kleur op een witte plaat bij foto's. Elke categorie en subcategorie heeft een foto.
9. Gele knop: één per blok (Plan service, Maak PDF, Bekijk alle n boten). Een tweede actie is omlijnd.
10. Voorraad is altijd direct zichtbaar: een Nachtblauwe pill "Op voorraad" met gele stip linksonder op de foto van elke boot die op voorraad is (kaart, lijstkaart, uitgelichte boot), en in de tekst "Op voorraad" in plaats van "Direct leverbaar". Boten op bestelling krijgen geen badge.
11. In de header krijgt Klop Premium Service™ altijd een geel accent: gele stip voor het label en een gele lijn eronder, op licht en op donker. Het label zelf blijft wit of nachtblauw.
12. Aanspreekvorm: overal je-vorm, ook in Mijn Klop, formulieren, de PDF en foutmeldingen.
