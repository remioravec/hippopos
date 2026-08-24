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
        photo_alt="Vitrine de boulangerie garnie de pains et de viennoiseries",
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
        photo_alt="Entremets et pâtisseries alignés en vitrine réfrigérée",
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
        photo_alt="Assortiment de chocolats et pralines dans son coffret",
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
        photo_alt="Comptoir réfrigéré de boucherie garni de pièces de viande",
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
        photo_alt="Rayon de fruits et légumes d'une épicerie",
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
