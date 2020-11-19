#!/usr/bin/env python3
from __future__ import annotations

from collections import Counter
from pathlib import Path

INPUT_PATH = Path(__file__).parent / "input.txt"

WIDTH = 25
HEIGHT = 6

# Read input
with INPUT_PATH.open("r") as input_fp:
    pixels = [int(n) for n in input_fp.read().strip()]

layer_size = WIDTH * HEIGHT
layers = [pixels[i : i + layer_size] for i in range(0, len(pixels), layer_size)]
layers_counters = [Counter(layer) for layer in layers]
min_0_layer = min(layers_counters, key=lambda layer: layer[0])
product = min_0_layer[1] * min_0_layer[2]
print(product)
