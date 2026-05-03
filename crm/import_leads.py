"""
One-time import: pulls leads from the local lead-finder CSV into the CRM DB.
Groups multiple listings sharing the same phone into one lead with N properties.
Run with: python import_leads.py
"""
import csv
import json
import re
import sys
from pathlib import Path

import db
from countries import country_for_region

CSV_PATH = Path(__file__).parent.parent / "lead-finder" / "output" / "leads.csv"


def normalize_phone(p: str) -> str:
    return re.sub(r"[^\d+]", "", p or "")


def main():
    if not CSV_PATH.exists():
        print(f"ERROR: {CSV_PATH} not found")
        sys.exit(1)

    db.init_schema()

    with open(CSV_PATH, encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    # Group rows by phone
    by_phone = {}
    skipped = 0
    for r in rows:
        phone = normalize_phone(r.get("phone", ""))
        if not phone:
            skipped += 1
            continue
        by_phone.setdefault(phone, []).append(r)

    inserted = 0
    updated = 0
    multi_owner = 0
    for phone, group in by_phone.items():
        properties = [{
            "region": r.get("region", ""),
            "name": r.get("name", ""),
            "category": r.get("category", ""),
            "gmaps_url": r.get("gmaps_url", ""),
        } for r in group]
        if len(group) > 1:
            multi_owner += 1
        # Primary = listing with longest name
        primary = max(group, key=lambda r: len(r.get("name", "")))
        primary_region = primary.get("region", "")
        # CSV may already have a country column (newer lead-finder); if not,
        # derive from region.
        primary_country = (primary.get("country", "")
                            or country_for_region(primary_region))

        existing = db.query_one(
            "SELECT phone FROM leads WHERE phone = ?", (phone,))
        if existing:
            db.execute("""
                UPDATE leads SET country = ?, region = ?, name = ?,
                    category = ?, email = ?, gmaps_url = ?,
                    online_presence = ?, domain_gr_available = ?,
                    domain_com_available = ?, domain_suggestion = ?,
                    enriched_at = ?, properties = ?
                WHERE phone = ?
            """, (
                primary_country, primary_region, primary.get("name", ""),
                primary.get("category", ""), primary.get("email", ""),
                primary.get("gmaps_url", ""), primary.get("online_presence", ""),
                primary.get("domain_gr_available", ""),
                primary.get("domain_com_available", ""),
                primary.get("domain_suggestion", ""),
                primary.get("enriched_at", ""),
                json.dumps(properties, ensure_ascii=False), phone,
            ))
            updated += 1
        else:
            db.execute("""
                INSERT INTO leads (phone, country, region, name, category,
                    email, gmaps_url, online_presence, domain_gr_available,
                    domain_com_available, domain_suggestion, enriched_at,
                    properties)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                phone, primary_country, primary_region,
                primary.get("name", ""),
                primary.get("category", ""), primary.get("email", ""),
                primary.get("gmaps_url", ""), primary.get("online_presence", ""),
                primary.get("domain_gr_available", ""),
                primary.get("domain_com_available", ""),
                primary.get("domain_suggestion", ""),
                primary.get("enriched_at", ""),
                json.dumps(properties, ensure_ascii=False),
            ))
            db.execute(
                "INSERT INTO lead_state (lead_phone, status) VALUES (?, 'new')",
                (phone,))
            inserted += 1

    print(f"Imported from {CSV_PATH}")
    print(f"  CSV rows:                {len(rows)}")
    print(f"  unique owners (phones):  {len(by_phone)}")
    print(f"  multi-property owners:   {multi_owner}")
    print(f"  inserted: {inserted}, updated: {updated}, skipped: {skipped}")


if __name__ == "__main__":
    main()
