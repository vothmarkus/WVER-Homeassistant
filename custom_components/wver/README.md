# WVER Custom Integration for Home Assistant

Diese Custom-Integration liest WVER-Messwerte für die konfigurierten Stationen aus und stellt pro Station und interessantem Signal eigene Sensoren bereit.

## Enthaltene Stationen
- Stb. Heimbach UW
- Stb. Obermaubach UW
- Rur Monschau LANUK
- Rur Dedenborn
- Rurtalsperre Schwammenauel
- Urfttalsperre

## Enthaltene Signale
- wasserstand
- abfluss
- abgabe
- zufluss
- wasserstand_seit_wwj2001
- wasserstand_hauptsee_seit_wwj2001
- wasserstand_hauptsee
- abgabe_hauptsee
- zufluss_obersee
- wasserstand_obersee

## Installation
1. Ordner `custom_components/wver` nach `/config/custom_components/wver` kopieren.
2. Home Assistant neu starten.
3. Unter **Einstellungen -> Geräte & Dienste -> Integration hinzufügen** nach **WVER** suchen.
4. Namen und Aktualisierungsintervall festlegen.

## Attribute
Jeder Sensor bringt zusätzliche Attribute mit:
- `station`
- `station_key`
- `signal`
- `timestamp`
- `absolute_value`
- `source_url`
- `parser`
- `page_url`

## Hinweise
- Wasserstand wird, wenn keine Einheit geliefert wird, als `cm` interpretiert.
- Abfluss, Abgabe und Zufluss werden, wenn keine Einheit geliefert wird, als `m³/s` interpretiert.
- Einzelne fehlerhafte Signale blockieren die übrigen Sensoren nicht.
