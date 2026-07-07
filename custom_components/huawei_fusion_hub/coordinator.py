"""Coordinator: discovers source entities, resolves values by priority."""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from homeassistant.core import Event, HomeAssistant, callback
from homeassistant.helpers import device_registry as dr, entity_registry as er
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
        device_registry = dr.async_get(self.hass)
        overrides: dict[str, dict[str, str]] = self.entry.options.get(
            CONF_OVERRIDES, {}
        )

        # index registry entries by platform (source domain),
        # each entry paired with its device model (for FSP disambiguation)
        by_source: dict[str, list[tuple[er.RegistryEntry, str]]] = {
            s: [] for s in self.priority
        }
        for entity in registry.entities.values():
            if entity.platform in by_source and entity.domain == "sensor":
                model = ""
                if entity.device_id:
                    device = device_registry.async_get(entity.device_id)
                    if device and device.model:
                        model = device.model
                by_source[entity.platform].append((entity, model))

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
        sensor_def: HubSensorDef,
        source: str,
        entities: list[tuple[er.RegistryEntry, str]],
    ) -> str | None:
        """Two-layer, language-independent matching.

        Layer 1 (primary): unique_id patterns from mapping.py. A pattern
        matches when the unique_id equals it or ends with "_pattern" /
        "-pattern" (case-insensitive). "Model:pattern" syntax restricts
        the match to entities whose device model equals Model (needed
        for FusionSolarPlus, which reuses numeric signal ids across
        device types). When both the definition and the registry entry
        declare a device class, they must agree.

        Layer 2 (fallback): same logic against object_ids, for older
        source versions with different unique_id schemes.
        """

        def _find(patterns: list[str], attr: str) -> str | None:
            for raw_pattern in patterns:
                if ":" in raw_pattern:
                    model_req, _, pattern = raw_pattern.partition(":")
                else:
                    model_req, pattern = None, raw_pattern
                pattern = pattern.lower()
                matches: list[tuple[int, str]] = []
                for entity, model in entities:
                    if model_req and model.lower() != model_req.lower():
                        continue
                    if attr == "unique_id":
                        haystack = (entity.unique_id or "").lower()
                    else:
                        haystack = entity.entity_id.split(".", 1)[1].lower()
                    if not (
                        haystack == pattern
                        or haystack.endswith(f"_{pattern}")
                        or haystack.endswith(f"-{pattern}")
                    ):
                        continue
                    if (
                        sensor_def.device_class
                        and entity.original_device_class
                        and str(entity.original_device_class)
                        != str(sensor_def.device_class)
                    ):
                        continue
                    matches.append((len(haystack), entity.entity_id))
                if matches:
                    # shortest haystack wins: "SER_active_power" beats
                    # "SER_power_meter_active_power" for "active_power"
                    return sorted(matches)[0][1]
            return None

        result = _find(sensor_def.matchers.get(source, []), "unique_id")
        if result:
            return result
        return _find(sensor_def.fallbacks.get(source, []), "object_id")

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
