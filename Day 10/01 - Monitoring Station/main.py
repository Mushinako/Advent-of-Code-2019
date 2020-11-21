#!/usr/bin/env python3
from __future__ import annotations

from math import gcd
from itertools import product
from pathlib import Path
from typing import Set, Tuple

INPUT_PATH = Path(__file__).parent / "input.txt"


def _reduce_num_pair(a: int, b: int) -> Tuple[int, int]:
    """
    Reduce a pair of numbers `(a, b)` such that `gcd(a, b) == 1`

    Args:
        a, b (int*2): The 2 numbers

    Returns:
        (int*2): The pair of reduced numbers
    """
    g = gcd(a, b)
    return a // g, b // g


# Read input
with INPUT_PATH.open("r") as input_fp:
    space_map = [list(line.strip()) for line in input_fp if line]

height = len(space_map)
width = len(space_map[0])

max_observed = 0

asteroid_locations = [
    (r, c) for r, c in product(range(height), range(width)) if space_map[r][c] == "#"
]

# Iterate through all asteroids as "base coord" (rb, cb)
for rb, cb in asteroid_locations:
    slopes: Set[Tuple[int, int]] = set()

    # Convert other asteroid's coordinate relative to "base coord"
    for r, c in asteroid_locations:
        r -= rb
        c -= cb
        # Ignore (0, 0), which is the base asteroid
        if r or c:
            slopes.add(_reduce_num_pair(r, c))

    max_observed = max(max_observed, len(slopes))

# Print output
print(max_observed)