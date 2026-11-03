"""Test cases written to reach line (code) coverage of fuel_station.py."""
import pytest
from fuel_station import fuel_bill, pump_allowed, session_status


# ---------- fuel_bill ----------
def test_within_covered_litres():
    assert fuel_bill("regular", 8, "silver") == 0


def test_unknown_grade_raises():
    with pytest.raises(ValueError, match="unknown fuel grade"):
        fuel_bill("kerosene", 10, "silver")


def test_negative_litres_raises():
    with pytest.raises(ValueError, match="invalid litres"):
        fuel_bill("regular", -1, "silver")


def test_regular_extra_litres_standard_rate():
    # covered 10, extra 5, rate 105
    assert fuel_bill("regular", 15, "silver") == 5 * 105


def test_premium_gold_gets_five_extra_covered_litres():
    # covered 15 + 5 = 20, extra 20, rate 105
    assert fuel_bill("premium", 40, "gold") == 20 * 105


def test_diesel_standard_rate():
    # covered 20, extra 10, rate 90
    assert fuel_bill("diesel", 30, "silver") == 10 * 90


def test_diesel_gold_bulk_discount():
    # covered 20 (no gold bonus on diesel), extra 40, rate 90 - 6 - 4 = 80
    assert fuel_bill("diesel", 60, "gold") == 40 * 80


# ---------- pump_allowed ----------
def test_pump_allowed():
    assert pump_allowed(30, 1, False) is True


def test_fleet_within_limit():
    assert pump_allowed(150, 5, True) is True


def test_non_fleet_over_litre_limit():
    assert pump_allowed(80, 1, False) is False


# ---------- session_status ----------
def test_card_night_session_active():
    # cutoff = 60 + 30 = 90
    assert session_status(100, True, True) == "active"


def test_cash_day_session_warning():
    # cutoff = 30, warning band is 15 to 29
    assert session_status(20, False, False) == "warning"


def test_session_timed_out():
    assert session_status(5, False, False) == "timed_out"
