#!/usr/bin/env python3
"""Builds the static pages for R.B Electricals & Enterprises.

Edit the BUSINESS / SERVICES / CLIENTS data below, then run:
    python3 tools/build.py
The HTML pages are written to the repository root.
"""
import json, os, html, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.environ.get("SITE_URL", "https://rb-electricals-and-enterprises.vercel.app").rstrip("/")

BUSINESS = {
    "name": "R.B Electricals & Enterprises",
    "short": "RB Enterprises",
    "tag": "Govt. Certified Class - 1 Licensed Electrical Contractor",
    "license": "57/8",
    "kno": "492492",
    "street": "No 57/8, K No 492492, Ropena Agrahara",
    "locality": "Ropena Agrahara",
    "city": "Bengaluru",
    "region": "Karnataka",
    "pin": "560068",
    "phones": ["8970772028", "9494514228", "9535688541"],
    "email": "rb.electricalsandenterprises@gmail.com",
    "gstin": "29ASLPV0247P1ZU",
    "pan": "ASLPV0247P",
    "wa": "918970772028",
}
B = BUSINESS
MAP_Q = "Ropena Agrahara, Bengaluru, Karnataka 560068"

def fmt_phone(p):
    return f"+91 {p[:5]} {p[5:]}"

# ---------------------------------------------------------------- icons
P = {
 "building": '<rect x="4" y="2" width="16" height="20" rx="1.5"/><path d="M9 22v-4h6v4M8 6h.01M12 6h.01M16 6h.01M8 10h.01M12 10h.01M16 10h.01M8 14h.01M12 14h.01M16 14h.01"/>',
 "briefcase": '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2M2 13h20M10 13v2h4v-2"/>',
 "home": '<path d="M3 10.5 12 3l9 7.5"/><path d="M5 9v12h14V9"/><path d="M10 21v-6h4v6"/>',
 "cog": '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09a1.65 1.65 0 0 0-1.08-1.51 1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 1 1 0-4h.09a1.65 1.65 0 0 0 1.51-1.08 1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 1 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>',
 "sofa": '<path d="M20 9V7a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v2"/><path d="M2 16a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-5a2 2 0 0 0-4 0v1.5H6V11a2 2 0 0 0-4 0z"/><path d="M4 18v2M20 18v2"/>',
 "bricks": '<rect x="2" y="4" width="20" height="16" rx="1.5"/><path d="M2 9.5h20M2 14.5h20M8 4v5.5M16 4v5.5M12 9.5v5M6 14.5V20M18 14.5V20"/>',
 "ceiling": '<path d="M2 4h20M4 4v3h16V4"/><path d="M12 7v4"/><path d="M8 15a4 4 0 0 1 8 0z"/><path d="M10 18h4M6 11l-2 2M18 11l2 2"/>',
 "zap": '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
 "bulb": '<path d="M9 18h6M10 22h4"/><path d="M12 2a7 7 0 0 0-4 12.74V17h8v-2.26A7 7 0 0 0 12 2z"/>',
 "cctv": '<path d="M4 6.5 16.5 3 19 9.5 6.5 13z"/><path d="m16 11 3 6M6.5 13 7 17H3M3 14v6"/><path d="M19.5 17a2.5 2.5 0 1 0 0-.01"/>',
 "wifi": '<path d="M5 12.55a11 11 0 0 1 14 0M1.42 9a16 16 0 0 1 21.16 0M8.53 16.11a6 6 0 0 1 6.95 0M12 20h.01"/>',
 "battery": '<rect x="2" y="7" width="17" height="10" rx="2"/><path d="M22 11v2M11 9l-2 3h4l-2 3"/>',
 "roller": '<rect x="3" y="3" width="15" height="6" rx="1.5"/><path d="M18 6h2a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1h-8v3"/><rect x="10" y="14" width="4" height="7" rx="1"/>',
 "hardhat": '<path d="M2 18h20v-2a10 10 0 0 0-20 0z"/><path d="M10 6v5M14 6v5M8 6.5A7 7 0 0 1 16 6.5"/><path d="M4 18v2h16v-2"/>',
 "check": '<circle cx="12" cy="12" r="10"/><path d="m8 12.5 2.5 2.5L16 9.5"/>',
 "shield": '<path d="M12 2 4 5v6c0 5 3.4 9.4 8 11 4.6-1.6 8-6 8-11V5z"/><path d="m8.5 12 2.5 2.5 4.5-5"/>',
 "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
 "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
 "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.8 19.8 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>',
 "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 6-10 7L2 6"/>',
 "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>',
 "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
 "menu": '<path d="M3 6h18M3 12h18M3 18h18"/>',
 "x": '<path d="M18 6 6 18M6 6l12 12"/>',
 "award": '<circle cx="12" cy="8" r="6"/><path d="M8.2 13.2 7 22l5-3 5 3-1.2-8.8"/>',
 "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>',
 "target": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
 "handshake": '<path d="m11 17 2 2a1 1 0 1 0 3-3"/><path d="m14 14 2.5 2.5a1 1 0 1 0 3-3l-3.88-3.88a3 3 0 0 0-4.24 0l-.88.88a1 1 0 1 1-3-3l2.81-2.81a5.79 5.79 0 0 1 7.06-.87l.47.28a2 2 0 0 0 1.42.25L21 4"/><path d="m21 3 1 11h-2M3 3 2 14l6.5 6.5a1 1 0 1 0 3-3M3 4h8"/>',
 "map": '<path d="M9 3 3 6v15l6-3 6 3 6-3V3l-6 3z"/><path d="M9 3v15M15 6v15"/>',
 "fb": '<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>',
 "ig": '<rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><path d="M17.5 6.5h.01"/>',
 "in": '<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-4 0v7h-4v-7a6 6 0 0 1 6-6zM2 9h4v12H2z"/><circle cx="4" cy="4" r="2"/>',
}
WA_SVG = '<svg class="icon" viewBox="0 0 24 24" style="fill:currentColor;stroke:none" aria-hidden="true"><path d="M17.47 14.38c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.17-.17.2-.35.22-.65.07-.3-.15-1.26-.46-2.4-1.48-.89-.79-1.49-1.77-1.66-2.07-.17-.3-.02-.46.13-.61.13-.13.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.02-.52-.08-.15-.67-1.62-.92-2.22-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.8.37-.27.3-1.04 1.02-1.04 2.48 0 1.46 1.07 2.88 1.21 3.08.15.2 2.1 3.2 5.08 4.49.71.31 1.26.49 1.7.63.71.23 1.36.2 1.87.12.57-.09 1.76-.72 2-1.41.25-.7.25-1.29.17-1.41-.07-.13-.27-.2-.57-.35zM12.04 21.5h-.01a9.45 9.45 0 0 1-4.82-1.32l-.35-.2-3.58.94.96-3.49-.23-.36a9.43 9.43 0 0 1-1.45-5.03c0-5.22 4.25-9.47 9.48-9.47a9.4 9.4 0 0 1 6.7 2.78 9.4 9.4 0 0 1 2.77 6.7c0 5.22-4.25 9.46-9.47 9.46zm8.06-17.52A11.32 11.32 0 0 0 12.04.64C5.76.64.65 5.75.65 12.03c0 2 .52 3.96 1.52 5.69L.55 23.6l6.02-1.58a11.36 11.36 0 0 0 5.46 1.39h.01c6.28 0 11.39-5.11 11.39-11.39 0-3.04-1.18-5.9-3.33-8.05z"/></svg>'

def ic(name, cls="icon"):
    if name == "wa":
        return WA_SVG
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true">{P[name]}</svg>'

# ---------------------------------------------------------------- content
SERVICES = [
 ("interior-fit-out", "Interior Fit-Out & Furnishing", "sofa",
  "Complete office and home interiors, from workstations and cabins to reception, pantry and furniture.",
  "We design and execute functional, good-looking interiors for offices, commercial spaces and homes, handling layout, joinery, furniture and soft furnishing under one roof.",
  ["Workstations & cabins", "Reception & lounges", "Modular furniture", "Pantry & cafeteria", "Soft furnishing"]),
 ("civil-partition", "Civil & Partition Works", "bricks",
  "Masonry, flooring and partitions in gypsum, glass and board to shape every space.",
  "Our civil team handles the structural side of a fit-out: block work, plastering, flooring, tiling and dry partitions built for clean finishes and fast timelines.",
  ["Gypsum & board partitions", "Glass partitions", "Block work & plastering", "Flooring & tiling", "Demolition & alterations"]),
 ("false-ceiling-pop", "False Ceiling & POP", "ceiling",
  "Gypsum, grid and POP ceilings with clean lines and integrated lighting.",
  "We build false ceilings that hide services, improve acoustics and frame lighting, in gypsum, mineral-fibre grid, metal and decorative POP.",
  ["Gypsum ceilings", "Grid / mineral fibre", "POP & cornices", "Cove & feature ceilings", "Acoustic ceilings"]),
 ("electrical-ht-lt", "Electrical Works – HT & LT", "zap",
  "Licensed HT and LT installations, panels, cabling and complete building wiring.",
  "As a Government certified Class-1 licensed contractor, we take on high-tension and low-tension electrical works, from panels and cabling to full internal wiring, with safety and compliance first.",
  ["HT & LT installations", "Panels & distribution boards", "Cabling & cable trays", "Internal wiring", "Earthing & protection"]),
 ("lighting-power", "Lighting & Power Systems", "bulb",
  "Energy-efficient lighting design and reliable power points for every workspace.",
  "We plan and install lighting and power layouts that suit how a space is used, combining efficient LED fittings, feature lighting and well-placed power points.",
  ["LED & panel lighting", "Feature & cove lighting", "Raw & UPS power points", "Floor boxes", "Lighting controls"]),
 ("lan-cctv-wifi", "LAN / CCTV / Wi-Fi", "cctv",
  "Structured cabling, networking, CCTV surveillance and Wi-Fi coverage.",
  "We set up the low-voltage systems modern offices depend on: structured LAN cabling, network racks, CCTV surveillance and dependable Wi-Fi coverage.",
  ["Structured cabling", "Network racks", "CCTV & surveillance", "Wi-Fi access points", "Access control"]),
 ("ups-power-distribution", "UPS & Power Distribution", "battery",
  "UPS systems, power distribution and backup to keep operations running.",
  "We install and integrate UPS systems with dedicated distribution so critical equipment keeps running through power cuts and fluctuations.",
  ["UPS installation", "Dedicated UPS DBs", "Power distribution", "Load balancing", "Backup planning"]),
 ("painting-finishing", "Painting & Finishing", "roller",
  "Interior and exterior painting, textures and premium surface finishes.",
  "Our finishing team delivers the final look: smooth painting, textures, polishing and touch-ups that make a space hand-over ready.",
  ["Interior painting", "Exterior painting", "Texture & feature walls", "Wood polish", "Final touch-ups"]),
 ("turnkey-projects", "Turnkey Project Execution", "hardhat",
  "One team, one contract: design to handover for complete interior and electrical projects.",
  "Hand over the whole job to us. We manage planning, materials, civil, interiors, electrical and finishing as a single point of responsibility, and hand over a ready-to-use space.",
  ["Single point responsibility", "Detailed BOQ", "Project management", "Quality checks", "On-time handover"]),
]

CLIENTS = [
 ("Enyzme", "Office Spaces Pvt Ltd", "Enyzme Office Spaces Pvt Ltd"),
 ("ACKO", "Technology", "Acko Technology Pvt Ltd"),
 ("UV", "Inchnmile Pvt Ltd", "UV (Inchnmile Pvt Ltd)"),
 ("ELLISYS", "India Pvt Ltd", "Ellisys India Pvt Ltd"),
 ("GoPro", "Ventures LLP", "GoPro Ventures LLP"),
 ("chin", "Design", "Chin Design"),
 ("vishwaa", "Apparels", "Vishwaa Apparels"),
 ("WORK", "Square", "Work Square"),
 ("GREAT", "Learning", "Great Learning"),
 ("iEnergizer", "", "iEnergizer"),
]

NAV = [("index.html", "Home"), ("about.html", "About Us"), ("services.html", "Services"),
       ("projects.html", "Projects"), ("projects.html#clients", "Clients"), ("about.html#why-rb", "Why RB"),
       ("contact.html", "Contact")]

# ---------------------------------------------------------------- layout
def head(title, desc, path, extra_ld=None):
    url = f"{SITE}/{'' if path == 'index.html' else path.replace('.html','')}"
    ld = [business_ld()]
    if extra_ld:
        ld.append(extra_ld)
    ld_html = "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    return f"""<!doctype html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="keywords" content="electrical contractor Bengaluru, Class 1 licensed electrical contractor, interior fit-out Bangalore, office interiors Bangalore, turnkey interior contractor, HT LT electrical works, false ceiling, partition works, LAN CCTV Wi-Fi installation, UPS installation, R.B Electricals, RB Enterprises">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow">
<meta name="theme-color" content="#14161a">
<meta name="geo.region" content="IN-KA">
<meta name="geo.placename" content="Bengaluru">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{B['name']}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/img/og-image.jpg">
<meta property="og:locale" content="en_IN">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="/favicon.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Montserrat:wght@600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/style.css">
{ld_html}
</head>
<body>
"""

def business_ld():
    return {
        "@context": "https://schema.org",
        "@type": ["Electrician", "GeneralContractor"],
        "@id": f"{SITE}/#business",
        "name": B["name"],
        "alternateName": ["R.B Electricals and Enterprises", "RB Enterprises", "RB Electricals"],
        "description": "Government certified Class-1 licensed electrical contractor in Bengaluru providing interior fit-out, civil and partition works, false ceiling, HT & LT electrical works, lighting, LAN/CCTV/Wi-Fi, UPS and turnkey project execution.",
        "url": SITE + "/",
        "logo": f"{SITE}/assets/img/logo.png",
        "image": f"{SITE}/assets/img/og-image.jpg",
        "telephone": "+91" + B["phones"][0],
        "email": B["email"],
        "address": {"@type": "PostalAddress", "streetAddress": B["street"], "addressLocality": B["city"],
                    "addressRegion": B["region"], "postalCode": B["pin"], "addressCountry": "IN"},
        "areaServed": {"@type": "City", "name": "Bengaluru"},
        "hasMap": "https://www.google.com/maps/search/?api=1&query=" + MAP_Q.replace(" ", "+"),
        "taxID": B["gstin"],
        "contactPoint": [{"@type": "ContactPoint", "telephone": "+91" + p, "contactType": "customer service",
                          "areaServed": "IN", "availableLanguage": ["English", "Kannada", "Hindi", "Telugu"]} for p in B["phones"]],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s[1], "description": s[3]}} for s in SERVICES]},
    }

def header(active):
    links = []
    for href, label in NAV:
        cls = ' class="active"' if href == active else ""
        links.append(f'<a href="/{href}"{cls}>{label}</a>')
    phones = " / ".join(B["phones"])
    return f"""<a class="sr-only" href="#main">Skip to content</a>
<div class="topbar"><div class="wrap">
  <div class="tb-left"><span class="badge">Govt. Certified Class-1 Licensed Electrical Contractor</span></div>
  <div class="tb-right">
    <a href="tel:+91{B['phones'][0]}">{ic('phone')}{fmt_phone(B['phones'][0])}</a>
    <a href="mailto:{B['email']}">{ic('mail')}{B['email']}</a>
  </div>
</div></div>
<header class="header"><div class="wrap">
  <a class="brand" href="/" aria-label="{B['name']} home">
    <img src="/assets/img/logo.png" alt="RB Enterprises logo" width="62" height="58">
    <div><div class="brand-name">{B['name']}</div><div class="brand-tag">Govt. Certified Class - 1<br>Licensed Electrical Contractor</div></div>
  </a>
  <button class="menu-btn" aria-label="Open menu" aria-expanded="false" aria-controls="nav">{ic('menu','icon i-open')}<span class="i-close" style="display:none">{ic('x')}</span></button>
  <nav class="nav" id="nav" aria-label="Main">
    {''.join(links)}
    <a class="btn btn-primary" href="/contact.html#quote">{ic('phone')}Get a Quote</a>
  </nav>
</div></header>
<main id="main">
"""

def footer():
    svc_links = "".join(f'<li><a href="/services.html#{s[0]}">{s[1]}</a></li>' for s in SERVICES[:6])
    phones = "".join(f'<a href="tel:+91{p}">{fmt_phone(p)}</a><br>' for p in B["phones"])
    return f"""</main>
<footer class="footer">
  <div class="wrap grid">
    <div>
      <div class="f-brand"><img src="/assets/img/logo-mark.png" alt="" width="64" height="53"><div><b>{B['name']}</b><span>Govt. Certified Class - 1 Licensed Electrical Contractor</span></div></div>
      <p>Complete interior, electrical and turnkey solutions for commercial, corporate and residential spaces across Bengaluru.</p>
      <p style="font-size:13px;margin:0">GSTIN: {B['gstin']}</p>
    </div>
    <div>
      <h4>Quick Links</h4>
      <ul><li><a href="/">Home</a></li><li><a href="/about.html">About Us</a></li><li><a href="/services.html">Services</a></li><li><a href="/projects.html">Projects</a></li><li><a href="/projects.html#clients">Clients</a></li><li><a href="/contact.html">Contact Us</a></li></ul>
    </div>
    <div>
      <h4>Our Services</h4>
      <ul>{svc_links}<li><a href="/services.html">All services →</a></li></ul>
    </div>
    <div>
      <h4>Get in Touch</h4>
      <ul class="f-contact">
        <li>{ic('phone')}<span>{phones}</span></li>
        <li>{ic('mail')}<a href="mailto:{B['email']}">{B['email']}</a></li>
        <li>{ic('pin')}<a href="https://www.google.com/maps/search/?api=1&amp;query={MAP_Q.replace(' ','+')}" target="_blank" rel="noopener">{B['street']},<br>{B['city']} - {B['pin']}</a></li>
      </ul>
      <div class="socials">
        <a href="https://wa.me/{B['wa']}" target="_blank" rel="noopener" aria-label="WhatsApp">{ic('wa')}</a>
        <a href="tel:+91{B['phones'][0]}" aria-label="Call">{ic('phone')}</a>
        <a href="mailto:{B['email']}" aria-label="Email">{ic('mail')}</a>
      </div>
    </div>
  </div>
  <div class="wrap f-bottom">
    <span>© <span id="year">2026</span> {B['name']}. All rights reserved.</span>
    <span>Ropena Agrahara, Bengaluru · Karnataka</span>
  </div>
</footer>
<div class="fab">
  <a class="wa" href="https://wa.me/{B['wa']}?text=Hello%20R.B%20Electricals%2C%20I%20would%20like%20to%20enquire%20about%20your%20services." target="_blank" rel="noopener" aria-label="Chat on WhatsApp">{ic('wa')}</a>
  <a class="call" href="tel:+91{B['phones'][0]}" aria-label="Call us">{ic('phone')}</a>
</div>
<div class="lightbox" id="lightbox" hidden><button class="lb-close" aria-label="Close">×</button><button class="lb-prev" aria-label="Previous">‹</button><figure><img alt=""><figcaption></figcaption></figure><button class="lb-next" aria-label="Next">›</button></div>
<div class="progress" aria-hidden="true"></div>
<script src="/assets/js/main.js" defer></script>
</body>
</html>
"""

def page_hero(title, sub, crumb):
    return f"""<section class="page-hero"><div class="wrap">
  <div class="crumbs"><a href="/">Home</a> / {crumb}</div>
  <h1>{title}</h1><p>{sub}</p>
</div></section>"""

def svc_cards(items):
    out = []
    for i, s in enumerate(items, 1):
        out.append(f"""<a class="svc reveal" href="/services.html#{s[0]}"><span class="num">{i:02d}</span>
  <div class="ic">{ic(s[2])}</div><h3>{s[1]}</h3><p>{s[3]}</p></a>""")
    return "\n".join(out)

def client_tiles(items):
    return "\n".join(f'<div class="client reveal" title="{c[2]}"><div><b>{c[0]}</b>{f"<span>{c[1]}</span>" if c[1] else ""}</div></div>' for c in items)

def marquee_items(hidden=False):
    aria = ' aria-hidden="true"' if hidden else ""
    return "".join(f'<div class="mq-item"{aria}><b>{c[0]}</b>{f"<span>{c[1]}</span>" if c[1] else ""}</div>' for c in CLIENTS)

GALLERY_CATS = [("offices", "Offices"), ("electrical", "Electrical"), ("interiors", "Interiors"), ("ceiling", "Ceiling & Civil"), ("networking", "LAN / CCTV")]

def gallery_items():
    """Photos in assets/img/gallery/<category>/*.jpg are shown automatically."""
    items = []
    base = os.path.join(ROOT, "assets", "img", "gallery")
    for slug, label in GALLERY_CATS:
        d = os.path.join(base, slug)
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                cap = os.path.splitext(f)[0].replace("-", " ").replace("_", " ").strip().capitalize()
                items.append((slug, label, f"/assets/img/gallery/{slug}/{f}", cap))
    return items

def gallery_section():
    items = gallery_items()
    if not items:
        return ""
    used = []
    for it in items:
        if it[0] not in used:
            used.append(it[0])
    btns = '<button class="gf on" data-filter="all">All</button>' + "".join(
        f'<button class="gf" data-filter="{s}">{l}</button>' for s, l in GALLERY_CATS if s in used)
    tiles = "".join(f'<a class="g-item reveal" href="{src}" data-cat="{slug}" data-caption="{html.escape(cap)}"><img src="{src}" alt="{html.escape(cap)}" loading="lazy"><span>{label}</span></a>' for slug, label, src, cap in items)
    return f"""<section class="section" id="gallery"><div class="wrap">
  <div class="sec-head center reveal"><div class="eyebrow">Gallery</div><h2>Our Work in Pictures</h2><p>Photos from our completed and ongoing sites.</p></div>
  <div class="g-filters">{btns}</div>
  <div class="gallery">{tiles}</div>
</div></section>"""

def proj_cards(items, status=True):
    out = []
    for c in items:
        slug = c[2].lower().replace(" ", "-").replace("(", "").replace(")", "").replace(".", "")
        img_rel = f"assets/img/projects/{slug}.jpg"
        img = f'<img src="/{img_rel}" alt="{c[2]} project" loading="lazy">' if os.path.exists(os.path.join(ROOT, img_rel)) else ""
        has = " has-img" if img else ""
        mono = "" if img else f'<img class="wm" src="/assets/img/logo-mark.png" alt="" loading="lazy"><div class="mono">{c[0]}<small>{c[1] or "CLIENT"}</small></div>'
        out.append(f"""<article class="proj reveal{has}">
  <div class="cover">{img}{mono}{'<span class="status">Client project</span>' if status else ''}</div>
  <div class="body"><h3>{c[2]}</h3><p><span class="dot"></span>Interior &amp; Electrical Works</p></div>
</article>""")
    return "\n".join(out)

def cta_band():
    return f"""<section class="section tight"><div class="wrap">
  <div class="cta-band reveal">
    <div><h2>Planning an office, store or home project?</h2><p>Share your requirement and get a detailed, transparent quote from our team.</p></div>
    <div class="acts"><a class="btn btn-primary" href="/contact.html#quote">Get a Quote {ic('arrow')}</a><a class="btn btn-wa" href="https://wa.me/{B['wa']}" target="_blank" rel="noopener">{ic('wa')} WhatsApp</a></div>
  </div>
</div></section>"""

def creds_band():
    phones = " / ".join(B["phones"])
    return f"""<section class="section"><div class="wrap">
  <div class="creds reveal">
    <div>
      <h3>Our Credentials</h3>
      <div class="seal">{ic('shield')}<div><strong>Govt. Certified Class - 1 Licensed Electrical Contractor</strong>
        <dl class="kv"><dt>License No.</dt><dd>{B['license']}</dd><dt>K No.</dt><dd>{B['kno']}</dd><dt>Location</dt><dd>{B['locality']}, {B['city']} - {B['pin']}</dd></dl></div></div>
    </div>
    <div>
      <h3>Why Choose RB</h3>
      <ul class="check-list">
        <li>{ic('check')}Single point responsibility for interior &amp; electrical works</li>
        <li>{ic('check')}Experienced &amp; skilled project execution team</li>
        <li>{ic('check')}Quality materials and industry best practices</li>
        <li>{ic('check')}Transparent pricing &amp; detailed BOQ</li>
        <li>{ic('check')}On-time delivery with safe execution</li>
      </ul>
    </div>
    <div>
      <h3>Company Details</h3>
      <dl class="kv">
        <dt>GSTIN</dt><dd>{B['gstin']}</dd>
        <dt>PAN</dt><dd>{B['pan']}</dd>
        <dt>Email</dt><dd><a href="mailto:{B['email']}">{B['email']}</a></dd>
        <dt>Phone</dt><dd>{phones}</dd>
        <dt>Address</dt><dd>{B['locality']}, {B['city']} - {B['pin']}</dd>
      </dl>
    </div>
  </div>
</div></section>"""

# ---------------------------------------------------------------- pages
def page_home():
    pills = [("building", "Commercial<br>Spaces"), ("briefcase", "Corporate<br>Offices"), ("home", "Residential<br>Interiors"), ("cog", "Turnkey<br>Projects")]
    pills_html = "".join(f"<li>{ic(i)}<span>{t}</span></li>" for i, t in pills)
    faq = [
        ("Are you a licensed electrical contractor?", f"Yes. {B['name']} is a Government certified Class-1 licensed electrical contractor (License No. {B['license']}), qualified to carry out HT and LT electrical works."),
        ("Do you handle complete interior projects?", "Yes. We take on turnkey projects covering civil and partition works, false ceilings, electrical, lighting, networking, UPS, painting and furnishing, with a single point of responsibility from start to handover."),
        ("Which areas do you serve?", "We are based in Ropena Agrahara, Bengaluru, and take up commercial, corporate and residential projects across Bengaluru."),
        ("How do I get a quotation?", f"Call or WhatsApp us on {fmt_phone(B['phones'][0])}, email {B['email']}, or fill in the quote form on our Contact page. We share a detailed BOQ so pricing is transparent."),
    ]
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
    faq_html = "".join(f"<details class=\"reveal\"><summary>{q}</summary><p>{a}</p></details>" for q, a in faq)
    body = f"""
<section class="hx">
  <div class="hx-bg" aria-hidden="true"><img src="/assets/img/hero-office.jpg" alt="" width="1000" height="876" fetchpriority="high"></div>
  <svg class="hx-lines" viewBox="0 0 1440 800" preserveAspectRatio="none" aria-hidden="true">
    <path d="M-20 620 H380 L430 570 H760 L800 610 H1460"/><path d="M-20 680 H240 L290 730 H900 L950 680 H1460"/><path d="M1460 160 H1100 L1050 210 H820"/>
  </svg>
  <div class="wrap hx-inner">
    <div class="hx-copy">
      <div class="hx-badge">{ic('shield')}<span>Govt. Certified Class-1 Licensed Electrical Contractor</span></div>
      <h1>Complete Interior, <span class="hl">Electrical</span> &amp; Turnkey Solutions</h1>
      <p class="lead">From concept to completion. We design, build, wire and hand over offices, commercial spaces and homes across Bengaluru, with one team accountable for everything.</p>
      <div class="hero-cta">
        <a class="btn btn-primary btn-lg" href="/contact.html#quote">Get a Free Quote {ic('arrow')}</a>
        <a class="btn btn-ghost btn-lg" href="/projects.html">View Our Projects</a>
      </div>
      <ul class="hero-pills">{pills_html}</ul>
    </div>
    <aside class="hx-card reveal">
      <div class="hx-card-top"><img src="/assets/img/logo-mark.png" alt="" width="54" height="45"><div><b>Why clients choose RB</b><span>Single point responsibility</span></div></div>
      <ul>
        <li>{ic('check')}Licensed HT &amp; LT electrical works</li>
        <li>{ic('check')}Interiors, civil, ceiling &amp; painting under one roof</li>
        <li>{ic('check')}LAN, CCTV, Wi-Fi &amp; UPS integration</li>
        <li>{ic('check')}Transparent BOQ, on-time handover</li>
      </ul>
      <a class="hx-call" href="tel:+91{B['phones'][0]}">{ic('phone')}<span><small>Call us now</small>{fmt_phone(B['phones'][0])}</span></a>
    </aside>
  </div>
  <div class="wrap"><div class="hx-stats">
    <div class="stat"><b><span data-count="10">10</span>+</b><span>Corporate clients</span></div>
    <div class="stat"><b><span data-count="9">9</span></b><span>Services under one roof</span></div>
    <div class="stat"><b>Class-1</b><span>Govt. licensed contractor</span></div>
    <div class="stat"><b><span data-count="1">1</span></b><span>Point of responsibility</span></div>
  </div></div>
</section>

<section class="marquee-band" aria-label="Our clients">
  <div class="wrap"><p class="marquee-label">Trusted by leading companies across Bengaluru</p></div>
  <div class="marquee"><div class="marquee-track">{marquee_items()}{marquee_items(True)}</div></div>
</section>

<section class="section"><div class="wrap split">
  <div class="reveal">
    <div class="eyebrow">About Us</div>
    <h2 style="font-size:clamp(28px,3.4vw,40px)">Delivering Excellence in Every Project</h2>
    <p class="lede">{B['name']} is a Government Certified Class - 1 Licensed Electrical Contractor providing comprehensive solutions in Interiors, Electrical and Turnkey Project Execution for commercial, corporate and residential spaces.</p>
    <p>With a skilled team, quality materials and a commitment to timelines, we transform spaces into functional, aesthetic and efficient environments.</p>
    <div class="trio">
      <div class="item">{ic('award')}<h3>Quality Assured</h3><p>Best materials &amp; workmanship</p></div>
      <div class="item">{ic('users')}<h3>Experienced Team</h3><p>Skilled professionals for every task</p></div>
      <div class="item">{ic('clock')}<h3>On-Time Delivery</h3><p>Committed to deadlines</p></div>
    </div>
    <p style="margin-top:28px"><a class="btn btn-outline" href="/about.html">Know More About Us {ic('arrow')}</a></p>
  </div>
  <div class="media reveal">
    <img src="/assets/img/about-lounge.jpg" alt="Office lounge and breakout area interior" width="900" height="624" loading="lazy">
    <div class="tag"><b>End-to-End</b><span>Design · Build · Power · Handover</span></div>
  </div>
</div></section>

<section class="section bg-cream"><div class="wrap">
  <div class="sec-head center reveal"><div class="eyebrow">Our Services</div><h2>End-to-End Solutions</h2><p>Everything your space needs, delivered by one accountable team.</p></div>
  <div class="services">{svc_cards(SERVICES)}</div>
  <div class="center-cta"><a class="btn btn-primary" href="/services.html">View All Services {ic('arrow')}</a></div>
</div></section>

<section class="section bg-dark"><div class="wrap dual">
  <div>
    <div class="sec-head reveal" style="margin-bottom:32px"><div class="eyebrow">Our Projects</div><h2>Recent Work</h2><p>Interior and electrical works for growing companies across Bengaluru.</p></div>
    <div class="mini-proj">{proj_cards(CLIENTS[:4], status=False)}</div>
    <p style="margin-top:28px"><a class="btn btn-ghost" href="/projects.html">View All Projects {ic('arrow')}</a></p>
  </div>
  <div>
    <div class="sec-head reveal" style="margin-bottom:32px"><div class="eyebrow">Our Clients</div><h2>Trusted by Leading Companies</h2><p>Completed and ongoing projects with these organisations.</p></div>
    <div class="mini-clients">{client_tiles(CLIENTS[:9])}</div>
    <p style="margin-top:28px"><a class="btn btn-primary" href="/projects.html#clients">View All Clients {ic('arrow')}</a></p>
  </div>
</div></section>

{creds_band()}

<section class="section bg-cream"><div class="wrap">
  <div class="sec-head center reveal"><div class="eyebrow">FAQ</div><h2>Common Questions</h2></div>
  <div class="faq">{faq_html}</div>
</div></section>

{cta_band()}
"""
    title = f"{B['name']} | Class-1 Licensed Electrical Contractor & Interior Turnkey Solutions in Bengaluru"
    desc = "Govt. certified Class-1 licensed electrical contractor in Bengaluru. Interior fit-out, civil & partitions, false ceiling, HT & LT electrical, lighting, LAN/CCTV/Wi-Fi, UPS and turnkey projects. Call 8970772028."
    return head(title, desc, "index.html", faq_ld) + header("index.html") + body + footer()

def page_about():
    body = page_hero("About Us", "A licensed electrical contractor and interior partner that takes full responsibility for your space, from concept to completion.", "About Us") + f"""
<section class="section"><div class="wrap split">
  <div class="reveal">
    <div class="eyebrow">Who We Are</div>
    <h2 style="font-size:clamp(28px,3.4vw,40px)">Powering spaces, building trust</h2>
    <p class="lede">{B['name']} is a Government Certified Class - 1 Licensed Electrical Contractor based in Ropena Agrahara, Bengaluru.</p>
    <p>We provide comprehensive solutions in interiors, electrical and turnkey project execution for commercial, corporate and residential spaces. Our clients range from fast-growing technology companies to managed office providers and design studios.</p>
    <p>With a skilled team, quality materials and a firm commitment to timelines, we transform spaces into functional, aesthetic and efficient environments, and we stay accountable for every part of the job.</p>
    <ul class="check-list">
      <li>{ic('check')}Government certified Class-1 electrical licence (No. {B['license']})</li>
      <li>{ic('check')}Interiors, civil, electrical and networking under one roof</li>
      <li>{ic('check')}Registered business — GSTIN {B['gstin']}</li>
    </ul>
  </div>
  <div class="media reveal">
    <img src="/assets/img/hero-office.jpg" alt="Open-plan office with workstations" width="1000" height="876" loading="lazy">
    <div class="tag"><b>Class-1</b><span>Licensed electrical contractor</span></div>
  </div>
</div></section>

<section class="section bg-cream"><div class="wrap">
  <div class="sec-head center reveal"><div class="eyebrow">What Drives Us</div><h2>Our Commitments</h2></div>
  <div class="values">
    <div class="value reveal">{ic('award')}<h3>Quality Assured</h3><p>We use the right materials and proven workmanship, so what we build looks good on day one and keeps working for years.</p></div>
    <div class="value reveal">{ic('shield')}<h3>Safety &amp; Compliance</h3><p>As a licensed Class-1 contractor, every electrical installation follows safety standards and statutory requirements.</p></div>
    <div class="value reveal">{ic('clock')}<h3>On-Time Delivery</h3><p>Planned schedules, coordinated trades and daily supervision keep projects on track for handover.</p></div>
    <div class="value reveal">{ic('file')}<h3>Transparent Pricing</h3><p>Detailed BOQs and clear scope, so you know exactly what you are paying for before work begins.</p></div>
    <div class="value reveal">{ic('users')}<h3>Skilled Team</h3><p>Electricians, carpenters, civil and finishing crews who work together as one coordinated team.</p></div>
    <div class="value reveal">{ic('handshake')}<h3>Single Point of Contact</h3><p>One partner responsible for interiors and electrical works, so nothing falls between contractors.</p></div>
  </div>
</div></section>

<section class="section bg-dark" id="why-rb"><div class="wrap">
  <div class="sec-head center reveal"><div class="eyebrow">How We Work</div><h2>From Concept to Completion</h2><p>A simple, accountable process for every project.</p></div>
  <div class="process">
    <div class="step reveal"><h3>Site Visit &amp; Requirement</h3><p>We visit the site, understand how you will use the space and take accurate measurements.</p></div>
    <div class="step reveal"><h3>Design &amp; BOQ</h3><p>You receive a clear plan with a detailed bill of quantities and transparent pricing.</p></div>
    <div class="step reveal"><h3>Execution</h3><p>Civil, interiors, electrical and networking crews work to one coordinated schedule.</p></div>
    <div class="step reveal"><h3>Testing &amp; Handover</h3><p>Every system is tested and checked for quality before we hand over a ready-to-use space.</p></div>
  </div>
</div></section>

{creds_band()}
{cta_band()}
"""
    return head(f"About Us | {B['name']} – Class-1 Licensed Electrical Contractor, Bengaluru",
                f"Learn about {B['name']}, a Government certified Class-1 licensed electrical contractor in Bengaluru delivering interiors, electrical and turnkey projects.",
                "about.html") + header("about.html") + body + footer()

def page_services():
    rows = []
    for s in SERVICES:
        tags = "".join(f"<li>{t}</li>" for t in s[5])
        rows.append(f"""<article class="svc-row reveal" id="{s[0]}"><div class="ic">{ic(s[2])}</div><div><h3>{s[1]}</h3><p>{s[4]}</p><ul>{tags}</ul></div></article>""")
    svc_ld = {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [
        {"@type": "ListItem", "position": i, "item": {"@type": "Service", "name": s[1], "description": s[4],
         "provider": {"@id": f"{SITE}/#business"}, "areaServed": "Bengaluru"}} for i, s in enumerate(SERVICES, 1)]}
    body = page_hero("Our Services", "Interior, civil, electrical, networking and finishing services, delivered individually or as one complete turnkey project.", "Services") + f"""
<section class="section"><div class="wrap">
  <div class="sec-head center reveal"><div class="eyebrow">End-to-End Solutions</div><h2>What We Do</h2><p>Choose a single service or hand over the complete project to us.</p></div>
  <div class="svc-detail">{''.join(rows)}</div>
</div></section>
<section class="section bg-dark"><div class="wrap">
  <div class="sec-head center reveal"><div class="eyebrow">Spaces We Build</div><h2>For Every Kind of Space</h2></div>
  <div class="process">
    <div class="step reveal"><h3>Commercial Spaces</h3><p>Showrooms, retail and commercial floors fitted out and powered to run.</p></div>
    <div class="step reveal"><h3>Corporate Offices</h3><p>Workstations, cabins, meeting rooms, server rooms and breakout zones.</p></div>
    <div class="step reveal"><h3>Residential Interiors</h3><p>Homes and apartments with safe wiring, lighting and finished interiors.</p></div>
    <div class="step reveal"><h3>Turnkey Projects</h3><p>Complete design-to-handover projects with a single point of responsibility.</p></div>
  </div>
</div></section>
{cta_band()}
"""
    return head(f"Services | Interior Fit-Out, HT & LT Electrical, False Ceiling, LAN/CCTV, UPS – {B['short']} Bengaluru",
                "Interior fit-out & furnishing, civil & partition works, false ceiling & POP, HT & LT electrical works, lighting, LAN/CCTV/Wi-Fi, UPS & power distribution, painting and turnkey projects in Bengaluru.",
                "services.html", svc_ld) + header("services.html") + body + footer()

def page_projects():
    body = page_hero("Projects &amp; Clients", "Interior and electrical works for companies across Bengaluru, with completed and ongoing projects.", "Projects") + f"""
<section class="section bg-dark"><div class="wrap">
  <div class="sec-head reveal"><div class="eyebrow">Our Work</div><h2>Client Projects</h2><p>A selection of organisations we have delivered interior and electrical works for.</p></div>
  <div class="proj-grid">{proj_cards(CLIENTS)}</div>
</div></section>
{gallery_section()}
<section class="section bg-cream" id="clients"><div class="wrap">
  <div class="sec-head center reveal"><div class="eyebrow">Our Clients</div><h2>Trusted by Leading Companies</h2><p>Completed and ongoing projects with these organisations.</p></div>
  <div class="clients">{client_tiles(CLIENTS)}</div>
</div></section>
{cta_band()}
"""
    return head(f"Projects & Clients | {B['name']} Bengaluru",
                "Interior and electrical projects for Acko, Great Learning, Enyzme Office Spaces, Ellisys, Work Square, iEnergizer and more across Bengaluru.",
                "projects.html") + header("projects.html") + body + footer()

def page_contact():
    opts = "".join(f"<option>{s[1]}</option>" for s in SERVICES) + "<option>Other / Not sure</option>"
    phones = "".join(f'<a href="tel:+91{p}">{fmt_phone(p)}</a>' for p in B["phones"])
    mq = MAP_Q.replace(" ", "+")
    body = page_hero("Contact Us", "Tell us about your project. Call, WhatsApp, email or send the form and we will get back to you quickly.", "Contact") + f"""
<section class="section"><div class="wrap contact-grid">
  <div class="cards">
    <div class="ccard reveal"><div class="ic">{ic('phone')}</div><div><h3>Call Us</h3><div class="lines">{phones}</div></div></div>
    <div class="ccard reveal"><div class="ic">{ic('wa')}</div><div><h3>WhatsApp</h3><a href="https://wa.me/{B['wa']}" target="_blank" rel="noopener">Chat on {fmt_phone(B['phones'][0])}</a></div></div>
    <div class="ccard reveal"><div class="ic">{ic('mail')}</div><div><h3>Email</h3><a href="mailto:{B['email']}">{B['email']}</a></div></div>
    <div class="ccard reveal"><div class="ic">{ic('pin')}</div><div><h3>Office Address</h3><p>{B['name']}<br>{B['street']},<br>{B['city']}, {B['region']} - {B['pin']}</p></div></div>
    <div class="ccard reveal"><div class="ic">{ic('file')}</div><div><h3>Company Details</h3><p>GSTIN: {B['gstin']}<br>PAN: {B['pan']}<br>Class-1 Licence No.: {B['license']}</p></div></div>
  </div>
  <form class="form reveal" id="quote-form" novalidate>
    <span id="quote" style="position:relative;top:-120px"></span>
    <h3>Get a Free Quote</h3>
    <p class="note">Fill in your details and send them to us on WhatsApp or by email.</p>
    <div class="fgrid">
      <div class="field"><label for="f-name">Your name *</label><input id="f-name" name="name" required autocomplete="name"></div>
      <div class="field"><label for="f-phone">Phone *</label><input id="f-phone" name="phone" type="tel" required autocomplete="tel" pattern="[0-9+ ]{{10,15}}"></div>
      <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email"></div>
      <div class="field"><label for="f-service">Service needed *</label><select id="f-service" name="service" required>{opts}</select></div>
      <div class="field full"><label for="f-location">Site location</label><input id="f-location" name="location" placeholder="e.g. Koramangala, Bengaluru"></div>
      <div class="field full"><label for="f-message">Project details</label><textarea id="f-message" name="message" placeholder="Type of space, area in sq ft, timeline…"></textarea></div>
    </div>
    <div class="form-acts">
      <button class="btn btn-wa" type="submit">{ic('wa')} Send on WhatsApp</button>
      <button class="btn btn-dark" type="button" id="quote-email">{ic('mail')} Send by Email</button>
    </div>
  </form>
</div></section>
<section class="section tight bg-cream" id="map"><div class="wrap">
  <div class="sec-head center reveal" style="margin-bottom:32px"><div class="eyebrow">Find Us</div><h2>Our Location</h2></div>
  <div class="map reveal">
    <iframe title="Map showing {B['name']} at Ropena Agrahara, Bengaluru" src="https://maps.google.com/maps?q={mq}&amp;z=15&amp;output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
    <div class="map-bar"><div><strong>{B['name']}</strong><span>{B['street']}, {B['city']} - {B['pin']}</span></div>
      <a class="btn btn-primary" href="https://www.google.com/maps/dir/?api=1&amp;destination={mq}" target="_blank" rel="noopener">{ic('map')} Get Directions</a></div>
  </div>
</div></section>
"""
    return head(f"Contact Us | {B['name']} – Ropena Agrahara, Bengaluru",
                f"Contact {B['name']}, Ropena Agrahara, Bengaluru 560068. Call 8970772028 / 9494514228 / 9535688541 or email {B['email']} for a free quote.",
                "contact.html") + header("contact.html") + body + footer()

def page_404():
    body = page_hero("Page not found", "The page you are looking for has moved or does not exist.", "404") + f"""
<section class="section"><div class="wrap" style="text-align:center"><a class="btn btn-primary" href="/">Back to Home {ic('arrow')}</a></div></section>"""
    return head(f"Page not found | {B['name']}", "Page not found.", "404.html").replace('content="index, follow"', 'content="noindex"') + header("") + body + footer()

def clean_links(c):
    c = c.replace('href="/index.html"', 'href="/"')
    return re.sub(r'href="/([a-z0-9-]+)\.html', r'href="/\1', c)

def write(name, content):
    if name.endswith(".html"):
        content = clean_links(content)
    with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
        f.write(content)

def main():
    pages = {"index.html": page_home(), "about.html": page_about(), "services.html": page_services(),
             "projects.html": page_projects(), "contact.html": page_contact(), "404.html": page_404()}
    for n, c in pages.items():
        write(n, c)
    urls = [("", "1.0"), ("about", "0.8"), ("services", "0.9"), ("projects", "0.8"), ("contact", "0.9")]
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
          "".join(f"  <url><loc>{SITE}/{u}</loc><priority>{p}</priority></url>\n" for u, p in urls) + "</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    write("site.webmanifest", json.dumps({"name": B["name"], "short_name": B["short"], "start_url": "/",
          "display": "standalone", "background_color": "#ffffff", "theme_color": "#14161a",
          "icons": [{"src": "/assets/img/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, indent=2))
    print("Built", ", ".join(pages), "for", SITE)

if __name__ == "__main__":
    main()
