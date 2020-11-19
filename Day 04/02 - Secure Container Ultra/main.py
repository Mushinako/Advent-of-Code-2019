#!/usr/bin/env python3
from __future__ import annotations

LOWER = 254032
UPPER = 789860

count = 0

# Brute-force through the numbers
for n in range(LOWER, UPPER + 1):
    ns = str(n)
    current_char = ""
    double = False
    combo = 1

    for char in ns:
        # Next character is smaller than this one; this number is invalid
        if current_char > char:
            break
        # Next character is same as this one; increment `combo`
        elif current_char == char:
            combo += 1
        # Next character is larger this one; commit and reset `combo`, mark number as
        #  double iff `combo` is 2
        else:
            if combo == 2:
                double = True
            combo = 1
            current_char = char

    else:
        # Add to `count` only if all are satisfactory
        if double or combo == 2:
            count += 1

# Print output
print(count)
