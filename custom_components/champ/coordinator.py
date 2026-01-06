"""Data coordinator for CHAMP integration."""

from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import (
    CONF_LEVEL_CONFIG,
    CONF_MEMBER_ID,
    CONF_MEMBERS,
    CONF_POINTS_PER_LEVEL,
    CONF_TASKS,
    DEFAULT_POINTS_PER_LEVEL,
    DOMAIN,
    UPDATE_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)


class ChampDataCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Class to manage fetching CHAMP data."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )
        self.config_entry = entry

        # Initialize member data from config entry
        self._init_member_data()

    def _init_member_data(self) -> None:
        """Initialize member data structure."""
        members_data = {}

        for member in self.config_entry.data.get(CONF_MEMBERS, []):
            member_id = member[CONF_MEMBER_ID]
            members_data[member_id] = {
                "points": 0,  # Will be loaded from state if available
                "level": 0,
                "points_to_next_level": self._get_points_per_level(),
                "config": member,
            }

        self.data = {
            "members": members_data,
            "tasks": self.config_entry.data.get(CONF_TASKS, []),
            "level_config": self.config_entry.data.get(
                CONF_LEVEL_CONFIG, {CONF_POINTS_PER_LEVEL: DEFAULT_POINTS_PER_LEVEL}
            ),
        }

    def _get_points_per_level(self) -> int:
        """Get points required per level."""
        level_config = self.config_entry.data.get(CONF_LEVEL_CONFIG, {})
        return level_config.get(CONF_POINTS_PER_LEVEL, DEFAULT_POINTS_PER_LEVEL)

    def get_member_points(self, member_id: str) -> int:
        """Get current points for a member."""
        return self.data["members"].get(member_id, {}).get("points", 0)

    def get_member_level(self, member_id: str) -> int:
        """Calculate current level for a member."""
        points = self.get_member_points(member_id)
        points_per_level = self._get_points_per_level()
        return points // points_per_level

    def get_points_to_next_level(self, member_id: str) -> int:
        """Calculate points needed for next level."""
        points = self.get_member_points(member_id)
        points_per_level = self._get_points_per_level()
        return points_per_level - (points % points_per_level)

    async def award_points(self, member_id: str, points: int) -> None:
        """Award points to a member."""
        if member_id not in self.data["members"]:
            _LOGGER.error("Member ID %s not found", member_id)
            return

        current_points = self.data["members"][member_id]["points"]
        new_points = current_points + points

        self.data["members"][member_id]["points"] = new_points
        self.data["members"][member_id]["level"] = self.get_member_level(member_id)
        self.data["members"][member_id]["points_to_next_level"] = (
            self.get_points_to_next_level(member_id)
        )

        _LOGGER.debug(
            "Awarded %d points to %s. New total: %d",
            points,
            member_id,
            new_points,
        )

        # Notify all listeners
        await self.async_refresh()

    async def reset_points(self, member_id: str) -> None:
        """Reset points for a member."""
        if member_id not in self.data["members"]:
            _LOGGER.error("Member ID %s not found", member_id)
            return

        self.data["members"][member_id]["points"] = 0
        self.data["members"][member_id]["level"] = 0
        self.data["members"][member_id][
            "points_to_next_level"
        ] = self._get_points_per_level()

        _LOGGER.info("Reset points for member %s", member_id)

        # Notify all listeners
        await self.async_refresh()

    async def _async_update_data(self) -> dict[str, Any]:
        """Update data via library."""
        # For now, we just return the current data
        # In future phases, this could sync with external storage
        return self.data
