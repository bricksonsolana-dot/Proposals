"""
Apply current validation rules retroactively to leads.csv. Drops rows that
don't pass and writes them to removed_leads.csv with the rejection reason
so they can be reviewed before being purged for good.

Rules applied (string-only — no network):
    - Hotel chain blacklist by name (NH, Hilton, Marriott, ...).

Not applied retroactively (would require re-scrape — addresses were never
stored in the CSV, so we can't tell whether a foreign-prefix phone belongs
to a legit foreign owner of a local property or to a cross-card data leak):
    - Address country mismatch.
    - Phone country mismatch (causes high false-positive rate without
      address as corroborating signal — many vacation rentals legitimately
      list a +44/+33/+49 owner phone).
    - Wrong gmaps_url: handled separately by `backfill_urls.py --replace`.

Usage:
    python cleanup_leads.py                      # show what would be removed
    python cleanup_leads.py --apply              # actually rewrite leads.csv
    python cleanup_leads.py --apply --country Netherlands   # scope to NL
"""
import argparse
import csv
from pathlib import Path

from gmaps_scraper import is_chain_hotel


ROOT = Path(__file__).parent
MASTER_CSV = ROOT / "output" / "leads.csv"
REMOVED_CSV = ROOT / "output" / "removed_leads.csv"


def reject_reason(row: dict) -> str:
    """Returns rejection reason string, or '' if the row is OK."""
    name = row.get("name", "")
    if is_chain_hotel(name):
        return "chain_hotel"
    return ""


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--apply", action="store_true",
                   help="actually rewrite leads.csv (default: dry-run)")
    p.add_argument("--country", help="limit to this country (case-insensitive)")
    args = p.parse_args()

    with open(MASTER_CSV, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    kept = []
    removed = []
    for r in rows:
        if args.country and r.get("country", "").lower() != args.country.lower():
            kept.append(r)
            continue
        reason = reject_reason(r)
        if reason:
            r2 = dict(r)
            r2["_reason"] = reason
            removed.append(r2)
        else:
            kept.append(r)

    print(f"Total leads: {len(rows)}")
    print(f"  kept:    {len(kept)}")
    print(f"  removed: {len(removed)}")
    if removed:
        # Group by reason for visibility
        from collections import Counter
        by_reason = Counter(r["_reason"].split(" ")[0] for r in removed)
        for reason, count in by_reason.most_common():
            print(f"    {reason}: {count}")

    if not args.apply:
        print("\n[dry-run] re-run with --apply to rewrite leads.csv.")
        if removed:
            preview = removed[:10]
            print(f"\nFirst {len(preview)} rows that would be removed:")
            for r in preview:
                print(f"  [{r['_reason']}] {r.get('country','')}/"
                      f"{r.get('region','')}: {r.get('name','')} "
                      f"({r.get('phone','')})")
        return

    # Write removed file (append-friendly: replace each run, since we always
    # operate on the current leads.csv)
    REMOVED_CSV.parent.mkdir(exist_ok=True)
    with open(REMOVED_CSV, "w", newline="", encoding="utf-8-sig") as f:
        out_fields = list(fieldnames) + ["_reason"]
        w = csv.DictWriter(f, fieldnames=out_fields, extrasaction="ignore")
        w.writeheader()
        for r in removed:
            w.writerow(r)
    print(f"  -> wrote {REMOVED_CSV}")

    with open(MASTER_CSV, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for r in kept:
            w.writerow(r)
    print(f"  -> wrote {MASTER_CSV} ({len(kept)} leads)")


if __name__ == "__main__":
    main()
