"""API client for the WVER integration."""
from __future__ import annotations

import asyncio
import json
import logging
import re
from typing import Any
import urllib.request

from .const import INTERESTING_SIGNALS
from .wver_stationen import WVER_STATIONS

_LOGGER = logging.getLogger(__name__)

RANGE_BYTES = 8192
PAIR_PATTERN = re.compile(r'\["([^"]+)",\s*([0-9.+-]+)\]')


class WverApiClient:
    """Small API client for WVER JSON endpoints."""

    def __init__(self) -> None:
        self._timeout = 30

    async def async_fetch_all(self) -> dict[str, Any]:
        """Fetch all configured stations and signals."""
        return await asyncio.to_thread(self._fetch_all)

    def _fetch_all(self) -> dict[str, Any]:
        results: dict[str, Any] = {}

        for station_key, station in WVER_STATIONS.items():
            station_results: dict[str, Any] = {}

            for signal_key, url in station["signals"].items():
                if signal_key not in INTERESTING_SIGNALS:
                    continue

                try:
                    result = self._extract_signal(signal_key, url)
                    unit = self._infer_unit(signal_key, result["unit"])
                    station_results[signal_key] = {
                        "timestamp": result["timestamp"],
                        "value": result["value"],
                        "absolute_value": result["absolute_value"],
                        "unit": unit,
                        "url": url,
                        "parser": result["parser"],
                    }
                except Exception as err:  # noqa: BLE001
                    _LOGGER.warning(
                        "Error fetching %s/%s from %s: %s",
                        station_key,
                        signal_key,
                        url,
                        err,
                    )
                    station_results[signal_key] = {
                        "error": str(err),
                        "url": url,
                    }

            results[station_key] = {
                "name": station["name"],
                "page_url": station["page_url"],
                "primary_signal": station["primary_signal"],
                "signals": station_results,
            }

        return results

    def _fetch_text_range(self, url: str, range_bytes: int = RANGE_BYTES) -> str:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Range": f"bytes=-{range_bytes}",
            },
        )
        with urllib.request.urlopen(req, timeout=self._timeout) as response:
            return response.read().decode("utf-8", errors="replace")

    def _fetch_json_full(self, url: str) -> Any:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=self._timeout) as response:
            return json.loads(response.read().decode("utf-8", errors="replace"))

    @staticmethod
    def _normalize_unit(unit: str | None) -> str | None:
        if unit is None:
            return None
        return str(unit).replace("m�/s", "m³/s").replace("m?/s", "m³/s")

    @staticmethod
    def _infer_unit(signal_key: str, current_unit: str | None) -> str | None:
        if current_unit:
            return current_unit
        if "wasserstand" in signal_key:
            return "cm"
        if any(key in signal_key for key in ("abfluss", "abgabe", "zufluss")):
            return "m³/s"
        return None

    @staticmethod
    def _to_float_or_none(value: Any) -> float | None:
        if value in (None, "", "-"):
            return None
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    def _parse_pegel_tail(self, url: str) -> dict[str, Any]:
        text = self._fetch_text_range(url)
        matches = PAIR_PATTERN.findall(text)
        if not matches:
            raise ValueError("Kein [timestamp, value]-Paar im Tail gefunden")

        ts, value = matches[-1]
        return {
            "timestamp": ts,
            "value": float(value),
            "absolute_value": None,
            "unit": None,
            "parser": "range_tail",
        }

    def _parse_talsperre_json(self, url: str) -> dict[str, Any]:
        obj = self._fetch_json_full(url)

        columns_raw = obj.get("columns")
        data = obj.get("data", [])
        unit = self._normalize_unit(obj.get("ts_unitsymbol"))

        if not columns_raw or not data:
            raise ValueError("JSON enthält keine brauchbaren columns/data")

        columns = [c.strip() for c in columns_raw.split(",")] if isinstance(columns_raw, str) else list(columns_raw)

        ts_idx = columns.index("Timestamp")
        val_idx = columns.index("Value")
        abs_idx = columns.index("Absolute Value") if "Absolute Value" in columns else None

        for row in reversed(data):
            ts = row[ts_idx]
            value = self._to_float_or_none(row[val_idx])
            abs_value = self._to_float_or_none(row[abs_idx]) if abs_idx is not None else None

            if value is not None:
                return {
                    "timestamp": ts,
                    "value": value,
                    "absolute_value": abs_value,
                    "unit": unit,
                    "parser": "full_json_last_valid",
                }

        raise ValueError("Kein gültiger numerischer Wert in data gefunden")

    def _extract_signal(self, signal_key: str, url: str) -> dict[str, Any]:
        if any(
            key in signal_key
            for key in (
                "wasserstand_seit_wwj2001",
                "wasserstand_hauptsee_seit_wwj2001",
                "wasserstand_hauptsee",
                "abgabe_hauptsee",
                "zufluss_obersee",
                "wasserstand_obersee",
                "abgabe",
                "zufluss",
            )
        ) or "Tag.Mittel.json" in url or "Tag.Summe.json" in url or "seitWWJ2001" in url:
            return self._parse_talsperre_json(url)

        return self._parse_pegel_tail(url)
