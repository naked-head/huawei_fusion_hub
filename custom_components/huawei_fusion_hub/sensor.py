"""Aggregated sensors exposed by the hub."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    ATTR_CANDIDATES,
    ATTR_SOURCE,
    ATTR_SOURCE_ENTITY,
    DEVICE_HUB,
    DEVICE_NAMES,
    DOMAIN,
    ENTITY_PREFIX,
    SIGNAL_NEW_KEYS,
)
from .coordinator import HubCoordinator
from .mapping import SENSOR_DEFS_BY_KEY, HubSensorDef


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: HubCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        HubSensor(coordinator, SENSOR_DEFS_BY_KEY[key])
        for key in coordinator.candidates
    )

    @callback
    def _add_new_keys(new_keys: list[str]) -> None:
        async_add_entities(
            HubSensor(coordinator, SENSOR_DEFS_BY_KEY[key]) for key in new_keys
        )

    entry.async_on_unload(
        async_dispatcher_connect(
            hass, f"{SIGNAL_NEW_KEYS}_{entry.entry_id}", _add_new_keys
        )
    )


class HubSensor(CoordinatorEntity[HubCoordinator], SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator: HubCoordinator, sensor_def: HubSensorDef) -> None:
        super().__init__(coordinator)
        self._def = sensor_def
        self._attr_unique_id = f"{ENTITY_PREFIX}_{sensor_def.key}"
        self._attr_suggested_object_id = f"{ENTITY_PREFIX}_{sensor_def.key}"
        self._attr_name = sensor_def.name
        self._attr_device_class = sensor_def.device_class
        self._attr_state_class = sensor_def.state_class
        self._attr_native_unit_of_measurement = sensor_def.unit
        self._attr_icon = sensor_def.icon
        device = sensor_def.device
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, device)},
            name=DEVICE_NAMES[device],
            manufacturer="naked-head",
            model="Aggregated device",
            entry_type=DeviceEntryType.SERVICE,
            via_device=(DOMAIN, DEVICE_HUB),
        )

    @property
    def native_value(self):
        resolved = self.coordinator.data.get(self._def.key)
        return resolved.value if resolved else None

    @property
    def available(self) -> bool:
        resolved = self.coordinator.data.get(self._def.key)
        return bool(resolved and resolved.value is not None)

    @property
    def extra_state_attributes(self):
        resolved = self.coordinator.data.get(self._def.key)
        return {
            ATTR_SOURCE: resolved.source if resolved else None,
            ATTR_SOURCE_ENTITY: resolved.source_entity if resolved else None,
            ATTR_CANDIDATES: self.coordinator.candidates.get(self._def.key, {}),
        }
