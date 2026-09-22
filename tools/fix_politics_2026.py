#!/usr/bin/env python3
"""Apply the audit's politics/economy corrections to patches/history_countries.

Covers the section 5 findings of docs/Audit-2026.md:
  * stale election dates (HOL, KOR, KOS, MLV, EGY, NRY, ALB, POR, BRM),
  * Ukraine's elections_allowed under martial law,
  * Taiwan's implausible debt,
  * GDP-per-capita outliers (TUR, MNT, UZB, KYR, ALB, POL, TAJ).

Run once; re-running is a no-op. Regenerate with `python tools/rebase.py history`
afterwards.
"""
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import rebase  # noqa: E402

ROOT = os.path.join(REPO, "patches", "history_countries")

# (patch tag, description, old text, new text)
EDITS = [
    ("HOL", "last election 2025.10.29",
     'last_election = "2023.11.22"', 'last_election = "2025.10.29"'),
    ("KOR", "last election 2025.6.3 (snap presidential)",
     'last_election = "2024.4.10"', 'last_election = "2025.6.3"'),
    ("KOS", "last election 2025.12.28 (snap)",
     'last_election = "2021.2.14"', 'last_election = "2025.12.28"'),
    ("MLV", "last election 2025.9.28",
     'last_election = "2023.7.11"', 'last_election = "2025.9.28"'),
    ("EGY", "last election 2025.11.10",
     'last_election = "2024.12.10"', 'last_election = "2025.11.10"'),
    ("NOR", "last election 2025.9.8",
     'last_election = "2021.9.13"', 'last_election = "2025.9.8"'),
    ("ALB", "last election 2025.5.11",
     'last_election = "2025.4.25"', 'last_election = "2025.5.11"'),
    ("POR", "last election 2025.5.18",
     'last_election = "2024.3.10"', 'last_election = "2025.5.18"'),
    ("BRM", "elections held 28 Dec 2025 (first phase)",
     'last_election = "2000.1.1"\n\t\telection_frequency = 999\n\t\telections_allowed = no',
     'last_election = "2025.12.28"\n\t\telection_frequency = 60\n\t\telections_allowed = yes'),
    ("UKR", "martial law bars elections",
     'last_election = "2019.4.21"\n\t\telection_frequency = 60\n\t\telections_allowed = yes',
     'last_election = "2019.4.21"\n\t\telection_frequency = 60\n\t\telections_allowed = no'),
    # debt / GDP
    ("TAI", "government debt ~USD 210bn (was 30)",
     'set_variable = { var = debt value = 30.000 }',
     'set_variable = { var = debt value = 210.000 }'),
    ("TUR", "GDP/capita 13.0 -> 18.6 (IMF WEO Oct 2025)",
     'set_variable = { gdp_per_capita = 13.000 }',
     'set_variable = { gdp_per_capita = 18.600 }'),
    ("MNT", "GDP/capita 12.0 -> 7.5",
     'set_variable = { gdp_per_capita = 12.000 }',
     'set_variable = { gdp_per_capita = 7.500 }'),
    ("UZB", "GDP/capita 2.5 -> 4.0",
     'set_variable = { gdp_per_capita = 2.500 }',
     'set_variable = { gdp_per_capita = 4.000 }'),
    ("KYR", "GDP/capita 1.7 -> 3.1",
     'set_variable = { gdp_per_capita = 1.700 }',
     'set_variable = { gdp_per_capita = 3.100 }'),
    ("ALB", "GDP/capita 8.0 -> 12.7",
     'set_variable = { gdp_per_capita = 8.000 }',
     'set_variable = { gdp_per_capita = 12.700 }'),
    ("POL", "GDP/capita 22.0 -> 28.4",
     'set_variable = { gdp_per_capita = 22.000 }',
     'set_variable = { gdp_per_capita = 28.400 }'),
    ("TAJ", "GDP/capita 1.1 -> 1.7",
     'set_variable = { gdp_per_capita = 1.100 }',
     'set_variable = { gdp_per_capita = 1.700 }'),
]


def main():
    applied, skipped, failed = 0, 0, 0
    for tag, why, old, new in EDITS:
        path = os.path.join(ROOT, tag + ".txt")
        if not os.path.exists(path):
            print(f"!! {tag}: no {path}")
            failed += 1
            continue
        text = rebase.read(path)
        if new in text and old not in text:
            skipped += 1
            continue
        n = text.count(old)
        if n != 1:
            print(f"!! {tag}: found {n} occurrences of {old!r}")
            failed += 1
            continue
        rebase.write(path, text.replace(old, new, 1))
        applied += 1
        print(f"ok {tag}: {why}")
    print(f"{applied} applied, {skipped} already done, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
