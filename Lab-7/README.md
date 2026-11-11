# Lab 7: Fuzzing for Input Validation Bugs

Name: B V TEJAS
SRN: PES1UG24CS108
Section: B

Application: Fuel Station (same application as Lab 6)

Assigned repository: https://github.com/SETAPESU26/L6_L7_47_fuel_station/tree/main/Lab%207

My repository with the commits: https://github.com/Tejas6499/L6_L7_47_fuel_station/tree/main/Lab%207

## Files

| File | Description |
|------|-------------|
| fuel_station.py | The application (processor.py in the handout) with the input validation bugs fixed |
| test_fuel_station.py | Hypothesis fuzz tests for parse_purchase, volume_average and payable_bill (test_processor.py in the handout) |

## Commands

    pip install hypothesis pytest
    python fuel_station.py
    pytest test_fuel_station.py

Original code: 8 of 10 tests failed. Fixed code: 10 passed.
