# Lead Finder — Ξενοδοχεία/Καταλύματα χωρίς Website

Βρίσκει αυτόματα ξενοδοχεία, studios, villas, apartments, rooms και B&Bs σε τουριστικές περιοχές που **έχουν τηλέφωνο αλλά ΔΕΝ έχουν δικό τους website** — έτοιμα leads για cold calling.

**Υποστηριζόμενες χώρες:** 🇬🇷 Ελλάδα · 🇳🇱 Ολλανδία (επεκτάσιμο σε όποια χώρα θες — δες §9)

Πηγή δεδομένων: **Google Maps** (μέσω Playwright browser automation).

---

## 🚀 Γρηγορότερος τρόπος: Web Dashboard

```bash
cd c:\Users\odyst\Git-Repositories\Proposals\lead-finder
python dashboard.py
```

Άνοιξε **http://localhost:5000** στον browser. Από εκεί:
- ✅ Επιλέγεις περιοχές με ένα click — οργανωμένες ανά **χώρα → group → περιοχή**
- ✅ Πατάς **Start** ή **Scrape ALL**
- ✅ Βλέπεις live πρόοδο (ποια περιοχή σαρώνεις τώρα, πόσα leads βρήκες)
- ✅ Βλέπεις τον πίνακα με όλα τα leads — ανανεώνεται αυτόματα κάθε 5 sec
- ✅ Φιλτράρεις ανά **χώρα** (🇬🇷 Greece / 🇳🇱 Netherlands), ανά περιοχή, ή με free text αναζήτηση
- ✅ Πατάς **Stop** όποτε θες

---

## 1. Setup (μία φορά μόνο)

Αν στήνεις το project σε καινούργιο υπολογιστή:

```bash
cd lead-finder
pip install -r requirements.txt
pip install flask
python -m playwright install chromium
```

Στον δικό σου υπολογιστή είναι ήδη εγκατεστημένα.

---

## 2. Πώς το τρέχεις

Πάντα πρώτα μπες στον φάκελο:

```bash
cd c:\Users\odyst\Git-Repositories\Proposals\lead-finder
```

Μετά διάλεξε εντολή:

### Μία περιοχή
```bash
python find_leads.py --region Paros
python find_leads.py --region Amsterdam       # Netherlands example
```
Χρόνος: ~10 λεπτά για μικρή περιοχή, ~1 ώρα για Amsterdam (53 neighborhoods × 12 queries). Output: ~20-200 νέα leads.

### Πολλαπλές περιοχές
```bash
python find_leads.py --regions Paros,Naxos,Mykonos
python find_leads.py --regions Amsterdam,Rotterdam,"The Hague"
```

### Όλες οι περιοχές (όλες οι χώρες)
```bash
python find_leads.py --all
```
Χρόνος: ~24+ ώρες (Greece+Netherlands μαζί). Άστο να τρέχει στο background.

### Συνέχιση μετά από διακοπή (resume)
Αν διέκοψες με Ctrl+C ή έκλεισε ο υπολογιστής:
```bash
python find_leads.py --all --skip-existing
```
Παραλείπει όσες περιοχές έχουν ήδη raw αρχείο και συνεχίζει από εκεί που σταμάτησε.

### Debug με ορατό browser
Αν κάτι δεν δουλεύει σωστά:
```bash
python find_leads.py --region Paros --headed
```
Ανοίγει το Chrome και βλέπεις τι κάνει.

---

## 3. Πού πάνε τα αποτελέσματα

```
lead-finder/output/
├── all_leads.csv      ← MASTER αρχείο. Όλα τα leads από ΟΛΕΣ τις περιοχές.
├── all_leads.txt      ← Ίδια δεδομένα σε στυλ cold-call list.
└── raw/
    ├── Athens.csv
    ├── Paros.csv
    └── ...            ← Raw scraped data ανά περιοχή (για debugging / re-filter)
```

**Στήλες του master CSV**: `country`, `region`, `name`, `category`, `phone`, `email`, `gmaps_url`, `online_presence`, `domain_gr_available`, `domain_com_available`, `domain_suggestion`, `enriched_at`

Η στήλη `category` δείχνει τι τύπος επιχείρησης είναι σύμφωνα με το Google Maps (π.χ. "Hotel", "Apartment building", "Vacation home rental agency", "Bed and breakfast"). Άσχετες επιχειρήσεις (tattoo studio, recording studio, real estate agency, restaurants κλπ) **φιλτράρονται αυτόματα**.

**Format του master TXT**:
```
////Athens////
Hotel ABC [Hotel] , 2106422418
Studios XYZ [Apartment building] , 6932749195

////Paros////
Margarita Rooms [Vacation home rental agency] , 2284051123
...
```

Κάθε νέο run **προσθέτει** στο master χωρίς να σβήσει τα παλιά. Deduplication γίνεται με βάση `(περιοχή, τηλέφωνο)` — δεν θα δεις διπλά leads.

---

## 4. Re-filter παλιών δεδομένων

Αν αναβαθμίσεις τη blacklist των OTAs στο [gmaps_scraper.py](gmaps_scraper.py) (π.χ. βρεις νέο aggregator), δεν χρειάζεται να ξανακάνεις scraping. Απλώς:

```bash
python refilter.py
```

Ξανατρέχει το φίλτρο σε όλα τα `raw/*.csv` και προσθέτει τα νέα leads στο master.

Ή για συγκεκριμένες περιοχές:
```bash
python refilter.py Paros Athens
```

---

## 5. Διαθέσιμες περιοχές

Δες το πλήρες [regions.py](regions.py). Δομή: **χώρα → group → region**.

### 🇬🇷 Greece (76 regions)

- **Αττική (21)**: Athens, Piraeus, Glyfada, Voula, Vouliagmeni, Varkiza, Lagonisi, Anavyssos, Saronida, Palaia Fokaia, Sounio, Marathon, Schinias, Nea Makri, Rafina, Porto Rafti, Lavrio, Aegina, Spetses, Hydra, Poros
- **Κυκλάδες (21)**: Paros, Antiparos, Naxos, Mykonos, Santorini, Ios, Milos, Kimolos, Sifnos, Serifos, Kythnos, Kea, Tinos, Andros, Syros, Folegandros, Sikinos, Amorgos, Anafi, Koufonisia, Donousa
- **Β. Αιγαίο (11)**: Lesbos, Chios, Samos, Ikaria, Fourni, Lemnos, Agios Efstratios, Thassos, Samothrace, Psara, Oinousses
- **Δωδεκάνησα (13)**: Rhodes, Kos, Karpathos, Patmos, Leros, Kalymnos, Symi, Tilos, Astypalaia, Nisyros, Halki, Kasos, Lipsi
- **Σποράδες (4)**: Skiathos, Skopelos, Alonissos, Skyros
- **Επτάνησα (6)**: Corfu, Lefkada, Zakynthos, Kefalonia, Ithaca, Paxi

### 🇳🇱 Netherlands (~86 regions)

- **Noord-Holland**: Amsterdam (53 neighborhoods!), Haarlem, Zandvoort, Bloemendaal, Egmond aan Zee, Bergen aan Zee, Volendam, Texel, ...
- **Zuid-Holland**: Rotterdam, The Hague / Den Haag, Scheveningen, Delft, Leiden, Noordwijk aan Zee, Katwijk aan Zee, ...
- **Utrecht**: Utrecht, Amersfoort, Soest, Zeist, ...
- **Noord-Brabant**: Eindhoven, Den Bosch, Breda, Tilburg, ...
- **Gelderland (Veluwe)**: Arnhem, Nijmegen, Apeldoorn, Otterlo, Hoenderloo, Harderwijk, ...
- **Limburg**: Maastricht, Valkenburg aan de Geul, Heerlen, ...
- **Zeeland**: Domburg, Zoutelande, Cadzand, Renesse, Burgh-Haamstede, Veere, ...
- **Friesland**: Leeuwarden, Sneek, Vlieland, Terschelling, Ameland, Schiermonnikoog, ...
- **Noord-Nederland**: Groningen, Giethoorn, Zwolle, Deventer, Lelystad, ...

Hot destinations έχουν αναλυτικό **village/neighborhood expansion** (όπως η Athens). Π.χ. το Amsterdam σπάει σε Centrum, Jordaan, De Pijp, Oud-Zuid, Vondelpark, NDSM Noord, Bijlmer κλπ — 53 search targets × 12 queries = ~600 Google Maps searches → πολλαπλά εκατοντάδες leads.

### Προσθήκη νέας περιοχής σε υπάρχουσα χώρα

Άνοιξε το [regions.py](regions.py), βρες την χώρα μέσα στο `COUNTRIES` και πρόσθεσε το όνομα στο σχετικό group:
```python
"Greece": {
    "code": "GR",
    "groups": {
        "Κυκλάδες": [..., "My New Island"],   # ← ΕΔΩ
        ...
    },
},
```

Optional αλλά συνιστώμενο: για μεγάλες πόλεις/προορισμούς, πρόσθεσε neighborhoods στο [villages.py](villages.py):
```python
VILLAGES["My New Island"] = [
    "My New Island Town", "Beach 1", "Village 2", ...
]
```

---

## 6. Πώς δουλεύει εσωτερικά

Για κάθε περιοχή (ή για κάθε village αν έχει expansion) τρέχει 12 Google Maps queries σε 3 γλώσσες:

**Αγγλικά** (δουλεύουν παντού):
1. `hotels in <region>`
2. `rooms <region>`
3. `apartments <region>`
4. `studios <region>`
5. `bed and breakfast <region>`
6. `guest house <region>`

**Ελληνικά**:
7. `ξενοδοχεία <region>`
8. `δωμάτια <region>`

**Ολλανδικά**:
9. `appartementen <region>`
10. `B&B <region>`
11. `vakantiehuis <region>`
12. `pension <region>`

Για κάθε query:
- Σκρολάρει τη λίστα results μέχρι να εμφανιστούν όλα (~120 cards)
- Κάνει click κάθε card → παίρνει όνομα, τηλέφωνο, website, διεύθυνση από το side panel
- Φιλτράρει: κρατάει μόνο όσα έχουν phone και ΔΕΝ έχουν real website (μόνο OTA listings επιτρέπονται)

**Φιλτραρισμένα domains** (θεωρούνται "δεν έχει website"):
- Major OTAs: booking.com, airbnb.com, expedia.com, hotels.com, agoda.com, tripadvisor.com, vrbo.com, hostelworld.com
- Aggregators: bluepillow.com, hotelscheck-in.com, freecancellations.com, snaptrip.com, hotel-cyclades.com
- Social/link-in-bio: facebook.com, instagram.com, linktr.ee, wa.me
- Page builders: sites.google.com, wixsite.com, weebly.com, blogspot.com

Πλήρης λίστα στο [gmaps_scraper.py](gmaps_scraper.py) → `OTA_DOMAINS`.

---

## 7. Common issues

### "Executable doesn't exist at ms-playwright/chromium"
Το Playwright browser δεν είναι εγκατεστημένο. Τρέξε:
```bash
python -m playwright install chromium
```
Αν αποτύχει με network error, δοκίμασε διαφορετικό network/VPN.

### "found 0 cards in panel"
Πιθανόν το Google άλλαξε το DOM. Τρέξε με `--headed` για να δεις τι συμβαίνει.

### Πολύ λίγα leads από μια περιοχή
Φυσιολογικό για μικρά νησιά (Donousa, Sikinos κλπ). Σε μεγάλους προορισμούς περιμένεις 20-50 leads.

---

## 8. Αρχεία project

```
lead-finder/
├── find_leads.py        ← κύριο script (το τρέχεις εσύ)
├── gmaps_scraper.py     ← Google Maps scraper logic + queries σε 3 γλώσσες
├── regions.py           ← COUNTRIES dict — Greece + Netherlands (162 regions)
├── villages.py          ← neighborhood expansion για hot destinations
├── enrich.py            ← .gr/.com domain availability checker
├── dashboard.py         ← Flask web UI (country filter + chips)
├── crm_sync.py          ← push leads στο CRM
├── requirements.txt     ← Python dependencies
├── README.md            ← αυτό το αρχείο
└── output/
    └── leads.csv        ← master CSV (country, region, name, phone, ...)
```

---

## 9. Πώς προσθέτω καινούργια χώρα

Όλο το system είναι data-driven από το `COUNTRIES` dict στο [regions.py](regions.py). Για να προσθέσεις π.χ. **Italy**:

### Βήμα 1: Πρόσθεσε την χώρα στο [regions.py](regions.py)

```python
COUNTRIES = {
    "Greece": {...},
    "Netherlands": {...},
    "Italy": {                       # ← νέα χώρα
        "code": "IT",
        "groups": {
            "Lazio": ["Rome", "Ostia", "Tivoli"],
            "Tuscany": ["Florence", "Siena", "Pisa", "Lucca"],
            "Amalfi Coast": ["Amalfi", "Positano", "Sorrento", "Capri"],
            "Sicily": ["Palermo", "Catania", "Taormina", "Syracuse"],
        },
    },
}
```

### Βήμα 2 (optional): Πρόσθεσε neighborhoods για μεγάλες πόλεις στο [villages.py](villages.py)

```python
VILLAGES["Rome"] = [
    "Rome Centro Storico", "Trastevere", "Monti Rome",
    "Testaccio Rome", "Prati Rome", "Vatican Rome",
    "Termini Rome", "Aventino Rome", ...
]
```

### Βήμα 3 (optional): Πρόσθεσε Ιταλικά queries στο [gmaps_scraper.py](gmaps_scraper.py) → `QUERIES_PER_REGION`

```python
"hotel {region}",
"appartamento {region}",
"bed and breakfast {region}",
"agriturismo {region}",
"pensione {region}",
"camere {region}",
```

Και στα `ACCOMMODATION_CATEGORIES`:
```python
"agriturismo", "pensione", "camere", "casa vacanze",
```

### Βήμα 4: Restart το dashboard

```bash
python dashboard.py
```

Η νέα χώρα εμφανίζεται αυτόματα:
- Στο sidebar region picker (group by country)
- Στα country filter chips επάνω από τον leads πίνακα
- Στο `country` column κάθε νέου lead στο CSV
- Στο flag (🌍 default — πρόσθεσε emoji στο `COUNTRY_FLAGS` mapping του dashboard.py για ωραία icon)

**Τίποτα άλλο δεν χρειάζεται αλλαγή.** Το `find_leads.py`, `enrich.py`, `crm_sync.py`, `dashboard.py` διαβάζουν από τα ίδια data structures.
