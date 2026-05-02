"""
Web Push notifications via VAPID.

VAPID keys are stored in the `config` DB table so they survive Render
deploys (the ephemeral filesystem wipes on each redeploy, which would
otherwise rotate the keys and break every existing subscription).

Order of resolution:
  1. VAPID_PUBLIC_KEY + VAPID_PRIVATE_KEY environment variables
     (override for portable / multi-environment deploys)
  2. config table rows: vapid_public, vapid_private
  3. Generate fresh on first call, persist to the config table

To send a notification, call `send_push_to_user(user_id, payload_dict)`.
"""
from __future__ import annotations

import base64
import json
import os
import sys
import threading
from pathlib import Path

ROOT = Path(__file__).parent

_vapid_lock = threading.Lock()
_vapid = None  # cached dict {public_b64, private_pem, claims_email}
_vapid_ts = 0  # epoch seconds
# Cache for 5 seconds only — long enough to batch a request's needs,
# short enough that worker processes converge on the canonical DB
# value almost immediately. Avoids the multi-worker divergence bug.
_VAPID_CACHE_TTL = 5


def _b64url_encode(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode("ascii")


def _generate_keys() -> dict:
    """Generate a fresh VAPID key pair (P-256 ECDH).

    Uses the SEC1 / TraditionalOpenSSL format ("-----BEGIN EC PRIVATE
    KEY-----") because some older pywebpush + py_vapid versions choked
    on PKCS8 ("-----BEGIN PRIVATE KEY-----").
    """
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.hazmat.primitives import serialization

    private_key = ec.generate_private_key(ec.SECP256R1())
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("ascii")
    public_numbers = private_key.public_key().public_numbers()
    public_raw = (
        b"\x04" +
        public_numbers.x.to_bytes(32, "big") +
        public_numbers.y.to_bytes(32, "big")
    )
    public_b64 = _b64url_encode(public_raw)
    return {"private_pem": private_pem, "public_b64": public_b64}


def _validate_pem(pem: str) -> bool:
    """Confirm a PEM string actually parses as an EC private key."""
    if not pem or not isinstance(pem, str):
        return False
    try:
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.asymmetric import ec
        key = serialization.load_pem_private_key(
            pem.encode("ascii"), password=None)
        return isinstance(key, ec.EllipticCurvePrivateKey)
    except Exception as e:
        print(f"[push] PEM validation failed: {type(e).__name__}: {e}",
              flush=True)
        return False


def _normalize_pem(pem: str) -> str | None:
    """Re-encode any loadable EC private key as SEC1
    ('-----BEGIN EC PRIVATE KEY-----'). pywebpush + py_vapid handle
    SEC1 reliably; PKCS8 ('-----BEGIN PRIVATE KEY-----') has bitten us
    before. Returns None if the input doesn't parse."""
    if not pem or not isinstance(pem, str):
        return None
    try:
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.asymmetric import ec
        key = serialization.load_pem_private_key(
            pem.encode("ascii"), password=None)
        if not isinstance(key, ec.EllipticCurvePrivateKey):
            return None
        return key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        ).decode("ascii")
    except Exception:
        return None


def _config_get(key: str) -> str | None:
    import db
    row = db.query_one(
        "SELECT value FROM config WHERE key = ?", (key,))
    return row["value"] if row else None


def _config_set(key: str, value: str):
    import db
    existing = db.query_one(
        "SELECT key FROM config WHERE key = ?", (key,))
    if existing:
        db.execute(
            "UPDATE config SET value = ?, updated_at = CURRENT_TIMESTAMP "
            "WHERE key = ?", (value, key))
    else:
        db.execute(
            "INSERT INTO config (key, value) VALUES (?, ?)", (key, value))


def _load_or_generate() -> dict:
    """Load VAPID keys from env or DB config table; generate if missing.

    NO in-process caching. Each call hits the DB. With the connection
    pool this costs ~5ms and avoids the multi-worker bug where
    Worker A would regenerate keys but Worker B would keep signing
    with its stale cached private key — push gateway then rejects
    everything because the subscription's public key doesn't match
    the signing private key."""
    global _vapid, _vapid_ts
    import time as _t
    now = _t.time()
    with _vapid_lock:
        # Env override (highest priority)
        env_pub = os.environ.get("VAPID_PUBLIC_KEY")
        env_priv = os.environ.get("VAPID_PRIVATE_KEY")
        claims_email = os.environ.get(
            "VAPID_CLAIM_EMAIL", "mailto:noreply@devox.gr")
        if env_pub and env_priv:
            return {
                "public_b64": env_pub,
                "private_pem": env_priv.replace("\\n", "\n"),
                "claims_email": claims_email,
            }
        # DB-backed (persists across Render deploys)
        try:
            db_pub = _config_get("vapid_public")
            db_priv = _config_get("vapid_private")
            if db_pub and db_priv:
                # Re-encode the stored key as SEC1 every time we load
                # it. pywebpush / py_vapid have historically choked on
                # PKCS8 PEM ("-----BEGIN PRIVATE KEY-----"); SEC1
                # ("-----BEGIN EC PRIVATE KEY-----") works everywhere.
                normalized = _normalize_pem(db_priv)
                if normalized:
                    # If the on-disk format wasn't SEC1, write back the
                    # normalized version so future reads skip this step.
                    if normalized != db_priv:
                        try:
                            _config_set("vapid_private", normalized)
                            print("[push] re-encoded DB private key "
                                  "as SEC1", flush=True)
                        except Exception:
                            pass
                    print(f"[push] loaded VAPID keys from DB "
                          f"(public={db_pub[:12]}...)", flush=True)
                    return {
                        "public_b64": db_pub,
                        "private_pem": normalized,
                        "claims_email": claims_email,
                    }
                else:
                    print("[push] DB-stored VAPID private key did "
                          "not parse, regenerating", flush=True)
            elif db_pub or db_priv:
                print("[push] DB VAPID keys partial/missing, "
                      "regenerating", flush=True)
        except Exception as e:
            print(f"[push] DB read failed: {e}", flush=True)

        # First run OR previous keys broken — generate fresh, persist
        keys = _generate_keys()
        if not _validate_pem(keys["private_pem"]):
            print("[push] FATAL: freshly generated PEM failed to "
                  "validate — pywebpush will not work", flush=True)
        try:
            _config_set("vapid_public", keys["public_b64"])
            _config_set("vapid_private", keys["private_pem"])
            print(f"[push] generated and persisted new VAPID keys "
                  f"(public={keys['public_b64'][:12]}...)", flush=True)
        except Exception as e:
            print(f"[push] DB write failed, keys won't persist: {e}",
                  flush=True)

        # Re-read from DB so we use the canonical version (in case a
        # sibling worker already generated a different key and
        # raced us — the LAST writer wins, and we want every worker
        # to converge on whatever ended up persisted).
        try:
            db_pub = _config_get("vapid_public")
            db_priv = _config_get("vapid_private")
            normalized = _normalize_pem(db_priv) if db_priv else None
            if db_pub and normalized:
                keys = {"public_b64": db_pub, "private_pem": normalized}
                if db_pub != keys.get("public_b64"):
                    print("[push] race detected — using sibling "
                          "worker's keys", flush=True)
        except Exception:
            pass

        keys["claims_email"] = claims_email
        # Wipe stale subs (signed against any older key)
        try:
            import db as _db
            row = _db.query_one(
                "SELECT COUNT(*) AS n FROM push_subscriptions", ())
            n = (row or {}).get("n", 0) if row else 0
            if n:
                _db.execute("DELETE FROM push_subscriptions", ())
                print(f"[push] wiped {n} stale subscription(s) after "
                      f"VAPID key rotation", flush=True)
        except Exception as e:
            print(f"[push] could not wipe stale subs: {e}", flush=True)
        return keys


def public_key() -> str:
    """Return the VAPID public key (base64url) for the frontend."""
    return _load_or_generate()["public_b64"]


def send_push_to_user(user_id: int, payload: dict) -> int:
    import db
    subs = db.query(
        "SELECT id, endpoint, p256dh, auth FROM push_subscriptions "
        "WHERE user_id = ?", (user_id,))
    if not subs:
        print(f"[push] user {user_id} has no subscriptions", flush=True)
        return 0
    return _send_to_subscriptions(subs, payload)


def send_push_to_users(user_ids: list[int], payload: dict) -> int:
    if not user_ids:
        return 0
    import db
    placeholders = ",".join("?" * len(user_ids))
    subs = db.query(
        f"SELECT id, endpoint, p256dh, auth FROM push_subscriptions "
        f"WHERE user_id IN ({placeholders})",
        tuple(user_ids))
    return _send_to_subscriptions(subs, payload)


def _send_to_subscriptions(subs, payload: dict) -> int:
    if not subs:
        return 0
    try:
        from pywebpush import webpush, WebPushException
        import pywebpush as _pwp_mod
        _pwp_ver = getattr(_pwp_mod, "__version__", "unknown")
    except ImportError as e:
        print(f"[push] pywebpush not installed: {e}", flush=True)
        return 0
    cfg = _load_or_generate()
    pem = cfg["private_pem"]
    pem_first_line = pem.split("\n", 1)[0] if pem else ""
    print(f"[push] using pywebpush={_pwp_ver}, PEM starts: "
          f"{pem_first_line!r} (len={len(pem)}, "
          f"public_b64_prefix={cfg['public_b64'][:12]})",
          flush=True)
    body = json.dumps(payload, ensure_ascii=False)
    sent = 0
    dead = []
    errors = []  # list of (sub_id, error_string)
    import db
    for s in subs:
        info = {
            "endpoint": s["endpoint"],
            "keys": {"p256dh": s["p256dh"], "auth": s["auth"]},
        }
        try:
            webpush(
                subscription_info=info,
                data=body,
                vapid_private_key=cfg["private_pem"],
                vapid_claims={"sub": cfg["claims_email"]},
                ttl=60 * 60,
            )
            sent += 1
            # Clear any prior error from a successful send
            try:
                db.execute(
                    "UPDATE push_subscriptions SET last_error = NULL, "
                    "last_error_at = NULL WHERE id = ?", (s["id"],))
            except Exception:
                pass
        except WebPushException as e:
            status = getattr(getattr(e, "response", None),
                             "status_code", 0)
            err = f"HTTP {status}: {str(e)[:200]}"
            print(f"[push] WebPushException status={status} "
                  f"endpoint={s['endpoint'][:60]}... err={e}", flush=True)
            errors.append((s["id"], err))
            # 401 = bad VAPID signature (key rotated server-side, the
            # subscription is now orphaned). 403 = forbidden (app server
            # not authorised). 404 / 410 = endpoint gone. All four mean
            # this subscription is permanently dead — remove it.
            if status in (401, 403, 404, 410):
                dead.append(s["id"])
        except Exception as e:
            err = f"{type(e).__name__}: {str(e)[:200]}"
            print(f"[push] unexpected error: {err}", flush=True)
            errors.append((s["id"], err))
            import traceback
            traceback.print_exc(file=sys.stderr)
    # Persist last_error per subscription
    for sid, err in errors:
        if sid in dead:
            continue  # we'll delete below
        try:
            db.execute(
                "UPDATE push_subscriptions SET last_error = ?, "
                "last_error_at = CURRENT_TIMESTAMP WHERE id = ?",
                (err, sid))
        except Exception:
            pass
    if dead:
        for sid in dead:
            try:
                db.execute(
                    "DELETE FROM push_subscriptions WHERE id = ?", (sid,))
            except Exception:
                pass
        print(f"[push] removed {len(dead)} dead subscription(s)",
              flush=True)
    print(f"[push] sent {sent}/{len(subs)} successfully", flush=True)
    return sent
