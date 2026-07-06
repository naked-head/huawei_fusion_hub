# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/naked-head/huawei-fusion-hub/compare/0.1.0...HEAD
[0.1.0]: https://github.com/naked-head/huawei-fusion-hub/releases/tag/0.1.0
