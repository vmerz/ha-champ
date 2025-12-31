"""Fixtures for CHAMP integration tests."""

import sys

import pytest
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.champ.const import (CONF_CHILDREN, CONF_LEVEL_CONFIG,
                                           CONF_POINTS_PER_LEVEL, CONF_TASKS,
                                           DOMAIN)


# This fixture enables loading custom integrations in all tests
@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    """Enable custom integrations in all tests."""
    yield


@pytest.fixture
def mock_config_entry():
    """Create a mock config entry."""
    return MockConfigEntry(
        domain=DOMAIN,
        title="CHAMP Test",
        data={
            CONF_CHILDREN: [
                {
                    "id": "test_child_1",
                    "name": "Test Child",
                    "age": 10,
                    "icon": "mdi:account-child",
                }
            ],
            CONF_TASKS: [
                {
                    "id": "test_task",
                    "name": "Test Task",
                    "points": 5,
                    "icon": "mdi:checkbox-marked-circle",
                    "category": "chores",
                    "assigned_to": ["all"],
                }
            ],
            CONF_LEVEL_CONFIG: {CONF_POINTS_PER_LEVEL: 50},
        },
    )


@pytest.fixture
async def setup_integration(hass: HomeAssistant, mock_config_entry):
    """Set up the CHAMP integration for testing."""
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()
    return mock_config_entry
