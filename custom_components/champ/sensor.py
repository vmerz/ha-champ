"""Sensor platform for CHAMP integration."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_CHILD_NAME, DOMAIN
from .coordinator import ChampDataCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up CHAMP sensor platform."""
    coordinator: ChampDataCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    entities: list[SensorEntity] = []

    # Create sensors for each child
    for child_id, child_data in coordinator.data["children"].items():
        child_config = child_data["config"]

        # Points sensor
        entities.append(ChampPointsSensor(coordinator, child_id, child_config))

        # Level sensor
        entities.append(ChampLevelSensor(coordinator, child_id, child_config))

        # Points to next level sensor
        entities.append(
            ChampPointsToNextLevelSensor(coordinator, child_id, child_config)
        )

    async_add_entities(entities)

    _LOGGER.debug(
        "Added %d sensor entities for %d children",
        len(entities),
        len(coordinator.data["children"]),
    )


class ChampBaseSensor(CoordinatorEntity[ChampDataCoordinator], SensorEntity):
    """Base class for CHAMP sensors."""

    def __init__(
        self,
        coordinator: ChampDataCoordinator,
        child_id: str,
        child_config: dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._child_id = child_id
        self._child_config = child_config
        self._attr_device_info = {
            "identifiers": {(DOMAIN, child_id)},
            "name": child_config[CONF_CHILD_NAME],
            "manufacturer": "CHAMP",
            "model": "Child Profile",
        }


class ChampPointsSensor(ChampBaseSensor):
    """Sensor for child's current points."""

    _attr_state_class = SensorStateClass.TOTAL
    _attr_native_unit_of_measurement = "points"
    _attr_icon = "mdi:star"

    def __init__(
        self,
        coordinator: ChampDataCoordinator,
        child_id: str,
        child_config: dict[str, Any],
    ) -> None:
        """Initialize the points sensor."""
        super().__init__(coordinator, child_id, child_config)

        self._attr_name = f"{child_config[CONF_CHILD_NAME]} Points"
        self._attr_unique_id = f"{DOMAIN}_{child_id}_points"
        self.entity_id = f"sensor.{DOMAIN}_{child_id}_points"

    @property
    def native_value(self) -> int:
        """Return the current points."""
        return self.coordinator.get_child_points(self._child_id)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        return {
            "child_id": self._child_id,
            "child_name": self._child_config[CONF_CHILD_NAME],
        }


class ChampLevelSensor(ChampBaseSensor):
    """Sensor for child's current level."""

    _attr_state_class = SensorStateClass.TOTAL
    _attr_native_unit_of_measurement = "level"
    _attr_icon = "mdi:trophy"

    def __init__(
        self,
        coordinator: ChampDataCoordinator,
        child_id: str,
        child_config: dict[str, Any],
    ) -> None:
        """Initialize the level sensor."""
        super().__init__(coordinator, child_id, child_config)

        self._attr_name = f"{child_config[CONF_CHILD_NAME]} Level"
        self._attr_unique_id = f"{DOMAIN}_{child_id}_level"
        self.entity_id = f"sensor.{DOMAIN}_{child_id}_level"

    @property
    def native_value(self) -> int:
        """Return the current level."""
        return self.coordinator.get_child_level(self._child_id)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        return {
            "child_id": self._child_id,
            "child_name": self._child_config[CONF_CHILD_NAME],
            "points": self.coordinator.get_child_points(self._child_id),
            "points_per_level": self.coordinator._get_points_per_level(),
        }


class ChampPointsToNextLevelSensor(ChampBaseSensor):
    """Sensor for points needed to reach next level."""

    _attr_native_unit_of_measurement = "points"
    _attr_icon = "mdi:star-outline"

    def __init__(
        self,
        coordinator: ChampDataCoordinator,
        child_id: str,
        child_config: dict[str, Any],
    ) -> None:
        """Initialize the points to next level sensor."""
        super().__init__(coordinator, child_id, child_config)

        self._attr_name = f"{child_config[CONF_CHILD_NAME]} Points to Next Level"
        self._attr_unique_id = f"{DOMAIN}_{child_id}_points_to_next_level"
        self.entity_id = f"sensor.{DOMAIN}_{child_id}_points_to_next_level"

    @property
    def native_value(self) -> int:
        """Return points needed for next level."""
        return self.coordinator.get_points_to_next_level(self._child_id)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        current_level = self.coordinator.get_child_level(self._child_id)
        return {
            "child_id": self._child_id,
            "child_name": self._child_config[CONF_CHILD_NAME],
            "current_level": current_level,
            "next_level": current_level + 1,
            "current_points": self.coordinator.get_child_points(self._child_id),
        }
