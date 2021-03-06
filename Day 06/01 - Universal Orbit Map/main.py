#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional

INPUT_PATH = Path(__file__).parent / "input.txt"


class Planet:
    """
    Kinda like a tree node. Keeps track of its parent (orbitee)

    Properties:
        orbiting (Planet | None): Orbitee
    """

    def __init__(self) -> None:
        self.orbiting: Optional[Planet] = None

    def get_num_orbits(self) -> int:
        """
        Get the total number of direct and indirect orbits

        Returns:
            (int): The total number of direct and indirect orbits
        """
        if self.orbiting is None:
            return 0
        else:
            return self.orbiting.get_num_orbits() + 1


# Read input
with INPUT_PATH.open("r") as input_fp:
    data = [
        line.split(")")
        for line in (line.strip() for line in input_fp.readlines())
        if line
    ]

planets: Dict[str, Planet] = {}

for orbitee, orbiter in data:
    if orbitee not in planets:
        planets[orbitee] = Planet()
    if orbiter not in planets:
        planets[orbiter] = Planet()
    # Add parent to node
    planets[orbiter].orbiting = planets[orbitee]

sum_orbits = sum(planet.get_num_orbits() for planet in planets.values())

# Print output
print(sum_orbits)
