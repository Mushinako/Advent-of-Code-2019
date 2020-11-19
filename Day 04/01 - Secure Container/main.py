#!/usr/bin/env python3
LOWER = 254032
UPPER = 789860


def main():
    count = 0
    for n in range(LOWER, UPPER + 1):
        ns = str(n)
        double = False
        for i in range(len(ns) - 1):
            if ns[i] == ns[i + 1]:
                double = True
            elif ns[i] > ns[i + 1]:
                break
        else:
            if double:
                count += 1
    print(count)


main()