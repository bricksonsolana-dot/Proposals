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
                     request, session, g, Response, stream_with_context,
                     send_from_directory, abort)

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
# Cookie hardening — keep credentials away from JS, force same-site,
# require HTTPS in production (Render terminates TLS upstream of us).
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.environ.get("RENDER", "") != "" or
        os.environ.get("FLASK_ENV") == "production",
    # Cache static files (logos, icons, manifest) for a week — they
    # change rarely and the icons in particular are 5-50 KB each.
    SEND_FILE_MAX_AGE_DEFAULT=timedelta(days=7),
)


@app.after_request
def _set_cache_headers(response):
    """Add Cache-Control + immutable for /static/* (rebuilds bust caches
    via the deploy hash that Render rotates). API and page responses
    stay no-store so updates propagate without users needing to clear
    cache or reinstall the TWA."""
    if request.path.startswith("/static/"):
        response.headers["Cache-Control"] = "public, max-age=604800"
    elif request.path.startswith("/api/"):
        response.headers["Cache-Control"] = "no-store"
    elif request.path in ("/", "/login", "/download", "/sw.js"):
        # Inline-rendered HTML pages and the service worker — must
        # always re-fetch so a deploy is visible immediately
        response.headers["Cache-Control"] = "no-store, must-revalidate"
    return response

# Run a function in a background daemon thread so it doesn't block the
# HTTP response. Used for push notifications which fan out one HTTP
# request per subscribed device (200-500ms each over the wire).
import threading as _threading


def _run_in_background(fn, *args, **kwargs):
    t = _threading.Thread(
        target=lambda: _safe_call(fn, *args, **kwargs),
        daemon=True)
    t.start()


def _safe_call(fn, *args, **kwargs):
    try:
        fn(*args, **kwargs)
    except Exception as e:
        print(f"[bg] {fn.__name__} failed: {e}", flush=True)


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
<html lang="el"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Devox Sales">
<link rel="manifest" href="/static/manifest.json">
<link rel="apple-touch-icon" href="/static/icon-192.png">
<link rel="icon" type="image/png" sizes="192x192" href="/static/icon-192.png">
<link rel="icon" type="image/png" sizes="512x512" href="/static/icon-512.png">
<link rel="shortcut icon" href="/static/logo.ico">
<title>Sign in — Devox Sales</title>
<style>
:root {
  --bg: #0a0b0f; --surface: #12141b; --border: #232733;
  --border-strong: #2f3445; --text: #f4f5f7; --text-2: #b6bac6;
  --text-3: #7c818f; --text-4: #555b6a;
  --brand: #4f7cff; --brand-hover: #6c8fff;
  --danger: #ff5c6f; --danger-soft: rgba(255,92,111,0.12);
  --r-2: 6px; --r-3: 10px; --r-4: 14px;
}
* { box-sizing: border-box; }
body {
  font-family: 'Inter', -apple-system, 'Segoe UI', sans-serif;
  background: var(--bg);
  color: var(--text);
  margin: 0; min-height: 100vh;
  display: flex; align-items: center; justify-content: center;
  padding: 24px;
  -webkit-font-smoothing: antialiased;
  background-image:
    radial-gradient(at 20% 0%, rgba(79,124,255,0.06) 0%, transparent 50%),
    radial-gradient(at 80% 100%, rgba(79,124,255,0.04) 0%, transparent 50%);
}
.box {
  background: var(--surface);
  padding: 36px 32px 28px;
  border-radius: var(--r-4);
  width: 100%; max-width: 380px;
  border: 1px solid var(--border);
  box-shadow: 0 16px 48px rgba(0,0,0,0.4);
}
.logo {
  display: flex; align-items: center; justify-content: center;
  margin-bottom: 6px;
}
.logo img {
  height: 48px; width: auto;
  filter: brightness(0) invert(1);
}
h1 {
  font-size: 13px; margin: 0 0 28px; text-align: center;
  color: var(--text-3);
  font-weight: 600; letter-spacing: 0.16em;
  text-transform: uppercase;
}
label {
  display: block; font-size: 11px;
  color: var(--text-3); margin-bottom: 6px;
  font-weight: 600; text-transform: uppercase;
  letter-spacing: 0.06em;
}
input {
  width: 100%;
  padding: 0 14px;
  height: 44px;
  background: var(--bg);
  color: var(--text);
  border: 1px solid var(--border);
  border-radius: var(--r-2);
  font-family: inherit; font-size: 16px;
  margin-bottom: 16px;
  transition: border-color 0.12s, background 0.12s;
}
input:hover { border-color: var(--border-strong); }
input:focus {
  outline: 0; border-color: var(--brand);
  box-shadow: 0 0 0 3px rgba(79,124,255,0.12);
}
button {
  width: 100%; padding: 0;
  height: 46px;
  background: var(--brand);
  color: white;
  border: 0; border-radius: var(--r-2);
  font-family: inherit; font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.12s, transform 0.08s;
  margin-top: 4px;
}
button:hover { background: var(--brand-hover); }
button:active { transform: scale(0.99); }
.err {
  color: var(--danger);
  background: var(--danger-soft);
  border: 1px solid rgba(255,92,111,0.3);
  padding: 10px 14px;
  border-radius: var(--r-2);
  font-size: 13px; margin-top: 14px;
}
.download-link {
  display: block; text-align: center;
  margin-top: 22px;
  padding-top: 22px;
  border-top: 1px solid var(--border);
  color: var(--text-3);
  text-decoration: none; font-size: 13px;
  font-weight: 500;
}
.download-link:hover { color: var(--brand); }
</style></head>
<body>
<form class="box" method="POST">
  <div class="logo"><img src="/static/logo.png" alt="Devox"></div>
  <h1>Sales · Sign in</h1>
  <label>Username</label>
  <input name="username" autofocus required autocomplete="username">
  <label>Password</label>
  <input name="password" type="password" required autocomplete="current-password">
  <button type="submit">Sign in</button>
  {% if error %}<div class="err">{{ error }}</div>{% endif %}
  <a class="download-link" href="/download">↓ Download for Windows or Android</a>
</form>
</body></html>"""


@app.route("/login", methods=["GET", "POST"])
def login():
    # If the user already has a valid session, don't show the login
    # form — send them back into the app. This fixes the Android back
    # button showing the sign-in page after navigating around the SPA.
    if request.method == "GET" and "user_id" in session:
        if auth._check_still_active(session["user_id"]):
            return redirect("/")
        session.clear()
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
    # Don't SELECT l.properties — that JSON column can be 1-5KB per row
    # for owners with many listings. We only need the count of properties
    # in the list view. The full JSON is fetched in /api/lead/<phone>
    # when the side panel opens. Reduces /api/leads payload by 50-70%.
    sql = f"""
        SELECT l.phone, l.region, l.name, l.category, l.email,
                l.gmaps_url, l.online_presence,
                l.domain_gr_available, l.domain_com_available,
                l.domain_suggestion,
                ls.status, ls.assigned_to, ls.follow_up_date,
                ls.last_contact_at,
                u.full_name AS assigned_to_name,
                CASE WHEN f.user_id IS NOT NULL THEN 1 ELSE 0 END AS is_favorite,
                CASE WHEN l.properties IS NULL OR l.properties = ''
                     THEN 1 ELSE
                     COALESCE(
                         (LENGTH(l.properties) -
                          LENGTH(REPLACE(l.properties, '"region"', ''))) / 8,
                         1)
                END AS property_count
        FROM leads l
        LEFT JOIN lead_state ls ON ls.lead_phone = l.phone
        LEFT JOIN users u ON u.id = ls.assigned_to
        LEFT JOIN favorites f ON f.lead_phone = l.phone AND f.user_id = ?
        {where_sql}
        ORDER BY l.region, l.name
        LIMIT 5000
    """
    leads = db.query(sql, tuple(params))

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

    # Push notification to the newly assigned user (if not self-assign)
    if user_id and int(user_id) != g.user["id"]:
        lead = db.query_one(
            "SELECT name, region FROM leads WHERE phone = ?", (norm,))
        if lead:
            _run_in_background(_push.send_push_to_user, int(user_id), {
                "title": "New lead assigned",
                "body": f"{lead['name']} · {lead['region'] or 'no region'}",
                "tag": f"lead-{norm}",
                "data": {"url": "/", "lead_phone": norm},
            })
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
    include_inactive = request.args.get("include_inactive") == "1"
    if include_inactive and g.user["role"] == "admin":
        rows = db.query(
            "SELECT id, username, full_name, role, is_active, avatar "
            "FROM users ORDER BY is_active DESC, full_name", ())
    else:
        rows = db.query(
            "SELECT id, username, full_name, role, is_active, avatar "
            "FROM users WHERE is_active = 1 ORDER BY full_name", ())
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
        return jsonify({"error": "cannot deactivate yourself"}), 400
    target = db.query_one(
        "SELECT id, username, full_name, role, is_active FROM users "
        "WHERE id = ?", (uid,))
    if not target:
        return jsonify({"error": "user not found"}), 404
    if not target.get("is_active"):
        return jsonify({"error": "user is already deactivated"}), 400
    # Prevent deactivating the last active admin
    if target["role"] == "admin":
        active_admins = db.query_one(
            "SELECT COUNT(*) AS n FROM users "
            "WHERE role = 'admin' AND is_active = 1", ())
        if active_admins and active_admins["n"] <= 1:
            return jsonify(
                {"error": "cannot deactivate the last active admin"}), 400
    db.execute(
        "UPDATE users SET is_active = 0 WHERE id = ?", (uid,))
    # Free leads claimed by this user — they can't work them anymore
    db.execute(
        "UPDATE lead_state SET assigned_to = NULL, "
        "updated_at = CURRENT_TIMESTAMP WHERE assigned_to = ?", (uid,))
    # Drop their region assignments
    db.execute("DELETE FROM user_regions WHERE user_id = ?", (uid,))
    broadcast({
        "type": "user_deactivated",
        "user_id": uid,
        "full_name": target["full_name"],
    })
    return jsonify({"ok": True})


@app.route("/api/users/<int:uid>/role", methods=["POST"])
@auth.admin_required
def api_change_role(uid):
    data = request.get_json(force=True) or {}
    new_role = data.get("role") or ""
    if new_role not in ("admin", "sales"):
        return jsonify({"error": "role must be 'admin' or 'sales'"}), 400
    target = db.query_one(
        "SELECT id, role, is_active, full_name FROM users WHERE id = ?",
        (uid,))
    if not target:
        return jsonify({"error": "user not found"}), 404
    if target["role"] == new_role:
        return jsonify({"ok": True, "unchanged": True})
    # Prevent demoting yourself or the last active admin
    if target["role"] == "admin" and new_role == "sales":
        if uid == g.user["id"]:
            return jsonify(
                {"error": "you cannot demote yourself"}), 400
        active_admins = db.query_one(
            "SELECT COUNT(*) AS n FROM users "
            "WHERE role = 'admin' AND is_active = 1", ())
        if active_admins and active_admins["n"] <= 1:
            return jsonify(
                {"error": "cannot demote the last active admin"}), 400
    db.execute(
        "UPDATE users SET role = ? WHERE id = ?", (new_role, uid))
    broadcast({
        "type": "user_role_changed",
        "user_id": uid,
        "full_name": target["full_name"],
        "role": new_role,
    })
    return jsonify({"ok": True, "role": new_role})


@app.route("/api/users/<int:uid>/activate", methods=["POST"])
@auth.admin_required
def api_activate_user(uid):
    target = db.query_one(
        "SELECT id, full_name, is_active FROM users WHERE id = ?", (uid,))
    if not target:
        return jsonify({"error": "user not found"}), 404
    if target.get("is_active"):
        return jsonify({"error": "user is already active"}), 400
    db.execute(
        "UPDATE users SET is_active = 1 WHERE id = ?", (uid,))
    broadcast({
        "type": "user_activated",
        "user_id": uid,
        "full_name": target["full_name"],
    })
    return jsonify({"ok": True})


@app.route("/api/users/<int:uid>/password", methods=["POST"])
@auth.admin_required
def api_reset_password(uid):
    data = request.get_json(force=True) or {}
    new_pw = data.get("password") or ""
    if not new_pw:
        return jsonify({"error": "missing password"}), 400
    if len(new_pw) < 6:
        return jsonify({"error": "password must be at least 6 characters"}), 400
    db.execute("UPDATE users SET password_hash = ? WHERE id = ?",
                 (auth.hash_password(new_pw), uid))
    return jsonify({"ok": True})


@app.route("/api/me/avatar", methods=["POST"])
@auth.login_required
def api_set_my_avatar():
    """Upload a profile picture. Body: {"data": "data:image/jpeg;base64,..."}.
    The image is already compressed client-side (square crop, ~300px,
    JPEG q=0.8 → ~30-50KB). Setting null clears the avatar."""
    data = request.get_json(force=True) or {}
    avatar = data.get("data")
    if avatar is None or avatar == "":
        db.execute("UPDATE users SET avatar = NULL WHERE id = ?",
                     (g.user["id"],))
        return jsonify({"ok": True})
    if not isinstance(avatar, str) or not avatar.startswith("data:image/"):
        return jsonify({"error": "must be a data:image/* URL"}), 400
    if len(avatar) > 250_000:
        return jsonify(
            {"error": "avatar too large (max ~180KB after base64)"}), 400
    db.execute("UPDATE users SET avatar = ? WHERE id = ?",
                 (avatar, g.user["id"]))
    return jsonify({"ok": True})


@app.route("/api/users/<int:uid>/avatar")
@auth.login_required
def api_get_avatar(uid):
    """Return another user's avatar (or null). Cheap endpoint, used by
    the chat list and message rendering to overlay the avatar on top of
    the initials placeholder."""
    row = db.query_one(
        "SELECT avatar FROM users WHERE id = ? AND is_active = 1", (uid,))
    if not row:
        return jsonify({"avatar": None})
    return jsonify({"avatar": row.get("avatar")})


@app.route("/api/me/password", methods=["POST"])
@auth.login_required
def api_change_my_password():
    """Self-service password change. Requires the current password."""
    data = request.get_json(force=True) or {}
    current_pw = data.get("current_password") or ""
    new_pw = data.get("new_password") or ""
    if not current_pw or not new_pw:
        return jsonify(
            {"error": "current and new passwords are required"}), 400
    if len(new_pw) < 6:
        return jsonify(
            {"error": "new password must be at least 6 characters"}), 400
    if new_pw == current_pw:
        return jsonify(
            {"error": "new password must differ from current"}), 400
    row = db.query_one(
        "SELECT password_hash FROM users WHERE id = ?", (g.user["id"],))
    if not row or not auth.verify_password(current_pw, row["password_hash"]):
        return jsonify({"error": "current password is incorrect"}), 400
    db.execute(
        "UPDATE users SET password_hash = ? WHERE id = ?",
        (auth.hash_password(new_pw), g.user["id"]))
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

    previous = set(get_user_regions(uid))
    incoming = set(regions)
    added = incoming - previous
    removed = previous - incoming

    # Replace the user_regions set
    db.execute("DELETE FROM user_regions WHERE user_id = ?", (uid,))
    if regions:
        db.execute_many(
            "INSERT INTO user_regions (user_id, region) VALUES (?, ?)",
            [(uid, r) for r in regions])

    # Bulk-assign leads in newly added regions to this user (My Leads).
    # Skip leads already assigned to a DIFFERENT user — don't steal.
    bulk_assigned = 0
    for region in added:
        # Make sure each lead has a row in lead_state, then claim it if free
        unassigned_leads = db.query(
            "SELECT phone FROM leads WHERE region = ? AND phone NOT IN "
            "(SELECT lead_phone FROM lead_state WHERE assigned_to IS NOT NULL "
            " AND assigned_to <> ?)",
            (region, uid))
        for row in unassigned_leads:
            phone = row["phone"]
            existing = db.query_one(
                "SELECT lead_phone FROM lead_state WHERE lead_phone = ?",
                (phone,))
            if existing:
                db.execute(
                    "UPDATE lead_state SET assigned_to = ?, "
                    "updated_at = CURRENT_TIMESTAMP WHERE lead_phone = ?",
                    (uid, phone))
            else:
                db.execute(
                    "INSERT INTO lead_state (lead_phone, status, assigned_to) "
                    "VALUES (?, 'new', ?)", (phone, uid))
            bulk_assigned += 1

    # Un-assign leads in removed regions, but only the ones still
    # assigned to *this* user (don't touch leads other users have claimed).
    bulk_unassigned = 0
    for region in removed:
        rows = db.query(
            "SELECT lead_phone FROM lead_state ls "
            "JOIN leads l ON l.phone = ls.lead_phone "
            "WHERE l.region = ? AND ls.assigned_to = ?",
            (region, uid))
        for r in rows:
            db.execute(
                "UPDATE lead_state SET assigned_to = NULL, "
                "updated_at = CURRENT_TIMESTAMP WHERE lead_phone = ?",
                (r["lead_phone"],))
            bulk_unassigned += 1

    user = db.query_one(
        "SELECT username, full_name FROM users WHERE id = ?", (uid,))
    broadcast({
        "type": "regions_assigned",
        "user_id": uid,
        "username": user["username"] if user else "",
        "full_name": user["full_name"] if user else "",
        "regions": regions,
        "bulk_assigned": bulk_assigned,
        "bulk_unassigned": bulk_unassigned,
    })
    return jsonify({
        "ok": True,
        "regions": regions,
        "bulk_assigned": bulk_assigned,
        "bulk_unassigned": bulk_unassigned,
    })


@app.route("/api/regions/all")
@auth.login_required
def api_all_regions():
    """Distinct regions present in the leads table."""
    rows = db.query(
        "SELECT region, COUNT(*) AS lead_count FROM leads "
        "WHERE region IS NOT NULL AND region <> '' "
        "GROUP BY region ORDER BY region", ())
    return jsonify(rows)


# ---------- Presence (online users) ----------

PRESENCE_TIMEOUT_SECONDS = 90  # users inactive > 90s are considered offline


@app.route("/api/presence/ping", methods=["POST"])
@auth.login_required
def api_presence_ping():
    db.execute(
        "UPDATE users SET last_seen_at = CURRENT_TIMESTAMP WHERE id = ?",
        (g.user["id"],))
    return jsonify({"ok": True})


@app.route("/api/presence")
@auth.login_required
def api_presence():
    """Return user_ids currently online (pinged within 90s)."""
    if db.IS_POSTGRES:
        rows = db.query(
            "SELECT id, last_seen_at FROM users "
            "WHERE is_active = 1 AND last_seen_at > "
            "NOW() - INTERVAL '90 seconds'", ())
    else:
        rows = db.query(
            "SELECT id, last_seen_at FROM users "
            "WHERE is_active = 1 AND last_seen_at > "
            "datetime('now', '-90 seconds')", ())
    return jsonify({"online": [r["id"] for r in rows]})


# ---------- Chat ----------

def _get_or_create_team_chat() -> int:
    """The 'Team' group chat that everyone belongs to. Auto-created."""
    row = db.query_one(
        "SELECT id FROM chats WHERE type = 'team' LIMIT 1", ())
    if row:
        return row["id"]
    # Create the team chat
    if db.IS_POSTGRES:
        with db.get_conn() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO chats (type, name) VALUES ('team', 'Team') "
                "RETURNING id")
            chat_id = cur.fetchone()[0]
    else:
        db.execute(
            "INSERT INTO chats (type, name) VALUES ('team', 'Team')", ())
        row = db.query_one(
            "SELECT id FROM chats WHERE type = 'team' LIMIT 1", ())
        chat_id = row["id"]
    # Add every active user
    users = db.query(
        "SELECT id FROM users WHERE is_active = 1", ())
    for u in users:
        try:
            db.execute(
                "INSERT INTO chat_members (chat_id, user_id) VALUES (?, ?)",
                (chat_id, u["id"]))
        except Exception:
            pass  # already a member
    return chat_id


def _ensure_team_membership(uid: int):
    """Make sure the user is a member of the team chat."""
    team_id = _get_or_create_team_chat()
    existing = db.query_one(
        "SELECT chat_id FROM chat_members WHERE chat_id = ? AND user_id = ?",
        (team_id, uid))
    if not existing:
        try:
            db.execute(
                "INSERT INTO chat_members (chat_id, user_id) VALUES (?, ?)",
                (team_id, uid))
        except Exception:
            pass


def _chat_summary(chat_id: int, viewer_id: int) -> dict:
    """Compose a chat summary: id, type, display_name, last_message,
    unread_count, members (just user_ids for DMs to find the peer).
    """
    chat = db.query_one(
        "SELECT id, type, name, avatar, created_at FROM chats WHERE id = ?",
        (chat_id,))
    if not chat:
        return None
    member_rows = db.query(
        "SELECT cm.user_id, cm.last_read_at, u.full_name, u.username "
        "FROM chat_members cm JOIN users u ON u.id = cm.user_id "
        "WHERE cm.chat_id = ?", (chat_id,))
    members = [{"user_id": r["user_id"], "full_name": r["full_name"],
                 "username": r["username"]} for r in member_rows]
    me = next((r for r in member_rows if r["user_id"] == viewer_id), None)
    last_read = me["last_read_at"] if me else None

    # Unread count
    if last_read:
        urow = db.query_one(
            "SELECT COUNT(*) AS n FROM messages "
            "WHERE chat_id = ? AND user_id <> ? AND created_at > ?",
            (chat_id, viewer_id, last_read))
    else:
        urow = db.query_one(
            "SELECT COUNT(*) AS n FROM messages "
            "WHERE chat_id = ? AND user_id <> ?",
            (chat_id, viewer_id))
    unread = (urow or {}).get("n", 0) if urow else 0

    # Last message
    last = db.query_one(
        "SELECT m.id, m.body, m.created_at, m.user_id, u.full_name "
        "FROM messages m JOIN users u ON u.id = m.user_id "
        "WHERE m.chat_id = ? ORDER BY m.created_at DESC LIMIT 1",
        (chat_id,))

    # Display name: for DMs, the *other* member's name
    display_name = chat["name"]
    if chat["type"] == "dm":
        other = next((m for m in members if m["user_id"] != viewer_id),
                     None)
        display_name = other["full_name"] if other else "(unknown)"

    return {
        "id": chat["id"],
        "type": chat["type"],
        "name": display_name,
        "avatar": chat.get("avatar"),
        "members": members,
        "unread": unread,
        "last_message": {
            "id": last["id"], "body": last["body"],
            "created_at": last["created_at"].isoformat(timespec="seconds")
              if hasattr(last["created_at"], "isoformat")
              else str(last["created_at"]),
            "user_id": last["user_id"],
            "full_name": last["full_name"],
        } if last else None,
    }


@app.route("/api/chats")
@auth.login_required
def api_chats():
    """List the chats the current user is a member of.

    Used to be 4 queries per chat (N+1 problem). Now batches everything
    into 4 queries TOTAL regardless of how many chats the user is in.
    """
    _ensure_team_membership(g.user["id"])
    viewer_id = g.user["id"]

    rows = db.query(
        "SELECT chat_id FROM chat_members WHERE user_id = ?", (viewer_id,))
    chat_ids = [r["chat_id"] for r in rows]
    if not chat_ids:
        return jsonify({"chats": []})

    placeholders = ",".join("?" * len(chat_ids))

    # Q1: chat metadata + viewer's last_read_at
    chat_rows = db.query(
        f"SELECT c.id, c.type, c.name, c.avatar, cm.last_read_at "
        f"FROM chats c "
        f"JOIN chat_members cm ON cm.chat_id = c.id AND cm.user_id = ? "
        f"WHERE c.id IN ({placeholders})",
        (viewer_id,) + tuple(chat_ids))

    # Q2: every member of every chat
    member_rows = db.query(
        f"SELECT cm.chat_id, cm.user_id, u.full_name, u.username "
        f"FROM chat_members cm JOIN users u ON u.id = cm.user_id "
        f"WHERE cm.chat_id IN ({placeholders})",
        tuple(chat_ids))
    members_by_chat = {}
    for m in member_rows:
        members_by_chat.setdefault(m["chat_id"], []).append({
            "user_id": m["user_id"], "full_name": m["full_name"],
            "username": m["username"]})

    # Q3: last message per chat (window function on Postgres, GROUP BY
    # MAX(id) join on SQLite)
    if db.IS_POSTGRES:
        last_msgs = db.query(
            f"SELECT DISTINCT ON (m.chat_id) m.chat_id, m.id, m.body, "
            f"       m.user_id, m.created_at, u.full_name "
            f"FROM messages m JOIN users u ON u.id = m.user_id "
            f"WHERE m.chat_id IN ({placeholders}) "
            f"ORDER BY m.chat_id, m.created_at DESC",
            tuple(chat_ids))
    else:
        last_msgs = db.query(
            f"SELECT m.chat_id, m.id, m.body, m.user_id, "
            f"       m.created_at, u.full_name "
            f"FROM messages m "
            f"JOIN users u ON u.id = m.user_id "
            f"JOIN (SELECT chat_id, MAX(id) AS max_id FROM messages "
            f"      WHERE chat_id IN ({placeholders}) GROUP BY chat_id) "
            f"  AS lm ON lm.chat_id = m.chat_id AND lm.max_id = m.id",
            tuple(chat_ids))
    last_by_chat = {m["chat_id"]: m for m in last_msgs}

    # Q4: unread counts per chat for this viewer (using viewer's
    # last_read_at from Q1 as the threshold)
    last_read_by_chat = {c["id"]: c["last_read_at"] for c in chat_rows}
    if db.IS_POSTGRES:
        unread_rows = db.query(
            f"SELECT chat_id, COUNT(*) AS n FROM messages "
            f"WHERE chat_id IN ({placeholders}) AND user_id <> ? "
            f"GROUP BY chat_id",
            tuple(chat_ids) + (viewer_id,))
    else:
        unread_rows = db.query(
            f"SELECT chat_id, COUNT(*) AS n FROM messages "
            f"WHERE chat_id IN ({placeholders}) AND user_id <> ? "
            f"GROUP BY chat_id",
            tuple(chat_ids) + (viewer_id,))
    # Coarse total — we then subtract the read ones in Python by
    # comparing message timestamps. That's another query; instead we
    # just take the COUNT for chats with no last_read_at, and 0 for
    # the rest if last_read_at >= last_message.created_at.
    # For accuracy, recompute per chat with last_read_at.
    unread_by_chat = {r["chat_id"]: r["n"] for r in unread_rows}
    # Filter out: if viewer has read past the last message, force 0.
    for cid, lr in last_read_by_chat.items():
        last = last_by_chat.get(cid)
        if not last:
            unread_by_chat[cid] = 0
        elif lr is not None:
            # If we have a last_read_at after or equal to the last
            # message's created_at, no unreads
            try:
                lm_time = last["created_at"]
                if lr >= lm_time:
                    unread_by_chat[cid] = 0
                else:
                    # Re-count messages newer than last_read
                    cnt = db.query_one(
                        "SELECT COUNT(*) AS n FROM messages "
                        "WHERE chat_id = ? AND user_id <> ? "
                        "AND created_at > ?",
                        (cid, viewer_id, lr))
                    unread_by_chat[cid] = (cnt or {}).get("n", 0) if cnt else 0
            except Exception:
                pass

    out = []
    for c in chat_rows:
        cid = c["id"]
        members = members_by_chat.get(cid, [])
        last = last_by_chat.get(cid)
        display_name = c["name"]
        if c["type"] == "dm":
            other = next((m for m in members if m["user_id"] != viewer_id), None)
            display_name = other["full_name"] if other else "(unknown)"
        last_payload = None
        if last:
            ts = last["created_at"]
            last_payload = {
                "id": last["id"], "body": last["body"],
                "created_at": ts.isoformat(timespec="seconds")
                  if hasattr(ts, "isoformat") else str(ts),
                "user_id": last["user_id"],
                "full_name": last["full_name"],
            }
        out.append({
            "id": cid, "type": c["type"], "name": display_name,
            "avatar": c.get("avatar"),
            "members": members,
            "unread": unread_by_chat.get(cid, 0),
            "last_message": last_payload,
        })
    # Sort: team first, then by last message timestamp desc
    out.sort(key=lambda c: (
        0 if c["type"] == "team" else 1,
        -(c["last_message"]["id"] if c["last_message"] else 0),
    ))
    return jsonify({"chats": out})


@app.route("/api/chats/dm/<int:peer_id>", methods=["POST"])
@auth.login_required
def api_open_dm(peer_id):
    """Open a DM with another user. Creates the chat if it doesn't exist."""
    if peer_id == g.user["id"]:
        return jsonify({"error": "cannot DM yourself"}), 400
    peer = db.query_one(
        "SELECT id FROM users WHERE id = ? AND is_active = 1", (peer_id,))
    if not peer:
        return jsonify({"error": "user not found"}), 404

    # Look for an existing DM with exactly these two members
    rows = db.query(
        "SELECT c.id FROM chats c "
        "JOIN chat_members cm1 ON cm1.chat_id = c.id AND cm1.user_id = ? "
        "JOIN chat_members cm2 ON cm2.chat_id = c.id AND cm2.user_id = ? "
        "WHERE c.type = 'dm'", (g.user["id"], peer_id))
    for r in rows:
        # Confirm it has exactly 2 members
        cnt = db.query_one(
            "SELECT COUNT(*) AS n FROM chat_members WHERE chat_id = ?",
            (r["id"],))
        if cnt and cnt["n"] == 2:
            return jsonify({"chat_id": r["id"]})

    # Create new DM
    if db.IS_POSTGRES:
        with db.get_conn() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO chats (type, created_by) VALUES ('dm', %s) "
                "RETURNING id", (g.user["id"],))
            chat_id = cur.fetchone()[0]
    else:
        db.execute(
            "INSERT INTO chats (type, created_by) VALUES ('dm', ?)",
            (g.user["id"],))
        # SQLite: get the inserted id
        row = db.query_one(
            "SELECT MAX(id) AS id FROM chats WHERE type = 'dm' "
            "AND created_by = ?", (g.user["id"],))
        chat_id = row["id"]
    db.execute_many(
        "INSERT INTO chat_members (chat_id, user_id) VALUES (?, ?)",
        [(chat_id, g.user["id"]), (chat_id, peer_id)])
    return jsonify({"chat_id": chat_id})


@app.route("/api/chats/<int:chat_id>/messages")
@auth.login_required
def api_chat_messages(chat_id):
    """Return last 100 messages in the chat."""
    is_member = db.query_one(
        "SELECT 1 AS ok FROM chat_members WHERE chat_id = ? AND user_id = ?",
        (chat_id, g.user["id"]))
    if not is_member:
        return jsonify({"error": "forbidden"}), 403
    rows = db.query(
        "SELECT m.id, m.body, m.attachments, m.user_id, m.created_at, "
        "       m.edited_at, u.full_name, u.username "
        "FROM messages m JOIN users u ON u.id = m.user_id "
        "WHERE m.chat_id = ? ORDER BY m.created_at DESC LIMIT 100",
        (chat_id,))
    rows.reverse()
    out = []
    for r in rows:
        atts = []
        if r.get("attachments"):
            try:
                atts = json.loads(r["attachments"]) or []
            except Exception:
                atts = []
        out.append({
            "id": r["id"], "body": r["body"], "attachments": atts,
            "user_id": r["user_id"],
            "full_name": r["full_name"], "username": r["username"],
            "created_at": r["created_at"].isoformat(timespec="seconds")
              if hasattr(r["created_at"], "isoformat")
              else str(r["created_at"]),
            "edited_at": (r["edited_at"].isoformat(timespec="seconds")
              if hasattr(r["edited_at"], "isoformat")
              else str(r["edited_at"])) if r.get("edited_at") else None,
        })
    summary = _chat_summary(chat_id, g.user["id"])
    return jsonify({"chat": summary, "messages": out})


@app.route("/api/chats/<int:chat_id>/messages", methods=["POST"])
@auth.login_required
def api_send_message(chat_id):
    is_member = db.query_one(
        "SELECT 1 AS ok FROM chat_members WHERE chat_id = ? AND user_id = ?",
        (chat_id, g.user["id"]))
    if not is_member:
        return jsonify({"error": "forbidden"}), 403
    data = request.get_json(force=True) or {}
    body = (data.get("body") or "").strip()
    attachments = data.get("attachments") or []
    if not body and not attachments:
        return jsonify({"error": "empty message"}), 400
    if len(body) > 4000:
        return jsonify({"error": "message too long"}), 400
    # Validate attachments (each {type, data}). Limit total inline size.
    if not isinstance(attachments, list):
        return jsonify({"error": "bad attachments"}), 400
    if len(attachments) > 4:
        return jsonify({"error": "too many attachments (max 4)"}), 400
    total_bytes = 0
    for a in attachments:
        if not isinstance(a, dict): continue
        if a.get("type") not in ("image",):
            return jsonify({"error": "unsupported attachment type"}), 400
        url = a.get("data") or ""
        if not isinstance(url, str) or not url.startswith("data:image/"):
            return jsonify({"error": "bad attachment payload"}), 400
        # 4/3 base64 expansion → ~1.4MB on the wire becomes 1MB raw
        total_bytes += len(url)
    if total_bytes > 4 * 1024 * 1024:
        return jsonify({"error": "attachments too large (max ~4MB total)"}), 400
    attachments_json = json.dumps(attachments) if attachments else None

    if db.IS_POSTGRES:
        with db.get_conn() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO messages (chat_id, user_id, body, attachments) "
                "VALUES (%s, %s, %s, %s) RETURNING id, created_at",
                (chat_id, g.user["id"], body, attachments_json))
            row = cur.fetchone()
            msg_id = row[0]
            created_at = row[1]
    else:
        db.execute(
            "INSERT INTO messages (chat_id, user_id, body, attachments) "
            "VALUES (?, ?, ?, ?)",
            (chat_id, g.user["id"], body, attachments_json))
        row = db.query_one(
            "SELECT id, created_at FROM messages "
            "WHERE chat_id = ? AND user_id = ? "
            "ORDER BY id DESC LIMIT 1", (chat_id, g.user["id"]))
        msg_id = row["id"]
        created_at = row["created_at"]
    # Bump sender's last_read so they don't see their own message as unread
    db.execute(
        "UPDATE chat_members SET last_read_at = CURRENT_TIMESTAMP "
        "WHERE chat_id = ? AND user_id = ?", (chat_id, g.user["id"]))

    created_str = (created_at.isoformat(timespec="seconds")
        if hasattr(created_at, "isoformat") else str(created_at))
    payload = {
        "type": "chat_message",
        "chat_id": chat_id,
        "id": msg_id,
        "body": body,
        "attachments": attachments,
        "user_id": g.user["id"],
        "full_name": g.user["full_name"],
        "username": g.user["username"],
        "created_at": created_str,
    }
    broadcast(payload)

    # Push notifications fan out to a Mozilla/Google push endpoint per
    # device — that's a real HTTP call each (200-500ms). Don't make the
    # send-message API wait for them; fire-and-forget in a thread.
    other_members = db.query(
        "SELECT user_id FROM chat_members "
        "WHERE chat_id = ? AND user_id <> ?", (chat_id, g.user["id"]))
    chat_row = db.query_one(
        "SELECT type, name FROM chats WHERE id = ?", (chat_id,))
    title = (g.user["full_name"]
             if chat_row and chat_row["type"] == "dm"
             else f"{g.user['full_name']} in #{chat_row['name'] or 'chat'}")
    if body:
        snippet = body if len(body) <= 120 else body[:117] + "…"
    elif attachments:
        n_imgs = sum(1 for a in attachments if a.get("type") == "image")
        snippet = f"📷 sent {n_imgs} photo{'s' if n_imgs > 1 else ''}"
    else:
        snippet = ""
    _run_in_background(
        _push.send_push_to_users,
        [m["user_id"] for m in other_members],
        {
            "title": title, "body": snippet,
            "tag": f"chat-{chat_id}",
            "data": {"url": "/#chat", "chat_id": chat_id},
        })

    return jsonify({"ok": True, "message": payload})


@app.route("/api/chats/<int:chat_id>", methods=["PATCH"])
@auth.admin_required
def api_update_chat(chat_id):
    """Admin can rename a chat or change its avatar (group/team only).
    Body: {"name": "...", "avatar": "data:image/jpeg;base64,..." | null}"""
    chat = db.query_one(
        "SELECT id, type FROM chats WHERE id = ?", (chat_id,))
    if not chat:
        return jsonify({"error": "chat not found"}), 404
    if chat["type"] == "dm":
        return jsonify({"error": "cannot rename a direct message"}), 400
    data = request.get_json(force=True) or {}
    name = data.get("name")
    avatar = data.get("avatar", "__unchanged__")
    updates = []
    params = []
    if name is not None:
        nm = (name or "").strip()
        if not nm:
            return jsonify({"error": "name cannot be empty"}), 400
        if len(nm) > 60:
            return jsonify({"error": "name too long (max 60)"}), 400
        updates.append("name = ?"); params.append(nm)
    if avatar != "__unchanged__":
        if avatar is None or avatar == "":
            updates.append("avatar = NULL")
        else:
            if not isinstance(avatar, str) or not avatar.startswith("data:image/"):
                return jsonify({"error": "bad avatar"}), 400
            if len(avatar) > 250_000:
                return jsonify({"error": "avatar too large"}), 400
            updates.append("avatar = ?"); params.append(avatar)
    if not updates:
        return jsonify({"ok": True, "unchanged": True})
    params.append(chat_id)
    db.execute(
        f"UPDATE chats SET {', '.join(updates)} WHERE id = ?",
        tuple(params))
    broadcast({"type": "chat_updated", "chat_id": chat_id})
    return jsonify({"ok": True})


@app.route("/api/chats/<int:chat_id>/read", methods=["POST"])
@auth.login_required
def api_mark_read(chat_id):
    db.execute(
        "UPDATE chat_members SET last_read_at = CURRENT_TIMESTAMP "
        "WHERE chat_id = ? AND user_id = ?",
        (chat_id, g.user["id"]))
    return jsonify({"ok": True})


# ---------- Push notifications ----------

import push as _push

# Service worker MUST be served from the root so it controls the whole
# origin, not just /static/. (Browsers scope service workers by URL.)
@app.route("/sw.js")
def service_worker():
    response = send_from_directory(
        str(ROOT / "static"), "sw.js", mimetype="application/javascript")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["Service-Worker-Allowed"] = "/"
    return response


@app.route("/api/push/public-key")
@auth.login_required
def api_push_public_key():
    return jsonify({"key": _push.public_key()})


@app.route("/api/push/subscribe", methods=["POST"])
@auth.login_required
def api_push_subscribe():
    data = request.get_json(force=True) or {}
    endpoint = (data.get("endpoint") or "").strip()
    keys = data.get("keys") or {}
    p256dh = keys.get("p256dh")
    auth_token = keys.get("auth")
    if not endpoint or not p256dh or not auth_token:
        return jsonify({"error": "missing fields"}), 400
    ua = request.headers.get("User-Agent", "")[:255]
    # Upsert: replace existing subscription with same endpoint
    existing = db.query_one(
        "SELECT id FROM push_subscriptions WHERE endpoint = ?", (endpoint,))
    if existing:
        db.execute(
            "UPDATE push_subscriptions SET user_id = ?, p256dh = ?, auth = ?, "
            "user_agent = ? WHERE id = ?",
            (g.user["id"], p256dh, auth_token, ua, existing["id"]))
    else:
        db.execute(
            "INSERT INTO push_subscriptions "
            "(user_id, endpoint, p256dh, auth, user_agent) "
            "VALUES (?, ?, ?, ?, ?)",
            (g.user["id"], endpoint, p256dh, auth_token, ua))
    return jsonify({"ok": True})


@app.route("/api/push/unsubscribe", methods=["POST"])
@auth.login_required
def api_push_unsubscribe():
    data = request.get_json(force=True) or {}
    endpoint = (data.get("endpoint") or "").strip()
    if endpoint:
        db.execute(
            "DELETE FROM push_subscriptions WHERE endpoint = ?", (endpoint,))
    return jsonify({"ok": True})


@app.route("/api/push/test", methods=["POST"])
@auth.login_required
def api_push_test():
    """Send a test notification to the calling user. Returns rich
    diagnostic info so the frontend can tell the user exactly what's
    happening (no subs vs delivery failed)."""
    subs_before = db.query(
        "SELECT id, endpoint FROM push_subscriptions WHERE user_id = ?",
        (g.user["id"],))
    sent = _push.send_push_to_user(g.user["id"], {
        "title": "Devox Sales",
        "body": "Notifications are working — you'll get a ping for new messages and assignments.",
        "tag": "test",
        "data": {"url": "/"},
    })
    # Re-query after send so we know which subs survived (dead ones
    # got pruned). Pull the last_error too.
    subs_after = db.query(
        "SELECT id, endpoint, last_error FROM push_subscriptions "
        "WHERE user_id = ?", (g.user["id"],))
    hosts = []
    last_error = None
    for s in subs_after:
        ep = s.get("endpoint", "")
        try:
            from urllib.parse import urlparse
            host = urlparse(ep).netloc
            if host:
                hosts.append(host)
        except Exception:
            pass
        if s.get("last_error") and not last_error:
            last_error = s["last_error"]
    pruned = len(subs_before) - len(subs_after)
    return jsonify({
        "ok": True,
        "sent": sent,
        "subscriptions_before": len(subs_before),
        "subscriptions": len(subs_after),
        "pruned": pruned,
        "endpoint_hosts": hosts,
        "last_error": last_error,
    })


@app.route("/api/push/reset", methods=["POST"])
@auth.login_required
def api_push_reset():
    """Wipe ALL push subscriptions for the calling user. The frontend
    follows up with a fresh subscribe(). Useful when the cached
    subscription is signed against a stale VAPID key."""
    n = db.query_one(
        "SELECT COUNT(*) AS n FROM push_subscriptions WHERE user_id = ?",
        (g.user["id"],))
    db.execute(
        "DELETE FROM push_subscriptions WHERE user_id = ?",
        (g.user["id"],))
    return jsonify({"ok": True, "removed": (n or {}).get("n", 0)})


@app.route("/api/push/diagnose")
@auth.login_required
def api_push_diagnose():
    """Snapshot of push state for the current user."""
    subs = db.query(
        "SELECT endpoint, user_agent, created_at "
        "FROM push_subscriptions WHERE user_id = ? ORDER BY id DESC",
        (g.user["id"],))
    public = ""
    try:
        public = _push.public_key()
    except Exception:
        pass
    return jsonify({
        "vapid_public_key_set": bool(public),
        "subscriptions": [{
            "endpoint_host": __import__('urllib.parse').parse.urlparse(
                s["endpoint"]).netloc if s.get("endpoint") else "",
            "user_agent": s.get("user_agent") or "",
            "created_at": str(s.get("created_at") or ""),
        } for s in subs],
    })


# Banter messages — random pool used by the daily summary cron / admin
# broadcast endpoint to deliver "fun" notifications to whoever fell
# behind the goal or surprised the team.
BANTER_MISS = [
    "Beers on you Saturday 🍺",
    "Coffee run tomorrow morning, on you ☕",
    "The team's calling — literally, you owe a phone call 📞",
    "Top of the leaderboard from the bottom 🪤",
    "Daily target had its feelings hurt today 😅",
]
BANTER_HIT = [
    "Crushing it today — keep going 🚀",
    "Daily target ✓. Time for one more? 💪",
    "You're paying for your own beers tonight 🍻",
    "Officially carrying the team 🦾",
]


@app.route("/api/admin/broadcast", methods=["POST"])
@auth.admin_required
def api_admin_broadcast():
    """Admin-only: push a custom notification to selected users (or all)."""
    data = request.get_json(force=True) or {}
    title = (data.get("title") or "Devox Sales").strip()[:80]
    body = (data.get("body") or "").strip()[:300]
    if not body:
        return jsonify({"error": "body is required"}), 400
    user_ids = data.get("user_ids")  # list[int] or None for everyone
    if not user_ids:
        rows = db.query(
            "SELECT id FROM users WHERE is_active = 1", ())
        user_ids = [r["id"] for r in rows]
    sent = _push.send_push_to_users(
        [int(u) for u in user_ids],
        {"title": title, "body": body, "tag": "broadcast",
         "data": {"url": "/"}})
    return jsonify({"ok": True, "sent": sent})


@app.route("/api/admin/banter", methods=["POST"])
@auth.admin_required
def api_admin_banter():
    """One-tap fun: ping the slacker(s) from today's leaderboard.
    Pass {"behind": true} to push a random miss-banter to everyone
    below 50% of target, {"hit": true} to celebrate everyone over
    target, or {"user_id": N, "kind": "miss"|"hit"} for a single user."""
    import random
    data = request.get_json(force=True) or {}
    target = 20  # default daily call target

    if "user_id" in data:
        kind = data.get("kind", "miss")
        line = random.choice(
            BANTER_MISS if kind == "miss" else BANTER_HIT)
        sent = _push.send_push_to_user(int(data["user_id"]),
            {"title": "Devox Sales", "body": line, "tag": "banter",
             "data": {"url": "/"}})
        return jsonify({"ok": True, "sent": sent})

    today = date.today().isoformat()
    rows = db.query(
        "SELECT u.id, u.full_name, COUNT(a.id) AS calls FROM users u "
        "LEFT JOIN activity a ON a.user_id = u.id AND a.action = 'called' "
        "  AND date(a.created_at) = ? "
        "WHERE u.is_active = 1 GROUP BY u.id, u.full_name",
        (today,))
    behind = [r for r in rows if (r["calls"] or 0) < target * 0.5]
    hit = [r for r in rows if (r["calls"] or 0) >= target]

    sent_total = 0
    if data.get("behind"):
        for r in behind:
            line = random.choice(BANTER_MISS)
            sent_total += _push.send_push_to_user(r["id"],
                {"title": "Devox Sales", "body": line, "tag": "banter",
                 "data": {"url": "/"}})
    if data.get("hit"):
        for r in hit:
            line = random.choice(BANTER_HIT)
            sent_total += _push.send_push_to_user(r["id"],
                {"title": "Devox Sales", "body": line, "tag": "banter",
                 "data": {"url": "/"}})
    return jsonify({"ok": True, "sent": sent_total,
                    "behind": len(behind), "hit": len(hit)})


@app.route("/api/cron/daily-summary", methods=["POST"])
def api_cron_daily_summary():
    """Designed to be hit by an external cron (cron-job.org) every
    evening (e.g. 6pm). Sends each user their daily standing.
    Auth: same X-Sync-Token used for lead sync."""
    token_required = os.environ.get("SYNC_TOKEN", "dev-token")
    if request.headers.get("X-Sync-Token") != token_required:
        return jsonify({"error": "unauthorized"}), 401

    target = 20
    today = date.today().isoformat()
    rows = db.query(
        "SELECT u.id, u.full_name, COUNT(a.id) AS calls FROM users u "
        "LEFT JOIN activity a ON a.user_id = u.id AND a.action = 'called' "
        "  AND date(a.created_at) = ? "
        "WHERE u.is_active = 1 GROUP BY u.id, u.full_name",
        (today,))
    sent = 0
    import random
    for r in rows:
        calls = r["calls"] or 0
        if calls >= target:
            line = random.choice(BANTER_HIT)
            body = f"{calls}/{target} calls today. {line}"
        elif calls >= target * 0.5:
            body = (f"{calls}/{target} calls today — "
                    f"{target - calls} more to hit goal!")
        else:
            line = random.choice(BANTER_MISS)
            body = f"Only {calls}/{target} today. {line}"
        sent += _push.send_push_to_user(r["id"], {
            "title": "Daily summary",
            "body": body,
            "tag": "daily-summary",
            "data": {"url": "/"},
        })
    return jsonify({"ok": True, "sent": sent})


# ---------- Download (desktop app + mobile install instructions) ----------

DIST_DIR = ROOT / "dist"
DOWNLOAD_FILE = "DevoxSales-Setup.exe"
APK_FILE = "DevoxSales.apk"


DOWNLOAD_HTML = r"""<!doctype html>
<html lang="el">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
<link rel="apple-touch-icon" href="/static/icon-192.png">
<link rel="icon" type="image/png" sizes="192x192" href="/static/icon-192.png">
<link rel="shortcut icon" href="/static/logo.ico">
<title>Download — Devox Sales</title>
<style>
:root {
  --bg: #0a0b0f; --surface: #12141b; --surface-2: #1a1d26;
  --surface-3: #232733; --hover: #1e222c;
  --border: #232733; --border-strong: #2f3445;
  --text: #f4f5f7; --text-2: #b6bac6; --text-3: #7c818f;
  --text-4: #555b6a;
  --brand: #4f7cff; --brand-hover: #6c8fff;
  --brand-soft: rgba(79,124,255,0.12);
  --warning: #ffb547; --warning-soft: rgba(255,181,71,0.12);
  --r-2: 6px; --r-3: 10px; --r-4: 14px;
}
* { box-sizing: border-box; }
body {
  font-family: 'Inter', -apple-system, 'Segoe UI', sans-serif;
  margin: 0;
  background: var(--bg);
  color: var(--text);
  padding: 24px;
  min-height: 100vh;
  -webkit-font-smoothing: antialiased;
  background-image:
    radial-gradient(at 50% 0%, rgba(79,124,255,0.05) 0%, transparent 60%);
}
.wrap { max-width: 640px; margin: 32px auto; }
.logo {
  display: flex; align-items: center; justify-content: center;
  margin-bottom: 12px;
}
.logo img { height: 40px; filter: brightness(0) invert(1); }
h1 {
  text-align: center; font-size: 28px;
  margin: 0 0 6px;
  font-weight: 700; letter-spacing: -0.02em;
}
.sub {
  text-align: center; color: var(--text-3);
  margin-bottom: 32px; font-size: 14px;
}
.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--r-4);
  padding: 28px;
  margin-bottom: 16px;
}
.card h2 {
  margin: 0 0 18px; font-size: 17px;
  font-weight: 600;
  display: flex; align-items: center; gap: 10px;
  letter-spacing: -0.01em;
}
.card h2 .pill {
  font-size: 10px; font-weight: 700;
  padding: 3px 8px; border-radius: 999px;
  background: var(--surface-3); color: var(--text-3);
  text-transform: uppercase; letter-spacing: 0.06em;
}
.dl-btn {
  display: inline-flex; align-items: center; justify-content: center;
  gap: 10px; background: var(--brand);
  color: white !important; text-decoration: none;
  height: 52px; padding: 0 28px;
  border-radius: var(--r-3);
  font-family: inherit;
  font-weight: 600; font-size: 15px;
  width: 100%;
  transition: background 0.12s, transform 0.08s;
}
.dl-btn:hover { background: var(--brand-hover); }
.dl-btn:active { transform: scale(0.99); }
.dl-btn.secondary {
  background: var(--surface-3); color: var(--text) !important;
}
.dl-btn.secondary:hover { background: var(--border-strong); }
.size {
  font-size: 12px; color: var(--text-3);
  margin-top: 10px; text-align: center;
  font-weight: 500;
}
ol {
  margin: 18px 0 0 0; padding-left: 22px;
  line-height: 1.7; font-size: 13px;
  color: var(--text-2);
}
ol li {
  margin-bottom: 6px;
  padding-left: 6px;
}
ol li b, ol li strong { color: var(--text); font-weight: 600; }
code {
  background: var(--bg);
  padding: 3px 7px;
  border-radius: var(--r-2);
  font-family: 'JetBrains Mono', Consolas, monospace;
  font-size: 12px;
  color: var(--brand);
  border: 1px solid var(--border);
}
.platform-tabs {
  display: flex; gap: 4px;
  background: var(--surface);
  border: 1px solid var(--border);
  padding: 4px;
  border-radius: var(--r-3);
  margin-bottom: 18px;
}
.platform-tabs button {
  flex: 1; background: transparent;
  border: 0;
  color: var(--text-3);
  padding: 12px;
  border-radius: var(--r-2);
  font-family: inherit; font-weight: 600;
  cursor: pointer; font-size: 14px;
  transition: all 0.12s;
}
.platform-tabs button:hover { color: var(--text); }
.platform-tabs button.active {
  background: var(--brand); color: white;
}
.platform-content { display: none; }
.platform-content.active { display: block; }
.notice {
  background: var(--warning-soft);
  border: 1px solid rgba(255,181,71,0.25);
  color: var(--warning);
  padding: 12px 14px;
  border-radius: var(--r-3);
  font-size: 12px; margin-top: 18px;
  line-height: 1.6;
}
.back {
  display: inline-flex; align-items: center; gap: 6px;
  margin-top: 24px;
  color: var(--text-3); text-decoration: none;
  font-size: 13px; font-weight: 500;
}
.back:hover { color: var(--brand); }
.back-wrap { text-align: center; }
</style>
</head>
<body>
<div class="wrap">
  <div class="logo"><img src="/static/logo.png" alt="Devox"></div>
  <h1>Devox Sales</h1>
  <p class="sub">Κατέβασε την εφαρμογή για τη συσκευή σου</p>

  <div class="platform-tabs">
    <button id="tab-desktop" class="active">Windows</button>
    <button id="tab-mobile">Mobile</button>
  </div>

  <div id="content-desktop" class="platform-content active">
    <div class="card">
      <h2>Windows desktop app <span class="pill">{{ desktop_size }}</span></h2>
      <a class="dl-btn" href="/download/desktop">
        Download installer
      </a>
      <div class="size">DevoxSales-Setup.exe · Windows 10 / 11</div>
      <ol>
        <li>Πάτα το κουμπί download παραπάνω</li>
        <li>Κάνε διπλό κλικ στο <code>DevoxSales-Setup.exe</code></li>
        <li>Πάτα <b>Next</b> → <b>Install</b> → <b>Finish</b></li>
        <li>Η εφαρμογή θα έχει εικονίδιο στην επιφάνεια εργασίας
          και στο Start Menu</li>
        <li>Login με τα στοιχεία που σου έδωσε ο admin</li>
      </ol>
      <div class="notice">
        Την πρώτη φορά το Windows SmartScreen ίσως εμφανίσει warning.
        Πάτησε <b>"More info"</b> → <b>"Run anyway"</b>.
      </div>
    </div>
  </div>

  <div id="content-mobile" class="platform-content">
    {% if apk_available %}
    <div class="card">
      <h2>Android <span class="pill">{{ apk_size }}</span></h2>
      <a class="dl-btn" href="/download/android">
        Download DevoxSales.apk
      </a>
      <div class="size">Android 7.0+</div>
      <ol>
        <li>Πάτα το κουμπί download παραπάνω</li>
        <li>Όταν τελειώσει, άνοιξε το αρχείο <code>DevoxSales.apk</code></li>
        <li>Αν εμφανιστεί <b>"Install unknown apps"</b>, πάτα
          <b>Settings</b> → ενεργοποίησε
          <b>"Allow from this source"</b> για τον browser σου</li>
        <li>Πίσω και πάτα <b>Install</b></li>
        <li>Άνοιξε την εφαρμογή και κάνε login</li>
        <li><b>Καθάρισμα:</b> μετά το install μπορείς να σβήσεις το
          <code>DevoxSales.apk</code> από τα Downloads — δεν χρειάζεται
          πια. Το app ήδη εγκαταστάθηκε.</li>
      </ol>
      <div class="notice" style="margin-top:14px">
        <b>Για να απεγκαταστήσεις:</b> long-press το εικονίδιο στο home
        screen → Uninstall. Ή Settings → Apps → Devox Sales → Uninstall.
        <br>Δεν χρειάζεται να ψάξεις το APK στο file manager.
      </div>
      <div class="notice">
        Επειδή το APK δεν διανέμεται μέσω Google Play, το Android
        ζητά μία φορά άδεια ότι εμπιστεύεσαι την πηγή.
      </div>
    </div>
    {% endif %}

    <div class="card">
      <h2>iPhone / iPad</h2>
      <p style="color:var(--text-2);font-size:13px;line-height:1.6;margin:0 0 14px">
        Δεν υπάρχει .apk για iOS. Πρόσθεσε την εφαρμογή στην αρχική οθόνη
        και ανοίγει σαν native app.
      </p>
      <ol>
        <li>Άνοιξε το <code>{{ host_url }}</code> στο <b>Safari</b></li>
        <li>Πάτα το κουμπί Share κάτω-κέντρο</li>
        <li>Επίλεξε <b>"Add to Home Screen"</b></li>
        <li>Πάτα <b>Add</b> πάνω δεξιά</li>
      </ol>
      <a class="dl-btn secondary" href="/" style="margin-top:18px;height:44px;font-size:14px">
        Open in browser
      </a>
    </div>

    {% if not apk_available %}
    <div class="card">
      <h2>Android — Install as PWA</h2>
      <p style="color:var(--text-2);font-size:13px;line-height:1.6;margin:0 0 14px">
        Μέχρι να γίνει διαθέσιμο το APK, μπορείς να εγκαταστήσεις
        την εφαρμογή σαν Progressive Web App.
      </p>
      <ol>
        <li>Άνοιξε το <code>{{ host_url }}</code> στο Chrome</li>
        <li>Πάτα τις 3 τελείες πάνω δεξιά</li>
        <li>Επίλεξε <b>"Install app"</b> ή <b>"Add to Home screen"</b></li>
      </ol>
    </div>
    {% endif %}
  </div>

  <div class="back-wrap">
    <a class="back" href="/">← Back to sign in</a>
  </div>
</div>

<script>
function pickPlatform(p) {
  for (const id of ['desktop', 'mobile']) {
    document.getElementById('tab-' + id).classList.toggle('active', id === p);
    document.getElementById('content-' + id).classList.toggle('active', id === p);
  }
}
document.getElementById('tab-desktop').onclick = () => pickPlatform('desktop');
document.getElementById('tab-mobile').onclick = () => pickPlatform('mobile');

const isMobile = /Android|iPhone|iPad|iPod|Mobile/i.test(navigator.userAgent);
if (isMobile) pickPlatform('mobile');
</script>
</body>
</html>
"""


@app.route("/download")
def download_page():
    desktop_path = DIST_DIR / DOWNLOAD_FILE
    if desktop_path.exists():
        size_mb = desktop_path.stat().st_size / 1024 / 1024
        desktop_size = f"{size_mb:.1f} MB"
    else:
        desktop_size = "—"

    apk_path = DIST_DIR / APK_FILE
    apk_available = apk_path.exists()
    if apk_available:
        size_mb = apk_path.stat().st_size / 1024 / 1024
        apk_size = f"{size_mb:.1f} MB"
    else:
        apk_size = "—"

    return render_template_string(
        DOWNLOAD_HTML,
        desktop_size=desktop_size,
        apk_available=apk_available,
        apk_size=apk_size,
        host_url=request.host_url.rstrip("/"))


@app.route("/download/desktop")
def download_desktop():
    if not (DIST_DIR / DOWNLOAD_FILE).exists():
        abort(404, description="Desktop build not available yet")
    return send_from_directory(
        str(DIST_DIR), DOWNLOAD_FILE, as_attachment=True,
        download_name="DevoxSales-Setup.exe")


@app.route("/.well-known/assetlinks.json")
def assetlinks():
    """Digital Asset Links — verifies the TWA-packaged Android app
    is owned by this domain. Without this, the Android app shows the
    URL bar at the top instead of running fullscreen."""
    return send_from_directory(
        str(ROOT / "static" / ".well-known"),
        "assetlinks.json",
        mimetype="application/json")


@app.route("/download/android")
def download_android():
    if not (DIST_DIR / APK_FILE).exists():
        abort(404, description="Android build not available yet")
    # APK MIME type so browsers offer to install instead of viewing as text
    response = send_from_directory(
        str(DIST_DIR), APK_FILE, as_attachment=True,
        download_name="DevoxSales.apk")
    response.headers["Content-Type"] = "application/vnd.android.package-archive"
    return response


# ---------- Main UI ----------

def _enrich_me(user_dict: dict) -> dict:
    user_dict["regions"] = get_user_regions(user_dict["id"])
    row = db.query_one(
        "SELECT avatar FROM users WHERE id = ?", (user_dict["id"],))
    user_dict["avatar"] = (row or {}).get("avatar")
    return user_dict


@app.route("/")
@auth.login_required
def index():
    user = _enrich_me(dict(g.user))
    return render_template_string(INDEX_HTML, user=user)


@app.route("/api/me")
@auth.login_required
def api_me():
    user = _enrich_me(dict(g.user))
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
