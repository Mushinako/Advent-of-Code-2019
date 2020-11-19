#!/usr/bin/env python3
from __future__ import annotations

from io import TextIOWrapper
from pathlib import Path
from typing import List, Set, Tuple

INPUT_PATH = Path(__file__).parent / "input.txt"


def read_line(fp: TextIOWrapper) -> List[Tuple[str, int]]:
    """
    Read a line from file, split by comma, and separate the first letter from the
      numbers

    Args:
        fp (TextIOWrapper): The file object from which data is read

    Returns:
        (list[tuple[str, int]]): List of direction-stepcount pairs
    """
    return [(a[0], int(a[1:].strip())) for a in fp.readline().split(",")]


def get_coords(line: List[Tuple[str, int]]) -> Set[Tuple[int, int]]:
    """
    Get all the coords a line passes through

    Args:
        line (list[tuple[str, int]]): List of direction-stepcount pairs

    Returns:
        (set[tuple[int, int]]): Set of all x-y coordinates the line goes through
    """
    # Start position at (0, 0)
    x_curr = y_curr = 0
    coords: Set[Tuple[int, int]] = set()
    for direction, step in line:
        # Goes right
        if direction == "R":
            new_coords = {(x, y_curr) for x in range(x_curr + step, x_curr, -1)}
            x_curr += step
        # Goes up
        elif direction == "U":
            new_coords = {(x_curr, y) for y in range(y_curr + step, y_curr, -1)}
            y_curr += step
        # Goes left
        elif direction == "L":
            new_coords = {(x, y_curr) for x in range(x_curr - step, x_curr, 1)}
            x_curr -= step
        # Goes down
        elif direction == "D":
            new_coords = {(x_curr, y) for y in range(y_curr - step, y_curr, 1)}
            y_curr -= step
        else:
            raise ValueError()
        # Add new coords
        coords |= new_coords
    return coords


# Read input
with INPUT_PATH.open("r") as input_fp:
    line1 = read_line(input_fp)
    line2 = read_line(input_fp)

# Get coords each line goes through
coords1 = get_coords(line1)
coords2 = get_coords(line2)
# Get coords where both lines go through
common_coords = coords1 & coords2
# Get the min distance
min_distance = min(abs(x) + abs(y) for x, y in common_coords)

# Print output
print(min_distance)
