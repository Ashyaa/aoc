from functools import reduce
from pathlib import Path
from typing import List, Tuple


CWD = Path(__file__).parent


def read_input() -> List[Tuple[int, int, str]]:
    input_file = CWD.joinpath("input.txt")
    with open(input_file, "r") as reader:
        res = []
        for line in reader.readlines():
            line = line.rstrip()
            if line.startswith("mask"):
                res.append((-1, -1, line[7:]))
                continue
            addr, val = line.replace(" ", "").split("=", maxsplit=1)
            res.append((int(addr[4:-1]), int(val), ""))
        return res


def parse_mask(s: str) -> Tuple[int, int]:
    mask_0_base = reduce(lambda x, y: x|y, [ 1 << 64-i-1 for i in range(64-36)])
    mask_0 = int(s.replace("X", "1"), 2)
    mask_1 = int(s.replace("X", "0"), 2)
    return mask_0_base|mask_0, mask_1


def first(ins: List[Tuple[int, int, str]]) -> int:
    m0, m1, memory = 0, 0, {}
    for index, value, s in ins:
        if s != "":
            m0, m1 = parse_mask(s)
            continue
        v = value | m1
        memory[index] = v & m0
    return reduce(lambda x, y: x+y, [v for v in memory.values()])


def get_mask_list(s: str) -> List[int]:
    if 'X' not in s:
      return [int(s, 2)]
    return [] + get_mask_list(s.replace("X", "1", 1)) + get_mask_list(s.replace("X", "0", 1))


def second(ins: List[Tuple[int, int, str]]) -> int:
    mask_str, mask_1, memory = "", 0, {}
    for addr, val, s in ins:
        if s != "":
            mask_str = s
            mask_1 = int(s.replace("X", "0"), 2)
            continue
        tmp_addr_str = format(addr | mask_1, "036b")
        proto_addr = "".join(["X" if c == "X" else tmp_addr_str[index]
                                for  index, c in enumerate(mask_str)])
        for end_addr in get_mask_list(proto_addr):
            memory[end_addr] = val
    return reduce(lambda x, y: x+y, [v for v in memory.values()])


def run() -> None:
    ins = read_input()
    print("First step:")
    # 17765746710228
    print(first(ins))
    print("\nSecond step:")
    # 4401465949086
    print(second(ins))
