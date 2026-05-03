"""
Lead finder for Greek tourist accommodations without websites.
Uses Google Maps via Playwright. Maintains a single master CSV
in output/leads.csv that grows with every run (deduplicated).

Usage:
    python find_leads.py --region Paros
    python find_leads.py --regions Paros,Naxos,Mykonos
    python find_leads.py --all
    python find_leads.py --region Paros --headed   # see the browser
"""
import argparse
import asyncio
import csv
import json
import re
import sys
from pathlib import Path

from regions import REGIONS, country_for_region
from gmaps_scraper import scrape_region, filter_leads, _is_real_website,\
    is_blocked_category, is_accommodation_category, looks_like_accommodation_name


EMAIL_RE = re.compile(r"[\w\.\-+]+@[\w\.\-]+\.[a-zA-Z]{2,}")

OUTPUT_DIR = Path(__file__).parent / "output"
MASTER_CSV = OUTPUT_DIR / "leads.csv"
REJECTED_JSON = OUTPUT_DIR / "rejected.json"
SCRAPED_JSON = OUTPUT_DIR / "scraped.json"
PROGRESS_JSON = OUTPUT_DIR / "progress.json"
MASTER_FIELDS = ["country", "region", "name", "category", "phone", "email",
                  "gmaps_url", "online_presence",
                  "domain_gr_available", "domain_com_available",
                  "domain_suggestion", "enriched_at"]


def load_rejected() -> set[str]:
    """Load names previously rejected (had website, wrong category, etc)."""
    if not REJECTED_JSON.exists():
        return set()
    try:
        with open(REJECTED_JSON, encoding="utf-8") as f:
            return set(json.load(f))
    except Exception:
        return set()


def save_rejected(rejected: set[str]):
    REJECTED_JSON.parent.mkdir(exist_ok=True)
    with open(REJECTED_JSON, "w", encoding="utf-8") as f:
        json.dump(sorted(rejected), f, ensure_ascii=False, indent=0)


def load_scraped() -> dict:
    """Map: region -> {village_count, leads_count, scraped_at}."""
    if not SCRAPED_JSON.exists():
        return {}
    try:
        with open(SCRAPED_JSON, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_scraped(scraped: dict):
    SCRAPED_JSON.parent.mkdir(exist_ok=True)
    with open(SCRAPED_JSON, "w", encoding="utf-8") as f:
        json.dump(scraped, f, ensure_ascii=False, indent=2)


def mark_scraped(region: str, village_count: int, leads_count: int):
    """Mark a region as fully scraped after a successful run."""
    from datetime import datetime
    data = load_scraped()
    data[region] = {
        "scraped_at": datetime.now().isoformat(timespec="seconds"),
        "village_count": village_count,
        "scraped_villages": village_count,
        "leads_count": leads_count,
        "status": "done",
    }
    save_scraped(data)


def is_rejected_lead(lead: dict) -> bool:
    """Returns True if this lead would NOT pass filter — should be cached."""
    if _is_real_website(lead.get("website", "")):
        return True
    if is_blocked_category(lead.get("category", "")):
        return True
    if not lead.get("phone"):
        return True
    cat = lead.get("category", "")
    if not is_accommodation_category(cat) and \
            not (not cat and looks_like_accommodation_name(lead.get("name", ""))):
        return True
    return False


def extract_email(lead: dict) -> str:
    blob = " ".join(str(v) for v in lead.values() if v)
    m = EMAIL_RE.search(blob)
    return m.group(0) if m else ""


def normalize_phone(phone: str) -> str:
    return re.sub(r"[^\d+]", "", phone or "")


def clean_field(s: str) -> str:
    """Collapse internal whitespace/newlines so each lead is exactly one CSV row."""
    if not s:
        return ""
    return re.sub(r"\s+", " ", str(s)).strip()


def lead_key(lead: dict) -> tuple:
    """Dedup key: (region, normalized_phone) — same phone in same region = dup."""
    return (lead.get("region", "").strip().lower(),
            normalize_phone(lead.get("phone", "")))


def load_master() -> dict:
    """Load existing master CSV into dict keyed by (region, phone)."""
    existing = {}
    if MASTER_CSV.exists():
        with open(MASTER_CSV, encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                k = lead_key(row)
                if k[1]:
                    existing[k] = row
    return existing


def save_master(leads_by_key: dict):
    """Sort by region, then name, and write the single master CSV."""
    rows = sorted(leads_by_key.values(),
                   key=lambda r: (r.get("region", ""), r.get("name", "")))

    with open(MASTER_CSV, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=MASTER_FIELDS, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            region = r.get("region", "")
            # Backfill country from region if missing (handles legacy rows)
            country = r.get("country") or country_for_region(region)
            w.writerow({
                "country": clean_field(country),
                "region": clean_field(region),
                "name": clean_field(r.get("name", "")),
                "category": clean_field(r.get("category", "")),
                "phone": clean_field(r.get("phone", "")),
                "email": clean_field(r.get("email", "") or extract_email(r)),
                "gmaps_url": clean_field(r.get("gmaps_url", "")),
                "online_presence": clean_field(r.get("online_presence", "")),
                "domain_gr_available": clean_field(
                    r.get("domain_gr_available", "")),
                "domain_com_available": clean_field(
                    r.get("domain_com_available", "")),
                "domain_suggestion": clean_field(
                    r.get("domain_suggestion", "")),
                "enriched_at": clean_field(r.get("enriched_at", "")),
            })


async def run(args):
    if args.all:
        region_names = list(REGIONS.keys())
    elif args.regions:
        region_names = [r.strip() for r in args.regions.split(",")]
    elif args.region:
        region_names = [args.region]
    else:
        print("error: specify --region, --regions, or --all", file=sys.stderr)
        sys.exit(1)

    unknown = [r for r in region_names if r not in REGIONS]
    if unknown:
        print(f"warn: regions not in regions.py (will still search): {unknown}")

    OUTPUT_DIR.mkdir(exist_ok=True)
    master = load_master()
    print(f"Loaded master: {len(master)} existing leads in {MASTER_CSV}")

    if args.skip_existing:
        before = len(region_names)
        region_names = [n for n in region_names if not any(
            r.get("region", "").lower() == n.lower() for r in master.values())]
        skipped = before - len(region_names)
        if skipped:
            print(f"  [skip] {skipped} regions already have leads in master")

    print(f"\nScraping Google Maps for {len(region_names)} region(s) "
          f"with {args.concurrency} concurrent worker(s)...")

    save_lock = asyncio.Lock()
    rejected = load_rejected()
    print(f"Loaded rejected cache: {len(rejected)} names")
    new_total = 0

    # Resolve CRM sync config once. Each region will push its own leads as
    # soon as it finishes, so a Ctrl+C / crash mid-run still leaves all
    # already-completed regions in the CRM.
    crm_cfg = None
    if not args.no_sync:
        try:
            from crm_sync import load_config as _crm_load_config
            cfg = _crm_load_config()
            if cfg.get("url") and cfg.get("token"):
                crm_cfg = cfg
                print(f"[CRM Sync] enabled -> {cfg['url']} "
                      "(per-region push)")
            else:
                print("[CRM Sync] disabled — not configured. Run "
                      "'python crm_sync.py --setup' to enable.")
        except Exception as e:
            print(f"[CRM Sync] disabled — config error: {e}")

    # Progress tracker: maps region -> (queries_done, queries_total, last_ts)
    import time as _time
    try:
        from villages import expand_region as _expand
        from gmaps_scraper import QUERIES_PER_REGION as _QPR
    except ImportError:
        _expand = lambda r: [r]
        _QPR = ["hotels in {region}"]

    progress_state = {
        "started_at": _time.time(),
        "regions": {n: {
            "done": 0,
            "total": len(_expand(n)) * len(_QPR),
            "started": False,
        } for n in region_names},
        "completed_query_times": [],
    }

    # Clear any stale progress.json from a previous run, then write
    # an initial snapshot so the dashboard shows the progress bar
    # immediately (instead of waiting for the first query to finish).
    try:
        if PROGRESS_JSON.exists():
            PROGRESS_JSON.unlink()
    except Exception:
        pass

    def write_progress():
        elapsed = _time.time() - progress_state["started_at"]
        total_done = sum(r["done"] for r in progress_state["regions"].values())
        total_queries = sum(r["total"] for r in progress_state["regions"].values())
        avg = (sum(progress_state["completed_query_times"][-20:]) /
                len(progress_state["completed_query_times"][-20:])
                if progress_state["completed_query_times"] else 0)
        # Effective avg considering concurrency
        eff_avg = avg / max(1, args.concurrency)
        eta_seconds = (total_queries - total_done) * eff_avg if avg else 0

        try:
            with open(PROGRESS_JSON, "w", encoding="utf-8") as f:
                json.dump({
                    "elapsed": elapsed,
                    "queries_done": total_done,
                    "queries_total": total_queries,
                    "percent": (total_done / total_queries * 100)
                                if total_queries else 0,
                    "eta_seconds": eta_seconds,
                    "avg_query_seconds": avg,
                    "concurrency": args.concurrency,
                    "regions": progress_state["regions"],
                }, f, indent=2)
        except Exception:
            pass

    async def on_query_done(region: str, done: int, total: int):
        async with save_lock:
            r = progress_state["regions"].setdefault(
                region, {"done": 0, "total": total, "started": True})
            # Track time per query (rough)
            now = _time.time()
            last = r.get("last_query_ts", progress_state["started_at"])
            progress_state["completed_query_times"].append(now - last)
            r["last_query_ts"] = now
            r["done"] = done
            r["total"] = total
            r["started"] = True
            write_progress()

    async def process_region(name: str):
        nonlocal new_total
        print(f"\n[{name}] starting...")
        # Pre-load names already in master for this region (case-insensitive)
        existing_names = {
            r.get("name", "") for r in master.values()
            if r.get("region", "").lower() == name.lower()
        }
        # Track keys added during THIS region's run so the per-region CRM
        # push only sends newly-scraped leads, not the entire region.
        new_keys_this_region = set()

        # Incremental save: persist after every query inside the region
        async def on_progress(new_in_query):
            async with save_lock:
                added = 0
                rej_added = 0
                for lead in new_in_query:
                    name_lower = lead.get("name", "").lower().strip()
                    if is_rejected_lead(lead):
                        if name_lower:
                            if name_lower not in rejected:
                                rej_added += 1
                            rejected.add(name_lower)
                        continue
                    k = lead_key(lead)
                    if not k[1] or k in master:
                        continue
                    region = lead.get("region", name)
                    master[k] = {
                        "country": country_for_region(region),
                        "region": region,
                        "name": lead.get("name", ""),
                        "category": lead.get("category", ""),
                        "phone": lead.get("phone", ""),
                        "email": extract_email(lead),
                        "gmaps_url": lead.get("gmaps_url", ""),
                        "online_presence": lead.get("online_presence", ""),
                    }
                    new_keys_this_region.add(k)
                    added += 1
                # Always save both files when there's any progress
                if added or rej_added:
                    save_master(master)
                    save_rejected(rejected)
                print(f"    [save] +{added} leads, +{rej_added} rejected "
                      f"(master={len(master)}, rejected={len(rejected)}, "
                      f"this query={len(new_in_query)})", flush=True)

        try:
            leads = await scrape_region(name, headless=not args.headed,
                                          existing_names=existing_names,
                                          rejected_names=rejected,
                                          country=country_for_region(name),
                                          on_progress=on_progress,
                                          on_query_done=on_query_done)
        except Exception as e:
            print(f"[{name}] [error] {e}")
            leads = []

        with_phone = sum(1 for l in leads if l.get("phone"))
        with_site = sum(1 for l in leads if l.get("website"))
        filtered = filter_leads(leads)
        print(f"[{name}] scraped: {len(leads)}, with phone: {with_phone}, "
              f"with website: {with_site}, passed filter: {len(filtered)}",
              flush=True)

        # Final reconciliation (in case last query didn't fire callback)
        async with save_lock:
            new_in_region = 0
            for lead in filtered:
                k = lead_key(lead)
                if not k[1] or k in master:
                    continue
                region = lead.get("region", name)
                master[k] = {
                    "country": country_for_region(region),
                    "region": region,
                    "name": lead.get("name", ""),
                    "category": lead.get("category", ""),
                    "phone": lead.get("phone", ""),
                    "email": extract_email(lead),
                    "gmaps_url": lead.get("gmaps_url", ""),
                    "online_presence": lead.get("online_presence", ""),
                }
                new_keys_this_region.add(k)
                new_in_region += 1
            new_total += new_in_region
            save_master(master)
            save_rejected(rejected)

            # Count villages searched and total leads for this region
            try:
                from villages import expand_region
                village_count = len(expand_region(name))
            except Exception:
                village_count = 1
            region_leads = sum(1 for r in master.values()
                                if r.get("region", "").lower() == name.lower())
            mark_scraped(name, village_count, region_leads)

            print(f"[{name}] DONE — added: {new_in_region} extra "
                  f"(master total: {len(master)}, region total: "
                  f"{region_leads})", flush=True)

            # Push only the leads NEWLY ADDED in this region's run -- not
            # the entire region, which would re-push thousands of already-
            # synced rows for no benefit (the CRM upserts are idempotent
            # but every row still costs a round-trip).
            if crm_cfg and new_keys_this_region:
                new_rows = [master[k] for k in new_keys_this_region
                             if k in master and master[k].get("phone")]
                if new_rows:
                    try:
                        from crm_sync import push_to_crm
                        print(f"[{name}] [CRM] pushing {len(new_rows)} "
                              f"new leads...", flush=True)
                        result = push_to_crm(new_rows, crm_cfg["url"],
                                              crm_cfg["token"])
                        print(f"[{name}] [CRM] done — "
                              f"{result['upserted']} upserted", flush=True)
                    except Exception as e:
                        print(f"[{name}] [CRM] failed: {e}", flush=True)
            elif crm_cfg:
                print(f"[{name}] [CRM] no new leads to push.", flush=True)

    sem = asyncio.Semaphore(args.concurrency)

    async def bounded(name):
        async with sem:
            await process_region(name)

    # Write an initial snapshot so the dashboard shows the progress bar
    # immediately (with 0/total) — otherwise the bar stays hidden until
    # the first query finishes (which can take 30+ seconds while
    # Playwright spins up).
    write_progress()

    await asyncio.gather(*[bounded(n) for n in region_names])

    # Mark progress as complete
    try:
        with open(PROGRESS_JSON, "w", encoding="utf-8") as f:
            json.dump({"completed": True}, f)
    except Exception:
        pass

    print("\n" + "=" * 60)
    print(f"DONE. master has {len(master)} leads (+{new_total} this run)")
    print(f"  -> {MASTER_CSV}")
    if crm_cfg:
        print("[CRM Sync] all regions pushed during run "
              "(per-region push, see [<region>] [CRM] lines above).")
    # If you need to push the full CSV (e.g. after editing it manually),
    # run `python crm_sync.py` instead.


def main():
    p = argparse.ArgumentParser(description=__doc__)
    g = p.add_mutually_exclusive_group()
    g.add_argument("--region", help="single region (e.g. Paros)")
    g.add_argument("--regions", help="comma-separated regions")
    g.add_argument("--all", action="store_true",
                   help="all regions defined in regions.py")
    p.add_argument("--headed", action="store_true",
                   help="show the browser window (for debugging)")
    p.add_argument("--skip-existing", action="store_true",
                   help="skip regions that already have leads in the master CSV")
    p.add_argument("--concurrency", type=int, default=2,
                   help="number of regions to scrape in parallel (default 2)")
    p.add_argument("--no-sync", action="store_true",
                   help="don't push results to CRM after scraping")
    args = p.parse_args()
    asyncio.run(run(args))


if __name__ == "__main__":
    main()
