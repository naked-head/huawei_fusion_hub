# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.5.0] - 2026-07-08

### Added

- Optional aggregation of switch and select control entities (inverter on/off, battery working mode, charge from grid, excess PV use in TOU, capacity control mode, MPPT multimodal scanning) as write-through proxies. Off by default; a dedicated config-flow step explains why duplication is discouraged before letting the user opt in. Available in both initial setup and options.
- Entity categories: statuses, identifiers and configuration mirrors are now Diagnostic; control proxies are Configuration — matching the source integrations' device page layout.
- Complete FusionSolar coverage in the mapping: 58 sensors now match FusionSolar Northbound/OpenAPI realtime device data (Residential/String inverter, Battery, Power Sensor, Grid meter) in addition to the Kiosk plant sensors.
- Full localized names for all 221 sensors including the 90 battery pack entities (EN + IT), fixing duplicate labels in Battery Unit device pages.

### Changed

- Device model matching now uses prefix comparison, required for FusionSolar residential inverters whose model string includes the inverter type.
- ENTITY_MAP.md regenerated: complete FusionSolar column (Kiosk + OpenAPI) and new Controls section.

## [0.4.0] - 2026-07-07

### Added

- Options flow now allows adding or removing source integrations at any time, not just changing priority order.
- Entity names are now fully localized via `translation_key`: English and Italian translations included for all 131 named sensors and binary sensors.
- `icon@2x.png` (512×512) added to the `brand/` directory for correct display in HA device pages.

### Changed

- `brand/` directory renamed from `brands/` to match HACS specification.
- README rewritten following the ha-ilmeteo template: badges, feature list, installation, configuration, automation examples.
- Options flow priority step now preserves the previous order for unchanged sources when sources are added or removed.

## [0.3.0] - 2026-07-07

### Added

- Full entity coverage: 221 canonical sensors covering the complete union of the three sources, including single-source entities (inverter phase B/C, line voltages, DC input energy, hourly yield; meter three-phase and alternative meter models; battery system max power; battery units 1-2 with per-pack detail matching FSP Modules 1-2; full plant statistics, income and flows). See ENTITY_MAP.md.
- Battery Unit 1 and Battery Unit 2 sub-devices (huawei_solar battery units ↔ FusionSolarPlus Modules).
- Initial discovery summary notification: on first setup the hub reports how many entities were created, grouped per device and per source.
- Automatic rediscovery: when a source integration is installed or re-added later, the hub detects the new registry entities (debounced), creates the missing hub entities at runtime and notifies the user with grouped counts; existing entities gaining an additional fallback source are reported too.
- Online notification when a source comes back (the offline one is dismissed automatically).

### Changed

- mapping.py is now generated programmatically from structured tables instead of a hand-written list.
- Release tags use the `v` prefix from v0.3.0 onward.

## [0.2.0] - 2026-07-07

### Added

- Logical sub-devices: hub sensors are now grouped into Inverter, Battery, Power Meter and Plant devices, linked to the main hub device via `via_device`.
- Language-independent entity discovery: matching is now based on registry unique_ids (huawei_solar register names, FusionSolarPlus numeric signal ids with device-model disambiguation, FusionSolar sensor ids), with object_id fallback for older source versions.
- Device class agreement check between canonical definition and source entity to prevent false matches.

### Changed

- FusionSolarPlus matching uses `Model:pattern` syntax to disambiguate signal ids reused across device types (e.g. 10004 is meter active power and battery charge/discharge power).

## [0.1.0] - 2026-07-06

### Added

- Initial release.
- Priority-based aggregation of Huawei Solar (Modbus), FusionSolar (Kiosk/OpenAPI) and FusionSolarPlus entities.
- 15 canonical sensors covering inverter, meter and battery quantities with automatic unit normalization.
- Per-source connectivity binary sensors.
- Offline/online events on the HA event bus and optional persistent notifications.
- UI config flow with auto-detection of installed sources and configurable priority.
- Options flow to change priority and alert behavior without restart.
- English and Italian translations.

[Unreleased]: https://github.com/naked-head/huawei-fusion-hub/compare/v0.5.0...HEAD
[0.5.0]: https://github.com/naked-head/huawei-fusion-hub/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/naked-head/huawei-fusion-hub/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/naked-head/huawei-fusion-hub/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/naked-head/huawei-fusion-hub/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/naked-head/huawei-fusion-hub/releases/tag/v0.1.0
