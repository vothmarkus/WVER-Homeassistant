"""Constants for the WVER integration."""
from __future__ import annotations

from datetime import timedelta

DOMAIN = "wver"
NAME = "WVER"
MANUFACTURER = "Wasserverband Eifel-Rur"
DEFAULT_SCAN_INTERVAL = timedelta(minutes=15)

CONF_SCAN_INTERVAL = "scan_interval"

INTERESTING_SIGNALS: set[str] = {
    "wasserstand",
    "abfluss",
    "abgabe",
    "zufluss",
    "wasserstand_seit_wwj2001",
    "wasserstand_hauptsee_seit_wwj2001",
    "wasserstand_hauptsee",
    "abgabe_hauptsee",
    "zufluss_obersee",
    "wasserstand_obersee",
}

SIGNAL_TRANSLATIONS: dict[str, str] = {
    "wasserstand": "Wasserstand",
    "abfluss": "Abfluss",
    "abgabe": "Abgabe",
    "zufluss": "Zufluss",
    "wasserstand_seit_wwj2001": "Wasserstand seit WWJ 2001",
    "wasserstand_hauptsee_seit_wwj2001": "Wasserstand Hauptsee seit WWJ 2001",
    "wasserstand_hauptsee": "Wasserstand Hauptsee",
    "abgabe_hauptsee": "Abgabe Hauptsee",
    "zufluss_obersee": "Zufluss Obersee",
    "wasserstand_obersee": "Wasserstand Obersee",
}

SIGNAL_ICONS: dict[str, str] = {
    "wasserstand": "mdi:waves-arrow-up",
    "abfluss": "mdi:waves-arrow-right",
    "abgabe": "mdi:waves-arrow-right",
    "zufluss": "mdi:waves-arrow-left",
    "wasserstand_seit_wwj2001": "mdi:waves-arrow-up",
    "wasserstand_hauptsee_seit_wwj2001": "mdi:waves-arrow-up",
    "wasserstand_hauptsee": "mdi:waves-arrow-up",
    "abgabe_hauptsee": "mdi:waves-arrow-right",
    "zufluss_obersee": "mdi:waves-arrow-left",
    "wasserstand_obersee": "mdi:waves-arrow-up",
}
