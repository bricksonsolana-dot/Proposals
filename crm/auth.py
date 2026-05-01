"""
Authentication helpers — bcrypt password hashing + Flask sessions.
"""
import functools
import bcrypt
from flask import session, redirect, url_for, jsonify, request, g

import db


def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    if not hashed:
        return False
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except (ValueError, TypeError):
        return False


def create_user(username: str, password: str, full_name: str,
                  role: str = "sales") -> int:
    if role not in ("admin", "sales"):
        raise ValueError("role must be 'admin' or 'sales'")
    db.execute(
        """INSERT INTO users (username, password_hash, full_name, role)
           VALUES (?, ?, ?, ?)""",
        (username, hash_password(password), full_name, role),
    )
    row = db.query_one("SELECT id FROM users WHERE username = ?", (username,))
    return row["id"] if row else 0


def authenticate(username: str, password: str) -> dict | None:
    user = db.query_one(
        """SELECT id, username, password_hash, full_name, role, is_active
           FROM users WHERE username = ?""", (username,))
    if not user or not user.get("is_active"):
        return None
    if not verify_password(password, user["password_hash"]):
        return None
    return {k: user[k] for k in ("id", "username", "full_name", "role")}


def login_user(user: dict):
    session["user_id"] = user["id"]
    session["username"] = user["username"]
    session["full_name"] = user["full_name"]
    session["role"] = user["role"]
    session.permanent = True


def logout_user():
    session.clear()


def current_user() -> dict | None:
    if "user_id" not in session:
        return None
    return {
        "id": session["user_id"],
        "username": session["username"],
        "full_name": session["full_name"],
        "role": session["role"],
    }


def login_required(view):
    @functools.wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            if request.path.startswith("/api/"):
                return jsonify({"error": "not authenticated"}), 401
            return redirect("/login")
        g.user = current_user()
        return view(*args, **kwargs)
    return wrapped


def admin_required(view):
    @functools.wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            if request.path.startswith("/api/"):
                return jsonify({"error": "not authenticated"}), 401
            return redirect("/login")
        if session.get("role") != "admin":
            return jsonify({"error": "admin only"}), 403
        g.user = current_user()
        return view(*args, **kwargs)
    return wrapped


# ---------- First-time seed ----------

def seed_admin_if_empty():
    """Create a default admin user if no users exist yet."""
    row = db.query_one("SELECT COUNT(*) AS n FROM users", ())
    if row and row["n"] == 0:
        create_user("admin", "admin123", "Administrator", "admin")
        print("Seeded default admin user (username=admin, password=admin123)")
        print("CHANGE THIS PASSWORD IMMEDIATELY after first login.")
