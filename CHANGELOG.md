# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/naked-head/huawei-fusion-hub/compare/0.2.0...HEAD
[0.2.0]: https://github.com/naked-head/huawei-fusion-hub/compare/0.1.0...0.2.0
[0.1.0]: https://github.com/naked-head/huawei-fusion-hub/releases/tag/0.1.0
