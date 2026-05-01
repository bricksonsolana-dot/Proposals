"""
Pushes leads from the local lead-finder CSV to the cloud CRM.
Configured via environment variables:
  CRM_URL    — base URL of the CRM (e.g. https://yourapp.onrender.com)
  CRM_TOKEN  — sync token (must match SYNC_TOKEN in CRM env)

Usage:
  python crm_sync.py                # push all leads from output/leads.csv
  python crm_sync.py --since 1h     # only leads imported/enriched in last hour
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
    p = argparse.ArgumentParser()
    p.add_argument("--setup", action="store_true",
                   help="Interactive setup of CRM URL and token")
    p.add_argument("--dry-run", action="store_true",
                   help="Show what would be sent, don't push")
    args = p.parse_args()

    if args.setup:
        setup_interactive()
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

    print(f"Pushing {len(leads)} leads to {cfg['url']}...")
    if args.dry_run:
        print(f"[dry-run] would push {len(leads)} leads")
        return

    start = time.time()
    result = push_to_crm(leads, cfg["url"], cfg["token"])
    elapsed = time.time() - start
    print(f"\nDone in {elapsed:.1f}s — {result['upserted']} upserted")


if __name__ == "__main__":
    main()
