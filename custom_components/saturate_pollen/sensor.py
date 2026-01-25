"""Sensor platform for Pollen API integration."""
from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    CONF_API_URL,
    CONF_COUNTRY,
    CONF_REGION,
    CONF_LANGUAGE,
    DEFAULT_LANGUAGE,
    DEFAULT_SCAN_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=DEFAULT_SCAN_INTERVAL)

LEVEL_LABELS_EN = {
    0: "None",
    1: "Very Low",
    2: "Low",
    3: "Moderate",
    4: "High",
    5: "Very High",
}

LEVEL_LABELS_DA = {
    0: "Ingen",
    1: "Meget Lav",
    2: "Lav",
    3: "Moderat",
    4: "Høj",
    5: "Meget Høj",
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Pollen API sensor based on a config entry."""
    api_url = entry.data[CONF_API_URL]
    country = entry.data[CONF_COUNTRY]
    region = entry.data[CONF_REGION]
    language = entry.data.get(CONF_LANGUAGE, DEFAULT_LANGUAGE)

    session = async_get_clientsession(hass)

    async with session.get(f"{api_url}/v1/{country}/pollen-types") as response:
        if response.status == 200:
            data = await response.json()
            pollen_types = data.get("pollen_types", [])
        else:
            _LOGGER.error("Failed to fetch pollen types from API")
            return

    sensors = [
        PollenSensor(hass, api_url, country, region, language, pollen["id"], pollen["name"])
        for pollen in pollen_types
    ]

    async_add_entities(sensors, True)


class PollenSensor(SensorEntity):
    """Representation of a Pollen sensor."""

    def __init__(
        self,
        hass: HomeAssistant,
        api_url: str,
        country: str,
        region: str,
        language: str,
        pollen_id: str,
        pollen_name: str,
    ) -> None:
        """Initialize the sensor."""
        self.hass = hass
        self._api_url = api_url
        self._country = country
        self._region = region
        self._language = language
        self._pollen_id = pollen_id
        self._pollen_name = pollen_name
        self._state = None
        self._attributes = {}

        self._attr_name = f"Pollen {pollen_name}"
        self._attr_unique_id = f"{country}_{region}_{pollen_id}"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self._attributes

    async def async_update(self) -> None:
        """Fetch new state data for the sensor."""
        session = async_get_clientsession(self.hass)
        url = f"{self._api_url}/v1/{self._country}/{self._region}/forecast?lang={self._language}"

        try:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()

                    for item in data:
                        if item["pollen_type"] == self._pollen_id:
                            if not item.get("is_forecast", False):
                                level = item["level"]
                                labels = LEVEL_LABELS_DA if self._language == "da" else LEVEL_LABELS_EN
                                self._state = level
                                self._attributes = {
                                    "date": item["date"],
                                    "pollen_type": item["pollen_type"],
                                    "pollen_name": item["pollen_name"],
                                    "level": level,
                                    "level_text": labels.get(level, str(level)),
                                }

                                forecasts = [
                                    f for f in data
                                    if f["pollen_type"] == self._pollen_id and f.get("is_forecast", False)
                                ]
                                if forecasts:
                                    self._attributes["forecast"] = forecasts

                                break
                else:
                    _LOGGER.error(
                        "Failed to fetch forecast data: %s", response.status
                    )
        except Exception as err:
            _LOGGER.error("Error updating pollen sensor: %s", err)
