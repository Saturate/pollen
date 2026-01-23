"""Config flow for Pollen API integration."""
from __future__ import annotations

from typing import Any
import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import (
    CONF_API_URL,
    CONF_COUNTRY,
    CONF_REGION,
    CONF_LANGUAGE,
    DEFAULT_API_URL,
    DEFAULT_COUNTRY,
    DEFAULT_REGION,
    DEFAULT_LANGUAGE,
    DOMAIN,
)


async def validate_api(hass: HomeAssistant, api_url: str, country: str) -> dict[str, list[str]]:
    """Validate the API URL and fetch available regions."""
    session = async_get_clientsession(hass)

    async with session.get(f"{api_url}/v1/{country}/regions") as response:
        if response.status != 200:
            raise ValueError("Cannot connect to API")
        data = await response.json()
        return {
            "regions": [r["slug"] for r in data["regions"]]
        }


class PollenApiConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Pollen API."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            try:
                await validate_api(
                    self.hass,
                    user_input[CONF_API_URL],
                    user_input.get(CONF_COUNTRY, DEFAULT_COUNTRY),
                )
                return self.async_create_entry(
                    title=f"Pollen API ({user_input.get(CONF_REGION, DEFAULT_REGION)})",
                    data=user_input,
                )
            except Exception:
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_API_URL, default=DEFAULT_API_URL): str,
                    vol.Required(CONF_COUNTRY, default=DEFAULT_COUNTRY): str,
                    vol.Required(CONF_REGION, default=DEFAULT_REGION): str,
                    vol.Optional(CONF_LANGUAGE, default=DEFAULT_LANGUAGE): str,
                }
            ),
            errors=errors,
        )
