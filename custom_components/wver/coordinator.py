"""Coordinator for WVER."""
from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import WverApiClient
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class WverDataUpdateCoordinator(DataUpdateCoordinator[dict]):
    """Coordinator to fetch WVER data periodically."""

    def __init__(
        self,
        hass: HomeAssistant,
        client: WverApiClient,
        update_interval: timedelta,
    ) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=update_interval,
        )
        self.client = client

    async def _async_update_data(self) -> dict:
        try:
            return await self.client.async_fetch_all()
        except Exception as err:  # noqa: BLE001
            raise UpdateFailed(f"Error communicating with WVER: {err}") from err
