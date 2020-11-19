#!/usr/bin/env python3
from __future__ import annotations

from enum import IntEnum
from pathlib import Path
from typing import Iterator, List, Tuple

INPUT_PATH = Path(__file__).parent / "input.txt"


class OP_CODES(IntEnum):
    """
    Enum for opcodes for better readability
    """

    ADD = 1
    MUL = 2
    INPUT = 3
    OUTPUT = 4
    END = 99


class PARAM_TYPES(IntEnum):
    """
    Enum for parameter types for better readability
    """

    POINTER = 0
    VALUE = 1


def parse_op_code(op_code: int) -> Tuple[int, int, int]:
    """
    Parse opcodes into it's components: operation and parameter types
    The type for third parameter, if any, is ignored because it should always be 0

    Args:
        op_code (int): Full operation code

    Returns:
        (int): Operation (OP_CODES)
        (int): Parameter 1 type (PARAM_TYPES)
        (int): Parameter 2 type (PARAM_TYPES)
    """
    # Get rid of everything beyond thousand's place
    op_code %= 10000
    # Parameter 2 type on thousand's place
    param2_type, op_code = divmod(op_code, 1000)
    # Parameter 1 type on hundred's place
    # Operation on ten's and one's place
    param1_type, op = divmod(op_code, 100)
    return op, param1_type, param2_type


def get_op_code(codes_iter: Iterator[int]) -> Tuple[int, int, int]:
    """
    Get next code and try to parse it as operation

    Args:
        codes_iter (Iterator[int]): Iterator of the integer codes

    Returns:
        (int): Operation (OP_CODES)
        (int): Parameter 1 type (PARAM_TYPES)
        (int): Parameter 2 type (PARAM_TYPES)
    """
    op_code = next(codes_iter)
    return parse_op_code(op_code)


def get_param(codes_iter: Iterator[int], codes: List[int], param_type: int) -> int:
    """
    Get next code and try to parse it as parameter

    Args:
        codes_iter (Iterator[int]): Iterator of the integer codes, for `next()`
        codes      (list[int])    : List of the integer codes, for accessing at index
        param_type (int)          : Parameter type (PARAM_TYPES)

    Returns:
        (int): Parameter value
    """
    value = next(codes_iter)
    # If parameter is a pointer, access value at corresponding memory space
    if param_type == PARAM_TYPES.POINTER:
        return codes[value]
    # If parameter is a value, just return it
    elif param_type == PARAM_TYPES.VALUE:
        return value
    else:
        raise ValueError(f"{param_type=} unknown param type")


# Read input
with INPUT_PATH.open("r") as input_fp:
    codes = [int(code.strip()) for code in input_fp.readline().split(",")]

codes_iter = iter(codes)
output = 0

while True:
    op, param1_type, param2_type = get_op_code(codes_iter)
    # End program
    if op == OP_CODES.END:
        break
    # Output should always be `0` if it's not returned
    if output:
        raise ValueError(f"{output=} not 0")
    # Addition: Gets 2 params and save result to space pointed to by 3rd param
    if op == OP_CODES.ADD:
        param1 = get_param(codes_iter, codes, param1_type)
        param2 = get_param(codes_iter, codes, param2_type)
        output_pointer = next(codes_iter)
        codes[output_pointer] = param1 + param2
    # Multiplication: Gets 2 params and save result to space pointed to by 3rd param
    elif op == OP_CODES.MUL:
        param1 = get_param(codes_iter, codes, param1_type)
        param2 = get_param(codes_iter, codes, param2_type)
        output_pointer = next(codes_iter)
        codes[output_pointer] = param1 * param2
    # Input: Gets stdin and save result to space pointed to by 1st param
    elif op == OP_CODES.INPUT:
        inp = int(input("Input: "))
        output_pointer = next(codes_iter)
        codes[output_pointer] = inp
    # Input: Gets 1 param and save to output
    elif op == OP_CODES.OUTPUT:
        param1 = get_param(codes_iter, codes, param1_type)
        output = param1
    else:
        raise ValueError(f"{op=} unknown operation")

# Print output
print(output)
