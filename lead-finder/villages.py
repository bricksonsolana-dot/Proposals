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

    # === Attica (Αττική) — neighborhoods, beaches, landmarks ===
    # Mainland Attica regions are urban/suburban — single search misses
    # most listings. Expansion to neighborhoods + beaches + landmarks
    # dramatically improves coverage.

    "Athens": [
        # Historic center
        "Plaka Athens", "Monastiraki", "Syntagma Athens", "Thissio",
        "Psirri", "Acropolis Athens", "Omonia Athens",
        "Makriyianni Athens", "Koukaki", "Mets Athens",
        # Central residential
        "Kolonaki", "Exarchia", "Pagrati", "Neapoli Athens",
        "Lycabettus", "Ambelokipoi", "Ilisia",
        # North suburbs
        "Kifisia", "Kifissia", "Marousi", "Maroussi", "Halandri",
        "Chalandri", "Nea Erythraia", "Ekali",
        "Psychiko", "Filothei", "Neo Psychiko",
        # West / South center
        "Petralona", "Kerameikos", "Gazi Athens", "Metaxourgeio",
        "Neos Kosmos Athens",
        # Coastal / South
        "Faliro", "Palaio Faliro", "Alimos", "Elliniko",
    ],

    "Piraeus": [
        "Piraeus port", "Piraeus center", "Mikrolimano",
        "Pasalimani", "Zea Marina", "Kastella",
        "Freattyda", "Piraiki", "Terpsithea Piraeus",
        "Kaminia Piraeus", "Neo Faliro",
        "Drapetsona", "Keratsini",
    ],

    "Glyfada": [
        "Glyfada", "Glyfada Athens", "Glyfada beach", "Glyfada square",
        "Glyfada center", "Glyfada marina",
        "Asteria Glyfada", "Ano Glyfada", "Kato Glyfada",
        "Astir Glyfada", "Pirnari Glyfada",
        "Glyfada golf", "Glyfada seafront",
    ],

    "Voula": [
        "Voula", "Voula Athens", "Voula beach", "Voula center",
        "Kato Voula", "Ano Voula",
        "Voula A beach", "Voula B beach", "Asteras Voula",
        "Voula marina", "Pigadakia Voula",
    ],

    "Vouliagmeni": [
        "Vouliagmeni", "Vouliagmeni Athens", "Vouliagmeni beach",
        "Vouliagmeni center", "Lake Vouliagmeni", "Limni Vouliagmeni",
        "Astir Beach Vouliagmeni", "Astir Palace Vouliagmeni",
        "Kavouri", "Kavouri beach", "Kavouri Athens",
        "Limanakia Vouliagmeni", "Mikro Kavouri",
    ],

    "Varkiza": [
        "Varkiza", "Varkiza beach", "Varkiza Resort",
        "Yabanaki Varkiza", "Varkiza center", "Varkiza marina",
        "Vari Varkiza",
    ],

    "Lagonisi": [
        "Lagonisi", "Lagonisi beach", "Mavro Lithari Lagonisi",
        "Grand Resort Lagonisi", "Lagonisi center",
        "Kitezia Lagonisi", "Kitsi Lagonisi",
    ],

    "Anavyssos": [
        "Anavyssos", "Anavissos", "Anavyssos beach", "Anavissos beach",
        "Mavro Lithari Anavyssos", "Eden beach Anavyssos",
        "Agios Nikolaos Anavyssos", "Anavyssos center",
        "Anavyssos seaside", "Paralia Anavyssou",
    ],

    "Saronida": [
        "Saronida", "Saronida beach", "Saronida Athens",
        "Saronida center", "Saronida seafront",
    ],

    "Palaia Fokaia": [
        "Palaia Fokaia", "Palea Fokea", "Palaia Fokaia beach",
        "Palea Fokea beach", "Palaia Fokaia center",
        "Palaia Fokaia seaside",
    ],

    "Sounio": [
        "Sounio", "Sounion", "Cape Sounio",
        "Temple of Poseidon Sounio", "Sounio beach",
        "Legrena", "Legrena beach", "Charakas Sounio",
        "Agios Konstantinos Sounio", "Thorikos",
    ],

    "Marathon": [
        "Marathon", "Marathonas", "Marathon beach",
        "Marathon Greece", "Nea Makri Marathon",
        "Kato Souli Marathon", "Vrana Marathon",
        "Marathon Lake", "Limni Marathona",
        "Tymvos Marathonos", "Schinias Marathon",
    ],

    "Schinias": [
        "Schinias", "Schinias beach", "Schinias National Park",
        "Schinias Marathon", "Paralia Schinia",
        "Olympic Rowing Center Schinias",
    ],

    "Nea Makri": [
        "Nea Makri", "Nea Makri beach", "Nea Makri center",
        "Zouberi Nea Makri", "Mati Nea Makri", "Mati Attica",
        "Agios Andreas Nea Makri", "Paralia Nea Makri",
        "Nea Makri seafront",
    ],

    "Rafina": [
        "Rafina", "Rafina port", "Rafina beach",
        "Rafina center", "Mati Rafina", "Pikermi",
        "Kallitechnoupoli Rafina", "Neos Voutzas",
        "Diasporiti Rafina",
    ],

    "Porto Rafti": [
        "Porto Rafti", "Porto Rafti beach", "Porto Rafti center",
        "Avlaki Porto Rafti", "Erotospilia Porto Rafti",
        "Agios Spyridon Porto Rafti", "Markopoulo Porto Rafti",
        "Vravrona", "Brauron",
    ],

    "Lavrio": [
        "Lavrio", "Lavrion", "Lavrio port", "Lavrio beach",
        "Lavrio center", "Lavrio Greece",
        "Thorikos Lavrio", "Pasa Limani Lavrio",
        "Punta Zeza Lavrio", "Agios Andreas Lavrio",
    ],

    # Saronic islands (already had some — expanded for completeness)
    "Aegina": [
        "Aegina Town", "Aegina port", "Agia Marina Aegina",
        "Perdika Aegina", "Souvala Aegina", "Vagia Aegina",
        "Marathonas Aegina", "Portes Aegina",
        "Kypseli Aegina", "Mesagros Aegina",
    ],

    "Spetses": [
        "Spetses Town", "Spetses port", "Old Harbour Spetses",
        "Agia Marina Spetses", "Agioi Anargyroi Spetses",
        "Vrellos Spetses", "Zogeria Spetses",
        "Kounoupitsa Spetses", "Ligoneri Spetses",
    ],

    "Hydra": [
        "Hydra Town", "Hydra port", "Kamini Hydra",
        "Vlychos Hydra", "Mandraki Hydra", "Palamidas Hydra",
        "Plakes Hydra", "Bisti Hydra",
    ],

    "Poros": [
        "Poros Town", "Poros port", "Askeli Poros",
        "Neorio Poros", "Monastiri Poros", "Russian Bay Poros",
        "Megalo Neorio Poros", "Mikro Neorio Poros",
        "Kanali Poros",
    ],

    # ====================================================================
    # ============== NETHERLANDS — neighborhoods & coastal areas =========
    # ====================================================================
    # Same logic as Athens / Greek hotspots: a single city-wide search misses
    # most listings on Google Maps. Each Dutch city is expanded to its
    # districts, neighborhoods, beaches, and landmarks for max coverage.

    # === Amsterdam — full district expansion ===
    "Amsterdam": [
        # Historic center
        "Amsterdam Centrum", "Amsterdam Old Town", "Dam Square Amsterdam",
        "Damrak Amsterdam", "Rokin Amsterdam", "Nieuwmarkt Amsterdam",
        "Red Light District Amsterdam", "De Wallen Amsterdam",
        "Jordaan Amsterdam", "Westerpark Amsterdam",
        # West
        "Oud-West Amsterdam", "De Baarsjes Amsterdam",
        "Bos en Lommer Amsterdam", "Westerpark district Amsterdam",
        "Kinkerstraat Amsterdam", "Helmersbuurt Amsterdam",
        # South — premium areas
        "Oud-Zuid Amsterdam", "De Pijp Amsterdam",
        "Museumkwartier Amsterdam", "Vondelpark Amsterdam",
        "Apollolaan Amsterdam", "Beethovenstraat Amsterdam",
        "Zuidas Amsterdam", "Rivierenbuurt Amsterdam",
        "Stadionbuurt Amsterdam", "Hoofddorppleinbuurt Amsterdam",
        # East
        "Oost Amsterdam", "Plantage Amsterdam",
        "Indische Buurt Amsterdam", "Oosterpark Amsterdam",
        "Watergraafsmeer Amsterdam", "IJburg Amsterdam",
        "Java-eiland Amsterdam", "KNSM-eiland Amsterdam",
        # North (across the IJ)
        "Amsterdam Noord", "NDSM Amsterdam", "Buiksloterham Amsterdam",
        "Tuindorp Oostzaan", "Nieuwendam Amsterdam",
        # Tourist / nightlife squares
        "Leidseplein Amsterdam", "Rembrandtplein Amsterdam",
        "Spui Amsterdam", "Waterlooplein Amsterdam",
        # Stations / transport hubs (lots of B&Bs nearby)
        "Amsterdam Centraal", "Amsterdam Zuid station",
        "Amsterdam Sloterdijk", "Amstel station Amsterdam",
        # Outer / Bijlmer
        "Bijlmer Amsterdam", "Amsterdam Zuidoost",
        "Slotermeer Amsterdam", "Osdorp Amsterdam",
        "Slotervaart Amsterdam", "Geuzenveld Amsterdam",
    ],

    # === Rotterdam — districts + waterfront ===
    "Rotterdam": [
        "Rotterdam Centrum", "Rotterdam city center",
        "Cool district Rotterdam", "Stadsdriehoek Rotterdam",
        "Kop van Zuid Rotterdam", "Wilhelminapier Rotterdam",
        "Katendrecht Rotterdam", "Erasmusbrug Rotterdam",
        "Delfshaven Rotterdam", "Historisch Delfshaven",
        "Witte de Withstraat Rotterdam", "Oude Haven Rotterdam",
        "Markthal Rotterdam", "Blaak Rotterdam",
        "Kralingen Rotterdam", "Kralingse Plas Rotterdam",
        "Hillegersberg Rotterdam", "Schiebroek Rotterdam",
        "Bergpolder Rotterdam", "Noord Rotterdam",
        "Oude Westen Rotterdam", "Nieuwe Westen Rotterdam",
        "Lloydkwartier Rotterdam", "Müllerpier Rotterdam",
        "Hoek van Holland", "Rozenburg Rotterdam",
        "Hoogvliet Rotterdam",
    ],

    # === The Hague / Den Haag — incl. Scheveningen beach ===
    "The Hague": [
        "Den Haag Centrum", "The Hague center",
        "Binnenhof Den Haag", "Plein Den Haag",
        "Statenkwartier Den Haag", "Archipelbuurt Den Haag",
        "Benoordenhout Den Haag", "Vogelwijk Den Haag",
        "Zeeheldenkwartier Den Haag", "Willemspark Den Haag",
        "Bezuidenhout Den Haag", "Mariahoeve Den Haag",
        "Voorhout Den Haag", "Voorburg",
        # Coastal districts
        "Scheveningen", "Scheveningen beach", "Scheveningen boulevard",
        "Scheveningen harbour", "Kurhaus Scheveningen",
        "Kijkduin", "Kijkduin beach", "Madurodam",
    ],

    # Den Haag = same place as The Hague — duplicate with Dutch name so
    # whichever the user picks works.
    "Den Haag": [
        "Den Haag Centrum", "Binnenhof Den Haag",
        "Statenkwartier Den Haag", "Archipelbuurt Den Haag",
        "Benoordenhout Den Haag", "Bezuidenhout Den Haag",
        "Scheveningen", "Scheveningen beach",
        "Kijkduin", "Voorburg",
    ],

    # === Utrecht — old town + neighborhoods ===
    "Utrecht": [
        "Utrecht Centrum", "Utrecht binnenstad",
        "Domplein Utrecht", "Oudegracht Utrecht",
        "Wittevrouwen Utrecht", "Vogelenbuurt Utrecht",
        "Lombok Utrecht", "Tuinwijk Utrecht",
        "Wilhelminapark Utrecht", "Rivierenwijk Utrecht",
        "Tuindorp Utrecht", "Voordorp Utrecht",
        "Lunetten Utrecht", "Hoograven Utrecht",
        "Oog in Al Utrecht", "Leidsche Rijn Utrecht",
        "Kanaleneiland Utrecht", "Overvecht Utrecht",
    ],

    # === Maastricht — historic center ===
    "Maastricht": [
        "Maastricht Centrum", "Binnenstad Maastricht",
        "Vrijthof Maastricht", "Markt Maastricht",
        "Wyck Maastricht", "Jekerkwartier Maastricht",
        "Sint Pieter Maastricht", "Boschstraatkwartier Maastricht",
        "Statenkwartier Maastricht", "Wittevrouwenveld Maastricht",
        "Maastricht station", "Sphinxkwartier Maastricht",
    ],

    # === Eindhoven — design district + center ===
    "Eindhoven": [
        "Eindhoven Centrum", "Eindhoven city center",
        "Stratumseind Eindhoven", "Markt Eindhoven",
        "Strijp-S Eindhoven", "Strijp Eindhoven",
        "Woensel Eindhoven", "Stratum Eindhoven",
        "Tongelre Eindhoven", "Gestel Eindhoven",
        "Eindhoven Airport", "Eindhoven station",
    ],

    # === Haarlem — historic center near Amsterdam ===
    "Haarlem": [
        "Haarlem Centrum", "Grote Markt Haarlem",
        "Spaarne Haarlem", "Vijfhoek Haarlem",
        "Burgwal Haarlem", "Haarlem station",
        "Oude Stad Haarlem", "Bloemendaal",
        "Haarlemmerhout Haarlem",
    ],

    # === Groningen — north student city ===
    "Groningen": [
        "Groningen Centrum", "Grote Markt Groningen",
        "Vismarkt Groningen", "A-kwartier Groningen",
        "Hortusbuurt Groningen", "Korreweg Groningen",
        "Schildersbuurt Groningen", "Helpman Groningen",
        "Paddepoel Groningen", "Groningen station",
    ],

    # === Nijmegen — oldest city in NL ===
    "Nijmegen": [
        "Nijmegen Centrum", "Grote Markt Nijmegen",
        "Waalkade Nijmegen", "Benedenstad Nijmegen",
        "Bottendaal Nijmegen", "Nijmegen-Oost",
        "Hunnerberg Nijmegen", "Nijmegen station",
    ],

    # === Breda ===
    "Breda": [
        "Breda Centrum", "Grote Markt Breda",
        "Ginneken Breda", "Boschstraat Breda",
        "Princenhage Breda", "Breda station",
    ],

    # === Tilburg ===
    "Tilburg": [
        "Tilburg Centrum", "Heuvel Tilburg",
        "Korvel Tilburg", "Tilburg station",
        "Piushaven Tilburg", "Spoorzone Tilburg",
    ],

    # === Den Bosch / 's-Hertogenbosch ===
    "'s-Hertogenbosch": [
        "Den Bosch Centrum", "Markt Den Bosch",
        "Sint Jan Den Bosch", "Uilenburg Den Bosch",
        "Vughterstraat Den Bosch",
    ],

    "Den Bosch": [
        "Den Bosch Centrum", "Markt Den Bosch",
        "Sint Jan Den Bosch", "Uilenburg Den Bosch",
    ],

    # === Coastal hotspots (Noord-Holland & Zuid-Holland) ===
    "Zandvoort": [
        "Zandvoort", "Zandvoort beach", "Zandvoort aan Zee",
        "Boulevard Barnaart Zandvoort", "Zandvoort centrum",
        "Bloemendaal aan Zee",
    ],

    "Bergen aan Zee": [
        "Bergen aan Zee", "Bergen NH", "Bergen Noord-Holland",
        "Bergen aan Zee beach", "Bergen aan Zee centrum",
    ],

    "Egmond aan Zee": [
        "Egmond aan Zee", "Egmond aan Zee beach",
        "Egmond aan den Hoef", "Egmond-Binnen",
    ],

    "Noordwijk aan Zee": [
        "Noordwijk", "Noordwijk aan Zee",
        "Noordwijk Binnen", "Noordwijk boulevard",
        "Noordwijk beach",
    ],

    "Katwijk aan Zee": [
        "Katwijk", "Katwijk aan Zee",
        "Katwijk boulevard", "Katwijk beach",
    ],

    "Volendam": [
        "Volendam", "Volendam harbour",
        "Volendam centrum", "Edam-Volendam",
    ],

    # === Texel — biggest Wadden island ===
    "Texel": [
        "Texel", "Den Burg Texel", "De Cocksdorp Texel",
        "De Koog Texel", "Oudeschild Texel",
        "Den Hoorn Texel", "Oosterend Texel",
        "De Waal Texel",
    ],

    # === Other Wadden islands ===
    "Vlieland": [
        "Vlieland", "Oost-Vlieland", "Vlieland beach",
    ],
    "Terschelling": [
        "Terschelling", "West-Terschelling", "Midsland Terschelling",
        "Hoorn Terschelling", "Oosterend Terschelling",
    ],
    "Ameland": [
        "Ameland", "Nes Ameland", "Hollum Ameland",
        "Ballum Ameland", "Buren Ameland",
    ],
    "Schiermonnikoog": [
        "Schiermonnikoog", "Schiermonnikoog village",
        "Schiermonnikoog beach",
    ],

    # === Zeeland coast (Walcheren + Schouwen-Duiveland) ===
    "Domburg": [
        "Domburg", "Domburg beach", "Domburg centrum",
        "Oostkapelle", "Vrouwenpolder",
    ],

    "Zoutelande": [
        "Zoutelande", "Zoutelande beach", "Westkapelle",
        "Dishoek Zoutelande",
    ],

    "Cadzand": [
        "Cadzand", "Cadzand-Bad", "Cadzand beach",
        "Nieuwvliet-Bad", "Breskens",
    ],

    "Renesse": [
        "Renesse", "Renesse beach", "Brouwersdam Renesse",
        "Burgh-Haamstede", "Westenschouwen",
    ],

    "Burgh-Haamstede": [
        "Burgh-Haamstede", "Westenschouwen",
        "Nieuw-Haamstede", "Renesse",
    ],

    # === Veluwe — forest/holiday area in Gelderland ===
    "Otterlo": [
        "Otterlo", "Hoge Veluwe", "Kröller-Müller Otterlo",
        "Hoenderloo",
    ],
    "Hoenderloo": [
        "Hoenderloo", "Hoge Veluwe", "Apeldoorn",
    ],
    "Putten Veluwe": [
        "Putten", "Putten Gelderland", "Putten Veluwe",
    ],
    "Harderwijk": [
        "Harderwijk", "Harderwijk centrum", "Harderwijk haven",
        "Dolfinarium Harderwijk",
    ],

    # === Limburg hills (Maastricht surroundings) ===
    "Valkenburg aan de Geul": [
        "Valkenburg", "Valkenburg aan de Geul",
        "Valkenburg centrum", "Vilt Valkenburg",
        "Schin op Geul",
    ],

    # === Friesland lakes / villages ===
    "Giethoorn": [
        "Giethoorn", "Giethoorn village", "Giethoorn boats",
    ],

    "Sneek": [
        "Sneek", "Sneek centrum", "Sneek harbour",
        "Waterpoort Sneek",
    ],

    "Stavoren": [
        "Stavoren", "Stavoren harbour", "Hindeloopen",
    ],

    # === Other ===
    "Delft": [
        "Delft Centrum", "Markt Delft", "Oude Kerk Delft",
        "Nieuwe Kerk Delft", "Delft station",
    ],

    "Leiden": [
        "Leiden Centrum", "Pieterswijk Leiden",
        "Leiden station", "Burcht Leiden",
    ],

    "Gouda": [
        "Gouda Centrum", "Markt Gouda", "Gouda station",
    ],

    "Arnhem": [
        "Arnhem Centrum", "Korenmarkt Arnhem",
        "Arnhem station", "Sonsbeek Arnhem",
    ],

    "Apeldoorn": [
        "Apeldoorn Centrum", "Apeldoorn station",
        "Het Loo Apeldoorn",
    ],
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
