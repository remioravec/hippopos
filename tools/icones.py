"""Jeu d'icônes SVG du site — trait 1,75, grille 24, `currentColor`.

Remplace les emoji, signalés comme défaut par la checklist UI (« No emojis as
icons »). Tout est inline : aucune requête réseau, aucune dépendance, et
l'icône hérite de la couleur du contexte.
"""

_ENVELOPPE = (
    '<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" '
    'aria-hidden="true" focusable="false">{}</svg>'
)

_TRACES = {
    # Caisse tactile — un terminal sur pied
    "caisse-tactile":
        '<rect x="3" y="3" width="18" height="12" rx="2"/>'
        '<path d="M7 19h10M12 15v4"/><path d="M7 7h5M7 10.5h3"/>',
    # Conformité — bouclier validé
    "conformite":
        '<path d="M12 3l7 3v5c0 4.4-2.9 7.4-7 8.9C7.9 18.4 5 15.4 5 11V6l7-3z"/>'
        '<path d="M9 11.5l2 2 4-4"/>',
    # Stock — carton
    "stock":
        '<path d="M3.5 7.5L12 3l8.5 4.5v9L12 21l-8.5-4.5v-9z"/>'
        '<path d="M3.5 7.5L12 12l8.5-4.5M12 12v9"/>',
    # Clôtures — billets
    "clotures":
        '<rect x="2.5" y="6" width="19" height="12" rx="2"/>'
        '<circle cx="12" cy="12" r="2.5"/><path d="M6 12h.01M18 12h.01"/>',
    # Équipe — deux personnes
    "equipe":
        '<circle cx="9" cy="8" r="3"/>'
        '<path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/>'
        '<path d="M16 5.3a3 3 0 0 1 0 5.4M17.5 14.4A6 6 0 0 1 21 20"/>',
    # Tickets — ticket dentelé
    "tickets":
        '<path d="M6 3h12a1 1 0 0 1 1 1v17l-2.5-1.6L14 21l-2-1.6L10 21l-2.5-1.6L5 21V4a1 1 0 0 1 1-1z"/>'
        '<path d="M9 8h6M9 12h6M9 16h3"/>',
    # Multi-magasins — devanture
    "multi-magasins":
        '<path d="M4 9.5V20h16V9.5"/>'
        '<path d="M2.5 9.5L4.5 4h15l2 5.5a3 3 0 0 1-5.8 1 3 3 0 0 1-5.8 0 3 3 0 0 1-5.8-1z"/>'
        '<path d="M10 20v-5h4v5"/>',
    # Fidélité — carte à tampon
    "fidelite":
        '<rect x="2.5" y="5" width="19" height="14" rx="2"/>'
        '<circle cx="8" cy="12" r="1.6"/><circle cx="12" cy="12" r="1.6"/>'
        '<path d="M16.4 12h.01"/>',
    # Étiquettes — étiquette et son œillet
    "etiquettes":
        '<path d="M20.6 12.6l-8 8a2 2 0 0 1-2.8 0l-6.4-6.4A2 2 0 0 1 3 12.8V5a2 2 0 0 1 2-2h7.8a2 2 0 0 1 1.4.6l6.4 6.4a2 2 0 0 1 0 2.8z"/>'
        '<circle cx="8" cy="8" r="1.4"/>',
    # Chèques cadeaux — coffret et ruban
    "cheques-cadeaux":
        '<rect x="3" y="9" width="18" height="12" rx="1.5"/>'
        '<path d="M2 9h20M12 9v12"/>'
        '<path d="M12 9C10.5 6 9 3.5 7.2 4.2 5.4 4.9 6.3 8 12 9zM12 9c1.5-3 3-5.5 4.8-4.8C18.6 4.9 17.7 8 12 9z"/>',
    # Vente au poids — balance
    "poids":
        '<path d="M12 4v16M8 20h8"/>'
        '<path d="M5 8h14l-2.5-3h-9L5 8z"/>'
        '<path d="M3 12a3 3 0 0 0 6 0l-3-4-3 4zM15 12a3 3 0 0 0 6 0l-3-4-3 4z"/>',
    # Variantes — cases déclinées
    "variantes":
        '<rect x="3" y="3" width="7.5" height="7.5" rx="1.5"/>'
        '<rect x="13.5" y="3" width="7.5" height="7.5" rx="1.5"/>'
        '<rect x="3" y="13.5" width="7.5" height="7.5" rx="1.5"/>'
        '<path d="M17.25 13.5v7.5M13.5 17.25h7.5"/>',

    # ---- Peurs et frustrations ------------------------------------------
    # Une icône par contrainte de comptoir, pour que la peur se lise avant le
    # texte — la section était un paragraphe centré, elle devient trois cartes.
    "horloge":
        '<circle cx="12" cy="12" r="9"/><path d="M12 7v5.2l3.2 2"/>',
    "alerte":
        '<path d="M10.3 3.9L2.6 17.2A2 2 0 0 0 4.3 20.2h15.4a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/>'
        '<path d="M12 9.5v4M12 16.8v.01"/>',
    "calcul":
        '<rect x="4" y="2.5" width="16" height="19" rx="2"/>'
        '<path d="M8 6.5h8"/><path d="M8.5 11h.01M12 11h.01M15.5 11h.01"/>'
        '<path d="M8.5 14.5h.01M12 14.5h.01M15.5 14.5h.01"/><path d="M8.5 18h3.5M15.5 18h.01"/>',
    "controle":
        '<path d="M13.5 2.5H7a2 2 0 0 0-2 2v15a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/>'
        '<path d="M13.5 2.5V8H19"/><circle cx="11.5" cy="14" r="2.6"/><path d="M13.4 15.9L16 18.5"/>',
    "rupture":
        '<path d="M3.5 7.5L12 3l8.5 4.5v9L12 21l-8.5-4.5v-9z"/>'
        '<path d="M3.5 7.5L12 12l8.5-4.5M12 12v9"/><path d="M12 6.5v.01"/>',
    "oeil":
        '<path d="M2 12s3.6-6.5 10-6.5S22 12 22 12s-3.6 6.5-10 6.5S2 12 2 12z"/>'
        '<circle cx="12" cy="12" r="2.8"/>',
    "cadenas":
        '<rect x="4" y="10" width="16" height="11" rx="2"/>'
        '<path d="M8 10V7a4 4 0 0 1 8 0v3"/><path d="M12 14.5v2.5"/>',
    "calendrier":
        '<rect x="3" y="5" width="18" height="16" rx="2"/>'
        '<path d="M3 9.5h18M8 3v4M16 3v4"/><path d="M7.5 13.5h3v3h-3z"/>',

    # ---- Métiers -------------------------------------------------------
    "m-boulangerie":
        '<path d="M4.5 15.5c-1.4-1.4-1.4-3.6 0-5l6-6c1.4-1.4 3.6-1.4 5 0l3.5 3.5c1.4 1.4 1.4 3.6 0 5l-6 6c-1.4 1.4-3.6 1.4-5 0z"/>'
        '<path d="M8.5 8.5l3 3M11.5 5.5l3 3M5.5 11.5l3 3"/>',
    "m-patisserie":
        '<path d="M4 20h16v-6a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4z"/>'
        '<path d="M4 15c1.6 0 1.6 1.5 3.2 1.5S8.8 15 10.4 15s1.6 1.5 3.2 1.5S15.2 15 16.8 15s1.6 1.5 3.2 1.5"/>'
        '<path d="M12 10V6M12 4.5v.01"/>',
    "m-chocolaterie":
        '<rect x="4" y="4" width="16" height="16" rx="2"/>'
        '<path d="M4 9.3h16M4 14.6h16M9.3 4v16M14.6 4v16"/>',
    "m-boucherie":
        '<path d="M14.5 3.5l5 5-9 9a4.5 4.5 0 0 1-6.4-6.4z"/>'
        '<path d="M6 15.5a2 2 0 1 0 2.8 2.8"/><path d="M17 6l3.5-2.5"/>',
    "m-charcuterie":
        '<path d="M5.5 5.5c6 0 13 7 13 13a4 4 0 0 1-4-4c0-3.9-5.1-9-9-9z" />'
        '<path d="M4 4.2a2 2 0 1 1 2.8 2.8M19.8 20a2 2 0 1 0-2.8-2.8"/>'
        '<path d="M9 9.5l.01.01M12 12.5l.01.01M14.5 16l.01.01"/>',
    "m-poissonnerie":
        '<path d="M2.5 12c3-4.5 7-6.5 10.5-6.5S19.5 8 21.5 12c-2 4-5 6.5-8.5 6.5S5.5 16.5 2.5 12z"/>'
        '<path d="M21.5 12c0-2 .5-3.5 0-4.5-1 .5-2.3 1.6-3 2.6M9 11.5h.01"/>'
        '<path d="M13 5.5c-.5 2-.5 11 0 13"/>',
    "m-traiteur":
        '<path d="M3 15h18a9 9 0 0 0-18 0z"/><path d="M2 18.5h20"/>'
        '<path d="M12 6V4.5M10.5 4.5h3"/>',
    "m-epicerie":
        '<path d="M3 7h18l-1.8 11.2a2 2 0 0 1-2 1.8H6.8a2 2 0 0 1-2-1.8z"/>'
        '<path d="M8.5 7V5.5a3.5 3.5 0 0 1 7 0V7"/><path d="M9.5 11.5v4M14.5 11.5v4"/>',
    # Métier sans page dédiée — devanture générique, pour que la colonne
    # du menu reste alignée quand l'icône métier n'existe pas encore.
    "m-generique":
        '<path d="M4.5 10.5V20h15v-9.5"/>'
        '<path d="M3 10.5l1.8-5.5h14.4l1.8 5.5"/>'
        '<path d="M3 10.5h18"/><path d="M9.5 20v-5.5h5V20"/>',
    # Matériel — douchette
    "douchette":
        '<path d="M4 5v14M7 5v14M10.5 5v14M14 5v14M17.5 5v10"/>'
        '<path d="M20 15.5l-2.5 5.5"/>',
    # Matériel — imprimante
    "imprimante":
        '<path d="M7 9V4h10v5"/>'
        '<rect x="3" y="9" width="18" height="7" rx="1.5"/>'
        '<path d="M7 14h10v6H7z"/>',
}


def ico(cle):
    """Renvoie le SVG inline de l'icône, ou une chaîne vide si elle n'existe pas."""
    trace = _TRACES.get(cle)
    return _ENVELOPPE.format(trace) if trace else ""
