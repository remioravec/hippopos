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
