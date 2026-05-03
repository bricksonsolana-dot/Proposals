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
    "bed & breakfast", "bed and breakfast", "b&b",
    "vacation", "holiday", "villa",
    "rooms", "rented room", "self-catering",
    "pension", "boutique",
    # Greek
    "ξενοδοχ", "ξενώνας", "ξενώνες", "δωμάτι", "διαμέρισμα",
    "διαμερίσματα", "πανσιόν", "πανδοχ", "βίλα", "βίλες",
    "κατάλυμα", "καταλύματα", "ενοικιαζ",
    # Dutch
    "appartement", "appartementen", "vakantie", "vakantiehuis",
    "vakantiewoning", "vakantiepark", "logies", "gastenverblijf",
    "bungalowpark", "campinghuisje",
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

# Tier-2 validation: country-aware sanity checks on extracted leads.
# A lead's phone must start with the country dial prefix, and its address
# must contain the country name OR a postal-code pattern from that country.
# Cross-country leakage (e.g. a Greek phone on a Netherlands lead) is the
# clearest signature of stale-DOM data leaking between cards.
COUNTRY_PHONE_PREFIX = {
    "Greece": "+30",
    "Netherlands": "+31",
}

COUNTRY_ADDRESS_KEYWORDS = {
    "Greece": ["greece", "ελλάδα", "ελλάς"],
    "Netherlands": ["netherlands", "nederland"],
}

# Postal-code patterns per country (used as fallback when the address string
# omits the country name — common in localised Google Maps responses).
COUNTRY_POSTAL_PATTERNS = {
    "Netherlands": re.compile(r"\b\d{4}\s?[A-Z]{2}\b"),
    "Greece": re.compile(r"\b\d{3}\s?\d{2}\b"),
}

# Hotel brand fragments to reject by name. These are large international or
# regional chains whose properties always have real websites — Google Maps
# attaches an auto-generated "Official site" link for them in hotel-listing
# mode, so they slip past the website filter. Substring match, lowercase.
# Conservative list: only highly distinctive brand phrases to avoid false
# positives on independent properties that happen to share a generic word.
HOTEL_CHAIN_BRANDS = [
    # International majors
    "nh hotel", "nh collection", "nh city",
    "hilton", "doubletree by hilton", "hampton by hilton",
    "conrad ", "waldorf astoria",
    "marriott", "sheraton", "westin", "courtyard by marriott",
    "renaissance hotel", "residence inn", "fairfield inn",
    "moxy hotel", "aloft hotel", "four points",
    "mercure hotel", "mercure amsterdam", "mercure rotterdam",
    "novotel", "sofitel", "pullman ", "ibis hotel", "ibis amsterdam",
    "ibis budget", "ibis styles", "swissôtel", "swissotel",
    "mövenpick", "movenpick",
    "holiday inn", "crowne plaza", "intercontinental",
    "indigo hotel", "staybridge suites", "candlewood suites",
    "best western", "premier inn", "travelodge",
    "radisson", "park inn by radisson",
    "hyatt regency", "hyatt place", "hyatt house", "andaz amsterdam",
    "motel one", "citizenm", "kimpton",
    "park plaza", "art'otel",
    "steigenberger",
    "leonardo hotel", "leonardo royal",
    "scandic hotel",
    "hapimag",
    "accor",
    # Dutch chains
    "van der valk",
    "fletcher hotel",
    "bilderberg",
    "postillion hotel",
    "westcord",
    "eden hotel",
    "amrâth", "amrath",
    "valk exclusief",
    # Aparthotel / serviced-apartment chains
    "the social hub", "student hotel",
    "yays concierged",
    "zoku amsterdam", "zoku rotterdam",
    "adagio aparthotel",
    "staycity",
    # Budget chains
    "oyo ", "a&o hotel",
]


def is_chain_hotel(name: str) -> bool:
    """True if the name matches a known hotel-chain brand fragment."""
    if not name:
        return False
    n = name.lower()
    return any(brand in n for brand in HOTEL_CHAIN_BRANDS)


def phone_matches_country(phone: str, country: str) -> bool:
    """True when the phone's country code matches the expected country.
    Returns True when we have no rule for the country (fail-open) or when
    the phone is empty (other filters handle that case)."""
    if not phone or not country:
        return True
    expected = COUNTRY_PHONE_PREFIX.get(country)
    if not expected:
        return True
    digits = re.sub(r"[^\d+]", "", phone)
    if not digits.startswith("+"):
        # Local number — accept (we can't tell, and empty-prefix is common
        # when Google formats e.g. "020 555 1234" without country code)
        return True
    return digits.startswith(expected)


def address_matches_country(address: str, country: str) -> bool:
    """True when the address contains the country name or a postal-code
    pattern matching the country. Fail-open if we have no rule."""
    if not address or not country:
        return True
    a = address.lower()
    keywords = COUNTRY_ADDRESS_KEYWORDS.get(country, [])
    if any(k in a for k in keywords):
        return True
    pat = COUNTRY_POSTAL_PATTERNS.get(country)
    if pat and pat.search(address):
        return True
    return False


QUERIES_PER_REGION = [
    # English (works in any country)
    "hotels in {region}",
    "rooms {region}",
    "apartments {region}",
    "studios {region}",
    "bed and breakfast {region}",
    "guest house {region}",
    # Greek
    "ξενοδοχεία {region}",
    "δωμάτια {region}",
    # Dutch
    "appartementen {region}",
    "B&B {region}",
    "vakantiehuis {region}",
    "pension {region}",
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


async def _extract_card_data(page, card, *, expected_card_name: str = "",
                              previous_panel_url: str = ""):
    """Click a card and extract data from the side panel.

    Returns:
        dict with extracted fields on success, augmented with `_status`:
            "ok"          — clean read, all consistency checks passed
            "drift"       — pre-click card name doesn't match post-click h1
                            (DOM-recycling has shifted us to a different place)
            "no_navigate" — panel URL never changed after click; we'd be
                            reading stale data from the previous lead
        None on hard failure (no h1, click error, etc.).
    """
    try:
        link = await card.query_selector('a.hfpxzc')
        if link:
            await link.click()
        else:
            await card.click()
    except Exception:
        return None

    # Tier-1 sync: wait for the panel URL to land on a NEW /maps/place/ page.
    # If the URL never changes, the previous panel is still showing — reading
    # fields now would attribute one place's data to another.
    try:
        if previous_panel_url:
            import json as _json
            await page.wait_for_function(
                "(prev) => location.href !== prev && "
                "location.pathname.includes('/maps/place/')",
                arg=previous_panel_url,
                timeout=5000,
            )
        else:
            await page.wait_for_url(re.compile(r"/maps/place/"), timeout=5000)
    except PWTimeout:
        return {"_status": "no_navigate",
                 "expected_name": expected_card_name}

    try:
        await page.wait_for_selector('h1.DUwDvf', timeout=4000)
    except PWTimeout:
        return None
    await asyncio.sleep(0.2)

    name = ""
    phone = ""
    website = ""
    address = ""
    category = ""
    panel_url = page.url or ""

    name_el = await page.query_selector('h1.DUwDvf')
    if name_el:
        name = (await name_el.inner_text()).strip()

    # Tier-1 drift check: the name shown on the card before clicking should
    # match the h1 in the panel after clicking. If not, the card handle has
    # been recycled by virtual scrolling and we'd be saving mismatched data.
    if expected_card_name and name:
        e = expected_card_name.lower().strip()
        n = name.lower().strip()
        if e != n and e not in n and n not in e:
            return {"_status": "drift",
                     "expected_name": expected_card_name,
                     "name": name,
                     "gmaps_url": panel_url}

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

    # Standard place-page website link
    site_btn = await page.query_selector('a[data-item-id="authority"]')
    if site_btn:
        href = await site_btn.get_attribute("href") or ""
        website = href.strip()

    # Hotel-listing mode: Google auto-attaches "Official site" / "Visit hotel
    # website" links sourced from third-party data even when the owner hasn't
    # claimed/added a website themselves. These don't expose the standard
    # data-item-id="authority" selector. Catch them via aria-label / text.
    if not website:
        hotel_site_selectors = [
            'a[aria-label*="website" i]',
            'a[aria-label*="Official site" i]',
            'a[aria-label*="Visit hotel" i]',
            'a[data-tooltip*="website" i]',
            'a:has-text("Official site")',
            'a:has-text("Visit hotel website")',
            'a:has-text("Visit website")',
        ]
        for sel in hotel_site_selectors:
            try:
                el = await page.query_selector(sel)
            except Exception:
                continue
            if not el:
                continue
            href = await el.get_attribute("href") or ""
            href = href.strip()
            # Skip internal Google links (directions, share, etc.)
            if href and not href.startswith("https://www.google.com/maps") \
                    and not href.startswith("/maps") \
                    and "google.com/local" not in href:
                website = href
                break

    addr_btn = await page.query_selector('button[data-item-id="address"]')
    if addr_btn:
        aria = await addr_btn.get_attribute("aria-label") or ""
        address = aria.replace("Address: ", "").strip()

    return {
        "_status": "ok",
        "name": name,
        "phone": phone,
        "website": website,
        "address": address,
        "category": category,
        "gmaps_url": panel_url,
        "online_presence": _classify_online_presence(website),
    }


async def scrape_region(region: str, queries: list[str] = None,
                         headless: bool = True,
                         existing_names: set[str] = None,
                         rejected_names: set[str] = None,
                         country: str = "",
                         on_progress=None,
                         on_query_done=None) -> list[dict]:
    """Scrape Google Maps for a region. Returns deduplicated leads.

    If the region has villages defined in villages.py, the search expands
    to cover each village separately. Otherwise searches the region name.

    Args:
        existing_names: names already accepted as leads (skip before click)
        rejected_names: names previously rejected (had website etc) — skip too
        country: country name (e.g. "Netherlands") — enables phone-prefix /
                 address-country / chain-blacklist validation. If empty, those
                 checks fail-open.
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
                drift_count = 0
                no_navigate_count = 0
                chain_count = 0
                phone_country_count = 0
                addr_country_count = 0
                previous_panel_url = page.url or ""
                for i, (card, pre_key) in enumerate(cards_to_click):
                    try:
                        data = await _extract_card_data(
                            page, card,
                            expected_card_name=pre_key,
                            previous_panel_url=previous_panel_url,
                        )
                    except Exception:
                        continue
                    if not data:
                        continue
                    status = data.get("_status", "ok")
                    if status == "drift":
                        drift_count += 1
                        # Don't update previous_panel_url — the click did
                        # navigate, but to a different place than the card
                        # advertised. The new place may still be re-clicked
                        # later from its own card.
                        previous_panel_url = data.get("gmaps_url",
                                                       previous_panel_url)
                        continue
                    if status == "no_navigate":
                        no_navigate_count += 1
                        continue
                    if not data.get("name"):
                        continue

                    # Tier-2 validation: country-aware sanity checks.
                    # Address is the strongest signal — it tells us where the
                    # place actually IS. A foreign-owner phone (+44 on a Greek
                    # listing) is common for vacation rentals and is NOT a bug,
                    # so we don't reject on phone alone. Phone is checked only
                    # when address also disagrees, as a corroborating signal.
                    name = data["name"]
                    phone = data.get("phone", "")
                    address = data.get("address", "")
                    if is_chain_hotel(name):
                        chain_count += 1
                        previous_panel_url = data.get("gmaps_url",
                                                       previous_panel_url)
                        continue
                    if country and address and not address_matches_country(
                            address, country):
                        addr_country_count += 1
                        previous_panel_url = data.get("gmaps_url",
                                                       previous_panel_url)
                        continue
                    # Address missing — fall back to phone country code as a
                    # weaker signal. (When address is present, foreign-owner
                    # phones on legit vacation rentals would false-positive.)
                    if (country and phone and not address
                            and not phone_matches_country(phone, country)):
                        phone_country_count += 1
                        previous_panel_url = data.get("gmaps_url",
                                                       previous_panel_url)
                        continue

                    previous_panel_url = data.get("gmaps_url",
                                                   previous_panel_url)
                    key = name.lower().strip()
                    if key in seen:
                        if not seen[key]["phone"] and phone:
                            seen[key]["phone"] = phone
                        if not seen[key].get("gmaps_url") and data.get("gmaps_url"):
                            seen[key]["gmaps_url"] = data["gmaps_url"]
                        continue
                    data["region"] = region
                    # Strip internal status field before saving
                    data.pop("_status", None)
                    seen[key] = data
                    new_in_query.append(data)
                    new_count += 1
                    if (i + 1) % 20 == 0:
                        print(f"    clicked {i+1}/{len(cards_to_click)} "
                              f"(unique: {len(seen)})", flush=True)
                print(f"    +{new_count} new from this query "
                      f"(total unique: {len(seen)})", flush=True)
                if (drift_count or no_navigate_count or chain_count
                        or phone_country_count or addr_country_count):
                    print(f"    rejected: drift={drift_count} "
                          f"no_nav={no_navigate_count} chain={chain_count} "
                          f"wrong_phone_cc={phone_country_count} "
                          f"wrong_addr_country={addr_country_count}",
                          flush=True)

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
        # Dutch
        "appartement", "vakantiehuis", "vakantiewoning",
        "logies", "huisje", "bungalow", "b&b",
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
