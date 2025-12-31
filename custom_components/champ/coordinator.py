"""Data coordinator for CHAMP integration."""

from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import (CONF_CHILD_ID, CONF_CHILDREN, CONF_LEVEL_CONFIG,
                    CONF_POINTS_PER_LEVEL, CONF_TASKS,
                    DEFAULT_POINTS_PER_LEVEL, DOMAIN, UPDATE_INTERVAL)

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

        # Initialize child data from config entry
        self._init_child_data()

    def _init_child_data(self) -> None:
        """Initialize child data structure."""
        children_data = {}

        for child in self.config_entry.data.get(CONF_CHILDREN, []):
            child_id = child[CONF_CHILD_ID]
            children_data[child_id] = {
                "points": 0,  # Will be loaded from state if available
                "level": 0,
                "points_to_next_level": self._get_points_per_level(),
                "config": child,
            }

        self.data = {
            "children": children_data,
            "tasks": self.config_entry.data.get(CONF_TASKS, []),
            "level_config": self.config_entry.data.get(
                CONF_LEVEL_CONFIG, {CONF_POINTS_PER_LEVEL: DEFAULT_POINTS_PER_LEVEL}
            ),
        }

    def _get_points_per_level(self) -> int:
        """Get points required per level."""
        level_config = self.config_entry.data.get(CONF_LEVEL_CONFIG, {})
        return level_config.get(CONF_POINTS_PER_LEVEL, DEFAULT_POINTS_PER_LEVEL)

    def get_child_points(self, child_id: str) -> int:
        """Get current points for a child."""
        return self.data["children"].get(child_id, {}).get("points", 0)

    def get_child_level(self, child_id: str) -> int:
        """Calculate current level for a child."""
        points = self.get_child_points(child_id)
        points_per_level = self._get_points_per_level()
        return points // points_per_level

    def get_points_to_next_level(self, child_id: str) -> int:
        """Calculate points needed for next level."""
        points = self.get_child_points(child_id)
        points_per_level = self._get_points_per_level()
        return points_per_level - (points % points_per_level)

    async def award_points(self, child_id: str, points: int) -> None:
        """Award points to a child."""
        if child_id not in self.data["children"]:
            _LOGGER.error("Child ID %s not found", child_id)
            return

        current_points = self.data["children"][child_id]["points"]
        new_points = current_points + points

        self.data["children"][child_id]["points"] = new_points
        self.data["children"][child_id]["level"] = self.get_child_level(child_id)
        self.data["children"][child_id]["points_to_next_level"] = (
            self.get_points_to_next_level(child_id)
        )

        _LOGGER.debug(
            "Awarded %d points to %s. New total: %d",
            points,
            child_id,
            new_points,
        )

        # Notify all listeners
        await self.async_refresh()

    async def reset_points(self, child_id: str) -> None:
        """Reset points for a child."""
        if child_id not in self.data["children"]:
            _LOGGER.error("Child ID %s not found", child_id)
            return

        self.data["children"][child_id]["points"] = 0
        self.data["children"][child_id]["level"] = 0
        self.data["children"][child_id][
            "points_to_next_level"
        ] = self._get_points_per_level()

        _LOGGER.info("Reset points for child %s", child_id)

        # Notify all listeners
        await self.async_refresh()

    async def _async_update_data(self) -> dict[str, Any]:
        """Update data via library."""
        # For now, we just return the current data
        # In future phases, this could sync with external storage
        return self.data
