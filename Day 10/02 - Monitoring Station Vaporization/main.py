#!/usr/bin/env python3
from __future__ import annotations

import math
from itertools import product
from collections import defaultdict
from pathlib import Path
from typing import DefaultDict, List, Tuple

INPUT_PATH = Path(__file__).parent / "input.txt"

BET_ID = 200
FLOAT_DECIMAL_PRECISION = 10


def _calc_angle(x: int, y: int) -> float:
    """
    Calculate the angle in radians clockwise from positive-y direction

    Args:
        x, y (int*2): x- and y-coordinates

    Returns:
        (float): The angle in radians clockwise from positive-y direction
    """
    # Note that this is `sin(θ)` for regular trig, however we're calculating with respect
    #   to `π/2-θ`, and `sin(θ) == cos(θ-π/2)`
    # 1st and 3rd quadrant
    if x >= 0:
        cos = -y / math.sqrt(x * x + y * y)
        angle = math.acos(cos)
    # 2nd and 3rd quadrant, out of the range of `acos`
    else:
        cos = y / math.sqrt(x * x + y * y)
        angle = math.acos(cos) + math.pi
    return round(angle, 10)


# Read input
with INPUT_PATH.open("r") as input_fp:
    space_map = [list(line.strip()) for line in input_fp if line]

height = len(space_map)
width = len(space_map[0])

max_observed = 221
max_x = max_y = 0
max_slopes: DefaultDict[float, List[Tuple[int, int]]] = defaultdict(lambda: [])

asteroid_locations = [
    (x, y) for y, x in product(range(height), range(width)) if space_map[y][x] == "#"
]

# Get the optimum coordinate
# Iterate through all asteroids as "base coord" (xb, yb)
for xb, yb in asteroid_locations:
    slopes: DefaultDict[float, List[Tuple[int, int]]] = defaultdict(lambda: [])

    # Convert other asteroid's coordinate relative to "base coord"
    for x, y in asteroid_locations:
        x -= xb
        y -= yb
        # Ignore (0, 0), which is the base asteroid
        if x or y:
            slopes[_calc_angle(x, y)].append((x, y))

    if len(slopes) == max_observed:
        max_x = xb
        max_y = yb
        max_slopes = slopes
        break

# Optimum coordinate got
# Sort the dict. Note that `.items()` have to be used, because even though the angle
#   is not recorded, it's used in the sorting process
slopes_sorted = [
    sorted(coords, key=lambda c: abs(c[0]) + abs(c[1]))
    for _, coords in sorted(max_slopes.items())
]

# We know that first turn is 221 shots, so 200 is within the first turn
x, y = slopes_sorted[199][0]

print(100 * (x + max_x) + (y + max_y))
