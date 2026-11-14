#!/usr/bin/env python3
"""
Maakt van de ruwe Maxima-data (bron/*.json, uit scrape_maxima.py) de ingedeelde
data voor configurator 2.0 (public/data/*.json).

Wat het doet, per model:
- Verdeelt de ruwe stappen over vaste secties (Romp, Kuip & kussens, Buiskap, Motor, ...).
- Splitst de grote optielijsten in logische groepen (Deluxe pakket, Besturing, Audio, ...).
- Maakt van elkaar uitsluitende opties (Deluxe pakketten, tafels, displays) een "kies er één"-groep.
- Haalt de "ruitjes"-varianten van de kussensets eruit en maakt daar een aparte keuze "Stiksel" van.
- Schoont namen op ("Rompkleur donker blauw" -> "Donkerblauw") en zet toelichting tussen haakjes apart.
- Markeert opties waarbij een RAL-code nodig is.

Elke getoonde optie verwijst naar de originele Maxima-optie-id('s), zodat prijzen,
beeldlagen en offertes 1-op-1 aansluiten op de bron.

Gebruik:  python3 scripts/curate.py
Opties die geen regel raken komen in de groep "Overig" van hun sectie en worden gemeld.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "bron"
OUT = ROOT / "public" / "data"

# ---------------------------------------------------------------------------
# Secties: volgorde, titel en korte uitleg (je-vorm, kort en feitelijk).
# ---------------------------------------------------------------------------
SECTIONS = [
    ("romp", "Romp", "De kleur van de buitenkant en de waterlijn langs de zijkant."),
    ("kuip", "Kuip & kussens", "De binnenkant van de boot en de bekleding van de zitplaatsen."),
    ("kabelaring", "Kabelaring & stootrand", "De rand rondom de boot die hem beschermt bij het aanleggen."),
    ("buiskap", "Buiskap", "Beschutting tegen zon en regen."),
    ("motor", "Motor", "De aandrijving van je boot."),
    ("exterieur", "Exterieur", "Dek, besturing en uitrusting. Alles is optioneel."),
    ("interieur", "Interieur", "Extra kussens, een tafel en handige details."),
    ("elektronica", "Elektronica", "Navigatie, audio en stroom aan boord."),
    ("comfort", "Comfort", "Koelen, koken en meer comfort voor lange dagen op het water."),
]

# Ruwe staptitel -> (sectie, groepkey, groeptitel). Multi-stappen worden verder verdeeld via RULES.
STEP_MAP = {
    "Kies kleur buitenkant": ("romp", "rompkleur", "Rompkleur"),
    "Kies striping": ("romp", "waterlijn", "Waterlijn"),
    "Kies kleur binnenkant": ("kuip", "binnenkant", "Kleur binnenkant"),
    "Kies kussenset": ("kuip", "kussenset", "Kussenset"),
    "Kies kleur kabelaring-stootrand": ("kabelaring", "kabelaring", "Kabelaring of stootrand"),
    "Kies buiskap": ("buiskap", "buiskap", "Buiskap"),
    "Kies motor": ("motor", "motor", "Motor"),
    "Kies extra t.b.v. motorisering": ("motor", "motorisering", "Extra voor de motorisering"),
    "Kies exterieur opties": ("exterieur", None, None),
    "Kies interieur opties": ("interieur", None, None),
    "Kies interieur combinatie": ("interieur", None, None),
    "Kies electronics": ("elektronica", None, None),
    "Kies comfort": ("comfort", None, None),
    "Kies andere": ("exterieur", None, None),
}

# Groepen binnen de multi-stappen. Volgorde = weergavevolgorde in de sectie.
# (sectie, key, titel, type, hint, regex op de ruwe optienaam)
#   type "one"  = optioneel, kies er één (radio met "Geen")
#   type "many" = meerdere mogelijk
RULES = [
    ("buiskap", "kap-extra", "Extra bij de kap", "many", None,
     r"blindering|voorraam|biminitop|afdekhoes|achterzeil|achtertent|kuiphoes"),
    ("exterieur", "deluxe", "Deluxe pakket", "one", "Afwerking van vloer en zwemplateau.", r"^deluxe pakket"),
    ("exterieur", "voordek", "Voordek", "one", None, r"^voordek"),
    ("exterieur", "afwerking", "Romp & afwerking", "many", None,
     r"metallic|wrapped|motorkap spuiten|hardtop|carbon pakket|t-top"),
    ("exterieur", "besturing", "Manoeuvreren & besturing", "many", None,
     r"boegschroef|hekschroef|besturing|stuurbekrachtiging|trimtabs|zipwake"),
    ("exterieur", "dek", "Dek & uitrusting", "many", None,
     r"zwemtrap|hekdouche|eendenmat|zwemplat|antifouling|vaarklaar|anker|permateek op|permateek vloer|seadeck|zonnedek|maxima deur"),
    ("exterieur", "vlaggenmast", "Vlaggenmast", "one", None, r"^vlaggemast"),
    ("exterieur", "verlichting", "Verlichting", "many", None, r"^led |led verlichting|led dockinglights|led binnenverlichting|led lichtpakket"),
    ("exterieur", "brandstof", "Brandstof", "many", None, r"brandstoftank"),
    ("exterieur", "hoezen", "Hoezen", "many", None, r"overall cover"),
    ("exterieur", "beveiliging", "Beveiliging", "many", "SCM-gekeurd, vaak verplicht voor je verzekering.", r"^scm "),
    ("exterieur", "levering", "Levering", "many", None, r"^transport"),
    ("interieur", "bekleding", "Bekleding", "one", None, r"^bekleding"),
    ("interieur", "hout", "Houtafwerking", "one", None, r"^hpl "),
    ("interieur", "zitten", "Zitten & liggen", "many", "Kussens in dezelfde stof als je kussenset.",
     r"zonnebed|bunkussen|armsteun|verhoogd zitkussen|sierkussen|bestuurdersstoel"),
    ("interieur", "tafel", "Tafel", "one", None,
     r"^tafel |^tafeltje|cockpit tafel|kuiptafel|el\.tafel|^tafelset"),
    ("interieur", "handig", "Handig", "many", None,
     r"prullenbak|handgreep|opbergbox|gordijn|houten vloer|kussen op tafel"),
    ("elektronica", "display", "Display & navigatie", "one", None,
     r"^glass in cockpit|^maxima display|gps diepte"),
    ("elektronica", "navigatie-extra", "Extra navigatie", "many", None,
     r"2de scherm|radardome|vhf|stuurautomaat"),
    ("elektronica", "audio", "Audio", "many", None, r"radio|audio"),
    ("elektronica", "stroom", "Stroom", "many", None, r"accu|walstroom|omvormer|victron|generator"),
    ("comfort", "koeling", "Koeling", "one", None, r"^koel"),
    ("comfort", "keuken", "Keuken & sanitair", "many", None, r"keuken|toilet|wasbak|kookplaat|bbq"),
    ("comfort", "klimaat", "Klimaat & entertainment", "many", None, r"airc|verwarming|tv |schuifdak"),
]
RULES = [(s, k, t, ty, h, re.compile(rx, re.I)) for s, k, t, ty, h, rx in RULES]

# Opties die alleen samen met een buiskap zin hebben; zonder buiskap-stap gaan ze naar Exterieur.
NEEDS_HOOD = {"kap-extra"}


# ---------------------------------------------------------------------------
# Namen opschonen
# ---------------------------------------------------------------------------
COLOR_FIX = {
    "donker blauw": "Donkerblauw", "donker grijs": "Donkergrijs", "lichtgrijs": "Lichtgrijs",
    "wit": "Wit", "zwart": "Zwart", "grijs": "Grijs", "zilvergrijs": "Zilvergrijs", "oranje": "Oranje",
}


def cap(s):
    return s[:1].upper() + s[1:] if s else s


def split_sub(name):
    """'Vaarklaarpakket ( 4 lijnen, ...)' -> ('Vaarklaarpakket', '4 lijnen, ...')"""
    m = re.match(r"^(.*?)\s*\((.+)\)\s*$", name)
    if not m:
        return name, None
    main, sub = m.group(1).strip(), m.group(2).strip()
    if re.fullmatch(r"dezelfde stof als het kussenset", sub, re.I):
        return main, None  # staat al als hint bij de groep
    sub = re.sub(r"\s*/\s*", ", ", sub)
    sub = re.sub(r"\s*,\s*", ", ", sub)
    sub = re.sub(r"(\d)\s*x\s*(\d)", r"\1 × \2", sub)
    sub = re.sub(r"(\d)\s*w\b", r"\1 W", sub, flags=re.I)
    sub = sub.replace("depth", "diepte").replace("+lijn", "+ lijn")
    return main, cap(sub)


def clean_name(group, raw):
    n = re.sub(r"\s+", " ", raw).strip()
    sub = None
    low = n.lower()

    if group == "rompkleur":
        n = re.sub(r"^rompkleur\s+", "", n, flags=re.I)
    elif group == "binnenkant":
        n = re.sub(r"^binnenkant\s+", "", n, flags=re.I)
    elif group == "waterlijn":
        n = re.sub(r"^waterlijn\s+", "", n, flags=re.I) if not low.startswith("geen") else n
    elif group == "buiskap":
        n = re.sub(r"^buiskap\s+", "", n, flags=re.I) if not low.startswith("geen") else n
        n = re.sub(r"\bfamily\b", "family", n)
    elif group == "kabelaring":
        n = re.sub(r"^(kabelaring|stootrand)\s+", "", n, flags=re.I)
    elif group == "motor":
        m = re.match(r"^(\d+)\s+Honda\s+(.*)$", n)
        if m:
            rest = m.group(2)
            if re.search(r"elektronische motorbediening", rest, re.I):
                n, sub = f"Honda {m.group(1)} pk", "Met elektronische motorbediening"
            else:
                n = f"Honda {m.group(1)} pk {rest}".strip()
        m = re.match(r"^(\d+)\s*pk\s+Yanmar$", n, re.I)
        if m:
            n = f"Yanmar {m.group(1)} pk"
        m = re.match(r"^(\d+)\s*pk\s+vetus\s+(.*)$", n, re.I)
        if m:
            n, sub = f"Vetus {m.group(1)} pk", cap(m.group(2).replace("  ", " ").strip())
        m = re.match(r"^Electric\s+(\d+)KW\s+(.*?)\s*package$", n, re.I)
        if m:
            spec = re.sub(r"\s+", " ", m.group(2)).replace("met accu", "accu").replace("long run", "long range")
            n, sub = f"Elektrisch {m.group(1)} kW", cap(spec.strip())
        n = re.sub(r"el\.motorbediening", "elektronische motorbediening", n)
        n = re.sub(r"\s+met elektronische motorbediening$", "", n) if sub is None and "XDU" in n else n
        if "drive by wire" in n:
            n = n.replace(" drive by wire", "")
            sub = "Drive-by-wire"

    if group in ("rompkleur", "binnenkant", "waterlijn"):
        key = n.lower().strip()
        n = COLOR_FIX.get(key, n)
        if re.search(r"in ral kleur", n, re.I):
            n = "RAL-kleur naar keuze"

    if sub is None:
        n, sub = split_sub(n)

    # Losse correcties
    fixes = [
        (r"^RVS Zwemtrap$", "RVS zwemtrap"),
        (r"^Vlaggemast (klein|groot) model$", r"\1 model"),
        (r"^Glass in cockpit Garmin (\d+) touch met (.*)$", r'Glass cockpit Garmin \1" touch|Met \2'),
        (r"^Glass in cockpit (\d+) touch$", r'Glass cockpit \1" touch'),
        (r"^Maxima display ([\dx]+) inch$", r'Maxima display \1"'),
        (r"^Garmin (\d+)inch", r'Garmin \1"'),
        (r"^2de accu", "Tweede accu"),
        (r"^Deluxe pakket met ", "Met "),
        (r"^Voordek ", ""),
        (r"^Aircondtioning", "Airconditioning"),
        (r"^Electrische ankerlier", "Elektrische ankerlier"),
        (r"^Keukentje$", "Keukentje|Wasbak en kookplaatje"),
        (r"^Radio Fusion BT met 2 x 120 watt LED speakers$", "Radio Fusion BT|Met 2 × 120 W led-speakers"),
        (r"^Audio uitbreiding op Garmin met 4 x 120 w LED speakers$", "Audio-uitbreiding op Garmin|4 × 120 W led-speakers"),
        (r"^Audio uitbreiding op Garmin met 4 x 160w LED speakers en versterker$", "Audio-uitbreiding op Garmin plus versterker|4 × 160 W led-speakers en versterker"),
        (r"^Walstroomaansluiting met rvs inlet en walstroomkabel 15m$", "Walstroomaansluiting|Met rvs inlet en 15 m walstroomkabel"),
        (r"^Boegschroef Vetus (\d+)\s*kgf$", r"Boegschroef Vetus \1 kgf"),
        (r"^Tafel ovaal met Permateek met uitneembare poot$", "Tafel ovaal met permateek|Met uitneembare poot"),
        (r"^Tafel ovaal met (.*) en uitneembare poot$", r"Tafel ovaal met \1|Met uitneembare poot"),
        (r"^Tafel ovaal met uitneembare poot$", "Tafel ovaal|Met uitneembare poot"),
        (r"^Permateek cockpit tafel groot$", "Cockpittafel groot met permateek"),
        (r"^Stuurbekrachtiging \(\+ 200 pk\)", "Stuurbekrachtiging|Vanaf 200 pk"),
        (r"^Brandstoftank inbouw (\d+) liter \+ tankmeter", r"Inbouwtank \1 liter|Met tankmeter"),
    ]
    n = re.sub(r"^Tafeltje ovaal", "Tafel ovaal", n)
    for rx, rep in fixes:
        if re.search(rx, n, re.I):
            n = re.sub(rx, rep, n, flags=re.I)
            if "|" in n:
                n, extra = n.split("|", 1)
                sub = cap(extra.strip())
            break
    if group == "voordek":
        n = cap(n)
    return cap(n.strip()), sub


def is_ral(raw):
    return bool(re.search(r"\bral\b", raw, re.I))


# ---------------------------------------------------------------------------
def curate(raw):
    groups = {}  # key -> group dict
    order = []
    unmatched = []

    def group(section, key, title, gtype, required, hint=None):
        if key not in groups:
            groups[key] = {"section": section, "key": key, "title": title, "type": gtype,
                           "required": required, "hint": hint, "options": []}
            order.append(key)
        return groups[key]

    def opt(o, gkey):
        name, sub = clean_name(gkey, o["name"])
        out = {"id": o["id"], "name": name, "raw": o["name"].strip(), "price": o["price"]}
        if sub:
            out["sub"] = sub
        if o.get("image"):
            out["image"] = o["image"]
        if o.get("layer") and o.get("layerId") and o["layer"] in raw["layers"]:
            out["layer"], out["layerId"] = o["layer"], o["layerId"]
        if is_ral(o["name"]):
            out["ral"] = True
        return out

    has_hood = any(s["title"] == "Kies buiskap" for s in raw["steps"])

    for step in raw["steps"]:
        section, gkey, gtitle = STEP_MAP.get(step["title"], ("exterieur", None, None))
        if gkey:  # vaste enkele keuze
            g = group(section, gkey, gtitle, "single", not step["optional"])
            for o in step["options"]:
                g["options"].append(opt(o, gkey))
            continue
        for o in step["options"]:
            rule = next((r for r in RULES if r[5].search(o["name"])), None)
            if rule is None:
                unmatched.append(f"{step['title']}: {o['name']}")
                g = group(section, f"overig-{section}", "Overig", "many", False)
            else:
                rsec, rkey, rtitle, rtype, rhint, _ = rule
                if rkey in NEEDS_HOOD and not has_hood:
                    rsec, rkey, rtitle = "exterieur", "kap-extra-ext", "Kap & zonwering"
                g = group(rsec, rkey, rtitle, rtype, False, rhint)
            g["options"].append(opt(o, g["key"]))

    # Stiksel: "X ruitjes" wordt een variant van kussenset "X".
    if "kussenset" in groups:
        cushions = groups["kussenset"]["options"]
        by_name = {c["raw"].lower(): c for c in cushions}
        twins = {}
        for c in cushions:
            m = re.match(r"^(.*)\s+ruitjes$", c["raw"], re.I)
            if m and m.group(1).strip().lower() in by_name:
                base = by_name[m.group(1).strip().lower()]
                twins[base["id"]] = c
        if twins:
            twin_ids = {t["id"] for t in twins.values()}
            kept = []
            for c in cushions:
                if c["id"] in twin_ids:
                    continue
                if c["id"] in twins:
                    c["stitch"] = {"id": twins[c["id"]]["id"], "price": twins[c["id"]]["price"]}
                    if twins[c["id"]].get("layerId"):
                        c["stitch"]["layerId"] = twins[c["id"]]["layerId"]
                kept.append(c)
            groups["kussenset"]["options"] = kept
            deltas = sorted({round(b["stitch"]["price"] - b["price"], 2) for b in kept if "stitch" in b})
            g = group("kuip", "stiksel", "Stiksel kussenset", "stitch", True)
            g["options"] = [
                {"id": "glad", "name": "Glad", "price": 0},
                {"id": "ruitjes", "name": "Ruitjesstiksel", "sub": "Doorgestikt ruitpatroon op zitting en rugleuning.",
                 "price": deltas[0] if len(deltas) == 1 else None, "priceFrom": deltas[0] if len(deltas) > 1 else None},
            ]

    # Groep "Vlaggenmast" en "Overig" achteraan in de sectie; secties zonder groepen vallen weg.
    sections = []
    for skey, stitle, intro in SECTIONS:
        gs = [groups[k] for k in order if groups[k]["section"] == skey]
        # RULES-volgorde aanhouden voor multi-groepen, vaste groepen eerst
        rule_rank = {r[1]: i for i, r in enumerate(RULES)}
        fixed_rank = {k: i for i, k in enumerate(["rompkleur", "waterlijn", "binnenkant", "kussenset", "stiksel",
                                                  "kabelaring", "buiskap", "motor", "motorisering"])}
        gs.sort(key=lambda g: (0, fixed_rank[g["key"]]) if g["key"] in fixed_rank
                else (2, 0) if g["key"].startswith("overig") else (1, rule_rank.get(g["key"].replace("-ext", ""), 99)))
        if gs:
            sections.append({"key": skey, "title": stitle, "intro": intro, "groups": gs})

    for g in groups.values():
        del g["section"]
        if not g["hint"]:
            del g["hint"]

    # Titel kabelaring/stootrand afhankelijk van wat het model heeft
    for s in sections:
        if s["key"] == "kabelaring":
            names = " ".join(o["raw"].lower() for g in s["groups"] for o in g["options"])
            label = "Stootrand" if "stootrand" in names and "kabelaring" not in names else "Kabelaring"
            s["title"] = label
            s["groups"][0]["title"] = f"Kleur {label.lower()}"

    out = {k: raw[k] for k in ("id", "slug", "name", "image", "specs", "basePrice", "fixedCosts",
                               "imageBase", "views", "layers", "defaultView")}
    out["sections"] = sections
    return out, unmatched


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    index, all_unmatched = [], []
    for f in sorted(SRC.glob("maxima-*.json")):
        raw = json.loads(f.read_text())
        data, unmatched = curate(raw)
        all_unmatched += [f"{raw['name']}: {u}" for u in unmatched]
        (OUT / f.name).write_text(json.dumps(data, ensure_ascii=False, indent=1))
        index.append({k: data[k] for k in ("id", "slug", "name", "image", "specs", "basePrice")})
        n_opts = sum(len(g["options"]) for s in data["sections"] for g in s["groups"])
        print(f"{raw['name']:<36} {len(data['sections'])} stappen, "
              f"{sum(len(s['groups']) for s in data['sections'])} groepen, {n_opts} opties", file=sys.stderr)
    (OUT / "models.json").write_text(json.dumps(index, ensure_ascii=False, indent=1))
    if all_unmatched:
        print("\nNiet ingedeeld (staan onder 'Overig'):", file=sys.stderr)
        for u in all_unmatched:
            print("  " + u, file=sys.stderr)


if __name__ == "__main__":
    main()
