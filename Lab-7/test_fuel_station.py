import math

from hypothesis import given, settings, strategies as st
from fuel_station import parse_purchase, volume_average, payable_bill

# Inputs that mix random text with strings that look almost valid, so the
# fuzzer also reaches the number parsing and not only the first split() call.
numbers = st.one_of(
    st.integers(min_value=-10**6, max_value=10**6),
    st.floats(allow_nan=True, allow_infinity=True),
).map(str)
junk = st.text(max_size=20)
grades = st.sampled_from(["regular", "premium", "diesel", "", " ", "Diesel"])

purchase_inputs = st.one_of(
    st.text(), st.none(),
    st.builds(lambda g, n: f"{g}:{n}", grades | junk, numbers | junk),
    st.builds(lambda g, n, m: f"{g}:{n}:{m}", grades, numbers, numbers),
)
volume_inputs = st.one_of(
    st.text(), st.none(),
    st.lists(numbers | junk, max_size=8).map(",".join),
)
bill_inputs = st.one_of(
    st.text(), st.none(),
    st.builds(lambda b, d: f"{b}|{d}", numbers | junk, numbers | junk),
    st.builds(lambda b, d, e: f"{b}|{d}|{e}", numbers, numbers, numbers),
)


def is_number(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


# ---------- parse_purchase ----------
@settings(max_examples=300)
@given(st.text() | st.none())
def test_parse_purchase_no_crash(s):
    try:
        parse_purchase(s)
    except Exception as e:
        assert False, f"parse_purchase crashed with: {e!r}"


@settings(max_examples=300)
@given(purchase_inputs)
def test_parse_purchase_result_is_valid(s):
    try:
        result = parse_purchase(s)
    except Exception as e:
        assert False, f"parse_purchase crashed with: {e!r}"
    if result is not None:
        grade, litres = result
        assert isinstance(grade, str) and grade.strip() != "", f"empty grade for {s!r}"
        assert is_number(litres) and math.isfinite(litres), f"litres not finite for {s!r}"
        assert litres > 0, f"litres must be positive, got {litres} for {s!r}"


@given(st.sampled_from(["regular", "premium", "diesel"]),
       st.integers(min_value=1, max_value=500))
def test_parse_purchase_valid_input(grade, litres):
    assert parse_purchase(f"{grade}:{litres}") == (grade.title(), float(litres))
    assert parse_purchase(f"  {grade} : {litres} ") == (grade.title(), float(litres))


# ---------- volume_average ----------
@settings(max_examples=300)
@given(st.text() | st.none())
def test_volume_average_no_crash(s):
    try:
        volume_average(s)
    except Exception as e:
        assert False, f"volume_average crashed with: {e!r}"


@settings(max_examples=300)
@given(volume_inputs)
def test_volume_average_result_is_valid(s):
    try:
        result = volume_average(s)
    except Exception as e:
        assert False, f"volume_average crashed with: {e!r}"
    if result is not None:
        assert is_number(result) and math.isfinite(result), f"bad average {result!r} for {s!r}"
        assert result >= 0, f"negative average {result} for {s!r}"


@given(st.lists(st.integers(min_value=0, max_value=1000), min_size=1, max_size=20))
def test_volume_average_matches_mean(volumes):
    result = volume_average(",".join(map(str, volumes)))
    expected = sum(volumes) / len(volumes)
    assert math.isclose(result, expected, abs_tol=0.01), \
        f"average of {volumes} should be {expected}, got {result}"
    assert min(volumes) <= result <= max(volumes)


# ---------- payable_bill ----------
@settings(max_examples=300)
@given(st.text() | st.none())
def test_payable_bill_no_crash(s):
    try:
        payable_bill(s)
    except Exception as e:
        assert False, f"payable_bill crashed with: {e!r}"


@settings(max_examples=300)
@given(bill_inputs)
def test_payable_bill_result_is_valid(s):
    try:
        result = payable_bill(s)
    except Exception as e:
        assert False, f"payable_bill crashed with: {e!r}"
    if result is not None:
        assert is_number(result) and math.isfinite(result), f"bill not finite: {result!r} for {s!r}"
        assert result >= 0, f"negative bill {result} for {s!r}"


@given(st.integers(min_value=0, max_value=100000), st.integers(min_value=-1000, max_value=100000))
def test_payable_bill_never_more_than_bill_with_tax(bill, discount):
    result = payable_bill(f"{bill}|{discount}")
    if result is not None:
        assert result <= bill * 1.18 + 0.01, \
            f"payable {result} is more than bill with tax {bill * 1.18} for discount {discount}"


@given(st.integers(min_value=0, max_value=100000), st.integers(min_value=0, max_value=100000))
def test_payable_bill_valid_input(bill, discount):
    expected = max(bill * 1.18 - discount, 0)
    assert math.isclose(payable_bill(f"{bill}|{discount}"), expected, abs_tol=0.01)
