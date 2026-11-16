"""Bouwt tools/beeld_sectie.html: deepdive op de beelden van de merkuitingen."""
import os, html, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
e = html.escape
TAGS = {
 'T': ('Letter', 'Tekst in het beeld is door de generator getekend: schreefletter in plaats van Funnel, onscherp of fout.'),
 'U': ('U-vorm', 'De u-vorm staat in het beeld zelf ("Uw boot", "U vaart"). Niet te corrigeren zonder nieuw beeld.'),
 'L': ('Logo', 'Het embleem is een leeg blauw ovaal, of staat los op de foto in plaats van op een witte plaat.'),
 'N': ('Naam', 'Verzonnen namen (Peter Klöpfer, Kees, Hugo, Pieter, Daan Klop). Gebruik echte Vrijheidsvaarders, met toestemming.'),
 'Z': ('Zon', 'Weer gouden tegenlicht met de zon in beeld. Het brandbook vraagt laag licht, ook mist en blauw uur; nu is het eentonig.'),
 'B': ('Boot', 'Steeds dezelfde witte sloep, geen boot uit de eigen voorraad of van de eigen merken.'),
 'F': ('Feit', 'Klopt niet met de site of de werkelijkheid: oud schermontwerp, verzonnen boot of interface, verkeerd gebouw of auto.'),
 'G': ('Geel', 'Te veel geel (meer dan één vlak) of een oranje tint in plaats van Oliegoed #EFA91F.'),
 'R': ('Resolutie', 'Te klein voor print: 1024 of 1400 px breed. Billboard en abri vragen minstens 6.000 px of een opgemaakt bestand.'),
 'E': ('Moet echt', 'Mensen, gebouw, haven en werkplaats: het brandbook zegt eigen mensen en eigen plek, geen stockbeeld.'),
}
SPOOR = {
 'FOTO': ('Fotodag', 'Echte foto op locatie, met eigen mensen en boten.'),
 'SCHERM': ('Echt scherm', 'Screenshot van de echte site, configurator of Mijn Klop in een apparaat, automatisch gemaakt.'),
 'DRUK': ('Drukwerk eerst', 'Eerst de echte opmaak (pas, label, offerte, bordje), daarna als mockup of drukproef in beeld.'),
 'PLAAT': ('AI-plaat + opmaak', 'Alleen de scène genereren, zonder tekst of logo. Tekst, logo en label komen uit de opmaaklaag.'),
 'OK': ('Bruikbaar', 'Kan blijven als sfeerplaat, eventueel opschalen.'),
}
# nr, uiting, wat moet het laten zien, tags, spoor, prioriteit, toelichting
R = [
 (1,'Cover','Sfeer, rivier in ochtendmist','R','OK',3,'Goede plaat: rust, veel lucht en water. Alleen groter nodig voor print.'),
 (4,'M01 Mijn Klop','De status van je boot op de telefoon','TUZ','SCHERM',1,'"Uw boot ligt voor u klaar" staat in het beeld. Vervang het scherm door de echte Mijn Klop.'),
 (5,'M02 Service-updates','Bericht dat de boot klaar ligt','TUNZ','SCHERM',1,'Chattekst in u-vorm en ondertekend door "Kees". Echte melding in de app tonen.'),
 (6,'M03 Serviceplaatje','Plaatje op de boot met QR','TZ','DRUK',2,'Concept klopt. Plaatje eerst echt opmaken, dan fotograferen of als vector op de foto zetten.'),
 (7,'M04 Vandaag geregeld','Scherm in de showroom','TFG','SCHERM',2,'Nep-interface met vijf gele balken. Echt scherm uit het CRM tonen, op de echte showroomwand.'),
 (8,'M05 Overdrachtsbox','De box bij de aflevering','GZ','DRUK',2,'Box is helemaal geel: geel is een label, geen verpakking. Box nachtblauw, met één geel label.'),
 (9,'M06 Servicepas','De pas met je vaste aanspreekpunt','TNLZ','DRUK',1,'"Peter Klöpfer" en een leeg ovaal als logo. Echte pasopmaak met een echte Vrijheidsvaarder.'),
 (10,'M07 Logboek','Het gebonden logboek','TZ','DRUK',3,'Sterk beeld. Kaftopmaak in Funnel en het echte embleem, daarna productfoto.'),
 (11,'M08 Het gele label','Het kernbeeld: label aan het stuur','TNZ','PLAAT',1,'Het beste beeld van de serie, maar het label is getekend en ondertekend door "Hugo". Label als opmaak, echte voornaam.'),
 (12,'M09 Klop-onderhouden','Bordje bij een gebruikte boot','TB','FOTO',2,'Bordje in schreefletter. Echte occasion in de eigen showroom fotograferen met opgemaakt bordje.'),
 (13,'M10 Gevel en entree','De payoff waar je binnenkomt','TLFE','FOTO',1,'Verzonnen gebouw en leeg logo-ovaal. Echte gevel aan de Rivierdijk fotograferen, belettering als opmaak erop.'),
 (14,'M11 Servicebalie','De balie met de belofte','TE','FOTO',2,'Verzonnen medewerker. Echte balie en echte collega, wandtekst als opmaak.'),
 (15,'M12 Showroombordje','Bordje bij elke nieuwe boot','TB','DRUK',2,'Concept klopt. Bordje echt opmaken (Funnel, Oliegoed) en bij een echte boot uit de voorraad zetten.'),
 (16,'M13 Servicehaven','Steiger 2, boot ligt klaar','ZBE','FOTO',2,'Mooi beeld, maar het is niet de eigen haven. Op de fotodag nemen, in de ochtend.'),
 (17,'M14 Stalling','Droog en veilig gestald','BE','FOTO',2,'Generieke hal. De echte stalling met gele labels aan de hoezen fotograferen.'),
 (18,'M15 Beursstand','Stand op de Hiswa','TG','PLAAT',3,'Twee gele vlakken en schreefletter op de wand. Stand als 3D-render met de echte opmaak.'),
 (19,'M16 Het oliegoed','Monteur in de gele jas','ZE','FOTO',1,'Sterk idee, verzonnen persoon. Een echte monteur, in de schemering, kijkt in de camera.'),
 (20,'M17 Naambadge','Collega bij naam','NE','FOTO',2,'"Kees" bestaat niet. Badge van een echte Vrijheidsvaarder.'),
 (21,'M18 De overdracht','Sleutel over, aanspreekpunt erbij','ZE','FOTO',1,'Belangrijk moment, nu stockachtig. Op de fotodag met echte klanten (toestemming) of acteurs.'),
 (22,'M19 Zo doen wij het','Kaartje in de borstzak','E','FOTO',3,'Detailfoto, makkelijk echt te maken.'),
 (23,'M20 Partnerhavens','Bord bij een partnerhaven','TU','PLAAT',2,'"wij uw boot" in het bord. Bord als opmaak op een echte partnerhaven-foto.'),
 (24,'M21 Naast de botenmerken','Plaatje op de boot','TLB','DRUK',2,'Leeg ovaal. Plaatje echt opmaken en op een boot van een eigen merk monteren.'),
 (25,'M22 Aanleggen bij','Gids voor Klop-vaarders','TZ','DRUK',3,'Tijdschrift met getekende titel. Kaft echt opmaken, mockup erop.'),
 (26,'M23 Website, laptop','De site op een laptop','TF','SCHERM',1,'Toont een site die niet bestaat. Echte screenshot in de laptop.'),
 (27,'M23 Voorpagina','Screenshot voorpagina','','SCHERM',0,'Gedaan: vervangen door een echte screenshot van de huidige site (met je-vorm), gemaakt met tools/site_screens.js.'),
 (28,'M23b Bootpagina, laptop','Bootpagina','TF','SCHERM',1,'"Sloep 7.50" bestaat niet in het aanbod. Echte bootpagina tonen.'),
 (29,'M23b Bootpagina','Screenshot bootpagina','','SCHERM',0,'Gedaan: vervangen door een echte screenshot van de huidige site (met je-vorm), gemaakt met tools/site_screens.js.'),
 (30,'M23c Configurator, tablet','Configurator in de hand','TF','SCHERM',1,'Verzonnen interface. Echte configurator (algemeen of Maxima) tonen.'),
 (31,'M23c Configurator','Screenshot configurator','','SCHERM',0,'Gedaan: vervangen door een echte screenshot van de huidige site (met je-vorm), gemaakt met tools/site_screens.js.'),
 (32,'M23d Configurator, tablet','Service en overzicht','TF','SCHERM',2,'Verzonnen interface.'),
 (33,'M23d Configurator','Screenshot service-stap','','SCHERM',0,'Gedaan: vervangen door een echte screenshot van de huidige site (met je-vorm), gemaakt met tools/site_screens.js.'),
 (34,'M23e Servicepagina, monitor','Servicepagina','TF','SCHERM',2,'Verzonnen interface.'),
 (35,'M23e Servicepagina','Screenshot servicepagina','','SCHERM',0,'Gedaan: vervangen door een echte screenshot van de huidige site (met je-vorm), gemaakt met tools/site_screens.js.'),
 (36,'M26 Campagne, abri','Abri "Vaar je vrijheid"','TLGR','PLAAT',1,'Schreefletter, leeg ovaal, oranje label, te klein voor print. Plaat houden, opmaak opnieuw.'),
 (37,'M26 Campagne, plaat','Hal met sloep','R','OK',3,'Bruikbare plaat zonder tekst. Opschalen.'),
 (38,'M26 Campagne, plaat','Weg langs het water, trailer','R','OK',3,'Bruikbare plaat. Opschalen.'),
 (39,'M26b Campagne online','Advertenties op telefoon en tablet','TUF','SCHERM',1,'"Geregeld. U vaart." in het beeld. Advertenties echt opmaken en in een mockup zetten.'),
 (40,'M26c Campagne buiten','Billboard winterstalling','TULR','PLAAT',1,'Zie de proef hierboven: zelfde idee, met echte letter, logo, label en je-vorm.'),
 (41,'M26c Campagne, plaat','Sloep aan de steiger in mist','R','OK',3,'Beste sfeerplaat van de serie: precies wat het brandbook vraagt. Gebruikt voor de proef.'),
 (42,'M26c Campagne, plaat','Reiger in de ochtend','R','OK',3,'Mooi, geen boot. Goed als rustbeeld.'),
 (43,'M26d Campagne direct','Mail en app','TF','SCHERM',2,'Verzonnen schermen. Echte mail en melding opmaken.'),
 (44,'M26e Campagne video','Storyboard','ZE','FOTO',2,'Goed storyboard, maar voor video is een echte opname nodig.'),
 (45,'M26e Campagne, plaat','Stuur met geel label','R','OK',3,'Bruikbaar als plaat.'),
 (46,'M24 Offerte en afleverbrief','De offerte op tafel','TZ','DRUK',2,'Verzonnen offerte. Echte offerte-opmaak, dan mockup.'),
 (47,'M25 Seizoenspost','Kaart op de deurmat','TUNL','DRUK',1,'"Uw boot is winterklaar. Klopt. Pieter" en leeg ovaal. Kaart echt opmaken.'),
 (48,'M27 Bedrijfswagen','Auto met trailer','TF','PLAAT',2,'Amerikaanse pick-up. Echte (of Europese) bedrijfswagen, belettering als opmaak.'),
 (49,'M28 Mailhandtekening','Handtekening in een mail','NL','SCHERM',2,'"Daan Klop" en leeg ovaal. De echte HTML-handtekening tonen.'),
]
cnt = {k: sum(k in r[3] for r in R) for k in TAGS}
sp = {k: sum(r[4] == k for r in R) for k in SPOOR}
p1 = sum(r[5] == 1 for r in R)
def tag(t): return '<i class="bt bt-%s" title="%s">%s</i>' % (t, e(TAGS[t][1]), TAGS[t][0])
rows = ''.join('<tr data-s="%s" data-p="%d"><td><button class="th" data-set="beeld" data-i="%d"><img loading="lazy" src="{{PFX}}beeld/%02d.jpg" alt=""></button></td><td><b>%s</b><small>%s</small></td><td>%s</td><td><span class="sp sp-%s">%s</span></td><td class="pr">%s</td><td>%s</td></tr>' % (
    r[4], r[5], i, r[0], e(r[1]), e(r[2]), ''.join(tag(t) for t in r[3]), r[4], SPOOR[r[4]][0], {0:'Gedaan',1:'Nu',2:'Daarna',3:'Later'}[r[5]], e(r[6])) for i, r in enumerate(R))
themes = ''.join('<div class="bth"><b>%d</b><span>%s</span><p>%s</p></div>' % (cnt[k], TAGS[k][0], e(TAGS[k][1])) for k in sorted(TAGS, key=lambda k: -cnt[k]))
spoor = ''.join('<div class="bsp sp-%s"><b>%d</b><span>%s</span><p>%s</p></div>' % (k, sp[k], SPOOR[k][0], e(SPOOR[k][1])) for k in ['FOTO', 'SCHERM', 'DRUK', 'PLAAT', 'OK'])
STIJL = '''Documentary photograph, Dutch river landscape near Hardinxveld-Giessendam, the Netherlands.
Low light: early morning with soft mist, or blue hour after sunset. The sun itself is NOT in frame.
Calm, wide composition: one boat, lots of water and sky, generous empty space on the [left/right] third for text.
Colours: muted blue-grey water and sky, white hull, deep navy (#0B1930) details.
At most ONE yellow accent (#EFA91F): a cardboard tag, a work jacket or a mooring line.
Shot on a full-frame camera, 35mm lens, f/4, natural colours, fine grain, no HDR, no lens flare.
NO text, NO letters, NO numbers, NO logos, NO signs, NO screens with content, NO people unless specified.'''
SCENES = [
 ('M08 Het gele label (plaat)', 'Close-up of the stainless steering wheel of a white Dutch sloep moored at a wooden jetty, early morning mist. A blank matte yellow cardboard tag (#EFA91F) hangs from the wheel on a navy cord, the tag is empty. Shallow depth of field, river softly blurred behind.', 'Label met "Klaar om te varen." en "Klopt. [voornaam]" in Funnel, uit het label-component.'),
 ('M26 Campagne winter (plaat)', 'A white sloep with a navy cover, moored alone at a wooden jetty on a misty river at dawn, frost on the jetty planks, reeds on the far bank. Empty sky on the right half.', 'Billboard- en abri-opmaak: kop in Funnel Display 300, geel label, logo op witte plaat.'),
 ('M27 Bedrijfswagen (plaat)', 'A dark navy European pick-up truck towing a white sloep on a trailer along a Dutch dike road at dawn, river on the left, flat polder on the right, light ground mist. Plain unmarked vehicle doors.', 'Belettering van de wagen als vector op de deur, of de echte wagen fotograferen.'),
]
scenes = ''.join('<div class="bsc"><b>%s</b><pre>%s</pre><small>Opmaaklaag: %s</small></div>' % (e(a), e(b), e(c)) for a, b, c in SCENES)
out = '''<div class="bdive" id="beeld"><div class="sh" style="margin-top:clamp(56px,7vw,96px)"><div><span class="kick">Merkuitingen · beeld</span><h2 style="font-size:clamp(34px,4vw,56px)">Wat beter moet, en hoe</h2></div><p class="lead">Alle %d beelden van de merkuitingen naast het brandbook, het designsysteem en de site gelegd. Het idee per uiting is sterk; de uitvoering nog niet. Hieronder wat er mis is, wat we per beeld doen en hoe we het maken.</p></div>

<div class="cx"><h3>In één oogopslag</h3>
<div class="bsum"><div><b>%d</b><span>beelden beoordeeld</span></div><div><b>%d</b><span>moeten nu opnieuw</span></div><div><b>%d</b><span>al opgelost</span></div><div><b>%d</b><span>bruikbaar als sfeerplaat</span></div><div><b>%d</b><span>kunnen alleen echt (fotodag)</span></div></div>
<p class="lead" style="margin-top:20px">De kern: de generator heeft alles in één keer getekend, ook letters, logo en schermen. Juist die onderdelen moet je niet laten tekenen, want ze moeten exact kloppen met het merk. Daarom splitsen we: de foto is de plaat, alles met merk erop komt uit het designsysteem.</p></div>

<div class="cx"><h3>Wat er mis is</h3><p class="lead">Elk probleem met het aantal beelden waarin het voorkomt. Toetsing aan het brandbook (fotografie, het gele label, logo, typografie, tone of voice), het designsysteem en de site.</p><div class="bths">%s</div></div>

<div class="cx"><h3>Proef: zelfde idee, goed gemaakt</h3>
<div class="bdemo"><figure><button class="th" data-set="beeld" data-i="%d"><img src="{{PFX}}beeld/40.jpg" alt=""></button><figcaption><b>Nu</b> Schreefletter, "Geregeld. U vaart.", leeg blauw ovaal, oranje label, 1400 px.</figcaption></figure>
<figure><button class="th" data-set="beelddemo" data-i="0"><img src="{{PFX}}beeld/demo-billboard.jpg" alt=""></button><figcaption><b>Proef</b> Bestaande plaat zonder tekst (nr. 41), opmaak uit het designsysteem: Funnel Display, het gele label, "Jij vaart.", het echte logo op een witte plaat. Gemaakt met de opmaakpijplijn van deze repo, op elk formaat te renderen.</figcaption></figure></div></div>

<div class="cx"><h3>Canva-plaatjesmaker met goede scripts?</h3>
<div class="bcanva"><div><b>Alleen de plaatjesmaker: nee</b><p>Of het nu Canva, Gemini of een andere generator is: ze tekenen letters, logo's en schermen niet exact. Betere prompts lossen dat niet op. Je houdt dezelfde fouten, alleen mooier.</p></div>
<div><b>Canva als opmaaklaag: ja</b><p>Canva is sterk in het tweede deel: een merkset met Funnel, Oliegoed en het logo, sjablonen per formaat (billboard, abri, social, drukwerk), automatisch vullen en verkleinen, en het team kan zelf teksten aanpassen.</p></div>
<div><b>Ons advies: vier sporen</b><p>Echt wat echt moet (fotodag), echte schermen uit de site, drukwerk eerst echt opmaken, en AI alleen voor sfeerplaten zonder tekst. De opmaak komt uit het designsysteem: in code (zoals de proef) of in Canva-sjablonen.</p></div></div></div>

<div class="cx"><h3>De vier sporen</h3><div class="bsps">%s</div></div>

<div class="cx"><h3>Per beeld</h3>
<div class="bflt"><button data-bf="all" class="on">Alles</button><button data-bf="p1">Nu opnieuw</button><button data-bf="p0">Gedaan</button><button data-bf="FOTO">Fotodag</button><button data-bf="SCHERM">Echt scherm</button><button data-bf="DRUK">Drukwerk eerst</button><button data-bf="PLAAT">AI-plaat + opmaak</button><button data-bf="OK">Bruikbaar</button></div>
<div class="tblw"><table class="btab"><thead><tr><th></th><th>Uiting</th><th>Problemen</th><th>Spoor</th><th>Wanneer</th><th>Toelichting</th></tr></thead><tbody id="btb">%s</tbody></table></div></div>

<div class="cx"><h3>De scripts: zo sturen we de generator</h3><p class="lead">Eén vast stijlblok uit het brandbook, plus per uiting een korte scènebeschrijving. Nooit tekst of logo in de prompt; dat doet de opmaaklaag. Prompts staan als data in de repo, zodat elke plaat herhaalbaar is.</p>
<div class="bsc"><b>Stijlblok (voor elke plaat)</b><pre>%s</pre><small>Vertaald uit het brandbook: laag licht, rust (één boot, veel water en lucht), geel hooguit één keer, geen folderbeeld.</small></div>
<div class="bscs">%s</div></div>

<div class="cx"><h3>Controle voor oplevering</h3><ol class="rules">
<li><b>Geen gegenereerde tekst</b> in het beeld; alle tekst uit de opmaak in Funnel.</li>
<li><b>Je-vorm</b> in alle teksten, "Jij vaart." als payoff-regel.</li>
<li><b>Echt logo</b>, altijd op een witte plaat bij foto's.</li>
<li><b>Eén geel accent</b> per beeld, in Oliegoed #EFA91F.</li>
<li><b>Echte namen</b> van Vrijheidsvaarders, met toestemming.</li>
<li><b>Eén set feiten</b>: brandbook zegt 5.000 m² en 15 merken, de site 4.000 m² en 13 merken. Eerst vastzetten, daarna overal gelijk.</li>
<li><b>Laag licht, zon niet in beeld</b>, afwisseling tussen ochtendmist en blauw uur.</li>
<li><b>Printformaat</b>: plaat minstens 6.000 px of opgemaakt als vector.</li>
</ol></div>

<div class="cx"><h3>Zo pakken we het aan</h3><ol class="phase">
<li><small>Week 1</small><b>Schermen en drukwerk</b><p>Alle schermbeelden opnieuw uit de site (automatisch). Pas, label, kaart, offerte en bordjes echt opmaken.</p></li>
<li><small>Week 1–2</small><b>Platen en opmaak</b><p>Sfeerplaten opnieuw genereren met het stijlblok, opschalen. Campagne-opmaak als sjablonen in code en in Canva.</p></li>
<li><small>Week 2–3</small><b>Fotodag</b><p>Eén dag aan de Rivierdijk: gevel, showroom, balie, haven, stalling, werkplaats, oliegoed, overdracht. Shotlist uit deze tabel.</p></li>
<li class="io"><small>Nodig van Klop</small><b>Input</b><p>Toestemming van medewerkers, een ochtend in de haven, de echte bedrijfswagen, en welke boten uit de voorraad in beeld mogen.</p></li>
</ol><p class="note">De weken zijn een richting, geen planning; die maken we samen.</p></div>
</div>''' % (len(R), len(R), p1, sum(r[5]==0 for r in R), sp['OK'], cnt['E'], themes, [r[0] for r in R].index(40), spoor, rows, e(STIJL), scenes)
open(os.path.join(ROOT, 'tools/beeld_sectie.html'), 'w').write(out)
json.dump([{'f': '{{PFX}}beeld/%02d.jpg' % r[0], 't': r[1]} for r in R], open(os.path.join(ROOT, 'tools/beeld_data.json'), 'w'))
print('ok', len(R), cnt, sp, p1)
