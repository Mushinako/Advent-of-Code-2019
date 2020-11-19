#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

INPUT_PATH = Path(__file__).parent / "input.txt"

TARGET = 19690720

# Read input
with INPUT_PATH.open("r") as input_fp:
    code_orig = [int(i.strip()) for i in input_fp.readline().split(",")]

# Brute-force through 0-99 for each input
for i in range(100):
    for j in range(100):
        # Copy and initiate code
        code = code_orig[:]
        code[1] = i
        code[2] = j
        pointer = 0

        while True:
            action = code[pointer]
            # End program if action code is `99`
            if action == 99:
                break
            # Read 2 inputs
            a = code[code[pointer + 1]]
            b = code[code[pointer + 2]]
            # Do the respective calculation
            if action == 1:
                c = a + b
            elif action == 2:
                c = a * b
            else:
                raise ValueError()
            # Write output back
            code[code[pointer + 3]] = c
            # Increment pointer
            pointer += 4

        if code[0] == TARGET:
            # Found it. Print output and quit
            print(100 * i + j)
            sys.exit(0)
