#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

INPUT_PATH = Path(__file__).parent / "input.txt"

# Read input
with INPUT_PATH.open("r") as input_fp:
    masses = [int(m.strip()) for m in input_fp]

fuel_total = 0

for mass in masses:
    # Keep adding until the amount of fuel required is 0 or less
    while (fuel := mass // 3 - 2) > 0:
        fuel_total += fuel
        mass = fuel

# Print output
print(fuel_total)
