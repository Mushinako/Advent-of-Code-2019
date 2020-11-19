#!/usr/bin/env python3
from io import TextIOWrapper
from typing import Dict, List, Set, Tuple


def read_line(fp: TextIOWrapper) -> List[Tuple[str, int]]:
    return [(a[0], int(a[1:].strip())) for a in fp.readline().split(",")]


def get_coords(line: List[Tuple[str, int]]) -> Dict[Tuple[int, int], int]:
    x_curr = y_curr = 0
    coords: Dict[Tuple[int, int], int] = {}
    steps_total = 0
    for direction, step in line:
        if direction == "R":
            for x in range(x_curr + 1, x_curr + step + 1, 1):
                steps_total += 1
                pos = (x, y_curr)
                if pos not in coords:
                    coords[pos] = steps_total
            x_curr += step
        elif direction == "U":
            for y in range(y_curr + 1, y_curr + step + 1, 1):
                steps_total += 1
                pos = (x_curr, y)
                if pos not in coords:
                    coords[pos] = steps_total
            y_curr += step
        elif direction == "L":
            for x in range(x_curr - 1, x_curr - step - 1, -1):
                steps_total += 1
                pos = (x, y_curr)
                if pos not in coords:
                    coords[pos] = steps_total
            x_curr -= step
        elif direction == "D":
            for y in range(y_curr - 1, y_curr - step - 1, -1):
                steps_total += 1
                pos = (x_curr, y)
                if pos not in coords:
                    coords[pos] = steps_total
            y_curr -= step
        else:
            raise ValueError()
    return coords


def main():
    with open("input.txt", "r") as fp:
        line1 = read_line(fp)
        line2 = read_line(fp)
    coords1 = get_coords(line1)
    coords2 = get_coords(line2)
    print(min(coords1[coord] + coords2[coord] for coord in set(coords1) & set(coords2)))


main()