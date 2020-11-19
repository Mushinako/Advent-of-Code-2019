#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

INPUT_PATH = Path(__file__).parent / "input.txt"

WIDTH = 25
HEIGHT = 6

# Read input
with INPUT_PATH.open("r") as input_fp:
    pixels = [int(n) for n in input_fp.read().strip()]

layer_size = WIDTH * HEIGHT
layers = [pixels[i : i + layer_size] for i in range(0, len(pixels), layer_size)]

picture = [["."] * WIDTH for _ in range(HEIGHT)]

for layer in layers[::-1]:
    for i in range(HEIGHT):
        for j, cell in enumerate(layer[i * WIDTH : i * WIDTH + WIDTH]):
            if cell == 0:
                picture[i][j] = "#"
            elif cell == 1:
                picture[i][j] = " "

for row in picture:
    print("".join(row))