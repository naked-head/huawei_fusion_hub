# Migrating the Energy Dashboard to Huawei Fusion Hub

This guide walks you through replacing the source integration entities with the corresponding `sensor.hf_hub_*` entities in the Home Assistant Energy Dashboard, while preserving your historical statistics.

> **⚠️ This procedure modifies the Home Assistant database directly. It is intended for advanced users who are comfortable working with SQLite from the command line.**
>
> **Always create a full backup before proceeding.** The author assumes no responsibility for data loss, corrupted databases, or any other damage resulting from following this guide.

---

## Why migrate?

The Energy Dashboard stores long-term statistics (hourly aggregates in kWh) tied to specific `statistic_id` values. When you switch from a source entity (e.g. `sensor.power_meter_consumption`) to the hub equivalent (e.g. `sensor.hf_hub_grid_imported_energy`), the dashboard starts fresh — all historical data appears to be gone.

It's not gone: the statistics are still in the database, just linked to the old entity name. This procedure renames the `statistic_id` so the Energy Dashboard sees the hub entity as having the full history.

---

## Prerequisites

- Huawei Fusion Hub installed and running with hub entities confirmed working
- SSH access to the Home Assistant server
- `sqlite3` command-line tool available
- A **full backup** (snapshot) of Home Assistant

---

## Entity mapping

The table below shows the Energy Dashboard roles and the corresponding entity from each source integration. Identify which source you are currently using, then note the hub entity you will migrate to.

| Role | Huawei Solar (Modbus) | FusionSolarPlus | Hub entity |
|------|-----------------------|-----------------|------------|
| Grid import (kWh) | `sensor.power_meter_consumption` | `sensor.positive_active_energy` | `sensor.hf_hub_grid_imported_energy` |
| Grid export (kWh) | `sensor.power_meter_exported` | `sensor.negative_active_energy` | `sensor.hf_hub_grid_exported_energy` |
| Grid power (W) | `sensor.power_meter_active_power` | `sensor.active_power` | `sensor.hf_hub_meter_active_power` |
| Solar yield (kWh) | `sensor.inverter_daily_yield` | `sensor.daily_energy` | `sensor.hf_hub_inverter_yield_today` |
| Battery charge (kWh) | `sensor.battery_day_charge` | `sensor.energy_charged_today` | `sensor.hf_hub_battery_charged_today` |
| Battery discharge (kWh) | `sensor.battery_day_discharge` | `sensor.energy_discharged_today` | `sensor.hf_hub_battery_discharged_today` |

> **Note:** your source entity names may differ depending on your configuration and language settings. Verify the actual entity IDs in **Developer Tools → States** before proceeding. FusionSolarPlus in particular creates entities with generic names (no prefix), so double-check that the entity belongs to the correct integration.

---

## Procedure

### Step 1 — Stop Home Assistant

```bash
ha core stop
```

### Step 2 — Identify the database IDs

Query the database to find the numeric IDs for both old (source) and new (hub) entities:

```bash
sqlite3 /config/home-assistant_v2.db <<'EOF'
.mode column
.headers on
SELECT id, statistic_id, source, unit_of_measurement
FROM statistics_meta
WHERE statistic_id IN (
  -- Source entities (replace with yours if different)
  'sensor.power_meter_consumption',
  'sensor.power_meter_exported',
  'sensor.power_meter_active_power',
  'sensor.inverter_daily_yield',
  'sensor.battery_day_charge',
  'sensor.battery_day_discharge',
  -- Hub entities
  'sensor.hf_hub_grid_imported_energy',
  'sensor.hf_hub_grid_exported_energy',
  'sensor.hf_hub_meter_active_power',
  'sensor.hf_hub_inverter_yield_today',
  'sensor.hf_hub_battery_charged_today',
  'sensor.hf_hub_battery_discharged_today'
);
EOF
```

You will see two groups, identifiable by the `statistic_id` name:

- **Source entities** — names matching your current source integration (e.g. `sensor.power_meter_*`, `sensor.inverter_*`, `sensor.battery_*`, or FusionSolarPlus equivalents). These carry months or years of accumulated statistics — their `id` values are the ones to preserve.
- **Hub entities** — names starting with `sensor.hf_hub_*`. These have only hours or days of data since Fusion Hub was installed — their `id` values will be deleted.

**Write down the `id` values for both groups.** You will need them in the next steps.

Example output:

```
id    statistic_id                            unit_of_measurement
----  --------------------------------------  -------------------
260   sensor.power_meter_consumption          kWh       ← SOURCE, keep this id
259   sensor.power_meter_exported             kWh       ← SOURCE, keep this id
257   sensor.power_meter_active_power         W         ← SOURCE, keep this id
252   sensor.inverter_daily_yield             kWh       ← SOURCE, keep this id
267   sensor.battery_day_charge               kWh       ← SOURCE, keep this id
268   sensor.battery_day_discharge            kWh       ← SOURCE, keep this id
3414  sensor.hf_hub_grid_imported_energy      kWh       ← HUB, will be deleted
3413  sensor.hf_hub_grid_exported_energy      kWh       ← HUB, will be deleted
3421  sensor.hf_hub_meter_active_power        W         ← HUB, will be deleted
3400  sensor.hf_hub_inverter_yield_today      kWh       ← HUB, will be deleted
3419  sensor.hf_hub_battery_charged_today     kWh       ← HUB, will be deleted
3420  sensor.hf_hub_battery_discharged_today  kWh       ← HUB, will be deleted
```

### Step 3 — Delete the new hub statistics

The hub entities have been accumulating a small amount of statistics since installation. These must be removed before renaming to avoid conflicts.

**Replace the IDs below with the HUB (`sensor.hf_hub_*`) `id` values from your Step 2 output:**

```bash
sqlite3 /config/home-assistant_v2.db <<'EOF'
-- Delete statistics accumulated by the new hub entities
DELETE FROM statistics WHERE metadata_id IN (3414, 3413, 3421, 3400, 3419, 3420);
DELETE FROM statistics_short_term WHERE metadata_id IN (3414, 3413, 3421, 3400, 3419, 3420);
DELETE FROM statistics_meta WHERE id IN (3414, 3413, 3421, 3400, 3419, 3420);
EOF
```

### Step 4 — Rename the old statistic IDs to the hub names

This is the core of the migration. By renaming the `statistic_id` in `statistics_meta`, all existing historical rows in `statistics` and `statistics_short_term` are automatically associated with the hub entity — no row-by-row migration needed.

**Replace the IDs below with the SOURCE `id` values from your Step 2 output:**

```bash
sqlite3 /config/home-assistant_v2.db <<'EOF'
-- Rename: old source statistic_id → new hub statistic_id
-- The id is the OLD numeric id that carries all the historical data

UPDATE statistics_meta
  SET statistic_id = 'sensor.hf_hub_grid_imported_energy'
  WHERE id = 260;   -- was sensor.power_meter_consumption

UPDATE statistics_meta
  SET statistic_id = 'sensor.hf_hub_grid_exported_energy'
  WHERE id = 259;   -- was sensor.power_meter_exported

UPDATE statistics_meta
  SET statistic_id = 'sensor.hf_hub_meter_active_power'
  WHERE id = 257;   -- was sensor.power_meter_active_power

UPDATE statistics_meta
  SET statistic_id = 'sensor.hf_hub_inverter_yield_today'
  WHERE id = 252;   -- was sensor.inverter_daily_yield

UPDATE statistics_meta
  SET statistic_id = 'sensor.hf_hub_battery_charged_today'
  WHERE id = 267;   -- was sensor.battery_day_charge

UPDATE statistics_meta
  SET statistic_id = 'sensor.hf_hub_battery_discharged_today'
  WHERE id = 268;   -- was sensor.battery_day_discharge
EOF
```

### Step 5 — Verify the rename

```bash
sqlite3 /config/home-assistant_v2.db <<'EOF'
.mode column
.headers on
SELECT id, statistic_id, unit_of_measurement
FROM statistics_meta
WHERE statistic_id LIKE 'sensor.hf_hub_%'
ORDER BY id;
EOF
```

You should see the **old numeric IDs** now associated with the **new hub statistic_id names**. This confirms the historical data is linked to the hub entities.

### Step 6 — Restart and reconfigure the Energy Dashboard

```bash
ha core start
```

After Home Assistant is back up:

1. Go to **Settings → Dashboards → Energy**
2. Replace each source entity with its hub equivalent:
   - Grid consumption → `sensor.hf_hub_grid_imported_energy`
   - Grid return → `sensor.hf_hub_grid_exported_energy`
   - Grid power measurement → `sensor.hf_hub_meter_active_power` (type: Standard)
   - Solar production → `sensor.hf_hub_inverter_yield_today`
   - Battery charge → `sensor.hf_hub_battery_charged_today`
   - Battery discharge → `sensor.hf_hub_battery_discharged_today`
3. Optionally add these real-time sensors (no migration needed — they show instantaneous values, not cumulative energy):
   - Battery power → `sensor.hf_hub_battery_power`
   - Battery state of charge → `sensor.hf_hub_battery_soc`
   - Solar power → `sensor.hf_hub_pv_input_power`
4. Save

The Energy Dashboard should show the complete historical data with no gaps.

---

## How it works

The `statistics_meta` table maps a `statistic_id` (the entity name string) to a numeric `id`. The `statistics` and `statistics_short_term` tables reference this numeric `id` through the `metadata_id` column. By renaming the `statistic_id` in `statistics_meta`, all existing rows in `statistics` and `statistics_short_term` are automatically associated with the new entity name — the historical data stays exactly where it is.

---

## Troubleshooting

**"Entity not tracked" warning after migration**
The hub entity is not in the recorder's include list or is being caught by an exclude rule. Ensure your `recorder` configuration includes the hub entities you're using in the Energy Dashboard.

**Statistics appear duplicated**
This happens if the new hub statistics were not removed before renaming (Step 3). Stop HA, identify the duplicate `statistics_meta` entries, delete them and their rows from `statistics` / `statistics_short_term`, then restart.

**Historical data shows a small gap**
A gap of minutes to hours around the migration time is expected — this is the window between when the old entity stopped accumulating statistics and the renamed entry started receiving new data from the hub.

---

## Disclaimer

This procedure modifies the Home Assistant SQLite database directly. While the operations are straightforward, errors in SQL commands can corrupt your database or cause data loss. The author of this integration assumes no responsibility for any damage resulting from following this guide. Always work on a backup and verify each step before proceeding.