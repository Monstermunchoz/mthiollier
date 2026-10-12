#!/usr/bin/env python3
"""Assemble le site statique M. Thiollier Conseils.

    python build.py

- src/pages/*.html      -> pages (fragment + bloc meta) assemblées avec en-tête/pied de page
- src/articles/*.html   -> actualites/<slug>.html + actualites/index.html
- sitemap.xml, robots.txt
Aucune dépendance hors bibliothèque standard.
"""
import json, re, html, datetime, pathlib

ROOT = pathlib.Path(__file__).parent
SITE = "https://www.mthiollierconseils.fr"
BRAND = "M. Thiollier Conseils"
PHONE = "06 43 64 29 64"
EMAIL = "mickael@mthiollierconseils.fr"
ADDR = "1000 Grande Rue, 01700 Miribel"
CALENDLY = "https://calendly.com/m-thiollierconseils/prise-de-contact"
TODAY = datetime.date.today().isoformat()

NAV = [("expertises.html", "Expertises"), ("cabinet.html", "Le cabinet"), ("actualites/index.html", "Actualités & conseils"),
       ("recrutement.html", "Recrutement"), ("contact.html", "Contact")]


U = "https://images.unsplash.com/photo-{}?auto=format&fit=crop&w={}&q=65"
PHOTOS = {
    "per-plan-epargne-retraite-guide-2026": "1782994978963-ad86f1eea34c",
    "preparer-sa-retraite-a-40-ans": "1774354669545-6265156237d4",
    "assurance-vie-fiscalite-apres-8-ans": "1772588627342-5ec373e236d8",
    "investir-en-scpi-guide-complet": "1781231702773-4cf3247fc061",
    "reduire-ses-impots-7-leviers-legaux": "1772588627483-d036793569e8",
    "placer-tresorerie-entreprise": "1781246212288-7fa538344718",
    "transmettre-son-patrimoine-donation-demembrement": "1777502626612-68ea24358eeb",
    "lmnp-location-meublee-2026": "1751945965597-71171ec7a458",
    "conseiller-gestion-patrimoine-independant-ou-banque": "1569087306794-db9947393580",
    "investissement-responsable-isr-labels": "1753246281088-51bbd10df0f2",
}
def photo(slug, w=1200):
    pid = PHOTOS.get(slug)
    return U.format(pid, w) if pid else ""
def vis(slug, label, w=900, cls="post-vis", alt=""):
    alt = html.escape(re.sub(r"<.*?>", "", alt).replace("&nbsp;", " "), quote=True) if alt else f"Illustration {label}"
    src = photo(slug, w)
    img = f'<img src="{src}" alt="{alt}" loading="lazy" decoding="async" onload="this.parentNode.classList.add(\'has-photo\')" onerror="this.remove()">' if src else ""
    return f'<div class="{cls}" aria-hidden="true">{img}<span>{label}</span></div>'

def meta_block(src):
    m = re.search(r"<!--\s*meta(.*?)-->", src, re.S)
    meta = {}
    if m:
        for line in m.group(1).strip().splitlines():
            if ":" in line:
                k, v = line.split(":", 1); meta[k.strip()] = v.strip()
        src = src[m.end():]
    return meta, src.strip()

def head(meta, rel, path, extra_ld=None):
    url = f"{SITE}/{path}".replace("/index.html", "/")
    ld = [{
        "@context": "https://schema.org", "@type": "FinancialService", "name": BRAND,
        "url": SITE + "/", "telephone": "+33643642964", "email": EMAIL,
        "address": {"@type": "PostalAddress", "streetAddress": "1000 Grande Rue", "postalCode": "01700", "addressLocality": "Miribel", "addressCountry": "FR"},
        "geo": {"@type": "GeoCoordinates", "latitude": 45.824046, "longitude": 4.952965},
        "areaServed": ["Miribel", "Lyon", "Ain", "Rhône", "Auvergne-Rhône-Alpes"],
        "founder": {"@type": "Person", "name": "Mickaël Thiollier", "jobTitle": "Conseiller en gestion de patrimoine", "image": SITE + "/assets/mickael-thiollier.webp"},
        "priceRange": "Premier entretien offert",
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": "5", "reviewCount": "7"}
    }]
    if extra_ld: ld += extra_ld
    og_type = meta.get("ogtype", "website")
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(meta['title'])}</title>
<meta name="description" content="{html.escape(meta['description'])}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta property="og:locale" content="fr_FR">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{html.escape(meta['title'])}">
<meta property="og:description" content="{html.escape(meta['description'])}">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:image" content="{SITE}/assets/og-image.svg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{rel}assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="/assets/fonts/plus-jakarta-sans.woff2" as="font" type="font/woff2" crossorigin>
<style>{CSS_INLINE}</style>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<a class="skip" href="#main">Aller au contenu</a>
"""

def header(rel, current):
    items = []
    for href, label in NAV:
        cur = ' aria-current="page"' if current and "#" not in href and href == current else ""
        items.append(f'<li><a href="{rel}{href}"{cur}>{label}</a></li>')
    return f"""<header class="site-header" id="top">
  <div class="wrap nav">
    <a class="brand" href="{rel}index.html">
      <span class="monogram" aria-hidden="true">MT</span>
      <span class="brand-text"><b>{BRAND}</b><small>Conseil en gestion de patrimoine</small></span>
    </a>
    <ul class="links" id="links">{''.join(items)}</ul>
    <div class="nav-cta">
      <a class="btn btn-primary" href="{rel}rendez-vous.html">Prendre rendez-vous</a>
      <button class="burger" id="burger" aria-label="Ouvrir le menu" aria-expanded="false" aria-controls="links"><i data-i="menu"></i></button>
    </div>
  </div>
</header>
<main id="main">
"""

def footer(rel):
    return f"""</main>
<footer class="foot">
  <div class="wrap">
    <div>
      <a class="brand" href="{rel}index.html"><span class="monogram" aria-hidden="true">MT</span><span class="brand-text"><b>{BRAND}</b><small>Conseil en gestion de patrimoine</small></span></a>
      <p>Cabinet de conseil en gestion de patrimoine indépendant. Conseiller en investissements financiers (CIF) enregistré à l'ORIAS, membre de la CNCEF Patrimoine, association agréée par l'Autorité des marchés financiers.</p>
    </div>
    <div>
      <p class="fh">Le cabinet</p>
      <ul><li><a href="{rel}expertises.html">Expertises</a></li><li><a href="{rel}expertises/assurance-vie.html">Assurance-vie</a></li><li><a href="{rel}expertises/plan-epargne-retraite.html">Plan d'épargne retraite</a></li><li><a href="{rel}expertises/accompagnement-dirigeants.html">Dirigeants</a></li><li><a href="{rel}cabinet.html">Qui suis-je</a></li><li><a href="{rel}simulateur.html">Simulateur</a></li><li><a href="{rel}recrutement.html">Recrutement</a></li></ul>
    </div>
    <div>
      <p class="fh">Ressources</p>
      <ul><li><a href="{rel}actualites/index.html">Actualités &amp; conseils</a></li><li><a href="{rel}actualites/per-plan-epargne-retraite-guide-2026.html">Guide du PER</a></li><li><a href="{rel}actualites/assurance-vie-fiscalite-apres-8-ans.html">Fiscalité de l'assurance-vie</a></li><li><a href="{rel}actualites/reduire-ses-impots-7-leviers-legaux.html">Réduire ses impôts</a></li></ul>
    </div>
    <div>
      <p class="fh">Contact</p>
      <ul><li>{ADDR}</li><li><a href="tel:+33643642964">{PHONE}</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li><a href="{rel}rendez-vous.html">Prendre rendez-vous</a></li></ul>
    </div>
    <div class="legal">
      <span>© 2026 Mickaël Thiollier. Tous droits réservés.</span>
      <span><a href="{rel}mentions-legales.html">Mentions légales</a> · <a href="{rel}mentions-legales.html#cgu">Conditions générales</a> · <a href="{rel}mentions-legales.html#rgpd">Confidentialité</a></span>
    </div>
  </div>
</footer>
<a class="fab" id="fab" href="{rel}rendez-vous.html" aria-label="Prendre rendez-vous"><i data-i="calendar-check"></i><span>Prendre rendez-vous</span></a>
<script src="{rel}assets/main.min.js?v={VER}" defer></script>
</body>
</html>
"""

ICONS = {}
def _icon(name, cls):
    if name not in ICONS:
        p = ROOT / "src/icons" / f"{name}.svg"
        if not p.exists():
            raise SystemExit(f"Icône introuvable : {name}")
        svg = re.sub(r"<!--.*?-->", "", p.read_text(), flags=re.S).strip()
        svg = re.sub(r"\s+", " ", svg)
        svg = re.sub(r'class="[^"]*"', "", svg)
        svg = re.sub(r'\s(width|height)="24"', "", svg).replace('stroke-width="2"', 'stroke-width="1.75"')
        ICONS[name] = svg
    klass = ("i " + cls).strip()
    return ICONS[name].replace("<svg ", f'<svg class="{klass}" aria-hidden="true" focusable="false" ', 1)

def icons(html_text):
    return re.sub(r'<i data-i="([a-z0-9-]+)"(?: class="([^"]*)")?></i>', lambda m: _icon(m.group(1), m.group(2) or ""), html_text)

import posixpath
def clean(u):
    """/cabinet.html -> /cabinet ; /actualites/index.html -> /actualites ; /index.html -> /"""
    base, frag = (u.split("#", 1) + [""])[:2]
    q = ""
    if "?" in base: base, q = base.split("?", 1); q = "?" + q
    if base.endswith(".html"):
        base = base[:-5]
        if base.endswith("/index") or base == "index" or base == "/index": base = base[:-5] or "/"
        if base != "/" and base.endswith("/"): base = base[:-1]
    return base + q + ("#" + frag if frag else "")

def absolutize(path, html_text):
    """Liens internes en chemins absolus et URL propres (sans .html), pour Vercel cleanUrls."""
    d = posixpath.dirname(path)
    def rep(m):
        attr, link = m.group(1), m.group(2)
        if re.match(r"^(https?:|mailto:|tel:|#|data:|//|javascript:)", link): return m.group(0)
        if link.startswith("/"): target = link
        else:
            p, _, rest = link.partition("#"); p, _, qs = p.partition("?")
            target = "/" + posixpath.normpath(posixpath.join(d, p)) if p else "/" + path
            target = target.replace("/./", "/")
            if target.endswith("/."): target = target[:-1]
            if qs: target += "?" + qs
            if rest: target += "#" + rest
        return f'{attr}="{clean(target)}"'
    html_text = re.sub(r'\b(href|src|action)="([^"]*)"', rep, html_text)
    # URL absolues du site (canonical, og, JSON-LD) sans .html
    html_text = re.sub(re.escape(SITE) + r'(/[^"\s<>]*?\.html)', lambda m: SITE + clean(m.group(1)), html_text)
    return html_text

import rcssmin, rjsmin, hashlib
_css = rcssmin.cssmin((ROOT / "assets/style.css").read_text(encoding="utf-8"))
_js = rjsmin.jsmin((ROOT / "assets/main.js").read_text(encoding="utf-8"))
(ROOT / "assets/style.min.css").write_text(_css, encoding="utf-8")
(ROOT / "assets/main.min.js").write_text(_js, encoding="utf-8")
VER = hashlib.md5((_css + _js).encode()).hexdigest()[:8]
FONT_FACE = "@font-face{font-family:'Plus Jakarta Sans';font-style:normal;font-display:swap;font-weight:200 800;src:url(/assets/fonts/plus-jakarta-sans.woff2) format('woff2');unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}"
CSS_INLINE = FONT_FACE + _css

def write(path, content):
    p = ROOT / path; p.parent.mkdir(parents=True, exist_ok=True)
    if path.endswith(".html"): content = absolutize(path, content)
    elif path == "sitemap.xml": content = re.sub(re.escape(SITE) + r'(/[^<]*?\.html)', lambda m: SITE + clean(m.group(1)), content).replace(SITE + "/actualites/<", SITE + "/actualites<")
    content = content.replace(SITE + '/actualites/"', SITE + '/actualites"').replace(SITE + '/actualites/<', SITE + '/actualites<')
    p.write_text(icons(content), encoding="utf-8"); print("✓", path)

# ---------- Articles ----------
arts = []
for f in sorted((ROOT / "src/articles").glob("*.html")):
    meta, body = meta_block(f.read_text(encoding="utf-8"))
    meta["slug"] = f.stem
    meta["body"] = body
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", body, re.S).group(1)
    meta["h1"] = re.sub("<.*?>", "", h1).strip()
    meta["words"] = len(re.sub("<.*?>", " ", body).split())
    arts.append(meta)
arts.sort(key=lambda m: m["date"], reverse=True)

CTA = """<div class="cta-band s-white">
  <div class="wrap">
    <div class="cta-box">
      <div>
        <h2>Faisons le point sur votre situation patrimoniale</h2>
        <p>Premier rendez-vous d'1h30 offert, en visioconférence ou au cabinet. Vous repartez avec une analyse écrite de votre situation.</p>
      </div>
      <div class="actions">
        <a class="btn btn-dark btn-lg" href="{REL}rendez-vous.html">Prendre rendez-vous<i data-i="arrow-right"></i></a>
        <a class="btn btn-ghost btn-lg" href="{REL}contact.html">Poser une question</a>
      </div>
    </div>
  </div>
</div>"""

def card(o, featured=False, w=900):
    lab = "".join(x[0] for x in o["keyword"].split()[:2]).upper()
    return (f'<a class="post{" featured" if featured else ""}" href="{{REL}}actualites/{o["slug"]}.html" data-cat="{o["category"]}">'
            f'{vis(o["slug"], lab, w, alt=o["h1"])}<div class="post-body"><div class="post-meta"><span class="cat">{o["category"]}</span>'
            f'<span>{o["reading"]} de lecture</span></div><h3>{o["h1"]}</h3><p>{o["excerpt"]}</p></div></a>')

KEYS = {
 "assurance-vie-fiscalite-apres-8-ans": ["Tant que vous ne retirez rien, l'assurance-vie ne génère aucun impôt sur le revenu.", "Après 8 ans, un couple peut retirer chaque année jusqu'à 9&nbsp;200&nbsp;€ de gains sans impôt sur le revenu.", "Pour la transmission, chaque bénéficiaire profite d'un abattement de 152&nbsp;500&nbsp;€ sur les primes versées avant 70 ans."],
 "conseiller-gestion-patrimoine-independant-ou-banque": ["Un conseiller sérieux est immatriculé à l'ORIAS et membre d'une association agréée (CIF).", "Indépendant ne veut pas dire gratuit&nbsp;: la rémunération doit être écrite et compréhensible.", "La banque suffit pour des besoins simples&nbsp;; une stratégie globale demande une architecture ouverte."],
 "investir-en-scpi-guide-complet": ["Une SCPI permet d'investir dans l'immobilier d'entreprise sans gestion, à partir de quelques centaines d'euros.", "Le bon rendement est le rendement net d'impôt dans votre situation, pas le taux affiché.", "Le principal risque est la liquidité&nbsp;: une SCPI s'envisage sur 8 à 10 ans minimum."],
 "investissement-responsable-isr-labels": ["Trois labels, trois promesses&nbsp;: ISR, Greenfin et Finansol.", "Le label ISR a été durci en 2024&nbsp;: vérifiez la date de labellisation du fonds.", "Un placement responsable s'intègre facilement dans une assurance-vie ou un PER."],
 "lmnp-location-meublee-2026": ["Au régime réel, l'amortissement neutralise l'essentiel de l'impôt sur les loyers.", "La réforme de 2025 alourdit la plus-value en cas de revente, pas la fiscalité des loyers.", "Pour une détention de 15 ans et plus, le LMNP reste l'un des régimes locatifs les plus efficaces."],
 "per-plan-epargne-retraite-guide-2026": ["Les versements sont déductibles de votre revenu imposable, dans la limite d'un plafond reportable.", "Le PER reporte l'impôt, il ne l'efface pas&nbsp;: il est gagnant si votre taux d'imposition baisse à la retraite.", "L'épargne est bloquée jusqu'à la retraite, sauf cas de déblocage anticipé comme l'achat de la résidence principale."],
 "placer-tresorerie-entreprise": ["Commencez par isoler la trésorerie réellement excédentaire de celle utile à l'exploitation.", "Compte à terme pour le court terme, contrat de capitalisation pour le long terme.", "L'usufruit temporaire de SCPI est un outil réservé aux sociétés, fiscalement très efficace."],
 "preparer-sa-retraite-a-40-ans": ["À 40 ans, vous avez encore 20 à 25 ans d'effort d'épargne devant vous&nbsp;: le temps travaille pour vous.", "Chiffrez d'abord votre taux de remplacement, puis le manque mensuel à combler.", "Automatisez un versement réparti entre PER, assurance-vie et immobilier, et ajustez tous les deux ans."],
 "reduire-ses-impots-7-leviers-legaux": ["Réduction, déduction et crédit d'impôt n'ont pas le même effet sur votre impôt.", "Priorité aux leviers sans risque&nbsp;: emploi à domicile, dons et, dès 30&nbsp;% d'imposition, le PER.", "Immobilier (déficit foncier, Denormandie, LMNP) et FIP/FCPI viennent ensuite, selon votre profil."],
 "transmettre-son-patrimoine-donation-demembrement": ["Chaque parent peut donner 100&nbsp;000&nbsp;€ à chaque enfant sans droits, abattement renouvelable tous les 15 ans.", "Le démembrement permet de transmettre plus pour une valeur fiscale moindre, surtout si l'on donne tôt.", "L'assurance-vie offre un circuit de transmission parallèle, hors succession."],
}

# ---------- Logos partenaires (défilement) ----------
FIN = [("swiss-life","Swiss Life"),("arkea","Arkéa"),("corum","Corum"),("perial-asset-management","Perial Asset Management"),("norma-capital","Norma Capital"),("eiffel-investment-group","Eiffel Investment Group"),("altaroc","Altaroc"),("eres","Eres"),("inter-invest","Inter Invest"),("inter-gestion","Inter Gestion"),("horizon-asset-management","Horizon AM"),("kyaneos","Kyaneos"),("m-capital","M Capital"),("alderian","Alderian"),("fiducial","Fiducial"),("selencia","Selencia"),("sodify","Sodify"),("digital-insure","Digital Insure"),("crequy","Crequy"),("u-wine","U'Wine"),("3-colonnes-economie-solidaire","3 Colonnes"),("prestige-immobilier","Prestige Immobilier")]
IMMO = [("vinci","Vinci Immobilier"),("perl","Perl"),("urbat","Urbat"),("groupe-edouard-denis","Groupe Edouard Denis"),("saint-agne-groupe-immobilier","Saint-Agne"),("lp-promotion","LP Promotion"),("green-city-immobilier","Green City Immobilier"),("groupe-cailleau","Groupe Cailleau"),("groupe-cir","Groupe CIR"),("cbo-territoria","CBo Territoria"),("colonies","Colonies"),("colocatere-location-autrement","Colocatère"),("confiance-groupe-immobilier","Confiance Immobilier"),("group-flot-immobilier","Flot Immobilier"),("loftwood","Loftwood"),("village-or-residences-seniors","Village d'Or")]
from PIL import Image as _Im
LOGO_SIZE = {p.stem: _Im.open(p).size for p in (ROOT / "assets/partenaires").glob("*.webp")}
def marquee(items, rel="", reverse=False, label="Nos partenaires"):
    def li(hidden):
        return "".join(f'<li><img src="{rel}assets/partenaires/{f}.webp" alt="{n}" loading="lazy" decoding="async" width="{LOGO_SIZE[f][0]}" height="{LOGO_SIZE[f][1]}"></li>' for f, n in items)
    return (f'<div class="marquee{" rev" if reverse else ""}" role="region" aria-label="{label}">'
            f'<ul class="mq-track"><li class="mq-group"><ul>{li(False)}</ul></li><li class="mq-group" aria-hidden="true"><ul>{li(True)}</ul></li></ul></div>')

LATEST = '<div class="posts">' + "".join(card(o) for o in arts[:3]) + '</div>'

# ---------- Pages ----------
pages = []
for f in sorted((ROOT / "src/pages").glob("*.html")):
    meta, body = meta_block(f.read_text(encoding="utf-8"))
    name = f.name
    rel = ""
    extra = None
    if meta.get("faq") == "1":
        qs = re.findall(r"<summary>(.*?)</summary>\s*<p>(.*?)</p>", body, re.S)
        extra = [{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": html.unescape(re.sub("<.*?>", "", q)).strip(), "acceptedAnswer": {"@type": "Answer", "text": html.unescape(re.sub("<.*?>", "", a)).strip()}} for q, a in qs]}]
    if meta.get("jobposting") == "1":
        extra = (extra or []) + [{
            "@context": "https://schema.org", "@type": "JobPosting",
            "title": "Conseiller(ère) en gestion de patrimoine – développement commercial",
            "description": "Rejoignez un cabinet indépendant près de Lyon en tant que mandataire : clientèle particuliers et dirigeants, architecture ouverte, rémunération 100 % variable non plafonnée, formation et back-office assurés.",
            "datePosted": TODAY, "employmentType": "CONTRACTOR",
            "hiringOrganization": {"@type": "Organization", "name": BRAND, "sameAs": SITE},
            "jobLocation": {"@type": "Place", "address": {"@type": "PostalAddress", "streetAddress": "1000 Grande Rue", "postalCode": "01700", "addressLocality": "Miribel", "addressRegion": "Auvergne-Rhône-Alpes", "addressCountry": "FR"}},
            "applicantLocationRequirements": {"@type": "Country", "name": "France"},
            "jobLocationType": "TELECOMMUTE", "directApply": True
        }]
    body = body.replace("<!--MQ-ALL-->", marquee(FIN[:11]+IMMO[:4]+FIN[11:]+IMMO[4:])).replace("<!--MQ-FIN-->", marquee(FIN, label="Partenaires financiers")).replace("<!--MQ-IMMO-->", marquee(IMMO, reverse=True, label="Partenaires immobiliers")).replace("<!--LATEST-->", LATEST.replace("{REL}", "")).replace("<!--CTA-->", CTA.replace("{REL}", ""))
    out = head(meta, rel, name, extra) + header(rel, name) + body + "\n" + footer(rel)
    write(name, out); pages.append((name, meta.get("priority", "0.7")))


def ymd_fr(d):
    y, m, dd = d.split("-"); mois = ["janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"]
    return f"{int(dd)} {mois[int(m)-1]} {y}"

for i, a in enumerate(arts):
    rel = "../"; path = f"actualites/{a['slug']}.html"; url = f"{SITE}/{path}"
    body = a["body"]
    # Sommaire à partir des h2 (hors FAQ et conclusion "Ce que je vous conseille")
    h2s = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body)
    toc = "".join(f'<li><a href="#{i_}">{re.sub("<.*?>", "", t)}</a></li>' for i_, t in h2s)
    # Tableaux scrollables
    body = re.sub(r"<table>(.*?)</table>", r'<div class="tbl"><table>\1</table></div>', body, flags=re.S)
    # Retirer le h1 et le chapô du corps (affichés dans l'en-tête)
    body = re.sub(r"<h1[^>]*>.*?</h1>\s*", "", body, count=1, flags=re.S)
    lede = re.search(r'<p class="lede">(.*?)</p>', body, re.S)
    lede_html = lede.group(1) if lede else ""
    body = re.sub(r'<p class="lede">.*?</p>\s*', "", body, count=1, flags=re.S)
    keys = KEYS.get(a["slug"], [])
    ess = ('<div class="essentiel"><b>L\'essentiel en 30 secondes</b><ul>' + "".join(f"<li>{k}</li>" for k in keys) + '</ul></div>') if keys else ""
    faqs = re.findall(r"<summary>(.*?)</summary>\s*<p>(.*?)</p>", body, re.S)
    ld = [{
        "@context": "https://schema.org", "@type": "Article", "headline": a["h1"], "description": a["description"],
        "datePublished": a["date"], "dateModified": a["date"], "wordCount": a["words"], "inLanguage": "fr-FR",
        "mainEntityOfPage": url, "image": photo(a["slug"], 1200) or f"{SITE}/assets/og-image.svg", "articleSection": a["category"],
        "author": {"@type": "Person", "name": "Mickaël Thiollier", "jobTitle": "Conseiller en gestion de patrimoine (CIF)", "url": SITE + "/cabinet.html"},
        "publisher": {"@type": "Organization", "name": BRAND, "url": SITE, "logo": {"@type": "ImageObject", "url": f"{SITE}/assets/favicon.svg"}}
    }, {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Accueil", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": "Actualités & conseils", "item": SITE + "/actualites/"},
        {"@type": "ListItem", "position": 3, "name": a["h1"], "item": url}]}]
    if faqs:
        ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": html.unescape(re.sub("<.*?>", "", q)).strip(), "acceptedAnswer": {"@type": "Answer", "text": html.unescape(re.sub("<.*?>", "", an)).strip()}} for q, an in faqs]})
    # Articles liés : 3 suivants (même catégorie en priorité)
    others = [o for o in arts if o is not a]
    same = [o for o in others if o["category"] == a["category"]]
    related = (same + [o for o in others if o not in same])[:3]
    rel_cards = "".join(f"""<a class="post" href="{o['slug']}.html" data-cat="{o['category']}">{vis(o['slug'], o['category'][:2], alt=o['h1'])}<div class="post-body"><div class="post-meta"><span class="cat">{o['category']}</span><span>{o['reading']}</span></div><h3>{o['h1']}</h3><p>{o['excerpt']}</p></div></a>""" for o in related)
    initials = "".join(w[0] for w in a["keyword"].split()[:2]).upper()
    page = head({"title": a["title"], "description": a["description"], "ogtype": "article"}, rel, path, ld) + header(rel, "actualites/index.html") + f"""
<div class="read-progress" aria-hidden="true"><i></i></div>
<article>
  <div class="art-head">
    <div class="wrap">
      <nav class="crumbs" aria-label="Fil d'Ariane"><a href="../index.html">Accueil</a><span>/</span><a href="index.html">Actualités &amp; conseils</a><span>/</span><span>{a['category']}</span></nav>
      <span class="eyebrow">{a['category']} · {a['reading']} de lecture</span>
      <h1>{a['h1']}</h1>
      <p class="lede">{lede_html}</p>
      <div class="art-meta">
        <span class="author"><img src="../assets/mickael-thiollier.webp" alt="Mickaël Thiollier" width="32" height="32" style="width:32px;height:32px;border-radius:50%;object-fit:cover">Mickaël Thiollier, conseiller en gestion de patrimoine</span>
        <time datetime="{a['date']}">Publié le {ymd_fr(a['date'])}</time>
        <span>Mis à jour le {ymd_fr(a['date'])}</span>
      </div>
    </div>
  </div>
  <div class="art-vis"><div role="img" aria-label="Illustration : {a['keyword']}" style="position:relative">{('<img src="' + photo(a['slug'], 1200) + '" alt="' + html.escape(a['keyword'], quote=True) + '" fetchpriority="high" decoding="async" onload="this.parentNode.classList.add(&#39;has-photo&#39;)" onerror="this.remove()">') if photo(a['slug']) else ''}<span>{initials}</span></div></div>
  <div class="art-layout">
    <div class="art-body">
{ess}
{body}
      <p class="disclaimer">Les informations de cet article sont fournies à titre pédagogique à la date de publication et ne constituent pas un conseil personnalisé. Les placements présentent un risque de perte en capital ; la fiscalité dépend de votre situation et de la législation en vigueur. Seule une étude patrimoniale permet de valider une stratégie.</p>
      <div class="author-box">
        <img src="../assets/mickael-thiollier.webp" alt="Mickaël Thiollier" width="64" height="64" style="width:64px;height:64px;border-radius:50%;object-fit:cover">
        <div><b>Mickaël Thiollier</b><p>Conseiller en gestion de patrimoine indépendant (CIF, ORIAS, CNCEF). Dix ans d'expérience en finance après un parcours dans l'immobilier. Il accompagne particuliers, dirigeants et professions libérales en visioconférence ou au cabinet.</p><p style="margin-top:14px"><a class="btn btn-dark" href="../rendez-vous.html">Prendre rendez-vous<i data-i="arrow-right"></i></a></p></div>
      </div>
    </div>
    <aside class="toc" aria-label="Sommaire">
      <b>Sommaire</b>
      <ol>{toc}</ol>
      <div class="cta"><p>Une question sur votre situation&nbsp;? Parlons-en, le premier entretien est offert.</p><a class="btn btn-primary" href="../rendez-vous.html">Prendre rendez-vous</a></div>
    </aside>
  </div>
</article>
<section class="related"><div class="wrap"><h2>À lire ensuite</h2><div class="posts">{rel_cards}</div></div></section>
""" + CTA.replace("{REL}", "../") + footer(rel)
    write(path, page)

# ---------- Index des actualités ----------
cats = sorted(set(a["category"] for a in arts))
filters = '<button class="tab" role="tab" aria-selected="true" data-cat="all">Tous</button>' + "".join(f'<button class="tab" role="tab" aria-selected="false" data-cat="{c}">{c}</button>' for c in cats)
cards = ""
for i, a in enumerate(arts):
    cards += f"""<a class="post{' featured' if i == 0 else ''}" href="{a['slug']}.html" data-cat="{a['category']}">{vis(a['slug'], ''.join(w[0] for w in a['keyword'].split()[:2]).upper(), 1400 if i == 0 else 900)}<div class="post-body"><div class="post-meta"><span class="cat">{a['category']}</span><span>{ymd_fr(a['date'])}</span><span>· {a['reading']}</span></div><h3>{a['h1']}</h3><p>{a['excerpt']}</p></div></a>"""
idx_meta = {"title": "Actualités & conseils gestion de patrimoine | M. Thiollier",
            "description": "Décryptages chiffrés sur le PER, l'assurance-vie, les SCPI, la fiscalité, la retraite et la transmission, rédigés par un conseiller en gestion de patrimoine indépendant."}
ld_idx = [{"@context": "https://schema.org", "@type": "Blog", "name": "Actualités & conseils", "url": SITE + "/actualites/", "publisher": {"@type": "Organization", "name": BRAND},
           "blogPost": [{"@type": "BlogPosting", "headline": a["h1"], "url": f"{SITE}/actualites/{a['slug']}.html", "datePublished": a["date"]} for a in arts]}]
idx = head(idx_meta, "../", "actualites/index.html", ld_idx) + header("../", "actualites/index.html") + f"""
<section class="page-head"><div class="wrap">
  <nav class="crumbs" aria-label="Fil d'Ariane"><a href="../index.html">Accueil</a><span>/</span><span>Actualités &amp; conseils</span></nav>
  <h1>Décryptages et conseils patrimoniaux</h1>
  <p class="lede">Fiscalité, placements, retraite, immobilier, transmission&nbsp;: des analyses sourcées et mises à jour avec les règles en vigueur, pour éclairer vos décisions patrimoniales.</p>
</div></section>
<section class="s-white" style="padding-top:clamp(48px,6vw,72px)"><div class="wrap">
  <h2 class="sr-only">Tous les articles</h2>
  <div class="filters" role="tablist" aria-label="Filtrer par thème">{filters}</div>
  <div class="posts">{cards}</div>
</div></section>
""" + CTA.replace("{REL}", "../") + footer("../")
write("actualites/index.html", idx)

# ---------- Pages expertises (une page par expertise) ----------
import importlib.util as _ilu
_spec = _ilu.spec_from_file_location("expdata", ROOT / "src/expertises_data.py"); _m = _ilu.module_from_spec(_spec); _spec.loader.exec_module(_m)
EXPERTISES = _m.EXPERTISES
EXP = {e["slug"]: e for e in EXPERTISES}
ART = {a["slug"]: a for a in arts}

def exp_card(e, rel, i=0):
    blue = " blue" if i % 2 else ""
    return (f'<a class="card" href="{rel}expertises/{e["slug"]}.html"><span class="ico{blue}"><i data-i="{e["icon"]}"></i></span>'
            f'<h3>{e["name"]}</h3><p>{e["card"]}</p><span class="btn-link">Découvrir l\'expertise<i data-i="arrow-right"></i></span></a>')

for e in EXPERTISES:
    rel = "../"; path = f"expertises/{e['slug']}.html"; url = f"{SITE}/{path}"
    # Articles liés : l'article principal, puis ceux des expertises voisines
    slugs = [e["article"]] + [EXP[r]["article"] for r in e["related"] if r in EXP]
    seen = []
    for sl in slugs:
        if sl in ART and sl not in seen: seen.append(sl)
    for a in arts:
        if len(seen) >= 3: break
        if a["slug"] not in seen: seen.append(a["slug"])
    posts = '<div class="posts">' + "".join(card(ART[sl]) for sl in seen[:3]).replace("{REL}", rel) + "</div>"
    enjeux = "".join(f'<div class="card"><span class="ico{" blue" if i % 2 else ""}"><i data-i="{ic}"></i></span><h3>{t}</h3><p>{d}</p></div>' for i, (ic, t, d) in enumerate(e["enjeux"]))
    steps = "".join(f'<div class="step"><span class="step-n">Étape {i+1}</span><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(e["approche"]))
    sols = "".join(f'<div class="sol"><span class="ico{" blue" if i % 2 else ""}"><i data-i="circle-check"></i></span><div><h3>{t}</h3><p>{d}</p></div></div>' for i, (t, d) in enumerate(e["solutions"]))
    pq = "".join(f'<li><span class="ico white"><i data-i="{ic}"></i></span><span>{t}</span></li>' for ic, t in zip(["user-round", "users", "target"], e["pourqui"]))
    faq = "".join(f'<details{" open" if i == 0 else ""}><summary>{q}</summary><p>{a}</p></details>' for i, (q, a) in enumerate(e["faq"]))
    others = "".join(exp_card(EXP[r], rel, i) for i, r in enumerate(e["related"]) if r in EXP)
    ld = [{"@context": "https://schema.org", "@type": "Service", "name": e["h1"], "description": e["description"], "url": url,
           "serviceType": "Conseil en gestion de patrimoine", "areaServed": "FR",
           "provider": {"@type": "FinancialService", "name": BRAND, "url": SITE + "/"}},
          {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
              {"@type": "ListItem", "position": 1, "name": "Accueil", "item": SITE + "/"},
              {"@type": "ListItem", "position": 2, "name": "Expertises", "item": SITE + "/expertises.html"},
              {"@type": "ListItem", "position": 3, "name": e["name"], "item": url}]},
          {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
              {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in e["faq"]]}]
    body = f"""
<section class="page-head exp-head">
  <div class="wrap">
    <nav class="crumbs" aria-label="Fil d'Ariane"><a href="../index.html">Accueil</a><span>/</span><a href="../expertises.html">Expertises</a><span>/</span><span>{e['name']}</span></nav>
    <span class="exp-ico ico"><i data-i="{e['icon']}"></i></span>
    <h1>{e['h1']}</h1>
    <p class="lede">{e['lede']}</p>
    <div class="hero-actions"><a class="btn btn-primary btn-lg" href="../rendez-vous.html">Demander un bilan offert<i data-i="arrow-right"></i></a><a class="btn btn-ghost btn-lg" href="#articles">Lire nos guides</a></div>
  </div>
</section>

<section class="s-white">
  <div class="wrap">
    <div class="sec-head center"><h2>Les enjeux</h2><p class="lede">Ce qui fait la différence entre une décision prise au hasard et une stratégie qui tient dans la durée.</p></div>
    <div class="cards cards-3">{enjeux}</div>
  </div>
</section>

<section class="s-navy exp-pq">
  <div class="wrap">
    <div class="sec-head center"><h2>Pour qui&nbsp;?</h2></div>
    <ul class="pq">{pq}</ul>
  </div>
</section>

<section class="s-soft">
  <div class="wrap">
    <div class="sec-head center"><h2>Notre accompagnement</h2><p class="lede">Une démarche en quatre étapes, formalisée par écrit, pour décider en toute connaissance de cause.</p></div>
    <div class="steps four">{steps}</div>
  </div>
</section>

<section class="s-white">
  <div class="wrap">
    <div class="sec-head center"><h2>Les solutions mobilisées</h2><p class="lede">Sélectionnées parmi près de 40 partenaires, comparées sur leurs frais, leur qualité de gestion et leur solidité.</p></div>
    <div class="sols">{sols}</div>
  </div>
</section>

<section class="s-soft" id="faq">
  <div class="wrap faq">
    <div class="sec-head tight"><h2>Questions fréquentes</h2><p class="lede">{e['name']}&nbsp;: les réponses aux questions que l'on me pose le plus souvent.</p></div>
    <div class="faq-list">{faq}</div>
  </div>
</section>

<section class="s-white" id="articles">
  <div class="wrap">
    <div class="sec-head center"><h2>Pour aller plus loin</h2><p class="lede">Nos guides pour approfondir le sujet avant notre premier échange.</p></div>
    {posts}
    <p style="margin-top:40px;text-align:center"><a class="btn btn-ghost" href="../actualites/index.html">Tous les articles<i data-i="arrow-right"></i></a></p>
  </div>
</section>

<section class="s-soft">
  <div class="wrap">
    <div class="sec-head center"><h2>Expertises associées</h2></div>
    <div class="cards cards-3">{others}</div>
  </div>
</section>
""" + CTA.replace("{REL}", rel)
    page = head({"title": e["title"], "description": e["description"]}, rel, path, ld) + header(rel, "expertises.html") + body + "\n" + footer(rel)
    write(path, page); pages.append((path, "0.8"))


# ---------- Sitemap & robots ----------
urls = [("", "1.0", "weekly")] + [(p, pr, "monthly") for p, pr in pages if p != "index.html"] + [("actualites/", "0.8", "weekly")] + [(f"actualites/{a['slug']}.html", "0.7", "monthly") for a in arts]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
    f"  <url><loc>{SITE}/{u}</loc><lastmod>{TODAY}</lastmod><changefreq>{c}</changefreq><priority>{p}</priority></url>\n" for u, p, c in urls) + "</urlset>\n"
write("sitemap.xml", sm)
write("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /src/\nSitemap: {SITE}/sitemap.xml\n")
print(f"\n{len(pages)} pages, {len(arts)} articles.")
