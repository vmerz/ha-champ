"""Fixtures for CHAMP integration tests."""

import sys
from pathlib import Path

import pytest
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.champ.const import (
    CONF_LEVEL_CONFIG,
    CONF_MEMBER_BIRTHDATE,
    CONF_MEMBER_ICON,
    CONF_MEMBER_ID,
    CONF_MEMBER_NAME,
    CONF_MEMBERS,
    CONF_POINTS_PER_LEVEL,
    CONF_TASK_ASSIGNED_TO,
    CONF_TASK_CATEGORY,
    CONF_TASK_ICON,
    CONF_TASK_ID,
    CONF_TASK_NAME,
    CONF_TASK_POINTS,
    CONF_TASKS,
    DOMAIN,
)

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


# This fixture is provided by pytest-homeassistant-custom-component
# and enables loading custom integrations
@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    """Enable custom integrations for all tests."""
    yield


@pytest.fixture
def mock_config_entry():
    """Create a mock config entry."""
    return MockConfigEntry(
        domain=DOMAIN,
        title="CHAMP Test",
        data={
            CONF_MEMBERS: [
                {
                    CONF_MEMBER_ID: "test_member_1",
                    CONF_MEMBER_NAME: "Test Member",
                    CONF_MEMBER_BIRTHDATE: "2015-01-15",
                    CONF_MEMBER_ICON: "mdi:account-child",
                }
            ],
            CONF_TASKS: [
                {
                    CONF_TASK_ID: "test_task",
                    CONF_TASK_NAME: "Test Task",
                    CONF_TASK_POINTS: 5,
                    CONF_TASK_ICON: "mdi:checkbox-marked-circle",
                    CONF_TASK_CATEGORY: "chores",
                    CONF_TASK_ASSIGNED_TO: ["all"],
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
