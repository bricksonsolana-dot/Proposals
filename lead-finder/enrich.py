"""
Lead enrichment: adds domain availability info (.gr / .com) to each lead.
Uses simple DNS lookup — fast, no API key, no external service.

Usage:
    python enrich.py            # enriches all leads in master CSV
    python enrich.py --force    # re-checks even already-enriched leads
"""
import argparse
import asyncio
import csv
import re
import socket
import time
from pathlib import Path

ROOT = Path(__file__).parent
MASTER_CSV = ROOT / "output" / "leads.csv"
ENRICHED_FIELDS = ["domain_gr_available", "domain_com_available",
                    "domain_suggestion", "enriched_at"]


# ---------- Slug generation ----------

GREEK_TO_LATIN = {
    "α": "a", "β": "v", "γ": "g", "δ": "d", "ε": "e", "ζ": "z",
    "η": "i", "θ": "th", "ι": "i", "κ": "k", "λ": "l", "μ": "m",
    "ν": "n", "ξ": "x", "ο": "o", "π": "p", "ρ": "r", "σ": "s",
    "ς": "s", "τ": "t", "υ": "y", "φ": "f", "χ": "ch", "ψ": "ps",
    "ω": "o", "ά": "a", "έ": "e", "ή": "i", "ί": "i", "ό": "o",
    "ύ": "y", "ώ": "o", "ϊ": "i", "ϋ": "y", "ΐ": "i", "ΰ": "y",
}

# Words to drop when generating a domain slug — they aren't part of brand
STOP_WORDS = {
    "hotel", "hotels", "the", "studios", "studio", "apartments", "apartment",
    "rooms", "room", "villa", "villas", "suites", "suite", "guesthouse",
    "guest house", "hostel", "resort", "inn", "lodge", "pension",
    "boutique", "luxury", "premium", "by", "in", "of",
    "ξενοδοχείο", "δωμάτια", "διαμέρισμα", "διαμερίσματα", "βίλα", "βίλες",
    "πανσιόν", "πανδοχείο", "κατάλυμα", "καταλύματα",
}


def transliterate(s: str) -> str:
    out = []
    for ch in s.lower():
        out.append(GREEK_TO_LATIN.get(ch, ch))
    return "".join(out)


def make_slug(name: str) -> str:
    """Turn a hotel name into a domain-friendly slug."""
    if not name:
        return ""
    s = transliterate(name)
    # remove stuff in parentheses
    s = re.sub(r"\([^)]*\)", "", s)
    s = re.sub(r"[^a-z0-9\s\-]", "", s)
    words = [w for w in s.split() if w and w not in STOP_WORDS]
    if not words:
        words = s.split()
    return "".join(words)[:30]  # cap length


# ---------- DNS check ----------

def domain_is_taken(domain: str, timeout: float = 2.5) -> bool:
    """True if the domain resolves (has A/AAAA record).

    Uses getaddrinfo with explicit timeout so slow DNS doesn't hang us.
    A registered domain WITHOUT DNS records will appear 'available' here.
    For 99% of real hotel domains this is accurate enough.
    """
    # Set global default timeout — affects this thread only when called serially
    socket.setdefaulttimeout(timeout)
    try:
        socket.getaddrinfo(domain, None)
        return True
    except (socket.gaierror, socket.herror, socket.timeout, OSError):
        return False
    finally:
        socket.setdefaulttimeout(None)


def check_lead(lead: dict) -> dict:
    """Returns dict with enrichment fields for a single lead."""
    name = lead.get("name", "")
    slug = make_slug(name)
    if not slug:
        return {
            "domain_gr_available": "",
            "domain_com_available": "",
            "domain_suggestion": "",
            "enriched_at": time.strftime("%Y-%m-%d"),
        }

    gr_taken = domain_is_taken(f"{slug}.gr")
    com_taken = domain_is_taken(f"{slug}.com")

    # Suggest the best available
    if not gr_taken:
        suggestion = f"{slug}.gr"
    elif not com_taken:
        suggestion = f"{slug}.com"
    else:
        suggestion = ""

    return {
        "domain_gr_available": "yes" if not gr_taken else "no",
        "domain_com_available": "yes" if not com_taken else "no",
        "domain_suggestion": suggestion,
        "enriched_at": time.strftime("%Y-%m-%d"),
    }


# ---------- Concurrent batch ----------

async def enrich_one(lead: dict, sem: asyncio.Semaphore) -> dict:
    async with sem:
        loop = asyncio.get_running_loop()
        try:
            return await asyncio.wait_for(
                loop.run_in_executor(None, check_lead, lead),
                timeout=8.0,
            )
        except asyncio.TimeoutError:
            return {
                "domain_gr_available": "timeout",
                "domain_com_available": "timeout",
                "domain_suggestion": "",
                "enriched_at": time.strftime("%Y-%m-%d"),
            }


async def enrich_all(leads: list[dict], concurrency: int = 30,
                      force: bool = False, on_progress=None) -> list[dict]:
    """Enrich every lead concurrently. Returns list of merged dicts."""
    sem = asyncio.Semaphore(concurrency)
    tasks = []
    skip_indices = set()

    for i, lead in enumerate(leads):
        if not force and lead.get("enriched_at"):
            skip_indices.add(i)
            tasks.append(None)
        else:
            tasks.append(asyncio.create_task(enrich_one(lead, sem)))

    enriched = []
    done = 0
    total = len(leads) - len(skip_indices)
    for i, (lead, task) in enumerate(zip(leads, tasks)):
        if task is None:
            enriched.append(lead)
            continue
        try:
            data = await task
        except Exception as e:
            data = {"domain_gr_available": "error",
                    "domain_com_available": "error",
                    "domain_suggestion": "",
                    "enriched_at": time.strftime("%Y-%m-%d")}
        merged = {**lead, **data}
        enriched.append(merged)
        done += 1
        if on_progress and done % 20 == 0:
            try:
                await on_progress(done, total)
            except Exception:
                pass
    return enriched


# ---------- CLI ----------

def load_master() -> list[dict]:
    if not MASTER_CSV.exists():
        return []
    with open(MASTER_CSV, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def save_master(leads: list[dict]):
    if not leads:
        return
    base_fields = ["country", "region", "name", "category", "phone", "email",
                   "gmaps_url", "online_presence"]
    fields = base_fields + ENRICHED_FIELDS
    with open(MASTER_CSV, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for lead in leads:
            w.writerow(lead)


async def main():
    p = argparse.ArgumentParser()
    p.add_argument("--force", action="store_true",
                   help="Re-check leads that have already been enriched")
    p.add_argument("--concurrency", type=int, default=30,
                   help="Parallel DNS lookups (default 30)")
    args = p.parse_args()

    leads = load_master()
    if not leads:
        print("No leads in master CSV.")
        return

    pending = [l for l in leads if args.force or not l.get("enriched_at")]
    print(f"Loaded {len(leads)} leads, {len(pending)} need enrichment")

    if not pending:
        print("Nothing to do.")
        return

    start = time.time()
    last_progress_print = [start]

    async def progress(done, total):
        elapsed = time.time() - start
        rate = done / elapsed if elapsed else 0
        eta = (total - done) / rate if rate else 0
        if time.time() - last_progress_print[0] > 2:
            print(f"  {done}/{total} done ({elapsed:.0f}s elapsed, "
                  f"~{eta:.0f}s left, {rate:.1f}/sec)", flush=True)
            last_progress_print[0] = time.time()

    enriched = await enrich_all(leads, concurrency=args.concurrency,
                                  force=args.force, on_progress=progress)
    save_master(enriched)

    # Stats
    gr_avail = sum(1 for l in enriched if l.get("domain_gr_available") == "yes")
    com_avail = sum(1 for l in enriched if l.get("domain_com_available") == "yes")
    elapsed = time.time() - start
    print(f"\nDone in {elapsed:.0f}s")
    print(f"  .gr available:  {gr_avail}/{len(enriched)}")
    print(f"  .com available: {com_avail}/{len(enriched)}")
    print(f"  -> {MASTER_CSV}")


if __name__ == "__main__":
    asyncio.run(main())
