# Lab 5 - Static Code Analysis

- Name: B V TEJAS
- SRN: PES1UG24CS108
- Section: B

## Links

- Assigned repository: https://github.com/SETAPESU26/L5_47_ecommerce_cart_system
- My fork with the fixes (one commit per tool): https://github.com/Tejas6499/L5_47_ecommerce_cart_system
- Commit history: https://github.com/Tejas6499/L5_47_ecommerce_cart_system/commits/main

## Commits for the fixes

1. Fix Bandit issues: remove eval and os.system, use SHA-256 and secrets, catch KeyError
2. Fix Pylint issues: snake_case names, docstrings, no mutable default or global, main guard
3. Fix Flake8 issues: wrap lines longer than 79 characters

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 3.86/10 | 10.00/10 |
| Bandit | 5 issues (2 High, 1 Medium, 2 Low) | No issues |
| Flake8 | 7 issues | No issues |

## Files in this folder

- `ecommerce_cart_system.py` - the fixed program.
- `issues.md` - table of the issues found and how they were fixed.
- `reflection.md` - answers to the reflection questions.
- `pylint_report_before.txt`, `bandit_report_before.txt`, `flake8_report_before.txt` - reports on the original file.
- `pylint_report_after.txt`, `bandit_report_after.txt`, `flake8_report_after.txt` - reports on the fixed file. The Flake8 report is empty because no issues were found.
