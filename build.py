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
SITE = "https://mthiollierconseils.fr"
BRAND = "M. Thiollier Conseils"
PHONE = "06 43 64 29 64"
EMAIL = "mickael@mthiollierconseils.fr"
ADDR = "1000 Grande Rue, 01700 Miribel"
CALENDLY = "https://calendly.com/m-thiollierconseils/prise-de-contact"
TODAY = datetime.date.today().isoformat()

NAV = [("expertises.html", "Expertises"), ("cabinet.html", "Le cabinet"), ("actualites/index.html", "Actualités & conseils"),
       ("recrutement.html", "Recrutement"), ("contact.html", "Contact")]


U = "https://images.unsplash.com/photo-{}?auto=format&fit=crop&w={}&q=72"
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
def vis(slug, label, w=900, cls="post-vis"):
    src = photo(slug, w)
    img = f'<img src="{src}" alt="" loading="lazy" decoding="async" onload="this.parentNode.classList.add(\'has-photo\')" onerror="this.remove()">' if src else ""
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
        "openingHours": "Mo-Fr 09:00-19:00", "priceRange": "Premier entretien offert",
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
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Instrument+Serif:ital@1&display=swap">
<link rel="stylesheet" href="{rel}assets/style.css">
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
    <a class="brand" href="{rel}index.html" aria-label="{BRAND}, accueil">
      <span class="monogram" aria-hidden="true">MT</span>
      <span class="brand-text"><b>{BRAND}</b><small>Gestion de patrimoine · Lyon &amp; Ain</small></span>
    </a>
    <ul class="links" id="links">{''.join(items)}</ul>
    <div class="nav-cta">
      <a class="btn btn-ghost" href="tel:+33643642964"><i data-i="phone"></i>06 43 64 29 64</a>
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
      <a class="brand" href="{rel}index.html"><span class="monogram" aria-hidden="true">MT</span><span class="brand-text"><b>{BRAND}</b><small>Gestion de patrimoine · Lyon &amp; Ain</small></span></a>
      <p>Cabinet indépendant de conseil en gestion de patrimoine à Miribel, près de Lyon. Conseiller en investissements financiers (CIF) enregistré à l'ORIAS, membre de la CNCEF Patrimoine, association agréée par l'AMF.</p>
    </div>
    <div>
      <h4>Le cabinet</h4>
      <ul><li><a href="{rel}expertises.html">Expertises</a></li><li><a href="{rel}cabinet.html">Qui suis-je</a></li><li><a href="{rel}simulateur.html">Simulateur</a></li><li><a href="{rel}recrutement.html">Recrutement</a></li></ul>
    </div>
    <div>
      <h4>Ressources</h4>
      <ul><li><a href="{rel}actualites/index.html">Actualités &amp; conseils</a></li><li><a href="{rel}actualites/per-plan-epargne-retraite-guide-2026.html">Guide du PER</a></li><li><a href="{rel}actualites/assurance-vie-fiscalite-apres-8-ans.html">Fiscalité de l'assurance-vie</a></li><li><a href="{rel}actualites/reduire-ses-impots-7-leviers-legaux.html">Réduire ses impôts</a></li></ul>
    </div>
    <div>
      <h4>Contact</h4>
      <ul><li>{ADDR}</li><li><a href="tel:+33643642964">{PHONE}</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li><a href="{rel}rendez-vous.html">Prendre rendez-vous</a></li></ul>
    </div>
    <div class="legal">
      <span>© 2026 Mickaël Thiollier. Tous droits réservés.</span>
      <span><a href="{rel}mentions-legales.html">Mentions légales</a> · <a href="{rel}mentions-legales.html#cgu">Conditions générales</a> · <a href="{rel}mentions-legales.html#rgpd">Confidentialité</a></span>
    </div>
  </div>
</footer>
<script src="{rel}assets/main.js" defer></script>
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

def write(path, content):
    p = ROOT / path; p.parent.mkdir(parents=True, exist_ok=True)
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
        <h2>Un premier rendez-vous d'1h30, offert et sans engagement</h2>
        <p>En visio ou au cabinet de Miribel. Vous repartez avec un bilan écrit de votre situation.</p>
      </div>
      <div class="actions">
        <a class="btn btn-dark btn-lg" href="{REL}rendez-vous.html">Réserver mon créneau<i data-i="arrow-right"></i></a>
        <a class="btn btn-ghost btn-lg" href="{REL}contact.html">Poser une question</a>
      </div>
    </div>
  </div>
</div>"""

def card(o, featured=False, w=900):
    lab = "".join(x[0] for x in o["keyword"].split()[:2]).upper()
    return (f'<a class="post{" featured" if featured else ""}" href="{{REL}}actualites/{o["slug"]}.html" data-cat="{o["category"]}">'
            f'{vis(o["slug"], lab, w)}<div class="post-body"><div class="post-meta"><span class="cat">{o["category"]}</span>'
            f'<span>{o["reading"]} de lecture</span></div><h3>{o["h1"]}</h3><p>{o["excerpt"]}</p></div></a>')
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
    body = body.replace("<!--LATEST-->", LATEST.replace("{REL}", "")).replace("<!--CTA-->", CTA.replace("{REL}", ""))
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
    rel_cards = "".join(f"""<a class="post" href="{o['slug']}.html" data-cat="{o['category']}">{vis(o['slug'], o['category'][:2])}<div class="post-body"><div class="post-meta"><span class="cat">{o['category']}</span><span>{o['reading']}</span></div><h3>{o['h1']}</h3><p>{o['excerpt']}</p></div></a>""" for o in related)
    initials = "".join(w[0] for w in a["keyword"].split()[:2]).upper()
    page = head({"title": a["title"], "description": a["description"], "ogtype": "article"}, rel, path, ld) + header(rel, "actualites/index.html") + f"""
<article>
  <div class="art-head">
    <div class="wrap">
      <nav class="crumbs" aria-label="Fil d'Ariane"><a href="../index.html">Accueil</a><span>/</span><a href="index.html">Actualités &amp; conseils</a><span>/</span><span>{a['category']}</span></nav>
      <span class="eyebrow">{a['category']} · {a['reading']} de lecture</span>
      <h1>{a['h1']}</h1>
      <p class="lede">{lede_html}</p>
      <div class="art-meta">
        <span class="author"><img src="../assets/mickael-thiollier.webp" alt="" width="32" height="32" style="width:32px;height:32px;border-radius:50%;object-fit:cover">Mickaël Thiollier, conseiller en gestion de patrimoine</span>
        <time datetime="{a['date']}">Publié le {ymd_fr(a['date'])}</time>
        <span>Mis à jour le {ymd_fr(a['date'])}</span>
      </div>
    </div>
  </div>
  <div class="art-vis"><div role="img" aria-label="Illustration : {a['keyword']}" style="position:relative">{('<img src="' + photo(a['slug'], 1600) + '" alt="" fetchpriority="high" decoding="async" onload="this.parentNode.classList.add(&#39;has-photo&#39;)" onerror="this.remove()">') if photo(a['slug']) else ''}<span>{initials}</span></div></div>
  <div class="art-layout">
    <div class="art-body">
{body}
      <p class="disclaimer">Les informations de cet article sont fournies à titre pédagogique à la date de publication et ne constituent pas un conseil personnalisé. Les placements présentent un risque de perte en capital ; la fiscalité dépend de votre situation et de la législation en vigueur. Seule une étude patrimoniale permet de valider une stratégie.</p>
      <div class="author-box">
        <img src="../assets/mickael-thiollier.webp" alt="Mickaël Thiollier" width="64" height="64" style="width:64px;height:64px;border-radius:50%;object-fit:cover">
        <div><b>Mickaël Thiollier</b><p>Conseiller en gestion de patrimoine indépendant (CIF, ORIAS, CNCEF) à Miribel, près de Lyon. Dix ans de finance après un parcours en immobilier. Il reçoit en visio ou au cabinet pour un premier entretien offert.</p><p style="margin-top:14px"><a class="btn btn-dark" href="../rendez-vous.html">Prendre rendez-vous<i data-i="arrow-right"></i></a></p></div>
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
            "description": "Guides clairs et chiffrés sur le PER, l'assurance-vie, les SCPI, la fiscalité, la retraite et la transmission, rédigés par un conseiller indépendant près de Lyon."}
ld_idx = [{"@context": "https://schema.org", "@type": "Blog", "name": "Actualités & conseils", "url": SITE + "/actualites/", "publisher": {"@type": "Organization", "name": BRAND},
           "blogPost": [{"@type": "BlogPosting", "headline": a["h1"], "url": f"{SITE}/actualites/{a['slug']}.html", "datePublished": a["date"]} for a in arts]}]
idx = head(idx_meta, "../", "actualites/index.html", ld_idx) + header("../", "actualites/index.html") + f"""
<section class="page-head"><div class="wrap">
  <nav class="crumbs" aria-label="Fil d'Ariane"><a href="../index.html">Accueil</a><span>/</span><span>Actualités &amp; conseils</span></nav>
  <h1>Actualités & conseils</h1>
  <p class="lede">Des guides longs, sourcés et mis à jour, écrits par le conseiller que vous rencontrerez. Les chiffres 2026, les cas où ça marche et ceux où ça ne marche pas.</p>
</div></section>
<section class="s-white" style="padding-top:clamp(48px,6vw,72px)"><div class="wrap">
  <div class="filters" role="tablist" aria-label="Filtrer par thème">{filters}</div>
  <div class="posts">{cards}</div>
</div></section>
""" + CTA.replace("{REL}", "../") + footer("../")
write("actualites/index.html", idx)

# ---------- Sitemap & robots ----------
urls = [("", "1.0", "weekly")] + [(p, pr, "monthly") for p, pr in pages if p != "index.html"] + [("actualites/", "0.8", "weekly")] + [(f"actualites/{a['slug']}.html", "0.7", "monthly") for a in arts]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
    f"  <url><loc>{SITE}/{u}</loc><lastmod>{TODAY}</lastmod><changefreq>{c}</changefreq><priority>{p}</priority></url>\n" for u, p, c in urls) + "</urlset>\n"
write("sitemap.xml", sm)
write("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /src/\nSitemap: {SITE}/sitemap.xml\n")
print(f"\n{len(pages)} pages, {len(arts)} articles.")
