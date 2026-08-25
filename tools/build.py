#!/usr/bin/env python3
"""Génère les pages de l'arbre Hippopos à partir des gabarits et de pages.py.

Le site reste servi tel quel — aucun build à l'hébergement. Ce script produit du
HTML statique commité dans le dépôt : Vercel continue de servir des fichiers, et
les 101 pages de la roadmap ne se recopient pas à la main.

    python3 tools/build.py

Gabarits, dans l'ordre des maquettes SXO du 15/08/2026 :
  · hub de silo    — fil d'Ariane, hero, grille des filles, socle commun, FAQ, CTA
  · unité d'achat  — fil d'Ariane, hero, signature métier, preuve, couvert/non
                     couvert, déclinaisons, sœurs, CTA
  · page tarifs    — fil d'Ariane, hero, formules, ce que le prix ne dit pas, FAQ
"""
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from icones import ico  # noqa: E402
from pages import (  # noqa: E402
    METIERS, METIERS_COUVERTS, FAQ_SILO_METIERS, FONCTIONS, FONCTIONS_PUBLIEES,
    PEURS, FONCTIONS_DETAIL, CAS, VARIANTES_EXEMPLE, PEURS_HUB,
)

RACINE = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://hippopos.fr"
APP = "https://app.hippopos.fr"

SILOS = [
    ("/logiciel-de-caisse/", "Métiers"),
    ("/fonctionnalites/", "Fonctionnalités"),
    ("/nf525/", "Conformité NF525"),
    ("/tarifs/", "Tarifs"),
]


# --------------------------------------------------------------------------
# Briques communes
# --------------------------------------------------------------------------
def head(titre, desc, url, blocs_ld, profondeur):
    """En-tête commun. `profondeur` donne le préfixe vers la racine."""
    r = "../" * profondeur
    ld = "\n".join(
        '  <script type="application/ld+json">\n'
        + json.dumps(b, ensure_ascii=False, indent=2)
        + "\n  </script>"
        for b in blocs_ld
    )
    return f"""<!doctype html>
<html lang="fr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{titre}</title>
  <meta name="description" content="{desc}" />
  <link rel="icon" type="image/svg+xml" href="{r}assets/favicon.svg" />
  <link rel="canonical" href="{BASE}{url}" />

  <meta property="og:type" content="website" />
  <meta property="og:url" content="{BASE}{url}" />
  <meta property="og:site_name" content="Hippopos" />
  <meta property="og:title" content="{titre}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:locale" content="fr_FR" />

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link
    href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&display=swap"
    rel="stylesheet"
  />
  <link rel="stylesheet" href="{r}styles.css" />
{ld}
</head>"""



CHEVRON = ('<svg class="chev" width="13" height="13" viewBox="0 0 24 24" fill="none"'
           ' stroke="currentColor" stroke-width="2.4" stroke-linecap="round"'
           ' stroke-linejoin="round" aria-hidden="true">'
           '<polyline points="6 9 12 15 18 9"></polyline></svg>')


def _axes(base):
    """Le contenu des deux axes, partagé par le méga-menu et le menu mobile.

    Un seul jeu de données pour les deux surfaces : ce qui s'ouvre au doigt dit
    exactement ce qui s'ouvre à la souris. Les métiers sans page publiée sont
    listés sans lien — le menu dit l'offre, pas l'état de production.
    """
    return [
        ("metiers", "Métiers", f"{base}/logiciel-de-caisse/",
         "Logiciel de caisse pour commerce de détail",
         [(f"{base}/logiciel-de-caisse/{sl}/" if pub else None,
           "m-" + sl if ico("m-" + sl) else "m-generique", lab)
          for sl, lab, pub in METIERS_COUVERTS]),
        ("fonctionnalites", "Fonctionnalités", f"{base}/fonctionnalites/",
         "Les fonctionnalités d'un logiciel de caisse",
         [(f"{base}/fonctionnalites/#{i}", i, t) for i, t, _ in BRIQUES + ADDONS]),
    ]


def mega_menu(profondeur):
    """Méga-menu de bureau — les deux colonnes du modèle, ouvertes par le chevron."""
    base = ("../" * profondeur).rstrip("/") or "."
    colonnes = []
    for _, titre, url_mere, libelle_mere, items in _axes(base):
        lignes = "\n".join(
            f'            <a href="{u}">{ico(i)}{lab}</a>' if u
            else f'            <span>{ico(i)}{lab}</span>'
            for u, i, lab in items
        )
        colonnes.append(f"""          <div>
            <h4>{titre}</h4>
            <a class="mega-mere" href="{url_mere}">{libelle_mere}</a>
            <div class="mega-liste">
{lignes}
            </div>
          </div>""")
    return f"""
      <div class="mega" id="mega" data-ouvert="false">
{chr(10).join(colonnes)}
          <p class="mega-note">
            Conformité et tarifs : <a href="{base}/nf525/">logiciel de caisse certifié</a> ·
            <a href="{base}/tarifs/">prix d'un logiciel de caisse</a>
          </p>
      </div>"""


def menu_mobile(profondeur):
    """Menu mobile — même arborescence que le méga-menu, en accordéon.

    Le libellé reste un lien vers la mère ; c'est le chevron, cible de 44 px,
    qui déplie la liste. Sans cela, les 18 métiers et les 10 fonctions étaient
    inatteignables au doigt : le menu mobile s'arrêtait aux quatre axes.
    """
    base = ("../" * profondeur).rstrip("/") or "."
    sous = {"/logiciel-de-caisse/": "metiers", "/fonctionnalites/": "fonctionnalites"}
    contenus = {cle: items for cle, _, _, _, items in _axes(base)}
    lignes = []
    for u, lab in SILOS:
        cle = sous.get(u)
        if cle:
            items = contenus[cle]
            liste = "\n".join(
                f'          <a href="{lu}">{ico(i)}{l}</a>' if lu
                else f'          <span>{ico(i)}{l}</span>'
                for lu, i, l in items
            )
            lignes.append(f"""      <div class="m-groupe">
        <div class="m-ligne">
          <a href="{base}{u}">{lab}</a>
          <button type="button" class="m-plus" data-sous="m-{cle}"
                  aria-expanded="false" aria-controls="m-{cle}"
                  aria-label="Afficher les {lab.lower()}">{CHEVRON}</button>
        </div>
        <div class="m-sous" id="m-{cle}" hidden>
{liste}
        </div>
      </div>""")
        else:
            lignes.append(f'      <a href="{base}{u}">{lab}</a>')
    return "\n".join(lignes)


def entete(profondeur, actif=""):
    r = "../" * profondeur
    AXES = {"/logiciel-de-caisse/", "/fonctionnalites/"}
    liens = "\n".join(
        (f'        <a href="{r.rstrip("/") or "."}{u}" class="mega-btn"'
         f' data-mega aria-expanded="false" aria-controls="mega"'
         + (' aria-current="page"' if u == actif else "")
         + f">{lab}{CHEVRON}</a>"
         if u in AXES else
         f'        <a href="{r.rstrip("/") or "."}{u}"'
         + (' aria-current="page"' if u == actif else "")
         + f">{lab}</a>")
        for u, lab in SILOS
    )
    return f"""<body>
  <header class="site-header">
    <div class="container">
      <a href="{r or "/"}" class="brand">
        <img src="{r}assets/hippopos-logo.png" alt="Hippopos" style="height: 40px;" />
      </a>
      <nav class="main-nav">
{mega_menu(profondeur)}
{liens}
      </nav>
      <div class="header-actions">
        <a href="{APP}" class="btn btn-ghost">Se connecter</a>
        <a href="{APP}/inscription" class="btn btn-cta">Essayer gratuitement</a>
        <button
          type="button"
          class="nav-toggle"
          id="navToggle"
          aria-label="Ouvrir le menu"
          aria-expanded="false"
          aria-controls="mobileNav"
        >
          <span></span><span></span><span></span>
        </button>
      </div>
    </div>
    <nav class="mobile-nav" id="mobileNav">
{menu_mobile(profondeur)}
      <a href="{APP}">Se connecter</a>
      <a href="{APP}/inscription" class="btn btn-cta">Essayer gratuitement</a>
    </nav>
  </header>"""


def ariane(items, profondeur):
    """items : [(libellé, url ou None pour la page courante)]"""
    r = "../" * profondeur
    li = []
    for lab, u in items:
        if u is None:
            li.append(f'        <li aria-current="page">{lab}</li>')
        else:
            href = (r.rstrip("/") or ".") + u if u != "/" else (r or "/")
            li.append(f'        <li><a href="{href}">{lab}</a></li>')
    return f"""
  <nav class="breadcrumb container" aria-label="Fil d'Ariane">
    <ol>
{chr(10).join(li)}
    </ol>
  </nav>"""


def bande_cta(titre, texte, libelle="Essayer gratuitement"):
    return f"""
    <section>
      <div class="container">
        <div class="cta-band">
          <h2>{titre}</h2>
          <p>{texte}</p>
          <a href="{APP}/inscription" class="btn btn-light">{libelle}</a>
        </div>
      </div>
    </section>"""


def pied(profondeur):
    r = "../" * profondeur
    base = r.rstrip("/") or "."
    silos = "\n".join(
        f'            <li><a href="{base}{u}">{lab}</a></li>' for u, lab in SILOS
    )
    metiers = "\n".join(
        f'            <li><a href="{base}/logiciel-de-caisse/{s}/">{lab}</a></li>'
        for s, lab, publie in METIERS_COUVERTS if publie
    )
    return f"""
  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-brand">
          <a href="{r or "/"}" class="brand">
            <img src="{r}assets/hippopos-logo.png" alt="Hippopos" style="height: 32px;" />
          </a>
          <p>Le logiciel de caisse pensé pour le commerce indépendant, du comptoir au multi-magasins.</p>
        </div>
        <div class="footer-col">
          <h4>Produit</h4>
          <ul>
{silos}
            <li><a href="{APP}">Se connecter</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4>Métiers</h4>
          <ul>
{metiers}
          </ul>
        </div>
        <div class="footer-col">
          <h4>Légal</h4>
          <ul>
            <li><a href="{base}/mentions-legales.html">Mentions légales</a></li>
            <li><a href="{base}/cgu.html">CGU / CGV</a></li>
            <li><a href="{base}/confidentialite.html">Confidentialité</a></li>
            <li><a href="mailto:contact@hippopos.fr">Contact</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <span>© 2026 Hippopos. Tous droits réservés.</span>
        <span>Fait pour les commerçants, par des commerçants.</span>
      </div>
    </div>
  </footer>

  <script src="{r}menu.js" defer></script>
</body>
</html>
"""


def ld_ariane(url, items):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "@id": f"{BASE}{url}#ariane",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": lab, "item": f"{BASE}{u}"}
            for i, (lab, u) in enumerate(items)
        ],
    }


def bloc_faq(questions, titre, chapeau=""):
    items = "\n".join(
        f"""          <details class="faq-item">
            <summary>{q}</summary>
            <p>{r}</p>
          </details>"""
        for q, r in questions
    )
    ch = f"\n          <p>{chapeau}</p>" if chapeau else ""
    return f"""
    <section id="faq">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">Questions fréquentes</span>
          <h2>{titre}</h2>{ch}
        </div>
        <div class="faq-list">
{items}
        </div>
      </div>
    </section>"""


def ld_faq(questions):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": r},
            }
            for q, r in questions
        ],
    }


def ecrire(chemin, contenu):
    f = RACINE / chemin
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(contenu, encoding="utf-8")
    return chemin


# --------------------------------------------------------------------------
# Gabarit — unité d'achat (page métier)
# --------------------------------------------------------------------------
def faq_metier(nom):
    """Deux questions seulement, qui portent les liens vers les guides. Placées
    après la bande de conversion : elles ne détournent personne."""
    return [
        (f"Combien coûte un logiciel de caisse pour une {nom} ?",
         "Entre 29 et 69 € HT par mois selon le nombre de vendeurs et de magasins, "
         "sans matériel à acheter et sans engagement. Le détail poste par poste est "
         'sur la page <a href="../../tarifs/">prix d\'un logiciel de caisse</a>.'),
        (f"Une caisse de {nom} doit-elle être conforme NF525 ?",
         "Oui, dès lors que le commerce est assujetti à la TVA et encaisse des "
         "particuliers. Les quatre exigences et la façon de les vérifier sont "
         'détaillées sur la page <a href="../../nf525/">logiciel de caisse certifié</a>.'),
    ]


# --------------------------------------------------------------------------
# Gabarit — sections d'une page métier : peurs, puis fonctionnalités
# --------------------------------------------------------------------------
# Le modèle Combo pose une alternance texte / visuel, une section par
# fonctionnalité. Les visuels sont construits en HTML : aucune capture, aucun
# écran inventé qui vieillirait mal — un panneau sobre, marqué « Exemple », qui
# montre la donnée dont parle la section.

def grille_peurs(peurs, eyebrow, titre):
    """Trois contraintes illustrées — au lieu d'un paragraphe centré."""
    cartes = "\n".join(
        f"""          <div class="peur-card">
            <div class="peur-ico">{ico(i)}</div>
            <h3>{t}</h3>
            <p>{txt}</p>
          </div>"""
        for i, t, txt in peurs
    )
    return f"""    <!-- Peurs et frustrations · 0 lien -->
    <section>
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">{eyebrow}</span>
          <h2>{titre}</h2>
        </div>
        <div class="peur-grid">
{cartes}
        </div>
      </div>
    </section>
"""


def bloc_peurs(slug, nom):
    return grille_peurs(PEURS[slug], "Ce qui coince au comptoir",
                        f"Les trois contraintes d'une caisse de {nom}")


def _ligne_panneau(gauche, droite, sous="", ton=""):
    s = f'<span class="p-sub">{sous}</span>' if sous else ""
    return (f'            <div class="p-ligne{ton}">'
            f'<div><span class="p-nom">{gauche}</span>{s}</div>'
            f'<span class="p-val">{droite}</span></div>')


def panneau(cle, slug, m):
    """Le visuel d'une section de fonctionnalité — construit, jamais capturé."""
    lignes_ticket = m["ticket"][1]

    if cle == "vente-au-poids":
        n, sub, prix = next((l for l in lignes_ticket if " kg × " in l[1]), lignes_ticket[0])
        poids, tarif = (sub.split(" × ") + [""])[:2]
        corps = f"""            <div class="p-balance">
              <span class="p-poids">{poids}</span>
              <span class="p-tarif">{tarif}</span>
            </div>
{_ligne_panneau(n, prix, "Ligne créée par la balance")}"""
        return _panneau("Balance connectée", corps)

    if cle == "variantes-produit":
        produit, variantes = VARIANTES_EXEMPLE[slug]
        puces = "\n".join(_ligne_panneau(v, p) for v, p in variantes)
        return _panneau("Fiche produit",
                        f'            <div class="p-mere">{produit}</div>\n{puces}')

    if cle == "gestion-de-stock":
        n1, n2, n3 = [l[0] for l in lignes_ticket]
        corps = "\n".join([
            _ligne_panneau(n1, "24", "En rayon"),
            _ligne_panneau(n2, "2,4 kg", "Seuil d'alerte atteint", " est-alerte"),
            _ligne_panneau(n3, "31", "En rayon"),
        ])
        return _panneau("Stock", corps)

    if cle == "inventaire-guide":
        n1, n2, n3 = [l[0] for l in lignes_ticket]
        corps = "\n".join([
            _ligne_panneau(n1, "= 0", "Théorique 24 · compté 24"),
            _ligne_panneau(n2, "− 3", "Théorique 15 · compté 12", " est-alerte"),
            _ligne_panneau(n3, "= 0", "Théorique 31 · compté 31"),
        ])
        return _panneau("Inventaire en cours", corps)

    if cle == "cloture-de-caisse":
        corps = "\n".join([
            _ligne_panneau("Espèces", "312,40 €"),
            _ligne_panneau("Carte bancaire", "1 048,60 €"),
            _ligne_panneau("Fond de caisse compté", "150,00 €"),
            _ligne_panneau("Écart", "0,00 €", "", " est-ok"),
        ])
        return _panneau("Clôture du jour", corps)

    if cle == "comptes-vendeurs":
        corps = "\n".join([
            _ligne_panneau("Responsable", "Tous les droits", "Remises · annulations · clôtures"),
            _ligne_panneau("Vendeur", "Encaissement", "Ouverture au code PIN"),
            _ligne_panneau("Extra", "Encaissement", "Ni réglages ni chiffres du magasin"),
        ])
        return _panneau("Comptes ouverts", corps)

    if cle == "multi-magasins":
        corps = "\n".join([
            _ligne_panneau("Magasin 1", "24", "Stock propre"),
            _ligne_panneau("Magasin 2", "3", "Stock propre", " est-alerte"),
            _ligne_panneau("Transfert de 6 pièces", "Envoyé", "À recevoir côté magasin 2"),
        ])
        return _panneau("Catalogue centralisé", corps)

    if cle == "etiquettes":
        n = lignes_ticket[0][0]
        corps = f"""            <div class="p-etiquette">
              <span class="p-etiq-nom">{n}</span>
              <span class="p-etiq-prix">{lignes_ticket[0][2]}</span>
              <span class="p-codebarres" aria-hidden="true"></span>
              <span class="p-sub">Code produit généré par la fiche</span>
            </div>"""
        return _panneau("Étiquette à imprimer", corps)

    if cle == "cheques-cadeaux":
        corps = "\n".join([
            _ligne_panneau("Montant émis", "50,00 €"),
            _ligne_panneau("Première utilisation", "− 27,50 €"),
            _ligne_panneau("Solde restant", "22,50 €", "Suivi par la caisse", " est-ok"),
        ])
        return _panneau("Chèque cadeau · code unique", corps)

    if cle == "conformite":
        corps = "\n".join([
            _ligne_panneau("Vente n° 1 042", "12:04:38", "Horodatée à l'enregistrement"),
            _ligne_panneau("Chaînée à la vente", "n° 1 041", "Lien conservé"),
            _ligne_panneau("Contrôle d'intégrité", "Conforme", "", " est-ok"),
        ])
        return _panneau("Journal des ventes", corps)

    if cle == "ticket":
        entete, lignes, total = m["ticket"]
        rangs = "\n".join(
            f"""              <div class="hero-product-row">
                <div>
                  <div class="name">{n}</div>
                  <div class="sub">{sub}</div>
                </div>
                <div class="price">{prix}</div>
              </div>"""
            for n, sub, prix in lignes)
        return f"""          <div class="hero-card">
            <div class="hero-card-header">
              <strong>{entete}</strong>
              <span>Ticket en cours</span>
            </div>
            <div class="hero-card-body">
{rangs}
            </div>
            <div class="hero-total">
              <span>Total TTC</span>
              <span>{total}</span>
            </div>
          </div>"""

    if cle == "fidelite":
        corps = "\n".join([
            _ligne_panneau("Mécanique choisie", "Carte à tampons"),
            _ligne_panneau("Compteur du client", "7 / 10"),
            _ligne_panneau("Récompense", "Au 10e passage", "", " est-ok"),
        ])
        return _panneau("Programme de fidélité", corps)

    return ""


def _panneau(titre, corps):
    return f"""          <div class="panneau">
            <div class="p-tete"><span>{titre}</span><span class="p-tag">Exemple</span></div>
{corps}
          </div>"""


def section_fonction(rang, cle, slug, m, ancre, url):
    """Une fonctionnalité, une section : texte d'un côté, visuel de l'autre."""
    d = FONCTIONS_DETAIL[cle]
    puces = "\n".join(f"            <li>{p}</li>" for p in d["puces"])
    badge = ('<span class="p-tag p-addon">Activable à la demande</span>'
             if d["addon"] else "")
    inverse = " est-inverse" if rang % 2 else ""
    fond = " bande" if rang % 2 else ""
    return f"""    <section class="fonction{inverse}{fond}">
      <div class="container">
        <div class="fonction-texte">
          <span class="eyebrow">{ico(ICO_FONCTION.get(cle, ""))} Fonctionnalité {rang + 1}</span>
          <h3>{d["titre"]} {badge}</h3>
          <p class="fonction-chapeau">{d["chapeau"]}</p>
          <p class="fonction-cas">{CAS[slug][cle]}</p>
          <ul class="check-list">
{puces}
          </ul>
          <p class="lien-fonction-ligne"><a class="lien-fonction" href="{url}">{ancre}</a></p>
        </div>
        <div class="fonction-visuel">
{panneau(cle, slug, m)}
        </div>
      </div>
    </section>
"""


def section_hub_fonction(rang, id_, titre, chapeau, puces, panneau_cle, m, addon=False):
    """Une brique du produit, une section — même gabarit que sur les pages métier.

    L'ancre reste `#id` : les pages métier pointent dessus, et la grille de
    cartes qu'elle remplace la portait déjà.
    """
    liste = "\n".join(f"            <li>{x}</li>" for x in puces)
    badge = ('<span class="p-tag p-addon">Activable à la demande</span>' if addon else "")
    inverse = " est-inverse" if rang % 2 else ""
    fond = " bande" if rang % 2 else ""
    return f"""    <section class="fonction{inverse}{fond}" id="{id_}">
      <div class="container">
        <div class="fonction-texte">
          <span class="eyebrow">{ico(id_)} {"Add-on" if addon else "Brique comprise"}</span>
          <h3>{titre} {badge}</h3>
          <p class="fonction-chapeau">{chapeau}</p>
          <ul class="check-list">
{liste}
          </ul>
        </div>
        <div class="fonction-visuel">
{panneau(panneau_cle, "boulangerie", m)}
        </div>
      </div>
    </section>
"""


ICO_FONCTION = {
    "vente-au-poids": "poids", "variantes-produit": "variantes",
    "gestion-de-stock": "stock", "inventaire-guide": "stock",
    "multi-magasins": "multi-magasins", "fidelite": "fidelite",
    "etiquettes": "etiquettes", "cloture-de-caisse": "clotures",
    "comptes-vendeurs": "equipe", "cheques-cadeaux": "cheques-cadeaux",
}


REASSURANCE = [
    ("conformite", "Conforme <strong>NF525</strong>", "ventes chaînées et horodatées"),
    ("horloge", "<strong>14 jours</strong> d'essai", "sans carte bancaire"),
    ("cadenas", "Sans engagement", "résiliable à tout moment"),
    ("douchette", "Votre matériel <strong>reste en place</strong>", "douchette, balance, imprimante"),
]


def bande_reassurance():
    """Ligne de flottaison — quatre garanties, pas des logos clients.

    Le modèle place ici une rangée de logos. Aucun logo client n'a été fourni :
    en inventer serait faux, alors la bande porte ce qui est vérifiable.
    """
    items = "\n".join(
        f"""        <div class="reassurance-item">
          {ico(i)}
          <span><span class="r-titre">{titre}</span><span class="r-sous">{sous}</span></span>
        </div>"""
        for i, titre, sous in REASSURANCE
    )
    return f"""    <div class="trust-strip">
      <div class="container reassurance">
{items}
      </div>
    </div>
"""


def page_metier(slug):
    m = METIERS[slug]
    url = f"/logiciel-de-caisse/{slug}/"
    nom = m["nom"]
    fil = [("Accueil", "/"), ("Logiciel de caisse", "/logiciel-de-caisse/"),
           (nom.capitalize(), url)]

    ld = [
        ld_ariane(url, fil),
        {
            "@context": "https://schema.org",
            "@type": "Service",
            "name": f"Logiciel de caisse pour {nom}",
            "serviceType": "Logiciel de caisse",
            "provider": {"@id": f"{BASE}/#organisation"},
            "areaServed": {"@type": "Country", "name": "France"},
            "isSimilarTo": {"@id": f"{BASE}/#logiciel"},
            "offers": {"@type": "Offer", "price": "29", "priceCurrency": "EUR",
                       "url": f"{BASE}/tarifs/"},
        },
    ]

    couvert = "\n".join(f"              <li>{x}</li>" for x in m["couvert"])
    absent = "\n".join(f"              <li>{x}</li>" for x in m["absent"])
    note_absent = m.get(
        "absent_note",
        "Dire ce que le produit ne fait pas évite les essais qui n'aboutissent pas.",
    )

    soeurs = "\n".join(
        f"""          <a class="link-card" href="../{s}/">
            {ico("m-" + s)}
            <strong>Logiciel de caisse {METIERS[s]["nom"]}</strong>
            <span>{METIERS[s]["signature_titre"]}</span>
          </a>"""
        for s in m["soeurs"]
    )

    def cible_fonction(cle):
        ancre, slug_page, section = FONCTIONS[cle]
        url = (f"../../fonctionnalites/{slug_page}/" if cle in FONCTIONS_PUBLIEES
               else f"../../fonctionnalites/#{section}")
        return ancre, url

    fonctions = "\n".join(
        section_fonction(rang, c, slug, m, *cible_fonction(c))
        for rang, c in enumerate(m["croisements"])
    )

    photo_src = m.get("photo")
    photo = (f'        <figure class="hero-visuel">\n'
             f'          <img class="hero-photo" src="../../assets/{photo_src}"\n'
             f'               alt="{m.get("photo_alt", "")}" width="1200" height="900" />\n'
             f'        </figure>\n'
             if photo_src else "")

    ticket_entete, lignes_ticket, ticket_total = m["ticket"]
    lignes = "\n".join(
        f"""              <div class="hero-product-row">
                <div>
                  <div class="name">{n}</div>
                  <div class="sub">{sub}</div>
                </div>
                <div class="price">{prix}</div>
              </div>"""
        for n, sub, prix in lignes_ticket
    )

    corps = f"""
  <main>
    <!-- 1. Hero — USP et réassurance · 0 lien interne -->
    <section class="page-hero hero-metier-page">
      <div class="container">
        <div class="hero-mots">
          <span class="tag-metier">{ico("m-" + slug) if ico("m-" + slug) else ico("m-generique")}{m["famille"]}</span>
          <h1>{m["h1"]}</h1>
          <p class="lede">{m["lede"]}</p>
          <div class="hero-cta-row">
            <a href="{APP}/inscription" class="btn btn-cta">Essayer 14 jours</a>
          </div>
          <p class="hero-note">Sans engagement · Sans carte bancaire · Votre matériel reste en place</p>
        </div>
{photo}      </div>
    </section>

    <!-- 2. Réassurance — ligne de flottaison · 0 lien -->
{bande_reassurance()}
{bloc_peurs(slug, nom)}
    <!-- 4. Fonctionnalités — une section par fonction · 3 liens -->
    <section class="fonctions-tete">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">{m["signature_titre"]}</span>
          <h2>Ce qu'une caisse de {nom} doit savoir faire</h2>
          <p>{m["signature"]}</p>
        </div>
      </div>
    </section>
{fonctions}
    <!-- 4 bis. Le ticket — ce que la caisse produit · 0 lien -->
    <section class="fonction est-inverse bande">
      <div class="container">
        <div class="fonction-texte">
          <span class="eyebrow">{ico("tickets")} Le ticket</span>
          <h3>Pièce, poids et part sur le même ticket</h3>
          <p class="fonction-chapeau">Le détail que le client attend, et la trace que
             l'administration peut demander : c'est le même document.</p>
          <ul class="check-list">
            <li>Imprimé sur l'imprimante thermique en place, ou envoyé par email</li>
            <li>Logo et coordonnées du magasin repris de votre fiche</li>
            <li>Chaque vente chaînée et horodatée, conforme NF525</li>
          </ul>
        </div>
        <div class="fonction-visuel">
          <div class="hero-card">
            <div class="hero-card-header">
              <strong>{ticket_entete}</strong>
              <span>Ticket en cours</span>
            </div>
            <div class="hero-card-body">
{lignes}
            </div>
            <div class="hero-total">
              <span>Total TTC</span>
              <span>{ticket_total}</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 5. Axe sœur · 2 liens métier + 1 vers la mère -->
    <section>
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">Métiers proches</span>
          <h2>Les autres métiers de comptoir</h2>
          <p>Vous cherchez un autre commerce ? Voir les 18 métiers que couvre le
             <a href="../">logiciel de caisse pour commerce de détail</a>.</p>
        </div>
        <div class="link-grid">
{soeurs}
        </div>
      </div>
    </section>

    <!-- 6. E-E-A-T — ce qui est couvert, et ce qui ne l'est pas -->
    <section class="bande">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">Ce que couvre Hippopos</span>
          <h2>Ce que fait Hippopos en {nom}</h2>
        </div>
        <div class="coverage">
          <div class="coverage-col coverage-yes">
            <h3>Couvert</h3>
            <ul>
{couvert}
            </ul>
          </div>
          <div class="coverage-col coverage-no">
            <h3>Non couvert aujourd'hui</h3>
            <ul>
{absent}
            </ul>
            <p class="coverage-note">{note_absent}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- 7. Step by step — comment ça se met en place · 0 lien -->
    <section>
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">Mise en route</span>
          <h2>Opérationnel dès le prochain service</h2>
        </div>
        <div class="steps">
          <div class="step">
            <div class="step-number">1</div>
            <h3>Créez votre compte</h3>
            <p>Aucune carte bancaire pour l'essai, aucun matériel à commander.</p>
          </div>
          <div class="step">
            <div class="step-number">2</div>
            <h3>Importez votre catalogue</h3>
            <p>Produits, catégories et prix — un par un ou en une fois.</p>
          </div>
          <div class="step">
            <div class="step-number">3</div>
            <h3>Branchez votre balance</h3>
            <p>Le poids remonte en caisse, plus aucun montant à ressaisir.</p>
          </div>
          <div class="step">
            <div class="step-number">4</div>
            <h3>Encaissez</h3>
            <p>Sur tablette, ordinateur ou votre terminal tactile existant.</p>
          </div>
        </div>
      </div>
    </section>
{bande_cta(f"Voir Hippopos en {nom}",
           "14 jours d'essai, sans carte bancaire, votre catalogue importé en une fois.")}
{bloc_faq(faq_metier(nom), f"Les questions qu'on nous pose en {nom}")}
  </main>"""

    html = (head(m["title"], m["desc"], url, ld, 2)
            + entete(2, "/logiciel-de-caisse/")
            + ariane(fil[:-1] + [(nom.capitalize(), None)], 2)
            + corps + pied(2))
    return ecrire(f"logiciel-de-caisse/{slug}/index.html", html)


# --------------------------------------------------------------------------
# Gabarit — hub de silo
# --------------------------------------------------------------------------
def page_hub(url, titre, desc, h1, lede, eyebrow, sections, faq, faq_titre,
             nom_ld, profondeur=1, faq_chapeau="", titre_peurs=""):
    fil = [("Accueil", "/"), (eyebrow, url)]
    ld = [
        ld_ariane(url, fil),
        {
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "name": nom_ld,
            "url": f"{BASE}{url}",
            "isPartOf": {"@id": f"{BASE}/#organisation"},
            "breadcrumb": {"@id": f"{BASE}{url}#ariane"},
        },
        ld_faq(faq),
    ]
    corps = f"""
  <main>
    <section class="page-hero">
      <div class="container">
        <span class="eyebrow">{eyebrow}</span>
        <h1>{h1}</h1>
        <p class="lede">{lede}</p>
        <div class="hero-cta-row">
          <a href="{APP}/inscription" class="btn btn-cta">Essayer 14 jours</a>
        </div>
      </div>
    </section>
{bande_reassurance()}
{grille_peurs(PEURS_HUB[url][1], PEURS_HUB[url][0], titre_peurs) if url in PEURS_HUB else ""}
{sections}
{bloc_faq(faq, faq_titre, faq_chapeau)}
{bande_cta("Prêt à simplifier votre caisse ?",
           "Essayez Hippopos gratuitement pendant 14 jours, sans carte bancaire.")}
  </main>"""
    html = (head(titre, desc, url, ld, profondeur)
            + entete(profondeur, url)
            + ariane([("Accueil", "/"), (eyebrow, None)], profondeur)
            + corps + pied(profondeur))
    return ecrire(url.strip("/") + "/index.html", html)


# --------------------------------------------------------------------------
# Les 4 hubs de l'étage 1
# --------------------------------------------------------------------------
def hub_metiers():
    cartes = []
    for slug, lab, publie in METIERS_COUVERTS:
        if publie:
            m = METIERS[slug]
            cartes.append(
                f"""          <a class="link-card" href="{slug}/">
            {ico("m-" + slug)}
            <strong>Logiciel de caisse {m["nom"]}</strong>
            <span>{m["signature_titre"]}</span>
          </a>"""
            )
    autres = [lab for slug, lab, publie in METIERS_COUVERTS if not publie]
    phrase = (
        ", ".join(autres[:-1]).lower() + " et " + autres[-1].lower()
    )
    sections = f"""
    <section>
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">Que vendez-vous ?</span>
          <h2>Les 18 métiers couverts</h2>
          <p>Hippopos s'adresse aux commerces qui vendent en boutique, à la pièce, au poids
             ou par variantes. La restauration servie en salle et les métiers sur rendez-vous
             ne sont pas couverts : ni écran cuisine, ni plan de salle, ni agenda.</p>
        </div>
        <div class="link-grid">
{chr(10).join(cartes)}
        </div>
        <p style="margin:28px auto 0;max-width:70ch;text-align:center;color:var(--text-muted);font-size:0.96rem;">
          Hippopos couvre aussi le {phrase} : mêmes fonctions, même conformité,
          même tarif. <a href="mailto:contact@hippopos.fr" style="color:inherit;text-decoration:underline;">Écrivez-nous</a>
          pour en parler.
        </p>
      </div>
    </section>

    <section>
      <div class="container">
        <div class="highlight">
          <div class="container">
            <div class="highlight-copy">
              <span class="eyebrow">Le socle commun</span>
              <h2>Ce qui ne change pas d'un métier à l'autre</h2>
              <p>La façon de vendre change ; la conformité, le stock et les clôtures, non.
                 Ces briques sont les mêmes sur les 18 métiers, sans module payant caché.</p>
              <ul class="check-list">
                <li>Chaînage et horodatage de chaque vente et de chaque clôture, conformes NF525</li>
                <li>Suivi de stock par produit ou par variante, inventaires guidés</li>
                <li>Clôtures jour, mois et année, comptage du fond de caisse</li>
                <li>Comptes vendeurs, code PIN et permissions par personne</li>
                <li>Fonctionne dans le navigateur : douchette, balance et imprimante existantes restent en place</li>
              </ul>
            </div>
            <div class="highlight-visual">
              <div class="shop-row">
                <div>
                  <div class="shop-name">Vente au poids</div>
                  <div class="shop-stock">Balance lue, montant porté au ticket</div>
                </div>
                <span class="pill">Inclus</span>
              </div>
              <div class="shop-row">
                <div>
                  <div class="shop-name">Variantes produit</div>
                  <div class="shop-stock">Taille, parfum, format, contenance</div>
                </div>
                <span class="pill">Inclus</span>
              </div>
              <div class="shop-row">
                <div>
                  <div class="shop-name">Multi-magasins</div>
                  <div class="shop-stock">Stock par magasin et transferts</div>
                </div>
                <span class="pill">Formule 69 €</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>"""
    return page_hub(
        url="/logiciel-de-caisse/",
        titre="Logiciel de caisse pour commerce de détail : 18 métiers",
        desc="Vente au poids ou à la pièce, variantes, stock par magasin et clôtures "
             "conformes NF525. 18 métiers de détail couverts, à partir de 29 € HT par mois.",
        h1="Logiciel de caisse pour commerce de détail",
        lede="Boulangerie, boucherie, épicerie, chocolaterie : la façon de vendre change d'un "
             "comptoir à l'autre, la caisse doit suivre. Choisissez votre métier pour voir ce "
             "qu'Hippopos couvre — et ce qu'il ne couvre pas.",
        eyebrow="Logiciel de caisse",
        sections=sections,
        faq=FAQ_SILO_METIERS,
        faq_titre="Les questions qu'on nous pose avant de choisir",
        nom_ld="Logiciel de caisse pour commerce de détail",
        titre_peurs="Trois contraintes que la caisse doit lever",
    )


BRIQUES = [
    ("caisse-tactile", "Caisse tactile rapide", "Vente à la pièce ou au poids, variantes, codes-barres, remises et paiements mixtes."),
    ("conformite", "Conformité NF525", "Ventes et clôtures chaînées et horodatées, journaux consultables, archivage inaltérable."),
    ("stock", "Stock et inventaires", "Suivi par produit ou par variante, inventaires guidés, alertes de rupture."),
    ("clotures", "Clôtures et fond de caisse", "Clôtures jour, mois et année, comptage du fond, entrées et sorties d'espèces."),
    ("equipe", "Équipe et permissions", "Un vendeur par membre de l'équipe, code PIN et droits d'accès personnalisés."),
    ("tickets", "Tickets et reçus", "Ticket imprimable ou envoyé par email, avec logo et coordonnées du magasin."),
]

# Activables à la demande depuis les paramètres (restructuration du 22/08/2026).
ADDONS = [
    ("multi-magasins", "Multi-magasins", "Catalogue centralisé, stock indépendant par magasin, transferts en deux temps."),
    ("fidelite", "Fidélité clients", "Points, carte à tampons ou cashback : le programme qui correspond au commerce."),
    ("etiquettes", "Étiquettes et codes-barres", "Génération et impression d'étiquettes produit, scan par douchette ou caméra."),
    ("cheques-cadeaux", "Tickets et chèques cadeaux", "Ticket cadeau sans les prix, et chèques cadeaux à code unique dont le solde se suit tout seul."),
]

COMPATIBILITES = [
    ("douchette", "Douchette code-barres", "Les modèles USB et Bluetooth déjà en place fonctionnent tels quels."),
    ("poids", "Balance connectée", "Le poids est lu par la caisse : plus de montant ressaisi à la main."),
    ("imprimante", "Imprimante à tickets", "Les imprimantes thermiques existantes restent utilisables."),
]


# Ce que chaque brique met en avant sur le hub. Le titre et le chapeau viennent
# de BRIQUES/ADDONS ; les puces reprennent le détail écrit pour les pages métier
# quand il existe, pour que les deux étages disent la même chose.
PUCES_HUB = {
    "caisse-tactile": ["Vente à la pièce, au poids ou par variante, sur le même ticket",
                       "Remises en pourcentage ou en euros, à la ligne ou au ticket",
                       "Paiements mixtes : espèces, carte et chèque sur une même vente"],
    "conformite": ["Chaque vente chaînée à la précédente et horodatée",
                   "Journaux de vente et de clôture consultables à tout moment",
                   "Clôtures archivées, présentables en cas de contrôle"],
    # Le ticket cadeau appartient à l'add-on « tickets et chèques cadeaux »,
    # pas à cette brique : il n'est pas cité ici.
    "tickets": ["Imprimé sur l'imprimante thermique en place, ou envoyé par email",
                "Logo et coordonnées du magasin repris de votre fiche",
                "Lignes, remises et moyens de paiement détaillés sur le ticket"],
}

# id du hub → (clé de FONCTIONS_DETAIL pour les puces, clé de panneau)
SOURCE_HUB = {
    "caisse-tactile": (None, "vente-au-poids"),
    "conformite": (None, "conformite"),
    "stock": ("gestion-de-stock", "stock"),
    "clotures": ("cloture-de-caisse", "clotures"),
    "equipe": ("comptes-vendeurs", "equipe"),
    "tickets": (None, "ticket"),
    "multi-magasins": ("multi-magasins", "multi-magasins"),
    "fidelite": ("fidelite", "fidelite"),
    "etiquettes": ("etiquettes", "etiquettes"),
    "cheques-cadeaux": ("cheques-cadeaux", "cheques-cadeaux"),
}


def hub_fonctionnalites():
    m = METIERS["boulangerie"]

    def section(rang, id_, titre, desc, addon):
        cle_detail, cle_panneau = SOURCE_HUB[id_]
        puces = (FONCTIONS_DETAIL[cle_detail]["puces"] if cle_detail
                 else PUCES_HUB[id_])
        return section_hub_fonction(rang, id_, titre, desc, puces, cle_panneau, m, addon)

    briques = "\n".join(section(r, i, t, d, False)
                        for r, (i, t, d) in enumerate(BRIQUES))
    addons = "\n".join(section(r, i, t, d, True)
                       for r, (i, t, d) in enumerate(ADDONS, start=len(BRIQUES)))
    compat = "\n".join(
        f"""          <div class="link-card is-info">
            {ico(i)}
            <strong>{t}</strong>
            <span>{d}</span>
          </div>"""
        for i, t, d in COMPATIBILITES
    )
    sections = f"""
    <section class="fonctions-tete">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">Vendre et piloter</span>
          <h2>Les 6 briques comprises</h2>
          <p>Ces six briques sont dans l'abonnement dès la première formule, sans supplément
             et sans réglage préalable.</p>
        </div>
      </div>
    </section>
{briques}
    <section class="fonctions-tete">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">À la demande</span>
          <h2>Les 4 add-ons activables</h2>
          <p>Ils s'activent en un clic depuis les paramètres, uniquement si le commerce
             en a besoin — et sont facturés à partir de la formule qui les porte.</p>
        </div>
      </div>
    </section>
{addons}

    <section>
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">Compatibilité matériel</span>
          <h2>Votre matériel actuel reste en place</h2>
          <p>Hippopos fonctionne dans le navigateur, sur tablette, ordinateur ou terminal
             tactile. Aucun matériel n'est imposé et rien n'est vendu avec l'abonnement.</p>
        </div>
        <div class="link-grid">
{compat}
        </div>
      </div>
    </section>"""
    faq = [
        ("Toutes les fonctions sont-elles comprises dans l'abonnement ?",
         "Six briques le sont dès la formule Solo : caisse, conformité NF525, stock, clôtures, "
         "permissions et tickets. Quatre add-ons s'activent à la demande — fidélité, étiquettes "
         "et chèques cadeaux à partir de la formule Équipe, le multi-magasins avec la formule "
         "du même nom à 69 € HT par mois."),
        ("Qu'est-ce qu'un chèque cadeau chez Hippopos ?",
         "Un code unique remis au client, utilisable en un ou plusieurs paiements, dont le solde "
         "se met à jour tout seul. À ne pas confondre avec le ticket cadeau, qui est le ticket "
         "d'achat sans les prix, remis pour offrir un article."),
        ("Hippopos gère-t-il la vente au poids ?",
         "Oui. La balance connectée est lue par la caisse et le montant est porté au ticket "
         "sans ressaisie. Le poids et la pièce cohabitent sur un même ticket."),
        ("Peut-on connecter Hippopos à une boutique en ligne ?",
         "Non, pas aujourd'hui. Il n'y a ni connexion e-commerce, ni click and collect. "
         "Hippopos couvre la vente en boutique."),
        ("Y a-t-il un écran cuisine ou un plan de salle ?",
         "Non. Hippopos ne couvre pas la restauration servie en salle. Il n'y a ni écran "
         "cuisine, ni plan de salle, ni commande à table. Pour voir ces fonctions appliquées "
         'à un commerce, voir le <a href="../logiciel-de-caisse/">logiciel de caisse pour '
         'commerce de détail</a>.'),
    ]
    return page_hub(
        url="/fonctionnalites/",
        titre="Fonctionnalités d'un logiciel de caisse : les 9 briques utiles",
        desc="Caisse tactile, stock, clôtures, permissions et tickets compris ; multi-magasins, "
             "fidélité, étiquettes et chèques cadeaux activables à la demande.",
        h1="Les fonctionnalités d'un logiciel de caisse, brique par brique",
        lede="Six briques comprises couvrent l'encaissement, le catalogue, le stock et la "
             "conformité ; quatre add-ons s'activent à la demande. Cette page dit ce qu'elles "
             "font — et, à la fin, ce qu'Hippopos ne fait pas.",
        eyebrow="Fonctionnalités",
        sections=sections,
        faq=faq,
        faq_titre="Ce qu'on nous demande sur les fonctions",
        nom_ld="Fonctionnalités du logiciel de caisse Hippopos",
        titre_peurs="Trois questions à poser avant l'essai",
    )


EXIGENCES = [
    ("cadenas", "Inaltérabilité", "Une vente enregistrée ne peut plus être modifiée ni supprimée."),
    ("conformite", "Sécurisation", "Chaque opération est tracée et chaînée à la précédente par un calcul cryptographique."),
    ("oeil", "Conservation", "Les données de vente sont conservées et restent consultables dans le temps."),
    ("archive", "Archivage", "Les clôtures sont archivées et présentables en cas de contrôle fiscal."),
]


def hub_nf525():
    ex = "\n".join(
        f"""          <div class="feature-card">
            <div class="feature-icon">{ico(i)}</div>
            <h3>{t}</h3>
            <p>{d}</p>
          </div>"""
        for i, t, d in EXIGENCES
    )
    sections = f"""
    <section>
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">Ce que la loi exige</span>
          <h2>Les quatre exigences, dites simplement</h2>
          <p>Depuis la loi anti-fraude à la TVA, un commerçant assujetti qui encaisse des
             particuliers doit utiliser un logiciel de caisse répondant à quatre exigences.</p>
        </div>
        <div class="features-grid">
{ex}
        </div>
      </div>
    </section>

    <section>
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">Vérifier sa caisse</span>
          <h2>Comment savoir si votre caisse est conforme</h2>
        </div>
        <div class="steps">
          <div class="step">
            <div class="step-number">1</div>
            <h3>Demandez le justificatif</h3>
            <p>Certificat délivré par un organisme accrédité, ou attestation individuelle
               remise par l'éditeur. L'un des deux suffit, mais l'un des deux est exigible.</p>
          </div>
          <div class="step">
            <div class="step-number">2</div>
            <h3>Vérifiez qu'il vous nomme</h3>
            <p>L'attestation est nominative : elle désigne votre entreprise et la version du
               logiciel que vous utilisez.</p>
          </div>
          <div class="step">
            <div class="step-number">3</div>
            <h3>Contrôlez les clôtures</h3>
            <p>Une caisse conforme produit des clôtures jour, mois et année, consultables et
               non modifiables après coup.</p>
          </div>
          <div class="step">
            <div class="step-number">4</div>
            <h3>Gardez-le accessible</h3>
            <p>Le justificatif se présente en cas de contrôle. Sans lui, l'amende s'applique
               par logiciel non conforme.</p>
          </div>
        </div>
      </div>
    </section>

"""
    faq = [
        ("Le logiciel de caisse est-il obligatoire ?",
         "Il l'est pour tout assujetti à la TVA qui enregistre des règlements de clients "
         "particuliers. En sont notamment dispensés les assujettis en franchise en base et "
         "ceux dont l'activité s'adresse exclusivement à des professionnels."),
        ("Quelle est la différence entre certificat et attestation ?",
         "Le certificat est délivré à l'éditeur par un organisme accrédité. L'attestation "
         "individuelle est remise par l'éditeur à chacun de ses clients. L'un ou l'autre "
         "suffit à justifier la conformité."),
        ("Que risque un commerçant non conforme ?",
         "Une amende s'applique par logiciel non conforme, et l'administration peut demander "
         "la régularisation. Le justificatif doit pouvoir être présenté lors d'un contrôle."),
        ("Une caisse à touches est-elle concernée ?",
         "Oui, dès lors qu'elle enregistre des règlements de particuliers. La forme du "
         "matériel ne change rien : c'est la fonction d'enregistrement qui déclenche "
         "l'obligation. Les fonctions de conformité sont les mêmes sur les 18 métiers du "
         '<a href="../logiciel-de-caisse/">logiciel de caisse pour commerce de détail</a>.'),
    ]
    return page_hub(
        url="/nf525/",
        titre="Logiciel de caisse certifié NF525 : ce que la loi exige",
        desc="Inaltérabilité, sécurisation, conservation, archivage : les quatre exigences "
             "auxquelles votre caisse doit répondre, et comment le vérifier.",
        h1="Logiciel de caisse certifié NF525 : ce que la loi exige vraiment",
        lede="Quatre exigences, un justificatif à pouvoir présenter, et une amende à la clé "
             "en cas de contrôle. Cette page dit ce que la norme impose et comment vérifier "
             "que votre caisse y répond.",
        eyebrow="Conformité NF525",
        sections=sections,
        faq=faq,
        faq_titre="Les questions de conformité",
        nom_ld="Conformité NF525 du logiciel de caisse Hippopos",
        titre_peurs="Trois inquiétudes que la conformité doit lever",
    )


def hub_tarifs():
    sections = """
    <section>
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">Votre budget mensuel</span>
          <h2>Les trois formules Hippopos</h2>
          <p>14 jours d'essai gratuit sur toutes les formules. Sans engagement, résiliable
             à tout moment, sans carte bancaire à l'inscription.</p>
        </div>
        <div class="pricing-grid">
          <div class="price-card">
            <div class="plan-name">Solo</div>
            <div class="plan-desc">Pour un commerce avec un seul point de vente.</div>
            <div class="plan-price"><strong>29 €</strong><span>/ mois HT</span></div>
            <div class="price-card-note">1 magasin · 2 comptes vendeur inclus</div>
            <ul class="check-list">
              <li>Caisse, catalogue et stock illimités</li>
              <li>Clôtures conformes NF525</li>
              <li>Tickets et reçus par email</li>
              <li>Support par email</li>
            </ul>
            <a href="https://app.hippopos.fr/inscription" class="btn btn-ghost btn-block">Essayer gratuitement</a>
          </div>
          <div class="price-card featured">
            <span class="plan-badge">Le plus choisi</span>
            <div class="plan-name">Équipe</div>
            <div class="plan-desc">Pour un commerce avec plusieurs vendeurs.</div>
            <div class="plan-price"><strong>49 €</strong><span>/ mois HT</span></div>
            <div class="price-card-note">1 magasin · Comptes vendeur illimités</div>
            <ul class="check-list">
              <li>Tout Solo, plus :</li>
              <li>Permissions par vendeur</li>
              <li>Programme de fidélité</li>
              <li>Étiquettes produit</li>
              <li>Tickets et chèques cadeaux</li>
              <li>Support prioritaire</li>
            </ul>
            <a href="https://app.hippopos.fr/inscription" class="btn btn-cta btn-block">Essayer gratuitement</a>
          </div>
          <div class="price-card">
            <div class="plan-name">Multi-magasins</div>
            <div class="plan-desc">Pour les enseignes à plusieurs adresses (1er magasin inclus).</div>
            <div class="plan-price"><strong>69 €</strong><span>/ mois HT</span></div>
            <div class="price-card-note">+ 39 € HT / mois par magasin supplémentaire</div>
            <ul class="check-list">
              <li>Tout Équipe, plus :</li>
              <li>Catalogue centralisé</li>
              <li>Stock indépendant par magasin</li>
              <li>Transferts entre magasins</li>
              <li>Accompagnement au démarrage</li>
            </ul>
            <a href="https://app.hippopos.fr/inscription" class="btn btn-ghost btn-block">Essayer gratuitement</a>
          </div>
        </div>
      </div>
    </section>

    <section>
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">Lire un tarif de caisse</span>
          <h2>Ce que le prix affiché ne dit pas</h2>
          <p>Trois postes font l'essentiel de l'écart entre le prix annoncé par un éditeur
             et ce qui est réellement payé la première année.</p>
        </div>
        <div class="table-wrap">
          <table class="price-table">
            <thead>
              <tr><th>Poste</th><th>Ce qu'il faut regarder</th><th>Chez Hippopos</th></tr>
            </thead>
            <tbody>
              <tr>
                <td>Le matériel</td>
                <td>Beaucoup d'offres incluent un terminal, facturé à l'achat ou en location sur 36 mois.</td>
                <td>Aucun matériel vendu ni imposé. Le vôtre reste en place.</td>
              </tr>
              <tr>
                <td>Le magasin supplémentaire</td>
                <td>Le tarif affiché vaut souvent pour un seul point de vente.</td>
                <td>39 € HT par mois et par magasin, au-delà du premier.</td>
              </tr>
              <tr>
                <td>L'engagement</td>
                <td>Un tarif bas suppose fréquemment 12 à 36 mois d'engagement.</td>
                <td>Sans engagement, résiliable à tout moment.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>"""
    faq = [
        ("Combien coûte un logiciel de caisse par mois ?",
         "Les offres du marché vont de la gratuité, souvent limitée, à environ 90 € HT par "
         "mois pour une caisse complète. Hippopos se situe entre 29 et 69 € HT par mois selon "
         "le nombre de vendeurs et de magasins."),
        ("Y a-t-il des frais d'installation ?",
         "Non. L'inscription se fait en ligne, le catalogue s'importe et le réglage de la TVA, "
         "des moyens de paiement et du ticket se fait depuis l'application."),
        ("Faut-il une carte bancaire pour l'essai ?",
         "Non. Les 14 jours d'essai ne demandent aucune carte bancaire. À la fin de l'essai, "
         "vous choisissez de passer à une formule payante ou d'arrêter."),
        ("Que devient l'historique après résiliation ?",
         "L'historique de ventes reste consultable après résiliation, et les données restent "
         "accessibles pour l'export."),
        ("Le tarif change-t-il si j'ouvre un second magasin ?",
         "Oui : le passage à la formule Multi-magasins à 69 € HT par mois inclut le premier "
         "magasin, puis chaque magasin supplémentaire coûte 39 € HT par mois. "
         'Le tarif ne change pas d\'un métier à l\'autre : voir le '
         '<a href="../logiciel-de-caisse/">logiciel de caisse pour commerce de détail</a>.'),
    ]
    return page_hub(
        url="/tarifs/",
        titre="Prix d'un logiciel de caisse : combien coûte une caisse en 2026",
        desc="Les prix du marché vont de la gratuité à 89 € HT par mois. Le détail poste par "
             "poste, et les trois formules Hippopos à 29, 49 et 69 € HT par mois.",
        h1="Prix d'un logiciel de caisse : ce que coûte vraiment une caisse en 2026",
        lede="Le prix affiché n'est presque jamais le prix payé : le matériel, le second "
             "magasin et l'engagement font l'écart. Voici les trois postes à regarder, puis "
             "les tarifs d'Hippopos.",
        eyebrow="Tarifs",
        sections=sections,
        faq=faq,
        faq_titre="Les questions sur le prix",
        nom_ld="Tarifs du logiciel de caisse Hippopos",
        titre_peurs="Trois postes qui gonflent le prix d'une caisse",
    )


def synchroniser_accueil():
    """Réaligne l'en-tête de l'accueil sur `entete(0)`.

    `index.html` est écrit à la main par Timothy : on n'y touche qu'à l'en-tête,
    pour qu'une entrée ajoutée au menu ne manque jamais sur la page la plus vue.
    """
    f = RACINE / "index.html"
    s = f.read_text(encoding="utf-8")
    d = s.index('  <header class="site-header">')
    fin = s.index("  </header>", d) + len("  </header>")
    neuf = entete(0).split("<body>\n", 1)[1].rstrip()
    s = s[:d] + neuf + s[fin:]

    # La bande de réassurance, elle aussi, pour que l'accueil et les pages
    # métier ne racontent pas la même promesse de deux façons différentes.
    # Bornée par l'indentation : compter les </div> échouait dès que la bande
    # avait déjà été remplacée par la version imbriquée.
    s = re.sub(r'    <div class="trust-strip">.*?\n    </div>',
               lambda _: bande_reassurance().rstrip(), s, count=1, flags=re.S)

    if s == f.read_text(encoding="utf-8"):
        return "index.html (déjà à jour)"
    f.write_text(s, encoding="utf-8")
    return "index.html (en-tête et réassurance resynchronisés)"


def main():
    faits = [hub_metiers(), hub_fonctionnalites(), hub_nf525(), hub_tarifs()]
    faits += [page_metier(s) for s in METIERS]
    faits.append(synchroniser_accueil())
    for f in faits:
        print("écrit", f)
    print(f"\n{len(faits)} fichiers écrits.")


if __name__ == "__main__":
    main()
