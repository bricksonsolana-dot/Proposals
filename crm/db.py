"""
DB abstraction layer.

Detects backend from DATABASE_URL env var:
  - If empty or starts with "sqlite:", uses SQLite (local file)
  - If starts with "postgresql://" or "postgres://", uses Postgres

Same query syntax works in both: we use ? placeholders and convert to %s
for Postgres.
"""
import os
import re
import sqlite3
import threading
from contextlib import contextmanager
from pathlib import Path

ROOT = Path(__file__).parent

# Load .env before reading DATABASE_URL
try:
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env")
except ImportError:
    pass

DEFAULT_SQLITE_PATH = ROOT / "data" / "crm.db"

DATABASE_URL = os.environ.get("DATABASE_URL", "")
IS_POSTGRES = DATABASE_URL.startswith(("postgresql://", "postgres://"))

# Threading lock for SQLite (Postgres handles concurrency natively)
_sqlite_lock = threading.Lock()


def _get_pg_conn():
    import psycopg2
    import psycopg2.extras
    url = DATABASE_URL
    if url.startswith("postgres://"):
        url = "postgresql://" + url[len("postgres://"):]
    conn = psycopg2.connect(url)
    conn.autocommit = False
    return conn


def _get_sqlite_conn():
    DEFAULT_SQLITE_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DEFAULT_SQLITE_PATH), check_same_thread=False,
                            isolation_level=None)  # autocommit
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


@contextmanager
def get_conn():
    """Yield a connection, commit on success / rollback on error."""
    if IS_POSTGRES:
        conn = _get_pg_conn()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    else:
        with _sqlite_lock:
            conn = _get_sqlite_conn()
            try:
                yield conn
            finally:
                conn.close()


def _convert_placeholders(sql: str) -> str:
    """Convert ? placeholders to %s for Postgres."""
    if not IS_POSTGRES:
        return sql
    # Naive but works for our queries (no ? inside strings)
    return sql.replace("?", "%s")


def query(sql: str, params: tuple = ()) -> list[dict]:
    """Run SELECT and return list of dicts."""
    sql = _convert_placeholders(sql)
    with get_conn() as conn:
        if IS_POSTGRES:
            import psycopg2.extras
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute(sql, params)
            rows = cur.fetchall()
            return [dict(r) for r in rows]
        else:
            cur = conn.execute(sql, params)
            return [dict(r) for r in cur.fetchall()]


def query_one(sql: str, params: tuple = ()) -> dict | None:
    rows = query(sql, params)
    return rows[0] if rows else None


def execute(sql: str, params: tuple = ()) -> int:
    """Run INSERT/UPDATE/DELETE. Returns last inserted id (when applicable)."""
    sql = _convert_placeholders(sql)
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(sql, params)
        try:
            return cur.lastrowid if hasattr(cur, "lastrowid") else 0
        except Exception:
            return 0


def execute_many(sql: str, params_list: list[tuple]):
    sql = _convert_placeholders(sql)
    with get_conn() as conn:
        cur = conn.cursor()
        cur.executemany(sql, params_list)


# ----------- Schema -----------

SCHEMA_SQLITE = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'sales',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS leads (
    phone TEXT PRIMARY KEY,
    region TEXT,
    name TEXT,
    category TEXT,
    email TEXT,
    gmaps_url TEXT,
    online_presence TEXT,
    domain_gr_available TEXT,
    domain_com_available TEXT,
    domain_suggestion TEXT,
    enriched_at TEXT,
    properties TEXT,                     -- JSON list of all listings sharing this phone
    imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS lead_state (
    lead_phone TEXT PRIMARY KEY,
    status TEXT NOT NULL DEFAULT 'new',
    assigned_to INTEGER,
    follow_up_date DATE,
    last_contact_at TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (lead_phone) REFERENCES leads(phone) ON DELETE CASCADE,
    FOREIGN KEY (assigned_to) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS activity (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lead_phone TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    action TEXT NOT NULL,
    details TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (lead_phone) REFERENCES leads(phone) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS favorites (
    user_id INTEGER NOT NULL,
    lead_phone TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, lead_phone),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (lead_phone) REFERENCES leads(phone) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS user_regions (
    user_id INTEGER NOT NULL,
    region TEXT NOT NULL,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, region),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_lead_state_assigned ON lead_state(assigned_to);
CREATE INDEX IF NOT EXISTS idx_lead_state_status ON lead_state(status);
CREATE INDEX IF NOT EXISTS idx_activity_lead ON activity(lead_phone);
CREATE INDEX IF NOT EXISTS idx_activity_user_date ON activity(user_id, created_at);
CREATE INDEX IF NOT EXISTS idx_favorites_user ON favorites(user_id);
CREATE INDEX IF NOT EXISTS idx_user_regions_user ON user_regions(user_id);
CREATE INDEX IF NOT EXISTS idx_user_regions_region ON user_regions(region);
"""

SCHEMA_POSTGRES = """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'sales',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS leads (
    phone TEXT PRIMARY KEY,
    region TEXT,
    name TEXT,
    category TEXT,
    email TEXT,
    gmaps_url TEXT,
    online_presence TEXT,
    domain_gr_available TEXT,
    domain_com_available TEXT,
    domain_suggestion TEXT,
    enriched_at TEXT,
    properties TEXT,                     -- JSON list of all listings sharing this phone
    imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS lead_state (
    lead_phone TEXT PRIMARY KEY REFERENCES leads(phone) ON DELETE CASCADE,
    status TEXT NOT NULL DEFAULT 'new',
    assigned_to INTEGER REFERENCES users(id) ON DELETE SET NULL,
    follow_up_date DATE,
    last_contact_at TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS activity (
    id SERIAL PRIMARY KEY,
    lead_phone TEXT NOT NULL REFERENCES leads(phone) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    action TEXT NOT NULL,
    details TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS favorites (
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    lead_phone TEXT NOT NULL REFERENCES leads(phone) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, lead_phone)
);

CREATE TABLE IF NOT EXISTS user_regions (
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    region TEXT NOT NULL,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, region)
);

CREATE INDEX IF NOT EXISTS idx_lead_state_assigned ON lead_state(assigned_to);
CREATE INDEX IF NOT EXISTS idx_lead_state_status ON lead_state(status);
CREATE INDEX IF NOT EXISTS idx_activity_lead ON activity(lead_phone);
CREATE INDEX IF NOT EXISTS idx_activity_user_date ON activity(user_id, created_at);
CREATE INDEX IF NOT EXISTS idx_favorites_user ON favorites(user_id);
CREATE INDEX IF NOT EXISTS idx_user_regions_user ON user_regions(user_id);
CREATE INDEX IF NOT EXISTS idx_user_regions_region ON user_regions(region);
"""


def _migrate_add_column(table: str, column: str, coltype: str):
    """Add a column to an existing table if it doesn't exist (idempotent)."""
    if IS_POSTGRES:
        sql = (f"ALTER TABLE {table} "
                f"ADD COLUMN IF NOT EXISTS {column} {coltype}")
        try:
            with get_conn() as conn:
                conn.cursor().execute(sql)
        except Exception:
            pass
    else:
        # SQLite: introspect and add if missing
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute(f"PRAGMA table_info({table})")
            cols = {row[1] for row in cur.fetchall()}
            if column not in cols:
                try:
                    cur.execute(
                        f"ALTER TABLE {table} ADD COLUMN {column} {coltype}")
                except Exception:
                    pass


def init_schema():
    schema = SCHEMA_POSTGRES if IS_POSTGRES else SCHEMA_SQLITE
    with get_conn() as conn:
        cur = conn.cursor()
        # SQLite executescript handles multiple statements
        if IS_POSTGRES:
            for stmt in schema.split(";\n\n"):
                stmt = stmt.strip()
                if stmt:
                    cur.execute(stmt)
        else:
            cur.executescript(schema)
    # Migrations for existing DBs
    _migrate_add_column("leads", "properties", "TEXT")


if __name__ == "__main__":
    init_schema()
    backend = "Postgres" if IS_POSTGRES else f"SQLite ({DEFAULT_SQLITE_PATH})"
    print(f"Schema initialized in {backend}")
