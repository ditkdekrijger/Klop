#!/usr/bin/env python3
"""
Haalt de configuratordata van alle Maxima-modellen op van maximaboats.nl
(dealer-hash van Klop Watersport) en schrijft de ruwe data naar bron/.
Daarna: python3 scripts/curate.py  (maakt de ingedeelde data in public/data/).

Gebruik:  python3 scripts/scrape_maxima.py
Alleen stdlib; draai opnieuw wanneer Maxima prijzen of opties wijzigt.
"""
import html, json, re, sys, time, urllib.request
from bs4 import BeautifulSoup  # pip install beautifulsoup4
from pathlib import Path

BASE = "https://www.maximaboats.nl/"
HASH = "edd9dcdb1a193e689569d0de6e024d76e18c9684"  # dealer-hash Klop Watersport
OUT = Path(__file__).resolve().parent.parent / "bron"  # ruwe data; scripts/curate.py maakt daar public/data van
UA = {"User-Agent": "Mozilla/5.0 (KlopConfiguratorSync)"}


def get(url, attempts=6):
    """Haalt een pagina op; probeert opnieuw bij netwerkfouten en bij de
    bot-check-pagina ("One moment, please...") die maximaboats.nl soms toont."""
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                body = r.read().decode("utf-8", "replace")
            if "<title>One moment" not in body:
                return body
        except Exception:
            if attempt == attempts - 1:
                raise
        time.sleep(3 * (attempt + 1))
    raise RuntimeError(f"Geen bruikbare respons van {url}")


def text(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def abs_url(u):
    if not u:
        return None
    return u if u.startswith("http") else BASE + u.lstrip("/")


def num(s):
    s = re.sub(r"[^\d,.-]", "", s or "")
    return float(s.replace(".", "").replace(",", ".")) if s else 0.0


def parse_overview(doc):
    soup = BeautifulSoup(doc, "html.parser")
    out, seen = [], set()
    for card in soup.select(".separateConfigurator__products__product"):
        a = card.find("a", href=re.compile(r"configurator/\?p=\d+"))
        h2 = card.find("h2")
        if not a or not h2:
            continue
        pid = int(re.search(r"p=(\d+)", a["href"]).group(1))
        if pid in seen:
            continue
        seen.add(pid)
        specs = {}
        for row in card.select(".separateConfigurator__products__product__text > span.row"):
            k, v = row.select_one(".bold"), row.select("span.col6")
            if k and v:
                specs[text(str(k))] = text(str(v[-1]))
        img = card.select_one(".separateConfigurator__products__product__image img")
        out.append({"id": pid, "name": h2.get_text(strip=True),
                    "image": abs_url(img["src"]) if img else None, "specs": specs})
    return out


def parse_model(doc):
    soup = BeautifulSoup(doc, "html.parser")
    form = soup.select_one("form.configurator__form")
    base_dir = form.get("data-base-directory", "") if form else ""
    total = soup.select_one(".totalPrice[data-base-price]")

    views = list(dict.fromkeys(v["data-view"] for v in soup.select(".configurator__summary__views__view[data-view]")))
    layers = []
    for part in soup.select(".configurator__summary__boat .part"):
        name = next((c[5:] for c in part["class"] if c.startswith("part-")), None)
        if name and name != "full":
            layers.append(name)

    base_price, fixed = 0.0, []
    items = soup.select_one(".configurator__summary__data__items")
    if items:
        for row in items.find_all(class_="configurator__summary__data__row", recursive=False):
            spans = row.find_all(["span", "strong"], recursive=False)
            if len(spans) < 2:
                continue
            label, val = spans[0].get_text(strip=True).rstrip(":").strip(), num(spans[1].get_text())
            if "basePrice" in row.get("class", []):
                base_price = val
            else:
                fixed.append({"label": label, "price": val})

    steps = []
    for st in soup.select(".configurator__steps .step"):
        if st.select_one(".configurator__personal"):
            continue
        title_el = st.select_one(".step__title__text__top") or st.select_one(".step__title")
        title = title_el.get_text(" ", strip=True) if title_el else ""
        options, kind = [], "single"
        for opt in st.select(".options .option"):
            inp = opt.find("input")
            if not inp:
                continue
            if inp.get("type") == "checkbox":
                kind = "multi"
            img = opt.select_one("img.option__text__row__image")
            desc = opt.select_one(".option__description, .description")
            options.append({
                "id": int(opt["data-id"].replace("option_", "")),
                "name": (opt.get("data-name") or opt.select_one(".name").get_text()).strip(),
                "price": num(opt.get("data-price")),
                "image": abs_url(img["src"]) if img and img.get("src") else None,
                "layer": (inp.get("data-option") or "").replace(" ", "-") or None,
                "layerId": inp.get("data-option-id") or None,
                "description": desc.get_text(" ", strip=True) if desc else None,
            })
        sel = st.select_one(".options select")
        if sel:
            for o in sel.find_all("option"):
                if not o.get("value"):
                    continue
                options.append({"id": int(o["value"]) if o["value"].isdigit() else o["value"],
                                "name": o.get_text(strip=True), "price": num(o.get("price")),
                                "image": None, "layer": (sel.get("data-option") or "").replace(" ", "-") or None,
                                "layerId": o["value"], "description": None})
        if options:
            steps.append({"title": title, "type": kind,
                          "optional": bool(st.select_one(".step__optionalLabel")), "options": options})

    return {
        "imageBase": abs_url(base_dir),
        "defaultView": (form.get("data-view") if form else None) or (views[0] if views else None),
        "views": views,
        "layers": layers,
        "basePrice": base_price or (float(total["data-base-price"]) if total else 0.0),
        "fixedCosts": fixed,
        "steps": steps,
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    overview = []
    for attempt in range(5):  # de server geeft af en toe een lege lijst terug
        overview = parse_overview(get(f"{BASE}configurator/?hash={HASH}&embed=1&lang=nl"))
        if overview:
            break
        time.sleep(3)
    if not overview:
        sys.exit("Geen modellen gevonden op maximaboats.nl; data niet overschreven.")
    print(f"{len(overview)} modellen gevonden", file=sys.stderr)
    index = []
    for m in overview:
        doc = get(f"{BASE}configurator/?p={m['id']}&hash={HASH}&embed=1&lang=nl")
        data = {**m, **parse_model(doc)}
        if not data["steps"]:
            sys.exit(f"Geen stappen gevonden voor {m['name']}; afgebroken zodat bestaande data intact blijft.")
        slug = re.sub(r"[^a-z0-9]+", "-", m["name"].lower()).strip("-")
        data["slug"] = slug
        (OUT / f"{slug}.json").write_text(json.dumps(data, ensure_ascii=False, indent=1))
        index.append({k: data[k] for k in ("id", "slug", "name", "image", "specs", "basePrice")})
        print(f"  {m['name']}: {len(data['steps'])} stappen, "
              f"{sum(len(s['options']) for s in data['steps'])} opties, lagen={data['layers']}", file=sys.stderr)
        time.sleep(0.5)
    (OUT / "models.json").write_text(json.dumps(index, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
