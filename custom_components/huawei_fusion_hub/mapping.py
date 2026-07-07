"""Canonical sensor definitions, generated programmatically.

Full union of the sensor entities exposed by the three sources.
See ENTITY_MAP.md for the human-readable correspondence table.

Pattern syntax and matching rules are documented in coordinator._match:
unique_id primary layer ("Model:pattern" restricts to a device model),
object_id fallback layer for older source versions.
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
    UnitOfTime,
)

from .const import (
    DEVICE_BATTERY,
    DEVICE_BATTERY_UNIT_1,
    DEVICE_BATTERY_UNIT_2,
    DEVICE_INVERTER,
    DEVICE_METER,
    DEVICE_PLANT,
    SOURCE_FUSION_SOLAR,
    SOURCE_FUSION_SOLAR_PLUS,
    SOURCE_HUAWEI_SOLAR,
)

HS = SOURCE_HUAWEI_SOLAR
FS = SOURCE_FUSION_SOLAR
FSP = SOURCE_FUSION_SOLAR_PLUS

INV = "Inverter"
BAT = "Battery"
PWS = "Power Sensor"
PLT = "Plant"


@dataclass(frozen=True)
class HubSensorDef:
    key: str
    name: str
    device: str
    device_class: SensorDeviceClass | None = None
    state_class: SensorStateClass | None = None
    unit: str | None = None
    icon: str | None = None
    matchers: dict[str, list[str]] = field(default_factory=dict)
    fallbacks: dict[str, list[str]] = field(default_factory=dict)


# kind -> (device_class, state_class, unit)
_KINDS = {
    "power": (SensorDeviceClass.POWER, SensorStateClass.MEASUREMENT, UnitOfPower.WATT),
    "energy": (SensorDeviceClass.ENERGY, SensorStateClass.TOTAL_INCREASING, UnitOfEnergy.KILO_WATT_HOUR),
    "energy_storage": (SensorDeviceClass.ENERGY_STORAGE, None, UnitOfEnergy.KILO_WATT_HOUR),
    "voltage": (SensorDeviceClass.VOLTAGE, SensorStateClass.MEASUREMENT, UnitOfElectricPotential.VOLT),
    "current": (SensorDeviceClass.CURRENT, SensorStateClass.MEASUREMENT, UnitOfElectricCurrent.AMPERE),
    "percent": (None, SensorStateClass.MEASUREMENT, PERCENTAGE),
    "battery": (SensorDeviceClass.BATTERY, SensorStateClass.MEASUREMENT, PERCENTAGE),
    "temp": (SensorDeviceClass.TEMPERATURE, SensorStateClass.MEASUREMENT, UnitOfTemperature.CELSIUS),
    "freq": (SensorDeviceClass.FREQUENCY, SensorStateClass.MEASUREMENT, UnitOfFrequency.HERTZ),
    "pf": (SensorDeviceClass.POWER_FACTOR, SensorStateClass.MEASUREMENT, None),
    "reactive": (SensorDeviceClass.REACTIVE_POWER, SensorStateClass.MEASUREMENT, "var"),
    "resistance": (None, SensorStateClass.MEASUREMENT, "MΩ"),
    "minutes": (SensorDeviceClass.DURATION, SensorStateClass.MEASUREMENT, UnitOfTime.MINUTES),
    "text": (None, None, None),
}


def _def(key, name, device, kind, hs=None, fsp=None, fs=None, icon=None):
    device_class, state_class, unit = _KINDS[kind]
    matchers: dict[str, list[str]] = {}
    if hs:
        matchers[HS] = [hs] if isinstance(hs, str) else list(hs)
    if fsp:
        matchers[FSP] = [fsp] if isinstance(fsp, str) else list(fsp)
    if fs:
        matchers[FS] = [fs] if isinstance(fs, str) else list(fs)
    return HubSensorDef(
        key=key, name=name, device=device, device_class=device_class,
        state_class=state_class, unit=unit, icon=icon, matchers=matchers,
        fallbacks=_FALLBACKS.get(key, {}),
    )


# object_id fallbacks for older source versions (v0.2 verified set)
_FALLBACKS: dict[str, dict[str, list[str]]] = {
    "pv_active_power": {HS: ["inverter_active_power"], FSP: ["current_active_power"]},
    "pv_input_power": {HS: ["inverter_input_power"], FSP: ["flow_solar_power"]},
    "inverter_yield_today": {HS: ["inverter_daily_yield"], FSP: ["daily_energy"]},
    "inverter_yield_month": {HS: ["inverter_monthly_yield"]},
    "inverter_yield_year": {HS: ["inverter_yearly_yield"]},
    "inverter_yield_total": {HS: ["inverter_total_yield"], FSP: ["total_energy_produced"]},
    "inverter_temperature": {HS: ["inverter_internal_temperature"], FSP: ["temperature"]},
    "inverter_efficiency": {HS: ["inverter_efficiency"]},
    "inverter_power_factor": {HS: ["inverter_power_factor"], FSP: ["power_factor"]},
    "inverter_reactive_power": {HS: ["inverter_reactive_power"], FSP: ["reactive_power"]},
    "inverter_status": {HS: ["inverter_device_status"], FSP: ["status"]},
    "inverter_insulation_resistance": {
        HS: ["inverter_insulation_resistance"], FSP: ["insulation_resistance"],
    },
    "inverter_phase_a_voltage": {HS: ["inverter_phase_a_voltage"], FSP: ["phase_a_voltage"]},
    "inverter_phase_a_current": {HS: ["inverter_phase_a_current"], FSP: ["phase_a_current"]},
    "inverter_grid_frequency": {FSP: ["grid_frequency"]},
    "pv_1_voltage": {HS: ["inverter_pv_1_voltage"], FSP: ["pv_1_input_voltage"]},
    "pv_1_current": {HS: ["inverter_pv_1_current"], FSP: ["pv_1_input_current"]},
    "pv_1_power": {FSP: ["pv_1_input_power"]},
    "pv_2_voltage": {HS: ["inverter_pv_2_voltage"], FSP: ["pv_2_input_voltage"]},
    "pv_2_current": {HS: ["inverter_pv_2_current"], FSP: ["pv_2_input_current"]},
    "pv_2_power": {FSP: ["pv_2_input_power"]},
    "meter_active_power": {HS: ["power_meter_active_power"], FSP: ["active_power"]},
    "meter_reactive_power": {HS: ["power_meter_reactive_power"], FSP: ["reactive_power_2"]},
    "meter_power_factor": {HS: ["power_meter_power_factor"], FSP: ["power_factor_2"]},
    "meter_phase_a_voltage": {HS: ["power_meter_voltage"], FSP: ["phase_a_voltage_2"]},
    "meter_phase_a_current": {HS: ["power_meter_current"], FSP: ["phase_a_current_2"]},
    "meter_frequency": {HS: ["power_meter_frequency"], FSP: ["grid_frequency_2"]},
    "grid_exported_energy": {HS: ["power_meter_exported"], FSP: ["positive_active_energy"]},
    "grid_imported_energy": {HS: ["power_meter_consumption"], FSP: ["negative_active_energy"]},
    "meter_status": {HS: ["power_meter_meter_status"], FSP: ["meter_status"]},
    "battery_soc": {HS: ["battery_state_of_capacity"], FSP: ["state_of_charge"]},
    "battery_power": {HS: ["battery_charge_discharge_power"], FSP: ["charge_discharge_power"]},
    "battery_charged_today": {HS: ["battery_day_charge"], FSP: ["energy_charged_today"]},
    "battery_discharged_today": {HS: ["battery_day_discharge"], FSP: ["energy_discharged_today"]},
    "battery_total_charge": {HS: ["battery_total_charge"]},
    "battery_total_discharge": {HS: ["battery_total_discharge"]},
    "battery_bus_voltage": {HS: ["battery_bus_voltage"], FSP: ["bus_voltage"]},
    "battery_bus_current": {HS: ["battery_bus_current"]},
    "battery_status": {HS: ["battery_status"], FSP: ["operating_status"]},
    "battery_working_mode": {FSP: ["charge_discharge_mode"]},
    "battery_rated_capacity": {FSP: ["rated_capacity"]},
    "battery_unit_1_temperature": {FSP: ["module_1_internal_temperature"]},
    "battery_unit_1_bus_current": {FSP: ["module_1_bus_current"]},
    "plant_power": {FS: ["realtime_power"], FSP: ["flow_solar_power"]},
    "plant_energy_today": {FS: ["total_current_day_energy"], FSP: ["today_energy"]},
    "plant_energy_month": {FS: ["total_current_month_energy"], FSP: ["monthly_energy"]},
    "plant_energy_year": {FS: ["total_current_year_energy"], FSP: ["yearly_energy"]},
    "plant_energy_total": {FS: ["total_lifetime_energy"], FSP: ["total_energy"]},
    "consumption_today": {FSP: ["consumption_today"]},
    "self_used_energy_today": {FSP: ["self_used_energy_today"]},
    "pv_feed_in_energy_today": {FSP: ["pv_feed_in_energy"]},
    "imported_grid_energy_today": {FSP: ["imported_grid_energy"]},
    "self_consumption_ratio": {FSP: ["self_consumption_ratio"]},
    "grid_import_ratio": {FSP: ["grid_import_ratio"]},
    "flow_battery_power": {FSP: ["flow_battery_power"]},
    "flow_load_power": {FSP: ["flow_load_power"]},
    "flow_grid_power": {FSP: ["flow_grid_power"]},
}


def _build() -> list[HubSensorDef]:
    defs: list[HubSensorDef] = []
    d = defs.append
    DI, DM, DB, DP = DEVICE_INVERTER, DEVICE_METER, DEVICE_BATTERY, DEVICE_PLANT

    # ---------------- Inverter ----------------
    d(_def("inverter_rated_power", "Rated power", DI, "power",
           hs="rated_power", fsp=f"{INV}:10006"))
    d(_def("inverter_p_max", "P max", DI, "power", hs="p_max"))
    d(_def("pv_input_power", "PV input power", DI, "power",
           hs="input_power", fsp=f"{PLT}:flow_solar_power", icon="mdi:solar-power"))
    d(_def("inverter_line_voltage_a_b", "Line voltage A-B", DI, "voltage",
           hs="line_voltage_a_b"))
    d(_def("inverter_line_voltage_b_c", "Line voltage B-C", DI, "voltage",
           hs="line_voltage_b_c"))
    d(_def("inverter_line_voltage_c_a", "Line voltage C-A", DI, "voltage",
           hs="line_voltage_c_a"))
    d(_def("inverter_phase_a_voltage", "Phase A voltage", DI, "voltage",
           hs="phase_a_voltage", fsp=[f"{INV}:10011", f"{INV}:10008"]))
    d(_def("inverter_phase_b_voltage", "Phase B voltage", DI, "voltage",
           hs="phase_b_voltage", fsp=f"{INV}:10012"))
    d(_def("inverter_phase_c_voltage", "Phase C voltage", DI, "voltage",
           hs="phase_c_voltage", fsp=f"{INV}:10013"))
    d(_def("inverter_phase_a_current", "Phase A current", DI, "current",
           hs="phase_a_current", fsp=f"{INV}:10014"))
    d(_def("inverter_phase_b_current", "Phase B current", DI, "current",
           hs="phase_b_current", fsp=f"{INV}:10015"))
    d(_def("inverter_phase_c_current", "Phase C current", DI, "current",
           hs="phase_c_current", fsp=f"{INV}:10016"))
    d(_def("inverter_day_active_power_peak", "Day active power peak", DI, "power",
           hs="day_active_power_peak"))
    d(_def("pv_active_power", "PV active power", DI, "power",
           hs="active_power", fsp=f"{INV}:10018"))
    d(_def("inverter_reactive_power", "Reactive power", DI, "reactive",
           hs="reactive_power", fsp=f"{INV}:10019"))
    d(_def("inverter_power_factor", "Power factor", DI, "pf",
           hs="power_factor", fsp=f"{INV}:10020"))
    d(_def("inverter_grid_frequency", "Grid frequency", DI, "freq",
           hs="grid_frequency", fsp=f"{INV}:10021"))
    d(_def("inverter_efficiency", "Efficiency", DI, "percent",
           hs="efficiency", icon="mdi:percent"))
    d(_def("inverter_temperature", "Temperature", DI, "temp",
           hs="internal_temperature", fsp=f"{INV}:10023"))
    d(_def("inverter_insulation_resistance", "Insulation resistance", DI,
           "resistance", hs="insulation_resistance", fsp=f"{INV}:10024",
           icon="mdi:omega"))
    d(_def("inverter_status", "Status", DI, "text",
           hs="device_status", fsp=f"{INV}:10025", icon="mdi:power-settings"))
    d(_def("inverter_startup_time", "Last startup time", DI, "text",
           hs="startup_time", fsp=f"{INV}:10027", icon="mdi:clock-start"))
    d(_def("inverter_shutdown_time", "Last shutdown time", DI, "text",
           hs="shutdown_time", fsp=f"{INV}:10028", icon="mdi:clock-end"))
    d(_def("inverter_yield_total", "Yield total", DI, "energy",
           hs="accumulated_yield_energy", fsp=f"{INV}:10029"))
    d(_def("inverter_total_dc_input_energy", "Total DC input energy", DI,
           "energy", hs="total_dc_input_power"))
    d(_def("inverter_statistics_time", "Statistics time", DI, "text",
           hs="current_electricity_generation_statistics_time",
           icon="mdi:clock-outline"))
    d(_def("inverter_yield_hour", "Yield this hour", DI, "energy",
           hs="hourly_yield_energy"))
    d(_def("inverter_yield_today", "Yield today", DI, "energy",
           hs="daily_yield_energy", fsp=f"{INV}:10032"))
    d(_def("inverter_yield_month", "Yield this month", DI, "energy",
           hs="monthly_yield_energy"))
    d(_def("inverter_yield_year", "Yield this year", DI, "energy",
           hs="yearly_yield_energy"))
    d(_def("inverter_state_1", "State 1", DI, "text", hs="state_1",
           icon="mdi:state-machine"))
    d(_def("inverter_output_mode", "Output mode", DI, "text",
           fsp=f"{INV}:21029", icon="mdi:sine-wave"))
    for n, (v, c, p) in {1: ("11001", "11002", "11003"),
                         2: ("11004", "11005", "11006")}.items():
        d(_def(f"pv_{n}_voltage", f"PV string {n} voltage", DI, "voltage",
               hs=f"pv_0{n}_voltage", fsp=f"{INV}:{v}"))
        d(_def(f"pv_{n}_current", f"PV string {n} current", DI, "current",
               hs=f"pv_0{n}_current", fsp=f"{INV}:{c}"))
        d(_def(f"pv_{n}_power", f"PV string {n} power", DI, "power",
               fsp=f"{INV}:{p}", icon="mdi:solar-panel"))

    # ---------------- Power Meter ----------------
    d(_def("meter_status", "Status", DM, "text",
           hs="meter_status", fsp=f"{PWS}:10001", icon="mdi:meter-electric"))
    d(_def("meter_active_power", "Active power", DM, "power",
           hs="power_meter_active_power",
           fsp=[f"{PWS}:10004", f"{PWS}:11207", f"{PWS}:2101271"],
           icon="mdi:transmission-tower"))
    d(_def("meter_reactive_power", "Reactive power", DM, "reactive",
           hs="power_meter_reactive_power",
           fsp=[f"{PWS}:10005", f"{PWS}:11208", f"{PWS}:2101272"]))
    d(_def("meter_power_factor", "Power factor", DM, "pf",
           hs="active_grid_power_factor",
           fsp=[f"{PWS}:10006", f"{PWS}:10014", f"{PWS}:2101280"]))
    d(_def("meter_frequency", "Grid frequency", DM, "freq",
           hs="active_grid_frequency", fsp=f"{PWS}:10007"))
    d(_def("grid_exported_energy", "Grid exported energy", DM, "energy",
           hs="grid_exported_energy", fsp=[f"{PWS}:10008", f"{PWS}:11116"],
           icon="mdi:transmission-tower-import"))
    d(_def("grid_imported_energy", "Grid imported energy", DM, "energy",
           hs="grid_accumulated_energy", fsp=[f"{PWS}:10009", f"{PWS}:11115"],
           icon="mdi:transmission-tower-export"))
    d(_def("meter_reactive_energy", "Reactive energy", DM, "text",
           hs="grid_accumulated_reactive_power", icon="mdi:counter"))
    for ph, (hsv, fspv, hsc, fspc, hsp, fspp) in {
        "a": ("grid_a_voltage", [f"{PWS}:10002", f"{PWS}:11204", f"{PWS}:2101256"],
              "active_grid_a_current", [f"{PWS}:10003", f"{PWS}:2101268"],
              "active_grid_a_power", [f"{PWS}:10019", f"{PWS}:2101281"]),
        "b": ("grid_b_voltage", [f"{PWS}:10010", f"{PWS}:11205", f"{PWS}:2101257"],
              "active_grid_b_current", [f"{PWS}:10012", f"{PWS}:2101269"],
              "active_grid_b_power", [f"{PWS}:10020", f"{PWS}:2101282"]),
        "c": ("grid_c_voltage", [f"{PWS}:10011", f"{PWS}:11206", f"{PWS}:2101264"],
              "active_grid_c_current", [f"{PWS}:10013", f"{PWS}:2101270"],
              "active_grid_c_power", [f"{PWS}:10021", f"{PWS}:2101283"]),
    }.items():
        d(_def(f"meter_phase_{ph}_voltage", f"Phase {ph.upper()} voltage",
               DM, "voltage", hs=hsv, fsp=fspv))
        d(_def(f"meter_phase_{ph}_current", f"Phase {ph.upper()} current",
               DM, "current", hs=hsc, fsp=fspc))
        d(_def(f"meter_phase_{ph}_active_power", f"Phase {ph.upper()} active power",
               DM, "power", hs=hsp, fsp=fspp))
    d(_def("meter_line_voltage_a_b", "Line voltage A-B", DM, "voltage",
           hs="active_grid_a_b_voltage", fsp=f"{PWS}:2101252"))
    d(_def("meter_line_voltage_b_c", "Line voltage B-C", DM, "voltage",
           hs="active_grid_b_c_voltage", fsp=f"{PWS}:2101253"))
    d(_def("meter_line_voltage_c_a", "Line voltage C-A", DM, "voltage",
           hs="active_grid_c_a_voltage", fsp=f"{PWS}:2101254"))
    d(_def("meter_rs485_port_mode", "RS485-2 port mode", DM, "text",
           fsp=f"{PWS}:230700283"))
    d(_def("meter_wifi_signal_strength", "WiFi signal strength", DM, "text",
           fsp=f"{PWS}:15101", icon="mdi:wifi"))
    d(_def("meter_signal_strength", "Signal strength", DM, "text",
           fsp=f"{PWS}:15102", icon="mdi:signal"))
    d(_def("meter_communication_status", "Communication status", DM, "text",
           fsp=[f"{PWS}:2101249", f"{PWS}:2101602"], icon="mdi:lan-connect"))
    d(_def("meter_iacmeter", "iAcMeter", DM, "text", fsp=f"{PWS}:2101600"))
    d(_def("meter_iacmeter_ip", "iAcMeter IP", DM, "text",
           fsp=f"{PWS}:2101601", icon="mdi:ip-network"))
    d(_def("meter_iacmeter_mode", "iAcMeter mode", DM, "text",
           fsp=f"{PWS}:2101605"))
    d(_def("meter_data_source", "Meter data source", DM, "text",
           fsp=f"{PWS}:2101606"))

    # ---------------- Battery (system) ----------------
    d(_def("battery_soc", "State of charge", DB, "battery",
           hs="storage_state_of_capacity", fsp=f"{BAT}:10006"))
    d(_def("battery_power", "Charge/discharge power", DB, "power",
           hs="storage_charge_discharge_power", fsp=f"{BAT}:10004",
           icon="mdi:battery-charging"))
    d(_def("battery_charged_today", "Charged today", DB, "energy",
           hs="storage_current_day_charge_capacity", fsp=f"{BAT}:10001",
           icon="mdi:battery-plus"))
    d(_def("battery_discharged_today", "Discharged today", DB, "energy",
           hs="storage_current_day_discharge_capacity", fsp=f"{BAT}:10002",
           icon="mdi:battery-minus"))
    d(_def("battery_total_charge", "Total charge", DB, "energy",
           hs="storage_total_charge"))
    d(_def("battery_total_discharge", "Total discharge", DB, "energy",
           hs="storage_total_discharge"))
    d(_def("battery_status", "Status", DB, "text",
           hs="storage_running_status", fsp=f"{BAT}:10003",
           icon="mdi:battery-heart-variant"))
    d(_def("battery_bus_voltage", "Bus voltage", DB, "voltage",
           hs="storage_bus_voltage", fsp=f"{BAT}:10005"))
    d(_def("battery_bus_current", "Bus current", DB, "current",
           hs="storage_bus_current"))
    d(_def("battery_rated_capacity", "Rated capacity", DB, "energy_storage",
           hs="storage_rated_capacity", fsp=f"{BAT}:10013",
           icon="mdi:battery-high"))
    d(_def("battery_max_charge_power", "Maximum charge power", DB, "power",
           hs="storage_maximum_charge_power"))
    d(_def("battery_max_discharge_power", "Maximum discharge power", DB, "power",
           hs="storage_maximum_discharge_power"))
    d(_def("battery_working_mode", "Working mode", DB, "text",
           fsp=f"{BAT}:10008", icon="mdi:battery-sync"))
    d(_def("battery_backup_time", "Backup time", DB, "minutes",
           fsp=f"{BAT}:10015"))

    # ---------------- Battery units 1-2 (HS units <-> FSP modules) ----------------
    # FSP module signal ids per unit, extracted from FSP battery const.py
    fsp_unit = {
        1: {"no": "230320252", "status": "230320459", "sn": "230320275",
            "sw": "230320146", "soc": "230320463", "power": "230320473",
            "temp": "230320462", "charged_today": "230320469",
            "discharged_today": "230320470", "total_discharge": "230320108",
            "bus_v": "230320460", "bus_i": "230320461", "fe": "230320514",
            "total_charge": "230320107"},
        2: {"no": "230320253", "status": "230320464", "sn": "230320276",
            "sw": "230320145", "soc": "230320468", "power": "230320474",
            "temp": "230320467", "charged_today": "230320471",
            "discharged_today": "230320472", "total_discharge": "230320115",
            "bus_v": "230320465", "bus_i": "230320466", "fe": "230320515",
            "total_charge": "230320114"},
    }
    # FSP pack signal ids: {unit: {field: (pack1, pack2, pack3)}}
    fsp_pack = {
        1: {"no": ("230320265", "230320266", "230320267"),
            "firmware_version": ("230320148", "230320165", "230320181"),
            "serial_number": ("230320147", "230320164", "230320180"),
            "status": ("230320151", "230320168", "230320184"),
            "voltage": ("230320159", "230320174", "230320190"),
            "power": ("230320158", "230320173", "230320189"),
            "max_temperature": ("230320446", "230320448", "230320450"),
            "min_temperature": ("230320447", "230320449", "230320451"),
            "soc": ("230320152", "230320169", "230320185"),
            "total_discharge": ("230320163", "230320179", "230320194"),
            "health_check": ("230320492", "230320493", "230320494"),
            "heating_status": ("230320498", "230320499", "230320500")},
        2: {"no": ("230320268", "230320269", "230320270"),
            "firmware_version": ("230320196", "230320211", "230320226"),
            "serial_number": ("230320195", "230320210", "230320225"),
            "status": ("230320199", "230320214", "230320229"),
            "voltage": ("230320205", "230320220", "230320235"),
            "power": ("230320204", "230320219", "230320234"),
            "max_temperature": ("230320452", "230320454", "230320456"),
            "min_temperature": ("230320453", "230320455", "230320457"),
            "soc": ("230320200", "230320215", "230320230"),
            "total_discharge": ("230320209", "230320224", "230320239"),
            "health_check": ("230320495", "230320496", "230320497"),
            "heating_status": ("230320501", "230320502", "230320503")},
    }
    pack_fields = [
        # (field, name, kind, hs_template or None)
        ("no", "No.", "text", None),
        ("status", "Operating status", "text",
         "storage_unit_{u}_battery_pack_{p}_working_status"),
        ("firmware_version", "Firmware version", "text",
         "storage_unit_{u}_battery_pack_{p}_firmware_version"),
        ("serial_number", "Serial number", "text",
         "storage_unit_{u}_battery_pack_{p}_serial_number"),
        ("voltage", "Voltage", "voltage",
         "storage_unit_{u}_battery_pack_{p}_voltage"),
        ("power", "Charge/discharge power", "power",
         "storage_unit_{u}_battery_pack_{p}_charge_discharge_power"),
        ("soc", "State of charge", "battery",
         "storage_unit_{u}_battery_pack_{p}_state_of_capacity"),
        ("max_temperature", "Maximum temperature", "temp",
         "storage_unit_{u}_battery_pack_{p}_maximum_temperature"),
        ("min_temperature", "Minimum temperature", "temp",
         "storage_unit_{u}_battery_pack_{p}_minimum_temperature"),
        ("total_discharge", "Total discharge", "energy",
         "storage_unit_{u}_battery_pack_{p}_total_discharge"),
        ("health_check", "Health check", "text", None),
        ("heating_status", "Heating status", "text", None),
        # HS-only pack fields
        ("current", "Current", "current",
         "storage_unit_{u}_battery_pack_{p}_current"),
        ("soh_calibration", "SOH calibration", "text",
         "storage_unit_{u}_battery_pack_{p}_soh_calibration_status"),
        ("total_charge", "Total charge", "energy",
         "storage_unit_{u}_battery_pack_{p}_total_charge"),
    ]
    unit_devices = {1: DEVICE_BATTERY_UNIT_1, 2: DEVICE_BATTERY_UNIT_2}
    for u in (1, 2):
        dev = unit_devices[u]
        pref = f"battery_unit_{u}"
        sig = fsp_unit[u]
        d(_def(f"{pref}_working_mode", "Working mode", dev, "text",
               hs=f"storage_unit_{u}_working_mode_b", icon="mdi:battery-sync"))
        d(_def(f"{pref}_charged_today", "Charged today", dev, "energy",
               hs=f"storage_unit_{u}_current_day_charge_capacity",
               fsp=f"{BAT}:{sig['charged_today']}", icon="mdi:battery-plus"))
        d(_def(f"{pref}_discharged_today", "Discharged today", dev, "energy",
               hs=f"storage_unit_{u}_current_day_discharge_capacity",
               fsp=f"{BAT}:{sig['discharged_today']}", icon="mdi:battery-minus"))
        d(_def(f"{pref}_bus_current", "Bus current", dev, "current",
               hs=f"storage_unit_{u}_bus_current", fsp=f"{BAT}:{sig['bus_i']}"))
        d(_def(f"{pref}_bus_voltage", "Bus voltage", dev, "voltage",
               hs=f"storage_unit_{u}_bus_voltage", fsp=f"{BAT}:{sig['bus_v']}"))
        d(_def(f"{pref}_temperature", "Temperature", dev, "temp",
               hs=f"storage_unit_{u}_battery_temperature",
               fsp=f"{BAT}:{sig['temp']}"))
        d(_def(f"{pref}_remaining_time", "Remaining charge/discharge time",
               dev, "minutes",
               hs=f"storage_unit_{u}_remaining_charge_dis_charge_time"))
        d(_def(f"{pref}_total_charge", "Total charge", dev, "energy",
               hs=f"storage_unit_{u}_total_charge",
               fsp=f"{BAT}:{sig['total_charge']}"))
        d(_def(f"{pref}_total_discharge", "Total discharge", dev, "energy",
               hs=f"storage_unit_{u}_total_discharge",
               fsp=f"{BAT}:{sig['total_discharge']}"))
        d(_def(f"{pref}_soc", "State of charge", dev, "battery",
               hs=f"storage_unit_{u}_state_of_capacity",
               fsp=f"{BAT}:{sig['soc']}"))
        d(_def(f"{pref}_status", "Status", dev, "text",
               hs=f"storage_unit_{u}_running_status",
               fsp=f"{BAT}:{sig['status']}", icon="mdi:battery-heart-variant"))
        d(_def(f"{pref}_power", "Charge/discharge power", dev, "power",
               hs=f"storage_unit_{u}_charge_discharge_power",
               fsp=f"{BAT}:{sig['power']}", icon="mdi:battery-charging"))
        d(_def(f"{pref}_no", "No.", dev, "text",
               hs=f"storage_unit_{u}_no", fsp=f"{BAT}:{sig['no']}"))
        d(_def(f"{pref}_sn", "Serial number", dev, "text",
               fsp=f"{BAT}:{sig['sn']}"))
        d(_def(f"{pref}_software_version", "Software version", dev, "text",
               hs=f"storage_unit_{u}_software_version",
               fsp=f"{BAT}:{sig['sw']}"))
        d(_def(f"{pref}_fe_connection", "FE connection", dev, "text",
               fsp=f"{BAT}:{sig['fe']}", icon="mdi:lan-connect"))
        if u == 1:
            d(_def(f"{pref}_soh_calibration", "SOH calibration", dev, "text",
                   hs="storage_unit_soh_calibration_status"))
        for p in (1, 2, 3):
            for f_key, f_name, f_kind, hs_tpl in pack_fields:
                hs_reg = hs_tpl.format(u=u, p=p) if hs_tpl else None
                fsp_sig = (
                    f"{BAT}:{fsp_pack[u][f_key][p - 1]}"
                    if f_key in fsp_pack[u] else None
                )
                if not hs_reg and not fsp_sig:
                    continue
                d(_def(f"{pref}_pack_{p}_{f_key}", f"Pack {p} {f_name.lower()}",
                       dev, f_kind, hs=hs_reg, fsp=fsp_sig))

    # ---------------- Plant ----------------
    d(_def("plant_power", "Realtime power", DP, "power",
           fs="realtime_power", fsp=f"{PLT}:flow_solar_power",
           icon="mdi:solar-power-variant"))
    d(_def("plant_energy_today", "Energy today", DP, "energy",
           fs="total_current_day_energy", fsp=f"{PLT}:dailyEnergy"))
    d(_def("plant_energy_month", "Energy this month", DP, "energy",
           fs="total_current_month_energy", fsp=f"{PLT}:monthEnergy"))
    d(_def("plant_energy_year", "Energy this year", DP, "energy",
           fs="total_current_year_energy", fsp=f"{PLT}:yearEnergy"))
    d(_def("plant_energy_total", "Energy total", DP, "energy",
           fs="total_lifetime_energy", fsp=f"{PLT}:cumulativeEnergy"))
    d(_def("plant_income_today", "Income today", DP, "text",
           fsp=f"{PLT}:dailyIncome", icon="mdi:cash"))
    d(_def("self_used_energy_today", "Self-used energy today", DP, "energy",
           fsp=f"{PLT}:totalSelfUseEnergy", icon="mdi:home-battery"))
    d(_def("consumption_today", "Consumption today", DP, "energy",
           fsp=f"{PLT}:dailyUseEnergy", icon="mdi:home-lightning-bolt"))
    d(_def("pv_self_consumption_energy", "PV self-consumption", DP, "energy",
           fsp=f"{PLT}:pvSelfConsumptionEnergy"))
    d(_def("pv_feed_in_energy_today", "PV feed-in energy today", DP, "energy",
           fsp=f"{PLT}:totalFeedInEnergy", icon="mdi:transmission-tower-import"))
    d(_def("imported_grid_energy_today", "Imported grid energy today", DP,
           "energy", fsp=f"{PLT}:totalGridImportEnergy",
           icon="mdi:transmission-tower-export"))
    d(_def("total_consumption", "Total consumption", DP, "energy",
           fsp=f"{PLT}:totalConsumptionEnergy"))
    d(_def("grid_import_ratio", "Grid import ratio", DP, "percent",
           fsp=f"{PLT}:gridImportRatio", icon="mdi:percent"))
    d(_def("self_consumption_ratio", "Self-consumption ratio", DP, "percent",
           fsp=f"{PLT}:pvSelfConsumptionRatio", icon="mdi:percent"))
    d(_def("self_consumption_ratio_by_production",
           "Self-consumption ratio (by production)", DP, "percent",
           fsp=f"{PLT}:pvSelfConsumptionRatioByProduction", icon="mdi:percent"))
    d(_def("flow_battery_power", "Flow battery power", DP, "power",
           fsp=f"{PLT}:flow_battery_power", icon="mdi:battery-arrow-up-outline"))
    d(_def("flow_load_power", "Flow load power", DP, "power",
           fsp=f"{PLT}:flow_load_power", icon="mdi:home-lightning-bolt-outline"))
    d(_def("flow_grid_power", "Flow grid power", DP, "power",
           fsp=f"{PLT}:flow_grid_power", icon="mdi:transmission-tower"))

    return defs


SENSOR_DEFS: list[HubSensorDef] = _build()
SENSOR_DEFS_BY_KEY = {d.key: d for d in SENSOR_DEFS}
