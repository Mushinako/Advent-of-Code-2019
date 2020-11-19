#!/usr/bin/env python3
from __future__ import annotations

from enum import IntEnum
from typing import Iterator, List, Tuple


class OP_CODES(IntEnum):
    ADD = 1
    MUL = 2
    INPUT = 3
    OUTPUT = 4
    END = 99


class PARAM_TYPES(IntEnum):
    POINTER = 0
    VALUE = 1


def parse_op_code(op_code: int) -> Tuple[int, int, int]:
    op_code %= 10000
    param2_type, op_code = divmod(op_code, 1000)
    param1_type, op = divmod(op_code, 100)
    return op, param1_type, param2_type


def get_op_code(codes_iter: Iterator[int]) -> Tuple[int, int, int]:
    op_code = next(codes_iter)
    return parse_op_code(op_code)


def get_param(codes_iter: Iterator[int], codes: List[int], param_type: int) -> int:
    value = next(codes_iter)
    if param_type == PARAM_TYPES.POINTER:
        return codes[value]
    elif param_type == PARAM_TYPES.VALUE:
        return value
    else:
        raise ValueError(f"{param_type=} unknown param type")


def main() -> None:
    with open("input.txt", "r") as fp:
        codes = [int(code.strip()) for code in fp.readline().split(",")]
    codes_iter = iter(codes)
    output = 0
    while True:
        op, param1_type, param2_type = get_op_code(codes_iter)
        if op == OP_CODES.END:
            break
        if output:
            raise ValueError(f"{output=} not 0")
        if op == OP_CODES.ADD:
            param1 = get_param(codes_iter, codes, param1_type)
            param2 = get_param(codes_iter, codes, param2_type)
            output_pointer = next(codes_iter)
            codes[output_pointer] = param1 + param2
        elif op == OP_CODES.MUL:
            param1 = get_param(codes_iter, codes, param1_type)
            param2 = get_param(codes_iter, codes, param2_type)
            output_pointer = next(codes_iter)
            codes[output_pointer] = param1 * param2
        elif op == OP_CODES.INPUT:
            inp = int(input("Input: "))
            output_pointer = next(codes_iter)
            codes[output_pointer] = inp
        elif op == OP_CODES.OUTPUT:
            param1 = get_param(codes_iter, codes, param1_type)
            output = param1
        else:
            raise ValueError(f"{op=} unknown operation")
    print(output)


main()