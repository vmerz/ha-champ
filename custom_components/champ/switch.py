"""Switch platform for CHAMP integration."""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    CONF_CHILD_NAME,
    CONF_TASK_ASSIGNED_TO,
    CONF_TASK_ICON,
    CONF_TASK_ID,
    CONF_TASK_NAME,
    CONF_TASK_POINTS,
    DOMAIN,
)
from .coordinator import ChampDataCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up CHAMP switch platform."""
    coordinator: ChampDataCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    entities: list[SwitchEntity] = []

    # Create task switches for each child
    for child_id, child_data in coordinator.data["children"].items():
        child_config = child_data["config"]

        # Create switches for tasks assigned to this child
        for task in coordinator.data["tasks"]:
            # Check if task is assigned to this child or to all
            assigned_to = task.get(CONF_TASK_ASSIGNED_TO, ["all"])
            if "all" in assigned_to or child_id in assigned_to:
                entities.append(
                    ChampTaskSwitch(coordinator, child_id, child_config, task)
                )

    async_add_entities(entities)

    _LOGGER.debug(
        "Added %d task switches for %d children",
        len(entities),
        len(coordinator.data["children"]),
    )


class ChampTaskSwitch(CoordinatorEntity[ChampDataCoordinator], SwitchEntity):
    """Switch entity for a CHAMP task."""

    _attr_is_on = False

    def __init__(
        self,
        coordinator: ChampDataCoordinator,
        child_id: str,
        child_config: dict[str, Any],
        task_config: dict[str, Any],
    ) -> None:
        """Initialize the task switch."""
        super().__init__(coordinator)

        self._child_id = child_id
        self._child_config = child_config
        self._task_config = task_config

        task_id = task_config[CONF_TASK_ID]
        child_name = child_config[CONF_CHILD_NAME]
        task_name = task_config[CONF_TASK_NAME]

        self._attr_name = f"{child_name} - {task_name}"
        self._attr_unique_id = f"{DOMAIN}_{child_id}_{task_id}"
        self.entity_id = f"switch.{DOMAIN}_{child_id}_{task_id}"
        self._attr_icon = task_config.get(CONF_TASK_ICON, "mdi:checkbox-marked-circle")

        self._attr_device_info = {
            "identifiers": {(DOMAIN, child_id)},
            "name": child_name,
            "manufacturer": "CHAMP",
            "model": "Child Profile",
        }

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        return {
            "child_id": self._child_id,
            "child_name": self._child_config[CONF_CHILD_NAME],
            "task_id": self._task_config[CONF_TASK_ID],
            "task_name": self._task_config[CONF_TASK_NAME],
            "points": self._task_config[CONF_TASK_POINTS],
        }

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on the switch (complete the task)."""
        points = self._task_config[CONF_TASK_POINTS]
        child_name = self._child_config[CONF_CHILD_NAME]
        task_name = self._task_config[CONF_TASK_NAME]

        _LOGGER.debug(
            "Task completed: %s - %s (%d points)",
            child_name,
            task_name,
            points,
        )

        # Award points
        await self.coordinator.award_points(self._child_id, points)

        # Turn switch on temporarily
        self._attr_is_on = True
        self.async_write_ha_state()

        # Send notification
        await self._send_notification(child_name, task_name, points)

        # Auto turn off after 2 seconds (provides visual feedback)
        await asyncio.sleep(2)
        self._attr_is_on = False
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off the switch."""
        # Switches auto turn off, manual turn off does nothing
        self._attr_is_on = False
        self.async_write_ha_state()

    async def _send_notification(
        self, child_name: str, task_name: str, points: int
    ) -> None:
        """Send a notification about task completion."""
        total_points = self.coordinator.get_child_points(self._child_id)
        level = self.coordinator.get_child_level(self._child_id)

        message = (
            f"{child_name} hat {points} Punkte für {task_name} verdient! "
            f"Gesamt: {total_points} Punkte (Level {level})"
        )

        await self.hass.services.async_call(
            "persistent_notification",
            "create",
            {
                "title": "🎉 Punkte verdient!",
                "message": message,
            },
        )
