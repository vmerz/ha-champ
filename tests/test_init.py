"""Test CHAMP integration setup."""

from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component

from custom_components.champ.const import DOMAIN


async def test_setup(hass: HomeAssistant):
    """Test component setup."""
    assert await async_setup_component(hass, DOMAIN, {})


async def test_setup_entry(hass: HomeAssistant, setup_integration):
    """Test setting up config entry."""
    assert DOMAIN in hass.config_entries.async_domains()

    # Check that coordinator was created
    assert setup_integration.entry_id in hass.data[DOMAIN]


async def test_unload_entry(hass: HomeAssistant, setup_integration):
    """Test unloading config entry."""
    entry = setup_integration

    # Unload the entry
    assert await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()

    # Check that it was removed
    assert entry.entry_id not in hass.data[DOMAIN]
