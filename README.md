# Hippopos — Site vitrine

Site public de présentation de Hippopos, séparé de l'application (`app.hippopos.fr`).
HTML/CSS statique, aucun build ni dépendance — sert directement les fichiers tels quels.

## Développement local

```bash
python3 -m http.server 4173
```

Puis ouvrir http://localhost:4173

## Structure

- `index.html` — page d'accueil (fonctionnalités, multi-magasins, tarifs, FAQ)
- `logiciel-de-caisse/`, `fonctionnalites/`, `nf525/`, `tarifs/` — les 4 hubs de silo
- `logiciel-de-caisse/{metier}/` — les pages métier (8 publiées, 10 à venir)
- `tools/build.py` + `tools/pages.py` — génèrent les pages de l'arbre. Le HTML
  produit est commité : l'hébergement sert toujours des fichiers statiques.
  Régénérer après toute modification de `tools/pages.py` : `python3 tools/build.py`
- `menu.js` — menu mobile, partagé par toutes les pages
- `vercel.json` — redirection www → apex, en-têtes de sécurité et de cache
- `sitemap.xml` — 13 URL, écrit à la main (automatisation prévue en septembre)
- `mentions-legales.html`, `cgu.html`, `confidentialite.html` — pages placeholder,
  contenu réel à rédiger avant le lancement commercial (voir TODO ci-dessous)
- `assets/` — logo et favicon
- `styles.css` — feuille de style unique, palette alignée sur l'application

## À faire avant mise en ligne

**Bloquants — l'indexation est désormais ouverte, ces points doivent être traités
avant que le site soit réellement mis en avant :**

- [ ] Rédiger le contenu réel des pages légales (mentions légales, CGU/CGV, confidentialité)
      — un site commercial indexé sans mentions légales n'est pas conforme
- [ ] Confirmer et ajuster les tarifs — la page d'accueil affiche encore
      « Tarifs indicatifs », ce qui ne doit pas rester en ligne face à un prospect
- [ ] Fournir le justificatif NF525 (numéro de certificat ou modèle d'attestation
      individuelle) et arrêter la formulation exacte employée sur `/nf525/`
- [ ] Remplacer `contact@hippopos.fr` par une adresse réelle

**Reste à faire :**

- [ ] Remplacer les liens `https://app.hippopos.fr` par l'URL réelle de l'application
- [ ] Configurer le domaine : `hippopos.fr` en apex (retenu), `www` redirigé en 301
      par `vercel.json` — à vérifier une fois le DNS en place
- [ ] Fournir les captures produit et les chiffres de parc : tout ce qui manque
      apparaît **surligné en jaune** sur les pages, jamais comblé par une valeur inventée

## Fait — tickets de lancement d'août 2026

- [x] `robots.txt` ouvert à l'indexation, sitemap déclaré
- [x] `noindex` retiré de la page d'accueil (conservé sur les 3 pages légales)
- [x] `sitemap.xml` publié (13 URL)
- [x] Domaine unique : canonical vers l'apex, redirection 301 du `www`
- [x] Title et meta description de l'accueil réécrits
- [x] JSON-LD posé : Organization, SoftwareApplication, FAQPage, BreadcrumbList
- [x] 12 pages de l'arbre publiées (4 hubs + 8 métiers)

Restent à la charge de l'éditeur, hors dépôt : Search Console et Bing Webmaster
Tools, conteneur GTM, propriété GA4, les 6 événements de conversion, la mesure
inter-domaines avec `app.hippopos.fr` et le bandeau de consentement.
