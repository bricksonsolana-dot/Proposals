"""
CRM workspace for the sales team.
Run with: python app.py
"""
import json
import os
import secrets
import time
from datetime import date, datetime, timedelta
from pathlib import Path
from queue import Queue, Empty

# Load .env if present, before any other module reads env vars
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent / ".env")
except ImportError:
    pass

from flask import (Flask, jsonify, redirect, render_template_string,
                     request, session, g, Response, stream_with_context)

import db
import auth
from ui import INDEX_HTML

ROOT = Path(__file__).parent
SECRET_FILE = ROOT / "data" / ".secret_key"


def _load_or_create_secret() -> str:
    env = os.environ.get("SECRET_KEY")
    if env:
        return env
    SECRET_FILE.parent.mkdir(parents=True, exist_ok=True)
    if SECRET_FILE.exists():
        return SECRET_FILE.read_text().strip()
    new_secret = secrets.token_hex(32)
    SECRET_FILE.write_text(new_secret)
    return new_secret


app = Flask(__name__)
app.secret_key = _load_or_create_secret()
app.permanent_session_lifetime = timedelta(days=30)

# Ensure DB schema exists
db.init_schema()
auth.seed_admin_if_empty()


# ---------- SSE event broadcasting ----------

_subscribers: list[Queue] = []
_subscribers_lock = __import__("threading").Lock()


def broadcast(event: dict):
    """Push an event to all connected SSE clients."""
    payload = f"data: {json.dumps(event)}\n\n"
    with _subscribers_lock:
        dead = []
        for q in _subscribers:
            try:
                q.put_nowait(payload)
            except Exception:
                dead.append(q)
        for q in dead:
            _subscribers.remove(q)


@app.route("/events")
@auth.login_required
def events():
    q = Queue()
    with _subscribers_lock:
        _subscribers.append(q)

    def stream():
        try:
            yield "data: {\"type\":\"connected\"}\n\n"
            while True:
                try:
                    item = q.get(timeout=20)
                    yield item
                except Empty:
                    yield ": keepalive\n\n"
        finally:
            with _subscribers_lock:
                if q in _subscribers:
                    _subscribers.remove(q)

    return Response(stream_with_context(stream()),
                     mimetype="text/event-stream",
                     headers={"Cache-Control": "no-cache",
                              "X-Accel-Buffering": "no"})


# ---------- Auth routes ----------

LOGIN_HTML = """<!doctype html>
<html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
<title>Login - CRM</title>
<style>
body { font-family: -apple-system, Segoe UI, sans-serif; background: #0f1117;
       color: #e8eaf0; margin: 0; min-height: 100vh; display: flex;
       align-items: center; justify-content: center; padding: 16px; }
.box { background: #1a1d27; padding: 32px; border-radius: 12px;
       width: 100%; max-width: 360px; border: 1px solid #2a2f3d; }
input { font-size: 16px !important; }
.logo { display: flex; align-items: center; justify-content: center;
        margin-bottom: 20px; }
.logo img { height: 56px; width: auto;
            filter: brightness(0) invert(1); }
h1 { font-size: 18px; margin: 0 0 24px; text-align: center;
     color: #8b92a6; font-weight: 500; letter-spacing: 0.5px; }
label { display: block; font-size: 12px; color: #8b92a6; margin-bottom: 6px;
        text-transform: uppercase; letter-spacing: 0.5px; }
input { width: 100%; padding: 10px 12px; background: #0a0c12; color: #e8eaf0;
        border: 1px solid #2a2f3d; border-radius: 6px; font-size: 14px;
        margin-bottom: 16px; box-sizing: border-box; }
button { width: 100%; padding: 12px; background: #2563eb; color: white;
         border: 0; border-radius: 6px; font-weight: 600; cursor: pointer;
         font-size: 14px; }
button:hover { background: #1d4ed8; }
.err { color: #fca5a5; font-size: 13px; margin-top: 8px; }
.hint { color: #6b7280; font-size: 11px; margin-top: 16px; text-align: center; }
</style></head>
<body>
<form class="box" method="POST">
  <div class="logo"><img src="/static/logo.png" alt="Devox"></div>
  <h1>CRM Workspace</h1>
  <label>Username</label>
  <input name="username" autofocus required>
  <label>Password</label>
  <input name="password" type="password" required>
  <button type="submit">Sign In</button>
  {% if error %}<div class="err">{{ error }}</div>{% endif %}
</form>
</body></html>"""


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""
        user = auth.authenticate(username, password)
        if user:
            auth.login_user(user)
            return redirect("/")
        error = "Invalid username or password"
    return render_template_string(LOGIN_HTML, error=error)


@app.route("/logout")
def logout():
    auth.logout_user()
    return redirect("/login")


# ---------- Lead state helpers ----------

def get_or_create_state(phone: str) -> dict:
    state = db.query_one(
        "SELECT * FROM lead_state WHERE lead_phone = ?", (phone,))
    if not state:
        db.execute(
            "INSERT INTO lead_state (lead_phone, status) VALUES (?, 'new')",
            (phone,))
        state = db.query_one(
            "SELECT * FROM lead_state WHERE lead_phone = ?", (phone,))
    return state


def log_activity(lead_phone: str, user_id: int, action: str,
                  details: str = ""):
    db.execute(
        """INSERT INTO activity (lead_phone, user_id, action, details)
           VALUES (?, ?, ?, ?)""",
        (lead_phone, user_id, action, details),
    )
    user = db.query_one("SELECT username, full_name FROM users WHERE id = ?",
                          (user_id,))
    lead = db.query_one("SELECT name, region FROM leads WHERE phone = ?",
                          (lead_phone,))
    broadcast({
        "type": "activity",
        "lead_phone": lead_phone,
        "lead_name": lead["name"] if lead else "",
        "lead_region": lead["region"] if lead else "",
        "user_id": user_id,
        "username": user["username"] if user else "",
        "full_name": user["full_name"] if user else "",
        "action": action,
        "details": details,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    })


# ---------- API: Leads ----------

@app.route("/api/leads")
@auth.login_required
def api_leads():
    """Return leads + their state, optionally filtered."""
    user = g.user
    args = request.args

    where = []
    params = [user["id"]]  # for the favorites JOIN

    if args.get("mine") == "1":
        where.append("ls.assigned_to = ?")
        params.append(user["id"])

    if args.get("my_regions") == "1":
        my_regions = get_user_regions(user["id"])
        if my_regions:
            placeholders = ",".join("?" * len(my_regions))
            where.append(f"l.region IN ({placeholders})")
            params.extend(my_regions)
        else:
            # User has no regions assigned -> return zero leads
            where.append("1 = 0")

    if args.get("favorites") == "1":
        where.append("f.user_id IS NOT NULL")

    status = args.get("status")
    if status:
        where.append("ls.status = ?")
        params.append(status)

    region = args.get("region")
    if region:
        where.append("l.region = ?")
        params.append(region)

    assigned = args.get("assigned_to")
    if assigned:
        if assigned == "unassigned":
            where.append("ls.assigned_to IS NULL")
        else:
            where.append("ls.assigned_to = ?")
            params.append(int(assigned))

    search = (args.get("q") or "").strip()
    if search:
        where.append(
            "(LOWER(l.name) LIKE ? OR l.phone LIKE ? OR LOWER(l.region) LIKE ? "
            "OR LOWER(l.category) LIKE ? OR LOWER(l.email) LIKE ?)")
        like = "%" + search.lower() + "%"
        params.extend([like, like, like, like, like])

    where_sql = ("WHERE " + " AND ".join(where)) if where else ""
    sql = f"""
        SELECT l.*, ls.status, ls.assigned_to, ls.follow_up_date,
                ls.last_contact_at,
                u.full_name AS assigned_to_name,
                CASE WHEN f.user_id IS NOT NULL THEN 1 ELSE 0 END AS is_favorite
        FROM leads l
        LEFT JOIN lead_state ls ON ls.lead_phone = l.phone
        LEFT JOIN users u ON u.id = ls.assigned_to
        LEFT JOIN favorites f ON f.lead_phone = l.phone AND f.user_id = ?
        {where_sql}
        ORDER BY l.region, l.name
        LIMIT 5000
    """
    leads = db.query(sql, tuple(params))

    # Add property count
    for l in leads:
        props = l.get("properties")
        if props:
            try:
                l["property_count"] = len(json.loads(props))
            except Exception:
                l["property_count"] = 1
        else:
            l["property_count"] = 1

    # Summaries
    by_status = {}
    by_region = {}
    for l in leads:
        s = l.get("status") or "new"
        by_status[s] = by_status.get(s, 0) + 1
        r = l.get("region") or ""
        by_region[r] = by_region.get(r, 0) + 1

    return jsonify({
        "total": len(leads),
        "by_status": by_status,
        "by_region": [{"region": r, "count": c}
                       for r, c in sorted(by_region.items())],
        "leads": leads,
    })


@app.route("/api/lead/<phone>")
@auth.login_required
def api_lead_detail(phone):
    import re
    norm = re.sub(r"[^\d+]", "", phone)
    lead = db.query_one("""
        SELECT l.*, ls.status, ls.assigned_to, ls.follow_up_date,
                ls.last_contact_at, u.full_name AS assigned_to_name,
                CASE WHEN f.user_id IS NOT NULL THEN 1 ELSE 0 END AS is_favorite
        FROM leads l
        LEFT JOIN lead_state ls ON ls.lead_phone = l.phone
        LEFT JOIN users u ON u.id = ls.assigned_to
        LEFT JOIN favorites f ON f.lead_phone = l.phone AND f.user_id = ?
        WHERE l.phone = ?
    """, (g.user["id"], norm))
    if not lead:
        return jsonify({"error": "not found"}), 404

    activity = db.query("""
        SELECT a.id, a.lead_phone, a.user_id, a.action, a.details,
                a.created_at, u.full_name, u.username
        FROM activity a
        LEFT JOIN users u ON u.id = a.user_id
        WHERE a.lead_phone = ?
        ORDER BY a.created_at DESC
        LIMIT 100
    """, (norm,))

    # Parse properties JSON if present
    props_raw = lead.get("properties")
    if props_raw:
        try:
            lead["properties_list"] = json.loads(props_raw)
        except Exception:
            lead["properties_list"] = []
    else:
        lead["properties_list"] = []

    return jsonify({"lead": lead, "activity": activity})


@app.route("/api/lead/<phone>/status", methods=["POST"])
@auth.login_required
def api_set_status(phone):
    import re
    norm = re.sub(r"[^\d+]", "", phone)
    data = request.get_json(force=True) or {}
    new_status = (data.get("status") or "").strip()
    valid = ["new", "called", "reached", "interested", "not_interested",
              "follow_up", "closed_won", "closed_lost", "disqualified"]
    if new_status not in valid:
        return jsonify({"error": "invalid status"}), 400

    state = get_or_create_state(norm)
    old_status = state.get("status") if state else "new"

    follow_up = data.get("follow_up_date") or None
    db.execute(
        """UPDATE lead_state
           SET status = ?, follow_up_date = ?,
               last_contact_at = CURRENT_TIMESTAMP,
               updated_at = CURRENT_TIMESTAMP
           WHERE lead_phone = ?""",
        (new_status, follow_up, norm),
    )
    log_activity(norm, g.user["id"], "status_change",
                  f"{old_status} → {new_status}"
                  + (f" (follow up: {follow_up})" if follow_up else ""))
    return jsonify({"ok": True})


@app.route("/api/lead/<phone>/note", methods=["POST"])
@auth.login_required
def api_add_note(phone):
    import re
    norm = re.sub(r"[^\d+]", "", phone)
    data = request.get_json(force=True) or {}
    note = (data.get("note") or "").strip()
    if not note:
        return jsonify({"error": "empty note"}), 400
    get_or_create_state(norm)
    log_activity(norm, g.user["id"], "note", note)
    return jsonify({"ok": True})


@app.route("/api/lead/<phone>/log_call", methods=["POST"])
@auth.login_required
def api_log_call(phone):
    import re
    norm = re.sub(r"[^\d+]", "", phone)
    data = request.get_json(force=True) or {}
    outcome = (data.get("outcome") or "").strip()  # answered / no_answer / wrong_number
    note = (data.get("note") or "").strip()
    if outcome not in ("answered", "no_answer", "wrong_number"):
        return jsonify({"error": "invalid outcome"}), 400
    get_or_create_state(norm)
    db.execute(
        """UPDATE lead_state SET last_contact_at = CURRENT_TIMESTAMP,
            updated_at = CURRENT_TIMESTAMP WHERE lead_phone = ?""", (norm,))
    details = outcome + (f": {note}" if note else "")
    log_activity(norm, g.user["id"], "called", details)
    return jsonify({"ok": True})


@app.route("/api/activity/recent")
@auth.login_required
def api_recent_activity():
    """Last 100 activity events across all leads — for the team feed."""
    rows = db.query("""
        SELECT a.id, a.lead_phone, a.user_id, a.action, a.details,
                a.created_at, u.full_name, u.username,
                l.name AS lead_name, l.region AS lead_region
        FROM activity a
        LEFT JOIN users u ON u.id = a.user_id
        LEFT JOIN leads l ON l.phone = a.lead_phone
        ORDER BY a.created_at DESC
        LIMIT 100
    """, ())
    return jsonify(rows)


@app.route("/api/lead/<phone>/favorite", methods=["POST", "DELETE"])
@auth.login_required
def api_favorite(phone):
    import re
    norm = re.sub(r"[^\d+]", "", phone)
    user_id = g.user["id"]
    if request.method == "DELETE":
        db.execute(
            "DELETE FROM favorites WHERE user_id = ? AND lead_phone = ?",
            (user_id, norm))
    else:
        existing = db.query_one(
            "SELECT 1 AS x FROM favorites WHERE user_id = ? AND lead_phone = ?",
            (user_id, norm))
        if not existing:
            db.execute(
                "INSERT INTO favorites (user_id, lead_phone) VALUES (?, ?)",
                (user_id, norm))
    return jsonify({"ok": True})


@app.route("/api/activity/<int:aid>", methods=["PATCH", "DELETE"])
@auth.login_required
def api_edit_activity(aid):
    """Admins can edit/delete any activity. Users can edit/delete their own."""
    row = db.query_one(
        "SELECT * FROM activity WHERE id = ?", (aid,))
    if not row:
        return jsonify({"error": "not found"}), 404
    is_admin = g.user["role"] == "admin"
    is_owner = row["user_id"] == g.user["id"]
    if not (is_admin or is_owner):
        return jsonify({"error": "forbidden"}), 403

    if request.method == "DELETE":
        db.execute("DELETE FROM activity WHERE id = ?", (aid,))
        broadcast({"type": "activity_deleted", "id": aid,
                    "lead_phone": row["lead_phone"]})
        return jsonify({"ok": True})

    data = request.get_json(force=True) or {}
    new_details = (data.get("details") or "").strip()
    db.execute("UPDATE activity SET details = ? WHERE id = ?",
                 (new_details, aid))
    broadcast({"type": "activity_updated", "id": aid,
                "lead_phone": row["lead_phone"], "details": new_details})
    return jsonify({"ok": True})


@app.route("/api/lead/<phone>/assign", methods=["POST"])
@auth.login_required
def api_assign(phone):
    import re
    norm = re.sub(r"[^\d+]", "", phone)
    data = request.get_json(force=True) or {}
    user_id = data.get("user_id")  # may be None to unassign
    get_or_create_state(norm)
    db.execute(
        "UPDATE lead_state SET assigned_to = ? WHERE lead_phone = ?",
        (user_id, norm),
    )
    target = db.query_one("SELECT full_name FROM users WHERE id = ?",
                            (user_id,)) if user_id else None
    log_activity(norm, g.user["id"], "assigned",
                  target["full_name"] if target else "unassigned")
    return jsonify({"ok": True})


# ---------- Daily plan ----------

@app.route("/api/daily_plan")
@auth.login_required
def api_daily_plan():
    user = g.user
    today = date.today().isoformat()

    # Calls made today by this user
    calls_today = db.query_one("""
        SELECT COUNT(*) AS n FROM activity
        WHERE user_id = ? AND action IN ('called', 'reached')
          AND DATE(created_at) = ?
    """, (user["id"], today))

    follow_ups = db.query("""
        SELECT l.*, ls.follow_up_date, ls.status
        FROM leads l JOIN lead_state ls ON ls.lead_phone = l.phone
        WHERE ls.assigned_to = ? AND ls.follow_up_date <= ?
          AND ls.status NOT IN ('closed_won','closed_lost','disqualified',
                                  'not_interested')
        ORDER BY ls.follow_up_date ASC
        LIMIT 50
    """, (user["id"], today))

    new_leads = db.query("""
        SELECT l.*, ls.status FROM leads l
        LEFT JOIN lead_state ls ON ls.lead_phone = l.phone
        WHERE ls.assigned_to = ? AND (ls.status = 'new' OR ls.status IS NULL)
        ORDER BY l.imported_at DESC
        LIMIT 100
    """, (user["id"],))

    return jsonify({
        "calls_today": calls_today["n"] if calls_today else 0,
        "target": 20,
        "follow_ups": follow_ups,
        "new_leads": new_leads,
    })


# ---------- API: Users (admin only) ----------

@app.route("/api/users")
@auth.login_required
def api_users():
    rows = db.query(
        "SELECT id, username, full_name, role, is_active FROM users "
        "ORDER BY full_name", ())
    return jsonify(rows)


@app.route("/api/users", methods=["POST"])
@auth.admin_required
def api_create_user():
    data = request.get_json(force=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""
    full_name = (data.get("full_name") or "").strip()
    role = data.get("role") or "sales"
    if not username or not password or not full_name:
        return jsonify({"error": "missing fields"}), 400
    try:
        uid = auth.create_user(username, password, full_name, role)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"ok": True, "id": uid})


@app.route("/api/users/<int:uid>", methods=["DELETE"])
@auth.admin_required
def api_delete_user(uid):
    if uid == g.user["id"]:
        return jsonify({"error": "cannot delete self"}), 400
    db.execute("UPDATE users SET is_active = 0 WHERE id = ?", (uid,))
    return jsonify({"ok": True})


@app.route("/api/users/<int:uid>/password", methods=["POST"])
@auth.admin_required
def api_reset_password(uid):
    data = request.get_json(force=True) or {}
    new_pw = data.get("password") or ""
    if not new_pw:
        return jsonify({"error": "missing password"}), 400
    db.execute("UPDATE users SET password_hash = ? WHERE id = ?",
                 (auth.hash_password(new_pw), uid))
    return jsonify({"ok": True})


# ---------- Leads sync (from local lead-finder) ----------

@app.route("/api/sync/leads", methods=["POST"])
def api_sync_leads():
    """Receive leads pushed from the local lead-finder.
    Auth via X-Sync-Token header.
    """
    token_required = os.environ.get("SYNC_TOKEN", "dev-token")
    token = request.headers.get("X-Sync-Token")
    if token != token_required:
        return jsonify({"error": "unauthorized"}), 401

    payload = request.get_json(force=True) or {}
    leads = payload.get("leads", [])

    # Group incoming leads by phone — multiple listings per owner become
    # one lead with N properties.
    by_phone = {}
    for lead in leads:
        phone = (lead.get("phone") or "").strip()
        if not phone:
            continue
        by_phone.setdefault(phone, []).append(lead)

    upserted = 0
    for phone, group in by_phone.items():
        # Collect every (region, name, category, gmaps_url) tuple for this owner
        properties = [{
            "region": l.get("region", ""),
            "name": l.get("name", ""),
            "category": l.get("category", ""),
            "gmaps_url": l.get("gmaps_url", ""),
        } for l in group]

        # Pick the "primary" listing — the one with longest name (more specific)
        primary = max(group, key=lambda l: len(l.get("name", "")))

        existing = db.query_one(
            "SELECT phone, properties FROM leads WHERE phone = ?", (phone,))

        if existing:
            # Merge with existing properties: keep any old listings not in
            # this batch (e.g. previous scrape), append new ones.
            existing_props = []
            if existing.get("properties"):
                try:
                    existing_props = json.loads(existing["properties"])
                except Exception:
                    existing_props = []
            seen_keys = {(p.get("region",""), p.get("name","")) for p in properties}
            for p in existing_props:
                if (p.get("region",""), p.get("name","")) not in seen_keys:
                    properties.append(p)

            db.execute("""
                UPDATE leads SET region = ?, name = ?, category = ?,
                    email = ?, gmaps_url = ?, online_presence = ?,
                    domain_gr_available = ?, domain_com_available = ?,
                    domain_suggestion = ?, enriched_at = ?, properties = ?
                WHERE phone = ?
            """, (primary.get("region", ""), primary.get("name", ""),
                  primary.get("category", ""), primary.get("email", ""),
                  primary.get("gmaps_url", ""), primary.get("online_presence", ""),
                  primary.get("domain_gr_available", ""),
                  primary.get("domain_com_available", ""),
                  primary.get("domain_suggestion", ""),
                  primary.get("enriched_at", ""),
                  json.dumps(properties, ensure_ascii=False), phone))
        else:
            db.execute("""
                INSERT INTO leads (phone, region, name, category, email,
                    gmaps_url, online_presence, domain_gr_available,
                    domain_com_available, domain_suggestion, enriched_at,
                    properties)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (phone, primary.get("region", ""), primary.get("name", ""),
                  primary.get("category", ""), primary.get("email", ""),
                  primary.get("gmaps_url", ""), primary.get("online_presence", ""),
                  primary.get("domain_gr_available", ""),
                  primary.get("domain_com_available", ""),
                  primary.get("domain_suggestion", ""),
                  primary.get("enriched_at", ""),
                  json.dumps(properties, ensure_ascii=False)))
            db.execute(
                "INSERT INTO lead_state (lead_phone, status) VALUES (?, 'new')",
                (phone,))
        upserted += 1

    if upserted:
        broadcast({"type": "leads_synced", "count": upserted})

    return jsonify({"ok": True, "upserted": upserted})


# ---------- User regions (admin assigns regions to sales users) ----------

def get_user_regions(user_id: int) -> list[str]:
    rows = db.query(
        "SELECT region FROM user_regions WHERE user_id = ? ORDER BY region",
        (user_id,))
    return [r["region"] for r in rows]


@app.route("/api/users/<int:uid>/regions")
@auth.login_required
def api_get_user_regions(uid):
    # Admin can see anyone's regions; non-admin only their own.
    if g.user["role"] != "admin" and uid != g.user["id"]:
        return jsonify({"error": "forbidden"}), 403
    return jsonify({"regions": get_user_regions(uid)})


@app.route("/api/users/<int:uid>/regions", methods=["POST"])
@auth.admin_required
def api_set_user_regions(uid):
    data = request.get_json(force=True) or {}
    regions = data.get("regions") or []
    if not isinstance(regions, list):
        return jsonify({"error": "regions must be a list"}), 400
    regions = [str(r).strip() for r in regions if str(r).strip()]
    # Replace the full set
    db.execute("DELETE FROM user_regions WHERE user_id = ?", (uid,))
    if regions:
        db.execute_many(
            "INSERT INTO user_regions (user_id, region) VALUES (?, ?)",
            [(uid, r) for r in regions])
    user = db.query_one(
        "SELECT username, full_name FROM users WHERE id = ?", (uid,))
    broadcast({
        "type": "regions_assigned",
        "user_id": uid,
        "username": user["username"] if user else "",
        "full_name": user["full_name"] if user else "",
        "regions": regions,
    })
    return jsonify({"ok": True, "regions": regions})


@app.route("/api/regions/all")
@auth.login_required
def api_all_regions():
    """Distinct regions present in the leads table."""
    rows = db.query(
        "SELECT region, COUNT(*) AS lead_count FROM leads "
        "WHERE region IS NOT NULL AND region <> '' "
        "GROUP BY region ORDER BY region", ())
    return jsonify(rows)


# ---------- Main UI ----------

@app.route("/")
@auth.login_required
def index():
    user = dict(g.user)
    user["regions"] = get_user_regions(user["id"])
    return render_template_string(INDEX_HTML, user=user)


@app.route("/api/me")
@auth.login_required
def api_me():
    user = dict(g.user)
    user["regions"] = get_user_regions(user["id"])
    return jsonify(user)


PROPOSAL_TEMPLATE = ROOT / "templates" / "proposal_template.html"


@app.route("/api/proposal/generate", methods=["POST"])
@auth.login_required
def api_generate_proposal():
    data = request.get_json(force=True) or {}
    if not PROPOSAL_TEMPLATE.exists():
        return jsonify({"error": "template missing"}), 500

    from jinja2 import Environment, FileSystemLoader, select_autoescape
    env = Environment(
        loader=FileSystemLoader(str(PROPOSAL_TEMPLATE.parent)),
        autoescape=select_autoescape(["html"]),
    )
    tpl = env.get_template(PROPOSAL_TEMPLATE.name)

    from datetime import date as _date
    from regions_context import get_context
    today = _date.today().strftime("%d/%m/%Y")
    location = data.get("location", "").strip() or "—"
    region_ctx = get_context(location)
    ctx = {
        "hotel_name": data.get("hotel_name", "").strip() or "—",
        "date": data.get("date", "").strip() or today,
        "location": location,
        "location_long": data.get("location_long", "").strip() or location,
        "location_short": data.get("location_short", "").strip() or location,
        "property_type": data.get("property_type", "villa"),
        "author_names": data.get("author_names", "").strip()
                        or g.user["full_name"],
        "author_phone": data.get("author_phone", "").strip() or "—",
        "author_email": data.get("author_email", "").strip() or "—",
        "option_a_price": data.get("option_a_price", "").strip()
                          or "€700 – €900",
        "option_b_price": data.get("option_b_price", "").strip()
                          or "€1.500 – €2.000",
        # Region-specific context
        "region_article": region_ctx.get("article", "την"),
        "region_genitive": region_ctx.get("genitive", "της περιοχής"),
        "region_description": region_ctx.get("description", ""),
        "region_sales_angle": region_ctx.get("sales_angle", ""),
        "region_highlights": region_ctx.get("highlights", ""),
    }
    html = tpl.render(**ctx)

    # Optionally log activity if lead phone provided
    lead_phone = (data.get("lead_phone") or "").strip()
    if lead_phone:
        import re as _re
        norm = _re.sub(r"[^\d+]", "", lead_phone)
        existing = db.query_one(
            "SELECT phone FROM leads WHERE phone = ?", (norm,))
        if existing:
            log_activity(norm, g.user["id"], "proposal_generated",
                          f"Generated proposal for {ctx['hotel_name']} "
                          f"({ctx['property_type']})")

    return jsonify({"html": html})


RESOURCES_DIR = ROOT / "resources"
RESOURCES_LIST = [
    {"slug": "cold_call_guide", "title": "📞 Cold Call Guide",
     "subtitle": "Πώς να κάνεις cold calls σε ξενοδοχεία"},
    {"slug": "email_templates", "title": "✉️ Email Templates",
     "subtitle": "Templates για email outreach"},
    {"slug": "sales_guide", "title": "📚 Sales Guide",
     "subtitle": "Συνολικός οδηγός πωλήσεων"},
]


@app.route("/api/resources")
@auth.login_required
def api_resources_list():
    return jsonify(RESOURCES_LIST)


@app.route("/api/resources/<slug>")
@auth.login_required
def api_resource(slug):
    import re as _re
    safe = _re.sub(r"[^a-z0-9_]", "", slug.lower())
    path = RESOURCES_DIR / f"{safe}.md"
    if not path.exists():
        return jsonify({"error": "not found"}), 404
    try:
        import markdown as md
        text = path.read_text(encoding="utf-8")
        html = md.markdown(text, extensions=["extra", "tables", "fenced_code"])
        meta = next((r for r in RESOURCES_LIST if r["slug"] == safe), None)
        return jsonify({
            "slug": safe,
            "title": meta["title"] if meta else safe,
            "subtitle": meta["subtitle"] if meta else "",
            "html": html,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)
