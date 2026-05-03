"""
Tier-3 validation pass: re-visits each lead's gmaps_url and drops those
that are clearly wrong. Two failure modes:

    1. URL points to a different place. The h1 on the page doesn't match
       the lead's saved name -> URL is wrong. Drop the lead.

    2. The place actually has a website. Includes the auto-attached
       "Official site" / "Visit hotel website" links Google adds for
       hotels in hotel-listing mode that the old scraper missed.
       OTA-only links (booking.com, airbnb, facebook) are NOT counted
       as a real website -- those leads stay.

Removed leads are written to validation_removed.csv with a reason column.
The leads.csv is rewritten to contain only the validated rows.

Usage:
    python validate_leads.py                                     # all leads
    python validate_leads.py --country Netherlands               # dry-run NL
    python validate_leads.py --region Amsterdam                  # dry-run one region
    python validate_leads.py --country Netherlands --apply       # commit
    python validate_leads.py --regions "Amsterdam,Rotterdam"     # multiple regions
    python validate_leads.py --country Netherlands --apply --concurrency 4
"""
import argparse
import asyncio
import csv
import re
import urllib.parse
from pathlib import Path

from playwright.async_api import async_playwright, TimeoutError as PWTimeout

from gmaps_scraper import _is_real_website, _classify_online_presence


ROOT = Path(__file__).parent
MASTER_CSV = ROOT / "output" / "leads.csv"
REMOVED_CSV = ROOT / "output" / "validation_removed.csv"

USER_AGENT = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
              "AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/124.0.0.0 Safari/537.36")


async def _accept_consent(page):
    for label in ["Accept all", "I agree"]:
        try:
            await page.click(f'button:has-text("{label}")', timeout=2000)
            return
        except PWTimeout:
            pass


async def _extract_website(page) -> str:
    """Return the first non-Google website link visible on the place page,
    or '' if none. Uses both the standard data-item-id="authority" link
    AND the hotel-listing aria-label / text fallbacks."""
    el = await page.query_selector('a[data-item-id="authority"]')
    if el:
        href = (await el.get_attribute("href") or "").strip()
        if href:
            return href

    selectors = [
        'a[aria-label*="website" i]',
        'a[aria-label*="Official site" i]',
        'a[aria-label*="Visit hotel" i]',
        'a[data-tooltip*="website" i]',
        'a:has-text("Official site")',
        'a:has-text("Visit hotel website")',
        'a:has-text("Visit website")',
    ]
    for sel in selectors:
        try:
            el = await page.query_selector(sel)
        except Exception:
            continue
        if not el:
            continue
        href = (await el.get_attribute("href") or "").strip()
        if not href:
            continue
        if href.startswith("/maps") \
                or href.startswith("https://www.google.com/maps") \
                or "google.com/local" in href:
            continue
        return href
    return ""


def _name_matches(saved: str, on_page: str) -> bool:
    """Loose comparison -- handles minor punctuation/case differences."""
    if not saved or not on_page:
        return False
    a = re.sub(r"[^\w]+", " ", saved.lower()).strip()
    b = re.sub(r"[^\w]+", " ", on_page.lower()).strip()
    if a == b:
        return True
    return a in b or b in a


async def _check_one(page, row: dict, idx: int, total: int) -> tuple[str, dict]:
    """Returns (verdict, info). Verdict is one of:
        "ok"            keep the lead
        "url_mismatch"  page name differs from saved name
        "has_website"   place has a real (non-OTA) website
        "load_failed"   couldn't load page / no h1 -- keep (fail-open)
    """
    name = row.get("name", "")
    url = row.get("gmaps_url", "")
    info = {"saved_name": name, "url": url}
    if not url:
        return "load_failed", info | {"detail": "no_url"}

    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=20000)
    except Exception as e:
        return "load_failed", info | {"detail": f"goto: {e}"}
    await _accept_consent(page)

    # Wait for the place panel
    try:
        await page.wait_for_selector('h1.DUwDvf', timeout=8000)
    except PWTimeout:
        return "load_failed", info | {"detail": "no_h1"}
    await asyncio.sleep(0.3)

    h1 = await page.query_selector('h1.DUwDvf')
    page_name = (await h1.inner_text()).strip() if h1 else ""
    info["page_name"] = page_name

    if not _name_matches(name, page_name):
        return "url_mismatch", info

    website = await _extract_website(page)
    info["website"] = website
    if website and _is_real_website(website):
        info["online_presence"] = _classify_online_presence(website)
        return "has_website", info

    return "ok", info


def _row_matches_filters(row, country, region_set):
    if country and row.get("country", "").lower() != country.lower():
        return False
    if region_set and row.get("region", "").lower() not in region_set:
        return False
    return True


async def run(args):
    with open(MASTER_CSV, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    region_set = set()
    if args.region:
        region_set.add(args.region.lower())
    if args.regions:
        region_set.update(r.strip().lower() for r in args.regions.split(",")
                            if r.strip())

    targets = [r for r in rows
                if _row_matches_filters(r, args.country, region_set)]
    skipped = len(rows) - len(targets)
    filt = []
    if args.country:
        filt.append(f"country={args.country}")
    if region_set:
        filt.append(f"regions={sorted(region_set)}")
    filt_desc = " ".join(filt) if filt else "no filter"
    print(f"Validating {len(targets)} leads ({filt_desc}; "
          f"skipping {skipped} outside filter)")

    pw = await async_playwright().start()
    browser = await pw.chromium.launch(headless=not args.headed,
                                         channel="chromium")
    sem = asyncio.Semaphore(args.concurrency)
    results = {}  # row id (idx) -> verdict

    async def worker(idx: int, row: dict):
        async with sem:
            ctx = await browser.new_context(user_agent=USER_AGENT,
                                              locale="en-US",
                                              viewport={"width": 1366,
                                                         "height": 900})
            page = await ctx.new_page()
            try:
                verdict, info = await _check_one(page, row, idx, len(targets))
            except Exception as e:
                verdict, info = "load_failed", {"detail": f"exception: {e}"}
            finally:
                await ctx.close()
            results[idx] = (verdict, info)
            done = len(results)
            tag = ("OK" if verdict == "ok" else
                    "MISMATCH" if verdict == "url_mismatch" else
                    "WEBSITE" if verdict == "has_website" else
                    "LOAD")
            extra = ""
            if verdict == "url_mismatch":
                extra = f" saved={info.get('saved_name','')!r} " \
                        f"page={info.get('page_name','')!r}"
            elif verdict == "has_website":
                extra = f" {info.get('website','')}"
            print(f"  [{done}/{len(targets)}] {tag:9} "
                  f"{row.get('name',''):60} {extra}", flush=True)

    # Index targets by their position in the original `rows` list
    target_indices = [i for i, r in enumerate(rows)
                       if _row_matches_filters(r, args.country, region_set)]

    await asyncio.gather(*[worker(i, rows[i]) for i in target_indices])

    try:
        await browser.close()
    except Exception:
        pass
    await pw.stop()

    # Tally
    kept_rows = []
    removed_rows = []
    for i, r in enumerate(rows):
        if i not in results:
            kept_rows.append(r)
            continue
        verdict, info = results[i]
        if verdict in ("url_mismatch", "has_website"):
            r2 = dict(r)
            r2["_reason"] = verdict
            r2["_detail"] = (info.get("page_name") if verdict == "url_mismatch"
                              else info.get("website", ""))
            removed_rows.append(r2)
        else:
            kept_rows.append(r)

    print()
    print(f"Validated:   {len(results)}")
    print(f"  ok:          {sum(1 for v,_ in results.values() if v=='ok')}")
    print(f"  url_mismatch: {sum(1 for v,_ in results.values() if v=='url_mismatch')}")
    print(f"  has_website: {sum(1 for v,_ in results.values() if v=='has_website')}")
    print(f"  load_failed: {sum(1 for v,_ in results.values() if v=='load_failed')}")
    print(f"Total leads: {len(rows)}  ->  kept: {len(kept_rows)}  "
          f"removed: {len(removed_rows)}")

    if not args.apply:
        print("\n[dry-run] re-run with --apply to rewrite leads.csv.")
        return

    REMOVED_CSV.parent.mkdir(exist_ok=True)
    with open(REMOVED_CSV, "w", newline="", encoding="utf-8-sig") as f:
        out_fields = list(fieldnames) + ["_reason", "_detail"]
        w = csv.DictWriter(f, fieldnames=out_fields, extrasaction="ignore")
        w.writeheader()
        for r in removed_rows:
            w.writerow(r)
    print(f"  -> wrote {REMOVED_CSV}")

    with open(MASTER_CSV, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for r in kept_rows:
            w.writerow(r)
    print(f"  -> wrote {MASTER_CSV} ({len(kept_rows)} leads)")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--country", help="limit to this country (case-insensitive)")
    p.add_argument("--region", help="limit to a single region (case-insensitive)")
    p.add_argument("--regions", help="comma-separated regions (case-insensitive)")
    p.add_argument("--apply", action="store_true",
                   help="actually rewrite leads.csv (default: dry-run)")
    p.add_argument("--concurrency", type=int, default=4,
                   help="parallel browser tabs (default 4)")
    p.add_argument("--headed", action="store_true",
                   help="show the browser (debugging)")
    args = p.parse_args()
    asyncio.run(run(args))


if __name__ == "__main__":
    main()
