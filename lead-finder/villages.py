"""
Tourist villages within each region. When a region has villages defined,
the scraper expands its searches to cover each village separately —
this finds far more accommodations than a single island-wide search.

When a region is NOT in this dict, the scraper falls back to searching
the region name directly.
"""

VILLAGES = {
    # === Tier 1: Top tourist hotspots ===

    "Mykonos": [
        "Mykonos Town", "Ornos", "Platis Gialos", "Psarou",
        "Elia Beach", "Paradise Beach", "Super Paradise",
        "Kalafati", "Ano Mera", "Agios Stefanos",
        "Tourlos", "Agios Ioannis Mykonos", "Kalo Livadi",
        "Agios Sostis Mykonos", "Houlakia", "Megali Ammos",
    ],

    "Santorini": [
        "Fira", "Oia", "Imerovigli", "Firostefani",
        "Pyrgos Santorini", "Kamari", "Perissa", "Akrotiri",
        "Megalochori", "Emporio Santorini", "Vothonas",
        "Karterados", "Messaria Santorini", "Vlychada",
        "Perivolos", "Monolithos Santorini", "Finikia",
    ],

    "Paros": [
        "Parikia", "Naoussa Paros", "Drios", "Aliki Paros",
        "Lefkes Paros", "Pisso Livadi", "Logaras",
        "Marpissa", "Prodromos Paros", "Marmara Paros",
        "Kostos", "Krotiri", "Ampelas", "Santa Maria Paros",
        "Golden Beach Paros", "Punda Beach",
    ],

    "Ios": [
        "Chora Ios", "Ios Town", "Mylopotas", "Mylopotas Ios",
        "Yialos Ios", "Ormos Ios", "Manganari", "Manganari Beach Ios",
        "Koumbara", "Koumbara Beach Ios", "Plakotos Ios", "Klima Ios",
        "Theodoti", "Agia Theodoti Ios", "Kalamos Ios",
    ],

    "Rhodes": [
        "Rhodes Town", "Lindos", "Faliraki", "Pefkos",
        "Afandou", "Ialysos", "Kremasti", "Kolymbia",
        "Tsambika", "Archangelos", "Stegna", "Kiotari",
        "Lardos", "Gennadi", "Prasonisi", "Kalathos",
        "Pastida", "Theologos Rhodes", "Haraki",
    ],

    "Corfu": [
        "Corfu Town", "Kerkyra", "Paleokastritsa",
        "Kassiopi", "Sidari", "Roda", "Acharavi",
        "Agios Gordios", "Glyfada Corfu", "Pelekas",
        "Benitses", "Moraitika", "Messonghi", "Kavos",
        "Dassia", "Ipsos", "Barbati", "Nissaki",
        "Agios Stefanos Corfu", "Arillas", "Agios Georgios Corfu",
    ],

    "Naxos": [
        "Naxos Town", "Chora Naxos", "Agios Prokopios",
        "Agia Anna Naxos", "Plaka Naxos", "Mikri Vigla",
        "Kastraki Naxos", "Apollonas", "Apiranthos",
        "Halki Naxos", "Filoti", "Sangri", "Glinado",
        "Galini", "Engares",
    ],

    "Zakynthos": [
        "Zakynthos Town", "Laganas", "Kalamaki Zakynthos",
        "Tsilivi", "Argassi", "Vasilikos", "Alykes",
        "Alikanas", "Planos", "Keri", "Limni Keriou",
        "Agios Sostis Zakynthos", "Porto Zoro",
        "Banana Beach Zakynthos", "Volimes", "Anafonitria",
    ],

    "Kefalonia": [
        "Argostoli", "Lassi", "Lixouri", "Skala Kefalonia",
        "Poros Kefalonia", "Sami", "Fiskardo", "Assos",
        "Agia Efimia", "Lourdas", "Trapezaki",
        "Spartia", "Karavomylos", "Katelios", "Svoronata",
    ],

    "Crete-Heraklion": [
        "Heraklion", "Hersonissos", "Malia", "Stalida",
        "Stalis", "Analipsi", "Gouves", "Kokkini Hani",
        "Amoudara", "Agia Pelagia", "Lygaria",
        "Bali Crete", "Matala", "Agia Galini",
    ],

    "Crete-Lasithi": [
        "Agios Nikolaos Crete", "Elounda", "Plaka Lasithi",
        "Sissi", "Sitia", "Ierapetra", "Makrigialos",
        "Mochlos", "Tourloti", "Kalo Chorio Lasithi",
        "Lasithi Plateau", "Tzermiado",
    ],

    "Crete-Chania": [
        "Chania", "Platanias", "Stalos", "Agia Marina Chania",
        "Kalathas", "Tersanas", "Kolymbari", "Kissamos",
        "Falassarna", "Elafonisi", "Paleochora", "Sougia",
        "Loutro", "Sfakia", "Georgioupoli", "Almyrida",
        "Plaka Chania", "Vamos",
    ],

    "Crete-Rethymno": [
        "Rethymno", "Adelianos Kampos", "Panormo Crete",
        "Bali Rethymno", "Plakias", "Triopetra",
        "Agia Galini Rethymno", "Anogia", "Spili",
        "Episkopi Rethymno", "Geropotamos",
    ],

    # === Tier 2: Popular but smaller ===

    "Milos": [
        "Adamantas", "Plaka Milos", "Pollonia", "Triovasalos",
        "Trypiti", "Klima Milos", "Sarakiniko", "Provatas",
        "Paleochori Milos", "Firopotamos",
    ],

    "Sifnos": [
        "Apollonia Sifnos", "Kamares Sifnos", "Platis Gialos Sifnos",
        "Faros Sifnos", "Vathi Sifnos", "Artemonas",
        "Kastro Sifnos", "Cherronisos",
    ],

    "Tinos": [
        "Tinos Town", "Chora Tinos", "Agios Sostis Tinos",
        "Pyrgos Tinos", "Panormos Tinos", "Kionia",
        "Ysternia", "Kardiani", "Volax",
    ],

    "Skiathos": [
        "Skiathos Town", "Koukounaries", "Megali Ammos Skiathos",
        "Vromolimnos", "Achladies", "Kanapitsa", "Troulos",
        "Agia Paraskevi Skiathos", "Lalaria", "Kastro Skiathos",
    ],

    "Skopelos": [
        "Skopelos Town", "Glossa", "Loutraki Skopelos",
        "Stafylos", "Panormos Skopelos", "Milia Skopelos",
        "Elios", "Neo Klima",
    ],

    "Kos": [
        "Kos Town", "Lambi", "Tigaki", "Marmari Kos",
        "Mastichari", "Kefalos", "Kardamena", "Psalidi",
        "Agios Fokas", "Lagada Kos", "Pyli Kos",
    ],

    "Lefkada": [
        "Lefkada Town", "Nidri", "Vasiliki Lefkada",
        "Agios Nikitas", "Kathisma", "Egremni",
        "Porto Katsiki", "Mikros Gialos", "Sivota Lefkada",
        "Kalamitsi Lefkada", "Vlycho", "Lygia Lefkada",
    ],

    "Halkidiki": [
        "Kassandra", "Sithonia", "Athos",
        "Kallithea Halkidiki", "Hanioti", "Pefkochori",
        "Polychrono", "Paliouri", "Afytos", "Sani",
        "Nikiti", "Neos Marmaras", "Vourvourou",
        "Sarti", "Toroni", "Ouranoupoli",
        "Kriopigi", "Fourka", "Posidi",
    ],

    "Thassos": [
        "Limenas Thassos", "Skala Potamia", "Golden Beach Thassos",
        "Limenaria", "Pefkari", "Potos", "Astris",
        "Skala Prinos", "Skala Rachoni", "Aliki Thassos",
        "Theologos Thassos",
    ],

    "Lesbos": [
        "Mytilene", "Mithymna", "Molyvos", "Petra Lesbos",
        "Skala Eressou", "Eressos", "Plomari",
        "Sigri Lesbos", "Vatera", "Skala Kalloni",
        "Anaxos", "Skala Sykamnia", "Agiasos",
        "Gera Lesbos", "Polichnitos",
    ],

    "Chios": [
        "Chios Town", "Karfas", "Vrontados",
        "Mesta Chios", "Pyrgi Chios", "Olympi", "Volissos",
        "Lagada Chios", "Emporios Chios", "Komi Chios",
        "Nagos", "Kardamyla", "Limnia Chios", "Avgonyma",
    ],

    "Samos": [
        "Samos Town", "Vathy", "Kokkari",
        "Pythagorio", "Karlovasi", "Marathokampos",
        "Votsalakia", "Ireon", "Kampos Marathokampou",
        "Limnionas Samos", "Avlakia", "Agios Konstantinos Samos",
        "Mytilinii",
    ],

    "Karpathos": [
        "Pigadia", "Karpathos Town", "Olympos Karpathos",
        "Diafani", "Lefkos", "Arkasa", "Finiki",
        "Amopi", "Kyra Panagia", "Aperi", "Menetes",
    ],

    "Patmos": [
        "Skala Patmos", "Chora Patmos", "Grikos",
        "Kampos Patmos", "Lambi Patmos",
    ],

    "Kalymnos": [
        "Pothia", "Kalymnos Town", "Massouri",
        "Myrties", "Telendos", "Vathys Kalymnos",
        "Emporios Kalymnos", "Panormos Kalymnos", "Kantouni",
    ],

    "Symi": [
        "Symi Town", "Gialos Symi", "Pedi", "Nimborio",
    ],

    "Astypalaia": [
        "Chora Astypalaia", "Pera Gialos", "Livadia Astypalaia",
        "Maltezana", "Vathy Astypalaia",
    ],

    "Andros": [
        "Chora Andros", "Batsi", "Gavrio", "Korthi",
        "Apoikia", "Stenies", "Achla",
    ],

    "Syros": [
        "Ermoupoli", "Ano Syros", "Galissas", "Kini Syros",
        "Vari Syros", "Posidonia", "Megas Gialos",
        "Azolimnos", "Foinikas",
    ],

    "Kythnos": [
        "Chora Kythnos", "Loutra Kythnos", "Merichas",
        "Driopida", "Kanala Kythnos",
    ],

    "Serifos": [
        "Chora Serifos", "Livadi Serifos", "Megalo Livadi",
        "Sykamia", "Ganema",
    ],

    "Folegandros": [
        "Chora Folegandros", "Karavostasi", "Ano Meria",
        "Agali Folegandros",
    ],

    "Amorgos": [
        "Chora Amorgos", "Katapola", "Aegiali",
        "Tholaria", "Langada Amorgos",
    ],

    "Ikaria": [
        "Agios Kirykos", "Evdilos", "Armenistis",
        "Nas", "Therma Ikaria", "Karavostamo", "Christos Raches",
    ],

    "Hydra": [
        "Hydra Town", "Kamini", "Mandraki Hydra",
        "Vlychos",
    ],

    "Spetses": [
        "Spetses Town", "Ligoneri", "Agia Marina Spetses",
        "Ksilokeriza",
    ],

    "Aegina": [
        "Aegina Town", "Agia Marina Aegina", "Perdika",
        "Marathonas", "Souvala", "Vagia Aegina",
    ],

    "Poros": [
        "Poros Town", "Askeli", "Neorio",
    ],

    "Ithaca": [
        "Vathy Ithaca", "Kioni", "Frikes", "Stavros Ithaca",
        "Anogi", "Perachori",
    ],

    "Paxi": [
        "Gaios", "Lakka Paxi", "Loggos Paxi", "Mongonisi",
    ],

    # === Athens Riviera coastal villages — already in regions.py individually ===
    # These don't need village expansion as they're already specific.
}


def expand_region(region: str) -> list[str]:
    """
    Returns the list of search targets for a region.
    If villages are defined, returns the villages prefixed with the region name
    for context (helps Google Maps disambiguate).
    Otherwise returns just the region name.
    """
    villages = VILLAGES.get(region)
    if not villages:
        return [region]
    return villages
