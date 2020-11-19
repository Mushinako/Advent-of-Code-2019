#!/usr/bin/env python3
from __future__ import annotations

from enum import IntEnum
from itertools import permutations
from pathlib import Path
from typing import Generator, Iterable, Tuple

INPUT_PATH = Path(__file__).parent / "input.txt"


class OP_CODES(IntEnum):
    """
    Enum for opcodes for better readability
    """

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
    """
    Enum for parameter types for better readability
    """

    POINTER = 0
    VALUE = 1


class Code_List(list):  # pyright: reportMissingTypeArgument=false
    """
    Basically a list with iterator capabilities

    Properties:
        pointer {int}: Current pointer for iterator
    """

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


def get_op_code(codes: Code_List) -> Tuple[int, int, int]:
    """
    Get next code and try to parse it as operation

    Args:
        codes_iter (Code_List): Iterator of the integer codes

    Returns:
        (int): Operation (OP_CODES)
        (int): Parameter 1 type (PARAM_TYPES)
        (int): Parameter 2 type (PARAM_TYPES)
    """
    op_code = next(codes)
    return parse_op_code(op_code)


def get_param(codes: Code_List, param_type: int) -> int:
    """
    Get next code and try to parse it as parameter

    Args:
        codes_iter (Code_List): Iterator/List of the integer codes
        param_type (int)      : Parameter type (PARAM_TYPES)

    Returns:
        (int): Parameter value
    """
    value = next(codes)
    # If parameter is a pointer, access value at corresponding memory space
    if param_type == PARAM_TYPES.POINTER:
        return codes[value]
    # If parameter is a value, just return it
    elif param_type == PARAM_TYPES.VALUE:
        return value
    else:
        raise ValueError(f"{param_type=} unknown param type")


def intcode_calculation(codes: Code_List) -> Generator[int, int, None]:
    """
    IntCode computer coroutine

    Args:
        codes (Code_List): Initial code

    Sends:
        inp (int): Outside input for op 3

    Yields:
        (int): Final result
    """
    while True:
        op, param1_type, param2_type = get_op_code(codes)
        # End program
        if op == OP_CODES.END:
            break
        # Addition: Gets 2 params, add, and save result to space pointed to by 3rd param
        if op == OP_CODES.ADD:
            param1 = get_param(codes, param1_type)
            param2 = get_param(codes, param2_type)
            output_pointer = next(codes)
            codes[output_pointer] = param1 + param2
        # Multiplication: Gets 2 params, multiply, and save result to space pointed to by
        #   3rd param
        elif op == OP_CODES.MUL:
            param1 = get_param(codes, param1_type)
            param2 = get_param(codes, param2_type)
            output_pointer = next(codes)
            codes[output_pointer] = param1 * param2
        # Input: Gets stdin and save result to space pointed to by 1st param
        elif op == OP_CODES.INPUT:
            inp: int = yield 0
            output_pointer = next(codes)
            codes[output_pointer] = inp
        # Input: Gets 1 param and save to output
        elif op == OP_CODES.OUTPUT:
            param1 = get_param(codes, param1_type)
            yield param1
        # Jump if True: Gets 2 params, check if the 1st is non-zero, and jump if true
        elif op == OP_CODES.JUMP_TRUE:
            param1 = get_param(codes, param1_type)
            param2 = get_param(codes, param2_type)
            if param1:
                codes.pointer = param2
        # Jump if False: Gets 2 params, check if the 1st is zero, and jump if true
        elif op == OP_CODES.JUMP_FALSE:
            param1 = get_param(codes, param1_type)
            param2 = get_param(codes, param2_type)
            if not param1:
                codes.pointer = param2
        # Less than: Gets 2 params, check if the 1st is less than the 2nd, and save result
        #   to space pointed to by 3rd param
        elif op == OP_CODES.LESS_THAN:
            param1 = get_param(codes, param1_type)
            param2 = get_param(codes, param2_type)
            output_pointer = next(codes)
            codes[output_pointer] = int(param1 < param2)
        # Equal: Gets 2 params, check if the 1st equals the 2nd, and save result to space
        #   pointed to by 3rd param
        elif op == OP_CODES.EQUAL:
            param1 = get_param(codes, param1_type)
            param2 = get_param(codes, param2_type)
            output_pointer = next(codes)
            codes[output_pointer] = int(param1 == param2)
        else:
            raise ValueError(f"{op=} unknown operation")


# Read input
with INPUT_PATH.open("r") as input_fp:
    codes_list = [int(code.strip()) for code in input_fp.readline().split(",")]

max_result = 0

# Permute all possible configurations
for configs in permutations(range(5, 10)):
    prev_result = 0
    result = 0
    stopped = False

    # Initialize amplifiers
    amplifiers = [intcode_calculation(Code_List(codes_list)) for _ in range(5)]
    for amp, config in zip(amplifiers, configs):
        next(amp)
        amp.send(config)

    while True:
        # A->E loop
        for amp in amplifiers:
            result = amp.send(result)
            try:
                next(amp)
            # The code has exited
            except StopIteration:
                stopped = True

        if result > prev_result:
            prev_result = result

        # The code has exited
        if stopped:
            break

    # Check if thrust is max yet
    if result > max_result:
        max_result = result

# Print output
print(max_result)
