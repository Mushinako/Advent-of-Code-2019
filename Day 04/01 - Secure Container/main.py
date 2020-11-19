#!/usr/bin/env python3
from __future__ import annotations

LOWER = 254032
UPPER = 789860

count = 0

# Brute-force through the numbers
for n in range(LOWER, UPPER + 1):
    ns = str(n)
    double = False

    for i in range(len(ns) - 1):
        # Next character is smaller than this one; this number is invalid
        if ns[i] > ns[i + 1]:
            break
        # Next character is same as this one; mark number as double
        elif ns[i] == ns[i + 1]:
            double = True

    else:
        # Add to `count` only if both are satisfactory
        if double:
            count += 1

# Print output
print(count)
