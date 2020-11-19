#!/usr/bin/env python3
from typing import Dict, Optional


class Planet:
    def __init__(self) -> None:
        self.orbiting: Optional[Planet] = None

    def get_num_orbits(self) -> int:
        if self.orbiting is None:
            return 0
        else:
            return self.orbiting.get_num_orbits() + 1


def main() -> None:
    with open("input.txt", "r") as fp:
        data = [
            line.split(")")
            for line in (line.strip() for line in fp.readlines())
            if line
        ]
    planets: Dict[str, Planet] = {}
    for orbitee, orbiter in data:
        if orbitee not in planets:
            planets[orbitee] = Planet()
        if orbiter not in planets:
            planets[orbiter] = Planet()
        planets[orbiter].orbiting = planets[orbitee]
    print(sum(planet.get_num_orbits() for planet in planets.values()))


main()