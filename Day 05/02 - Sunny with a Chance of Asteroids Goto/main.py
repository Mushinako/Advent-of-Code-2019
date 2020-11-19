#!/usr/bin/env python3
from __future__ import annotations

from enum import IntEnum
from typing import Iterable, Iterator, List, Tuple


class OP_CODES(IntEnum):
    ADD = 1
    MUL = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_TRUE = 5
    JUMP_FALSE = 6
    LESS_THAN = 7
    EQUAL = 8
    END = 99


class PARAM_TYPES(IntEnum):
    POINTER = 0
    VALUE = 1


class Code_List(list):  # pyright: reportMissingTypeArgument=false
    def __init__(self, it: Iterable[int]) -> None:
        super().__init__(it)  # pyright: reportUnknownMemberType=false
        self.pointer = 0

    def __next__(self) -> int:
        curr_pointer = self.pointer
        self.pointer += 1
        if 0 <= curr_pointer < len(self):
            return self[curr_pointer]  # pyright: reportUnknownVariableType=false
        else:
            raise StopIteration()


def parse_op_code(op_code: int) -> Tuple[int, int, int]:
    op_code %= 10000
    param2_type, op_code = divmod(op_code, 1000)
    param1_type, op = divmod(op_code, 100)
    return op, param1_type, param2_type


def get_op_code(codes: Code_List) -> Tuple[int, int, int]:
    op_code = next(codes)
    return parse_op_code(op_code)


def get_param(codes: Code_List, param_type: int) -> int:
    value = next(codes)
    if param_type == PARAM_TYPES.POINTER:
        return codes[value]
    elif param_type == PARAM_TYPES.VALUE:
        return value
    else:
        raise ValueError(f"{param_type=} unknown param type")


def main() -> None:
    with open("input.txt", "r") as fp:
        codes_list = [int(code.strip()) for code in fp.readline().split(",")]
    codes = Code_List(codes_list)  # pyright: reportGeneralTypeIssues=false
    output: int = 0
    while True:
        op, param1_type, param2_type = get_op_code(codes)
        if op == OP_CODES.END:
            break
        if output:
            raise ValueError(f"{output=} not 0")
        if op == OP_CODES.ADD:
            param1 = get_param(codes, param1_type)
            param2 = get_param(codes, param2_type)
            output_pointer = next(codes)
            codes[output_pointer] = param1 + param2
        elif op == OP_CODES.MUL:
            param1 = get_param(codes, param1_type)
            param2 = get_param(codes, param2_type)
            output_pointer = next(codes)
            codes[output_pointer] = param1 * param2
        elif op == OP_CODES.INPUT:
            inp = int(input("Input: "))
            output_pointer = next(codes)
            codes[output_pointer] = inp
        elif op == OP_CODES.OUTPUT:
            param1 = get_param(codes, param1_type)
            output = param1
        elif op == OP_CODES.JUMP_TRUE:
            param1 = get_param(codes, param1_type)
            param2 = get_param(codes, param2_type)
            if param1:
                codes.pointer = param2
        elif op == OP_CODES.JUMP_FALSE:
            param1 = get_param(codes, param1_type)
            param2 = get_param(codes, param2_type)
            if not param1:
                codes.pointer = param2
        elif op == OP_CODES.LESS_THAN:
            param1 = get_param(codes, param1_type)
            param2 = get_param(codes, param2_type)
            output_pointer = next(codes)
            codes[output_pointer] = int(param1 < param2)
        elif op == OP_CODES.EQUAL:
            param1 = get_param(codes, param1_type)
            param2 = get_param(codes, param2_type)
            output_pointer = next(codes)
            codes[output_pointer] = int(param1 == param2)
        else:
            raise ValueError(f"{op=} unknown operation")
    print(output)


main()