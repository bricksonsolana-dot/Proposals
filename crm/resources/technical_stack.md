# Τεχνικό Stack Devox — Τι Χρησιμοποιούμε και Γιατί

**Σκοπός:** Αναλυτικός οδηγός με κάθε τεχνολογία που χρησιμοποιούμε και την αιτιολόγησή της. Για χρήση από πωλητές όταν ο πελάτης (ή ο "τεχνικός γιος του") ρωτήσει "γιατί αυτό κι όχι WordPress;", "τι είναι το Next.js;", "γιατί Stripe και όχι PayPal;" κλπ.

**Φιλοσοφία μας σε μία πρόταση:** Δεν χτίζουμε με templates ή WordPress. Χτίζουμε custom με σύγχρονο stack επειδή η ταχύτητα, η ασφάλεια, το SEO και η συντηρησιμότητα δεν είναι luxuries — είναι requirements που μεταφράζονται άμεσα σε κρατήσεις.

---

## ΓΡΗΓΟΡΗ ΕΠΙΣΚΟΠΗΣΗ ΤΟΥ STACK

| Κατηγορία | Επιλογή μας | Γιατί |
|---|---|---|
| **Frontend Framework** | Next.js 16 | Ταχύτητα, SEO, μεγάλο οικοσύστημα |
| **Γλώσσα Προγραμματισμού** | TypeScript | Type safety, λιγότερα bugs, καλύτερο DX |
| **Styling** | Tailwind CSS | Γρήγορο development, consistent design |
| **CMS** | Sanity | Headless, real-time, developer-friendly |
| **Database** | Supabase (PostgreSQL) | Open source, managed, RLS security |
| **Authentication** | Supabase Auth | Built-in, secure, social logins |
| **Πληρωμές** | Stripe ή Viva Wallet | Industry standard, low fees |
| **Emails** | Resend | Developer-first, υψηλό deliverability |
| **Hosting** | Vercel | Edge network, zero-config, scales αυτόματα |
| **Version Control** | Git + GitHub | Industry standard |
| **Monitoring** | Vercel Analytics + Sentry | Real-user metrics, error tracking |

---

## 1. ΓΙΑΤΙ ΟΧΙ WORDPRESS

Πριν εξηγήσουμε τι **χρησιμοποιούμε**, πρέπει να εξηγήσουμε γιατί δεν χρησιμοποιούμε WordPress — γιατί αυτή είναι η πρώτη ερώτηση κάθε πελάτη.

### Τα προβλήματα του WordPress το 2026:

1. **Ταχύτητα:** Φορτώνει 3–8x πιο αργά από custom Next.js site. Η Google τιμωρεί αργά sites στο ranking, και το 53% των mobile χρηστών εγκαταλείπουν site που φορτώνει >3''.
2. **Ασφάλεια:** Το WordPress είναι ο #1 στόχος για hackers παγκοσμίως. >90% των hacked sites το 2024 ήταν WordPress (Sucuri report). Plugins με vulnerabilities, outdated themes, brute-force attacks σε wp-admin.
3. **Plugin hell:** Για να φτιάξεις τίποτα non-trivial χρειάζεσαι 20+ plugins. Κάθε plugin = security risk + performance drop + συμβατότητα με WP updates.
4. **Συντήρηση:** WordPress core updates σπάνε plugins. Plugin updates σπάνε άλλα plugins. Δεν είναι "set and forget" — είναι "set and pray".
5. **Vendor lock-in σε plugins:** Το λεγόμενο "WordPress" σου είναι 60% κώδικας από 30 διαφορετικούς δημιουργούς που μπορεί να εξαφανιστούν αύριο.
6. **Editor experience:** Ο Gutenberg editor είναι αργός και αδέξιος. Headless CMS όπως Sanity είναι 10x καλύτερα για content teams.
7. **SEO:** Ο πελάτης χρειάζεται plugin (Yoast/RankMath) για βασικό SEO. Στο Next.js το έχουμε built-in.
8. **Custom λειτουργικότητα:** Booking engine, payment integration, complex multi-tenant setups — στο WordPress απαιτεί hacks. Στο Next.js είναι natural.

### Πότε WordPress μπορεί να έχει νόημα (σπάνια):
- Πολύ απλό blog που ο πελάτης θα γράφει posts καθημερινά και τίποτα άλλο.
- Πελάτης που έχει ήδη team εκπαιδευμένο σε WP και αρνείται να αλλάξει.

**Φράση πώλησης:** *«Το WordPress είναι σαν IKEA έπιπλα: φτηνό μέχρι να σπάσει, και τότε δεν φτιάχνει — αντικαθίσταται. Εμείς κατασκευάζουμε όπως ένας μαραγκός: ακριβότερο αρχικά, αλλά κρατάει 10 χρόνια και είναι δικό σου.»*

---

## 2. NEXT.JS 16 — ΤΟ FRONTEND FRAMEWORK ΜΑΣ

### Τι είναι;
Το Next.js είναι ένα **React-based meta-framework** της εταιρίας Vercel. Είναι το πιο διαδεδομένο σύγχρονο framework για production websites παγκοσμίως. Το χρησιμοποιούν: Netflix, TikTok, Hulu, Twitch, Notion, Loom, Hashnode, OpenAI, Anthropic.

### Γιατί Next.js (αναλυτικά):

#### α) **Ταχύτητα — Server-Side Rendering & Static Generation**

Το Next.js στέλνει στον browser **έτοιμο HTML** αντί να φορτώνει JavaScript και μετά να χτίζει τη σελίδα στον client. Αποτελέσματα:
- **First Contentful Paint < 1''**, ενώ το WordPress συνήθως είναι 2–5''.
- **Lighthouse Performance score 95–100**, ενώ τυπικό WordPress site βγάζει 30–60.
- Άμεση επίδραση στο Google ranking μέσω **Core Web Vitals**.

Έχει **3 modes rendering** που τα συνδυάζουμε στρατηγικά:
- **Static Generation (SSG):** Σελίδες που δεν αλλάζουν συχνά (homepage, about) → προ-υπολογίζονται μία φορά, σερβίρονται από CDN.
- **Server-Side Rendering (SSR):** Σελίδες με δυναμικό περιεχόμενο που πρέπει να είναι φρέσκο (search results, διαθεσιμότητα ακινήτου) → υπολογίζονται ανά request.
- **Incremental Static Regeneration (ISR):** Hybrid — σελίδες σαν static, αλλά αυτο-ενημερώνονται κάθε X λεπτά (perfect για property pages).

#### β) **SEO Out-of-the-Box**

Επειδή το server στέλνει έτοιμο HTML, το Google crawler βλέπει αμέσως όλο το περιεχόμενο. SPA frameworks (vanilla React, Vue) έχουν πρόβλημα: ο crawler βλέπει άδειο `<div id="root">`. Built-in features:
- **Metadata API** για titles, descriptions, Open Graph, Twitter Cards
- **Automatic sitemap.xml + robots.txt generation**
- **JSON-LD structured data** (schema.org) για rich snippets
- **next/image** με αυτόματο responsive sizing, WebP/AVIF conversion, lazy loading

#### γ) **App Router & React Server Components (16+)**

Η σύγχρονη αρχιτεκτονική του Next.js. Server Components τρέχουν στον server, στέλνουν μόνο το αποτέλεσμα στον browser. Πλεονεκτήματα:
- Λιγότερο JavaScript στον client → πιο γρήγορες σελίδες σε mobile/slow networks
- Direct database access από component (χωρίς ενδιάμεσο API layer)
- Streaming UI: ο χρήστης βλέπει το πρώτο μέρος της σελίδας ενώ το υπόλοιπο φορτώνει ακόμα

#### δ) **Edge Functions**

Server logic που τρέχει στο **κοντινότερο data center στον χρήστη** (Vercel έχει 100+). Latency < 50ms παγκοσμίως. Χρήσιμο για:
- Geolocation (διαφορετικό περιεχόμενο ανά χώρα)
- Authentication checks
- A/B testing

#### ε) **Image Optimization**

Το `<Image>` component του Next.js:
- Αυτόματο cropping/resizing για κάθε device
- Conversion σε WebP/AVIF (50–80% μικρότερα από JPEG)
- Lazy loading (φορτώνει μόνο όταν ο χρήστης φτάσει εκεί)
- Blur placeholder κατά τη φόρτωση

Για ξενοδοχεία/καταλύματα όπου το gallery είναι κρίσιμο, αυτό είναι game-changer.

#### στ) **Developer Experience**

- Hot reload < 1 δευτερόλεπτο
- Built-in routing βασισμένο σε file structure
- TypeScript support out-of-the-box
- Massive community → στο 99% των προβλημάτων υπάρχει ήδη λύση στο Stack Overflow

### Εναλλακτικές που απορρίψαμε:

| Framework | Γιατί όχι |
|---|---|
| **Pure React (Create React App)** | Deprecated από Meta. SPA = κακό SEO. Όχι SSR. |
| **Vue/Nuxt** | Καλό framework, αλλά μικρότερο οικοσύστημα στην Ελλάδα. Δυσκολότερη εύρεση developers αν θέλει ο πελάτης να αλλάξει εταιρία. |
| **SvelteKit** | Πολύ καλό, αλλά νεότερο. Λιγότερο production-tested για μεγάλα projects. |
| **Astro** | Εξαιρετικό για content sites (blogs), αλλά όχι κατάλληλο για interactive booking flows. |
| **Remix** | Όμοιο με Next.js αλλά μικρότερη community. Συγχωνεύτηκε με React Router. |
| **Gatsby** | Σε παρακμή. Η Netlify τον στήριζε αλλά πλέον επενδύει αλλού. |

### Τι λέμε στον πελάτη:
*«Το Next.js είναι το framework που χρησιμοποιεί το Netflix και το TikTok. Αυτό σημαίνει ότι το site σας θα φορτώνει στην ίδια ταχύτητα με αυτές τις εταιρίες. Στο SEO αυτό μεταφράζεται σε υψηλότερη θέση στο Google, στις κρατήσεις σε λιγότερους επισκέπτες που εγκαταλείπουν.»*

---

## 3. TYPESCRIPT — Η ΓΛΩΣΣΑ ΠΡΟΓΡΑΜΜΑΤΙΣΜΟΥ

### Τι είναι;
Το TypeScript είναι **JavaScript με types**. Η Microsoft το έφτιαξε το 2012 και σήμερα είναι standard στις σοβαρές εταιρίες (Google, Microsoft, Slack, Airbnb).

### Γιατί TypeScript και όχι plain JavaScript;

#### α) **Λιγότερα bugs σε production**

Έρευνα στο GitHub (Microsoft, 2017): **TypeScript προλαβαίνει 15% των bugs** πριν καν φτάσουν σε commit. Σε booking platforms αυτό σημαίνει: λιγότερες "λάθος τιμές", λιγότερα crashes στο checkout, λιγότερες εξαφανισμένες κρατήσεις.

#### β) **Καλύτερη συντήρηση μακροπρόθεσμα**

Όταν 1 χρόνο μετά κάποιος (εμείς ή άλλος developer) ανοίγει τον κώδικα για να κάνει αλλαγή, οι types λειτουργούν σαν live documentation. Δεν χρειάζεται να μαντέψει "τι είδους object είναι αυτό;".

#### γ) **Καλύτερα tooling**

VS Code (που χρησιμοποιούν 90% των developers) δίνει autocomplete, refactoring, find-all-references για TypeScript code. Σε JavaScript είναι μερικά broken.

#### δ) **Καλύτερη ομαδική εργασία**

Νέος developer μπαίνει στην ομάδα → καταλαβαίνει σε ώρες αντί για μέρες ποια είναι η δομή του project.

### Τι λέμε στον πελάτη:
*«Σκεφτείτε το έτσι: το JavaScript είναι σαν Excel χωρίς τύπους κελιών — μπορείτε να βάλετε γράμμα όπου περιμένει αριθμό και θα κρασάρει αργότερα. Το TypeScript έχει τύπους — δεν αφήνει το λάθος να γίνει εξ αρχής.»*

---

## 4. TAILWIND CSS — STYLING

### Τι είναι;
Utility-first CSS framework. Αντί να γράφεις custom CSS classes, χρησιμοποιείς έτοιμα utility classes (`flex`, `text-center`, `bg-blue-500`, κλπ).

### Γιατί Tailwind;

#### α) **Ταχύτητα ανάπτυξης**
Δεν χρειάζεται να γράψεις/συντηρήσεις custom CSS αρχεία. Το styling γίνεται απευθείας στο component.

#### β) **Consistent design**
Έτοιμη σχεδιαστική γλώσσα: spacing scale (4, 8, 16, 24...), color palette, typography scale. Όλη η εφαρμογή φαίνεται «μία» αντί για ασύνδετα κομμάτια.

#### γ) **Μικρό CSS bundle**
Το Tailwind έχει **PurgeCSS** built-in: στο production, αφαιρεί όλες τις classes που δεν χρησιμοποιούνται. Το CSS του site είναι συνήθως < 20KB (vs 100–500KB σε WordPress themes).

#### δ) **Responsive design out-of-the-box**
Mobile-first με prefixes: `md:flex`, `lg:grid-cols-3`. Ταιριάζει με το γεγονός ότι 70%+ των κρατήσεων είναι mobile.

### Εναλλακτικές που απορρίψαμε:
- **CSS Modules / Sass:** Λειτουργικό αλλά αργό development.
- **Bootstrap:** Παλιό, "βαρύ", φαίνεται όλα τα sites ίδια.
- **Material UI / Chakra:** React component libraries — μας κλειδώνουν σε "look" που δεν είναι κατάλληλο για premium hospitality.

---

## 5. SANITY CMS

### Τι είναι;
**Headless CMS** — δηλαδή ένα διαχειριστικό περιβάλλον αποκλειστικά για περιεχόμενο, που εκθέτει τα δεδομένα σε API. Το frontend (Next.js) τα τραβάει από εκεί. Ιδρύθηκε στη Νορβηγία το 2017, χρησιμοποιείται από Nike, Sonos, Figma, Cloudflare.

### Γιατί Sanity;

#### α) **Πραγματικά headless**
Το CMS δεν αναμιγνύεται με το frontend. Αυτό σημαίνει: μπορείς να αλλάξεις frontend (Next.js → άλλο) χωρίς να ξανα-εισάγεις το περιεχόμενο. Vendor independence.

#### β) **Real-time collaboration**
Πολλοί χρήστες μπορούν να επεξεργάζονται ταυτόχρονα (όπως Google Docs). Κρίσιμο για hospitality teams όπου ο owner, ο property manager και η Hosthub ίσως έχουν παράλληλη πρόσβαση.

#### γ) **Schema-driven**
Ο schema του Sanity ορίζεται σε κώδικα. Αυτό σημαίνει: type-safe content (τα πεδία γνωστά εκ των προτέρων), version control του schema στο Git, εύκολες αλλαγές.

#### δ) **Generous free tier**
- 3 χρήστες, 10K documents, 1M API requests / μήνα δωρεάν
- Ξεπερνώντας: $99/μήνα (αλλά τυπικά μικρό-μεσαίο ξενοδοχειακό σύστημα μένει στο free tier)

#### ε) **Sanity Studio**
Το διαχειριστικό περιβάλλον είναι ένα React app. Customizable: μπορούμε να φτιάξουμε επιπλέον widgets για τον πελάτη (π.χ. preview κράτησης, integration με Hosthub button).

#### στ) **Έξοχο media handling**
Image hotspot/crop editing built-in. Ιδανικό για hospitality όπου το gallery είναι κεντρικό.

### Εναλλακτικές που εξετάσαμε:

| CMS | Γιατί όχι |
|---|---|
| **Contentful** | Πολύ ακριβό σε scale (από $300/μήνα). |
| **Strapi** | Self-hosted = ευθύνη υποδομής. Καλό αλλά απαιτεί δικό μας server. |
| **Payload CMS** | Πολύ καλό, αλλά νεότερο, μικρότερη community. |
| **Storyblok** | Visual editor είναι gimmick· δεν θέλουμε το CMS να ξέρει για το frontend layout. |
| **Directus** | Database-first, καλό για existing PostgreSQL DBs αλλά λιγότερο polished editor. |
| **WordPress (headless)** | Ακόμα έχει όλα τα προβλήματα του WP από κάτω. |

### Πότε το παρακάμπτουμε:
Στις προσφορές με **«Managed Content»** (όπου εμείς ανεβάζουμε καταλύματα) δεν χρειάζεται CMS — το περιεχόμενο μπαίνει απευθείας από εμάς. Αυτό μειώνει το αρχικό κόστος ανάπτυξης κατά ~€500–€1.000.

---

## 6. SUPABASE — DATABASE & AUTH

### Τι είναι;
Open-source εναλλακτική του Firebase. Built πάνω σε **PostgreSQL** (το πιο σοβαρό relational database του κόσμου). Παρέχει: database, authentication, storage, real-time subscriptions, edge functions.

### Γιατί Supabase;

#### α) **PostgreSQL**
Όχι NoSQL hype. Πραγματικό SQL με transactions, foreign keys, indexes. Battle-tested εδώ και 30 χρόνια.

#### β) **Row Level Security (RLS)**
Δυνατότητα PostgreSQL: ορίζεις στο επίπεδο της βάσης ποιος μπορεί να δει/τροποποιήσει ποια rows. Αυτό σημαίνει ότι ακόμα κι αν κάποιος βρει τρόπο να παρακάμψει το app layer, η βάση τον σταματά. **Major security advantage** για multi-tenant πλατφόρμες (πολλά καταλύματα, πολλοί owners).

#### γ) **Authentication built-in**
- Email/password
- Magic links (passwordless)
- OAuth (Google, Facebook, Apple)
- Phone OTP
- 2FA

Όλα δωρεάν μέχρι 50.000 monthly active users. Πέραν: $0.00325 / MAU.

#### δ) **Real-time subscriptions**
Αν θέλουμε live updates (π.χ. live διαθεσιμότητα όταν γίνεται κράτηση από άλλον χρήστη ταυτόχρονα), στέλνει push σε όλους τους connected clients.

#### ε) **Open source + ευκολία migration**
Αν θέλουμε να φύγουμε από το Supabase, μπορούμε να εξάγουμε όλη τη βάση σε δικό μας PostgreSQL server με ένα εντολή. Όχι vendor lock-in.

#### στ) **Generous free tier**
- 500MB database, 1GB file storage, 50K MAU
- Pro: $25/μήνα για 8GB DB, 100GB transfer

### Εναλλακτικές που εξετάσαμε:

| DB | Γιατί όχι |
|---|---|
| **Firebase (Google)** | NoSQL = δύσκολες σχέσεις (κρατήσεις ↔ ακίνητα). Vendor lock-in. |
| **MongoDB Atlas** | NoSQL, ίδιο πρόβλημα. |
| **Vercel Postgres** | Καλό αλλά νεότερο, λιγότερα features από Supabase. |
| **AWS RDS** | Σωστό για enterprise, υπερβολικό setup για ξενοδοχεία. |
| **PlanetScale** | MySQL-based, χωρίς foreign keys, λιγότερο κατάλληλο. |

---

## 7. STRIPE — ΠΛΗΡΩΜΕΣ (& VIVA WALLET ΩΣ ΕΛΛΗΝΙΚΗ ΕΝΑΛΛΑΚΤΙΚΗ)

### Stripe — Τι είναι;
Η Stripe είναι ο de facto παγκόσμιος leader σε payment processing. Χρησιμοποιείται από Amazon, Google, Shopify, Lyft, Spotify, Zoom.

### Γιατί Stripe;

#### α) **Ποιότητα API**
Το πιο κομψό payment API που υπάρχει. Καλύτερο documentation, καλύτερο testing, λιγότερα edge cases.

#### β) **Παγκόσμια κάλυψη**
135+ νομίσματα, υποστηρίζει: Visa, Mastercard, Amex, Apple Pay, Google Pay, SEPA, iDEAL, Klarna, Afterpay, κλπ. Κρίσιμο για διεθνείς επισκέπτες.

#### γ) **Stripe Radar**
AI fraud detection built-in. Βλοκάρει ύποπτες συναλλαγές χωρίς extra setup.

#### δ) **Stripe Connect (πολλαπλοί ιδιοκτήτες)**
Αν στο μέλλον η πλατφόρμα έχει πολλούς ιδιοκτήτες ακινήτων που θέλουν direct payouts, το Stripe Connect είναι **the standard solution** για marketplace platforms.

#### ε) **Fees**
- 1,5% + €0,25 ανά συναλλαγή (Ευρώπη)
- Χωρίς setup fee, χωρίς monthly fee
- Άμεσο payout σε IBAN κάθε 7 μέρες

### Viva Wallet — Πότε προτείνουμε

Η Viva είναι ελληνική εταιρία. Πλεονεκτήματα:
- Ελληνική νομική οντότητα (αν ο πελάτης θέλει domestic provider)
- Ελληνική υποστήριξη στα Ελληνικά
- Παρόμοια fees με Stripe (~1,5%)
- Καλό integration με myDATA

**Μειονεκτήματα Viva σε σχέση με Stripe:**
- API ποιότητα κατώτερη
- Λιγότερα features (όχι Radar, όχι Connect-equivalent)
- Διεθνείς πελάτες σπανιότερα γνωρίζουν τη Viva

**Default σύσταση μας:** Stripe για διεθνή sites, Viva αν ο πελάτης το προτιμά ή έχει ήδη τερματικό POS της Viva.

### Εναλλακτικές που απορρίπτουμε:
- **PayPal:** Παλιό, υψηλά fees (~3%), κακή UX. Όλο και λιγότεροι το χρησιμοποιούν.
- **Eurobank/Πειραιώς direct:** Παλιότερα APIs, δύσκολη ολοκλήρωση, υψηλά fees.

---

## 8. RESEND — TRANSACTIONAL EMAILS

### Τι είναι;
Νεότερη υπηρεσία (2023, από τους creators του React Email) για αποστολή transactional emails (booking confirmations, password resets, κλπ).

### Γιατί Resend;

#### α) **Developer experience**
Το API είναι 10 γραμμές κώδικα. SendGrid (παλιότερη εναλλακτική) χρειάζεται 100+ γραμμές για το ίδιο.

#### β) **React Email**
Μπορούμε να γράφουμε email templates σε **React components** αντί για HTML soup. Type-safe, reusable, αυτόματη συμβατότητα με Outlook, Gmail, Apple Mail.

#### γ) **Deliverability**
Built-in DKIM, SPF, DMARC setup. Τα emails πέφτουν στο inbox, όχι στο spam. (Ο μεγαλύτερος εφιάλτης στα emails είναι "γιατί δεν ήρθε το confirmation;")

#### δ) **Tracking**
Ποιά emails ανοίχτηκαν, ποια clicks, ποια bounced. Όλα σε live dashboard.

#### ε) **Pricing**
- 3.000 emails/μήνα δωρεάν
- $20/μήνα για 50.000 emails
- Φθηνότερο από SendGrid ($89/μήνα για 50K)

### Εναλλακτικές:
- **SendGrid:** Παλιό, λειτουργικό, ακριβότερο, χειρότερο DX.
- **Mailgun:** OK αλλά γερασμένο.
- **AWS SES:** Φθηνότερο σε scale, αλλά πολύ χαμηλό-level (πρέπει να χτίσεις πολλά γύρω του).
- **Postmark:** Καλή deliverability αλλά API παλιότερο.

---

## 9. VERCEL — HOSTING

### Τι είναι;
Η εταιρία πίσω από το Next.js. Παρέχει managed hosting βελτιστοποιημένο για Next.js apps.

### Γιατί Vercel;

#### α) **Zero-config deployment**
`git push` → site live σε 30''. Καμία διαμόρφωση server, κανένα Apache/nginx. Preview deployments σε κάθε pull request (περνάμε link στον πελάτη πριν το merge).

#### β) **Παγκόσμιο CDN (Edge Network)**
Static assets σερβίρονται από το κοντινότερο data center στον επισκέπτη. 100+ POPs παγκοσμίως. Latency < 50ms σχεδόν παντού.

#### γ) **Automatic HTTPS**
Let's Encrypt SSL αυτόματα, auto-renew, χωρίς να σκεφτείς τίποτα.

#### δ) **Auto-scaling**
Site γίνεται viral με 10.000 ταυτόχρονους χρήστες; Το Vercel scaling το χειρίζεται αυτόματα. Δεν κρασάρει.

#### ε) **DDoS protection**
Built-in. Στο shared hosting θα πέσει με την πρώτη επίθεση.

#### στ) **Pricing**
- **Hobby (free):** 100GB bandwidth/μήνα, αρκετά για μικρά sites
- **Pro ($20/μήνα):** 1TB bandwidth, αναλυτικά, αρκεί για 99% των hospitality projects μας

### Εναλλακτικές:
- **Netlify:** Παρόμοιο, λίγο χειρότερη υποστήριξη Next.js
- **Cloudflare Pages:** Φθηνότερο, αλλά λιγότερα features
- **AWS Amplify:** Πολύπλοκο, μόνο για enterprise
- **Self-hosted (VPS):** €20–50/μήνα + ώρες συντήρησης. Δεν αξίζει.

---

## 10. ΑΡΧΙΤΕΚΤΟΝΙΚΗ ΣΕ ΜΙΑ ΕΙΚΟΝΑ

```
Επισκέπτης → Cloudflare DNS → Vercel Edge (CDN)
                                    ↓
                              Next.js (App Router)
                              ├─ Static pages (SSG)
                              ├─ Dynamic pages (SSR/ISR)
                              └─ API routes (serverless)
                                    ↓
                ┌───────────────────┼─────────────────┐
                ↓                   ↓                 ↓
            Supabase            Sanity CMS        Hosthub
            (PostgreSQL)        (περιεχόμενο)     (channel mgr)
                ↓                                       ↑
                └───────────────────────────────────────┘
                              iCal / API sync
                                    ↓
            Stripe / Viva ← (πληρωμές) ← (κράτηση)
                ↓
            Resend (email confirmation)
```

---

## 11. SECURITY & GDPR — ΤΙ ΚΑΝΟΥΜΕ ΑΥΤΟΜΑΤΑ

- **HTTPS παντού** (Let's Encrypt μέσω Vercel)
- **Row Level Security** στη βάση (Supabase RLS)
- **Πληρωμές μέσω Stripe iframe** — οι αριθμοί κάρτας **ποτέ** δεν περνούν από τον δικό μας server (PCI compliance handled by Stripe)
- **CSRF, XSS protection** built-in στο Next.js
- **Rate limiting** στα APIs
- **Audit log** για admin ενέργειες
- **Cookie consent banner** GDPR-compliant
- **Privacy Policy / Terms / Cookies pages** συμπεριλαμβανομένες
- **Backup** ημερησίως (Supabase automatic backups)

---

## 12. ΠΟΙΑ ΕΡΓΑΛΕΙΑ ΧΡΗΣΙΜΟΠΟΙΟΥΜΕ ΕΣΩΤΕΡΙΚΑ (development)

| Εργαλείο | Σκοπός |
|---|---|
| **Git + GitHub** | Version control, code review |
| **VS Code + Cursor** | IDE με AI assistance |
| **pnpm** | Package manager (γρηγορότερος από npm) |
| **ESLint + Prettier** | Code quality, consistent formatting |
| **Vitest** | Unit testing |
| **Playwright** | End-to-end testing (booking flows) |
| **Sentry** | Error tracking σε production |
| **Vercel Analytics** | Real-user performance metrics |
| **Linear** | Project management, ticket tracking |
| **Figma** | UI design |

---

## 13. ΓΡΗΓΟΡΕΣ ΑΠΑΝΤΗΣΕΙΣ ΣΕ ΣΥΧΝΕΣ ΕΡΩΤΗΣΕΙΣ ΠΕΛΑΤΩΝ

**«Πότε θα φτιαχτεί;»** → 3–8 εβδομάδες ανάλογα με scope.

**«Θα μπορώ να αλλάζω εγώ τα κείμενα;»** → Στις προσφορές με CMS, ναι. Χωρίς CMS, στέλνεις σε εμάς και κάνουμε εμείς τις αλλαγές.

**«Είναι responsive σε κινητά;»** → Mobile-first σχεδιασμός. Πρώτα φτιάχνουμε το mobile και μετά scale up.

**«Θα φαίνεται στο Google;»** → Ναι, με όλα τα SEO best practices ενσωματωμένα. Αλλά ranking θέλει χρόνο και content.

**«Τι γίνεται αν θέλω να αλλάξω εταιρία;»** → Παίρνεις τον πλήρη πηγαίο κώδικα και τα στοιχεία πρόσβασης σε όλες τις υπηρεσίες (Vercel, Supabase, Sanity, Stripe). Καμία υπηρεσία δεν είναι "δική μας" — όλες είναι λογαριασμοί στο όνομά σου.

**«Θα δουλεύει αν έρθουν 1000 άτομα ταυτόχρονα;»** → Ναι, το Vercel auto-scaling το χειρίζεται. Ίδιο stack σερβίρει εκατομμύρια χρήστες σε άλλα projects.

**«Πληρώνω εγώ ή εσείς για Vercel/Supabase/Sanity;»** → Εσύ, απευθείας στους παρόχους. Δίνουμε εμείς το setup, τα accounts είναι στο όνομά σου, και οι περισσότερες υπηρεσίες έχουν free tier που αρκεί για start.

**«Τι γίνεται αν εξαφανιστείτε εσείς;»** → Πηγαίος κώδικας στο GitHub στο όνομά σου. Όλο το stack είναι standard τεχνολογίες — οποιοσδήποτε Next.js developer μπορεί να συνεχίσει. Δεν είσαι κλειδωμένος σε εμάς.

**«WordPress δεν είναι πιο φθηνό;»** → Αρχικά ναι, μακροπρόθεσμα όχι. Plugin licenses, security patches, slow performance που χάνει κρατήσεις, hacks που χρειάζονται restore — όλα κοστίζουν. Custom Next.js αποσβένεται σε 1–2 χρόνια.

**«Πληρώνω μηνιαία για το stack ή μόνο μία φορά;»** → Μία φορά κόστος ανάπτυξης. Μηνιαίως: μικρά κόστη third-party (€0–€85), προαιρετικό πακέτο συντήρησης, Hosthub subscription (αν ήδη χρησιμοποιείς).

---

## 14. ΣΥΝΟΨΗ ΓΙΑ ΠΩΛΗΤΕΣ

Όταν ο πελάτης ρωτάει **«γιατί τόσο ακριβό;»**:

> *«Δεν χρησιμοποιούμε WordPress γιατί το WordPress σε κοστίζει αργοπορία, hacks, και hosting θέματα μακροπρόθεσμα. Χτίζουμε με Next.js, το ίδιο framework που χρησιμοποιεί το Netflix και το TikTok. Η βάση δεδομένων είναι Supabase, που το χρησιμοποιούν για 1 εκατομμύριο χρήστες. Οι πληρωμές με Stripe — Amazon, Google, Spotify. Το hosting σε Vercel, που scale-άρει αυτόματα από 10 σε 10.000 επισκέπτες χωρίς να κρασάρει. Όλο αυτό σημαίνει ότι το site σου θα φορτώνει σε 1 δευτερόλεπτο, θα βγαίνει υψηλά στο Google, δεν θα hack-αρθεί, και αν αύριο θες να αλλάξεις εταιρία ή να επεκτείνεις, ο κώδικας είναι 100% δικός σου, χωρίς vendor lock-in. Σε WordPress θα πληρώσεις λιγότερα τώρα και διπλάσια σε 2 χρόνια — ή θα χάσεις κρατήσεις σιωπηλά γιατί το site είναι αργό και ο χρήστης φεύγει.»*

---

**Τελευταία ενημέρωση:** Μάιος 2026
**Συντήρηση εγγράφου:** Αν αλλάξει το stack (π.χ. αναβάθμιση σε Next.js 17, αλλαγή CMS), ενημερώνουμε εδώ.
