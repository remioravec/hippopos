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
- `mentions-legales.html`, `cgu.html`, `confidentialite.html` — pages placeholder,
  contenu réel à rédiger avant le lancement commercial (voir TODO ci-dessous)
- `assets/` — logo et favicon
- `styles.css` — feuille de style unique, palette alignée sur l'application

## À faire avant mise en ligne

- [ ] Rédiger le contenu réel des pages légales (mentions légales, CGU/CGV, confidentialité)
- [ ] Confirmer et ajuster les tarifs (actuellement des valeurs indicatives à valider)
- [ ] Remplacer les liens `https://app.hippopos.fr` par l'URL réelle de l'application
- [ ] Remplacer `contact@hippopos.fr` par une adresse réelle
- [ ] Configurer le domaine (site vitrine sur le domaine racine, app sur un sous-domaine)
- [ ] **Retirer `noindex` (robots.txt + balise meta sur `index.html`) une fois prêt pour le référencement** —
      l'indexation est désactivée volontairement tant que le site n'est pas finalisé
