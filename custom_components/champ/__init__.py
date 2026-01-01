"""The CHAMP integration."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv

from .const import (
    CONF_CHILDREN,
    CONF_LEVEL_CONFIG,
    CONF_TASKS,
    DEFAULT_POINTS_PER_LEVEL,
    DOMAIN,
)
from .coordinator import ChampDataCoordinator

_LOGGER = logging.getLogger(__name__)

# Platforms to set up
PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.SWITCH]

# Configuration schema (empty since we use config flow)
CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, config: dict[str, Any]) -> bool:
    """Set up the CHAMP component."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up CHAMP from a config entry."""
    _LOGGER.debug("Setting up CHAMP integration for entry: %s", entry.entry_id)

    # Validate config data
    if not entry.data.get(CONF_CHILDREN):
        _LOGGER.warning("No children configured in CHAMP")
        return False

    # Create coordinator
    coordinator = ChampDataCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    # Store coordinator
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Set up platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Register services
    await async_setup_services(hass)

    _LOGGER.info(
        "CHAMP setup complete with %d children and %d tasks",
        len(entry.data.get(CONF_CHILDREN, [])),
        len(entry.data.get(CONF_TASKS, [])),
    )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.debug("Unloading CHAMP integration for entry: %s", entry.entry_id)

    # Unload platforms
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    # Remove coordinator
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)


async def async_setup_services(hass: HomeAssistant) -> None:
    """Set up CHAMP services."""
    # Services will be implemented in Phase 3
    # Placeholder for now
    pass
