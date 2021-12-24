#!/usr/bin/env python3

from pathlib import Path
from typing import *

from AoC.util import show

CWD = Path(__file__).parent


def read_input(filename: str = "input.txt") -> List[Tuple[int, int, int]]:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        res = []
        # operation & first argument are useless, as the code "loops" with limited changes
        # only the 2nd argument matters in lines 5, 6 and 16 of each iteration
        for _ in range(14):
            args = [reader.readline().strip().split(" ")[-1] for _ in range(18)]
            res.append((int(args[4]), int(args[5]), int(args[15])))
        return res


# the input code executes the same function 14 times, taking an input into w (the current digit)
# x and y are only local buffers, reset at each call. the final result is computed in z using a
# stack computation on base-26: z=0 means having en empty stack, a push is z = z = z*26 + value
# and a pop is value = z % 26 and z = z // 26.
# For each of the 14 iterations, two patterns exist:
# if arg_6 is positive, digit + arg_15 is pushed to the stack (z = z*26 + w + arg_15)
# else, arg_6 is negative, and arg_5 is always 26, which is equivalent to a pop on
# our stack. In the second case, the push is only done if w != value + arg_6.
# The input is conveniently 7 times the first pattern and 7 times the second,
# so to keep the stack empty and find a valid serial number, the optional push must
# always be avoided, by ensuring that:
# cur_digit = value + arg_6 = last_digit + last_arg_16 + arg_6
# Again, the input conveniently has arg_6 positive and below 16 in the first pattern, and
# negative in the second pattern, making sure the equality can happen.
@show
def first(inp: List[Tuple[int, int, int]]) -> Tuple[str, str]:
    min_serial = [0] * 14
    max_serial = [0] * 14
    stack: List[Tuple[int,int]] = []
    for i in range(14):
        arg_5, arg_6, arg_16 = inp[i]
        cur_digit = i
        if arg_5 == 1:
            # 1st pattern: push arg_16
            stack.append((cur_digit, arg_16))
        else:
            # 2nd pattern: pop
            prev_digit, prev_val = stack.pop()
            # offset = | last_arg_16 + arg_6 |
            offset = prev_val + arg_6
            if offset < 0:
                cur_digit, prev_digit = prev_digit, cur_digit
                offset *= -1
            # maximize: left-most digit is 9, current digit is 9 - offset
            max_serial[cur_digit] = 9
            max_serial[prev_digit] = 9 - offset
            # minimize: left-most digit is 1, current digit is 1 + offset
            min_serial[cur_digit] = 1 + offset
            min_serial[prev_digit] = 1
    return "".join(str(c) for c in max_serial), "".join(str(c) for c in min_serial)


if __name__ == "__main__":
    inp = read_input()
    first(inp)  # 92928914999991, 91811211611981
