#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path
from dataclasses import dataclass
from typing import List, Literal

INPUT_PATH = Path(__file__).parent / "input.txt"

INPUT_PATTERN = re.compile(r"^<x=(?P<x>\-?\d+), y=(?P<y>\-?\d+), z=(?P<z>\-?\d+)>$")


@dataclass
class _Position:
    """
    Position data

    Public Properties:
        x, y, z (int*3): Position vector
    """

    x: int
    y: int
    z: int


@dataclass
class _Velocity:
    """
    Velocity data

    Public Properties:
        dx, dy, dz (int*3): Velocity vector, default (0, 0, 0)
    """

    dx: int = 0
    dy: int = 0
    dz: int = 0


class _Satellite:
    """
    A class encompassing each satellite's motion

    Args:
        orig_pos_str (str): Input string

    Public Properties:
        p (_Position): Position of this satellite
        v (_Velocity): Velocity of this satellite
    """

    def __init__(self, orig_pos_str: str) -> None:
        params = INPUT_PATTERN.fullmatch(orig_pos_str)
        if params is None:
            raise ValueError(f"Invalid starting position {orig_pos_str}")
        self.p = _Position(int(params["x"]), int(params["y"]), int(params["z"]))
        self.v = _Velocity()

    def __repr__(self) -> str:
        return f"Satellite({self.p}, {self.v})"

    def update_velocity(self, satellites: List[_Satellite]) -> None:
        """
        Update self's velocity using all satellite positions

        Args:
            satellites (list[_Satellite]): All satellites, possibly including self
        """
        # For faster access
        p = self.p
        v = self.v

        for sat in satellites:
            v.dx += _cmp(sat.p.x, p.x)
            v.dy += _cmp(sat.p.y, p.y)
            v.dz += _cmp(sat.p.z, p.z)

    def update_position(self) -> None:
        """
        Update self's position using self's velocity
        """
        self.p.x += self.v.dx
        self.p.y += self.v.dy
        self.p.z += self.v.dz

    def get_total_energy(self) -> int:
        """
        Get total energy of this satellite

        Returns:
            (int): Total energy
        """
        potential = sum(abs(n) for n in (self.p.x, self.p.y, self.p.z))
        kinetic = sum(abs(n) for n in (self.v.dx, self.v.dy, self.v.dz))
        return potential * kinetic


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


# Read input
with INPUT_PATH.open("r") as input_fp:
    satellites = [_Satellite(line.strip()) for line in input_fp]

for _ in range(1000):
    for sat in satellites:
        sat.update_velocity(satellites)
    for sat in satellites:
        sat.update_position()

total_energy = sum(sat.get_total_energy() for sat in satellites)

# Print output
print(total_energy)
