#!/usr/bin/env python3
from io import TextIOWrapper
from typing import List, Set, Tuple


def read_line(fp: TextIOWrapper) -> List[Tuple[str, int]]:
    return [(a[0], int(a[1:].strip())) for a in fp.readline().split(",")]


def get_coords(line: List[Tuple[str, int]]) -> Set[Tuple[int, int]]:
    x_curr = y_curr = 0
    coords: Set[Tuple[int, int]] = set()
    for direction, step in line:
        if direction == "R":
            new_coords = {(x, y_curr) for x in range(x_curr + step, x_curr, -1)}
            x_curr += step
        elif direction == "U":
            new_coords = {(x_curr, y) for y in range(y_curr + step, y_curr, -1)}
            y_curr += step
        elif direction == "L":
            new_coords = {(x, y_curr) for x in range(x_curr - step, x_curr, 1)}
            x_curr -= step
        elif direction == "D":
            new_coords = {(x_curr, y) for y in range(y_curr - step, y_curr, 1)}
            y_curr -= step
        else:
            raise ValueError()
        coords |= new_coords
    return coords


def main():
    with open("input.txt", "r") as fp:
        line1 = read_line(fp)
        line2 = read_line(fp)
    coords1 = get_coords(line1)
    coords2 = get_coords(line2)
    print(min(abs(x) + abs(y) for x, y in coords1 & coords2))


main()