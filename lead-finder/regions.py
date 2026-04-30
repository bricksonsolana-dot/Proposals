"""
Greek tourist regions. Used as Google Maps search queries.
The bbox tuple (south, west, north, east) is kept for legacy OSM use
but the Google Maps scraper only needs the region NAME.
"""

REGION_GROUPS = {
    "Αττική": [
        "Athens", "Piraeus", "Glyfada", "Voula", "Vouliagmeni", "Varkiza",
        "Lagonisi", "Anavyssos", "Saronida", "Palaia Fokaia", "Sounio",
        "Marathon", "Schinias", "Nea Makri", "Rafina", "Porto Rafti",
        "Lavrio", "Aegina", "Spetses", "Hydra", "Poros",
    ],
    "Κυκλάδες": [
        "Paros", "Antiparos", "Naxos", "Mykonos", "Santorini", "Ios",
        "Milos", "Kimolos", "Sifnos", "Serifos", "Kythnos", "Kea", "Tinos",
        "Andros", "Syros", "Folegandros", "Sikinos", "Amorgos", "Anafi",
        "Koufonisia", "Donousa",
    ],
    "Β. Αιγαίο": [
        "Lesbos", "Chios", "Samos", "Ikaria", "Fourni", "Lemnos",
        "Agios Efstratios", "Thassos", "Samothrace", "Psara", "Oinousses",
    ],
    "Δωδεκάνησα": [
        "Rhodes", "Kos", "Karpathos", "Patmos", "Leros", "Kalymnos", "Symi",
        "Tilos", "Astypalaia", "Nisyros", "Halki", "Kasos", "Lipsi",
    ],
    "Σποράδες": [
        "Skiathos", "Skopelos", "Alonissos", "Skyros",
    ],
    "Επτάνησα": [
        "Corfu", "Lefkada", "Zakynthos", "Kefalonia", "Ithaca", "Paxi",
    ],
}

REGIONS = {
    # === Attica (Αττική) ===
    "Athens": (37.92, 23.65, 38.05, 23.85),
    "Piraeus": (37.92, 23.61, 37.97, 23.68),
    "Glyfada": (37.85, 23.73, 37.89, 23.78),
    "Voula": (37.83, 23.74, 37.86, 23.78),
    "Vouliagmeni": (37.80, 23.75, 37.83, 23.79),
    "Varkiza": (37.81, 23.79, 37.83, 23.83),
    "Lagonisi": (37.74, 23.85, 37.78, 23.92),
    "Anavyssos": (37.71, 23.92, 37.75, 23.98),
    "Saronida": (37.74, 23.91, 37.77, 23.95),
    "Palaia Fokaia": (37.70, 23.93, 37.73, 23.99),
    "Sounio": (37.64, 23.96, 37.69, 24.05),
    "Marathon": (38.13, 23.93, 38.18, 24.02),
    "Schinias": (38.13, 23.97, 38.18, 24.05),
    "Nea Makri": (38.05, 23.95, 38.10, 24.02),
    "Rafina": (38.00, 23.97, 38.05, 24.05),
    "Porto Rafti": (37.86, 23.98, 37.92, 24.05),
    "Lavrio": (37.69, 23.99, 37.75, 24.10),
    "Aegina": (37.70, 23.40, 37.78, 23.55),
    "Spetses": (37.23, 23.13, 37.30, 23.20),
    "Hydra": (37.32, 23.45, 37.40, 23.55),
    "Poros": (37.48, 23.43, 37.53, 23.50),

    # === Cyclades (Κυκλάδες) ===
    "Paros": (36.93, 25.05, 37.18, 25.30),
    "Antiparos": (36.95, 25.00, 37.05, 25.10),
    "Naxos": (36.95, 25.30, 37.22, 25.66),
    "Mykonos": (37.38, 25.28, 37.50, 25.50),
    "Santorini": (36.32, 25.32, 36.50, 25.55),
    "Ios": (36.66, 25.25, 36.78, 25.42),
    "Milos": (36.63, 24.32, 36.78, 24.60),
    "Kimolos": (36.78, 24.55, 36.85, 24.65),
    "Sifnos": (36.90, 24.62, 37.05, 24.80),
    "Serifos": (37.10, 24.45, 37.20, 24.60),
    "Kythnos": (37.35, 24.35, 37.48, 24.50),
    "Kea": (37.55, 24.27, 37.70, 24.42),
    "Tinos": (37.50, 25.10, 37.70, 25.30),
    "Andros": (37.75, 24.65, 37.97, 24.98),
    "Syros": (37.35, 24.85, 37.55, 25.00),
    "Folegandros": (36.58, 24.85, 36.68, 24.98),
    "Sikinos": (36.65, 25.08, 36.73, 25.18),
    "Amorgos": (36.78, 25.78, 36.92, 26.05),
    "Anafi": (36.32, 25.72, 36.40, 25.85),
    "Koufonisia": (36.92, 25.55, 36.97, 25.65),
    "Donousa": (36.99, 25.80, 37.05, 25.90),

    # === North Aegean (Β. Αιγαίο) ===
    "Lesbos": (38.95, 25.85, 39.45, 26.65),
    "Chios": (38.10, 25.85, 38.62, 26.20),
    "Samos": (37.65, 26.55, 37.85, 27.00),
    "Ikaria": (37.55, 26.05, 37.70, 26.40),
    "Fourni": (37.55, 26.42, 37.65, 26.55),
    "Lemnos": (39.85, 25.00, 40.05, 25.40),
    "Agios Efstratios": (39.45, 24.95, 39.55, 25.05),
    "Thassos": (40.55, 24.55, 40.80, 24.85),
    "Samothrace": (40.40, 25.45, 40.55, 25.70),
    "Psara": (38.50, 25.50, 38.60, 25.65),
    "Oinousses": (38.48, 26.20, 38.55, 26.30),

    # === South Aegean / Dodecanese (Δωδεκάνησα) ===
    "Rhodes": (35.85, 27.70, 36.48, 28.27),
    "Kos": (36.65, 26.90, 36.93, 27.42),
    "Karpathos": (35.32, 27.05, 35.78, 27.30),
    "Patmos": (37.27, 26.50, 37.42, 26.65),
    "Leros": (37.10, 26.78, 37.22, 26.92),
    "Kalymnos": (36.92, 26.92, 37.05, 27.10),
    "Symi": (36.55, 27.78, 36.68, 27.92),
    "Tilos": (36.40, 27.30, 36.50, 27.45),
    "Astypalaia": (36.50, 26.30, 36.65, 26.50),
    "Nisyros": (36.55, 27.10, 36.65, 27.22),
    "Halki": (36.18, 27.55, 36.28, 27.68),
    "Kasos": (35.35, 26.85, 35.45, 26.98),
    "Lipsi": (37.28, 26.72, 37.35, 26.82),

    # === Sporades (Σποράδες) ===
    "Skiathos": (39.10, 23.40, 39.22, 23.60),
    "Skopelos": (39.05, 23.55, 39.22, 23.85),
    "Alonissos": (39.05, 23.80, 39.20, 24.00),
    "Skyros": (38.78, 24.45, 38.95, 24.70),

    # === Ionian (Επτάνησα) ===
    "Lefkada": (38.55, 20.50, 38.93, 20.80),
    "Zakynthos": (37.66, 20.55, 37.95, 20.92),
    "Kefalonia": (38.05, 20.30, 38.50, 20.85),
    "Corfu": (39.35, 19.55, 39.83, 20.12),
    "Ithaca": (38.32, 20.62, 38.50, 20.82),
    "Paxi": (39.18, 20.10, 39.25, 20.25),
}
