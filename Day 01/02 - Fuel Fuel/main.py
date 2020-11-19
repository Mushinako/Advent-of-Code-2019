#!/usr/bin/env python3


def main():
    with open("input.txt", "r") as input_fp:
        masses = [int(m.strip()) for m in input_fp]
    fuel_total = 0
    for mass in masses:
        while (fuel := mass // 3 - 2) > 0:
            fuel_total += fuel
            mass = fuel
    print(fuel_total)


main()