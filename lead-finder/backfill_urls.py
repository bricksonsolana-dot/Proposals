"""
Backfills gmaps_url for leads. Generates a Google Maps search URL using the
lead's name + region — when the user clicks, Google takes them to the
matching place automatically.

Default behavior fills only missing URLs. Use --replace to overwrite existing
URLs (needed when an earlier scraper run captured wrong URLs due to virtual-
scroll DOM recycling). Scope the replacement with --country and/or --region.

Usage:
    python backfill_urls.py                          # fill empty only
    python backfill_urls.py --replace                # overwrite all
    python backfill_urls.py --replace --country Netherlands
    python backfill_urls.py --replace --region Amsterdam
"""
import argparse
import csv
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).parent
MASTER_CSV = ROOT / "output" / "leads.csv"


def make_search_url(name: str, region: str, country: str = "") -> str:
    query = f"{name} {region} {country}".strip()
    return ("https://www.google.com/maps/search/"
            + urllib.parse.quote(query) + "/?hl=en")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--replace", action="store_true",
                   help="overwrite existing URLs (not just empty ones)")
    p.add_argument("--country", help="limit to this country (case-insensitive)")
    p.add_argument("--region", help="limit to this region (case-insensitive)")
    args = p.parse_args()

    with open(MASTER_CSV, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    filled = 0
    replaced = 0
    for r in rows:
        name = r.get("name", "")
        region = r.get("region", "")
        country = r.get("country", "")
        if not name:
            continue
        if args.country and country.lower() != args.country.lower():
            continue
        if args.region and region.lower() != args.region.lower():
            continue
        had_url = bool(r.get("gmaps_url"))
        if had_url and not args.replace:
            continue
        r["gmaps_url"] = make_search_url(name, region, country)
        if had_url:
            replaced += 1
        else:
            filled += 1

    with open(MASTER_CSV, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)

    print(f"Filled (was empty): {filled}")
    print(f"Replaced (had url): {replaced}")
    print(f"Total leads: {len(rows)}")
    print(f"  -> {MASTER_CSV}")


if __name__ == "__main__":
    main()
