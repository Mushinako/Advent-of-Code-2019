#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

INPUT_PATH = Path(__file__).parent / "input.txt"

# Read input
with INPUT_PATH.open("r") as input_fp:
    code = [int(i.strip()) for i in input_fp.readline().split(",")]

# Initiate code with 2 inputs
code[1] = 12
code[2] = 2

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

# Print output
print(code[0])
