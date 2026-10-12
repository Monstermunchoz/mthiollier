# Brief rédaction — articles "Actualités & conseils" du site M. Thiollier Conseils

Site : cabinet indépendant de conseil en gestion de patrimoine (Mickaël Thiollier, CIF / ORIAS / CNCEF, 1000 Grande Rue, 01700 Miribel, près de Lyon). Clientèle : particuliers, cadres, dirigeants, TNS, professions libérales, retraités. Premier entretien offert (1h30). Rendez-vous : page `/rendez-vous.html`.

## Format de sortie (STRICT)

Un fichier par article : `/home/claude/mthiollier/actualites/_src/<slug>.html`, encodage UTF-8, **fragment HTML uniquement** (pas de doctype, html, head, body, header, footer, pas de `<style>`, pas de `<script>`). Le fragment est assemblé automatiquement dans le gabarit du site.

Structure exacte :

```
<!-- meta
title: <balise title, 50-60 caractères, mot-clé principal AU DÉBUT, contient un chiffre ET un mot fort (guide, complet, erreurs, simple, 2026…)>
description: <meta description 140-155 caractères, contient le mot-clé, incitation à l'action>
keyword: <mot-clé principal exact>
date: <2026-MM-JJ entre 2026-06-01 et 2026-10-10>
category: <Épargne | Fiscalité | Immobilier | Retraite | Transmission | Entreprise | Méthode>
reading: <N min>
excerpt: <1 phrase de 120-160 caractères pour la carte de la liste>
-->
<h1>…</h1>   (contient le mot-clé, peut différer du title, 1 seul h1)
<p class="lede">… (chapô 2-3 phrases, le mot-clé apparaît dans les 100 premiers mots)</p>
<h2 id="…">…</h2>  (6 à 9 sections h2, ids en kebab-case ; au moins un h2 contient le mot-clé)
<p>…</p> <h3>…</h3> <ul><li>…</li></ul> …
<table> … </table>   (au moins 1 tableau chiffré : plafonds, taux, comparatif)
<aside class="callout"><strong>À retenir</strong> …</aside>  (1 à 2 encadrés)
<blockquote>… (1 citation courte du conseiller, ton humain)</blockquote>
<h2 id="faq">Questions fréquentes</h2>
<details><summary>Question ?</summary><p>Réponse.</p></details>  (4 à 6 questions, formulées comme les gens les tapent sur Google)
```

## Règles SEO (objectif score 100 RankMath)
- Longueur : **1 800 à 2 300 mots** de corps (hors FAQ).
- Mot-clé principal : dans le title (début), dans la description, dans le h1, dans le premier paragraphe, dans ≥1 h2, densité 0,8 à 1,3 %. Utiliser aussi 3-5 variantes sémantiques.
- Paragraphes courts (2-4 phrases). Phrases ≤ 25 mots en moyenne. Voix active. Ton : expert, clair, humain, jamais vendeur ni "bateau". Pas de jargon non expliqué. Pas de tirets cadratins en aparté, pas de "il est à noter que".
- Liens internes (obligatoires, chemins relatifs depuis /actualites/) : au moins 3 parmi
  - `../rendez-vous.html` (CTA naturel dans le texte, texte d'ancre descriptif),
  - `../index.html#expertises`, `../index.html#simulateur`, `../index.html#methode`,
  - 2 autres articles de la liste ci-dessous (`<a href="<slug>.html">`).
- Liens externes (1 à 3) vers des sources officielles, ouverts dans un nouvel onglet : impots.gouv.fr, service-public.fr, amf-france.org, legifrance.gouv.fr, economie.gouv.fr, urssaf.fr, banque-france.fr. Attribut `target="_blank" rel="noopener"`.
- Chiffres : vérifier via recherche web les montants 2026 (plafonds, abattements, taux, PFU, barème). Si un chiffre n'est pas vérifiable, le présenter comme ordre de grandeur et renvoyer à la source officielle. Ne jamais inventer un rendement précis ; parler de fourchettes historiques et rappeler le risque de perte en capital.
- Conclure par une section h2 "Ce que je vous conseille" (à la première personne, Mickaël) avec 3-4 points et un lien vers `../rendez-vous.html`.
- Un seul `<h1>`. Aucune image (le gabarit ajoute un visuel). Aucun script. Français impeccable, typographie française (espaces insécables avant : ; ? ! via `&nbsp;`, guillemets « »).

## Liste des 10 articles (slug → mot-clé principal → angle)
1. `per-plan-epargne-retraite-guide-2026` → "PER" (plan d'épargne retraite) → fonctionnement, plafond de déduction 2026, sortie capital/rente, pour qui, erreurs.
2. `assurance-vie-fiscalite-apres-8-ans` → "fiscalité de l'assurance-vie" → avant/après 8 ans, abattement 4 600/9 200 €, PFU, 150 000 €, transmission 152 500 €, clause bénéficiaire.
3. `investir-en-scpi-guide-complet` → "investir en SCPI" → fonctionnement, frais, rendement historique, fiscalité, direct vs assurance-vie, crédit, risques de liquidité.
4. `reduire-ses-impots-7-leviers-legaux` → "réduire ses impôts" → PER, déficit foncier, FCPI/FIP, dons, emploi à domicile, Denormandie, LMNP ; tableau réduction vs déduction.
5. `placer-tresorerie-entreprise` → "placer la trésorerie de son entreprise" → compte à terme, contrat de capitalisation, SCPI via société, usufruit de SCPI, fiscalité IS, horizon.
6. `transmettre-son-patrimoine-donation-demembrement` → "transmettre son patrimoine" → abattements 100 000 € / 15 ans, donation-partage, démembrement, assurance-vie, barème des droits.
7. `lmnp-location-meublee-2026` → "LMNP" (loueur en meublé non professionnel) → micro-BIC vs réel, amortissement, réforme plus-values, seuils 2026, résidences services.
8. `preparer-sa-retraite-a-40-ans` → "préparer sa retraite" → taux de remplacement, calcul de l'effort d'épargne, PER vs assurance-vie vs immobilier, tableau d'effort mensuel selon l'âge.
9. `conseiller-gestion-patrimoine-independant-ou-banque` → "conseiller en gestion de patrimoine indépendant" → différences, statuts CIF/ORIAS, rémunération honoraires vs commissions, DER, questions à poser.
10. `investissement-responsable-isr-labels` → "investissement responsable" → labels ISR / Greenfin / Finansol, réforme du label ISR, performance, comment en mettre dans une assurance-vie ou un PER, greenwashing.

Auteur de tous les articles : Mickaël Thiollier. Les articles doivent se renvoyer les uns aux autres (maillage).
