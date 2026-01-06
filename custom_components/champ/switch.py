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
    CONF_MEMBER_NAME,
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

    # Create task switches for each member
    for member_id, member_data in coordinator.data["members"].items():
        member_config = member_data["config"]

        # Create switches for tasks assigned to this member
        for task in coordinator.data["tasks"]:
            # Check if task is assigned to this member or to all
            assigned_to = task.get(CONF_TASK_ASSIGNED_TO, ["all"])
            if "all" in assigned_to or member_id in assigned_to:
                entities.append(
                    ChampTaskSwitch(coordinator, member_id, member_config, task)
                )

    async_add_entities(entities)

    _LOGGER.debug(
        "Added %d task switches for %d members",
        len(entities),
        len(coordinator.data["members"]),
    )


class ChampTaskSwitch(CoordinatorEntity[ChampDataCoordinator], SwitchEntity):
    """Switch entity for a CHAMP task."""

    _attr_is_on = False

    def __init__(
        self,
        coordinator: ChampDataCoordinator,
        member_id: str,
        member_config: dict[str, Any],
        task_config: dict[str, Any],
    ) -> None:
        """Initialize the task switch."""
        super().__init__(coordinator)

        self._member_id = member_id
        self._member_config = member_config
        self._task_config = task_config

        task_id = task_config[CONF_TASK_ID]
        member_name = member_config[CONF_MEMBER_NAME]
        task_name = task_config[CONF_TASK_NAME]

        self._attr_name = f"{member_name} - {task_name}"
        self._attr_unique_id = f"{DOMAIN}_{member_id}_{task_id}"
        self.entity_id = f"switch.{DOMAIN}_{member_id}_{task_id}"
        self._attr_icon = task_config.get(CONF_TASK_ICON, "mdi:checkbox-marked-circle")

        self._attr_device_info = {
            "identifiers": {(DOMAIN, member_id)},
            "name": member_name,
            "manufacturer": "CHAMP",
            "model": "Member Profile",
        }

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        return {
            "member_id": self._member_id,
            "member_name": self._member_config[CONF_MEMBER_NAME],
            "task_id": self._task_config[CONF_TASK_ID],
            "task_name": self._task_config[CONF_TASK_NAME],
            "points": self._task_config[CONF_TASK_POINTS],
        }

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on the switch (complete the task)."""
        points = self._task_config[CONF_TASK_POINTS]
        member_name = self._member_config[CONF_MEMBER_NAME]
        task_name = self._task_config[CONF_TASK_NAME]

        _LOGGER.debug(
            "Task completed: %s - %s (%d points)",
            member_name,
            task_name,
            points,
        )

        # Award points
        await self.coordinator.award_points(self._member_id, points)

        # Turn switch on temporarily
        self._attr_is_on = True
        self.async_write_ha_state()

        # Send notification
        await self._send_notification(member_name, task_name, points)

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
        self, member_name: str, task_name: str, points: int
    ) -> None:
        """Send a notification about task completion."""
        total_points = self.coordinator.get_member_points(self._member_id)
        level = self.coordinator.get_member_level(self._member_id)

        message = (
            f"{member_name} hat {points} Punkte für {task_name} verdient! "
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
