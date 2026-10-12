# M. Thiollier Conseils — site vitrine

Site statique (HTML/CSS/JS sans framework), hébergeable sur GitHub Pages, Netlify, OVH, etc.

## Structure
- `src/pages/*.html` : contenu des pages (accueil, rendez-vous, recrutement, mentions légales) avec un bloc `<!-- meta -->`.
- `src/articles/*.html` : contenu des articles (voir `src/articles/BRIEF.md` pour la charte SEO).
- `build.py` : assemble en-tête, pied de page, données structurées (JSON-LD), sommaire des articles, index des actualités, `sitemap.xml` et `robots.txt`.
- `assets/` : `style.css`, `main.js`, favicon, image de partage, portrait.
- `src/icons/` : icônes Lucide (licence ISC). Dans les pages, écrire `<i data-i="nom-icone"></i>` : le build remplace par le SVG.

## Modifier le site
1. Éditer un fichier dans `src/`.
2. Lancer `python build.py` (Python 3, aucune dépendance).
3. Committer les fichiers générés.

Pour ajouter un article : créer `src/articles/<slug>.html` en suivant le BRIEF, relancer le build. Il apparaît automatiquement dans la liste, le sitemap et les « À lire ensuite ».

## Formulaires
Les trois formulaires (contact, rendez-vous, candidature) fonctionnent sans serveur : ils ouvrent un e-mail pré-rempli si aucun service d'envoi n'est configuré. Pour un envoi automatique, ajouter `data-endpoint="https://…"` sur la balise `<form>` (Formspree, Web3Forms, Netlify Forms, Brevo, ou votre propre API). Les données sont envoyées en JSON. Un champ pot de miel (`website`) bloque les robots.

## À compléter avant mise en ligne
- `src/pages/mentions-legales.html` : champs entre crochets (SIREN, n° ORIAS, hébergeur, RC pro).
- Photo de Mickaël : `assets/mickael-thiollier.webp` (récupérée du site actuel, 283 px). Remplacer par une version plus grande si disponible.
- Adresse du domaine dans `build.py` (`SITE`) si différent de mthiollierconseils.fr.
- Lien Calendly (`CALENDLY` dans `build.py` et dans les pages) et avis Google (lien « voir la fiche »).

## SEO
Chaque page : title (< 60 car.), meta description, canonical, Open Graph, JSON-LD (FinancialService, Article, FAQPage, BreadcrumbList, JobPosting, Blog). Articles de 1 800 à 2 300 mots, mot-clé dans title/h1/intro/h2/URL, tableau, FAQ, maillage interne, sources officielles. Lighthouse : aucune dépendance JS externe, polices Google uniquement.

## Photos
Les photos d'articles et les bandeaux viennent d'Unsplash (licence gratuite, photos non « Unsplash+ »), chargées depuis leur CDN. Les identifiants sont dans `PHOTOS` en haut de `build.py`. Si une photo ne charge pas, un visuel de couleur prend le relais.

## Envoi des formulaires (SMTP)

Les formulaires (rendez-vous, contact, candidature) envoient leurs données à `/api/send` (fonction Vercel, `api/send.js`).
Dans Vercel > Settings > Environment Variables, renseigner :

- `SMTP_HOST`, `SMTP_PORT` (465 ou 587), `SMTP_USER`, `SMTP_PASS`
- `MAIL_TO` : la boîte qui reçoit les demandes (ex. mickael@mthiollierconseils.fr)
- `MAIL_FROM` (optionnel)

Puis redéployer. Tant que ces variables sont absentes, le formulaire affiche un message d'erreur au lieu de confirmer l'envoi.
