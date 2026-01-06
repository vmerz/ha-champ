"""Sensor platform for CHAMP integration."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_MEMBER_NAME, DOMAIN
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

    # Create sensors for each member
    for member_id, member_data in coordinator.data["members"].items():
        member_config = member_data["config"]

        # Points sensor
        entities.append(ChampPointsSensor(coordinator, member_id, member_config))

        # Level sensor
        entities.append(ChampLevelSensor(coordinator, member_id, member_config))

        # Points to next level sensor
        entities.append(
            ChampPointsToNextLevelSensor(coordinator, member_id, member_config)
        )

    async_add_entities(entities)

    _LOGGER.debug(
        "Added %d sensor entities for %d members",
        len(entities),
        len(coordinator.data["members"]),
    )


class ChampBaseSensor(CoordinatorEntity[ChampDataCoordinator], SensorEntity):
    """Base class for CHAMP sensors."""

    def __init__(
        self,
        coordinator: ChampDataCoordinator,
        member_id: str,
        member_config: dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._member_id = member_id
        self._member_config = member_config
        self._attr_device_info = {
            "identifiers": {(DOMAIN, member_id)},
            "name": member_config[CONF_MEMBER_NAME],
            "manufacturer": "CHAMP",
            "model": "Member Profile",
        }


class ChampPointsSensor(ChampBaseSensor):
    """Sensor for member's current points."""

    _attr_state_class = SensorStateClass.TOTAL
    _attr_native_unit_of_measurement = "points"
    _attr_icon = "mdi:star"

    def __init__(
        self,
        coordinator: ChampDataCoordinator,
        member_id: str,
        member_config: dict[str, Any],
    ) -> None:
        """Initialize the points sensor."""
        super().__init__(coordinator, member_id, member_config)

        self._attr_name = f"{member_config[CONF_MEMBER_NAME]} Points"
        self._attr_unique_id = f"{DOMAIN}_{member_id}_points"
        self.entity_id = f"sensor.{DOMAIN}_{member_id}_points"

    @property
    def native_value(self) -> int:
        """Return the current points."""
        return self.coordinator.get_member_points(self._member_id)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        attributes = {
            "member_id": self._member_id,
            "member_name": self._member_config[CONF_MEMBER_NAME],
        }

        # NEW: Add birthdate and age if available
        birthdate = self._member_config.get(
            "birthdate"
        )  # Get birthdate (might be None)
        if birthdate:
            attributes["birthdate"] = birthdate

            # Calculate age from birthdate
            age = self._calculate_age(birthdate)
            if age is not None:
                attributes["age"] = age

        return attributes

    def _calculate_age(self, birthdate_str: str) -> int | None:
        """Calculate age from birthdate string."""
        from datetime import date, datetime

        try:
            # Convert string "1985-03-15" to date object
            birthdate = datetime.fromisoformat(birthdate_str).date()
            today = date.today()

            # Calculate age
            age = today.year - birthdate.year

            # Adjust if birthday hasn't happened yet this year
            if (today.month, today.day) < (birthdate.month, birthdate.day):
                age -= 1

            return age
        except (ValueError, AttributeError):
            return None


class ChampLevelSensor(ChampBaseSensor):
    """Sensor for member's current level."""

    _attr_state_class = SensorStateClass.TOTAL
    _attr_native_unit_of_measurement = "level"
    _attr_icon = "mdi:trophy"

    def __init__(
        self,
        coordinator: ChampDataCoordinator,
        member_id: str,
        member_config: dict[str, Any],
    ) -> None:
        """Initialize the level sensor."""
        super().__init__(coordinator, member_id, member_config)

        self._attr_name = f"{member_config[CONF_MEMBER_NAME]} Level"
        self._attr_unique_id = f"{DOMAIN}_{member_id}_level"
        self.entity_id = f"sensor.{DOMAIN}_{member_id}_level"

    @property
    def native_value(self) -> int:
        """Return the current level."""
        return self.coordinator.get_member_level(self._member_id)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        attributes = {
            "member_id": self._member_id,
            "member_name": self._member_config[CONF_MEMBER_NAME],
            "points": self.coordinator.get_member_points(self._member_id),
            "points_per_level": self.coordinator._get_points_per_level(),
        }

        # Add birthdate/age
        birthdate = self._member_config.get("birthdate")
        if birthdate:
            attributes["birthdate"] = birthdate
            age = self._calculate_age(birthdate)
            if age is not None:
                attributes["age"] = age

        return attributes


class ChampPointsToNextLevelSensor(ChampBaseSensor):
    """Sensor for points needed to reach next level."""

    _attr_native_unit_of_measurement = "points"
    _attr_icon = "mdi:star-outline"

    def __init__(
        self,
        coordinator: ChampDataCoordinator,
        member_id: str,
        member_config: dict[str, Any],
    ) -> None:
        """Initialize the points to next level sensor."""
        super().__init__(coordinator, member_id, member_config)

        self._attr_name = f"{member_config[CONF_MEMBER_NAME]} Points to Next Level"
        self._attr_unique_id = f"{DOMAIN}_{member_id}_points_to_next_level"
        self.entity_id = f"sensor.{DOMAIN}_{member_id}_points_to_next_level"

    @property
    def native_value(self) -> int:
        """Return points needed for next level."""
        return self.coordinator.get_points_to_next_level(self._member_id)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        current_level = self.coordinator.get_member_level(self._member_id)
        return {
            "member_id": self._member_id,
            "member_name": self._member_config[CONF_MEMBER_NAME],
            "current_level": current_level,
            "next_level": current_level + 1,
            "current_points": self.coordinator.get_member_points(self._member_id),
        }
