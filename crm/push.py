"""
Web Push notifications via VAPID.

The first time the server starts, generates a VAPID key pair and stores
it in `data/.vapid_keys`. The public key (base64 url-safe) is what the
frontend needs to subscribe to push.

To send a notification, call `send_push_to_user(user_id, payload_dict)`.
The function looks up every push subscription for that user, signs and
sends the notification, and prunes any subscription that comes back
with HTTP 410 Gone.
"""
from __future__ import annotations

import base64
import json
import os
import threading
from pathlib import Path

ROOT = Path(__file__).parent
VAPID_FILE = ROOT / "data" / ".vapid_keys"

_vapid_lock = threading.Lock()
_vapid = None  # cached dict {public, private, claims_email}


def _b64url_encode(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode("ascii")


def _generate_keys() -> dict:
    """Generate a fresh VAPID key pair (P-256 ECDH)."""
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.hazmat.primitives import serialization

    private_key = ec.generate_private_key(ec.SECP256R1())
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("ascii")
    # Public key as raw 65-byte point (0x04 + X + Y), then base64url
    public_numbers = private_key.public_key().public_numbers()
    public_raw = (
        b"\x04" +
        public_numbers.x.to_bytes(32, "big") +
        public_numbers.y.to_bytes(32, "big")
    )
    public_b64 = _b64url_encode(public_raw)
    return {"private_pem": private_pem, "public_b64": public_b64}


def _load_or_generate() -> dict:
    """Load VAPID keys from env vars or from the persisted file. If none
    exist yet, generate a fresh pair and persist it next to the secret
    key file."""
    global _vapid
    if _vapid is not None:
        return _vapid
    with _vapid_lock:
        if _vapid is not None:
            return _vapid
        # Env override takes priority (for portable deploys / CI)
        env_pub = os.environ.get("VAPID_PUBLIC_KEY")
        env_priv = os.environ.get("VAPID_PRIVATE_KEY")
        if env_pub and env_priv:
            _vapid = {
                "public_b64": env_pub,
                "private_pem": env_priv.replace("\\n", "\n"),
                "claims_email": os.environ.get(
                    "VAPID_CLAIM_EMAIL", "mailto:noreply@devox.gr"),
            }
            return _vapid
        # Otherwise persist locally
        VAPID_FILE.parent.mkdir(parents=True, exist_ok=True)
        if VAPID_FILE.exists():
            try:
                _vapid = json.loads(VAPID_FILE.read_text(encoding="utf-8"))
                _vapid.setdefault("claims_email", "mailto:noreply@devox.gr")
                return _vapid
            except Exception:
                pass
        keys = _generate_keys()
        keys["claims_email"] = "mailto:noreply@devox.gr"
        VAPID_FILE.write_text(
            json.dumps(keys, indent=2), encoding="utf-8")
        _vapid = keys
        return _vapid


def public_key() -> str:
    """Return the VAPID public key (base64url) for the frontend to
    subscribe."""
    return _load_or_generate()["public_b64"]


def send_push_to_user(user_id: int, payload: dict) -> int:
    """Send a push to every active subscription for `user_id`. Prunes
    410-Gone subs. Returns the count of successful sends."""
    import db
    subs = db.query(
        "SELECT id, endpoint, p256dh, auth FROM push_subscriptions "
        "WHERE user_id = ?", (user_id,))
    if not subs:
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
    except ImportError:
        # If pywebpush isn't installed yet (Render hasn't redeployed),
        # silently skip — the call site never wants to crash on this.
        return 0
    cfg = _load_or_generate()
    body = json.dumps(payload, ensure_ascii=False)
    sent = 0
    dead = []
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
                ttl=60 * 60,  # 1h — drop notifications older than that
            )
            sent += 1
        except WebPushException as e:
            status = getattr(getattr(e, "response", None), "status_code", 0)
            # 404 / 410: subscription expired or unsubscribed
            if status in (404, 410):
                dead.append(s["id"])
        except Exception:
            pass
    if dead:
        import db
        for sid in dead:
            try:
                db.execute(
                    "DELETE FROM push_subscriptions WHERE id = ?", (sid,))
            except Exception:
                pass
    return sent
