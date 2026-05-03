"""
Admin dashboard for the lead finder.
Run with:
    python dashboard.py

Then open http://localhost:5000 in your browser.

Provides:
  - Start/Stop scraping
  - Live progress (current region, query, leads found)
  - Live table of all leads in the master CSV
  - Region selection (single, multiple, all)
"""
import csv
import os
import signal
import subprocess
import sys
import threading
import time
from collections import deque
from pathlib import Path

from flask import Flask, jsonify, render_template_string, request

from regions import REGIONS, REGION_GROUPS, COUNTRIES, country_for_region

ROOT = Path(__file__).parent
OUTPUT_DIR = ROOT / "output"
MASTER_CSV = OUTPUT_DIR / "leads.csv"
PYTHON_EXE = sys.executable

app = Flask(__name__)

# Global scraper state
state = {
    "running": False,
    "process": None,
    "log": deque(maxlen=500),
    "started_at": None,
    "regions": [],
    "current_region": None,
}
state_lock = threading.Lock()


def log_line(line: str):
    line = line.rstrip()
    if line:
        with state_lock:
            state["log"].append({"t": time.strftime("%H:%M:%S"), "line": line})
            # Track current region from log lines
            if "] starting..." in line:
                start = line.find("[") + 1
                end = line.find("]")
                if 0 < start < end:
                    state["current_region"] = line[start:end]


def reader_thread(proc):
    """Read stdout from the scraper process and append to log."""
    try:
        for line in proc.stdout:
            log_line(line)
    except Exception as e:
        log_line(f"[reader error] {e}")
    finally:
        with state_lock:
            state["running"] = False
            state["process"] = None
            state["current_region"] = None
        log_line("=== scraper stopped ===")


def start_scraper(regions: list[str], concurrency: int):
    with state_lock:
        if state["running"]:
            return False, "already running"

    args = [PYTHON_EXE, "-u", str(ROOT / "find_leads.py"),
            "--concurrency", str(concurrency)]
    if not regions or regions == ["__all__"]:
        args.append("--all")
    elif len(regions) == 1:
        args.extend(["--region", regions[0]])
    else:
        args.extend(["--regions", ",".join(regions)])

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    # Clear stale progress file
    try:
        if PROGRESS_JSON.exists():
            PROGRESS_JSON.unlink()
    except Exception:
        pass

    proc = subprocess.Popen(
        args, cwd=str(ROOT),
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, encoding="utf-8", errors="replace",
        bufsize=1, env=env,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt"
                       else 0,
    )

    with state_lock:
        state["running"] = True
        state["process"] = proc
        state["started_at"] = time.time()
        state["regions"] = regions
        state["current_region"] = None
        state["log"].clear()
    log_line(f"=== started: {' '.join(args[1:])} ===")

    threading.Thread(target=reader_thread, args=(proc,), daemon=True).start()
    return True, "started"


def stop_scraper():
    with state_lock:
        proc = state["process"]
        if not proc:
            return False, "not running"
    log_line("=== stop requested ===")
    try:
        if os.name == "nt":
            proc.send_signal(signal.CTRL_BREAK_EVENT)
            time.sleep(2)
            if proc.poll() is None:
                proc.terminate()
        else:
            proc.terminate()
    except Exception as e:
        log_line(f"[stop error] {e}")
    return True, "stopping"


def load_leads():
    if not MASTER_CSV.exists():
        return []
    with open(MASTER_CSV, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


# ----------------------------- API endpoints -----------------------------

SCRAPED_JSON = ROOT / "output" / "scraped.json"
PROGRESS_JSON = ROOT / "output" / "progress.json"


def load_scraped_status() -> dict:
    if not SCRAPED_JSON.exists():
        return {}
    try:
        import json as _json
        with open(SCRAPED_JSON, encoding="utf-8") as f:
            return _json.load(f)
    except Exception:
        return {}


def load_progress() -> dict:
    if not PROGRESS_JSON.exists():
        return {}
    try:
        import json as _json
        with open(PROGRESS_JSON, encoding="utf-8") as f:
            return _json.load(f)
    except Exception:
        return {}


@app.route("/api/progress")
def api_progress():
    return jsonify(load_progress())


@app.route("/api/regions")
def api_regions():
    # Strip dict structure to what the UI needs (groups per country).
    countries = {
        name: {
            "code": data["code"],
            "groups": data["groups"],
        }
        for name, data in COUNTRIES.items()
    }
    return jsonify({
        "countries": countries,
        "groups": REGION_GROUPS,  # legacy: flat group->regions
        "all": list(REGIONS.keys()),
        "scraped": load_scraped_status(),
    })


@app.route("/api/status")
def api_status():
    with state_lock:
        log = list(state["log"])[-100:]
        return jsonify({
            "running": state["running"],
            "started_at": state["started_at"],
            "elapsed": (time.time() - state["started_at"])
                        if state["started_at"] else 0,
            "regions": state["regions"],
            "current_region": state["current_region"],
            "log": log,
        })


@app.route("/api/leads")
def api_leads():
    leads = load_leads()
    # Backfill country for legacy rows missing the column
    for l in leads:
        if not l.get("country"):
            l["country"] = country_for_region(l.get("region", ""))
    by_region = {}
    by_country = {}
    for l in leads:
        by_region.setdefault(l.get("region", ""), []).append(l)
        by_country.setdefault(l.get("country", "") or "Unknown",
                                []).append(l)
    return jsonify({
        "total": len(leads),
        "by_region": [{"region": r, "count": len(rows)}
                       for r, rows in sorted(by_region.items())],
        "by_country": [{"country": c, "count": len(rows)}
                        for c, rows in sorted(by_country.items())],
        "leads": leads,
    })


def generate_talking_points(lead: dict) -> list[str]:
    """Auto-generate sales pitch bullet points based on lead data."""
    points = []
    name = lead.get("name", "")
    op = (lead.get("online_presence") or "").lower()
    cat = (lead.get("category") or "").lower()

    # Online presence specific pitches
    if op == "none":
        points.append(
            "Δεν εμφανίζεται website στο Google Maps profile τους — "
            "τους χάνουν δυνητικοί επισκέπτες."
        )
    elif op == "facebook":
        points.append(
            "Έχουν μόνο Facebook page ως online presence — "
            "ένα professional site θα ανέβαζε credibility."
        )
    elif op == "instagram":
        points.append(
            "Έχουν μόνο Instagram ως κανάλι — "
            "δεν δέχονται direct booking, χάνουν σε προμήθειες OTA."
        )
    elif op == "booking":
        points.append(
            "Φαίνονται μόνο μέσω Booking.com — πληρώνουν 15-18% commission "
            "σε κάθε κράτηση. Με δικό τους site γλιτώνουν."
        )
    elif op == "airbnb":
        points.append(
            "Φαίνονται μόνο μέσω Airbnb — εξαρτώνται 100% από την πλατφόρμα."
        )
    elif op == "ota-aggregator" or op == "link-in-bio":
        points.append(
            "Δεν έχουν δικό τους site — μόνο OTA listing ή link-in-bio."
        )

    # Domain availability — VERY strong pitch
    sug = lead.get("domain_suggestion") or ""
    if sug:
        points.append(
            f"Το domain {sug} είναι διαθέσιμο — μπορούμε να το πιάσουμε "
            f"για εσάς πριν το κλείσει κάποιος άλλος."
        )

    # Category-based personalisation
    if "villa" in cat or "villa" in name.lower():
        points.append(
            "Premium κατάλυμα: το branding και τα high-quality photos "
            "παίζουν τεράστιο ρόλο. Ένα παρουσιαστικό site αυξάνει "
            "averageRate."
        )
    elif "apartment" in cat or "studio" in cat:
        points.append(
            "Self-catering κατάλυμα — οι direct guests προτιμούν να κλείνουν "
            "με τον ιδιοκτήτη όταν έχουν τη δυνατότητα."
        )

    # Email
    if not lead.get("email"):
        points.append(
            "Δεν φαίνεται email στο Google Maps — μπορείτε να ζητήσετε "
            "στο τηλέφωνο για να στείλετε προσφορά γραπτώς."
        )

    return points


@app.route("/api/lead/<phone>")
def api_lead_detail(phone):
    leads = load_leads()
    import re as _re
    norm = _re.sub(r"[^\d+]", "", phone)
    for l in leads:
        if _re.sub(r"[^\d+]", "", l.get("phone", "")) == norm:
            return jsonify({
                "lead": l,
                "talking_points": generate_talking_points(l),
            })
    return jsonify({"error": "not found"}), 404


enrich_state = {"running": False, "done": 0, "total": 0,
                  "started_at": None, "log": []}
enrich_lock = threading.Lock()


def run_enrich_thread(force: bool):
    import asyncio as _asyncio
    import sys as _sys
    sys.path.insert(0, str(ROOT))
    from enrich import load_master, save_master, enrich_all
    leads = load_master()
    pending = [l for l in leads if force or not l.get("enriched_at")]
    with enrich_lock:
        enrich_state["running"] = True
        enrich_state["done"] = 0
        enrich_state["total"] = len(pending)
        enrich_state["started_at"] = time.time()
        enrich_state["log"] = [
            f"Loaded {len(leads)} leads, {len(pending)} need enrichment"]

    async def progress(done, total):
        with enrich_lock:
            enrich_state["done"] = done

    try:
        loop = _asyncio.new_event_loop()
        _asyncio.set_event_loop(loop)
        enriched = loop.run_until_complete(
            enrich_all(leads, concurrency=30, force=force,
                        on_progress=progress))
        save_master(enriched)
        loop.close()
        gr = sum(1 for l in enriched if l.get("domain_gr_available") == "yes")
        com = sum(1 for l in enriched if l.get("domain_com_available") == "yes")
        with enrich_lock:
            enrich_state["log"].append(
                f".gr available: {gr}, .com available: {com}")
            enrich_state["done"] = enrich_state["total"]

        # Auto-sync to CRM after enrichment finishes
        try:
            from crm_sync import load_config, push_to_crm, load_leads as _ll
            cfg = load_config()
            if cfg.get("url") and cfg.get("token"):
                fresh = _ll()
                result = push_to_crm(fresh, cfg["url"], cfg["token"])
                with enrich_lock:
                    enrich_state["log"].append(
                        f"CRM sync: {result['upserted']} pushed")
        except Exception as e:
            with enrich_lock:
                enrich_state["log"].append(f"CRM sync failed: {e}")
    except Exception as e:
        with enrich_lock:
            enrich_state["log"].append(f"ERROR: {e}")
    finally:
        with enrich_lock:
            enrich_state["running"] = False


@app.route("/api/enrich", methods=["POST"])
def api_enrich():
    data = request.get_json(force=True) or {}
    force = bool(data.get("force", False))
    with enrich_lock:
        if enrich_state["running"]:
            return jsonify({"ok": False, "msg": "already running"})
    threading.Thread(target=run_enrich_thread, args=(force,),
                       daemon=True).start()
    return jsonify({"ok": True, "msg": "started"})


@app.route("/api/enrich/status")
def api_enrich_status():
    with enrich_lock:
        elapsed = (time.time() - enrich_state["started_at"]) \
            if enrich_state["started_at"] else 0
        rate = enrich_state["done"] / elapsed if elapsed else 0
        eta = ((enrich_state["total"] - enrich_state["done"]) / rate) \
            if rate else 0
        return jsonify({
            "running": enrich_state["running"],
            "done": enrich_state["done"],
            "total": enrich_state["total"],
            "percent": (enrich_state["done"] / enrich_state["total"] * 100)
                        if enrich_state["total"] else 0,
            "elapsed": elapsed,
            "eta": eta,
            "log": enrich_state["log"][-10:],
        })


sync_state = {"running": False, "msg": "", "last_result": None,
                "started_at": None}
sync_lock = threading.Lock()


def run_sync_thread():
    with sync_lock:
        sync_state["running"] = True
        sync_state["msg"] = "Loading config..."
        sync_state["started_at"] = time.time()
        sync_state["last_result"] = None
    try:
        sys.path.insert(0, str(ROOT))
        from crm_sync import load_config, push_to_crm, load_leads
        cfg = load_config()
        if not cfg.get("url") or not cfg.get("token"):
            with sync_lock:
                sync_state["msg"] = ("Not configured. Run "
                                       "'python crm_sync.py --setup' "
                                       "in terminal.")
            return
        leads = load_leads()
        with sync_lock:
            sync_state["msg"] = (f"Pushing {len(leads)} leads to "
                                   f"{cfg['url']}...")
        result = push_to_crm(leads, cfg["url"], cfg["token"])
        with sync_lock:
            sync_state["msg"] = (f"Done — {result['upserted']} upserted")
            sync_state["last_result"] = result
    except Exception as e:
        with sync_lock:
            sync_state["msg"] = f"ERROR: {e}"
    finally:
        with sync_lock:
            sync_state["running"] = False


@app.route("/api/sync_crm", methods=["POST"])
def api_sync_crm():
    with sync_lock:
        if sync_state["running"]:
            return jsonify({"ok": False, "msg": "already running"})
    threading.Thread(target=run_sync_thread, daemon=True).start()
    return jsonify({"ok": True, "msg": "started"})


@app.route("/api/sync_crm/status")
def api_sync_crm_status():
    with sync_lock:
        return jsonify({
            "running": sync_state["running"],
            "msg": sync_state["msg"],
            "last_result": sync_state["last_result"],
        })


@app.route("/api/start", methods=["POST"])
def api_start():
    data = request.get_json(force=True) or {}
    regions = data.get("regions", [])
    concurrency = int(data.get("concurrency", 2))
    ok, msg = start_scraper(regions, concurrency)
    return jsonify({"ok": ok, "msg": msg})


@app.route("/api/stop", methods=["POST"])
def api_stop():
    ok, msg = stop_scraper()
    return jsonify({"ok": ok, "msg": msg})


# ----------------------------- UI -----------------------------

INDEX_HTML = """<!doctype html>
<html lang="el">
<head>
<meta charset="utf-8">
<title>Lead Finder Dashboard</title>
<style>
  body { font-family: -apple-system, Segoe UI, sans-serif; margin: 0;
         background: #0f1117; color: #e8eaf0; }
  .top { padding: 16px 24px; background: #1a1d27;
         border-bottom: 1px solid #2a2f3d; display: flex;
         align-items: center; gap: 24px; }
  .top h1 { margin: 0; font-size: 18px; font-weight: 600; }
  .pill { padding: 4px 12px; border-radius: 999px; font-size: 12px;
          font-weight: 600; }
  .pill.running { background: #1e4d2b; color: #4ade80; }
  .pill.stopped { background: #4a1d1d; color: #f87171; }
  .container { display: grid; grid-template-columns: 360px 1fr;
               gap: 0; height: calc(100vh - 60px); }
  .sidebar { padding: 20px; border-right: 1px solid #2a2f3d;
             overflow-y: auto; }
  .main { padding: 20px; overflow-y: auto; }
  h2 { font-size: 14px; text-transform: uppercase; color: #8b92a6;
       margin: 24px 0 12px; letter-spacing: 0.5px; }
  h2:first-child { margin-top: 0; }
  button { background: #2563eb; color: white; border: 0; padding: 10px 16px;
           border-radius: 6px; font-weight: 600; cursor: pointer;
           font-size: 14px; }
  button:hover { background: #1d4ed8; }
  button.danger { background: #dc2626; }
  button.danger:hover { background: #b91c1c; }
  button:disabled { opacity: 0.4; cursor: not-allowed; }
  .controls { display: flex; gap: 8px; margin-bottom: 16px; }
  select { background: #1a1d27; color: #e8eaf0; border: 1px solid #2a2f3d;
           padding: 8px; border-radius: 6px; width: 100%; font-size: 14px; }
  .region-picker { background: #1a1d27; border: 1px solid #2a2f3d;
                   border-radius: 6px; padding: 8px; max-height: 420px;
                   overflow-y: auto; }
  .country { margin-bottom: 14px; }
  .country:last-child { margin-bottom: 0; }
  .country-header { display: flex; align-items: center; gap: 8px;
                    font-weight: 700; padding: 6px 4px; cursor: pointer;
                    background: #11141c; border-radius: 4px;
                    margin-bottom: 6px; font-size: 13px;
                    text-transform: uppercase; letter-spacing: 0.4px;
                    color: #93c5fd; }
  .country-header:hover { color: #bfdbfe; }
  .country.collapsed .country-body { display: none; }
  .country-flag { font-size: 14px; }
  .group { margin-bottom: 10px; }
  .group:last-child { margin-bottom: 0; }
  .group-header { display: flex; align-items: center; gap: 8px;
                  font-weight: 600; padding: 4px 4px; cursor: pointer;
                  border-bottom: 1px solid #2a2f3d; margin-bottom: 4px;
                  font-size: 12px; color: #cbd5e1; }
  .group-header:hover { color: #60a5fa; }
  .group-header .toggle { font-size: 11px; color: #6b7280; }
  .group-items { padding-left: 8px; display: grid;
                 grid-template-columns: 1fr 1fr; gap: 2px 8px; }
  .group.collapsed .group-items { display: none; }
  .region-item { display: flex; align-items: center; gap: 6px;
                 font-size: 13px; padding: 3px 0; cursor: pointer;
                 user-select: none; }
  .region-item input { cursor: pointer; }
  .region-item:hover { color: #60a5fa; }
  .quick-actions { display: flex; gap: 6px; margin-bottom: 8px; }
  .quick-actions button { background: #2a2f3d; padding: 6px 10px;
                          font-size: 12px; font-weight: 500; }
  .quick-actions button:hover { background: #3a3f4d; }
  .selected-count { font-size: 12px; color: #4ade80; margin-bottom: 8px; }
  .field { margin-bottom: 12px; }
  .field label { display: block; font-size: 12px; color: #8b92a6;
                 margin-bottom: 6px; text-transform: uppercase; }
  input[type=number] { background: #1a1d27; color: #e8eaf0;
                       border: 1px solid #2a2f3d; padding: 8px;
                       border-radius: 6px; width: 80px; font-size: 14px; }
  .stats { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
  .stat { background: #1a1d27; padding: 12px; border-radius: 6px; }
  .stat .label { font-size: 11px; color: #8b92a6; text-transform: uppercase; }
  .stat .value { font-size: 24px; font-weight: 700; margin-top: 4px; }
  .log { background: #0a0c12; padding: 12px; border-radius: 6px;
         font-family: Consolas, monospace; font-size: 12px;
         max-height: 280px; overflow-y: auto; line-height: 1.6; }
  .log .line { color: #b8bdcf; }
  .log .ts { color: #6b7280; margin-right: 8px; }
  table { width: 100%; border-collapse: collapse; font-size: 13px; }
  th { text-align: left; padding: 10px; background: #1a1d27;
       color: #8b92a6; font-weight: 600; text-transform: uppercase;
       font-size: 11px; letter-spacing: 0.5px; position: sticky; top: 0; }
  td { padding: 10px; border-bottom: 1px solid #1a1d27; }
  tr:hover td { background: #161922; }
  .filter { background: #1a1d27; border: 1px solid #2a2f3d;
            color: #e8eaf0; padding: 8px 12px; border-radius: 6px;
            width: 100%; font-size: 14px; margin-bottom: 12px; }
  .by-country { display: flex; flex-wrap: wrap; gap: 8px;
                margin-bottom: 12px; }
  .country-chip { background: #11141c; border: 1px solid #2a2f3d;
                  padding: 8px 16px; border-radius: 8px; font-size: 13px;
                  font-weight: 600; cursor: pointer;
                  display: inline-flex; align-items: center; gap: 6px; }
  .country-chip:hover { background: #1a1d27; border-color: #3b82f6; }
  .country-chip.active { background: #2563eb; border-color: #2563eb;
                         color: white; }
  .country-chip .flag { font-size: 16px; }
  .by-region { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 16px; }
  .chip { background: #1a1d27; padding: 4px 10px; border-radius: 999px;
          font-size: 12px; cursor: pointer; }
  .chip:hover { background: #2a2f3d; }
  .chip.active { background: #2563eb; color: white; }
  .empty { text-align: center; padding: 40px; color: #6b7280; }
  .op-badge { padding: 2px 8px; border-radius: 4px; font-size: 11px;
              font-weight: 600; text-transform: uppercase; }
  .op-none      { background: #4a1d1d; color: #fca5a5; }
  .op-facebook  { background: #1e3a8a; color: #93c5fd; }
  .op-instagram { background: #831843; color: #f9a8d4; }
  .op-booking   { background: #1e40af; color: #bfdbfe; }
  .op-airbnb    { background: #7f1d1d; color: #fca5a5; }
  .op-tripadvisor { background: #14532d; color: #86efac; }
  .op-link-in-bio { background: #44403c; color: #d6d3d1; }
  .op-whatsapp  { background: #064e3b; color: #6ee7b7; }
  .op-other, .op-ota-aggregator { background: #422006; color: #fcd34d; }
  .action-btn { background: #1e40af; color: #bfdbfe; padding: 4px 10px;
                border-radius: 4px; font-size: 12px; font-weight: 500;
                text-decoration: none; white-space: nowrap; }
  .action-btn:hover { background: #2563eb; color: white; }
  .wa-link { color: #4ade80; text-decoration: none; font-size: 14px;
             margin-left: 4px; }
  .wa-link:hover { color: #22c55e; }
  .scraped-tick { color: #4ade80; font-size: 14px; margin-left: 4px; }
  .domain-yes { color: #4ade80; font-weight: 600; font-size: 12px; }
  .domain-no { color: #6b7280; font-size: 12px; }

  .lead-row { cursor: pointer; }
  .lead-row.selected td { background: #1e293b !important; }

  /* Side panel overlay */
  .panel-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5);
                   display: none; z-index: 100; }
  .panel-overlay.open { display: block; }
  .side-panel { position: fixed; top: 0; right: 0; bottom: 0; width: 460px;
                background: #14171f; border-left: 1px solid #2a2f3d;
                box-shadow: -4px 0 24px rgba(0,0,0,0.4); z-index: 101;
                transform: translateX(100%); transition: transform 0.25s ease;
                overflow-y: auto; }
  .side-panel.open { transform: translateX(0); }
  .panel-header { padding: 18px 20px; border-bottom: 1px solid #2a2f3d;
                  display: flex; justify-content: space-between;
                  align-items: flex-start; gap: 12px; position: sticky;
                  top: 0; background: #14171f; z-index: 1; }
  .panel-close { background: transparent; color: #8b92a6; border: 0;
                 font-size: 20px; cursor: pointer; padding: 4px 8px; }
  .panel-close:hover { color: #e8eaf0; }
  .panel-body { padding: 20px; }
  .panel-body h3 { font-size: 11px; text-transform: uppercase;
                   color: #8b92a6; letter-spacing: 0.5px; margin: 20px 0 8px; }
  .panel-body h3:first-child { margin-top: 0; }
  .panel-body .name { font-size: 20px; font-weight: 700; color: #e8eaf0;
                      margin-bottom: 4px; }
  .panel-body .meta { font-size: 13px; color: #8b92a6; }
  .panel-actions { display: grid; grid-template-columns: 1fr 1fr 1fr;
                   gap: 8px; margin: 16px 0; }
  .panel-actions a { background: #2563eb; color: white; padding: 10px;
                     border-radius: 6px; text-align: center; font-size: 13px;
                     font-weight: 600; text-decoration: none;
                     display: flex; align-items: center; justify-content: center;
                     gap: 6px; }
  .panel-actions a.wa { background: #16a34a; }
  .panel-actions a.email { background: #7c3aed; }
  .panel-actions a:hover { opacity: 0.85; }
  .info-row { display: flex; justify-content: space-between;
              padding: 8px 0; border-bottom: 1px solid #1a1d27;
              font-size: 13px; }
  .info-row:last-child { border-bottom: 0; }
  .info-row .label { color: #8b92a6; }
  .info-row .value { color: #e8eaf0; font-weight: 500; max-width: 60%;
                     text-align: right; word-break: break-word; }
  .info-row .copy-btn { background: #1a1d27; border: 1px solid #2a2f3d;
                        color: #8b92a6; padding: 2px 6px; border-radius: 4px;
                        font-size: 11px; cursor: pointer; margin-left: 6px; }
  .info-row .copy-btn:hover { color: #e8eaf0; background: #2a2f3d; }
  .talking-points { background: #1a1d27; border-radius: 8px; padding: 14px;
                    border-left: 3px solid #4ade80; }
  .talking-points li { font-size: 13px; line-height: 1.5; margin-bottom: 8px;
                       color: #e8eaf0; }
  .talking-points li:last-child { margin-bottom: 0; }
  .panel-extlink { color: #60a5fa; text-decoration: none; }
  .panel-extlink:hover { text-decoration: underline; }
</style>
</head>
<body>
<div class="top">
  <h1>📞 Lead Finder Dashboard</h1>
  <span id="status-pill" class="pill stopped">stopped</span>
  <span id="elapsed" style="color:#8b92a6;font-size:13px"></span>
  <span id="current" style="color:#4ade80;font-size:13px;margin-left:auto"></span>
</div>

<div class="container">
  <div class="sidebar">
    <h2>Controls</h2>
    <div class="field">
      <label>Concurrency</label>
      <input id="concurrency" type="number" value="2" min="1" max="4">
    </div>
    <div class="field">
      <label>Regions</label>
      <div class="quick-actions">
        <button type="button" id="btn-select-all">Select All</button>
        <button type="button" id="btn-clear">Clear</button>
      </div>
      <div class="selected-count" id="selected-count">0 selected</div>
      <div class="region-picker" id="region-picker"></div>
    </div>
    <div class="controls">
      <button id="btn-all" type="button">Scrape ALL</button>
      <button id="btn-start" type="button">Start Selected</button>
      <button id="btn-stop" type="button" class="danger">Stop</button>
    </div>

    <h2>Stats</h2>
    <div class="stats">
      <div class="stat"><div class="label">Total leads</div>
        <div class="value" id="stat-total">0</div></div>
      <div class="stat"><div class="label">Regions covered</div>
        <div class="value" id="stat-regions">0</div></div>
    </div>

    <h2>Domain Enrichment</h2>
    <div style="font-size:12px;color:#8b92a6;margin-bottom:8px">
      Checks .gr / .com availability for every lead's name.
    </div>
    <div class="controls">
      <button id="btn-enrich" type="button">Enrich Domains</button>
    </div>
    <div id="enrich-card" style="display:none; background:#1a1d27;
         padding:10px; border-radius:6px; margin-top:8px; font-size:12px">
      <div style="display:flex; justify-content:space-between;
           margin-bottom:6px">
        <span id="enrich-text">0 / 0</span>
        <span id="enrich-eta" style="color:#fbbf24"></span>
      </div>
      <div style="background:#0a0c12; height:6px; border-radius:3px;
           overflow:hidden">
        <div id="enrich-bar" style="height:100%;
             background:linear-gradient(90deg,#f59e0b,#ef4444);
             width:0%; transition:width 0.3s"></div>
      </div>
    </div>

    <h2>CRM Sync</h2>
    <div style="font-size:12px;color:#8b92a6;margin-bottom:8px">
      Pushes all leads to the CRM workspace.
      Auto-runs after every scrape and enrichment.
    </div>
    <div class="controls">
      <button id="btn-sync-crm" type="button" style="background:#16a34a;
              padding:12px 16px; font-size:14px; width:100%">
        ⬆ Push leads to CRM
      </button>
    </div>
    <div id="sync-status" style="display:none; background:#1a1d27;
         padding:10px; border-radius:6px; margin-top:8px; font-size:12px">
      <span id="sync-msg">—</span>
    </div>

    <h2>Live Log</h2>
    <div class="log" id="log"></div>
  </div>

  <div class="main">
    <div id="progress-card" style="display:none; background:#1a1d27;
         padding:14px; border-radius:8px; margin-bottom:18px;
         border:1px solid #2a2f3d">
      <div style="display:flex;justify-content:space-between;
           align-items:center;margin-bottom:8px">
        <div style="font-weight:600;color:#e8eaf0">
          🔄 <span id="prog-region">Scraping...</span>
        </div>
        <div style="font-size:13px;color:#8b92a6">
          <span id="prog-text">0 / 0</span> queries •
          ETA: <span id="prog-eta" style="color:#fbbf24">calculating...</span>
        </div>
      </div>
      <div style="background:#0a0c12;border-radius:4px;height:8px;
           overflow:hidden">
        <div id="prog-bar" style="height:100%;background:linear-gradient(90deg,#3b82f6,#8b5cf6);
             width:0%;transition:width 0.3s ease"></div>
      </div>
      <div id="prog-percent" style="font-size:11px;color:#8b92a6;
           margin-top:4px;text-align:right">0%</div>
    </div>
    <h2>Leads <span id="lead-count" style="color:#8b92a6;font-weight:400"></span></h2>
    <div class="by-country" id="country-chips"></div>
    <div class="by-region" id="region-chips"></div>
    <input id="filter" class="filter" placeholder="Filter by name, phone or category...">
    <table>
      <thead><tr>
        <th>Country</th><th>Region</th><th>Name</th><th>Category</th>
        <th>Online</th><th>Phone</th><th>Email</th><th>Domain</th><th></th>
      </tr></thead>
      <tbody id="leads-body"><tr><td colspan="9" class="empty">No leads yet</td></tr></tbody>
    </table>
  </div>
</div>

<div class="panel-overlay" id="panel-overlay"></div>
<aside class="side-panel" id="side-panel">
  <div class="panel-header">
    <div>
      <div class="name" id="sp-name">—</div>
      <div class="meta" id="sp-meta">—</div>
    </div>
    <button class="panel-close" id="sp-close">✕</button>
  </div>
  <div class="panel-body" id="sp-body"></div>
</aside>

<script>
let allLeads = [];
let activeRegion = null;
let activeCountry = null;
let filterText = '';
let selectedLeadPhone = null;

let countriesData = {};       // {countryName: {code, groups}}
let regionToCountry = {};     // region name -> country name
let scrapedStatus = {};

const COUNTRY_FLAGS = {
  'Greece': '🇬🇷', 'Netherlands': '🇳🇱',
  'Italy': '🇮🇹', 'Spain': '🇪🇸', 'Portugal': '🇵🇹',
  'France': '🇫🇷', 'Germany': '🇩🇪', 'Croatia': '🇭🇷',
  'Cyprus': '🇨🇾', 'Turkey': '🇹🇷', 'United Kingdom': '🇬🇧',
};
function flagFor(country) { return COUNTRY_FLAGS[country] || '🌍'; }

function statusIcon(name) {
  const s = scrapedStatus[name];
  if (!s) return '';
  if (s.status === 'done') {
    return `<span class="scraped-tick" title="Done: ${s.leads_count} leads">✅</span>`;
  }
  if (s.status === 'partial') {
    return `<span class="scraped-tick" style="color:#fbbf24" title="Partial: ${s.leads_count} leads, ${s.scraped_villages}/${s.village_count} villages">🔄</span>`;
  }
  return '';
}

async function loadRegions() {
  const r = await fetch('/api/regions');
  const data = await r.json();
  countriesData = data.countries || {};
  scrapedStatus = data.scraped || {};

  // Build region->country map for client-side filtering
  regionToCountry = {};
  for (const [cName, cData] of Object.entries(countriesData)) {
    for (const regions of Object.values(cData.groups)) {
      for (const r of regions) regionToCountry[r] = cName;
    }
  }

  const picker = document.getElementById('region-picker');
  picker.innerHTML = Object.entries(countriesData).map(([cName, cData]) => {
    const allRegions = Object.values(cData.groups).flat();
    const doneCount = allRegions.filter(n =>
      scrapedStatus[n] && scrapedStatus[n].status === 'done').length;
    const cSuffix = doneCount > 0 ?
      ` <span style="color:#4ade80;font-size:11px">(${doneCount}/${allRegions.length} ✅)</span>` : '';
    const groupsHtml = Object.entries(cData.groups).map(
      ([groupName, items]) => {
        const groupDoneCount = items.filter(n =>
          scrapedStatus[n] && scrapedStatus[n].status === 'done').length;
        const groupSuffix = groupDoneCount > 0 ?
          ` <span style="color:#4ade80;font-size:11px">(${groupDoneCount}/${items.length} ✅)</span>` : '';
        return `
        <div class="group" data-group="${groupName}">
          <div class="group-header">
            <input type="checkbox" class="group-check" data-group="${groupName}">
            <span style="flex:1">${groupName} (${items.length})${groupSuffix}</span>
            <span class="toggle">▼</span>
          </div>
          <div class="group-items">
            ${items.map(name => `
              <label class="region-item">
                <input type="checkbox" class="region-check" value="${name}" data-country="${cName}">
                <span>${name}${statusIcon(name)}</span>
              </label>`).join('')}
          </div>
        </div>`;
      }).join('');
    return `
      <div class="country" data-country="${cName}">
        <div class="country-header">
          <input type="checkbox" class="country-check" data-country="${cName}">
          <span class="country-flag">${flagFor(cName)}</span>
          <span style="flex:1">${cName}${cSuffix}</span>
          <span class="toggle">▼</span>
        </div>
        <div class="country-body">${groupsHtml}</div>
      </div>`;
  }).join('');

  // Country header collapse/expand (click on the name, not the checkbox)
  for (const h of picker.querySelectorAll('.country-header')) {
    h.querySelectorAll('span:not(.country-flag)').forEach(s => {
      s.onclick = (e) => {
        e.stopPropagation();
        h.parentElement.classList.toggle('collapsed');
        const t = h.querySelector('.toggle');
        t.textContent = h.parentElement.classList.contains('collapsed') ? '▶' : '▼';
      };
    });
  }

  // Country checkbox: toggle every region in that country
  for (const cb of picker.querySelectorAll('.country-check')) {
    cb.onchange = (e) => {
      e.stopPropagation();
      const cName = e.target.dataset.country;
      const items = picker.querySelectorAll(
        `.country[data-country="${cName}"] .region-check`);
      for (const it of items) it.checked = e.target.checked;
      updateSelectedCount();
    };
  }

  // Group toggle (collapse/expand on header label click, not checkbox)
  for (const h of picker.querySelectorAll('.group-header')) {
    h.querySelector('span').onclick = (e) => {
      e.stopPropagation();
      h.parentElement.classList.toggle('collapsed');
      const t = h.querySelector('.toggle');
      t.textContent = h.parentElement.classList.contains('collapsed') ? '▶' : '▼';
    };
  }

  // Group checkbox: toggle all items in group
  for (const cb of picker.querySelectorAll('.group-check')) {
    cb.onchange = (e) => {
      const grp = e.target.dataset.group;
      const items = picker.querySelectorAll(
        `.group[data-group="${grp}"] .region-check`);
      for (const it of items) it.checked = e.target.checked;
      updateSelectedCount();
    };
  }

  // Individual region checkbox: update group state and counter
  for (const cb of picker.querySelectorAll('.region-check')) {
    cb.onchange = updateSelectedCount;
  }
  updateSelectedCount();
}

function getSelectedRegions() {
  return Array.from(document.querySelectorAll('.region-check:checked'))
    .map(c => c.value);
}

function updateSelectedCount() {
  const n = getSelectedRegions().length;
  document.getElementById('selected-count').textContent = `${n} selected`;
  // Update group checkbox indeterminate state
  for (const groupCb of document.querySelectorAll('.group-check')) {
    const grp = groupCb.dataset.group;
    const items = document.querySelectorAll(
      `.group[data-group="${grp}"] .region-check`);
    const checked = Array.from(items).filter(i => i.checked).length;
    groupCb.checked = checked === items.length && items.length > 0;
    groupCb.indeterminate = checked > 0 && checked < items.length;
  }
  // Update country checkbox indeterminate state
  for (const cCb of document.querySelectorAll('.country-check')) {
    const cName = cCb.dataset.country;
    const items = document.querySelectorAll(
      `.country[data-country="${cName}"] .region-check`);
    const checked = Array.from(items).filter(i => i.checked).length;
    cCb.checked = checked === items.length && items.length > 0;
    cCb.indeterminate = checked > 0 && checked < items.length;
  }
}

document.getElementById('btn-select-all').onclick = () => {
  for (const cb of document.querySelectorAll('.region-check'))
    cb.checked = true;
  updateSelectedCount();
};
document.getElementById('btn-clear').onclick = () => {
  for (const cb of document.querySelectorAll('.region-check'))
    cb.checked = false;
  updateSelectedCount();
};

async function refreshStatus() {
  const r = await fetch('/api/status');
  const s = await r.json();
  const pill = document.getElementById('status-pill');
  pill.className = 'pill ' + (s.running ? 'running' : 'stopped');
  pill.textContent = s.running ? 'running' : 'stopped';
  document.getElementById('elapsed').textContent =
    s.running && s.elapsed ? `${Math.floor(s.elapsed/60)}m ${Math.floor(s.elapsed%60)}s elapsed` : '';
  document.getElementById('current').textContent =
    s.current_region ? `► ${s.current_region}` : '';
  document.getElementById('btn-start').disabled = s.running;
  document.getElementById('btn-all').disabled = s.running;
  document.getElementById('btn-stop').disabled = !s.running;
  const log = document.getElementById('log');
  const wasAtBottom = log.scrollTop + log.clientHeight >= log.scrollHeight - 30;
  log.innerHTML = s.log.map(e =>
    `<div class="line"><span class="ts">${e.t}</span>${escapeHtml(e.line)}</div>`).join('');
  if (wasAtBottom) log.scrollTop = log.scrollHeight;
}

async function refreshLeads() {
  const r = await fetch('/api/leads');
  const data = await r.json();
  allLeads = data.leads;
  document.getElementById('stat-total').textContent = data.total;
  document.getElementById('stat-regions').textContent = data.by_region.length;

  // Country chips (Greece / Netherlands / ...). "All" shows everything.
  const cChips = document.getElementById('country-chips');
  const byCountry = data.by_country || [];
  cChips.innerHTML =
    `<div class="country-chip ${!activeCountry?'active':''}" data-c="">
       <span class="flag">🌍</span>All countries (${data.total})
     </div>` +
    byCountry.map(c =>
      `<div class="country-chip ${activeCountry===c.country?'active':''}" data-c="${escapeHtml(c.country)}">
         <span class="flag">${flagFor(c.country)}</span>${escapeHtml(c.country)} (${c.count})
       </div>`).join('');
  for (const ch of cChips.querySelectorAll('.country-chip')) {
    ch.onclick = () => {
      activeCountry = ch.dataset.c || null;
      // Reset region filter when country switches (region may not belong)
      if (activeRegion && regionToCountry[activeRegion] !== activeCountry
          && activeCountry) {
        activeRegion = null;
      }
      refreshLeads();
    };
  }

  // Region chips — narrowed to the active country if one is set
  const visibleRegions = activeCountry
    ? data.by_region.filter(r => {
        const c = regionToCountry[r.region]
                  || (allLeads.find(l => l.region === r.region) || {}).country;
        return c === activeCountry;
      })
    : data.by_region;
  const visibleTotal = visibleRegions.reduce((s, r) => s + r.count, 0);
  const chips = document.getElementById('region-chips');
  chips.innerHTML = `<div class="chip ${!activeRegion?'active':''}" data-r="">All (${visibleTotal})</div>` +
    visibleRegions.map(r =>
      `<div class="chip ${activeRegion===r.region?'active':''}" data-r="${escapeHtml(r.region)}">${escapeHtml(r.region)} (${r.count})</div>`).join('');
  for (const c of chips.querySelectorAll('.chip')) {
    c.onclick = () => { activeRegion = c.dataset.r || null; renderLeads(); };
  }
  renderLeads();
}

function renderLeads() {
  let rows = allLeads;
  if (activeCountry) {
    rows = rows.filter(l =>
      (l.country || regionToCountry[l.region] || '') === activeCountry);
  }
  if (activeRegion) rows = rows.filter(l => l.region === activeRegion);
  if (filterText) {
    const f = filterText.toLowerCase();
    rows = rows.filter(l =>
      (l.name||'').toLowerCase().includes(f) ||
      (l.phone||'').includes(f) ||
      (l.category||'').toLowerCase().includes(f) ||
      (l.email||'').toLowerCase().includes(f));
  }
  document.getElementById('lead-count').textContent = `(${rows.length} shown)`;
  const tbody = document.getElementById('leads-body');
  if (!rows.length) {
    tbody.innerHTML = '<tr><td colspan="9" class="empty">No leads match</td></tr>';
    return;
  }
  tbody.innerHTML = rows.map(l => {
    const op = (l.online_presence||'').toLowerCase();
    const opBadge = op && op !== 'none' ?
      `<span class="op-badge op-${op}">${escapeHtml(op)}</span>` :
      `<span class="op-badge op-none">none</span>`;
    const mapsBtn = l.gmaps_url ?
      `<a href="${escapeHtml(l.gmaps_url)}" target="_blank" class="action-btn">📍 Maps</a>` : '';
    const phone = escapeHtml(l.phone||'');
    const waLink = phone ?
      `<a href="https://wa.me/${phone.replace('+','')}" target="_blank" class="wa-link" title="WhatsApp">💬</a>` : '';
    let domainCell = '';
    const grA = l.domain_gr_available;
    const comA = l.domain_com_available;
    if (grA || comA) {
      const sug = l.domain_suggestion;
      if (sug) {
        domainCell = `<span class="domain-yes">✓ ${escapeHtml(sug)}</span>`;
      } else if (grA === 'no' && comA === 'no') {
        domainCell = `<span class="domain-no">✗ taken</span>`;
      }
    } else {
      domainCell = '<span style="color:#6b7280">—</span>';
    }
    const country = l.country || regionToCountry[l.region] || '';
    const countryCell = country
      ? `<span title="${escapeHtml(country)}">${flagFor(country)}</span>`
      : '<span style="color:#6b7280">—</span>';
    const rowClass = phone === selectedLeadPhone ? 'lead-row selected' : 'lead-row';
    return `<tr class="${rowClass}" data-phone="${phone}">
       <td>${countryCell}</td>
       <td>${escapeHtml(l.region||'')}</td>
       <td><b>${escapeHtml(l.name||'')}</b></td>
       <td>${escapeHtml(l.category||'')}</td>
       <td>${opBadge}</td>
       <td><a href="tel:${phone}" style="color:#60a5fa" onclick="event.stopPropagation()">${phone}</a> ${waLink}</td>
       <td>${escapeHtml(l.email||'')}</td>
       <td>${domainCell}</td>
       <td>${mapsBtn}</td></tr>`;
  }).join('');
  // Wire up row clicks
  for (const tr of tbody.querySelectorAll('tr.lead-row')) {
    tr.onclick = (e) => {
      // Don't open panel if clicking a link/button inside
      if (e.target.tagName === 'A' || e.target.tagName === 'BUTTON') return;
      openLeadPanel(tr.dataset.phone);
    };
  }
}

async function openLeadPanel(phone) {
  selectedLeadPhone = phone;
  renderLeads(); // re-highlight
  const overlay = document.getElementById('panel-overlay');
  const panel = document.getElementById('side-panel');
  overlay.classList.add('open');
  panel.classList.add('open');
  document.getElementById('sp-name').textContent = 'Loading...';
  document.getElementById('sp-meta').textContent = '';
  document.getElementById('sp-body').innerHTML = '';

  try {
    const r = await fetch(`/api/lead/${encodeURIComponent(phone)}`);
    const data = await r.json();
    if (data.error) {
      document.getElementById('sp-body').innerHTML =
        `<div style="color:#fca5a5">Lead not found</div>`;
      return;
    }
    renderLeadDetail(data.lead, data.talking_points || []);
  } catch (e) {
    document.getElementById('sp-body').innerHTML =
      `<div style="color:#fca5a5">Error: ${escapeHtml(String(e))}</div>`;
  }
}

function closeLeadPanel() {
  document.getElementById('panel-overlay').classList.remove('open');
  document.getElementById('side-panel').classList.remove('open');
  selectedLeadPhone = null;
  renderLeads();
}

document.getElementById('sp-close').onclick = closeLeadPanel;
document.getElementById('panel-overlay').onclick = closeLeadPanel;
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') closeLeadPanel();
});

function renderLeadDetail(l, talkingPoints) {
  document.getElementById('sp-name').textContent = l.name || '—';
  document.getElementById('sp-meta').textContent =
    [l.region, l.category].filter(Boolean).join(' • ');

  const phone = (l.phone || '').replace(/[^\\d+]/g, '');
  const waPhone = phone.replace('+','').replace(/^00/,'');
  const email = l.email || '';
  const gmaps = l.gmaps_url || '';
  const op = (l.online_presence || '').toLowerCase();
  const sug = l.domain_suggestion || '';
  const grA = l.domain_gr_available;
  const comA = l.domain_com_available;

  let domainBlock = '';
  if (grA || comA) {
    const grLabel = grA === 'yes' ? '<span class="domain-yes">✓ available</span>' :
                    grA === 'no' ? '<span class="domain-no">✗ taken</span>' :
                    '<span class="domain-no">' + escapeHtml(grA||'—') + '</span>';
    const comLabel = comA === 'yes' ? '<span class="domain-yes">✓ available</span>' :
                     comA === 'no' ? '<span class="domain-no">✗ taken</span>' :
                     '<span class="domain-no">' + escapeHtml(comA||'—') + '</span>';
    domainBlock = `
      <h3>Domain Availability</h3>
      <div class="info-row"><span class="label">.gr</span>
        <span class="value">${grLabel}</span></div>
      <div class="info-row"><span class="label">.com</span>
        <span class="value">${comLabel}</span></div>
      ${sug ? `<div class="info-row"><span class="label">Suggested</span>
        <span class="value"><b>${escapeHtml(sug)}</b>
          <button class="copy-btn" onclick="copyToClip('${escapeHtml(sug)}', this)">copy</button>
        </span></div>` : ''}`;
  } else {
    domainBlock = `<h3>Domain Availability</h3>
      <div style="color:#6b7280;font-size:13px">
        Not checked yet. Click "Enrich Domains" in the sidebar.
      </div>`;
  }

  const actions = `
    <div class="panel-actions">
      ${phone ? `<a href="tel:${phone}">📞 Call</a>` :
                '<a style="opacity:0.4;cursor:not-allowed">📞 Call</a>'}
      ${waPhone ? `<a class="wa" href="https://wa.me/${waPhone}" target="_blank">💬 WA</a>` :
                  '<a class="wa" style="opacity:0.4;cursor:not-allowed">💬 WA</a>'}
      ${email ? `<a class="email" href="mailto:${email}">✉️ Email</a>` :
                '<a class="email" style="opacity:0.4;cursor:not-allowed">✉️ Email</a>'}
    </div>`;

  const tpBlock = talkingPoints.length ?
    `<ul class="talking-points">
       ${talkingPoints.map(t => `<li>${escapeHtml(t)}</li>`).join('')}
     </ul>` :
    `<div style="color:#6b7280;font-size:13px">No specific talking points generated.</div>`;

  document.getElementById('sp-body').innerHTML = `
    ${actions}
    <h3>Contact</h3>
    <div class="info-row"><span class="label">Phone</span>
      <span class="value">${escapeHtml(phone || '—')}
        ${phone ? `<button class="copy-btn" onclick="copyToClip('${phone}', this)">copy</button>` : ''}
      </span></div>
    <div class="info-row"><span class="label">Email</span>
      <span class="value">${escapeHtml(email || '—')}
        ${email ? `<button class="copy-btn" onclick="copyToClip('${email}', this)">copy</button>` : ''}
      </span></div>
    <div class="info-row"><span class="label">Region</span>
      <span class="value">${escapeHtml(l.region || '—')}</span></div>
    <div class="info-row"><span class="label">Category</span>
      <span class="value">${escapeHtml(l.category || '—')}</span></div>

    <h3>Online Presence</h3>
    <div class="info-row"><span class="label">Status</span>
      <span class="value">
        <span class="op-badge op-${op || 'none'}">${escapeHtml(op || 'none')}</span>
      </span></div>
    ${gmaps ? `<div class="info-row"><span class="label">Google Maps</span>
      <span class="value"><a class="panel-extlink" href="${escapeHtml(gmaps)}" target="_blank">View listing →</a></span></div>` : ''}

    ${domainBlock}

    <h3>Sales Talking Points</h3>
    ${tpBlock}
  `;
}

function copyToClip(text, btn) {
  navigator.clipboard.writeText(text).then(() => {
    const old = btn.textContent;
    btn.textContent = '✓ copied';
    setTimeout(() => btn.textContent = old, 1200);
  });
}
window.copyToClip = copyToClip;

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, c =>
    ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}

document.getElementById('filter').oninput = e => {
  filterText = e.target.value;
  renderLeads();
};

document.getElementById('btn-all').onclick = async () => {
  if (!confirm('Scrape ALL 74 regions? This takes ~3-4 hours.')) return;
  await startScrape(['__all__']);
};

document.getElementById('btn-start').onclick = async () => {
  const regions = getSelectedRegions();
  if (!regions.length) { alert('Select at least one region.'); return; }
  await startScrape(regions);
};

document.getElementById('btn-stop').onclick = async () => {
  await fetch('/api/stop', {method: 'POST'});
};

document.getElementById('btn-enrich').onclick = async () => {
  await fetch('/api/enrich', {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({force: false}),
  });
};

document.getElementById('btn-sync-crm').onclick = async () => {
  await fetch('/api/sync_crm', { method: 'POST' });
};

async function refreshSyncCrm() {
  const r = await fetch('/api/sync_crm/status');
  const s = await r.json();
  const card = document.getElementById('sync-status');
  const btn = document.getElementById('btn-sync-crm');
  if (s.running) {
    card.style.display = 'block';
    btn.disabled = true;
    document.getElementById('sync-msg').textContent = s.msg || 'Working...';
  } else {
    btn.disabled = false;
    if (s.msg) {
      card.style.display = 'block';
      document.getElementById('sync-msg').textContent = s.msg;
    } else {
      card.style.display = 'none';
    }
  }
}

async function refreshEnrich() {
  const r = await fetch('/api/enrich/status');
  const s = await r.json();
  const card = document.getElementById('enrich-card');
  const btn = document.getElementById('btn-enrich');
  if (s.running) {
    card.style.display = 'block';
    btn.disabled = true;
    const pct = Math.round(s.percent || 0);
    document.getElementById('enrich-bar').style.width = pct + '%';
    document.getElementById('enrich-text').textContent =
      `${s.done} / ${s.total} (${pct}%)`;
    const eta = s.eta || 0;
    document.getElementById('enrich-eta').textContent =
      eta < 60 ? `${Math.round(eta)}s left` : `${Math.round(eta/60)}m left`;
  } else {
    btn.disabled = false;
    if (s.total && s.done >= s.total) {
      card.style.display = 'block';
      document.getElementById('enrich-bar').style.width = '100%';
      document.getElementById('enrich-text').textContent =
        `Done: ${s.done} / ${s.total}`;
      document.getElementById('enrich-eta').textContent = '✅';
      // Auto-refresh leads to show new columns
      refreshLeads();
    } else {
      card.style.display = 'none';
    }
  }
}

async function startScrape(regions) {
  const concurrency = +document.getElementById('concurrency').value;
  await fetch('/api/start', {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({regions, concurrency}),
  });
}

async function refreshProgress() {
  const [pr, sr] = await Promise.all([
    fetch('/api/progress'), fetch('/api/status'),
  ]);
  const p = await pr.json();
  const s = await sr.json();
  const card = document.getElementById('progress-card');

  // Show a "starting up" placeholder when the scraper is running but
  // progress.json hasn't been written yet (or is the stale `completed`
  // marker from a previous run).
  if (s.running && (!p || !p.queries_total || p.completed)) {
    card.style.display = 'block';
    document.getElementById('prog-bar').style.width = '5%';
    document.getElementById('prog-percent').textContent = 'warming up';
    document.getElementById('prog-text').textContent = 'starting...';
    document.getElementById('prog-region').textContent = 'Initializing Playwright...';
    document.getElementById('prog-eta').textContent = '—';
    return;
  }
  if (!p || !p.queries_total || p.completed) {
    card.style.display = 'none';
    return;
  }
  card.style.display = 'block';
  const pct = Math.round(p.percent || 0);
  document.getElementById('prog-bar').style.width = pct + '%';
  document.getElementById('prog-percent').textContent = pct + '%';
  document.getElementById('prog-text').textContent =
    `${p.queries_done || 0} / ${p.queries_total}`;
  // Find currently active region(s)
  const activeRegions = Object.entries(p.regions || {})
    .filter(([_, r]) => r.started && r.done < r.total)
    .map(([name, r]) => `${name} (${r.done}/${r.total})`);
  document.getElementById('prog-region').textContent =
    activeRegions.length ? activeRegions.join(' • ') : 'Initializing...';
  const eta = p.eta_seconds || 0;
  document.getElementById('prog-eta').textContent =
    eta < 60 ? `${Math.round(eta)}s` :
    eta < 3600 ? `${Math.round(eta/60)} min` :
    `${(eta/3600).toFixed(1)} h`;
}

loadRegions();
refreshStatus();
refreshLeads();
refreshProgress();
setInterval(refreshStatus, 1500);
setInterval(refreshLeads, 5000);
setInterval(refreshProgress, 2000);
setInterval(refreshEnrich, 1500);
setInterval(refreshSyncCrm, 2000);
// Refresh region list after scraping completes (to update checkmarks)
let wasRunning = false;
setInterval(async () => {
  const r = await fetch('/api/status');
  const s = await r.json();
  if (wasRunning && !s.running) loadRegions();
  wasRunning = s.running;
}, 3000);
</script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(INDEX_HTML)


if __name__ == "__main__":
    print("Lead Finder Dashboard running at http://localhost:5000")
    app.run(host="127.0.0.1", port=5000, debug=False, threaded=True)
