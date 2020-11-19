#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

INPUT_PATH = Path(__file__).parent / "input.txt"

# Read input
with INPUT_PATH.open("r") as input_fp:
    masses = [int(m.strip()) for m in input_fp]

# Sum fuel, which is mass//3-2
fuel = sum(m // 3 - 2 for m in masses)

# Print output
print(fuel)
