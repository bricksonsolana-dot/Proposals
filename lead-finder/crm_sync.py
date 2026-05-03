"""
Pushes leads from the local lead-finder CSV to the cloud CRM.
Configured via environment variables:
  CRM_URL    — base URL of the CRM (e.g. https://yourapp.onrender.com)
  CRM_TOKEN  — sync token (must match SYNC_TOKEN in CRM env)

Default behavior: only push leads whose phone number has never been
successfully pushed before (tracked in output/synced_phones.json). This
keeps every scrape fast and avoids re-uploading thousands of unchanged
rows. Use --force to push every lead in the CSV regardless of state
(e.g. after manual cleanup_leads.py / backfill_urls.py edits, or after
the CRM database was wiped).

Usage:
  python crm_sync.py                # push only new (never-synced) leads
  python crm_sync.py --force        # push everything in leads.csv
  python crm_sync.py --setup        # configure CRM_URL / CRM_TOKEN
  python crm_sync.py --dry-run      # show what would be pushed
"""
import argparse
import csv
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent
LEADS_CSV = ROOT / "output" / "leads.csv"
CONFIG_FILE = ROOT / "crm_sync.config.json"
SYNCED_JSON = ROOT / "output" / "synced_phones.json"


def _normalize_phone(phone: str) -> str:
    """Match the normalisation used by find_leads.lead_key, so the same
    phone string written by the scraper or read from the CSV produces the
    same key in synced_phones.json."""
    import re
    return re.sub(r"[^\d+]", "", phone or "")


def load_synced() -> set[str]:
    """Set of normalised phone numbers we've successfully pushed to the CRM."""
    if not SYNCED_JSON.exists():
        return set()
    try:
        with open(SYNCED_JSON, encoding="utf-8") as f:
            return set(json.load(f))
    except Exception:
        return set()


def _save_synced(s: set[str]):
    SYNCED_JSON.parent.mkdir(exist_ok=True)
    with open(SYNCED_JSON, "w", encoding="utf-8") as f:
        json.dump(sorted(s), f, ensure_ascii=False, indent=0)


def mark_synced(phones):
    """Add the given phones to the synced set on disk (idempotent)."""
    s = load_synced()
    new = {_normalize_phone(p) for p in phones if p}
    if new - s:
        s |= new
        _save_synced(s)


def filter_unsynced(leads: list[dict]) -> list[dict]:
    """Return only leads whose phone hasn't been successfully synced yet."""
    s = load_synced()
    return [l for l in leads
             if l.get("phone") and _normalize_phone(l["phone"]) not in s]


def load_config() -> dict:
    """Load CRM_URL and CRM_TOKEN from env vars or local config file."""
    cfg = {}
    if CONFIG_FILE.exists():
        try:
            cfg = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {
        "url": os.environ.get("CRM_URL") or cfg.get("url", ""),
        "token": os.environ.get("CRM_TOKEN") or cfg.get("token", ""),
    }


def save_config(url: str, token: str):
    CONFIG_FILE.write_text(
        json.dumps({"url": url, "token": token}, indent=2),
        encoding="utf-8")


def load_leads() -> list[dict]:
    if not LEADS_CSV.exists():
        return []
    with open(LEADS_CSV, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def push_to_crm(leads: list[dict], url: str, token: str,
                 batch_size: int = 50) -> dict:
    """Push leads in batches. Returns total upserted count.

    Retries on timeout (Render free tier may need cold-start).
    """
    if not url or not token:
        raise RuntimeError(
            "Missing CRM_URL or CRM_TOKEN. Set them as env vars or run "
            "`python crm_sync.py --setup`")

    endpoint = url.rstrip("/") + "/api/sync/leads"
    total_upserted = 0
    total_batches = (len(leads) + batch_size - 1) // batch_size

    for i in range(0, len(leads), batch_size):
        batch = leads[i:i+batch_size]
        body = json.dumps({"leads": batch}).encode("utf-8")
        batch_num = i // batch_size + 1

        attempt = 0
        last_err = None
        while attempt < 3:
            attempt += 1
            req = urllib.request.Request(
                endpoint, data=body, method="POST",
                headers={
                    "Content-Type": "application/json",
                    "X-Sync-Token": token,
                })
            # 90s timeout — first call may need cold-start on free tier
            timeout = 90 if attempt == 1 else 60
            try:
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    total_upserted += data.get("upserted", 0)
                    # Record successfully-pushed phones so future runs skip
                    # them. Persist after every batch (not just at end), so
                    # a crash/Ctrl+C mid-push still preserves what landed.
                    mark_synced(l.get("phone", "") for l in batch)
                    print(f"  batch {batch_num}/{total_batches}: "
                          f"{data.get('upserted', 0)} upserted", flush=True)
                    break  # success, next batch
            except urllib.error.HTTPError as e:
                err = e.read().decode("utf-8")[:200]
                raise RuntimeError(f"HTTP {e.code} from CRM: {err}") from None
            except (urllib.error.URLError, TimeoutError, OSError) as e:
                last_err = e
                if attempt < 3:
                    print(f"  batch {batch_num}: retry {attempt}/3 after error: "
                          f"{type(e).__name__}", flush=True)
                    time.sleep(3 * attempt)
                    continue
                raise RuntimeError(
                    f"Could not reach CRM at {url} after 3 attempts: "
                    f"{last_err}") from None

    return {"upserted": total_upserted, "sent": len(leads)}


def setup_interactive():
    print("CRM Sync Setup")
    print("--------------")
    cur = load_config()
    url = input(f"CRM URL [{cur.get('url') or 'http://localhost:5001'}]: ").strip()
    if not url:
        url = cur.get("url") or "http://localhost:5001"
    token = input(f"CRM Sync Token [{cur.get('token') or 'dev-token'}]: ").strip()
    if not token:
        token = cur.get("token") or "dev-token"
    save_config(url, token)
    print(f"\nSaved to {CONFIG_FILE}")
    print(f"  URL:   {url}")
    print(f"  Token: {token[:6]}***")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--setup", action="store_true",
                   help="Interactive setup of CRM URL and token")
    p.add_argument("--dry-run", action="store_true",
                   help="Show what would be sent, don't push")
    p.add_argument("--force", action="store_true",
                   help="Push every lead in the CSV, ignoring synced state. "
                         "Use after manual edits or CRM data loss.")
    p.add_argument("--mark-synced", action="store_true",
                   help="Mark every phone in the CSV as already-synced "
                         "WITHOUT pushing. Use this once if the CRM was "
                         "populated by an external sync (e.g. an old script) "
                         "so future scrapes know not to re-push them.")
    args = p.parse_args()

    if args.setup:
        setup_interactive()
        return

    if args.mark_synced:
        leads = load_leads()
        phones = {l.get("phone", "") for l in leads if l.get("phone")}
        before = len(load_synced())
        mark_synced(phones)
        after = len(load_synced())
        print(f"Marked {after - before} new phones as synced "
              f"(total: {after}). Future scrapes will skip them.")
        return

    cfg = load_config()
    if not cfg["url"] or not cfg["token"]:
        print("ERROR: CRM URL or token not configured.")
        print("Run: python crm_sync.py --setup")
        sys.exit(1)

    leads = load_leads()
    if not leads:
        print(f"No leads in {LEADS_CSV}")
        return

    if args.force:
        to_push = leads
        print(f"[--force] pushing all {len(to_push)} leads to {cfg['url']}...")
    else:
        synced_before = len(load_synced())
        to_push = filter_unsynced(leads)
        print(f"In CSV: {len(leads)}  already synced: {synced_before}  "
              f"to push: {len(to_push)}")
        if not to_push:
            print("Nothing to push -- everything in the CSV is already on the CRM.")
            return
        print(f"Pushing {len(to_push)} new leads to {cfg['url']}...")

    if args.dry_run:
        print(f"[dry-run] would push {len(to_push)} leads")
        return

    start = time.time()
    result = push_to_crm(to_push, cfg["url"], cfg["token"])
    elapsed = time.time() - start
    print(f"\nDone in {elapsed:.1f}s -- {result['upserted']} upserted")


if __name__ == "__main__":
    main()
