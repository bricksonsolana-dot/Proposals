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

from regions import REGIONS, REGION_GROUPS

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
    return jsonify({
        "groups": REGION_GROUPS,
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
    by_region = {}
    for l in leads:
        by_region.setdefault(l.get("region", ""), []).append(l)
    return jsonify({
        "total": len(leads),
        "by_region": [{"region": r, "count": len(rows)}
                       for r, rows in sorted(by_region.items())],
        "leads": leads,
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
                   border-radius: 6px; padding: 8px; max-height: 380px;
                   overflow-y: auto; }
  .group { margin-bottom: 12px; }
  .group:last-child { margin-bottom: 0; }
  .group-header { display: flex; align-items: center; gap: 8px;
                  font-weight: 600; padding: 6px 4px; cursor: pointer;
                  border-bottom: 1px solid #2a2f3d; margin-bottom: 4px; }
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
    <div class="by-region" id="region-chips"></div>
    <input id="filter" class="filter" placeholder="Filter by name, phone or category...">
    <table>
      <thead><tr>
        <th>Region</th><th>Name</th><th>Category</th><th>Online</th>
        <th>Phone</th><th>Email</th><th></th>
      </tr></thead>
      <tbody id="leads-body"><tr><td colspan="7" class="empty">No leads yet</td></tr></tbody>
    </table>
  </div>
</div>

<script>
let allLeads = [];
let activeRegion = null;
let filterText = '';

let regionGroups = {};
let scrapedStatus = {};

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
  regionGroups = data.groups;
  scrapedStatus = data.scraped || {};
  const picker = document.getElementById('region-picker');
  picker.innerHTML = Object.entries(regionGroups).map(([groupName, items]) => {
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
            <input type="checkbox" class="region-check" value="${name}">
            <span>${name}${statusIcon(name)}</span>
          </label>`).join('')}
      </div>
    </div>`;}).join('');

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
  const chips = document.getElementById('region-chips');
  chips.innerHTML = `<div class="chip ${!activeRegion?'active':''}" data-r="">All (${data.total})</div>` +
    data.by_region.map(r =>
      `<div class="chip ${activeRegion===r.region?'active':''}" data-r="${r.region}">${r.region} (${r.count})</div>`).join('');
  for (const c of chips.querySelectorAll('.chip')) {
    c.onclick = () => { activeRegion = c.dataset.r || null; renderLeads(); refreshLeads(); };
  }
  renderLeads();
}

function renderLeads() {
  let rows = allLeads;
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
    tbody.innerHTML = '<tr><td colspan="5" class="empty">No leads match</td></tr>';
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
    return `<tr><td>${escapeHtml(l.region||'')}</td>
       <td><b>${escapeHtml(l.name||'')}</b></td>
       <td>${escapeHtml(l.category||'')}</td>
       <td>${opBadge}</td>
       <td><a href="tel:${phone}" style="color:#60a5fa">${phone}</a> ${waLink}</td>
       <td>${escapeHtml(l.email||'')}</td>
       <td>${mapsBtn}</td></tr>`;
  }).join('');
}

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

async function startScrape(regions) {
  const concurrency = +document.getElementById('concurrency').value;
  await fetch('/api/start', {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({regions, concurrency}),
  });
}

async function refreshProgress() {
  const r = await fetch('/api/progress');
  const p = await r.json();
  const card = document.getElementById('progress-card');
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
