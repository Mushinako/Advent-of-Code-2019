#!/usr/bin/env python3
from __future__ import annotations

import re
from math import gcd
from functools import reduce
from itertools import count
from pathlib import Path
from dataclasses import dataclass
from typing import List, Literal, Tuple

INPUT_PATH = Path(__file__).parent / "input.txt"

INPUT_PATTERN = re.compile(r"^<x=(?P<x>\-?\d+), y=(?P<y>\-?\d+), z=(?P<z>\-?\d+)>$")


@dataclass
class _Satellite_1D:
    """
    A class encompassing each satellite's motion

    Args:
        position (int): 1D coordinate

    Public Properties:
        p (int): Position of this 1D satellite
        v (int): Velocity of this 1D satellite, default 0
    """

    p: int
    v: int = 0

    def update_velocity(self, satellite_1ds: List[_Satellite_1D]) -> None:
        """
        Update self's velocity using all satellite positions

        Args:
            satellite_1ds (list[_Satellite_1D]): All satellites, possibly including self
        """
        self.v += sum(_cmp(sat.p, self.p) for sat in satellite_1ds)

    def update_position(self) -> None:
        """
        Update self's position using self's velocity
        """
        self.p += self.v


def _cmp(x: int, y: int) -> Literal[-1, 0, 1]:
    """
    Compares 2 `int`; return -1 if x<y, 0 if x==y, 1 if x>y

    Args:
        x, y (int*2): 2 integers

    Returns:
        (-1 | 0 | 1): -1 if x<y, 0 if x==y, 1 if x>y
    """
    if x < y:
        return -1
    elif x > y:
        return 1
    else:
        return 0


def _parse_position(orig_pos_str: str) -> Tuple[int, int, int]:
    """
    Parse input position and extract (x,y,z)

    Input:
        orig_pos_str (str): Input string

    Returns:
        (int*3): xyz coordinate
    """
    params = INPUT_PATTERN.fullmatch(orig_pos_str)
    if params is None:
        raise ValueError(f"Invalid starting position {orig_pos_str}")
    return int(params["x"]), int(params["y"]), int(params["z"])


def _get_1d_cycle(
    satellites: List[_Satellite_1D], satellites_copy: List[_Satellite_1D]
) -> int:
    """
    Get cycle for one dimension

    Args:
        satellites      (list[_Satellite_1D]): List of satellites, for manipulation
        satellites_copy (list[_Satellite_1D]): List of satellites, for comparison

    Returns:
        (int): Length of cycle
    """
    for p in count(1):
        for sat in satellites:
            sat.update_velocity(satellites)
        for sat in satellites:
            sat.update_position()
        if satellites == satellites_copy:
            return p
    return 0  # For my linter


def _lcm(*nums: int) -> int:
    """
    Least common multiple

    Args:
        *nums (int): List of numbers to calculate the least common multiple

    Returns:
        (int): The least common multiple
    """
    return reduce((lambda a, b: a * b // gcd(a, b)), nums, 1)


# Read input
with INPUT_PATH.open("r") as input_fp:
    coords = [_parse_position(line.strip()) for line in input_fp if line]

# Separate x, y, and z
satellite_xs: List[_Satellite_1D] = []
satellite_ys: List[_Satellite_1D] = []
satellite_zs: List[_Satellite_1D] = []
satellite_xs_copy: List[_Satellite_1D] = []
satellite_ys_copy: List[_Satellite_1D] = []
satellite_zs_copy: List[_Satellite_1D] = []

for x, y, z in coords:
    satellite_xs.append(_Satellite_1D(x))
    satellite_ys.append(_Satellite_1D(y))
    satellite_zs.append(_Satellite_1D(z))
    satellite_xs_copy.append(_Satellite_1D(x))
    satellite_ys_copy.append(_Satellite_1D(y))
    satellite_zs_copy.append(_Satellite_1D(z))

x_cycle = _get_1d_cycle(satellite_xs, satellite_xs_copy)
y_cycle = _get_1d_cycle(satellite_ys, satellite_ys_copy)
z_cycle = _get_1d_cycle(satellite_zs, satellite_zs_copy)

# Print output
print(_lcm(x_cycle, y_cycle, z_cycle))
