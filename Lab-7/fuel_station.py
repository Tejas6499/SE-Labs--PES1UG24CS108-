"""Fuel station helpers: parse a purchase, average pump volumes and work out
the payable bill.

Every function validates its input and returns None for anything it cannot
handle, instead of raising an exception.
"""
import math
import re

GST_RATE = 1.18
MAX_INPUT_LENGTH = 1000
# Plain non-negative decimal number: digits with an optional fractional part.
# This rejects '', 'nan', 'inf', '1e5', '1_000', '-5' and non-ASCII digits.
NUMBER_PATTERN = re.compile(r"[0-9]+(\.[0-9]+)?")
GRADE_PATTERN = re.compile(r"[A-Za-z]+( [A-Za-z]+)*")


def _parse_number(text):
    """Return text as a finite non-negative float, or None if it is not one."""
    text = text.strip()
    if not NUMBER_PATTERN.fullmatch(text):
        return None
    value = float(text)
    if not math.isfinite(value):
        return None
    return value


def _split_two(text, separator):
    """Split text into exactly two parts, or return None."""
    if not isinstance(text, str) or len(text) > MAX_INPUT_LENGTH:
        return None
    parts = text.split(separator)
    if len(parts) != 2:
        return None
    return parts


def parse_purchase(text):
    """Parse 'grade:litres' into (Grade, litres). Return None if invalid."""
    parts = _split_two(text, ':')
    if parts is None:
        return None
    grade = parts[0].strip()
    litres = _parse_number(parts[1])
    if not GRADE_PATTERN.fullmatch(grade) or litres is None or litres <= 0:
        return None
    return grade.title(), litres


def volume_average(volumes_csv):
    """Return the mean of comma separated pump volumes. Return None if invalid."""
    if not isinstance(volumes_csv, str) or len(volumes_csv) > MAX_INPUT_LENGTH:
        return None
    values = []
    for part in volumes_csv.split(','):
        value = _parse_number(part)
        if value is None:
            return None
        values.append(value)
    return round(sum(values) / len(values), 2)


def payable_bill(text):
    """Return bill * 1.18 - discount for 'bill|discount', never below zero.

    Return None if the input is invalid.
    """
    parts = _split_two(text, '|')
    if parts is None:
        return None
    bill = _parse_number(parts[0])
    discount = _parse_number(parts[1])
    if bill is None or discount is None:
        return None
    total = bill * GST_RATE - discount
    if not math.isfinite(total):
        return None
    return round(max(total, 0.0), 2)


def main():
    print("==== Running parse_purchase ====")
    user_input = input("Enter grade:litres (e.g. diesel:25): ")
    result = parse_purchase(user_input)
    if result is None:
        print("Invalid input: expected grade:litres with litres greater than 0")
    else:
        print("Grade and Litres:", result)

    print("\n==== Running volume_average ====")
    user_input = input("Enter pump volumes in litres as CSV (e.g. 10,25,40): ")
    result = volume_average(user_input)
    if result is None:
        print("Invalid input: expected non-negative numbers separated by commas")
    else:
        print("Average Volume:", result)

    print("\n==== Running payable_bill ====")
    user_input = input("Enter bill|discount (e.g. 2500|100): ")
    result = payable_bill(user_input)
    if result is None:
        print("Invalid input: expected bill|discount as non-negative numbers")
    else:
        print("Payable Bill:", result)


if __name__ == "__main__":
    main()
