# WVER für Home Assistant

Custom-Integration für Home Assistant zum Abruf von Messwerten des **Wasserverbands Eifel-Rur (WVER)**.  
Die Integration fragt die hinterlegten WVER-Stationen regelmäßig ab und stellt die Messwerte als Sensoren in Home Assistant bereit.

## Funktionen

- Abfrage mehrerer WVER-Stationen über die vorhandenen JSON-Endpunkte
- Ein Gerät pro Station in Home Assistant
- Ein Sensor pro relevantem Signal
- Zentrale Aktualisierung per `DataUpdateCoordinator`
- Konfiguration über die Home-Assistant-Oberfläche
- Automatische Ergänzung fehlender Einheiten für bekannte Signaltypen
- Robuste Verarbeitung: einzelne fehlerhafte Signale blockieren die übrigen Sensoren nicht

## Enthaltene Stationen

Aktuell sind diese Stationen in der Integration hinterlegt:

- Stb. Heimbach UW
- Stb. Obermaubach UW
- Rur Monschau LANUK
- Rur Dedenborn
- Rurtalsperre Schwammenauel
- Urfttalsperre

## Unterstützte Signale

Die Integration legt Sensoren für folgende Signaltypen an, sofern sie an der jeweiligen Station vorhanden sind:

- `wasserstand`
- `abfluss`
- `abgabe`
- `zufluss`
- `wasserstand_seit_wwj2001`
- `wasserstand_hauptsee_seit_wwj2001`
- `wasserstand_hauptsee`
- `abgabe_hauptsee`
- `zufluss_obersee`
- `wasserstand_obersee`

## Einheiten

Falls der WVER-Endpunkt keine Einheit liefert, ergänzt die Integration bekannte Einheiten automatisch:

- `wasserstand*` → `cm`
- `abfluss`, `abgabe`, `zufluss` → `m³/s`

## Installation

### Manuell

1. Dieses Repository herunterladen oder klonen.
2. Den Ordner `custom_components/wver` nach folgendem Ziel kopieren:

   ```text
   /config/custom_components/wver
   ```

3. Home Assistant neu starten.
4. In Home Assistant öffnen:

   **Einstellungen → Geräte & Dienste → Integration hinzufügen**

5. Nach **WVER** suchen und die Integration hinzufügen.
6. Namen und Aktualisierungsintervall festlegen.

## Konfiguration

Die Integration wird über die Benutzeroberfläche eingerichtet. Derzeit gibt es folgende Optionen:

- **Name** der Integration
- **Aktualisierungsintervall** in Minuten

Aktuell ist die Integration als **Single Instance** ausgelegt, also nur einmal pro Home-Assistant-Instanz konfigurierbar.

## Entitäten

Für jede Station wird ein Gerät angelegt.  
Für jedes unterstützte Signal dieser Station wird eine Sensor-Entität erstellt.

Beispielhafte Entitäten:

- `sensor.stb_heimbach_uw_wasserstand`
- `sensor.stb_heimbach_uw_abfluss`
- `sensor.rurtalsperre_schwammenauel_abgabe`

Die tatsächlichen Entity-IDs hängen von der Namensnormalisierung in Home Assistant ab.

## Zusätzliche Attribute

Jeder Sensor stellt neben dem Messwert weitere Attribute bereit:

- `station`
- `station_key`
- `signal`
- `timestamp`
- `absolute_value`
- `source_url`
- `parser`
- `page_url`

## Projektstruktur

```text
custom_components/wver/
├── __init__.py
├── api.py
├── config_flow.py
├── const.py
├── coordinator.py
├── entity.py
├── manifest.json
├── sensor.py
├── wver_stationen.py
└── translations/
    ├── de.json
    └── en.json
```

## Technischer Aufbau

Die Integration besteht aus drei zentralen Bausteinen:

- **`api.py`**  
  HTTP-Abruf und Parsen der WVER-Daten
- **`coordinator.py`**  
  Zentrale Datenerneuerung über den Home-Assistant-`DataUpdateCoordinator`
- **`sensor.py`**  
  Erzeugung der Sensor-Entities auf Basis der geladenen Stations- und Signaldaten

Die bestehende Logik aus dem ursprünglichen Python-Skript wurde dabei in eine Home-Assistant-konforme Struktur überführt.

## Hinweise

- Die Stationen sind aktuell statisch in `wver_stationen.py` definiert.
- Nicht jedes Signal ist an jeder Station vorhanden.
- Wenn ein einzelner Abruf fehlschlägt, bleiben die übrigen Sensoren weiterhin verfügbar.
- Die Integration ist als Custom-Component gedacht und nicht Teil des offiziellen Home-Assistant-Core.

## Geplante Erweiterungen

Mögliche nächste Ausbaustufen:

- Auswahl einzelner Stationen über den Options-Dialog
- Auswahl einzelner Signale
- Diagnosedaten
- bessere Klassifizierung von Sensoren
- HACS-Unterstützung
- Branding für den Integrationsdialog

## Entwicklung

Zum lokalen Testen:

1. Repository in eine Testinstanz von Home Assistant einbinden.
2. Ordner `custom_components/wver` in das Config-Verzeichnis kopieren.
3. Home Assistant neu starten.
4. Logs in Home Assistant prüfen.

## Haftungsausschluss

Diese Integration ist ein inoffizielles Projekt.  
Es besteht keine Verbindung zum Wasserverband Eifel-Rur oder zu Home Assistant.

## Lizenz

MIT.
