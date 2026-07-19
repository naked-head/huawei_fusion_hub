"""Unit tests for HubCoordinator._normalize (unit conversion)."""
import sys
import os

from types import SimpleNamespace

sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "custom_components")
)

from huawei_fusion_hub.coordinator import HubCoordinator


def _state(value, unit=None, entity_id="sensor.test"):
    return SimpleNamespace(
        state=value,
        attributes={"unit_of_measurement": unit} if unit else {},
        entity_id=entity_id,
    )


def _def(unit):
    return SimpleNamespace(unit=unit)


def test_non_numeric_passthrough():
    assert HubCoordinator._normalize(_def("W"), _state("unavailable")) == "unavailable"


def test_same_unit_no_conversion():
    assert HubCoordinator._normalize(_def("W"), _state("42.5", "W")) == 42.5


def test_missing_units_returns_value():
    assert HubCoordinator._normalize(_def(None), _state("10", "W")) == 10.0
    assert HubCoordinator._normalize(_def("W"), _state("10")) == 10.0


def test_kw_to_w_conversion():
    assert HubCoordinator._normalize(_def("W"), _state("1.5", "kW")) == 1500.0


def test_kvar_to_var_custom():
    # not covered by HA converters — this is our own code path
    assert HubCoordinator._normalize(_def("var"), _state("2.0", "kvar")) == 2000.0


def test_kwh_to_wh_conversion():
    result = HubCoordinator._normalize(_def("Wh"), _state("2.5", "kWh"))
    assert result == 2500.0


if __name__ == "__main__":
    import traceback
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS {t.__name__}")
        except Exception:
            failed += 1
            print(f"FAIL {t.__name__}")
            traceback.print_exc()
    sys.exit(1 if failed else 0)