"""
Seed corpus generator for TM Compass.

Generates ~3,500-4,500 realistic EU trademark filings based on real brands
across Nice classes 9, 25, 35, 41. Each brand gets 5-15 variant filings
that mirror how real portfolios look:
  - Base word marks plus sub-brand variants ("NIKE AIR", "NIKE PRO")
  - Famous taglines for marquee brands ("JUST DO IT", "THINK DIFFERENT")
  - Cross-class filings (one owner files across multiple Nice classes)
  - Mix of mark types (word, figurative, combined, 3D, sound)
  - Realistic goods/services descriptions drawn from Nice class verbiage
  - Application dates spread 2018-2025; status weighted toward Registered

Weekend 1 unblock — TMview's public API is currently returning 500s.
The pipeline is API-agnostic; swap in EUIPO open-data bulk download later.
"""
import json
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(42)

OUT = Path(__file__).parent.parent / "data" / "raw" / "trademarks.jsonl"
OUT.parent.mkdir(parents=True, exist_ok=True)

# === BRAND CATALOG ============================================================
BRANDS = {
    "9": [
        "Apple", "Samsung", "Sony", "Microsoft", "Nintendo", "Bose", "Dell",
        "HP", "Lenovo", "ASUS", "Acer", "Logitech", "Razer", "Garmin", "Fitbit",
        "GoPro", "DJI", "Nokia", "Motorola", "Xiaomi", "Huawei", "OnePlus",
        "Philips", "LG", "Panasonic", "JBL", "Sennheiser", "Bang & Olufsen",
        "Sonos", "Anker", "Belkin", "TP-Link", "Netgear", "Cisco", "Intel",
        "AMD", "Nvidia", "Qualcomm", "Bosch", "Siemens", "Schneider Electric",
        "ABB", "Tesla", "Polestar", "Renault", "Peugeot", "Volkswagen", "BMW",
        "Audi", "Mercedes-Benz", "SAP", "Salesforce", "Oracle", "Adobe",
        "Autodesk", "Spotify", "Shopify", "Stripe", "Klarna", "Revolut",
        "N26", "Wise", "Booking", "Skyscanner", "TomTom", "Dyson", "Withings",
        "Nothing", "Ring", "Nest", "Roborock", "Ecovacs", "Polar", "Suunto",
        "Roku", "Plantronics", "SteelSeries", "Corsair", "MSI", "Gigabyte",
        "Crucial", "Western Digital", "Seagate", "Kingston", "SanDisk",
        "EVGA", "Noctua", "Thermaltake", "Cooler Master", "Fractal Design",
    ],
    "25": [
        "Nike", "Adidas", "Puma", "Zara", "H&M", "Mango", "Lacoste",
        "Hugo Boss", "Tommy Hilfiger", "Calvin Klein", "Levi's", "Diesel",
        "Gucci", "Prada", "Burberry", "Versace", "Dolce & Gabbana", "Armani",
        "Fendi", "Valentino", "Saint Laurent", "Chanel", "Hermès", "Loewe",
        "Balenciaga", "Bottega Veneta", "Givenchy", "Kenzo", "Stone Island",
        "Moncler", "Canada Goose", "The North Face", "Patagonia", "Columbia",
        "Salomon", "Arc'teryx", "Mammut", "Jack Wolfskin", "Helly Hansen",
        "Reebok", "New Balance", "ASICS", "Mizuno", "Under Armour",
        "Champion", "Fila", "Kappa", "Umbro", "Lotto", "Diadora",
        "Vans", "Converse", "Timberland", "Dr. Martens", "Birkenstock",
        "Crocs", "ECCO", "Geox", "Camper", "Pikolinos", "Massimo Dutti",
        "Pull&Bear", "Bershka", "Stradivarius", "Oysho", "Desigual",
        "Bimba y Lola", "Custo Barcelona", "Adolfo Domínguez", "Scalpers",
        "Carolina Herrera", "Manolo Blahnik", "Pronovias", "Cortefiel",
        "Springfield", "Suit Supply", "Brunello Cucinelli", "Loro Piana",
        "Tod's", "Salvatore Ferragamo", "Bally", "A.P.C.", "Acne Studios",
        "COS", "Arket", "& Other Stories", "Weekday", "Monki",
    ],
    "35": [
        "Amazon", "eBay", "Alibaba", "Walmart", "Carrefour", "Tesco",
        "Lidl", "Aldi", "Mercadona", "Eroski", "DIA", "Auchan", "Casino",
        "IKEA", "Leroy Merlin", "Decathlon", "Fnac", "MediaMarkt",
        "Saturn", "El Corte Inglés", "Galeries Lafayette", "Harrods",
        "Selfridges", "John Lewis", "Marks & Spencer", "Primark", "Costco",
        "Target", "Macy's", "Nordstrom", "TJ Maxx",
        "McKinsey", "BCG", "Bain", "Deloitte", "PwC", "KPMG", "EY",
        "Accenture", "Capgemini", "Atos", "Indra", "NTT Data", "Cognizant",
        "Infosys", "TCS", "Wipro", "HCL",
        "Glovo", "Cabify", "Bolt", "Free Now", "Uber",
        "Wallapop", "Vinted", "Idealista", "Fotocasa",
        "Just Eat", "Deliveroo", "Uber Eats", "Wolt", "DoorDash",
        "Booking.com", "Expedia", "Airbnb", "Vrbo", "Trivago", "Kayak",
        "eDreams", "Kiwi.com", "Hotels.com", "Trip.com", "Agoda",
        "Etsy", "ASOS", "Zalando", "Boohoo", "Shein", "Temu",
        "Veepee", "Privalia", "AliExpress", "JD.com", "Rakuten", "Mercado Libre",
    ],
    "41": [
        "Netflix", "Disney+", "HBO Max", "Amazon Prime Video", "Apple TV+",
        "Paramount+", "Peacock", "Hulu", "Spotify", "Apple Music",
        "YouTube Music", "Tidal", "Deezer", "SoundCloud",
        "Audible", "Storytel", "Scribd",
        "YouTube", "TikTok", "Twitch", "Vimeo", "Patreon", "Substack",
        "Coursera", "Udemy", "edX", "Khan Academy", "Skillshare",
        "MasterClass", "Pluralsight", "DataCamp", "Codecademy",
        "Duolingo", "Babbel", "Busuu", "Rosetta Stone", "Berlitz",
        "Cambridge English", "British Council", "Goethe-Institut", "Cervantes",
        "Alliance Française", "IE Business School", "ESADE", "IESE",
        "London Business School", "INSEAD", "HEC Paris", "Bocconi",
        "Real Madrid", "FC Barcelona", "Atlético Madrid", "Sevilla FC",
        "Valencia CF", "Athletic Bilbao", "Real Sociedad", "Real Betis",
        "Manchester United", "Manchester City", "Liverpool", "Arsenal",
        "Chelsea", "Tottenham", "Bayern Munich", "Borussia Dortmund",
        "Juventus", "AC Milan", "Inter Milan", "Roma", "Napoli",
        "Paris Saint-Germain", "UEFA", "FIFA", "Formula 1", "MotoGP",
        "NBA", "NFL", "Premier League", "La Liga",
        "Cinemark", "AMC Theatres", "Cineworld", "Pathé", "UCI Cinemas",
    ],
}

# === FAMOUS TAGLINES (modeled on real EU trademark filings) ===================
TAGLINES = {
    "Nike":         ["JUST DO IT", "AIR MAX", "FLYKNIT"],
    "Apple":        ["THINK DIFFERENT", "SHOT ON IPHONE"],
    "Adidas":       ["IMPOSSIBLE IS NOTHING", "ALL DAY I DREAM ABOUT SPORT"],
    "BMW":          ["THE ULTIMATE DRIVING MACHINE", "SHEER DRIVING PLEASURE"],
    "Disney+":      ["THE STORIES YOU LOVE"],
    "Spotify":      ["MUSIC FOR EVERYONE"],
    "Microsoft":    ["EMPOWER EVERY PERSON"],
    "Booking.com":  ["BOOKING.YEAH"],
    "Audi":         ["VORSPRUNG DURCH TECHNIK"],
    "Volkswagen":   ["DAS AUTO"],
    "Mercedes-Benz":["THE BEST OR NOTHING"],
    "Tesla":        ["ACCELERATING THE WORLD"],
}

# === VARIANT SUFFIXES BY NICE CLASS ===========================================
SUFFIXES = {
    "9":  ["PRO", "AIR", "MAX", "MINI", "ULTRA", "LITE", "STUDIO", "ONE",
           "PLUS", "GO", "ELITE", "SE", "X", "NEO", "EDGE", "CLOUD"],
    "25": ["ORIGINAL", "CLASSIC", "SPORT", "ATHLETIC", "PERFORMANCE",
           "ESSENTIALS", "HERITAGE", "PRO", "RUN", "TRAIL", "STUDIO",
           "ICON", "FLEX"],
    "35": ["PRIME", "EXPRESS", "PREMIUM", "SELECT", "DIRECT", "MARKETPLACE",
           "BUSINESS", "PARTNER", "REWARDS", "GOLD", "PLATINUM"],
    "41": ["PLUS", "ORIGINALS", "STUDIOS", "LIVE", "PREMIUM", "FAMILY",
           "KIDS", "GO", "NOW", "LITE", "EDU", "ACADEMY"],
}

# === GOODS & SERVICES TEMPLATES (Nice classification verbiage) ===============
# Templates exist for every class that can appear via cross_classes() below.
GOODS = {
    "9": [
        "Computer software for {topic}; downloadable mobile applications for {topic}; cloud-based platforms for {topic}.",
        "Smartphones; tablet computers; wearable devices; chargers; protective cases for portable electronic devices.",
        "Audio equipment, namely headphones, earphones, loudspeakers, soundbars, and home theatre systems.",
        "Computer hardware; integrated circuits; semiconductors; servers; networking equipment.",
        "Smart home devices, namely thermostats, security cameras, doorbells, lighting controls, and connected appliances.",
        "Virtual reality and augmented reality headsets; gaming controllers; eSports equipment.",
        "Electronic publications, downloadable; digital music files; streaming software for audio and video content.",
        "GPS navigation devices; fitness trackers; heart rate monitors; sports performance measurement apparatus.",
        "Batteries; battery chargers; power banks; charging cables and adapters for electronic devices.",
        "Optical apparatus; cameras; lenses; tripods; photography accessories.",
    ],
    "16": [
        "Printed matter; books; magazines; brochures; catalogs; posters; stationery.",
        "Paper and cardboard packaging materials; gift wrap; paper bags.",
        "Pens, pencils, markers; office supplies; writing instruments.",
    ],
    "18": [
        "Leather goods, namely handbags, wallets, briefcases, and luggage.",
        "Backpacks; travel bags; sports bags; duffel bags; tote bags.",
        "Umbrellas; walking sticks; trunks and travelling bags.",
    ],
    "25": [
        "Footwear, namely athletic shoes, running shoes, training shoes, hiking boots, and casual sneakers.",
        "Clothing, namely t-shirts, sweatshirts, hoodies, jackets, trousers, leggings, and shorts.",
        "Headwear, including caps, beanies, hats, and visors; scarves; gloves; socks.",
        "Apparel for sports, namely jerseys, kits, training tops, compression garments, and performance fabrics.",
        "Outerwear, namely waterproof jackets, parkas, technical shells, insulated coats, and base layers.",
        "Footwear for women, men, and children; leather shoes; boots; sandals; slippers.",
        "Underwear; sleepwear; loungewear; swimwear; beachwear.",
        "Belts; ties; bandanas; fashion accessories made of textile and leather; suspenders.",
        "Children's clothing; baby clothing; school uniforms; nursery garments.",
        "Formal wear; suits; dresses; evening gowns; bridal wear.",
    ],
    "28": [
        "Sporting goods, namely balls, rackets, fitness equipment, and exercise machines.",
        "Toys; games; playthings; collectible figurines; board games and card games.",
        "Athletic equipment for football, basketball, tennis, golf, and cycling.",
    ],
    "35": [
        "Online retail store services featuring {topic}; e-commerce platform services; marketplace services connecting buyers and sellers.",
        "Advertising; marketing services; promotion of goods and services through online media; social media advertising services.",
        "Business management consultancy; strategic business consulting; operational efficiency consulting.",
        "Customer loyalty program administration; reward program services; membership program services.",
        "Retail store services in the field of {topic}; mail order catalog services; subscription-based retail services.",
        "Procurement services for others; supply chain management services; sourcing services.",
        "Market research and analysis; consumer behavior research; data analytics services for business decision-making.",
        "Recruitment and staffing services; HR consultancy; talent acquisition services.",
        "Auctioneering services; online auction services; bidding platform services.",
        "Wholesale services in the field of {topic}; bulk distribution services; B2B trading services.",
    ],
    "36": [
        "Financial services; banking; payment processing; mobile payment services.",
        "Insurance services; underwriting; claims administration.",
        "Real estate services; property management; rental of office space.",
    ],
    "38": [
        "Telecommunications services; mobile telephony; broadband internet services.",
        "Streaming of audio, video, and data over telecommunications networks.",
        "Provision of access to electronic databases via the internet.",
    ],
    "39": [
        "Transport services; logistics; freight forwarding; courier delivery.",
        "Travel arrangement; tour operator services; arranging of cruises.",
        "Storage and warehousing of goods; vehicle rental; parking services.",
    ],
    "41": [
        "Streaming of video and audio content via the internet; on-demand entertainment services; subscription video-on-demand services.",
        "Production and distribution of motion pictures, television programs, and original series.",
        "Online education services; e-learning courses; certification programs in {topic}.",
        "Organization of sporting events; live sports broadcasting; sports league administration.",
        "Music streaming services; provision of audio recordings; podcast distribution services.",
        "Live performance services; concert organization; theatre production services.",
        "Publication of electronic books, magazines, and journals; digital library services.",
        "Video game distribution; online gaming services; eSports tournament organization.",
        "Conference, seminar, and workshop organization in the field of {topic}.",
        "Provision of fitness and wellness training; online coaching; personal training services.",
    ],
    "42": [
        "Software as a service (SaaS); platform as a service (PaaS); cloud computing.",
        "Design and development of computer software; IT consulting; custom software engineering.",
        "Hosting websites and web applications; data security services; cybersecurity consulting.",
    ],
    "45": [
        "Legal services; intellectual property consultation; trademark filing services.",
        "Security services; private investigation; surveillance services.",
        "Online social networking services; introduction services.",
    ],
}

# === TOPIC POOLS for {topic}-bearing templates ===============================
TOPICS = {
    "9":  ["productivity", "communication", "creative content", "data analytics",
           "cybersecurity", "artificial intelligence", "developer tools",
           "consumer electronics", "automotive systems", "smart home automation"],
    "25": ["athletic performance", "casual wear", "outdoor activities",
           "luxury fashion", "streetwear", "running"],
    "35": ["consumer electronics", "fashion and apparel", "home goods",
           "groceries", "beauty products", "sporting goods", "books and media",
           "travel services", "financial products", "automotive parts"],
    "41": ["software development", "data science", "language learning",
           "business administration", "creative writing", "music production",
           "fitness and wellness", "personal finance", "digital marketing"],
}

# === REALISTIC OWNERS =========================================================
# Specific brand → real owner mappings. Brands not listed get a random fallback.
BRAND_OWNERS = {
    "Apple": "Apple Inc.", "Samsung": "Samsung Electronics Co. Ltd.",
    "Sony": "Sony Group Corporation", "Microsoft": "Microsoft Corporation",
    "Nintendo": "Nintendo Co. Ltd.", "Bose": "Bose Corporation",
    "Dell": "Dell Inc.", "HP": "HP Inc.", "Lenovo": "Lenovo Group Limited",
    "ASUS": "ASUSTeK Computer Inc.", "Logitech": "Logitech International S.A.",
    "Garmin": "Garmin Ltd.", "Fitbit": "Fitbit LLC", "GoPro": "GoPro Inc.",
    "DJI": "SZ DJI Technology Co. Ltd.", "Nokia": "Nokia Corporation",
    "Xiaomi": "Xiaomi Communications Co. Ltd.", "Huawei": "Huawei Technologies Co. Ltd.",
    "Philips": "Koninklijke Philips N.V.", "LG": "LG Electronics Inc.",
    "Panasonic": "Panasonic Holdings Corporation", "Bosch": "Robert Bosch GmbH",
    "Siemens": "Siemens AG", "Tesla": "Tesla Inc.", "BMW": "BMW AG",
    "Audi": "AUDI AG", "Mercedes-Benz": "Mercedes-Benz Group AG",
    "Volkswagen": "Volkswagen AG", "Renault": "Renault S.A.S.",
    "Peugeot": "Automobiles Peugeot S.A.", "SAP": "SAP SE",
    "Salesforce": "Salesforce Inc.", "Oracle": "Oracle Corporation",
    "Adobe": "Adobe Inc.", "Spotify": "Spotify Technology S.A.",
    "Shopify": "Shopify Inc.", "Stripe": "Stripe Payments Europe Ltd.",
    "Klarna": "Klarna Bank AB", "Revolut": "Revolut Ltd.",

    "Nike": "Nike Inc.", "Adidas": "Adidas AG", "Puma": "Puma SE",
    "Zara": "Industria de Diseño Textil S.A.", "H&M": "H & M Hennes & Mauritz AB",
    "Mango": "Punto Fa S.L.", "Lacoste": "Lacoste S.A.S.",
    "Hugo Boss": "Hugo Boss AG", "Tommy Hilfiger": "Tommy Hilfiger Licensing LLC",
    "Calvin Klein": "Calvin Klein Trademark Trust", "Levi's": "Levi Strauss & Co.",
    "Diesel": "Diesel S.p.A.", "Gucci": "Guccio Gucci S.p.A.",
    "Prada": "Prada S.A.", "Burberry": "Burberry Limited",
    "Versace": "Gianni Versace S.r.l.", "Armani": "Giorgio Armani S.p.A.",
    "Hermès": "Hermès International", "Chanel": "Chanel SARL",
    "Balenciaga": "Balenciaga S.A.", "Reebok": "Reebok International Limited",
    "New Balance": "New Balance Athletics Inc.", "ASICS": "ASICS Corporation",
    "Under Armour": "Under Armour Inc.", "The North Face": "The North Face Apparel Corp.",
    "Patagonia": "Patagonia Inc.", "Vans": "VF Outdoor LLC",
    "Converse": "Converse Inc.", "Dr. Martens": "Dr. Martens AirWair Limited",
    "Massimo Dutti": "Industria de Diseño Textil S.A.",
    "Pull&Bear": "Industria de Diseño Textil S.A.",
    "Bershka": "Industria de Diseño Textil S.A.",
    "Stradivarius": "Industria de Diseño Textil S.A.",

    "Amazon": "Amazon Europe Core S.à r.l.", "eBay": "eBay Inc.",
    "Alibaba": "Alibaba Group Holding Limited", "Carrefour": "Carrefour S.A.",
    "Tesco": "Tesco PLC", "Lidl": "Lidl Stiftung & Co. KG", "Aldi": "Aldi GmbH & Co. KG",
    "Mercadona": "Mercadona S.A.", "IKEA": "Inter IKEA Systems B.V.",
    "Decathlon": "Decathlon S.A.S.", "El Corte Inglés": "El Corte Inglés S.A.",
    "Primark": "Primark Holdings", "Marks & Spencer": "Marks and Spencer plc",
    "McKinsey": "McKinsey & Company Inc.", "Deloitte": "Deloitte Touche Tohmatsu Limited",
    "PwC": "PricewaterhouseCoopers International Limited", "KPMG": "KPMG International Limited",
    "EY": "Ernst & Young Global Limited", "Accenture": "Accenture Global Services Limited",
    "Capgemini": "Capgemini SE", "Glovo": "Glovoapp23 S.L.",
    "Cabify": "Maxi Mobility Spain S.L.", "Bolt": "Bolt Operations OÜ",
    "Uber": "Uber Technologies Inc.", "Wallapop": "Wallapop S.L.",
    "Vinted": "Vinted UAB", "Idealista": "Idealista S.A.",
    "Just Eat": "Just Eat Holding Limited", "Deliveroo": "Roofoods Limited",
    "Booking.com": "Booking.com B.V.", "Expedia": "Expedia Group Inc.",
    "Airbnb": "Airbnb Ireland UC", "Etsy": "Etsy Inc.",
    "ASOS": "ASOS PLC", "Zalando": "Zalando SE",

    "Netflix": "Netflix International B.V.", "Disney+": "Disney Enterprises Inc.",
    "HBO Max": "Home Box Office Inc.", "Apple TV+": "Apple Inc.",
    "Spotify": "Spotify Technology S.A.", "Apple Music": "Apple Inc.",
    "YouTube": "Google LLC", "TikTok": "TikTok Information Technologies UK Limited",
    "Twitch": "Twitch Interactive Inc.", "Audible": "Audible Inc.",
    "Coursera": "Coursera Inc.", "Udemy": "Udemy Inc.",
    "Duolingo": "Duolingo Inc.", "Babbel": "Lesson Nine GmbH",
    "Cambridge English": "University of Cambridge",
    "British Council": "The British Council",
    "Goethe-Institut": "Goethe-Institut e.V.",
    "Cervantes": "Instituto Cervantes",
    "IE Business School": "IE University", "ESADE": "Fundación ESADE",
    "IESE": "IESE Business School",
    "Real Madrid": "Real Madrid Club de Fútbol",
    "FC Barcelona": "Futbol Club Barcelona",
    "Atlético Madrid": "Club Atlético de Madrid S.A.D.",
    "Manchester United": "Manchester United Football Club Limited",
    "Liverpool": "The Liverpool Football Club and Athletic Grounds Limited",
    "Bayern Munich": "FC Bayern München AG",
    "Juventus": "Juventus Football Club S.p.A.",
    "AC Milan": "AC Milan S.p.A.",
    "Paris Saint-Germain": "Paris Saint-Germain Football",
    "UEFA": "Union des Associations Européennes de Football",
    "FIFA": "Fédération Internationale de Football Association",
    "Formula 1": "Formula One Licensing B.V.",
}

# Generic owner pool used when a brand isn't in BRAND_OWNERS.
GENERIC_OWNERS = [
    "Telefónica S.A.", "Banco Santander S.A.", "BBVA S.A.",
    "Iberia Líneas Aéreas S.A.", "Repsol S.A.", "Iberdrola S.A.",
    "ACS Actividades de Construcción S.A.", "Ferrovial S.A.",
    "LVMH Moët Hennessy Louis Vuitton SE", "Kering S.A.",
    "Stellantis N.V.", "Heineken N.V.", "Anheuser-Busch InBev SA/NV",
    "Pernod Ricard S.A.", "Nestlé S.A.", "Unilever PLC", "L'Oréal S.A.",
    "Henkel AG & Co. KGaA",
]

# === CROSS-CLASS RELATIONSHIPS ================================================
# A primary class often appears alongside these related classes in real filings.
RELATED_CLASSES = {
    "9":  ["9", "35", "38", "42", "45"],
    "25": ["25", "18", "28", "35"],
    "35": ["35", "36", "38", "39", "41", "42"],
    "41": ["41", "9", "16", "38", "42"],
}

OUT_PATH = OUT  # alias for clarity in main

# === HELPERS ==================================================================
def random_date(start_year: int = 2018, end_year: int = 2025) -> str:
    start = date(start_year, 1, 1)
    end = date(end_year, 12, 31)
    return (start + timedelta(days=random.randint(0, (end - start).days))).isoformat()

def make_goods(primary_class: str) -> str:
    """Pick a Nice-class-appropriate goods/services template, filling {topic} if present."""
    templates = GOODS.get(primary_class, [
        f"Various goods and services in international class {primary_class}."
    ])
    template = random.choice(templates)
    if "{topic}" in template:
        topics = TOPICS.get(primary_class, ["various fields"])
        return template.format(topic=random.choice(topics))
    return template

def cross_classes(primary: str) -> list:
    """Realistic class spread — owners typically file across multiple Nice classes."""
    base = RELATED_CLASSES[primary]
    n_extra = random.randint(0, min(3, len(base) - 1))
    extras = random.sample([c for c in base if c != primary], k=n_extra)
    return sorted(set([primary] + extras))

def variants_for(brand: str, primary_class: str):
    """Yield 5-15 mark-name variants per brand, mirroring real portfolios."""
    seen = set()
    def add(v):
        if v not in seen:
            seen.add(v)
            return v
        return None

    # 1. Base mark — always present
    if (b := add(brand)): yield b
    # 2. Famous taglines for marquee brands
    for tag in TAGLINES.get(brand, []):
        if (b := add(tag)): yield b
    # 3. Sub-brand suffixes (6-12 of them, sampled from the class pool)
    pool = SUFFIXES[primary_class]
    n = random.randint(6, 12)
    for suffix in random.sample(pool, k=min(n, len(pool))):
        if (b := add(f"{brand} {suffix}")): yield b
    # 4. Stylized variants (uppercase / lowercase) — sometimes
    if random.random() < 0.25:
        if (b := add(brand.upper())): yield b
    if random.random() < 0.15:
        if (b := add(brand.lower())): yield b
    # 5. Anniversary marks — occasional
    if random.random() < 0.10:
        year = random.choice([25, 50, 75, 100])
        if (b := add(f"{brand} {year}")): yield b

def make_record(mark: str, primary_class: str, owner: str, idx: int) -> dict:
    classes = cross_classes(primary_class)
    application_date = date.fromisoformat(random_date())
    status = random.choices(
        ["Registered", "Pending", "Refused", "Withdrawn", "Expired"],
        weights=[70, 15, 8, 5, 2],
    )[0]
    # Registration always follows application — typically 4-18 months later.
    registration_date = None
    if status in ("Registered", "Expired"):
        registration_date = (
            application_date + timedelta(days=random.randint(120, 540))
        ).isoformat()
    return {
        "id": f"EM-{1000000 + idx:07d}",
        "office": "EM",
        "markName": mark,
        "markType": random.choices(
            ["WORD", "FIGURATIVE", "COMBINED", "3D", "SOUND"],
            weights=[60, 20, 18, 1, 1],
        )[0],
        "applicant": owner,
        "applicationDate": application_date.isoformat(),
        "registrationDate": registration_date,
        "status": status,
        "niceClasses": classes,
        "goodsAndServices": " ".join(make_goods(c) for c in classes),
    }

def main():
    written = 0
    seen = set()
    idx = 0
    with OUT_PATH.open("w", encoding="utf-8") as f:
        for nice_class, brands in BRANDS.items():
            for brand in brands:
                # Stable owner per brand — real owner if known, else random fallback
                owner = BRAND_OWNERS.get(brand) or random.choice(GENERIC_OWNERS)
                for variant in variants_for(brand, nice_class):
                    key = (variant, nice_class)
                    if key in seen:
                        continue
                    seen.add(key)
                    record = make_record(variant, nice_class, owner, idx)
                    f.write(json.dumps(record, ensure_ascii=False) + "\n")
                    written += 1
                    idx += 1
    print(f"Done. {written} records → {OUT_PATH}")

if __name__ == "__main__":
    main()
