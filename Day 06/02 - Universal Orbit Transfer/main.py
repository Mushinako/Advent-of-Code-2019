#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional

INPUT_PATH = Path(__file__).parent / "input.txt"

YOU_NAME = "YOU"
SANTA_NAME = "SAN"


class Planet:
    """
    Kinda like a tree node. Keeps track of its parent (orbitee)

    Properties:
        name     (str)          : Name of the node
        orbiting (Planet | None): Orbitee
    """

    def __init__(self, name: str) -> None:
        self.name = name
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

    def get_orbitees_names(self) -> List[str]:
        """
        Get the orbitees, closest first

        Returns:
            (list[str]): List of orbitees' names
        """
        if self.orbiting is None:
            return []
        else:
            return [self.orbiting.name] + self.orbiting.get_orbitees_names()


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
        planets[orbitee] = Planet(orbitee)
    if orbiter not in planets:
        planets[orbiter] = Planet(orbiter)
    # Add parent to node
    planets[orbiter].orbiting = planets[orbitee]

your_orbitees = planets[YOU_NAME].get_orbitees_names()
santas_orbitees = planets[SANTA_NAME].get_orbitees_names()

# Remove common parents
while your_orbitees[-1] == santas_orbitees[-1]:
    your_orbitees.pop()
    santas_orbitees.pop()

path_length = len(your_orbitees) + len(santas_orbitees)

# Print output
print(path_length)
