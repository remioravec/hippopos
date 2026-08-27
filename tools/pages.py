"""Données des pages de l'arbre — source de vérité du contenu généré.

Repris du dossier de mission du 15/08/2026 : spec-hippopos.json (relevés SERP,
volumes, règle d'offre), tableau-balisage-hippopos.xlsx (titles et descriptions
des étages 1) et maquettes-sxo-hippopos.html (ordre des modules).

Règle appliquée partout : rien d'inventé. Tout ce qui manque — chiffre de parc,
verbatim client, capture produit — est marqué A_FOURNIR et ressort surligné en
jaune sur la page, jamais comblé par une valeur plausible.
"""

# Cibles de croisement vers l'axe secondaire. Tant que la page fille n'existe pas
# (roadmap septembre), le lien pointe sur la section du hub — l'ancre, elle, porte
# déjà l'exact match de la requête cible de la future page.
FONCTIONS = {
    "vente-au-poids":     ("logiciel de caisse avec vente au poids", "avec-vente-au-poids", "caisse-tactile"),
    "variantes-produit":  ("logiciel de caisse avec variantes produit", "avec-variantes-produit", "caisse-tactile"),
    "gestion-de-stock":   ("logiciel de caisse avec gestion de stock", "avec-gestion-de-stock", "stock"),
    "inventaire-guide":   ("logiciel de caisse avec inventaire guidé", "avec-inventaire-guide", "stock"),
    "multi-magasins":     ("logiciel de caisse multi-magasins", "multi-magasins", "multi-magasins"),
    "fidelite":           ("logiciel de caisse avec programme de fidélité", "avec-programme-de-fidelite", "fidelite"),
    "etiquettes":         ("logiciel de caisse avec étiquettes et codes-barres", "avec-etiquettes-et-codes-barres", "etiquettes"),
    "cloture-de-caisse":  ("logiciel de caisse avec clôture de caisse", "avec-cloture-de-caisse", "clotures"),
    "comptes-vendeurs":   ("logiciel de caisse avec comptes vendeurs et permissions", "avec-comptes-vendeurs-et-permissions", "equipe"),
    "cheques-cadeaux":    ("logiciel de caisse avec chèques cadeaux", "avec-cheques-cadeaux", "cheques-cadeaux"),
}

# Pages filles de l'axe secondaire réellement publiées. Vide aujourd'hui : les
# croisements pointent donc sur la section du hub.
FONCTIONS_PUBLIEES = set()

# Les 18 métiers que l'offre couvre (spec 15/08/2026, offre=true).
# 9 autres sont écartés par la règle d'offre : restaurant, bar, café, food truck,
# restauration rapide, pizzeria, salon de thé (pas de module restauration),
# institut de beauté et coiffure (pas de module rendez-vous).
METIERS_COUVERTS = [
    ("boulangerie", "Boulangerie", True),
    ("patisserie", "Pâtisserie", True),
    ("chocolaterie", "Chocolaterie", True),
    ("boucherie", "Boucherie", True),
    ("charcuterie", "Charcuterie", True),
    ("poissonnerie", "Poissonnerie", True),
    ("traiteur", "Traiteur", True),
    ("epicerie", "Épicerie", True),
    ("caviste", "Caviste", False),
    ("fleuriste", "Fleuriste", False),
    ("fromagerie", "Fromagerie", False),
    ("primeur", "Primeur", False),
    ("magasin-de-vetements", "Magasin de vêtements", False),
    ("cbd", "Boutique CBD", False),
    ("magasin-de-sport", "Magasin de sport", False),
    ("animalerie", "Animalerie", False),
    ("librairie", "Librairie", False),
    ("magasin-de-decoration", "Magasin de décoration", False),
]

# Regroupement des 18 métiers pour le méga-menu et le menu mobile. Deux
# familles : ce qui se vend au comptoir de bouche, et le reste du détail.
FAMILLES_METIERS = [
    ("Métiers de bouche", ["boulangerie", "patisserie", "chocolaterie", "boucherie",
                           "charcuterie", "poissonnerie", "traiteur", "fromagerie",
                           "primeur", "caviste"]),
    ("Épicerie et commerce spécialisé", ["epicerie", "fleuriste", "magasin-de-vetements",
                                         "cbd", "magasin-de-sport", "animalerie",
                                         "librairie", "magasin-de-decoration"]),
]

# Activables à la demande depuis les paramètres (restructuration du 22/08/2026) :
# multi-magasins, fidélité, étiquettes et codes-barres, tickets et chèques cadeaux.
ADDONS_PRODUIT = [
    "multi-magasins", "fidélité", "étiquettes et codes-barres",
    "tickets et chèques cadeaux",
]

# Ce qu'Hippopos ne fait pas — liste produit, identique sur toutes les pages.
ABSENT_DU_PRODUIT = [
    "écran cuisine", "plan de salle", "commande à table", "click and collect",
    "connexion à une boutique en ligne", "agenda de rendez-vous",
    "monnayeur automatique",
]

# --------------------------------------------------------------------------
# Peurs et frustrations, par métier — trois par page
# --------------------------------------------------------------------------
# Règle : une peur n'est retenue que si le produit y répond. Lister une
# contrainte qu'Hippopos ne traite pas (commande à l'avance, plan de salle)
# ferait venir des essais qui n'aboutissent pas.

PEURS = {
    "boulangerie": [
        ("horloge", "Le coup de feu de 7 h 30",
         "Vingt personnes, des paniers à trois articles. Une caisse qui demande trois écrans pour une baguette fabrique la file toute seule."),
        ("calcul", "Le vrac converti de tête",
         "Chocolats, brioches à la coupe : le prix au kilo se calcule au comptoir, et l'écart ne se voit qu'à l'inventaire."),
        ("oeil", "Deux points de vente, deux vérités",
         "Le fournil et le dépôt ne tiennent pas le même catalogue, et personne ne sait lequel fait foi."),
    ],
    "patisserie": [
        ("variantes", "Le même gâteau en six déclinaisons",
         "Six parts, huit parts, vanille ou chocolat : autant de prix, et une caisse qui n'en connaît qu'un."),
        ("calcul", "La part et le kilo dans le même panier",
         "Un entremets à l'unité, une tarte à la part, des chocolats au poids : trois façons de compter au même comptoir."),
        ("etiquettes", "L'étiquette réécrite au feutre",
         "La vitrine change tous les matins. Le prix affiché finit par ne plus être celui de la caisse."),
    ],
    "chocolaterie": [
        ("calcul", "Le ballotin composé au gramme",
         "Le client choisit pièce par pièce, la balance affiche 0,250 kg, et le prix se pose pendant qu'on emballe."),
        ("calendrier", "L'année qui se joue en trois semaines",
         "Décembre concentre l'essentiel du chiffre. La boutique éphémère ouvre, et le catalogue doit suivre le jour même."),
        ("cheques-cadeaux", "Le chèque cadeau suivi au carnet",
         "Un numéro noté à la main, un solde retenu de mémoire : personne ne sait ce qui reste à consommer."),
    ],
    "boucherie": [
        ("calcul", "Le poids retapé à la main",
         "La balance affiche, le vendeur ressaisit. Un chiffre inversé, et la marge part avec le rôti."),
        ("cadenas", "Qui a passé cette remise ?",
         "Trois personnes derrière le comptoir, une seule caisse, aucun moyen de savoir qui a annulé la ligne."),
        ("alerte", "Le fond de caisse qui ne tombe jamais juste",
         "Le soir, l'écart de quelques euros se constate sans jamais s'expliquer."),
    ],
    "charcuterie": [
        ("calcul", "La tranche, la barquette et le kilo",
         "Six tranches de jambon, une terrine au poids, une quiche à la part : trois unités de vente sur le même ticket."),
        ("variantes", "Le même produit en trois formats",
         "Entière, demie, à la coupe : chaque format a son prix, et la caisse n'en retient qu'un."),
        ("etiquettes", "L'étiquette qui ne suit pas le prix",
         "Le tarif bouge en vitrine mais pas en caisse — ou l'inverse, et c'est le client qui le remarque."),
    ],
    "poissonnerie": [
        ("calcul", "Le poids ressaisi",
         "La balance affiche 0,480 kg, le vendeur tape 0,48 ou 480. Deux tickets, deux montants, un seul poisson."),
        ("horloge", "La clôture à 13 h",
         "L'étal ferme, il faut compter la caisse et repartir. La clôture doit tenir en quelques minutes."),
        ("etiquettes", "Le cours du jour",
         "Les prix bougent d'un matin à l'autre. Les reprendre produit par produit prend le temps qu'on n'a pas."),
    ],
    "traiteur": [
        ("calcul", "La barquette pesée devant le client",
         "Salade au poids, lasagnes à la part, terrine au kilo : le prix se pose à la balance, pas au clavier."),
        ("variantes", "La même recette en trois contenants",
         "250 g, 500 g ou au poids : trois prix pour un seul plat, et une caisse qui n'en connaît qu'un."),
        ("cadenas", "L'extra du samedi",
         "Un renfort ponctuel derrière le comptoir doit encaisser, sans accéder aux réglages ni aux chiffres du magasin."),
    ],
    "epicerie": [
        ("rupture", "La rupture découverte en rayon",
         "Le produit manque au moment où le client le demande. La commande, elle, est partie sans lui."),
        ("horloge", "L'inventaire du dimanche",
         "Des centaines de références comptées au stylo, puis ressaisies. Une journée entière, et un résultat déjà faux le lundi."),
        ("oeil", "Deux boutiques, un seul catalogue",
         "Le même produit, deux prix, deux stocks. L'un des deux est faux, et on ne sait pas lequel."),
    ],
}

# --------------------------------------------------------------------------
# Le détail d'une fonctionnalité, vue depuis une page métier
# --------------------------------------------------------------------------
# `addon` marque les quatre modules activables à la demande depuis les
# paramètres (restructuration du 22/08/2026) : les présenter comme compris
# serait faux.
# `panneau` désigne le visuel construit en HTML par build.py.

FONCTIONS_DETAIL = {
    "vente-au-poids": dict(
        titre="La balance parle à la caisse",
        chapeau="Le poids remonte dans la ligne de vente. Plus de conversion de tête, plus de montant ressaisi.",
        puces=["Prix à la pièce, au kilo ou aux cent grammes sur le même ticket",
               "Poids lu par la balance déjà en place, ou saisi si elle n'est pas connectée",
               "Tare et correction possibles avant de valider la ligne"],
        panneau="poids", addon=False),
    "variantes-produit": dict(
        titre="Un produit, toutes ses déclinaisons",
        chapeau="Taille, parfum, format : une seule fiche produit, autant de prix que de variantes.",
        puces=["Une fiche mère et ses variantes, au lieu d'autant de produits distincts",
               "Un prix propre à chaque variante",
               "Un stock suivi variante par variante"],
        panneau="variantes", addon=False),
    "gestion-de-stock": dict(
        titre="Le stock se tient à mesure qu'on vend",
        chapeau="Chaque vente décrémente le stock, et l'alerte tombe avant la rupture, pas après.",
        puces=["Suivi par produit ou par variante",
               "Alerte de rupture au seuil que vous fixez",
               "Entrées de marchandise enregistrées à la réception"],
        panneau="stock", addon=False),
    "inventaire-guide": dict(
        titre="L'inventaire sans le stylo",
        chapeau="Un parcours guidé, référence après référence, avec l'écart affiché au fur et à mesure.",
        puces=["Comptage guidé produit par produit",
               "Écart entre stock théorique et stock compté, visible immédiatement",
               "Validation qui met tout le stock à jour d'un coup"],
        panneau="inventaire", addon=False),
    "cloture-de-caisse": dict(
        titre="La clôture en quelques minutes",
        chapeau="Comptage du fond, ventilation par moyen de paiement, écart calculé : la journée se ferme sans reprendre les tickets.",
        puces=["Clôtures jour, mois et année, chaînées et horodatées",
               "Total par moyen de paiement, écart de caisse affiché",
               "Entrées et sorties d'espèces tracées"],
        panneau="clotures", addon=False),
    "comptes-vendeurs": dict(
        titre="Chaque vente porte un nom",
        chapeau="Un compte par personne, un code PIN, et des droits qui s'arrêtent là où ils doivent s'arrêter.",
        puces=["Ouverture de session au code PIN, en deux secondes",
               "Remises, annulations et clôtures réservées à qui vous décidez",
               "Ventes attribuées au vendeur qui les a passées"],
        panneau="equipe", addon=False),
    "multi-magasins": dict(
        titre="Plusieurs magasins, un seul catalogue",
        chapeau="Le catalogue est centralisé, le stock reste propre à chaque magasin, les transferts se font en deux temps.",
        puces=["Un catalogue et des prix tenus au même endroit",
               "Un stock indépendant par magasin",
               "Transfert envoyé d'un côté, reçu de l'autre"],
        panneau="multi-magasins", addon=True),
    "etiquettes": dict(
        titre="L'étiquette imprimée depuis la fiche produit",
        chapeau="Le prix de l'étiquette est celui de la caisse, parce que c'est la même donnée.",
        puces=["Génération d'étiquettes produit avec code-barres",
               "Impression par lot après un changement de prix",
               "Scan par douchette existante ou par la caméra"],
        panneau="etiquettes", addon=True),
    "cheques-cadeaux": dict(
        titre="Le chèque cadeau qui se suit tout seul",
        chapeau="Un code unique par chèque, un solde tenu par la caisse, et un ticket cadeau sans les prix.",
        puces=["Code unique généré à l'émission",
               "Solde décrémenté à chaque utilisation, partielle ou totale",
               "Ticket cadeau imprimable sans les montants"],
        panneau="cheques-cadeaux", addon=True),
    "fidelite": dict(
        titre="Le programme de fidélité qui correspond au commerce",
        chapeau="Points, carte à tampons ou cashback : un seul mécanisme, choisi une fois, appliqué en caisse.",
        puces=["Points, tampons ou cashback, au choix",
               "Compteur mis à jour à l'encaissement",
               "Solde consultable depuis la fiche client"],
        panneau="fidelite", addon=True),
}

# Le cas concret, métier par métier : ce que la fonction change à ce comptoir-là.
CAS = {
    "boulangerie": {
        "vente-au-poids": "Les chocolats en vrac partent au poids, la baguette à la pièce : le même ticket encaisse les deux sans changer d'écran.",
        "etiquettes": "Une hausse du prix du beurre, et les étiquettes de la vitrine se réimpriment en un lot, au tarif que la caisse applique déjà.",
        "multi-magasins": "Le fournil tient le catalogue, le dépôt le reçoit. Chacun garde son stock, personne ne ressaisit deux fois.",
    },
    "patisserie": {
        "variantes-produit": "L'entremets vanille existe en 6, 8 et 10 parts. Une fiche, trois prix, et le vendeur choisit la taille au moment de servir.",
        "vente-au-poids": "Les chocolats et les mignardises se vendent au poids sur le même ticket qu'un gâteau à l'unité.",
        "etiquettes": "La vitrine change chaque matin : les étiquettes se réimpriment avec les prix du jour, sans passer par le feutre.",
    },
    "chocolaterie": {
        "vente-au-poids": "Le ballotin se compose pièce par pièce, la balance donne le poids, la caisse applique le prix au kilo.",
        "multi-magasins": "La boutique de décembre ouvre avec le catalogue de la maison, et son stock à elle.",
        "cheques-cadeaux": "Le chèque émis en novembre est consommé en deux fois en janvier : le solde suit sans carnet.",
    },
    "boucherie": {
        "vente-au-poids": "Le rôti est pesé, le poids remonte dans la ligne, le prix au kilo s'applique : rien n'est retapé.",
        "comptes-vendeurs": "Chacun ouvre sa session au PIN. La remise et l'annulation restent réservées à qui vous désignez.",
        "cloture-de-caisse": "À la fermeture, le comptage du fond et la ventilation par moyen de paiement donnent l'écart tout de suite.",
    },
    "charcuterie": {
        "vente-au-poids": "Six tranches de jambon, une terrine pesée, une quiche à la part : trois unités de vente, un seul ticket.",
        "variantes-produit": "La terrine existe entière, en demie et à la coupe. Une fiche produit, trois prix.",
        "etiquettes": "Le prix change une fois, dans la fiche produit. L'étiquette de vitrine et la caisse disent la même chose.",
    },
    "poissonnerie": {
        "vente-au-poids": "Le filet est pesé devant le client : 0,480 kg au cours du jour, sans conversion de tête.",
        "cloture-de-caisse": "L'étal ferme à 13 h. Le comptage, la ventilation et l'écart tiennent dans le temps du rangement.",
        "etiquettes": "Le cours du jour se saisit une fois et les étiquettes de l'étal repartent au bon prix.",
    },
    "traiteur": {
        "vente-au-poids": "La barquette est pesée devant le client, la tare est déduite, le prix au kilo s'applique.",
        "variantes-produit": "La salade existe en 250 g, en 500 g et au poids. Une fiche, trois façons de la vendre.",
        "comptes-vendeurs": "L'extra du samedi encaisse avec son propre code, sans accéder aux réglages ni aux chiffres.",
    },
    "epicerie": {
        "gestion-de-stock": "Chaque passage en caisse décrémente le stock, et l'alerte tombe au seuil fixé, avant le rayon vide.",
        "inventaire-guide": "L'inventaire se fait référence après référence, l'écart s'affiche à mesure, et la validation met tout à jour d'un coup.",
        "multi-magasins": "Les deux boutiques partagent un catalogue et gardent chacune leur stock. Le transfert se voit des deux côtés.",
    },
}

# Déclinaisons montrées dans le visuel « variantes », par métier.
VARIANTES_EXEMPLE = {
    "patisserie": ("Entremets vanille", [("6 parts", "24,00 €"), ("8 parts", "32,00 €"), ("10 parts", "40,00 €")]),
    "charcuterie": ("Terrine de campagne", [("Entière", "18,00 €"), ("Demie", "9,50 €"), ("À la coupe", "19,00 €/kg")]),
    "traiteur": ("Salade piémontaise", [("Barquette 250 g", "3,75 €"), ("Barquette 500 g", "7,50 €"), ("Au poids", "15,00 €/kg")]),
}

# --------------------------------------------------------------------------
# Peurs et frustrations des quatre hubs de l'étage 1
# --------------------------------------------------------------------------
# Même règle que pour les métiers : rien qui ne trouve sa réponse dans la page.
# Et rien qui reproche à la concurrence ce qu'Hippopos fait aussi — les quatre
# modules activables à la demande sont dits, pas dissimulés.

PEURS_HUB = {
    "/logiciel-de-caisse/": ("Ce qui coince au comptoir", [
        ("calcul", "Trois façons de vendre, une seule caisse",
         "À la pièce, au poids, par variantes. La plupart des caisses en gèrent une proprement, et bricolent les deux autres."),
        ("controle", "La conformité découverte trop tard",
         "Un cahier ou un tableur ne chaîne rien. NF525 demande des ventes et des clôtures chaînées et horodatées."),
        ("alerte", "Le logiciel taillé pour la restauration",
         "Écran cuisine, plan de salle, commande à table : des fonctions payées et jamais ouvertes, et le poids qui manque."),
    ]),
    "/fonctionnalites/": ("Ce qu'on regarde vraiment avant de signer", [
        ("rupture", "Le module dont on ignore s'il est compris",
         "Fidélité, étiquettes, multi-magasins : mieux vaut savoir avant de signer ce qui est compris et ce qui s'active en plus."),
        ("calcul", "Les fonctions qu'on n'ouvrira jamais",
         "Une caisse de restaurant vendue à une épicerie : des écrans en trop, et rien pour vendre au poids."),
        ("controle", "Ce que le logiciel ne fait pas",
         "La liste des fonctions est toujours publiée. Celle des absences, presque jamais — c'est pourtant elle qui fait échouer un essai."),
    ]),
    "/nf525/": ("Ce qui inquiète avant un contrôle", [
        ("controle", "Le justificatif qu'on ne trouve pas",
         "L'attestation individuelle de conformité est demandée à l'entreprise, pas à l'éditeur. Encore faut-il l'avoir."),
        ("horloge", "Les ventes qu'on ne peut pas reconstituer",
         "Un tableur ne garde pas de trace : une ligne corrigée hier ressemble à une ligne saisie hier."),
        ("cadenas", "Le doute sur ce qu'on a le droit de corriger",
         "Annuler, rembourser, rectifier une erreur : la caisse doit conserver l'opération et sa correction, jamais effacer."),
    ]),
    "/tarifs/": ("Ce qui fait grimper la facture d'une caisse", [
        ("calcul", "Le matériel imposé",
         "Terminal, tiroir, imprimante : plusieurs centaines d'euros avant la première vente. Hippopos ne vend aucun matériel."),
        ("cadenas", "L'engagement de trente-six mois",
         "Le prix affiché suppose souvent une durée, et sortir avant terme se paie."),
        ("rupture", "Ce que le tarif d'appel ne comprend pas",
         "Nombre de magasins, nombre de vendeurs, modules activables : trois raisons pour que la facture ne ressemble pas à l'annonce. Les nôtres sont écrites plus bas."),
    ]),
}

# --------------------------------------------------------------------------
# Étage 2 — les 8 pages métier d'août
# --------------------------------------------------------------------------
# couvert  : fonctions réellement au produit (lues sur la home du 15/08)
# absent   : fonctions attendues sur ce métier mais absentes du produit —
#            dites, pas masquées : c'est un signal E-E-A-T et cela évite les
#            essais qui n'aboutissent pas.

METIERS = {
    "boulangerie": dict(
        nom="boulangerie", famille="Métiers de bouche", vol=70, releve="15/08/2026",
        requete="logiciel de caisse boulangerie",
        title="Logiciel de caisse boulangerie : vente au poids et file rapide",
        desc="Baguettes à l'unité, viennoiseries au sachet, chocolats au poids : trois modes de vente sur un même ticket. Caisse NF525 dès 29 € HT par mois.",
        h1="Logiciel de caisse boulangerie : encaisser au poids sans ralentir la file",
        lede="Baguettes à l'unité, viennoiseries au sachet, chocolats en vrac au poids : "
             "trois modes de vente sur un seul ticket, en trois gestes. Votre balance "
             "reste en place, Hippopos lit le poids.",
        signature_titre="Le prix au poids n'est jamais rond",
        signature="Une caisse à touches fixes oblige à ressaisir le montant à chaque pesée. "
                  "Dix fois par heure aux heures de pointe, c'est <em>dix files qui "
                  "s'allongent</em> et autant d'occasions de se tromper.",
        couvert=[
            "Vente au poids et à la pièce sur le même ticket",
            "Touches rapides pour les produits phares du matin",
            "Lecture de la balance connectée, sans ressaisie du montant",
            "Clôtures et chaînage conformes NF525",
            "Étiquettes, codes-barres et fidélité — add-ons activables",
            "Multi-magasins : deuxième point de vente, stock et transferts — add-on",
        ],
        absent=[
            "Monnayeur automatique",
            "Commandes de pâtisseries à l'avance avec acompte",
        ],
        absent_note="Ces deux fonctions reviennent dans les résultats de « logiciel de caisse "
                    "boulangerie » relevés le 15/08/2026. Hippopos ne les couvre pas aujourd'hui.",
        ticket=("Boulangerie — 7 h 40", [
            ("Baguette tradition", "2 × 1,20 €", "2,40 €"),
            ("Croissants", "4 × 1,30 €", "5,20 €"),
            ("Chocolats en vrac", "0,340 kg × 26,00 €/kg", "8,84 €"),
        ], "16,44 €"),
        photo="metiers/boulangerie.webp",
        photo_alt="Un boulanger enfourne des pains à la pelle dans un four à bois",
        croisements=['vente-au-poids', 'etiquettes', 'multi-magasins'],
        soeurs=['patisserie', 'chocolaterie'],
    ),
    "patisserie": dict(
        nom="pâtisserie", famille="Métiers de bouche", vol=10, releve="08/08/2026",
        requete="logiciel de caisse pâtisserie",
        title="Logiciel de caisse pâtisserie : la part, la pièce et le poids",
        desc="Un entremets décliné en formats et parfums reste un seul produit au catalogue. Vente à la part, à la pièce ou au poids, conformité NF525.",
        h1="Logiciel de caisse pâtisserie : la part, la pièce et le poids sur un même ticket",
        lede="Un entremets se vend à la part, en 6 ou en 8, parfois au poids. Les variantes "
             "évitent de créer douze fiches produit pour un seul gâteau — et de perdre le "
             "suivi de stock au passage.",
        signature_titre="Un produit, douze références",
        signature="Format, parfum, nombre de parts : sans variantes, chaque combinaison "
                  "devient une fiche produit distincte. Le catalogue triple et "
                  "<em>le stock ne veut plus rien dire</em>.",
        couvert=[
            "Variantes produit : format, parfum, nombre de parts",
            "Vente à la pièce, à la part ou au poids",
            "TVA différenciée sur place et à emporter",
            "Étiquettes produit et codes-barres — add-on",
            "Clôtures et chaînage conformes NF525",
            "Fidélité : points, carte à tampons ou cashback — add-on",
            "Ticket cadeau sans les prix, pour offrir une pièce — add-on",
        ],
        absent=[
            "Commandes nominatives à l'avance avec acompte",
            "Click and collect et boutique en ligne",
        ],
        ticket=("Pâtisserie — 11 h 05", [
            ("Entremets vanille — 6 parts", "1 × 24,00 €", "24,00 €"),
            ("Éclairs chocolat", "2 × 3,50 €", "7,00 €"),
            ("Tarte citron — à la part", "3 × 2,70 €", "8,10 €"),
        ], "39,10 €"),
        photo="metiers/patisserie.webp",
        photo_alt="Une pâtissière garnit un entremets dans son laboratoire",
        croisements=['variantes-produit', 'vente-au-poids', 'etiquettes'],
        soeurs=['boulangerie', 'chocolaterie'],
    ),
    "chocolaterie": dict(
        nom="chocolaterie", famille="Métiers de bouche", vol=10, releve="08/08/2026",
        requete="logiciel de caisse chocolaterie",
        title="Logiciel de caisse chocolaterie : le poids et la saison",
        desc="Le ballotin composé se pèse, le coffret se vend à la pièce. Vente au poids, variantes et stock par magasin, conforme NF525 dès 29 € HT.",
        h1="Logiciel de caisse chocolaterie : le ballotin au poids, le coffret à la pièce",
        lede="Un client compose son ballotin, vous le pesez ; le suivant prend un coffret "
             "déjà monté. Deux façons de vendre le même chocolat, sur le même ticket, "
             "sans changer d'écran.",
        signature_titre="Trois semaines qui font l'année",
        signature="À Noël et à Pâques, le volume d'une chocolaterie se concentre sur "
                  "quelques jours. C'est le moment où <em>une rupture de stock coûte le "
                  "plus cher</em> — et où l'on a le moins de temps pour la voir venir.",
        couvert=[
            "Vente au poids : ballotin composé pesé en caisse",
            "Variantes : format de coffret, assortiment, saison",
            "Alertes de rupture et inventaires guidés",
            "Étiquettes produit et codes-barres — add-on",
            "Multi-magasins : stock indépendant et transferts — add-on",
            "Chèques cadeaux à code unique, solde suivi automatiquement — add-on",
            "Clôtures et chaînage conformes NF525",
        ],
        absent=[
            "Boutique en ligne et click and collect",
            "Commandes à l'avance avec acompte",
        ],
        ticket=("Chocolaterie — 16 h 20", [
            ("Ballotin composé", "0,250 kg × 45,00 €/kg", "11,25 €"),
            ("Coffret de Noël 100 g", "1 × 18,00 €", "18,00 €"),
            ("Orangettes", "0,120 kg × 45,00 €/kg", "5,40 €"),
        ], "34,65 €"),
        photo="metiers/chocolaterie.webp",
        photo_alt="Un artisan travaille le chocolat au comptoir de sa boutique",
        croisements=['vente-au-poids', 'multi-magasins', 'cheques-cadeaux'],
        soeurs=['patisserie', 'boulangerie'],
    ),
    "boucherie": dict(
        nom="boucherie", famille="Métiers de bouche", vol=10, releve="08/08/2026",
        requete="logiciel de caisse boucherie",
        title="Logiciel de caisse boucherie : peser et encaisser",
        desc="Prix au kilo, découpe à la demande et plat cuisiné à la pièce, sur un même ticket. Votre balance reste en place. Caisse conforme NF525.",
        h1="Logiciel de caisse boucherie : peser, découper, encaisser sans ressaisie",
        lede="Le rôti se pèse, la saucisse se compte, le plat cuisiné se vend à la part. "
             "Hippopos lit le poids depuis votre balance et le porte au ticket, sans que "
             "personne ne retape un montant.",
        signature_titre="Le montant retapé est le montant faux",
        signature="Chaque pesée ressaisie à la main est une erreur possible sur le ticket "
                  "et sur le stock. À trois cents clients par jour, <em>l'écart de caisse "
                  "du soir devient impossible à expliquer</em>.",
        couvert=[
            "Lecture de la balance connectée, prix au kilo appliqué",
            "Vente au poids et à la pièce sur le même ticket",
            "Suivi de stock par produit et par variante",
            "TVA différenciée selon les produits",
            "Clôtures, fond de caisse et chaînage NF525",
            "Comptes vendeurs et permissions par code PIN",
        ],
        absent=[
            "Commandes à l'avance avec acompte",
            "Boutique en ligne et click and collect",
        ],
        ticket=("Boucherie — 10 h 15", [
            ("Rôti de bœuf", "1,240 kg × 20,00 €/kg", "24,80 €"),
            ("Saucisses de Toulouse", "6 × 1,20 €", "7,20 €"),
            ("Bœuf bourguignon — à la part", "2 × 5,50 €", "11,00 €"),
        ], "43,00 €"),
        photo="metiers/boucherie.webp",
        photo_alt="Deux bouchers préparent des morceaux de viande dans leur atelier",
        croisements=['vente-au-poids', 'comptes-vendeurs', 'cloture-de-caisse'],
        soeurs=['charcuterie', 'poissonnerie'],
    ),
    "charcuterie": dict(
        nom="charcuterie", famille="Métiers de bouche", vol=10, releve="08/08/2026",
        requete="logiciel de caisse charcuterie",
        title="Logiciel de caisse charcuterie : le poids, la tranche et le plat",
        desc="Jambon à la tranche, terrine au poids, plat cuisiné à la part : trois façons de vendre, un seul ticket, une caisse conforme NF525.",
        h1="Logiciel de caisse charcuterie : le poids, la tranche et le plat cuisiné",
        lede="On vend à la tranche, au poids et à la part dans la même minute. La caisse "
             "doit suivre les trois sans changer de mode, et sortir un ticket juste du "
             "premier coup.",
        signature_titre="Trois unités de vente, un seul client",
        signature="Le même client repart avec du jambon pesé, six tranches comptées et une "
                  "terrine à la part. Une caisse qui ne gère qu'une unité de vente "
                  "<em>oblige à faire trois tickets</em>.",
        couvert=[
            "Vente au poids, à la pièce et à la part sur un même ticket",
            "Lecture de la balance connectée",
            "TVA différenciée selon les produits",
            "Suivi de stock par produit et par variante",
            "Clôtures et chaînage conformes NF525",
            "Étiquettes produit et codes-barres — add-on",
        ],
        absent=[
            "Commandes à l'avance avec acompte",
            "Click and collect et boutique en ligne",
        ],
        ticket=("Charcuterie — 12 h 30", [
            ("Jambon blanc", "6 tranches × 0,90 €", "5,40 €"),
            ("Terrine de campagne", "0,320 kg × 19,00 €/kg", "6,08 €"),
            ("Quiche lorraine — à la part", "2 × 2,80 €", "5,60 €"),
        ], "17,08 €"),
        photo="metiers/charcuterie.webp",
        photo_alt="Un charcutier derrière son comptoir, devant les pièces suspendues",
        croisements=['vente-au-poids', 'variantes-produit', 'etiquettes'],
        soeurs=['boucherie', 'traiteur'],
    ),
    "poissonnerie": dict(
        nom="poissonnerie", famille="Métiers de bouche", vol=10, releve="08/08/2026",
        requete="logiciel de caisse poissonnerie",
        title="Logiciel de caisse poissonnerie : le prix au kilo du jour",
        desc="Le cours change avec l'arrivage : le prix au kilo se corrige en caisse, pas sur une étiquette de la veille. Vente au poids, NF525.",
        h1="Logiciel de caisse poissonnerie : un prix au kilo qui change avec l'arrivage",
        lede="Le cours du matin décide du prix de la journée. Le tarif se corrige en caisse "
             "en quelques secondes, et le ticket comme le stock suivent immédiatement.",
        signature_titre="Le prix de ce matin n'est pas celui d'hier",
        signature="Une caisse dont les prix se changent une fois par saison ne tient pas un "
                  "étal. Ici le tarif bouge à l'arrivage, et <em>chaque heure de retard se "
                  "paie sur la marge</em>.",
        couvert=[
            "Prix au kilo modifiable en caisse, effet immédiat",
            "Lecture de la balance connectée",
            "Vente au poids et à la pièce",
            "Suivi de stock et inventaires guidés",
            "Clôtures, fond de caisse et chaînage NF525",
            "Étiquettes produit réimprimables — add-on",
        ],
        absent=[
            "Commandes à l'avance avec acompte",
            "Boutique en ligne et click and collect",
        ],
        ticket=("Poissonnerie — 9 h 50", [
            ("Filet de bar", "0,480 kg × 28,00 €/kg", "13,44 €"),
            ("Moules de bouchot", "1,000 kg × 4,90 €/kg", "4,90 €"),
            ("Crevettes cuites", "0,300 kg × 29,00 €/kg", "8,70 €"),
        ], "27,04 €"),
        photo="metiers/poissonnerie.webp",
        photo_alt="Un poissonnier rafraîchit son étal de poissons sur glace",
        croisements=['vente-au-poids', 'cloture-de-caisse', 'etiquettes'],
        soeurs=['boucherie', 'charcuterie'],
    ),
    "traiteur": dict(
        nom="traiteur", famille="Métiers de bouche", vol=10, releve="08/08/2026",
        requete="logiciel de caisse traiteur",
        title="Logiciel de caisse traiteur : au poids, au plat, à emporter",
        desc="Barquettes pesées, plats à la part, TVA sur place et à emporter : la vente au comptoir tient sur une seule caisse conforme NF525.",
        h1="Logiciel de caisse traiteur : vendre au poids, au plat et à emporter",
        lede="La barquette se pèse, le plat se compte, et la TVA n'est pas la même selon que "
             "le client consomme sur place ou emporte. Hippopos couvre la vente au comptoir.",
        signature_titre="Sur place ou à emporter, ce n'est pas la même TVA",
        signature="Le taux dépend du mode de consommation, pas du produit. Une caisse qui ne "
                  "sait pas poser la question <em>fausse la déclaration tous les mois</em>.",
        couvert=[
            "Vente au poids, à la part et à la pièce",
            "TVA différenciée sur place et à emporter",
            "Lecture de la balance connectée",
            "Suivi de stock par produit et par variante",
            "Clôtures et chaînage conformes NF525",
            "Comptes vendeurs et permissions par code PIN",
        ],
        absent=[
            "Commandes de réception à l'avance avec acompte et devis",
            "Click and collect et boutique en ligne",
            "Écran cuisine et plan de salle",
        ],
        absent_note="Hippopos couvre la vente au comptoir d'un traiteur, pas l'activité de "
                    "réception sur devis. C'est dit ici pour éviter un essai qui n'aboutira pas.",
        ticket=("Traiteur — 11 h 45", [
            ("Salade piémontaise", "0,400 kg × 15,00 €/kg", "6,00 €"),
            ("Lasagnes — à la part", "2 × 5,50 €", "11,00 €"),
            ("Terrine de légumes", "0,180 kg × 24,00 €/kg", "4,32 €"),
        ], "21,32 €"),
        photo="metiers/traiteur.webp",
        photo_alt="Un traiteur garnit des bouchées avant le service",
        croisements=['vente-au-poids', 'variantes-produit', 'comptes-vendeurs'],
        soeurs=['charcuterie', 'boucherie'],
    ),
    "epicerie": dict(
        nom="épicerie", famille="Commerce de détail", vol=70, releve="07/08/2026",
        requete="logiciel de caisse épicerie",
        title="Logiciel de caisse épicerie : catalogue large, scanné et suivi",
        desc="Des centaines de références, du vrac au poids et des codes-barres à la douchette. Stock suivi et caisse NF525, dès 29 € HT par mois.",
        h1="Logiciel de caisse épicerie : un catalogue large, scanné et suivi",
        lede="Huit cents références en rayon, du vrac au poids, des lots à codes-barres : "
             "l'épicerie est le métier où le catalogue déborde le plus vite. Le scan et les "
             "variantes le tiennent.",
        signature_titre="Huit cents références, deux mètres de comptoir",
        signature="Chercher un produit à l'écran pendant que la file avance n'est pas une "
                  "option. La douchette et les touches rapides <em>ramènent l'encaissement "
                  "à un geste</em>.",
        couvert=[
            "Scan par douchette code-barres ou caméra",
            "Vente au poids pour le vrac, à la pièce pour le reste",
            "Variantes produit : contenance, parfum, lot",
            "Suivi de stock, alertes de rupture, inventaires guidés",
            "Multi-magasins : stock indépendant et transferts — add-on",
            "Clôtures et chaînage conformes NF525",
        ],
        absent=[
            "Boutique en ligne et click and collect",
            "Commandes à l'avance avec acompte",
        ],
        ticket=("Épicerie — 18 h 10", [
            ("Riz basmati 1 kg", "1 × 3,90 €", "3,90 €"),
            ("Amandes en vrac", "0,250 kg × 25,00 €/kg", "6,25 €"),
            ("Huile d'olive 75 cl", "1 × 9,80 €", "9,80 €"),
        ], "19,95 €"),
        photo="metiers/epicerie.webp",
        photo_alt="Un épicier réapprovisionne les fruits et légumes dans son rayon",
        croisements=['gestion-de-stock', 'inventaire-guide', 'multi-magasins'],
        soeurs=['chocolaterie', 'traiteur'],
    ),
}

# Déclinaisons de l'étage 3 — prévues, pas encore publiées (roadmap septembre+).
# Rendues en cartes inactives : jamais un lien vers une page qui n'existe pas.
DECLINAISONS = [
    ("Combien ça coûte", "Le budget d'une caisse, poste par poste.", "prix"),
    ("La conformité", "Ce que la norme impose à ce métier.", "nf525"),
    ("Changer de caisse", "Reprendre son catalogue sans fermer la boutique.", "migration"),
]

# FAQ du silo métiers — questions générales. Les questions propres à un métier
# vivent sur la page du métier : aucune question n'apparaît deux fois.
FAQ_SILO_METIERS = [
    ("Mon métier n'est pas dans la liste, puis-je quand même utiliser Hippopos ?",
     "Oui, si vous vendez en boutique, à la pièce, au poids ou par variantes. Hippopos ne "
     "couvre pas la restauration servie en salle — il n'y a ni écran cuisine ni plan de "
     "salle — ni la prise de rendez-vous."),
    ("Faut-il changer de matériel ?",
     "Non. Douchette code-barres, balance et imprimante ticket déjà en place restent "
     "compatibles. Hippopos fonctionne dans le navigateur, sur tablette, ordinateur ou "
     "terminal tactile."),
    ("Puis-je ouvrir un second magasin plus tard ?",
     "Oui. Le catalogue reste centralisé, chaque magasin garde son propre stock, sa propre "
     "caisse et ses propres clôtures, et le stock se transfère d'un magasin à l'autre en "
     "envoi puis réception."),
    ("Combien de temps pour être opérationnel ?",
     "Le jour même : création du compte sans carte bancaire, import du catalogue, réglage "
     "de la TVA, des moyens de paiement et du ticket, puis encaissement."),
]
