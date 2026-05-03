"""
Tourist regions per country. Used as Google Maps search queries.

Structure:
    COUNTRIES = {
        "Country Name": {
            "code": "GR",
            "groups": {
                "Group Name (e.g. Cyclades)": [region1, region2, ...],
                ...
            },
        },
        ...
    }

To add a new country, append a new entry to COUNTRIES — every other layer of
the system (dashboard, scraper, villages.py expansion, CSV writer) reads from
this dict and updates automatically.

The bbox tuple in REGIONS is kept for legacy OSM use; the Google Maps scraper
only needs the region NAME (which can include city/area context, e.g.
"Amsterdam, Netherlands").
"""

# ---------------------------------------------------------------------------
# Multi-country region catalogue
# ---------------------------------------------------------------------------

COUNTRIES = {
    "Greece": {
        "code": "GR",
        "groups": {
            "Αττική": [
                "Athens", "Piraeus", "Glyfada", "Voula", "Vouliagmeni",
                "Varkiza", "Lagonisi", "Anavyssos", "Saronida",
                "Palaia Fokaia", "Sounio", "Marathon", "Schinias",
                "Nea Makri", "Rafina", "Porto Rafti", "Lavrio",
                "Aegina", "Spetses", "Hydra", "Poros",
            ],
            "Κυκλάδες": [
                "Paros", "Antiparos", "Naxos", "Mykonos", "Santorini",
                "Ios", "Milos", "Kimolos", "Sifnos", "Serifos", "Kythnos",
                "Kea", "Tinos", "Andros", "Syros", "Folegandros", "Sikinos",
                "Amorgos", "Anafi", "Koufonisia", "Donousa",
            ],
            "Β. Αιγαίο": [
                "Lesbos", "Chios", "Samos", "Ikaria", "Fourni", "Lemnos",
                "Agios Efstratios", "Thassos", "Samothrace", "Psara",
                "Oinousses",
            ],
            "Δωδεκάνησα": [
                "Rhodes", "Kos", "Karpathos", "Patmos", "Leros", "Kalymnos",
                "Symi", "Tilos", "Astypalaia", "Nisyros", "Halki", "Kasos",
                "Lipsi",
            ],
            "Σποράδες": [
                "Skiathos", "Skopelos", "Alonissos", "Skyros",
            ],
            "Επτάνησα": [
                "Corfu", "Lefkada", "Zakynthos", "Kefalonia", "Ithaca",
                "Paxi",
            ],
        },
    },

    "Netherlands": {
        "code": "NL",
        "groups": {
            # === Noord-Holland (Amsterdam + coast) ===
            "Noord-Holland": [
                "Amsterdam", "Haarlem", "Zandvoort", "Bloemendaal aan Zee",
                "IJmuiden", "Egmond aan Zee", "Bergen aan Zee",
                "Schoorl", "Castricum aan Zee", "Wijk aan Zee",
                "Alkmaar", "Hoorn", "Enkhuizen", "Volendam", "Edam",
                "Marken", "Monnickendam", "Den Helder", "Texel",
            ],
            # === Zuid-Holland (Rotterdam, The Hague, Delft) ===
            "Zuid-Holland": [
                "Rotterdam", "The Hague", "Den Haag", "Scheveningen",
                "Kijkduin", "Delft", "Leiden", "Katwijk aan Zee",
                "Noordwijk aan Zee", "Wassenaar", "Gouda", "Dordrecht",
                "Hoek van Holland",
            ],
            # === Utrecht province ===
            "Utrecht": [
                "Utrecht", "Amersfoort", "Soest", "Zeist", "Houten",
                "Doorn", "Wijk bij Duurstede",
            ],
            # === Noord-Brabant ===
            "Noord-Brabant": [
                "Eindhoven", "Den Bosch", "'s-Hertogenbosch", "Breda",
                "Tilburg", "Helmond", "Bergen op Zoom",
            ],
            # === Gelderland (Arnhem, Veluwe) ===
            "Gelderland": [
                "Arnhem", "Nijmegen", "Apeldoorn", "Ede", "Wageningen",
                "Otterlo", "Hoenderloo", "Putten Veluwe", "Harderwijk",
            ],
            # === Limburg (Maastricht + south) ===
            "Limburg": [
                "Maastricht", "Valkenburg aan de Geul", "Heerlen",
                "Roermond", "Venlo", "Sittard",
            ],
            # === Zeeland (coast + Walcheren) ===
            "Zeeland": [
                "Middelburg", "Vlissingen", "Domburg", "Zoutelande",
                "Westkapelle", "Cadzand", "Renesse", "Burgh-Haamstede",
                "Veere",
            ],
            # === Friesland (Wadden islands + lakes) ===
            "Friesland": [
                "Leeuwarden", "Sneek", "Harlingen", "Stavoren",
                "Vlieland", "Terschelling", "Ameland", "Schiermonnikoog",
            ],
            # === Groningen / Drenthe / Overijssel / Flevoland ===
            "Noord-Nederland": [
                "Groningen", "Assen", "Emmen", "Giethoorn", "Zwolle",
                "Deventer", "Lemmer", "Lelystad",
            ],
        },
    },
}


# ---------------------------------------------------------------------------
# Derived structures (back-compat for callers that don't know about countries)
# ---------------------------------------------------------------------------


def _flatten_groups() -> dict:
    """Region group dict, merged across countries. Group names should be
    unique across countries (we use country-specific names like 'Αττική' /
    'Noord-Holland' so no collision in practice)."""
    out = {}
    for country in COUNTRIES.values():
        for group_name, regions in country["groups"].items():
            out[group_name] = list(regions)
    return out


def _flatten_regions() -> dict:
    """Region name -> dummy bbox (legacy). Region names should be globally
    unique across countries (we prefix Dutch ambiguous names with country
    context where needed, e.g. 'Den Haag')."""
    out = {}
    for country_name, country in COUNTRIES.items():
        for regions in country["groups"].values():
            for r in regions:
                # Bbox is only used by legacy OSM code, not by the Google Maps
                # scraper. Dummy zeros are fine.
                out.setdefault(r, (0, 0, 0, 0))
    return out


def _region_to_country() -> dict:
    """Region name -> country name. Used to tag every lead with its country."""
    out = {}
    for country_name, country in COUNTRIES.items():
        for regions in country["groups"].values():
            for r in regions:
                out.setdefault(r, country_name)
    return out


REGION_GROUPS = _flatten_groups()
REGIONS = _flatten_regions()
REGION_TO_COUNTRY = _region_to_country()


# Hand-rolled coordinates for a few Greek regions (kept for legacy callers).
# These do NOT affect Google Maps scraping — they only matter if some external
# tool reads `REGIONS[name]` expecting real bbox data.
_LEGACY_GREEK_BBOX = {
    "Athens": (37.92, 23.65, 38.05, 23.85),
    "Paros": (36.93, 25.05, 37.18, 25.30),
    "Mykonos": (37.38, 25.28, 37.50, 25.50),
    "Santorini": (36.32, 25.32, 36.50, 25.55),
    "Rhodes": (35.85, 27.70, 36.48, 28.27),
    "Corfu": (39.35, 19.55, 39.83, 20.12),
}
for _name, _bbox in _LEGACY_GREEK_BBOX.items():
    if _name in REGIONS:
        REGIONS[_name] = _bbox


def country_for_region(region: str) -> str:
    """Return the country that owns a given region name, or ''."""
    return REGION_TO_COUNTRY.get(region, "")


def regions_for_country(country: str) -> list:
    """Flat list of every region in a country."""
    c = COUNTRIES.get(country)
    if not c:
        return []
    out = []
    for regions in c["groups"].values():
        out.extend(regions)
    return out
