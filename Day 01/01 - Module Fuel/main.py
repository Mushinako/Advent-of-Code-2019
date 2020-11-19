#!/usr/bin/env python3


def main():
    with open("input.txt", "r") as input_fp:
        masses = [int(m.strip()) for m in input_fp]
    fuel = sum(m // 3 - 2 for m in masses)
    print(fuel)


main()