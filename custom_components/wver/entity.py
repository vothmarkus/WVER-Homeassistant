"""Base entities for WVER."""
from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MANUFACTURER


class WverCoordinatorEntity(CoordinatorEntity):
    """Base class for WVER coordinator entities."""

    def __init__(self, coordinator, station_key: str, station_data: dict) -> None:
        super().__init__(coordinator)
        self.station_key = station_key
        self.station_data = station_data

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self.station_key)},
            manufacturer=MANUFACTURER,
            model="Messstation",
            name=self.station_data["name"],
            configuration_url=self.station_data.get("page_url"),
        )
