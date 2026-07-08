"""Localized texts for backend notifications.

Backend-generated persistent notifications cannot use the frontend
translation system, so we pick the language from hass.config.language
with English fallback.
"""
from __future__ import annotations

TEXTS: dict[str, dict[str, str]] = {
    "en": {
        "title": "Huawei Fusion Hub",
        "summary": (
            "Discovery completed: **{total} entities** created ({counts}).\n\n"
            "Entities matched per source: {per_source}."
        ),
        "rediscovery_new": "**{n} new entities** created ({counts})",
        "rediscovery_gained": (
            "**{n} existing entities** gained an additional fallback source"
        ),
        "rediscovery": "New data detected from {sources}: {parts}.",
        "offline": (
            "Source **{name}** is offline. "
            "Values are now served by the next available source."
        ),
        "online": "Source **{name}** is back online.",
    },
    "it": {
        "title": "Huawei Fusion Hub",
        "summary": (
            "Discovery completata: **{total} entità** create ({counts}).\n\n"
            "Entità abbinate per sorgente: {per_source}."
        ),
        "rediscovery_new": "**{n} nuove entità** create ({counts})",
        "rediscovery_gained": (
            "**{n} entità esistenti** hanno guadagnato una sorgente di fallback"
        ),
        "rediscovery": "Nuovi dati rilevati da {sources}: {parts}.",
        "offline": (
            "La sorgente **{name}** è offline. "
            "I valori vengono ora forniti dalla successiva sorgente disponibile."
        ),
        "online": "La sorgente **{name}** è di nuovo online.",
    },
}


def get_texts(hass) -> dict[str, str]:
    lang = (hass.config.language or "en").split("-")[0].lower()
    return TEXTS.get(lang, TEXTS["en"])
