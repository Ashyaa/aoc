from collections import defaultdict
from pathlib import Path
from typing import Dict, List


CWD = Path(__file__).parent


def read_input() -> List[int]:
    input_file = CWD.joinpath("input.txt")
    with open(input_file, "r") as reader:
        tmp = sorted([0] + [int(l) for l in reader.read().rstrip().split("\n")])
        return tmp + [tmp[-1] + 3]


def first(numbers: List[int]) -> int:
    gaps = [numbers[i+1] - numbers[i] for i in range(len(numbers)-1)]
    return len([g for g in gaps if g == 1]) * len([g for g in gaps if g == 3])


def providers(numbers: List[int]) -> Dict[int, List[int]]:
    """ reversed list needed"""
    res = defaultdict(list)
    for i, n in enumerate(numbers):
        j = i+1
        while j < len(numbers):
            if n - numbers[j] > 3:
                break
            res[n].append(numbers[j])
            j +=1
    return res


def second(numbers: List[int]) -> int:
    p = providers(list(reversed(numbers)))
    q = {0: 1}
    for n in numbers[1:]:
      q[n] = 0
      for m in p[n]:
          q[n] += q[m]
    return q[numbers[-1]]


def run() -> None:
    numbers = read_input()
    print("First step:")
    # 2380
    res =first(numbers)
    print(res)
    print("\nSecond step:")
    # 48358655787008
    print(second(numbers))
