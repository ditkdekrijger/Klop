#!/usr/bin/env python3
"""
Kopieert alle beelden die de configurator gebruikt van maximaboats.nl naar public/media/,
zodat de configurator niet meer van hun server afhangt.

Doe dit pas als Maxima akkoord is met het zelf hosten van hun beelden.
Zet daarna in public/index.html: window.MX_CONFIG.mediaBase = 'media/'.

Gebruik:
  python3 maxima-configurator/scripts/mirror_media.py --dry-run   # alleen tellen
  python3 maxima-configurator/scripts/mirror_media.py             # downloaden (slaat bestaande over)
"""
import json
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "public" / "data"
OUT = ROOT / "public" / "media"
HOST = "https://www.maximaboats.nl/"
UA = {"User-Agent": "Mozilla/5.0 (KlopConfiguratorSync)"}


def urls():
    found = set()
    for f in sorted(DATA.glob("maxima-*.json")):
        m = json.loads(f.read_text())
        if m.get("image"):
            found.add(m["image"])
        base = m.get("imageBase") or ""
        for s in m["sections"]:
            for g in s["groups"]:
                for o in g["options"]:
                    if o.get("image"):
                        found.add(o["image"])
                    ids = [o.get("layerId")] + ([o["stitch"].get("layerId")] if o.get("stitch") else [])
                    for v in m.get("views", []):
                        if o.get("layer"):
                            for i in filter(None, ids):
                                found.add(f"{base}{v}/{o['layer']}/{i}.png")
        for v in m.get("views", []):
            if base:
                found.add(f"{base}{v}/full.png")
    return sorted(u for u in found if u.startswith(HOST))


def main():
    dry = "--dry-run" in sys.argv
    todo = urls()
    print(f"{len(todo)} beelden in de data", file=sys.stderr)
    if dry:
        return
    done = skipped = failed = 0
    for i, u in enumerate(todo, 1):
        dest = OUT / u[len(HOST):]
        if dest.exists() and dest.stat().st_size > 0:
            skipped += 1
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        try:
            with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30) as r:
                if not r.headers.get("Content-Type", "").startswith("image/"):
                    raise ValueError("geen afbeelding")
                dest.write_bytes(r.read())
            done += 1
        except Exception as e:  # noqa: BLE001
            failed += 1
            print(f"  mislukt: {u} ({e})", file=sys.stderr)
        if i % 100 == 0:
            print(f"  {i}/{len(todo)}", file=sys.stderr)
        time.sleep(0.1)
    size = sum(p.stat().st_size for p in OUT.rglob("*") if p.is_file()) / 1e6
    print(f"klaar: {done} nieuw, {skipped} al aanwezig, {failed} mislukt; public/media/ is {size:.0f} MB", file=sys.stderr)


if __name__ == "__main__":
    main()
