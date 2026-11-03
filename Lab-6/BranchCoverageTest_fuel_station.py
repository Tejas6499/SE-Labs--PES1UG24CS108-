"""Test cases written to reach branch coverage of fuel_station.py.

Every decision is taken both ways, and the boundary values are tested on
both sides (for example 30 and 31 extra litres, 60 and 61 litres).
"""
import pytest
from fuel_station import fuel_bill, pump_allowed, session_status


# ---------- fuel_bill: validation ----------
def test_within_covered_litres():
    assert fuel_bill("regular", 8, "silver") == 0


@pytest.mark.parametrize("grade", ["kerosene", "", "REGULAR"])
def test_unknown_grade_raises(grade):
    with pytest.raises(ValueError, match="unknown fuel grade"):
        fuel_bill(grade, 10, "silver")


def test_negative_litres_raises():
    with pytest.raises(ValueError, match="invalid litres"):
        fuel_bill("regular", -1, "silver")


def test_unknown_grade_is_checked_before_litres():
    with pytest.raises(ValueError, match="unknown fuel grade"):
        fuel_bill("kerosene", -5, "silver")


def test_zero_litres_is_valid_and_free():
    assert fuel_bill("diesel", 0, "silver") == 0


# ---------- fuel_bill: covered litres and gold bonus ----------
@pytest.mark.parametrize(
    "grade, litres, expected",
    [
        ("regular", 10, 0),      # exactly covered
        ("regular", 11, 105),    # one litre over
        ("premium", 15, 0),
        ("premium", 16, 105),
        ("diesel", 20, 0),
        ("diesel", 21, 90),
    ],
)
def test_voucher_boundary_non_gold(grade, litres, expected):
    assert fuel_bill(grade, litres, "silver") == expected


@pytest.mark.parametrize(
    "grade, litres, expected",
    [
        ("regular", 15, 0),      # 10 + 5 gold bonus
        ("regular", 16, 105),
        ("premium", 20, 0),      # 15 + 5 gold bonus
        ("premium", 21, 105),
        ("diesel", 20, 0),       # gold gets no bonus on diesel
        ("diesel", 21, 90),
    ],
)
def test_voucher_boundary_gold(grade, litres, expected):
    assert fuel_bill(grade, litres, "gold") == expected


def test_other_loyalty_tier_gets_no_bonus():
    assert fuel_bill("regular", 15, "bronze") == 5 * 105


# ---------- fuel_bill: bulk discount (extra > 30) ----------
def test_extra_exactly_30_has_no_bulk_discount():
    assert fuel_bill("regular", 40, "silver") == 30 * 105


def test_extra_31_regular_non_gold_bulk_discount():
    assert fuel_bill("regular", 41, "silver") == 31 * 99


def test_extra_30_gold_has_no_bulk_discount():
    assert fuel_bill("regular", 45, "gold") == 30 * 105


def test_extra_31_regular_gold_extra_discount():
    assert fuel_bill("regular", 46, "gold") == 31 * 95


def test_extra_31_diesel_non_gold():
    assert fuel_bill("diesel", 51, "silver") == 31 * 84


def test_extra_31_diesel_gold():
    assert fuel_bill("diesel", 51, "gold") == 31 * 80


# ---------- pump_allowed ----------
@pytest.mark.parametrize(
    "litres, containers, expected",
    [
        (200, 0, True),      # fleet, at the limit
        (201, 0, False),     # fleet, over the limit
        (100, 10, True),     # fleet ignores container count
    ],
)
def test_fleet_requests(litres, containers, expected):
    assert pump_allowed(litres, containers, True) is expected


@pytest.mark.parametrize(
    "litres, containers, expected",
    [
        (30, 1, True),
        (30, 0, True),
        (60, 1, True),       # at the litre limit
        (61, 1, False),      # over the litre limit
        (30, 2, False),      # too many containers
        (61, 2, False),
    ],
)
def test_non_fleet_requests(litres, containers, expected):
    assert pump_allowed(litres, containers, False) is expected


# ---------- session_status ----------
@pytest.mark.parametrize(
    "card, night, cutoff",
    [
        (False, False, 30),
        (True, False, 60),
        (False, True, 60),
        (True, True, 90),
    ],
)
def test_session_status_bands(card, night, cutoff):
    assert session_status(cutoff, card, night) == "active"
    assert session_status(cutoff - 1, card, night) == "warning"
    assert session_status(cutoff - 15, card, night) == "warning"
    assert session_status(cutoff - 16, card, night) == "timed_out"


def test_session_zero_seconds_left():
    assert session_status(0, True, True) == "timed_out"
