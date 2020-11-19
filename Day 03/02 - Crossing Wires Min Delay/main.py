#!/usr/bin/env python3
from __future__ import annotations

from io import TextIOWrapper
from pathlib import Path
from typing import Dict, List, Tuple

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


def get_coords(line: List[Tuple[str, int]]) -> Dict[Tuple[int, int], int]:
    """
    Get all the coords a line passes through

    Args:
        line (list[tuple[str, int]]): List of direction-stepcount pairs

    Returns:
        (dict[tuple[int, int], int]): Mapping of all x-y coordinates the line goes
                                      through to the path length
    """
    # Start position at (0, 0)
    x_curr = y_curr = 0
    coords: Dict[Tuple[int, int], int] = {}
    steps_total = 0
    for direction, step in line:
        # Goes right
        if direction == "R":
            for x in range(x_curr + 1, x_curr + step + 1, 1):
                steps_total += 1
                pos = (x, y_curr)
                # Make sure a smaller path length is not overwritten
                if pos not in coords:
                    coords[pos] = steps_total
            x_curr += step
        # Goes up
        elif direction == "U":
            for y in range(y_curr + 1, y_curr + step + 1, 1):
                steps_total += 1
                pos = (x_curr, y)
                # Make sure a smaller path length is not overwritten
                if pos not in coords:
                    coords[pos] = steps_total
            y_curr += step
        # Goes left
        elif direction == "L":
            for x in range(x_curr - 1, x_curr - step - 1, -1):
                steps_total += 1
                pos = (x, y_curr)
                # Make sure a smaller path length is not overwritten
                if pos not in coords:
                    coords[pos] = steps_total
            x_curr -= step
        # Goes down
        elif direction == "D":
            for y in range(y_curr - 1, y_curr - step - 1, -1):
                steps_total += 1
                pos = (x_curr, y)
                # Make sure a smaller path length is not overwritten
                if pos not in coords:
                    coords[pos] = steps_total
            y_curr -= step
        else:
            raise ValueError()
    return coords


# Read input
with INPUT_PATH.open("r") as input_fp:
    line1 = read_line(input_fp)
    line2 = read_line(input_fp)

# Get coords each line goes through and their distance from the origin for that line
coords1 = get_coords(line1)
coords2 = get_coords(line2)
# Get coords where both lines go through
common_coords = set(coords1) & set(coords2)
# Get the min total path length
min_total_path_length = min(coords1[coord] + coords2[coord] for coord in common_coords)

# Print output
print(min_total_path_length)
