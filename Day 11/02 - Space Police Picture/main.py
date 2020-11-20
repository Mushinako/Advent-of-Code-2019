#!/usr/bin/env python3
from __future__ import annotations

from enum import IntEnum
from collections import defaultdict
from pathlib import Path
from typing import DefaultDict, Generator, Iterable, Tuple

INPUT_PATH = Path(__file__).parent / "input.txt"


class _OP_CODES(IntEnum):
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
    ADJUST_REL_BASE = 9
    END = 99


class _PARAM_TYPES(IntEnum):
    """
    Enum for parameter types for better readability
    """

    POSITION = 0
    VALUE = 1
    RELATIVE = 2


class _Code_List(list):  # pyright: reportMissingTypeArgument=false
    """
    Basically a list with iterator capabilities

    Properties:
        pointer {int}: Current pointer for iterator
    """

    def __init__(self, it: Iterable[int]) -> None:
        super().__init__(it)  # pyright: reportUnknownMemberType=false
        self.pointer = 0
        self.rel_base = 0

    def __next__(self) -> int:
        curr_pointer = self.pointer
        self.pointer += 1
        if 0 <= curr_pointer < len(self):
            return self[curr_pointer]  # pyright: reportUnknownVariableType=false
        else:
            raise StopIteration()

    def __getitem__(self, index: int) -> int:
        """
        Only allows access of 1 element
        Disallows negative indices
        Allows access outside original data (default 0)
        """
        if index < 0:
            raise IndexError(f"Index cannot be negative; got {index}")
        elif index < len(self):
            return super().__getitem__(index)
        else:
            self += [0] * (index+1-len(self))
            return 0

    def __setitem__(self, index: int, value: int) -> None:
        """
        Only allows access of 1 element
        Disallows negative indices
        Allows access outside original data (default 0)
        """
        if index < 0:
            raise IndexError(f"Index cannot be negative; got {index}")
        elif index < len(self):
            return super().__setitem__(index, value)
        else:
            self += [0] * (index-len(self))
            self += [value]


def _parse_op_code(op_code: int) -> Tuple[int, int, int, int]:
    """
    Parse opcodes into it's components: operation and parameter types

    Args:
        op_code (int): Full operation code

    Returns:
        (int)  : Operation (OP_CODES)
        (int*3): Parameter 1-3 types (PARAM_TYPES)
    """
    # Get rid of everything beyond ten thousand's place
    op_code %= 100000
    # Parameter 3 type on ten-thousand's place
    param3_type, op_code = divmod(op_code, 10000)
    # Parameter 2 type on thousand's place
    param2_type, op_code = divmod(op_code, 1000)
    # Parameter 1 type on hundred's place
    # Operation on ten's and one's place
    param1_type, op = divmod(op_code, 100)
    return op, param1_type, param2_type, param3_type


def _get_op_code(codes: _Code_List) -> Tuple[int, int, int, int]:
    """
    Get next code and try to parse it as operation

    Args:
        codes_iter (Code_List): Iterator of the integer codes

    Returns:
        (int)  : Operation (OP_CODES)
        (int*3): Parameter 1-3 types (PARAM_TYPES)
    """
    op_code = next(codes)
    return _parse_op_code(op_code)


def _get_param_value(codes: _Code_List, param_type: int) -> int:
    """
    Get next code and try to parse it as parameter value

    Args:
        codes_iter (Code_List): Iterator/List of the integer codes
        param_type (int)      : Parameter type (_PARAM_TYPES)

    Returns:
        (int): Parameter value
    """
    value = next(codes)
    # If parameter is a position pointer, access value at corresponding memory space
    if param_type == _PARAM_TYPES.POSITION:
        return codes[value]
    # If parameter is a value, just return it
    elif param_type == _PARAM_TYPES.VALUE:
        return value
    # If parameter is a relative pointer, access value at corresponding memory space
    elif param_type == _PARAM_TYPES.RELATIVE:
        return codes[codes.rel_base+value]
    else:
        raise ValueError(f"{param_type=} unknown param type")

def _get_param_pointer(codes: _Code_List, param_type: int) -> int:
    """
    Get next code and try to parse it as parameter pointer
    Note that the type cannot be `_PARAM_TYPES.VALUE` (1)

    Args:
        codes_iter (Code_List): Iterator/List of the integer codes
        param_type (int)      : Parameter type (_PARAM_TYPES)

    Returns:
        (int): Parameter pointer
    """
    value = next(codes)
    # If parameter is a position pointer, access value at corresponding memory space
    if param_type == _PARAM_TYPES.POSITION:
        return value
    # If parameter is a relative pointer, access value at corresponding memory space
    elif param_type == _PARAM_TYPES.RELATIVE:
        return codes.rel_base+value
    else:
        raise ValueError(f"{param_type=} unknown or invalid param type")

def intcode_calculation(codes: _Code_List) -> Generator[int, int, None]:
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
        op, param1_type, param2_type, param3_type = _get_op_code(codes)
        # End program
        if op == _OP_CODES.END:
            break
        # Addition: Gets 2 params, add, and save result to space pointed to by 3rd param
        if op == _OP_CODES.ADD:
            param1 = _get_param_value(codes, param1_type)
            param2 = _get_param_value(codes, param2_type)
            param3 = _get_param_pointer(codes, param3_type)
            codes[param3] = param1 + param2
        # Multiplication: Gets 2 params, multiply, and save result to space pointed to by
        #   3rd param
        elif op == _OP_CODES.MUL:
            param1 = _get_param_value(codes, param1_type)
            param2 = _get_param_value(codes, param2_type)
            param3 = _get_param_pointer(codes, param3_type)
            codes[param3] = param1 * param2
        # Input: Gets stdin and save result to space pointed to by 1st param
        elif op == _OP_CODES.INPUT:
            inp: int = yield -1
            param1 = _get_param_pointer(codes, param1_type)
            codes[param1] = inp
        # Input: Gets 1 param and save to output
        elif op == _OP_CODES.OUTPUT:
            param1 = _get_param_value(codes, param1_type)
            yield param1
        # Jump if True: Gets 2 params, check if the 1st is non-zero, and jump if true
        elif op == _OP_CODES.JUMP_TRUE:
            param1 = _get_param_value(codes, param1_type)
            param2 = _get_param_value(codes, param2_type)
            if param1:
                codes.pointer = param2
        # Jump if False: Gets 2 params, check if the 1st is zero, and jump if true
        elif op == _OP_CODES.JUMP_FALSE:
            param1 = _get_param_value(codes, param1_type)
            param2 = _get_param_value(codes, param2_type)
            if not param1:
                codes.pointer = param2
        # Less than: Gets 2 params, check if the 1st is less than the 2nd, and save result
        #   to space pointed to by 3rd param
        elif op == _OP_CODES.LESS_THAN:
            param1 = _get_param_value(codes, param1_type)
            param2 = _get_param_value(codes, param2_type)
            param3 = _get_param_pointer(codes, param3_type)
            codes[param3] = int(param1 < param2)
        # Equal: Gets 2 params, check if the 1st equals the 2nd, and save result to space
        #   pointed to by 3rd param
        elif op == _OP_CODES.EQUAL:
            param1 = _get_param_value(codes, param1_type)
            param2 = _get_param_value(codes, param2_type)
            param3 = _get_param_pointer(codes, param3_type)
            codes[param3] = int(param1 == param2)
        # Adjust relative base: Gets 1 param and add to `rel_base`
        elif op == _OP_CODES.ADJUST_REL_BASE:
            param1 = _get_param_value(codes, param1_type)
            codes.rel_base += param1
        else:
            raise ValueError(f"{op=} unknown operation")


# Read input
with INPUT_PATH.open("r") as input_fp:
    codes_list = [int(code.strip()) for code in input_fp.readline().split(",")]

codes = _Code_List(codes_list)
bot = intcode_calculation(codes)

board: DefaultDict[complex, int] = defaultdict(lambda: 0)
direction: complex = 0+1j
position: complex = 0+0j

board[0+0j] = 1

while True:
    try:
        next(bot)
    except StopIteration:
        break
    board[position] = bot.send(board[position])
    direction_change = next(bot)
    if direction_change == 0:
        direction *= 0+1j
    elif direction_change == 1:
        direction *= 0-1j
    else:
        raise ValueError(f"Unknown direction change {direction_change}")
    position += direction
bot.close()

# Print output
heights = set(num.imag for num in board)
min_height = int(min(heights))
max_height = int(max(heights))

widths = set(num.real for num in board)
min_width = int(min(widths)) + 1
max_width = int(max(widths)) + 1

for r in range(max_height, min_height - 1, -1):
    row_str = ""
    for c in range(min_width, max_width + 1):
        color = board[complex(c, r)]
        if color == 0:
            row_str += " "
        elif color == 1:
            row_str += "█"
        else:
            raise ValueError(f"Unknown color {color}")
    print(row_str)
