"""
Google Maps scraper for tourist accommodations.
Searches "<query>" on Google Maps, scrolls the result panel until exhausted,
extracts name/phone/website/address from each card, and yields dicts.

Filters: keeps only entries with phone AND no real website (only OTAs allowed).
"""
import asyncio
import re
import urllib.parse
from playwright.async_api import async_playwright, TimeoutError as PWTimeout

USER_AGENT = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
              "AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/124.0.0.0 Safari/537.36")

# Allowed accommodation categories (substring match, case-insensitive).
# A Google Maps category is kept only if any of these substrings appears.
ACCOMMODATION_CATEGORIES = [
    "hotel", "motel", "resort", "inn",
    "apartment", "apartments",
    "guest house", "guesthouse",
    "hostel", "lodge", "lodging",
    "bed & breakfast", "bed and breakfast",
    "vacation", "holiday", "villa",
    "rooms", "rented room", "self-catering",
    "pension", "boutique",
    # Greek
    "ξενοδοχ", "ξενώνας", "ξενώνες", "δωμάτι", "διαμέρισμα",
    "διαμερίσματα", "πανσιόν", "πανδοχ", "βίλα", "βίλες",
    "κατάλυμα", "καταλύματα", "ενοικιαζ",
]

# Categories that should NEVER pass even if name contains "studio" etc.
BLOCKED_CATEGORY_HINTS = [
    "tattoo", "recording", "rehearsal", "dance",
    "yoga", "pilates", "fitness", "gym",
    "photography", "photo studio",
    "real estate", "rental agency",
    "music", "art studio", "design", "architect",
    "salon", "barber", "nail", "beauty",
    "gallery", "museum", "school", "academy",
    "office", "coworking",
    "restaurant", "cafe", "bar ", "bakery",
    "shop", "store", "supermarket", "pharmacy",
    "car rental", "boat rental", "scooter",
    "tour", "travel agency", "agency",
]


OTA_DOMAINS = [
    # Major OTAs
    "booking.com", "airbnb.com", "expedia.com", "hotels.com",
    "tripadvisor.com", "agoda.com", "trivago.com", "vrbo.com",
    "hostelworld.com", "kayak.com", "skyscanner",
    # Aggregators / meta-search
    "bluepillow.com", "hotelscheck-in.com", "hotels-check-in.com",
    "freecancellations.com", "snaptrip.com", "hotel-cyclades.com",
    "hotelmix.", "hotelsclick.com", "hrs.com", "lastminute.com",
    "ostrovok.", "reservations.com", "roomguru.", "stayforlong.com",
    "hotwire.com", "priceline.com", "orbitz.com", "ebookers.",
    "myhotelshop.com", "destinia.com", "travelmyth.com",
    # Greek / local OTAs
    "discovergreece.com", "greeka.com", "trekksoft.com",
    # Social / link-in-bio
    "facebook.com", "instagram.com", "linktr.ee", "lnk.bio",
    "wa.me", "whatsapp.com", "t.me", "tiktok.com",
    # Generic page builders / placeholders
    "sites.google.com", "google.com", "wixsite.com",
    "weebly.com", "blogspot.com",
]

QUERIES_PER_REGION = [
    "hotels in {region}",
    "rooms {region}",
    "apartments {region}",
    "studios {region}",
    "ξενοδοχεία {region}",
    "δωμάτια {region}",
]


def _is_real_website(url: str) -> bool:
    if not url:
        return False
    u = url.lower()
    return not any(d in u for d in OTA_DOMAINS)


def _normalize_phone(phone: str) -> str:
    if not phone:
        return ""
    return re.sub(r"[^\d+]", "", phone)


async def _accept_consent(page):
    for label in ["Accept all", "I agree", "Αποδοχή όλων", "Συμφωνώ"]:
        try:
            await page.click(f'button:has-text("{label}")', timeout=2000)
            return
        except PWTimeout:
            pass


CARD_SEL = 'div.Nv2PK'


async def _scroll_results(page, max_scrolls: int = 60):
    """Scroll the left results panel until exhausted."""
    panel_sel = 'div[role="feed"]'
    try:
        await page.wait_for_selector(panel_sel, timeout=12000)
    except PWTimeout:
        return

    last_count = 0
    stable = 0
    for i in range(max_scrolls):
        await page.evaluate(
            f"document.querySelector('{panel_sel}').scrollBy(0, 3000)"
        )
        await asyncio.sleep(0.8)

        end_marker = await page.query_selector(
            'div[role="feed"] span.HlvSq, '
            'div[role="feed"] >> text=/You.?ve reached the end|Φτάσατε στο τέλος/i'
        )
        if end_marker:
            break

        cards = await page.query_selector_all(CARD_SEL)
        count = len(cards)
        if count == last_count:
            stable += 1
            if stable >= 3:
                break
        else:
            stable = 0
        last_count = count


async def _get_card_name(card) -> str:
    """Extract the place name from a card without clicking it."""
    link = await card.query_selector('a.hfpxzc')
    if link:
        aria = await link.get_attribute("aria-label") or ""
        if aria:
            return aria.strip()
    name_el = await card.query_selector('div.qBF1Pd')
    if name_el:
        return (await name_el.inner_text()).strip()
    return ""


async def _get_card_gmaps_url(card) -> str:
    """Extract the Google Maps place URL from a card."""
    link = await card.query_selector('a.hfpxzc')
    if link:
        href = await link.get_attribute("href") or ""
        return href
    return ""


def _classify_online_presence(website: str) -> str:
    """Categorize the website link to indicate where the lead is online."""
    if not website:
        return "none"
    w = website.lower()
    if "facebook.com" in w:
        return "facebook"
    if "instagram.com" in w:
        return "instagram"
    if "booking.com" in w:
        return "booking"
    if "airbnb." in w:
        return "airbnb"
    if "tripadvisor." in w:
        return "tripadvisor"
    if "linktr.ee" in w or "lnk.bio" in w:
        return "link-in-bio"
    if "wa.me" in w or "whatsapp" in w:
        return "whatsapp"
    if any(d in w for d in OTA_DOMAINS):
        return "ota-aggregator"
    return "other"


async def _extract_card_data(page, card):
    """Click a card and extract data from the side panel."""
    try:
        link = await card.query_selector('a.hfpxzc')
        if link:
            await link.click()
        else:
            await card.click()
    except Exception:
        return None

    try:
        await page.wait_for_selector('h1.DUwDvf', timeout=4000)
    except PWTimeout:
        return None
    await asyncio.sleep(0.15)

    name = ""
    phone = ""
    website = ""
    address = ""
    category = ""

    name_el = await page.query_selector('h1.DUwDvf')
    if name_el:
        name = (await name_el.inner_text()).strip()

    # Try several selectors — Google Maps uses different DOM in different modes:
    # 1. Standard place page: button.DkEaL
    # 2. Hotel listing mode: tab "Hotels" / "Vacation rentals" is active
    # 3. Some places show category as <span> next to rating
    for sel in ['button.DkEaL', 'span.DkEaL', 'button[jsaction*="category"]',
                'button.GA4HJ.wjqEKe']:
        cat_el = await page.query_selector(sel)
        if cat_el:
            category = (await cat_el.inner_text()).strip()
            if category:
                break

    # Fallback: when in hotel-listing mode, infer from active tab
    if not category:
        for label in ["Hotels", "Vacation rentals", "Resorts"]:
            try:
                tab = await page.query_selector(
                    f'button.GA4HJ.wjqEKe:has-text("{label}")')
                if tab:
                    category = label.rstrip("s")
                    break
            except Exception:
                pass

    phone_btn = await page.query_selector('button[data-item-id^="phone:"]')
    if phone_btn:
        aria = await phone_btn.get_attribute("aria-label") or ""
        m = re.search(r"[\+\d][\d\s\-\(\)]{6,}", aria)
        if m:
            phone = _normalize_phone(m.group(0))

    site_btn = await page.query_selector('a[data-item-id="authority"]')
    if site_btn:
        href = await site_btn.get_attribute("href") or ""
        website = href.strip()

    addr_btn = await page.query_selector('button[data-item-id="address"]')
    if addr_btn:
        aria = await addr_btn.get_attribute("aria-label") or ""
        address = aria.replace("Address: ", "").strip()

    return {
        "name": name,
        "phone": phone,
        "website": website,
        "address": address,
        "category": category,
        "online_presence": _classify_online_presence(website),
    }


async def scrape_region(region: str, queries: list[str] = None,
                         headless: bool = True,
                         existing_names: set[str] = None,
                         rejected_names: set[str] = None,
                         on_progress=None,
                         on_query_done=None) -> list[dict]:
    """Scrape Google Maps for a region. Returns deduplicated leads.

    If the region has villages defined in villages.py, the search expands
    to cover each village separately. Otherwise searches the region name.

    Args:
        existing_names: names already accepted as leads (skip before click)
        rejected_names: names previously rejected (had website etc) — skip too
        on_progress: optional async callback(new_leads_list) called after
                     each query finishes; lets the caller persist incrementally
    """
    if queries is None:
        try:
            from villages import expand_region
            search_targets = expand_region(region)
        except ImportError:
            search_targets = [region]
        queries = []
        for target in search_targets:
            for q_template in QUERIES_PER_REGION:
                queries.append(q_template.format(region=target))
        if len(search_targets) > 1:
            print(f"  [region] {region}: expanding to "
                  f"{len(search_targets)} villages "
                  f"({len(queries)} total queries)", flush=True)

    # Pre-populate seen with existing names so we skip them before click
    seen = {}
    pre_skip_set = set()
    if existing_names:
        pre_skip_set |= {n.lower().strip() for n in existing_names if n}
    rejected_skip = set()
    if rejected_names:
        rejected_skip = {n.lower().strip() for n in rejected_names if n}
    if pre_skip_set or rejected_skip:
        print(f"  [region] {region}: pre-loaded "
              f"{len(pre_skip_set)} accepted + {len(rejected_skip)} rejected "
              f"names — they will be skipped before click", flush=True)

    pw = await async_playwright().start()
    browser = await pw.chromium.launch(headless=headless, channel="chromium")
    context = await browser.new_context(
        user_agent=USER_AGENT,
        locale="en-US",
        viewport={"width": 1366, "height": 900},
    )
    page = await context.new_page()

    try:
        for q_idx, q in enumerate(queries):
            safe_q = q.encode("ascii", errors="replace").decode("ascii")
            print(f"  [gmaps] query: {safe_q!r}", flush=True)
            url = ("https://www.google.com/maps/search/"
                   + urllib.parse.quote(q) + "/?hl=en")
            try:
                await page.goto(url, wait_until="domcontentloaded",
                                  timeout=30000)
                await _accept_consent(page)
                await _scroll_results(page)

                cards = await page.query_selector_all(CARD_SEL)
                print(f"    found {len(cards)} cards in panel", flush=True)

                # Pre-dedup: skip cards we've already processed by name,
                # OR that already exist in master CSV (accepted previously),
                # OR that we rejected before (had website / not accommodation)
                cards_to_click = []
                skipped_dups = 0
                skipped_accepted = 0
                skipped_rejected = 0
                for card in cards:
                    name = await _get_card_name(card)
                    key = name.lower().strip()
                    if not key:
                        cards_to_click.append((card, ""))
                        continue
                    if key in seen:
                        skipped_dups += 1
                        continue
                    if key in pre_skip_set:
                        skipped_accepted += 1
                        continue
                    if key in rejected_skip:
                        skipped_rejected += 1
                        continue
                    cards_to_click.append((card, key))
                if skipped_dups or skipped_accepted or skipped_rejected:
                    print(f"    skipped before click: {skipped_dups} dups, "
                          f"{skipped_accepted} accepted, "
                          f"{skipped_rejected} rejected", flush=True)

                new_count = 0
                new_in_query = []
                for i, (card, pre_key) in enumerate(cards_to_click):
                    # Capture gmaps URL from the card BEFORE click (DOM may
                    # change once the panel opens)
                    gmaps_url = await _get_card_gmaps_url(card)
                    try:
                        data = await _extract_card_data(page, card)
                    except Exception:
                        continue
                    if not data or not data["name"]:
                        continue
                    data["gmaps_url"] = gmaps_url
                    key = data["name"].lower().strip()
                    if key in seen:
                        if not seen[key]["phone"] and data["phone"]:
                            seen[key]["phone"] = data["phone"]
                        if not seen[key].get("gmaps_url") and gmaps_url:
                            seen[key]["gmaps_url"] = gmaps_url
                        continue
                    data["region"] = region
                    seen[key] = data
                    new_in_query.append(data)
                    new_count += 1
                    if (i + 1) % 20 == 0:
                        print(f"    clicked {i+1}/{len(cards_to_click)} "
                              f"(unique: {len(seen)})", flush=True)
                print(f"    +{new_count} new from this query "
                      f"(total unique: {len(seen)})", flush=True)

                # Incremental save: let caller persist what we found in this query
                if on_progress and new_in_query:
                    try:
                        await on_progress(new_in_query)
                    except Exception as e:
                        print(f"    [warn] on_progress callback failed: {e}",
                              flush=True)

                # Progress callback: signal query done (for ETA)
                if on_query_done:
                    try:
                        await on_query_done(region, q_idx + 1, len(queries))
                    except Exception:
                        pass
            except Exception as e:
                safe_err = str(e).encode("ascii", errors="replace").decode("ascii")
                print(f"    [warn] query failed: {safe_err}", flush=True)
    finally:
        try:
            await browser.close()
        except Exception:
            pass
        try:
            await pw.stop()
        except Exception:
            pass

    return list(seen.values())


def is_accommodation_category(category: str) -> bool:
    """True if category matches an accommodation type."""
    if not category:
        return False
    c = category.lower()
    return any(allowed in c for allowed in ACCOMMODATION_CATEGORIES)


def is_blocked_category(category: str) -> bool:
    """True if category is clearly a non-accommodation business."""
    if not category:
        return False
    c = category.lower()
    return any(blocked in c for blocked in BLOCKED_CATEGORY_HINTS)


def looks_like_accommodation_name(name: str) -> bool:
    """Heuristic: name contains words suggesting it's a place to stay."""
    if not name:
        return False
    n = name.lower()
    keywords = [
        "hotel", "apartment", "studio", "studios", "rooms", "villa",
        "villas", "suite", "suites", "guesthouse", "guest house",
        "hostel", "resort", "lodge", "inn", "pension", "boutique",
        "ξενοδοχ", "δωμάτι", "διαμέρισμ", "βίλα", "πανσιόν", "κατάλυμ",
        "house", "stay", "retreat", "residence",
    ]
    return any(k in n for k in keywords)


def filter_leads(leads: list[dict]) -> list[dict]:
    """Keep accommodations with phone and no real website.

    A lead passes if:
      - has phone AND
      - has no real website AND
      - either: category clearly an accommodation, OR
                 category empty AND name looks like accommodation
      - AND: category is not blocked (tattoo, recording, etc.)
    """
    out = []
    for l in leads:
        if not l.get("phone"):
            continue
        if _is_real_website(l.get("website", "")):
            continue
        cat = l.get("category", "")
        if is_blocked_category(cat):
            continue
        if is_accommodation_category(cat):
            out.append(l)
            continue
        if not cat and looks_like_accommodation_name(l.get("name", "")):
            out.append(l)
            continue
    return out
