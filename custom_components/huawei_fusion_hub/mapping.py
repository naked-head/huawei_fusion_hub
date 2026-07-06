"""Canonical sensor definitions and per-source matchers.

Matchers map a source domain to an ordered list of object_id patterns
(the part of the entity_id after "sensor."). Matching is exact-first,
then suffix ("*_<pattern>") — this handles prefixed entities such as
FusionSolar kiosk ("homeassistant_<kioskid>_realtime_power") and
FusionSolarPlus plant stats ("fsp_ne_<id>_flow_grid_power").

All patterns verified against a real installation dump (2026-07-06):
Huawei Solar (Modbus) + FusionSolar kiosk + FusionSolarPlus.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import (
    PERCENTAGE,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfFrequency,
    UnitOfPower,
    UnitOfTemperature,
)

from .const import (
    SOURCE_FUSION_SOLAR,
    SOURCE_FUSION_SOLAR_PLUS,
    SOURCE_HUAWEI_SOLAR,
)

HS = SOURCE_HUAWEI_SOLAR
FS = SOURCE_FUSION_SOLAR
FSP = SOURCE_FUSION_SOLAR_PLUS


@dataclass(frozen=True)
class HubSensorDef:
    key: str
    name: str
    device_class: SensorDeviceClass | None = None
    state_class: SensorStateClass | None = None
    unit: str | None = None
    icon: str | None = None
    matchers: dict[str, list[str]] = field(default_factory=dict)


def _power(key, name, matchers, icon=None):
    return HubSensorDef(
        key=key, name=name, device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT, unit=UnitOfPower.WATT,
        icon=icon, matchers=matchers,
    )


def _energy(key, name, matchers, icon=None):
    return HubSensorDef(
        key=key, name=name, device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        unit=UnitOfEnergy.KILO_WATT_HOUR, icon=icon, matchers=matchers,
    )


def _voltage(key, name, matchers):
    return HubSensorDef(
        key=key, name=name, device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        unit=UnitOfElectricPotential.VOLT, matchers=matchers,
    )


def _current(key, name, matchers):
    return HubSensorDef(
        key=key, name=name, device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        unit=UnitOfElectricCurrent.AMPERE, matchers=matchers,
    )


def _percent(key, name, matchers, device_class=None, icon="mdi:percent"):
    return HubSensorDef(
        key=key, name=name, device_class=device_class,
        state_class=SensorStateClass.MEASUREMENT, unit=PERCENTAGE,
        icon=None if device_class else icon, matchers=matchers,
    )


def _text(key, name, matchers, icon=None):
    return HubSensorDef(key=key, name=name, icon=icon, matchers=matchers)


SENSOR_DEFS: list[HubSensorDef] = [
    # ------------------------------------------------------------
    # Inverter
    # ------------------------------------------------------------
    _power("pv_active_power", "PV active power", {
        HS: ["inverter_active_power"],
        FSP: ["current_active_power"],
    }),
    _power("pv_input_power", "PV input power", {
        HS: ["inverter_input_power"],
        FSP: ["flow_solar_power"],
    }, icon="mdi:solar-power"),
    _energy("inverter_yield_today", "Inverter yield today", {
        HS: ["inverter_daily_yield"],
        FSP: ["daily_energy"],
    }),
    _energy("inverter_yield_month", "Inverter yield this month", {
        HS: ["inverter_monthly_yield"],
    }),
    _energy("inverter_yield_year", "Inverter yield this year", {
        HS: ["inverter_yearly_yield"],
    }),
    _energy("inverter_yield_total", "Inverter yield total", {
        HS: ["inverter_total_yield"],
        FSP: ["total_energy_produced"],
    }),
    HubSensorDef(
        key="inverter_temperature", name="Inverter temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        unit=UnitOfTemperature.CELSIUS,
        matchers={
            HS: ["inverter_internal_temperature"],
            FSP: ["temperature"],
        },
    ),
    _percent("inverter_efficiency", "Inverter efficiency", {
        HS: ["inverter_efficiency"],
    }),
    HubSensorDef(
        key="inverter_power_factor", name="Inverter power factor",
        device_class=SensorDeviceClass.POWER_FACTOR,
        state_class=SensorStateClass.MEASUREMENT,
        matchers={
            HS: ["inverter_power_factor"],
            FSP: ["power_factor"],
        },
    ),
    HubSensorDef(
        key="inverter_reactive_power", name="Inverter reactive power",
        device_class=SensorDeviceClass.REACTIVE_POWER,
        state_class=SensorStateClass.MEASUREMENT,
        unit="var",
        matchers={
            HS: ["inverter_reactive_power"],
            FSP: ["reactive_power"],
        },
    ),
    _text("inverter_status", "Inverter status", {
        HS: ["inverter_device_status"],
        FSP: ["status"],
    }, icon="mdi:power-settings"),
    HubSensorDef(
        key="inverter_insulation_resistance", name="Insulation resistance",
        state_class=SensorStateClass.MEASUREMENT,
        unit="MΩ", icon="mdi:omega",
        matchers={
            HS: ["inverter_insulation_resistance"],
            FSP: ["insulation_resistance"],
        },
    ),
    _voltage("inverter_phase_a_voltage", "Inverter phase A voltage", {
        HS: ["inverter_phase_a_voltage"],
        FSP: ["phase_a_voltage"],
    }),
    _current("inverter_phase_a_current", "Inverter phase A current", {
        HS: ["inverter_phase_a_current"],
        FSP: ["phase_a_current"],
    }),
    HubSensorDef(
        key="inverter_grid_frequency", name="Inverter grid frequency",
        device_class=SensorDeviceClass.FREQUENCY,
        state_class=SensorStateClass.MEASUREMENT,
        unit=UnitOfFrequency.HERTZ,
        matchers={
            FSP: ["grid_frequency"],
        },
    ),
    # ------------------------------------------------------------
    # PV strings
    # ------------------------------------------------------------
    _voltage("pv_1_voltage", "PV string 1 voltage", {
        HS: ["inverter_pv_1_voltage"],
        FSP: ["pv_1_input_voltage"],
    }),
    _current("pv_1_current", "PV string 1 current", {
        HS: ["inverter_pv_1_current"],
        FSP: ["pv_1_input_current"],
    }),
    _power("pv_1_power", "PV string 1 power", {
        FSP: ["pv_1_input_power"],
    }, icon="mdi:solar-panel"),
    _voltage("pv_2_voltage", "PV string 2 voltage", {
        HS: ["inverter_pv_2_voltage"],
        FSP: ["pv_2_input_voltage"],
    }),
    _current("pv_2_current", "PV string 2 current", {
        HS: ["inverter_pv_2_current"],
        FSP: ["pv_2_input_current"],
    }),
    _power("pv_2_power", "PV string 2 power", {
        FSP: ["pv_2_input_power"],
    }, icon="mdi:solar-panel"),
    # ------------------------------------------------------------
    # Meter / grid
    # ------------------------------------------------------------
    _power("meter_active_power", "Meter active power", {
        HS: ["power_meter_active_power"],
        FSP: ["active_power"],
    }, icon="mdi:transmission-tower"),
    HubSensorDef(
        key="meter_reactive_power", name="Meter reactive power",
        device_class=SensorDeviceClass.REACTIVE_POWER,
        state_class=SensorStateClass.MEASUREMENT,
        unit="var",
        matchers={
            HS: ["power_meter_reactive_power"],
            FSP: ["reactive_power_2"],
        },
    ),
    HubSensorDef(
        key="meter_power_factor", name="Meter power factor",
        device_class=SensorDeviceClass.POWER_FACTOR,
        state_class=SensorStateClass.MEASUREMENT,
        matchers={
            HS: ["power_meter_power_factor"],
            FSP: ["power_factor_2"],
        },
    ),
    _voltage("meter_voltage", "Meter voltage", {
        HS: ["power_meter_voltage"],
        FSP: ["phase_a_voltage_2"],
    }),
    _current("meter_current", "Meter current", {
        HS: ["power_meter_current"],
        FSP: ["phase_a_current_2"],
    }),
    HubSensorDef(
        key="meter_frequency", name="Meter grid frequency",
        device_class=SensorDeviceClass.FREQUENCY,
        state_class=SensorStateClass.MEASUREMENT,
        unit=UnitOfFrequency.HERTZ,
        matchers={
            HS: ["power_meter_frequency"],
            FSP: ["grid_frequency_2"],
        },
    ),
    # Verified: FSP positive_active_energy == HS power_meter_exported,
    # FSP negative_active_energy == HS power_meter_consumption.
    _energy("grid_exported_energy", "Grid exported energy", {
        HS: ["power_meter_exported"],
        FSP: ["positive_active_energy"],
    }, icon="mdi:transmission-tower-import"),
    _energy("grid_imported_energy", "Grid imported energy", {
        HS: ["power_meter_consumption"],
        FSP: ["negative_active_energy"],
    }, icon="mdi:transmission-tower-export"),
    _text("meter_status", "Meter status", {
        HS: ["power_meter_meter_status"],
        FSP: ["meter_status"],
    }, icon="mdi:meter-electric"),
    # ------------------------------------------------------------
    # Battery (system level)
    # ------------------------------------------------------------
    _percent("battery_soc", "Battery state of charge", {
        HS: ["battery_state_of_capacity"],
        FSP: ["state_of_charge"],
    }, device_class=SensorDeviceClass.BATTERY),
    _power("battery_power", "Battery charge/discharge power", {
        HS: ["battery_charge_discharge_power"],
        FSP: ["charge_discharge_power"],
    }, icon="mdi:battery-charging"),
    _energy("battery_charged_today", "Battery charged today", {
        HS: ["battery_day_charge"],
        FSP: ["energy_charged_today"],
    }, icon="mdi:battery-plus"),
    _energy("battery_discharged_today", "Battery discharged today", {
        HS: ["battery_day_discharge"],
        FSP: ["energy_discharged_today"],
    }, icon="mdi:battery-minus"),
    _energy("battery_total_charge", "Battery total charge", {
        HS: ["battery_total_charge"],
    }),
    _energy("battery_total_discharge", "Battery total discharge", {
        HS: ["battery_total_discharge"],
    }),
    _voltage("battery_bus_voltage", "Battery bus voltage", {
        HS: ["battery_bus_voltage"],
        FSP: ["bus_voltage"],
    }),
    _current("battery_bus_current", "Battery bus current", {
        HS: ["battery_bus_current"],
        FSP: ["module_1_bus_current"],
    }),
    HubSensorDef(
        key="battery_temperature", name="Battery temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        unit=UnitOfTemperature.CELSIUS,
        matchers={
            HS: ["battery_1_temperatura", "battery_1_temperature"],
            FSP: ["module_1_internal_temperature"],
        },
    ),
    _text("battery_status", "Battery status", {
        HS: ["battery_status"],
        FSP: ["operating_status"],
    }, icon="mdi:battery-heart-variant"),
    _text("battery_working_mode", "Battery working mode", {
        HS: ["battery_1_modo_di_funzionamento", "battery_1_working_mode"],
        FSP: ["charge_discharge_mode"],
    }, icon="mdi:battery-sync"),
    HubSensorDef(
        key="battery_rated_capacity", name="Battery rated capacity",
        device_class=SensorDeviceClass.ENERGY_STORAGE,
        unit=UnitOfEnergy.KILO_WATT_HOUR, icon="mdi:battery-high",
        matchers={
            FSP: ["rated_capacity"],
        },
    ),
    # ------------------------------------------------------------
    # Plant level
    # ------------------------------------------------------------
    _power("plant_power", "Plant realtime power", {
        FS: ["realtime_power"],
        FSP: ["flow_solar_power"],
    }, icon="mdi:solar-power-variant"),
    _energy("plant_energy_today", "Plant energy today", {
        FS: ["total_current_day_energy"],
        FSP: ["today_energy"],
    }),
    _energy("plant_energy_month", "Plant energy this month", {
        FS: ["total_current_month_energy"],
        FSP: ["monthly_energy"],
    }),
    _energy("plant_energy_year", "Plant energy this year", {
        FS: ["total_current_year_energy"],
        FSP: ["yearly_energy"],
    }),
    _energy("plant_energy_total", "Plant energy total", {
        FS: ["total_lifetime_energy"],
        FSP: ["total_energy"],
    }),
    # ------------------------------------------------------------
    # Consumption / flows (FusionSolarPlus only)
    # ------------------------------------------------------------
    _energy("consumption_today", "Consumption today", {
        FSP: ["consumption_today", "total_consumption"],
    }, icon="mdi:home-lightning-bolt"),
    _energy("self_used_energy_today", "Self-used energy today", {
        FSP: ["self_used_energy_today"],
    }, icon="mdi:home-battery"),
    _energy("pv_feed_in_energy_today", "PV feed-in energy today", {
        FSP: ["pv_feed_in_energy"],
    }, icon="mdi:transmission-tower-import"),
    _energy("imported_grid_energy_today", "Imported grid energy today", {
        FSP: ["imported_grid_energy"],
    }, icon="mdi:transmission-tower-export"),
    _percent("self_consumption_ratio", "Self-consumption ratio", {
        FSP: ["self_consumption_ratio"],
    }),
    _percent("grid_import_ratio", "Grid import ratio", {
        FSP: ["grid_import_ratio"],
    }),
    _power("flow_battery_power", "Flow battery power", {
        FSP: ["flow_battery_power"],
    }, icon="mdi:battery-arrow-up-outline"),
    _power("flow_load_power", "Flow load power", {
        FSP: ["flow_load_power"],
    }, icon="mdi:home-lightning-bolt-outline"),
    _power("flow_grid_power", "Flow grid power", {
        FSP: ["flow_grid_power"],
    }, icon="mdi:transmission-tower"),
]

SENSOR_DEFS_BY_KEY = {d.key: d for d in SENSOR_DEFS}
