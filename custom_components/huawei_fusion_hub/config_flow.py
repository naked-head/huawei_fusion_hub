"""Config flow for Huawei Fusion Hub."""
from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry, ConfigFlow, OptionsFlow
from homeassistant.core import callback
from homeassistant.helpers.selector import (
    BooleanSelector,
    SelectOptionDict,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from .const import (
    ALL_SOURCES,
    CONF_NOTIFY_ON_DISCONNECT,
    CONF_PRIORITY,
    CONF_SOURCES,
    DEFAULT_NOTIFY_ON_DISCONNECT,
    DOMAIN,
    SOURCE_NAMES,
)


def _installed_sources(hass) -> list[str]:
    """Sources that have at least one loaded config entry."""
    return [
        source
        for source in ALL_SOURCES
        if hass.config_entries.async_entries(source)
    ]


def _source_options(sources: list[str]) -> list[SelectOptionDict]:
    return [
        SelectOptionDict(value=s, label=SOURCE_NAMES[s]) for s in sources
    ]


class HuaweiFusionHubConfigFlow(ConfigFlow, domain=DOMAIN):
    """Two steps: pick sources, then order them by priority."""

    VERSION = 1

    def __init__(self) -> None:
        self._sources: list[str] = []

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> Any:
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()

        if user_input is not None:
            self._sources = user_input[CONF_SOURCES]
            if not self._sources:
                return self.async_show_form(
                    step_id="user",
                    data_schema=self._user_schema(),
                    errors={"base": "no_sources"},
                )
            if len(self._sources) == 1:
                return self._create(self._sources)
            return await self.async_step_priority()

        return self.async_show_form(step_id="user", data_schema=self._user_schema())

    def _user_schema(self) -> vol.Schema:
        detected = _installed_sources(self.hass)
        return vol.Schema(
            {
                vol.Required(CONF_SOURCES, default=detected): SelectSelector(
                    SelectSelectorConfig(
                        options=_source_options(ALL_SOURCES),
                        multiple=True,
                        mode=SelectSelectorMode.LIST,
                    )
                )
            }
        )

    async def async_step_priority(
        self, user_input: dict[str, Any] | None = None
    ) -> Any:
        if user_input is not None:
            priority = [user_input[f"priority_{i}"] for i in range(len(self._sources))]
            if len(set(priority)) != len(priority):
                return self.async_show_form(
                    step_id="priority",
                    data_schema=self._priority_schema(),
                    errors={"base": "duplicate_priority"},
                )
            return self._create(priority)

        return self.async_show_form(
            step_id="priority", data_schema=self._priority_schema()
        )

    def _priority_schema(self) -> vol.Schema:
        options = _source_options(self._sources)
        schema: dict[Any, Any] = {}
        for i, source in enumerate(self._sources):
            schema[vol.Required(f"priority_{i}", default=source)] = SelectSelector(
                SelectSelectorConfig(
                    options=options, mode=SelectSelectorMode.DROPDOWN
                )
            )
        return vol.Schema(schema)

    def _create(self, priority: list[str]) -> Any:
        return self.async_create_entry(
            title="Huawei Fusion Hub",
            data={
                CONF_SOURCES: self._sources,
                CONF_PRIORITY: priority,
                CONF_NOTIFY_ON_DISCONNECT: DEFAULT_NOTIFY_ON_DISCONNECT,
            },
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlow:
        return HubOptionsFlow(config_entry)


class HubOptionsFlow(OptionsFlow):
    """Re-order priority and toggle notifications at any time."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        self._entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> Any:
        sources: list[str] = self._entry.data[CONF_SOURCES]
        current_priority: list[str] = self._entry.options.get(
            CONF_PRIORITY, self._entry.data[CONF_PRIORITY]
        )
        current_notify: bool = self._entry.options.get(
            CONF_NOTIFY_ON_DISCONNECT,
            self._entry.data.get(CONF_NOTIFY_ON_DISCONNECT, True),
        )

        if user_input is not None:
            priority = [user_input[f"priority_{i}"] for i in range(len(sources))]
            if len(set(priority)) != len(priority):
                return self.async_show_form(
                    step_id="init",
                    data_schema=self._schema(sources, current_priority, current_notify),
                    errors={"base": "duplicate_priority"},
                )
            return self.async_create_entry(
                title="",
                data={
                    CONF_PRIORITY: priority,
                    CONF_NOTIFY_ON_DISCONNECT: user_input[CONF_NOTIFY_ON_DISCONNECT],
                },
            )

        return self.async_show_form(
            step_id="init",
            data_schema=self._schema(sources, current_priority, current_notify),
        )

    def _schema(
        self, sources: list[str], priority: list[str], notify: bool
    ) -> vol.Schema:
        options = _source_options(sources)
        schema: dict[Any, Any] = {}
        for i in range(len(sources)):
            default = priority[i] if i < len(priority) else sources[i]
            schema[vol.Required(f"priority_{i}", default=default)] = SelectSelector(
                SelectSelectorConfig(
                    options=options, mode=SelectSelectorMode.DROPDOWN
                )
            )
        schema[
            vol.Required(CONF_NOTIFY_ON_DISCONNECT, default=notify)
        ] = BooleanSelector()
        return vol.Schema(schema)
