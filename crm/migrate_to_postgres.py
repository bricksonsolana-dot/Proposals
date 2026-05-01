"""
Migrates existing data from local SQLite to Postgres (e.g. Supabase).

Reads SQLite from data/crm.db and writes to the Postgres URL set in
DATABASE_URL (env var or .env file).

Run with:
    python migrate_to_postgres.py

Idempotent: re-running upserts the same rows without creating duplicates.
"""
import os
import sqlite3
import sys
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent / ".env")
except ImportError:
    pass

import psycopg2
import psycopg2.extras

ROOT = Path(__file__).parent
SQLITE_PATH = ROOT / "data" / "crm.db"


def get_pg_conn():
    url = os.environ.get("DATABASE_URL", "")
    if not url:
        print("ERROR: DATABASE_URL not set. Add it to .env or environment.")
        sys.exit(1)
    if url.startswith("postgres://"):
        url = "postgresql://" + url[len("postgres://"):]
    return psycopg2.connect(url)


def get_sqlite_conn():
    if not SQLITE_PATH.exists():
        print(f"ERROR: {SQLITE_PATH} not found")
        sys.exit(1)
    conn = sqlite3.connect(str(SQLITE_PATH))
    conn.row_factory = sqlite3.Row
    return conn


SCHEMA_PG = """
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
    properties TEXT,
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

CREATE INDEX IF NOT EXISTS idx_lead_state_assigned ON lead_state(assigned_to);
CREATE INDEX IF NOT EXISTS idx_lead_state_status ON lead_state(status);
CREATE INDEX IF NOT EXISTS idx_activity_lead ON activity(lead_phone);
CREATE INDEX IF NOT EXISTS idx_activity_user_date ON activity(user_id, created_at);
CREATE INDEX IF NOT EXISTS idx_favorites_user ON favorites(user_id);
"""


def apply_schema(pg):
    cur = pg.cursor()
    for stmt in SCHEMA_PG.strip().split(";"):
        s = stmt.strip()
        if s:
            cur.execute(s)
    pg.commit()
    print("✓ schema applied")


def migrate_table(sqlite_conn, pg, table: str, columns: list[str],
                    conflict_cols: list[str]):
    src = sqlite_conn.execute(f"SELECT * FROM {table}").fetchall()
    if not src:
        print(f"  {table}: 0 rows")
        return

    cols_sql = ", ".join(columns)
    placeholders = ", ".join(["%s"] * len(columns))
    conflict_sql = ", ".join(conflict_cols)
    update_set = ", ".join(
        f"{c} = EXCLUDED.{c}" for c in columns if c not in conflict_cols)
    if update_set:
        upsert = (
            f"INSERT INTO {table} ({cols_sql}) VALUES ({placeholders}) "
            f"ON CONFLICT ({conflict_sql}) DO UPDATE SET {update_set}")
    else:
        upsert = (
            f"INSERT INTO {table} ({cols_sql}) VALUES ({placeholders}) "
            f"ON CONFLICT ({conflict_sql}) DO NOTHING")

    cur = pg.cursor()
    rows = [tuple(r[c] for c in columns) for r in src]
    psycopg2.extras.execute_batch(cur, upsert, rows, page_size=200)
    pg.commit()
    print(f"  {table}: {len(rows)} rows migrated")


def main():
    pg = get_pg_conn()
    print(f"✓ Connected to Postgres")
    apply_schema(pg)

    sqlite_conn = get_sqlite_conn()
    print(f"✓ Reading from {SQLITE_PATH}")
    print()
    print("Migrating tables...")

    # Order matters: users → leads → lead_state → activity → favorites
    migrate_table(sqlite_conn, pg, "users",
                    ["id", "username", "password_hash", "full_name",
                     "role", "created_at", "is_active"],
                    ["id"])

    migrate_table(sqlite_conn, pg, "leads",
                    ["phone", "region", "name", "category", "email",
                     "gmaps_url", "online_presence", "domain_gr_available",
                     "domain_com_available", "domain_suggestion",
                     "enriched_at", "properties", "imported_at"],
                    ["phone"])

    migrate_table(sqlite_conn, pg, "lead_state",
                    ["lead_phone", "status", "assigned_to",
                     "follow_up_date", "last_contact_at", "updated_at"],
                    ["lead_phone"])

    migrate_table(sqlite_conn, pg, "activity",
                    ["id", "lead_phone", "user_id", "action",
                     "details", "created_at"],
                    ["id"])

    migrate_table(sqlite_conn, pg, "favorites",
                    ["user_id", "lead_phone", "created_at"],
                    ["user_id", "lead_phone"])

    # Reset sequences so new INSERTs don't conflict with migrated IDs
    print()
    print("Resetting sequences...")
    cur = pg.cursor()
    for table, col in [("users", "id"), ("activity", "id")]:
        cur.execute(
            f"SELECT setval(pg_get_serial_sequence('{table}', '{col}'), "
            f"COALESCE((SELECT MAX({col}) FROM {table}), 1), true)")
        print(f"  {table}.{col} sequence reset")
    pg.commit()

    # Final counts
    print()
    print("Final row counts in Postgres:")
    for t in ["users", "leads", "lead_state", "activity", "favorites"]:
        cur.execute(f"SELECT COUNT(*) FROM {t}")
        print(f"  {t}: {cur.fetchone()[0]}")

    sqlite_conn.close()
    pg.close()
    print()
    print("✅ Migration complete.")


if __name__ == "__main__":
    main()
