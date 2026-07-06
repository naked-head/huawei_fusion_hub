# Huawei Fusion Hub

Failover aggregation layer for Huawei solar installations in Home Assistant.

If you monitor your Huawei inverter, battery and power meter through more than one integration — [Huawei Solar](https://github.com/wlcrs/huawei_solar) (local Modbus), [FusionSolar](https://github.com/tijsverkoyen/HomeAssistant-FusionSolar) (Kiosk/OpenAPI) or [FusionSolarPlus](https://github.com/JortvanSchijndel/FusionSolarPlus) — this integration exposes a **single, stable set of entities** that automatically falls back to the next available source when one disconnects.

Your automations reference `sensor.hf_hub_*` entities and keep working even when your Modbus connection drops or the cloud API is down.

## Features

- **Priority-based failover** — for every quantity, the hub uses the highest-priority source currently available. Priority is configurable from the UI at any time.
- **Works with any combination** — one, two or all three source integrations.
- **Unified entities** — same entity IDs regardless of which source is serving the data. Units are normalized (W, kWh, °C) even when sources report differently (e.g. kW vs W).
- **Source transparency** — every hub sensor exposes `source` and `source_entity` attributes so you always know where the current value comes from.
- **Disconnect alerts** — one `binary_sensor` per source (`connectivity` device class), an event bus event (`huawei_fusion_hub_source_offline` / `_online`) and an optional persistent notification when a source goes down or recovers.
- **Zero extra polling** — the hub never contacts your inverter or the cloud. It only reads states that the source integrations already publish in Home Assistant, reacting to state changes in real time.

## Installation

### HACS (recommended)

1. Add this repository to HACS (or install it from the default catalog once accepted).
2. Install **Huawei Fusion Hub** and restart Home Assistant.
3. Go to *Settings → Devices & Services → Add Integration* and search for **Huawei Fusion Hub**.

### Manual

Copy `custom_components/huawei_fusion_hub` into your `config/custom_components` folder and restart Home Assistant.

## Configuration

Everything is configured from the UI:

1. **Select sources** — installed integrations are auto-detected and pre-selected.
2. **Set priority** — order the sources; the first available one wins.

You can change the priority and the alert behavior later from the integration's **Configure** button, without restarting.

## Exposed entities

All entities are grouped under a single *Huawei Fusion Hub* device.

**Inverter**: `pv_active_power`, `pv_input_power`, `inverter_yield_today` / `_month` / `_year` / `_total`, `inverter_temperature`, `inverter_efficiency`, `inverter_power_factor`, `inverter_reactive_power`, `inverter_status`, `inverter_insulation_resistance`, `inverter_phase_a_voltage` / `_current`, `inverter_grid_frequency`

**PV strings**: `pv_1_voltage` / `_current` / `_power`, `pv_2_voltage` / `_current` / `_power`

**Meter / grid**: `meter_active_power`, `meter_reactive_power`, `meter_power_factor`, `meter_voltage`, `meter_current`, `meter_frequency`, `grid_exported_energy`, `grid_imported_energy`, `meter_status`

**Battery**: `battery_soc`, `battery_power`, `battery_charged_today` / `_discharged_today`, `battery_total_charge` / `_discharge`, `battery_bus_voltage` / `_current`, `battery_temperature`, `battery_status`, `battery_working_mode`, `battery_rated_capacity`

**Plant**: `plant_power`, `plant_energy_today` / `_month` / `_year` / `_total`

**Consumption & flows**: `consumption_today`, `self_used_energy_today`, `pv_feed_in_energy_today`, `imported_grid_energy_today`, `self_consumption_ratio`, `grid_import_ratio`, `flow_battery_power`, `flow_load_power`, `flow_grid_power`

**Diagnostics**: `binary_sensor.hf_hub_<source>_available` per source (connectivity device class).

All sensor entity IDs use the `sensor.hf_hub_` prefix. A hub sensor is created only when at least one configured source provides that quantity — quantities available from a single source are exposed too, without failover.

## Automation example

Alert when the local Modbus connection drops:

```yaml
automation:
  - alias: "Huawei Solar offline"
    triggers:
      - trigger: state
        entity_id: binary_sensor.hf_hub_huawei_solar_available
        to: "off"
        for: "00:02:00"
    actions:
      - action: notify.mobile_app_phone
        data:
          message: "Huawei Solar (Modbus) is offline — hub switched to cloud fallback."
```

## How source availability is determined

A source is marked offline when more than 80% of its mapped entities are `unavailable` or `unknown`. This avoids false positives when a single entity is temporarily missing.

## License

GPL v3
