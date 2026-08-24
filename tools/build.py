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
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from pages import (  # noqa: E402
    METIERS, METIERS_COUVERTS, FAQ_SILO_METIERS, DECLINAISONS,
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


def entete(profondeur, actif=""):
    r = "../" * profondeur
    liens = "\n".join(
        f'        <a href="{r.rstrip("/") or "."}{u}"'
        + (' aria-current="page"' if u == actif else "")
        + f">{lab}</a>"
        for u, lab in SILOS
    )
    liens_mobile = "\n".join(
        f'      <a href="{r.rstrip("/") or "."}{u}">{lab}</a>' for u, lab in SILOS
    )
    return f"""<body>
  <header class="site-header">
    <div class="container">
      <a href="{r or "/"}" class="brand">
        <img src="{r}assets/hippopos-logo.png" alt="Hippopos" style="height: 40px;" />
      </a>
      <nav class="main-nav">
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
{liens_mobile}
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

    declins = "\n".join(
        f"""          <div class="link-card is-soon">
            <strong>{t}</strong>
            <span>{d}</span>
            <span style="margin-top:8px;font-size:0.82rem;">Page prévue — roadmap {sl}</span>
          </div>"""
        for t, d, sl in DECLINAISONS
    )

    soeurs = "\n".join(
        f"""          <a class="link-card" href="../{s}/">
            <strong>Logiciel de caisse {METIERS[s]["nom"]}</strong>
            <span>{METIERS[s]["signature_titre"]}</span>
          </a>"""
        for s in m["soeurs"]
    )

    corps = f"""
  <main>
    <section class="page-hero">
      <div class="container">
        <span class="eyebrow">{m["famille"]}</span>
        <h1>{m["h1"]}</h1>
        <p class="lede">{m["lede"]}</p>
        <div class="hero-cta-row">
          <a href="{APP}/inscription" class="btn btn-cta">Essayer 14 jours</a>
          <a href="../../tarifs/" class="btn btn-ghost">Voir les tarifs</a>
        </div>
      </div>
    </section>

    <section>
      <div class="container">
        <div class="signature">
          <div>
            <span class="eyebrow">La contrainte du métier</span>
            <h2>{m["signature_titre"]}</h2>
            <p class="signature-quote">{m["signature"]}</p>
          </div>
          <div class="a-fournir-bloc">
            <strong>À fournir avant mise en ligne</strong>
            Capture de l'écran de caisse en {nom}, nombre de commerces équipés et
            verbatim client vérifiable. Aucun chiffre ni avis n'est publié tant
            qu'il n'a pas été fourni.
          </div>
        </div>
      </div>
    </section>

    <section>
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

    <section>
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">Aller plus loin</span>
          <h2>Le prix, la conformité et le changement de caisse</h2>
        </div>
        <div class="link-grid">
{declins}
        </div>
      </div>
    </section>

    <section>
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">Métiers proches</span>
          <h2>Les autres métiers de comptoir</h2>
        </div>
        <div class="link-grid">
{soeurs}
        </div>
      </div>
    </section>
{bande_cta(f"Voir Hippopos en {nom}",
           "14 jours d'essai, sans carte bancaire, votre catalogue importé en une fois.")}
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
             nom_ld, profondeur=1, faq_chapeau=""):
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
          <a href="{"../" * profondeur}tarifs/" class="btn btn-ghost">Voir les tarifs</a>
        </div>
      </div>
    </section>
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
            <strong>Logiciel de caisse {m["nom"]}</strong>
            <span>{m["signature_titre"]}</span>
          </a>"""
            )
        else:
            cartes.append(
                f"""          <div class="link-card is-soon">
            <strong>{lab}</strong>
            <span>Métier couvert par l'offre — page à venir</span>
          </div>"""
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
    )


BRIQUES = [
    ("Caisse tactile rapide", "Vente à la pièce ou au poids, variantes, codes-barres, remises et paiements mixtes."),
    ("Conformité NF525", "Ventes et clôtures chaînées et horodatées, journaux consultables, archivage inaltérable."),
    ("Stock et inventaires", "Suivi par produit ou par variante, inventaires guidés, alertes de rupture."),
    ("Clôtures et fond de caisse", "Clôtures jour, mois et année, comptage du fond, entrées et sorties d'espèces."),
    ("Équipe et permissions", "Un vendeur par membre de l'équipe, code PIN et droits d'accès personnalisés."),
    ("Tickets et reçus", "Ticket imprimable ou envoyé par email, avec logo et coordonnées du magasin."),
]

# Activables à la demande depuis les paramètres (restructuration du 22/08/2026).
ADDONS = [
    ("Multi-magasins", "Catalogue centralisé, stock indépendant par magasin, transferts en deux temps."),
    ("Fidélité clients", "Points, carte à tampons ou cashback : le programme qui correspond au commerce."),
    ("Étiquettes et codes-barres", "Génération et impression d'étiquettes produit, scan par douchette ou caméra."),
    ("Tickets et chèques cadeaux", "Ticket cadeau sans les prix, et chèques cadeaux à code unique dont le solde se suit tout seul."),
]

COMPATIBILITES = [
    ("Douchette code-barres", "Les modèles USB et Bluetooth déjà en place fonctionnent tels quels."),
    ("Balance connectée", "Le poids est lu par la caisse : plus de montant ressaisi à la main."),
    ("Imprimante à tickets", "Les imprimantes thermiques existantes restent utilisables."),
]


def hub_fonctionnalites():
    carte = lambda t, d: f"""          <div class="feature-card">
            <h3>{t}</h3>
            <p>{d}</p>
          </div>"""
    briques = "\n".join(carte(t, d) for t, d in BRIQUES)
    addons = "\n".join(carte(t, d) for t, d in ADDONS)
    compat = "\n".join(
        f"""          <div class="link-card is-soon">
            <strong>{t}</strong>
            <span>{d}</span>
          </div>"""
        for t, d in COMPATIBILITES
    )
    sections = f"""
    <section>
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">Vendre et piloter</span>
          <h2>Les 6 briques comprises</h2>
          <p>Ces six briques sont dans l'abonnement dès la première formule, sans supplément
             et sans réglage préalable.</p>
        </div>
        <div class="features-grid">
{briques}
        </div>

        <div class="subsection-head">
          <h3>Les 4 add-ons activables à la demande</h3>
          <p>Ils s'activent en un clic depuis les paramètres, uniquement si le commerce en a besoin.</p>
        </div>
        <div class="features-grid addons-grid">
{addons}
        </div>
      </div>
    </section>

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
         "cuisine, ni plan de salle, ni commande à table."),
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
    )


EXIGENCES = [
    ("Inaltérabilité", "Une vente enregistrée ne peut plus être modifiée ni supprimée."),
    ("Sécurisation", "Chaque opération est tracée et chaînée à la précédente par un calcul cryptographique."),
    ("Conservation", "Les données de vente sont conservées et restent consultables dans le temps."),
    ("Archivage", "Les clôtures sont archivées et présentables en cas de contrôle fiscal."),
]


def hub_nf525():
    ex = "\n".join(
        f"""          <div class="feature-card">
            <h3>{t}</h3>
            <p>{d}</p>
          </div>"""
        for t, d in EXIGENCES
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

    <section>
      <div class="container">
        <div class="a-fournir-bloc">
          <strong>À compléter avant mise en ligne</strong>
          Hippopos annonce des ventes et des clôtures chaînées et horodatées conformes aux
          exigences NF525. Le mot « certifié » ne doit pas figurer sur le site tant que le
          numéro de certificat ou le modèle d'attestation individuelle n'a pas été fourni :
          la formulation exacte et le justificatif sont attendus de l'éditeur.
        </div>
      </div>
    </section>"""
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
         "l'obligation."),
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
         "magasin, puis chaque magasin supplémentaire coûte 39 € HT par mois."),
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
    )


def main():
    faits = [hub_metiers(), hub_fonctionnalites(), hub_nf525(), hub_tarifs()]
    faits += [page_metier(s) for s in METIERS]
    for f in faits:
        print("écrit", f)
    print(f"\n{len(faits)} pages générées.")


if __name__ == "__main__":
    main()
