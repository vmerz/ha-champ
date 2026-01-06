"""Config flow for CHAMP integration."""

from __future__ import annotations

import logging
import uuid
from datetime import date, datetime
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import selector

from .const import (
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
    DEFAULT_MEMBER_ICON,
    DEFAULT_POINTS_PER_LEVEL,
    DEFAULT_TASK_ICON,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


class ChampConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):  # type: ignore[call-arg]
    """Handle a config flow for CHAMP."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._members: list[dict[str, Any]] = []
        self._tasks: list[dict[str, Any]] = []
        self._level_config: dict[str, Any] = {
            CONF_POINTS_PER_LEVEL: DEFAULT_POINTS_PER_LEVEL
        }

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is not None:
            # Store any initial configuration if needed
            return await self.async_step_add_member()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({}),
            description_placeholders={"docs_url": "https://github.com/vmerz/ha-champ"},
        )

    async def async_step_add_member(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle adding a member."""
        errors: dict[str, str] = {}

        if user_input is not None:
            # Validate member name
            if not user_input.get(CONF_MEMBER_NAME):
                errors["base"] = "name_required"

            # Validate birthdate if provided
            if (
                CONF_MEMBER_BIRTHDATE in user_input
                and user_input[CONF_MEMBER_BIRTHDATE]
            ):
                birthdate_str = user_input[CONF_MEMBER_BIRTHDATE]
                try:
                    birthdate = datetime.fromisoformat(birthdate_str).date()
                    today = date.today()
                    min_date = date(today.year - 120, today.month, today.day)

                    if birthdate > today:
                        errors[CONF_MEMBER_BIRTHDATE] = "future_date"
                    elif birthdate < min_date:
                        errors[CONF_MEMBER_BIRTHDATE] = "too_old"

                except ValueError:
                    errors[CONF_MEMBER_BIRTHDATE] = "invalid_date"

            # Only create member if no errors
            if not errors:  # ← Fixed!
                member = {
                    CONF_MEMBER_ID: str(uuid.uuid4())[:8],
                    CONF_MEMBER_NAME: user_input[CONF_MEMBER_NAME],
                    CONF_MEMBER_BIRTHDATE: user_input.get(CONF_MEMBER_BIRTHDATE),
                    CONF_MEMBER_ICON: user_input.get(
                        CONF_MEMBER_ICON, DEFAULT_MEMBER_ICON
                    ),
                }
                self._members.append(member)

                _LOGGER.debug("Added member: %s", member[CONF_MEMBER_NAME])

                return await self.async_step_add_another_member()

        return self.async_show_form(
            step_id="add_member",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_MEMBER_NAME): str,
                    vol.Optional(CONF_MEMBER_BIRTHDATE): selector.DateSelector(
                        selector.DateSelectorConfig()
                    ),
                    vol.Optional(
                        CONF_MEMBER_ICON, default=DEFAULT_MEMBER_ICON
                    ): selector.IconSelector(
                        selector.IconSelectorConfig(placeholder="mdi:account")
                    ),
                }
            ),
            errors=errors,
        )

    async def async_step_add_another_member(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Ask if user wants to add another member."""
        if user_input is not None:
            if user_input.get("add_another"):
                return await self.async_step_add_member()
            return await self.async_step_add_task()

        return self.async_show_form(
            step_id="add_another_member",
            data_schema=vol.Schema(
                {
                    vol.Required("add_another", default=False): bool,
                }
            ),
            description_placeholders={
                "members_count": str(len(self._members)),
                "members_names": ", ".join(c[CONF_MEMBER_NAME] for c in self._members),
            },
        )

    async def async_step_add_task(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle adding a task."""
        errors: dict[str, str] = {}

        if user_input is not None:
            # Validate task
            if not user_input.get(CONF_TASK_NAME):
                errors["base"] = "name_required"
            elif user_input.get(CONF_TASK_POINTS, 0) <= 0:
                errors["base"] = "invalid_points"
            else:
                # Create task entry
                task = {
                    CONF_TASK_ID: user_input[CONF_TASK_NAME].lower().replace(" ", "_"),
                    CONF_TASK_NAME: user_input[CONF_TASK_NAME],
                    CONF_TASK_ICON: user_input.get(CONF_TASK_ICON, DEFAULT_TASK_ICON),
                    CONF_TASK_POINTS: user_input[CONF_TASK_POINTS],
                    CONF_TASK_CATEGORY: user_input.get(CONF_TASK_CATEGORY, "other"),
                    CONF_TASK_ASSIGNED_TO: ["all"],  # Default to all members
                }
                self._tasks.append(task)

                _LOGGER.debug(
                    "Added task: %s (%d points)",
                    task[CONF_TASK_NAME],
                    task[CONF_TASK_POINTS],
                )

                return await self.async_step_add_another_task()

        return self.async_show_form(
            step_id="add_task",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_TASK_NAME): str,
                    vol.Required(CONF_TASK_POINTS, default=5): vol.All(
                        vol.Coerce(int), vol.Range(min=1, max=100)
                    ),
                    vol.Optional(
                        CONF_TASK_ICON, default=DEFAULT_TASK_ICON
                    ): selector.IconSelector(
                        selector.IconSelectorConfig()  # ← Changed!
                    ),
                    vol.Optional(
                        CONF_TASK_CATEGORY, default="other"
                    ): selector.SelectSelector(
                        selector.SelectSelectorConfig(
                            options=[
                                selector.SelectOptionDict(
                                    value="chores", label="chores"
                                ),
                                selector.SelectOptionDict(
                                    value="learning", label="learning"
                                ),
                                selector.SelectOptionDict(
                                    value="health", label="health"
                                ),
                                selector.SelectOptionDict(value="other", label="other"),
                            ],
                            mode=selector.SelectSelectorMode.DROPDOWN,
                            translation_key="task_category",  # ← Key for translations
                        )
                    ),
                }
            ),
            errors=errors,
        )

    async def async_step_add_another_task(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Ask if user wants to add another task."""
        if user_input is not None:
            if user_input.get("add_another"):
                return await self.async_step_add_task()
            return await self.async_step_level_config()

        return self.async_show_form(
            step_id="add_another_task",
            data_schema=vol.Schema(
                {
                    vol.Required("add_another", default=False): bool,
                }
            ),
            description_placeholders={
                "tasks_count": str(len(self._tasks)),
            },
        )

    async def async_step_level_config(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Configure level progression."""
        if user_input is not None:
            self._level_config = {
                CONF_POINTS_PER_LEVEL: user_input.get(
                    CONF_POINTS_PER_LEVEL, DEFAULT_POINTS_PER_LEVEL
                )
            }
            return await self.async_step_finish()

        return self.async_show_form(
            step_id="level_config",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_POINTS_PER_LEVEL, default=DEFAULT_POINTS_PER_LEVEL
                    ): vol.All(vol.Coerce(int), vol.Range(min=10, max=500)),
                }
            ),
        )

    async def async_step_finish(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Finish configuration."""
        # Create the config entry
        return self.async_create_entry(
            title=f"CHAMP ({len(self._members)} members)",
            data={
                CONF_MEMBERS: self._members,
                CONF_TASKS: self._tasks,
                CONF_LEVEL_CONFIG: self._level_config,
            },
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> ChampOptionsFlow:
        """Get the options flow for this handler."""
        return ChampOptionsFlow(config_entry)


class ChampOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for CHAMP."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            # Update the config entry with new data
            return self.async_create_entry(title="", data=user_input)

        # For now, show current configuration
        # Full options flow will be implemented in Phase 2
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({}),
        )
