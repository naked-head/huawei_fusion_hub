"""Coordinator: discovers source entities, resolves values by priority."""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from homeassistant.core import Event, HomeAssistant, callback
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.util.unit_conversion import (
    EnergyConverter,
    PowerConverter,
    TemperatureConverter,
)

from .const import (
    CONF_NOTIFY_ON_DISCONNECT,
    CONF_OVERRIDES,
    CONF_PRIORITY,
    DOMAIN,
    SOURCE_NAMES,
    SOURCE_OFFLINE_THRESHOLD,
)
from .mapping import SENSOR_DEFS, SENSOR_DEFS_BY_KEY, HubSensorDef

_LOGGER = logging.getLogger(__name__)

BAD_STATES = ("unavailable", "unknown", None, "")


@dataclass
class ResolvedValue:
    value: Any
    source: str | None
    source_entity: str | None


class HubCoordinator(DataUpdateCoordinator[dict[str, ResolvedValue]]):
    """Event-driven coordinator over already-existing HA entities."""

    def __init__(self, hass: HomeAssistant, entry) -> None:
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=None)
        self.entry = entry
        self.priority: list[str] = entry.options.get(
            CONF_PRIORITY, entry.data.get(CONF_PRIORITY, [])
        )
        self.notify_on_disconnect: bool = entry.options.get(
            CONF_NOTIFY_ON_DISCONNECT,
            entry.data.get(CONF_NOTIFY_ON_DISCONNECT, True),
        )
        # canonical_key -> {source: entity_id}
        self.candidates: dict[str, dict[str, str]] = {}
        # source -> set of its mapped entity_ids
        self.source_entities: dict[str, set[str]] = {}
        # source -> bool (last known availability)
        self.source_available: dict[str, bool] = {}
        self._unsub = None

    # ------------------------------------------------------------
    # Discovery
    # ------------------------------------------------------------
    def discover(self) -> None:
        """Scan entity registry and resolve candidate entities per canonical key."""
        registry = er.async_get(self.hass)
        overrides: dict[str, dict[str, str]] = self.entry.options.get(
            CONF_OVERRIDES, {}
        )

        # index registry entries by platform (source domain)
        by_source: dict[str, list[er.RegistryEntry]] = {s: [] for s in self.priority}
        for entity in registry.entities.values():
            if entity.platform in by_source and entity.domain == "sensor":
                by_source[entity.platform].append(entity)

        self.candidates = {}
        self.source_entities = {s: set() for s in self.priority}

        for sensor_def in SENSOR_DEFS:
            per_source: dict[str, str] = {}
            for source in self.priority:
                # explicit user override wins
                override = overrides.get(sensor_def.key, {}).get(source)
                if override:
                    per_source[source] = override
                    self.source_entities[source].add(override)
                    continue
                entity_id = self._match(sensor_def, source, by_source.get(source, []))
                if entity_id:
                    per_source[source] = entity_id
                    self.source_entities[source].add(entity_id)
            if per_source:
                self.candidates[sensor_def.key] = per_source

        _LOGGER.debug("Discovery result: %s", self.candidates)

    @staticmethod
    def _match(
        sensor_def: HubSensorDef, source: str, entities: list[er.RegistryEntry]
    ) -> str | None:
        """Exact object_id match first, then suffix match ('*_<pattern>').

        Suffix matching handles per-install prefixes such as
        'homeassistant_<kioskid>_realtime_power' (FusionSolar kiosk) or
        'fsp_ne_<plantid>_flow_grid_power' (FusionSolarPlus plant stats).
        """
        patterns = sensor_def.matchers.get(source, [])
        object_ids = {
            e.entity_id.split(".", 1)[1]: e.entity_id for e in entities
        }
        for pattern in patterns:
            if pattern in object_ids:
                return object_ids[pattern]
        for pattern in patterns:
            suffix_matches = [
                entity_id
                for object_id, entity_id in object_ids.items()
                if object_id.endswith(f"_{pattern}")
            ]
            if suffix_matches:
                return sorted(suffix_matches, key=len)[0]
        return None

    # ------------------------------------------------------------
    # Runtime
    # ------------------------------------------------------------
    async def async_start(self) -> None:
        self.discover()
        tracked = sorted(
            {eid for sources in self.candidates.values() for eid in sources.values()}
        )
        if tracked:
            self._unsub = async_track_state_change_event(
                self.hass, tracked, self._handle_state_change
            )
        self._refresh_data()

    async def async_stop(self) -> None:
        if self._unsub:
            self._unsub()
            self._unsub = None

    @callback
    def _handle_state_change(self, event: Event) -> None:
        self._refresh_data()

    @callback
    def _refresh_data(self) -> None:
        data: dict[str, ResolvedValue] = {}
        for key, per_source in self.candidates.items():
            data[key] = self._resolve(key, per_source)
        self._update_source_availability()
        self.async_set_updated_data(data)

    def _resolve(self, key: str, per_source: dict[str, str]) -> ResolvedValue:
        sensor_def = SENSOR_DEFS_BY_KEY[key]
        for source in self.priority:
            entity_id = per_source.get(source)
            if not entity_id:
                continue
            state = self.hass.states.get(entity_id)
            if state is None or state.state in BAD_STATES:
                continue
            value = self._normalize(sensor_def, state)
            if value is not None:
                return ResolvedValue(value, source, entity_id)
        return ResolvedValue(None, None, None)

    @staticmethod
    def _normalize(sensor_def: HubSensorDef, state) -> Any:
        """Convert source value to the canonical unit (W, kWh, °C)."""
        raw = state.state
        try:
            value = float(raw)
        except (ValueError, TypeError):
            return raw  # non-numeric passthrough (e.g. status strings)

        src_unit = state.attributes.get("unit_of_measurement")
        dst_unit = sensor_def.unit
        if not src_unit or not dst_unit or src_unit == dst_unit:
            return value
        # reactive power is not covered by HA unit converters
        if dst_unit == "var" and src_unit in ("kvar", "kVar"):
            return round(value * 1000, 1)
        try:
            for converter in (PowerConverter, EnergyConverter, TemperatureConverter):
                if (
                    src_unit in converter.VALID_UNITS
                    and dst_unit in converter.VALID_UNITS
                ):
                    return round(converter.convert(value, src_unit, dst_unit), 3)
        except Exception:  # noqa: BLE001
            _LOGGER.debug(
                "Unit conversion failed for %s: %s -> %s",
                state.entity_id,
                src_unit,
                dst_unit,
            )
        return value

    # ------------------------------------------------------------
    # Source availability + alerts
    # ------------------------------------------------------------
    def _update_source_availability(self) -> None:
        for source, entity_ids in self.source_entities.items():
            if not entity_ids:
                continue
            unavailable = 0
            for entity_id in entity_ids:
                state = self.hass.states.get(entity_id)
                if state is None or state.state in BAD_STATES:
                    unavailable += 1
            available = (unavailable / len(entity_ids)) < SOURCE_OFFLINE_THRESHOLD
            previous = self.source_available.get(source)
            self.source_available[source] = available

            if previous is True and not available:
                self._fire_alert(source, offline=True)
            elif previous is False and available:
                self._fire_alert(source, offline=False)

    def _fire_alert(self, source: str, offline: bool) -> None:
        name = SOURCE_NAMES.get(source, source)
        self.hass.bus.async_fire(
            f"{DOMAIN}_source_{'offline' if offline else 'online'}",
            {"source": source, "name": name},
        )
        if not self.notify_on_disconnect:
            return
        if offline:
            self.hass.async_create_task(
                self.hass.services.async_call(
                    "persistent_notification",
                    "create",
                    {
                        "notification_id": f"{DOMAIN}_{source}_offline",
                        "title": "Huawei Fusion Hub",
                        "message": (
                            f"Source **{name}** is offline. "
                            "Values are now served by the next available source."
                        ),
                    },
                )
            )
        else:
            self.hass.async_create_task(
                self.hass.services.async_call(
                    "persistent_notification",
                    "dismiss",
                    {"notification_id": f"{DOMAIN}_{source}_offline"},
                )
            )
