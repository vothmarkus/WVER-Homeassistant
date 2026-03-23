"""Sensor platform for WVER."""
from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfLength
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, SIGNAL_ICONS, SIGNAL_TRANSLATIONS
from .entity import WverCoordinatorEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities: list[WverSensor] = []

    for station_key, station_data in coordinator.data.items():
        for signal_key, signal_data in station_data["signals"].items():
            if "error" in signal_data:
                continue
            entities.append(WverSensor(coordinator, station_key, station_data, signal_key))

    async_add_entities(entities)


class WverSensor(WverCoordinatorEntity, SensorEntity):
    """Representation of a WVER sensor."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator,
        station_key: str,
        station_data: dict[str, Any],
        signal_key: str,
    ) -> None:
        super().__init__(coordinator, station_key, station_data)
        self.signal_key = signal_key
        self._attr_translation_key = signal_key
        self._attr_name = SIGNAL_TRANSLATIONS.get(signal_key, signal_key.replace("_", " ").title())
        self._attr_unique_id = f"{station_key}_{signal_key}"
        self._attr_icon = SIGNAL_ICONS.get(signal_key)

    @property
    def _signal(self) -> dict[str, Any] | None:
        return self.coordinator.data.get(self.station_key, {}).get("signals", {}).get(self.signal_key)

    @property
    def native_value(self) -> float | None:
        signal = self._signal
        if not signal or "error" in signal:
            return None
        return signal.get("value")

    @property
    def native_unit_of_measurement(self) -> str | None:
        signal = self._signal
        if not signal:
            return None
        unit = signal.get("unit")
        if unit == "cm":
            return UnitOfLength.CENTIMETERS
        return unit

    @property
    def device_class(self) -> SensorDeviceClass | None:
        signal = self._signal
        if not signal:
            return None
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        signal = self._signal or {}
        return {
            "station": self.station_data["name"],
            "station_key": self.station_key,
            "signal": self.signal_key,
            "timestamp": signal.get("timestamp"),
            "absolute_value": signal.get("absolute_value"),
            "source_url": signal.get("url"),
            "parser": signal.get("parser"),
            "page_url": self.station_data.get("page_url"),
        }

    @property
    def available(self) -> bool:
        signal = self._signal
        return bool(signal) and "error" not in signal and signal.get("value") is not None
