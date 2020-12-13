import math
from functools import reduce
from pathlib import Path
from typing import List, Tuple

CWD = Path(__file__).parent


def read_input() -> Tuple[int, List[int]]:
    input_file = CWD.joinpath("input.txt")
    with open(input_file, "r") as reader:
        estimate = int(reader.readline())
        return estimate, [int(s) if not s.startswith("x") else -1 for s in reader.readline().split(",")]


def first(est: int, times: List[int]) -> int:
    candidates = [(math.ceil(est / t) * t, t) for t in times if t > 0]
    m, ID = min(candidates, key=lambda t:t[0])
    return (m % est) * ID


def extended_euclidian(a, b: int) -> Tuple[int,int]:
    if a == 0:
        return 0, 1
    u1, v1 = extended_euclidian(b%a, a)
    return v1 - (b//a) * u1, u1


def second(times: List[int]) -> int:
    # x % t[n] = -index
    ts = [((-index%t), t) for index, t in enumerate(times) if t > 0]
    n = reduce(lambda x, y: x*y, [t for _, t in ts])
    remainders = []
    for shift, t in ts:
        m = n // t
        _, v = extended_euclidian(t,m)
        remainders.append(v * m * shift)
    return reduce(lambda x, y: x+y, remainders)%n


def run() -> None:
    est, times = read_input()
    print("First step:")
    # 4782
    print(first(est, times))
    print("\nSecond step:")
    # 1118684865113056
    print(second(times))
