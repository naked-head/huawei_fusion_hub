# Entity correspondence map

Full mapping between Huawei Fusion Hub entities and their sources.

Legend: `—` = not provided by that integration. Source columns show the
pattern used for matching: **register name** (unique_id `{serial}_{register}`)
for Huawei Solar, **device model / signal id** (unique_id `{device_id}_{signal_id}`)
for FusionSolarPlus, **sensor id** (unique_id `fusion_solar-{id}-{sensor_id}`)
for FusionSolar.

A hub sensor is created when **at least one** configured source provides the
quantity; single-source entities have no failover but keep a stable name.

## Inverter (38 entities)

| Hub entity (`sensor.hf_hub_…`) | Huawei Solar (Modbus) | FusionSolarPlus | FusionSolar |
|---|---|---|---|
| `inverter_rated_power` | `rated_power` | `Inverter:10006` | — |
| `inverter_p_max` | `p_max` | — | — |
| `pv_input_power` | `input_power` | `Plant:flow_solar_power` | — |
| `inverter_line_voltage_a_b` | `line_voltage_a_b` | — | — |
| `inverter_line_voltage_b_c` | `line_voltage_b_c` | — | — |
| `inverter_line_voltage_c_a` | `line_voltage_c_a` | — | — |
| `inverter_phase_a_voltage` | `phase_a_voltage` | `Inverter:10011`, `Inverter:10008` | — |
| `inverter_phase_b_voltage` | `phase_b_voltage` | `Inverter:10012` | — |
| `inverter_phase_c_voltage` | `phase_c_voltage` | `Inverter:10013` | — |
| `inverter_phase_a_current` | `phase_a_current` | `Inverter:10014` | — |
| `inverter_phase_b_current` | `phase_b_current` | `Inverter:10015` | — |
| `inverter_phase_c_current` | `phase_c_current` | `Inverter:10016` | — |
| `inverter_day_active_power_peak` | `day_active_power_peak` | — | — |
| `pv_active_power` | `active_power` | `Inverter:10018` | — |
| `inverter_reactive_power` | `reactive_power` | `Inverter:10019` | — |
| `inverter_power_factor` | `power_factor` | `Inverter:10020` | — |
| `inverter_grid_frequency` | `grid_frequency` | `Inverter:10021` | — |
| `inverter_efficiency` | `efficiency` | — | — |
| `inverter_temperature` | `internal_temperature` | `Inverter:10023` | — |
| `inverter_insulation_resistance` | `insulation_resistance` | `Inverter:10024` | — |
| `inverter_status` | `device_status` | `Inverter:10025` | — |
| `inverter_startup_time` | `startup_time` | `Inverter:10027` | — |
| `inverter_shutdown_time` | `shutdown_time` | `Inverter:10028` | — |
| `inverter_yield_total` | `accumulated_yield_energy` | `Inverter:10029` | — |
| `inverter_total_dc_input_energy` | `total_dc_input_power` | — | — |
| `inverter_statistics_time` | `current_electricity_generation_statistics_time` | — | — |
| `inverter_yield_hour` | `hourly_yield_energy` | — | — |
| `inverter_yield_today` | `daily_yield_energy` | `Inverter:10032` | — |
| `inverter_yield_month` | `monthly_yield_energy` | — | — |
| `inverter_yield_year` | `yearly_yield_energy` | — | — |
| `inverter_state_1` | `state_1` | — | — |
| `inverter_output_mode` | — | `Inverter:21029` | — |
| `pv_1_voltage` | `pv_01_voltage` | `Inverter:11001` | — |
| `pv_1_current` | `pv_01_current` | `Inverter:11002` | — |
| `pv_1_power` | — | `Inverter:11003` | — |
| `pv_2_voltage` | `pv_02_voltage` | `Inverter:11004` | — |
| `pv_2_current` | `pv_02_current` | `Inverter:11005` | — |
| `pv_2_power` | — | `Inverter:11006` | — |

## Power Meter (28 entities)

| Hub entity (`sensor.hf_hub_…`) | Huawei Solar (Modbus) | FusionSolarPlus | FusionSolar |
|---|---|---|---|
| `meter_status` | `meter_status` | `Power Sensor:10001` | — |
| `meter_active_power` | `power_meter_active_power` | `Power Sensor:10004`, `Power Sensor:11207`, `Power Sensor:2101271` | — |
| `meter_reactive_power` | `power_meter_reactive_power` | `Power Sensor:10005`, `Power Sensor:11208`, `Power Sensor:2101272` | — |
| `meter_power_factor` | `active_grid_power_factor` | `Power Sensor:10006`, `Power Sensor:10014`, `Power Sensor:2101280` | — |
| `meter_frequency` | `active_grid_frequency` | `Power Sensor:10007` | — |
| `grid_exported_energy` | `grid_exported_energy` | `Power Sensor:10008`, `Power Sensor:11116` | — |
| `grid_imported_energy` | `grid_accumulated_energy` | `Power Sensor:10009`, `Power Sensor:11115` | — |
| `meter_reactive_energy` | `grid_accumulated_reactive_power` | — | — |
| `meter_phase_a_voltage` | `grid_a_voltage` | `Power Sensor:10002`, `Power Sensor:11204`, `Power Sensor:2101256` | — |
| `meter_phase_a_current` | `active_grid_a_current` | `Power Sensor:10003`, `Power Sensor:2101268` | — |
| `meter_phase_a_active_power` | `active_grid_a_power` | `Power Sensor:10019`, `Power Sensor:2101281` | — |
| `meter_phase_b_voltage` | `grid_b_voltage` | `Power Sensor:10010`, `Power Sensor:11205`, `Power Sensor:2101257` | — |
| `meter_phase_b_current` | `active_grid_b_current` | `Power Sensor:10012`, `Power Sensor:2101269` | — |
| `meter_phase_b_active_power` | `active_grid_b_power` | `Power Sensor:10020`, `Power Sensor:2101282` | — |
| `meter_phase_c_voltage` | `grid_c_voltage` | `Power Sensor:10011`, `Power Sensor:11206`, `Power Sensor:2101264` | — |
| `meter_phase_c_current` | `active_grid_c_current` | `Power Sensor:10013`, `Power Sensor:2101270` | — |
| `meter_phase_c_active_power` | `active_grid_c_power` | `Power Sensor:10021`, `Power Sensor:2101283` | — |
| `meter_line_voltage_a_b` | `active_grid_a_b_voltage` | `Power Sensor:2101252` | — |
| `meter_line_voltage_b_c` | `active_grid_b_c_voltage` | `Power Sensor:2101253` | — |
| `meter_line_voltage_c_a` | `active_grid_c_a_voltage` | `Power Sensor:2101254` | — |
| `meter_rs485_port_mode` | — | `Power Sensor:230700283` | — |
| `meter_wifi_signal_strength` | — | `Power Sensor:15101` | — |
| `meter_signal_strength` | — | `Power Sensor:15102` | — |
| `meter_communication_status` | — | `Power Sensor:2101249`, `Power Sensor:2101602` | — |
| `meter_iacmeter` | — | `Power Sensor:2101600` | — |
| `meter_iacmeter_ip` | — | `Power Sensor:2101601` | — |
| `meter_iacmeter_mode` | — | `Power Sensor:2101605` | — |
| `meter_data_source` | — | `Power Sensor:2101606` | — |

## Battery (system) (14 entities)

| Hub entity (`sensor.hf_hub_…`) | Huawei Solar (Modbus) | FusionSolarPlus | FusionSolar |
|---|---|---|---|
| `battery_soc` | `storage_state_of_capacity` | `Battery:10006` | — |
| `battery_power` | `storage_charge_discharge_power` | `Battery:10004` | — |
| `battery_charged_today` | `storage_current_day_charge_capacity` | `Battery:10001` | — |
| `battery_discharged_today` | `storage_current_day_discharge_capacity` | `Battery:10002` | — |
| `battery_total_charge` | `storage_total_charge` | — | — |
| `battery_total_discharge` | `storage_total_discharge` | — | — |
| `battery_status` | `storage_running_status` | `Battery:10003` | — |
| `battery_bus_voltage` | `storage_bus_voltage` | `Battery:10005` | — |
| `battery_bus_current` | `storage_bus_current` | — | — |
| `battery_rated_capacity` | `storage_rated_capacity` | `Battery:10013` | — |
| `battery_max_charge_power` | `storage_maximum_charge_power` | — | — |
| `battery_max_discharge_power` | `storage_maximum_discharge_power` | — | — |
| `battery_working_mode` | — | `Battery:10008` | — |
| `battery_backup_time` | — | `Battery:10015` | — |

## Battery Unit 1 (huawei_solar unit 1 ↔ FSP Module 1) (62 entities)

| Hub entity (`sensor.hf_hub_…`) | Huawei Solar (Modbus) | FusionSolarPlus | FusionSolar |
|---|---|---|---|
| `battery_unit_1_working_mode` | `storage_unit_1_working_mode_b` | — | — |
| `battery_unit_1_charged_today` | `storage_unit_1_current_day_charge_capacity` | `Battery:230320469` | — |
| `battery_unit_1_discharged_today` | `storage_unit_1_current_day_discharge_capacity` | `Battery:230320470` | — |
| `battery_unit_1_bus_current` | `storage_unit_1_bus_current` | `Battery:230320461` | — |
| `battery_unit_1_bus_voltage` | `storage_unit_1_bus_voltage` | `Battery:230320460` | — |
| `battery_unit_1_temperature` | `storage_unit_1_battery_temperature` | `Battery:230320462` | — |
| `battery_unit_1_remaining_time` | `storage_unit_1_remaining_charge_dis_charge_time` | — | — |
| `battery_unit_1_total_charge` | `storage_unit_1_total_charge` | `Battery:230320107` | — |
| `battery_unit_1_total_discharge` | `storage_unit_1_total_discharge` | `Battery:230320108` | — |
| `battery_unit_1_soc` | `storage_unit_1_state_of_capacity` | `Battery:230320463` | — |
| `battery_unit_1_status` | `storage_unit_1_running_status` | `Battery:230320459` | — |
| `battery_unit_1_power` | `storage_unit_1_charge_discharge_power` | `Battery:230320473` | — |
| `battery_unit_1_no` | `storage_unit_1_no` | `Battery:230320252` | — |
| `battery_unit_1_sn` | — | `Battery:230320275` | — |
| `battery_unit_1_software_version` | `storage_unit_1_software_version` | `Battery:230320146` | — |
| `battery_unit_1_fe_connection` | — | `Battery:230320514` | — |
| `battery_unit_1_soh_calibration` | `storage_unit_soh_calibration_status` | — | — |
| `battery_unit_1_pack_1_no` | — | `Battery:230320265` | — |
| `battery_unit_1_pack_1_status` | `storage_unit_1_battery_pack_1_working_status` | `Battery:230320151` | — |
| `battery_unit_1_pack_1_firmware_version` | `storage_unit_1_battery_pack_1_firmware_version` | `Battery:230320148` | — |
| `battery_unit_1_pack_1_serial_number` | `storage_unit_1_battery_pack_1_serial_number` | `Battery:230320147` | — |
| `battery_unit_1_pack_1_voltage` | `storage_unit_1_battery_pack_1_voltage` | `Battery:230320159` | — |
| `battery_unit_1_pack_1_power` | `storage_unit_1_battery_pack_1_charge_discharge_power` | `Battery:230320158` | — |
| `battery_unit_1_pack_1_soc` | `storage_unit_1_battery_pack_1_state_of_capacity` | `Battery:230320152` | — |
| `battery_unit_1_pack_1_max_temperature` | `storage_unit_1_battery_pack_1_maximum_temperature` | `Battery:230320446` | — |
| `battery_unit_1_pack_1_min_temperature` | `storage_unit_1_battery_pack_1_minimum_temperature` | `Battery:230320447` | — |
| `battery_unit_1_pack_1_total_discharge` | `storage_unit_1_battery_pack_1_total_discharge` | `Battery:230320163` | — |
| `battery_unit_1_pack_1_health_check` | — | `Battery:230320492` | — |
| `battery_unit_1_pack_1_heating_status` | — | `Battery:230320498` | — |
| `battery_unit_1_pack_1_current` | `storage_unit_1_battery_pack_1_current` | — | — |
| `battery_unit_1_pack_1_soh_calibration` | `storage_unit_1_battery_pack_1_soh_calibration_status` | — | — |
| `battery_unit_1_pack_1_total_charge` | `storage_unit_1_battery_pack_1_total_charge` | — | — |
| `battery_unit_1_pack_2_no` | — | `Battery:230320266` | — |
| `battery_unit_1_pack_2_status` | `storage_unit_1_battery_pack_2_working_status` | `Battery:230320168` | — |
| `battery_unit_1_pack_2_firmware_version` | `storage_unit_1_battery_pack_2_firmware_version` | `Battery:230320165` | — |
| `battery_unit_1_pack_2_serial_number` | `storage_unit_1_battery_pack_2_serial_number` | `Battery:230320164` | — |
| `battery_unit_1_pack_2_voltage` | `storage_unit_1_battery_pack_2_voltage` | `Battery:230320174` | — |
| `battery_unit_1_pack_2_power` | `storage_unit_1_battery_pack_2_charge_discharge_power` | `Battery:230320173` | — |
| `battery_unit_1_pack_2_soc` | `storage_unit_1_battery_pack_2_state_of_capacity` | `Battery:230320169` | — |
| `battery_unit_1_pack_2_max_temperature` | `storage_unit_1_battery_pack_2_maximum_temperature` | `Battery:230320448` | — |
| `battery_unit_1_pack_2_min_temperature` | `storage_unit_1_battery_pack_2_minimum_temperature` | `Battery:230320449` | — |
| `battery_unit_1_pack_2_total_discharge` | `storage_unit_1_battery_pack_2_total_discharge` | `Battery:230320179` | — |
| `battery_unit_1_pack_2_health_check` | — | `Battery:230320493` | — |
| `battery_unit_1_pack_2_heating_status` | — | `Battery:230320499` | — |
| `battery_unit_1_pack_2_current` | `storage_unit_1_battery_pack_2_current` | — | — |
| `battery_unit_1_pack_2_soh_calibration` | `storage_unit_1_battery_pack_2_soh_calibration_status` | — | — |
| `battery_unit_1_pack_2_total_charge` | `storage_unit_1_battery_pack_2_total_charge` | — | — |
| `battery_unit_1_pack_3_no` | — | `Battery:230320267` | — |
| `battery_unit_1_pack_3_status` | `storage_unit_1_battery_pack_3_working_status` | `Battery:230320184` | — |
| `battery_unit_1_pack_3_firmware_version` | `storage_unit_1_battery_pack_3_firmware_version` | `Battery:230320181` | — |
| `battery_unit_1_pack_3_serial_number` | `storage_unit_1_battery_pack_3_serial_number` | `Battery:230320180` | — |
| `battery_unit_1_pack_3_voltage` | `storage_unit_1_battery_pack_3_voltage` | `Battery:230320190` | — |
| `battery_unit_1_pack_3_power` | `storage_unit_1_battery_pack_3_charge_discharge_power` | `Battery:230320189` | — |
| `battery_unit_1_pack_3_soc` | `storage_unit_1_battery_pack_3_state_of_capacity` | `Battery:230320185` | — |
| `battery_unit_1_pack_3_max_temperature` | `storage_unit_1_battery_pack_3_maximum_temperature` | `Battery:230320450` | — |
| `battery_unit_1_pack_3_min_temperature` | `storage_unit_1_battery_pack_3_minimum_temperature` | `Battery:230320451` | — |
| `battery_unit_1_pack_3_total_discharge` | `storage_unit_1_battery_pack_3_total_discharge` | `Battery:230320194` | — |
| `battery_unit_1_pack_3_health_check` | — | `Battery:230320494` | — |
| `battery_unit_1_pack_3_heating_status` | — | `Battery:230320500` | — |
| `battery_unit_1_pack_3_current` | `storage_unit_1_battery_pack_3_current` | — | — |
| `battery_unit_1_pack_3_soh_calibration` | `storage_unit_1_battery_pack_3_soh_calibration_status` | — | — |
| `battery_unit_1_pack_3_total_charge` | `storage_unit_1_battery_pack_3_total_charge` | — | — |

## Battery Unit 2 (huawei_solar unit 2 ↔ FSP Module 2) (61 entities)

| Hub entity (`sensor.hf_hub_…`) | Huawei Solar (Modbus) | FusionSolarPlus | FusionSolar |
|---|---|---|---|
| `battery_unit_2_working_mode` | `storage_unit_2_working_mode_b` | — | — |
| `battery_unit_2_charged_today` | `storage_unit_2_current_day_charge_capacity` | `Battery:230320471` | — |
| `battery_unit_2_discharged_today` | `storage_unit_2_current_day_discharge_capacity` | `Battery:230320472` | — |
| `battery_unit_2_bus_current` | `storage_unit_2_bus_current` | `Battery:230320466` | — |
| `battery_unit_2_bus_voltage` | `storage_unit_2_bus_voltage` | `Battery:230320465` | — |
| `battery_unit_2_temperature` | `storage_unit_2_battery_temperature` | `Battery:230320467` | — |
| `battery_unit_2_remaining_time` | `storage_unit_2_remaining_charge_dis_charge_time` | — | — |
| `battery_unit_2_total_charge` | `storage_unit_2_total_charge` | `Battery:230320114` | — |
| `battery_unit_2_total_discharge` | `storage_unit_2_total_discharge` | `Battery:230320115` | — |
| `battery_unit_2_soc` | `storage_unit_2_state_of_capacity` | `Battery:230320468` | — |
| `battery_unit_2_status` | `storage_unit_2_running_status` | `Battery:230320464` | — |
| `battery_unit_2_power` | `storage_unit_2_charge_discharge_power` | `Battery:230320474` | — |
| `battery_unit_2_no` | `storage_unit_2_no` | `Battery:230320253` | — |
| `battery_unit_2_sn` | — | `Battery:230320276` | — |
| `battery_unit_2_software_version` | `storage_unit_2_software_version` | `Battery:230320145` | — |
| `battery_unit_2_fe_connection` | — | `Battery:230320515` | — |
| `battery_unit_2_pack_1_no` | — | `Battery:230320268` | — |
| `battery_unit_2_pack_1_status` | `storage_unit_2_battery_pack_1_working_status` | `Battery:230320199` | — |
| `battery_unit_2_pack_1_firmware_version` | `storage_unit_2_battery_pack_1_firmware_version` | `Battery:230320196` | — |
| `battery_unit_2_pack_1_serial_number` | `storage_unit_2_battery_pack_1_serial_number` | `Battery:230320195` | — |
| `battery_unit_2_pack_1_voltage` | `storage_unit_2_battery_pack_1_voltage` | `Battery:230320205` | — |
| `battery_unit_2_pack_1_power` | `storage_unit_2_battery_pack_1_charge_discharge_power` | `Battery:230320204` | — |
| `battery_unit_2_pack_1_soc` | `storage_unit_2_battery_pack_1_state_of_capacity` | `Battery:230320200` | — |
| `battery_unit_2_pack_1_max_temperature` | `storage_unit_2_battery_pack_1_maximum_temperature` | `Battery:230320452` | — |
| `battery_unit_2_pack_1_min_temperature` | `storage_unit_2_battery_pack_1_minimum_temperature` | `Battery:230320453` | — |
| `battery_unit_2_pack_1_total_discharge` | `storage_unit_2_battery_pack_1_total_discharge` | `Battery:230320209` | — |
| `battery_unit_2_pack_1_health_check` | — | `Battery:230320495` | — |
| `battery_unit_2_pack_1_heating_status` | — | `Battery:230320501` | — |
| `battery_unit_2_pack_1_current` | `storage_unit_2_battery_pack_1_current` | — | — |
| `battery_unit_2_pack_1_soh_calibration` | `storage_unit_2_battery_pack_1_soh_calibration_status` | — | — |
| `battery_unit_2_pack_1_total_charge` | `storage_unit_2_battery_pack_1_total_charge` | — | — |
| `battery_unit_2_pack_2_no` | — | `Battery:230320269` | — |
| `battery_unit_2_pack_2_status` | `storage_unit_2_battery_pack_2_working_status` | `Battery:230320214` | — |
| `battery_unit_2_pack_2_firmware_version` | `storage_unit_2_battery_pack_2_firmware_version` | `Battery:230320211` | — |
| `battery_unit_2_pack_2_serial_number` | `storage_unit_2_battery_pack_2_serial_number` | `Battery:230320210` | — |
| `battery_unit_2_pack_2_voltage` | `storage_unit_2_battery_pack_2_voltage` | `Battery:230320220` | — |
| `battery_unit_2_pack_2_power` | `storage_unit_2_battery_pack_2_charge_discharge_power` | `Battery:230320219` | — |
| `battery_unit_2_pack_2_soc` | `storage_unit_2_battery_pack_2_state_of_capacity` | `Battery:230320215` | — |
| `battery_unit_2_pack_2_max_temperature` | `storage_unit_2_battery_pack_2_maximum_temperature` | `Battery:230320454` | — |
| `battery_unit_2_pack_2_min_temperature` | `storage_unit_2_battery_pack_2_minimum_temperature` | `Battery:230320455` | — |
| `battery_unit_2_pack_2_total_discharge` | `storage_unit_2_battery_pack_2_total_discharge` | `Battery:230320224` | — |
| `battery_unit_2_pack_2_health_check` | — | `Battery:230320496` | — |
| `battery_unit_2_pack_2_heating_status` | — | `Battery:230320502` | — |
| `battery_unit_2_pack_2_current` | `storage_unit_2_battery_pack_2_current` | — | — |
| `battery_unit_2_pack_2_soh_calibration` | `storage_unit_2_battery_pack_2_soh_calibration_status` | — | — |
| `battery_unit_2_pack_2_total_charge` | `storage_unit_2_battery_pack_2_total_charge` | — | — |
| `battery_unit_2_pack_3_no` | — | `Battery:230320270` | — |
| `battery_unit_2_pack_3_status` | `storage_unit_2_battery_pack_3_working_status` | `Battery:230320229` | — |
| `battery_unit_2_pack_3_firmware_version` | `storage_unit_2_battery_pack_3_firmware_version` | `Battery:230320226` | — |
| `battery_unit_2_pack_3_serial_number` | `storage_unit_2_battery_pack_3_serial_number` | `Battery:230320225` | — |
| `battery_unit_2_pack_3_voltage` | `storage_unit_2_battery_pack_3_voltage` | `Battery:230320235` | — |
| `battery_unit_2_pack_3_power` | `storage_unit_2_battery_pack_3_charge_discharge_power` | `Battery:230320234` | — |
| `battery_unit_2_pack_3_soc` | `storage_unit_2_battery_pack_3_state_of_capacity` | `Battery:230320230` | — |
| `battery_unit_2_pack_3_max_temperature` | `storage_unit_2_battery_pack_3_maximum_temperature` | `Battery:230320456` | — |
| `battery_unit_2_pack_3_min_temperature` | `storage_unit_2_battery_pack_3_minimum_temperature` | `Battery:230320457` | — |
| `battery_unit_2_pack_3_total_discharge` | `storage_unit_2_battery_pack_3_total_discharge` | `Battery:230320239` | — |
| `battery_unit_2_pack_3_health_check` | — | `Battery:230320497` | — |
| `battery_unit_2_pack_3_heating_status` | — | `Battery:230320503` | — |
| `battery_unit_2_pack_3_current` | `storage_unit_2_battery_pack_3_current` | — | — |
| `battery_unit_2_pack_3_soh_calibration` | `storage_unit_2_battery_pack_3_soh_calibration_status` | — | — |
| `battery_unit_2_pack_3_total_charge` | `storage_unit_2_battery_pack_3_total_charge` | — | — |

## Plant (18 entities)

| Hub entity (`sensor.hf_hub_…`) | Huawei Solar (Modbus) | FusionSolarPlus | FusionSolar |
|---|---|---|---|
| `plant_power` | — | `Plant:flow_solar_power` | `realtime_power` |
| `plant_energy_today` | — | `Plant:dailyEnergy` | `total_current_day_energy` |
| `plant_energy_month` | — | `Plant:monthEnergy` | `total_current_month_energy` |
| `plant_energy_year` | — | `Plant:yearEnergy` | `total_current_year_energy` |
| `plant_energy_total` | — | `Plant:cumulativeEnergy` | `total_lifetime_energy` |
| `plant_income_today` | — | `Plant:dailyIncome` | — |
| `self_used_energy_today` | — | `Plant:totalSelfUseEnergy` | — |
| `consumption_today` | — | `Plant:dailyUseEnergy` | — |
| `pv_self_consumption_energy` | — | `Plant:pvSelfConsumptionEnergy` | — |
| `pv_feed_in_energy_today` | — | `Plant:totalFeedInEnergy` | — |
| `imported_grid_energy_today` | — | `Plant:totalGridImportEnergy` | — |
| `total_consumption` | — | `Plant:totalConsumptionEnergy` | — |
| `grid_import_ratio` | — | `Plant:gridImportRatio` | — |
| `self_consumption_ratio` | — | `Plant:pvSelfConsumptionRatio` | — |
| `self_consumption_ratio_by_production` | — | `Plant:pvSelfConsumptionRatioByProduction` | — |
| `flow_battery_power` | — | `Plant:flow_battery_power` | — |
| `flow_load_power` | — | `Plant:flow_load_power` | — |
| `flow_grid_power` | — | `Plant:flow_grid_power` | — |

## Entities excluded by design

Huawei Solar **writable control entities** (`number.*`, `select.*`, `switch.*`,
`button.*`: battery max charge/discharge power, end-of-charge/discharge SOC,
working mode select, inverter power limits, forcible charge, TOU periods)
are not aggregated: they only exist on the Modbus connection, have no cloud
equivalent to fail over to, and mirroring them as read-only sensors would be
ambiguous. Automations that write keep using the native huawei_solar entities.

**Total hub entities: 221**