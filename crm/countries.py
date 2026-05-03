"""
CRM-side country catalogue. Mirrors lead-finder/regions.py so the CRM is
self-contained (doesn't import from the lead-finder package).

The lead-finder pushes a `country` field on every synced lead, so this
catalogue is mostly used for:
  - Backfilling country on legacy leads that pre-date the new column
  - Grouping the admin region-picker UI by country
  - Validating / displaying flag icons in the leads list

To support a new country in the CRM, add it here AND in
lead-finder/regions.py. The two should stay in sync but neither imports
from the other.
"""

COUNTRIES = {
    "Greece": {
        "code": "GR",
        "flag": "🇬🇷",
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
        "flag": "🇳🇱",
        "groups": {
            "Noord-Holland": [
                "Amsterdam", "Haarlem", "Zandvoort", "Bloemendaal aan Zee",
                "IJmuiden", "Egmond aan Zee", "Bergen aan Zee",
                "Schoorl", "Castricum aan Zee", "Wijk aan Zee",
                "Alkmaar", "Hoorn", "Enkhuizen", "Volendam", "Edam",
                "Marken", "Monnickendam", "Den Helder", "Texel",
            ],
            "Zuid-Holland": [
                "Rotterdam", "The Hague", "Den Haag", "Scheveningen",
                "Kijkduin", "Delft", "Leiden", "Katwijk aan Zee",
                "Noordwijk aan Zee", "Wassenaar", "Gouda", "Dordrecht",
                "Hoek van Holland",
            ],
            "Utrecht": [
                "Utrecht", "Amersfoort", "Soest", "Zeist", "Houten",
                "Doorn", "Wijk bij Duurstede",
            ],
            "Noord-Brabant": [
                "Eindhoven", "Den Bosch", "'s-Hertogenbosch", "Breda",
                "Tilburg", "Helmond", "Bergen op Zoom",
            ],
            "Gelderland": [
                "Arnhem", "Nijmegen", "Apeldoorn", "Ede", "Wageningen",
                "Otterlo", "Hoenderloo", "Putten Veluwe", "Harderwijk",
            ],
            "Limburg": [
                "Maastricht", "Valkenburg aan de Geul", "Heerlen",
                "Roermond", "Venlo", "Sittard",
            ],
            "Zeeland": [
                "Middelburg", "Vlissingen", "Domburg", "Zoutelande",
                "Westkapelle", "Cadzand", "Renesse", "Burgh-Haamstede",
                "Veere",
            ],
            "Friesland": [
                "Leeuwarden", "Sneek", "Harlingen", "Stavoren",
                "Vlieland", "Terschelling", "Ameland", "Schiermonnikoog",
            ],
            "Noord-Nederland": [
                "Groningen", "Assen", "Emmen", "Giethoorn", "Zwolle",
                "Deventer", "Lemmer", "Lelystad",
            ],
        },
    },
}


def _build_region_to_country() -> dict:
    out = {}
    for country_name, country in COUNTRIES.items():
        for regions in country["groups"].values():
            for r in regions:
                out.setdefault(r, country_name)
    return out


REGION_TO_COUNTRY = _build_region_to_country()


def country_for_region(region: str) -> str:
    """Return the country a region belongs to, or '' if unknown.
    Used to backfill the country column on legacy leads.
    """
    if not region:
        return ""
    return REGION_TO_COUNTRY.get(region.strip(), "")


def flag_for_country(country: str) -> str:
    """Return the emoji flag for a known country, or globe for unknown."""
    if not country:
        return "🌍"
    c = COUNTRIES.get(country)
    return c["flag"] if c else "🌍"


def all_countries() -> list[str]:
    return list(COUNTRIES.keys())
