"""
Backfills missing gmaps_url for leads that were scraped before we
captured place URLs. Generates a Google Maps search URL using the
lead's name + region — when the user clicks, Google takes them to
the matching place automatically.
"""
import csv
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).parent
MASTER_CSV = ROOT / "output" / "leads.csv"


def make_search_url(name: str, region: str) -> str:
    query = f"{name} {region} Greece".strip()
    return ("https://www.google.com/maps/search/"
            + urllib.parse.quote(query) + "/?hl=en")


def main():
    with open(MASTER_CSV, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    filled = 0
    for r in rows:
        if r.get("gmaps_url"):
            continue
        name = r.get("name", "")
        region = r.get("region", "")
        if not name:
            continue
        r["gmaps_url"] = make_search_url(name, region)
        filled += 1

    with open(MASTER_CSV, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)

    print(f"Backfilled {filled} leads with search-based URLs")
    print(f"Total leads: {len(rows)}")
    print(f"  -> {MASTER_CSV}")


if __name__ == "__main__":
    main()
