# Lead Finder — Ξενοδοχεία/Καταλύματα χωρίς Website

Βρίσκει αυτόματα ξενοδοχεία, studios, villas και rooms σε ελληνικές τουριστικές περιοχές που **έχουν τηλέφωνο αλλά ΔΕΝ έχουν δικό τους website** — έτοιμα leads για cold calling.

Πηγή δεδομένων: **Google Maps** (μέσω Playwright browser automation).

---

## 🚀 Γρηγορότερος τρόπος: Web Dashboard

```bash
cd c:\Users\odyst\Git-Repositories\Proposals\lead-finder
python dashboard.py
```

Άνοιξε **http://localhost:5000** στον browser. Από εκεί:
- ✅ Επιλέγεις περιοχές με ένα click
- ✅ Πατάς **Start** ή **Scrape ALL**
- ✅ Βλέπεις live πρόοδο (ποια περιοχή σαρώνεις τώρα, πόσα leads βρήκες)
- ✅ Βλέπεις τον πίνακα με όλα τα leads — ανανεώνεται αυτόματα κάθε 5 sec
- ✅ Φιλτράρεις ανά περιοχή ή με αναζήτηση
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
```
Χρόνος: ~10 λεπτά. Output: ~20-40 νέα leads.

### Πολλαπλές περιοχές
```bash
python find_leads.py --regions Paros,Naxos,Mykonos
```

### Όλες οι περιοχές (74 σύνολο)
```bash
python find_leads.py --all
```
Χρόνος: ~12 ώρες. Άστο να τρέχει στο background.

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

**Στήλες του master CSV**: `region`, `name`, `category`, `phone`, `email`

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

## 5. Διαθέσιμες περιοχές (74)

Δες το πλήρες [regions.py](regions.py). Ομαδοποιημένα:

- **Αττική (21)**: Athens, Piraeus, Glyfada, Voula, Vouliagmeni, Varkiza, Lagonisi, Anavyssos, Saronida, Palaia Fokaia, Sounio, Marathon, Schinias, Nea Makri, Rafina, Porto Rafti, Lavrio, Aegina, Spetses, Hydra, Poros
- **Κυκλάδες (21)**: Paros, Antiparos, Naxos, Mykonos, Santorini, Ios, Milos, Kimolos, Sifnos, Serifos, Kythnos, Kea, Tinos, Andros, Syros, Folegandros, Sikinos, Amorgos, Anafi, Koufonisia, Donousa
- **Β. Αιγαίο (11)**: Lesbos, Chios, Samos, Ikaria, Fourni, Lemnos, Agios Efstratios, Thassos, Samothrace, Psara, Oinousses
- **Δωδεκάνησα (13)**: Rhodes, Kos, Karpathos, Patmos, Leros, Kalymnos, Symi, Tilos, Astypalaia, Nisyros, Halki, Kasos, Lipsi
- **Σποράδες (4)**: Skiathos, Skopelos, Alonissos, Skyros
- **Λευκάδα (4)**: Lefkada, Lefkada-Vasiliki, Lefkada-Nidri, Lefkada-Agios-Nikitas

### Προσθήκη νέας περιοχής

Άνοιξε το [regions.py](regions.py) και πρόσθεσε γραμμή:
```python
"Όνομα Περιοχής": (south, west, north, east),
```

Το bbox δεν είναι απαραίτητο για το Google Maps — το όνομα μετράει. Μπορείς να βάλεις dummy values:
```python
"My New Place": (0, 0, 0, 0),
```

---

## 6. Πώς δουλεύει εσωτερικά

Για κάθε περιοχή τρέχει 4 Google Maps queries:
1. `hotels in <region>`
2. `studios in <region>`
3. `rooms <region>`
4. `ξενοδοχείο <region>`

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
├── gmaps_scraper.py     ← Google Maps scraper logic
├── refilter.py          ← re-apply filter στα raw CSVs
├── regions.py           ← λίστα 74 περιοχών
├── requirements.txt     ← Python dependencies
├── README.md            ← αυτό το αρχείο
└── output/
    ├── all_leads.csv
    ├── all_leads.txt
    └── raw/
        └── <region>.csv
```
