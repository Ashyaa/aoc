from pathlib import Path
from typing import Tuple

CWD = Path(__file__).parent

EXAMPLE = (5764801,17807724)
INPUT = (11404017,13768789)


def transform(n: int, size: int) -> int:
    res = 1
    for _ in range(size):
        res = (res * n) % 20201227
    return res


def loop_size(n: int, key: int) -> int:
    res = 1
    count = 0
    while True:
        res = (res * n) % 20201227
        count += 1
        if res == key:
            return count


def first(keys: Tuple[int, int]) -> None:
    size_card = loop_size(7, keys[0])
    return transform(keys[1], size_card)


def second(keys: Tuple[int, int]) -> None:
    pass


def test_example() -> None:
    assert transform(7, 8) == 5764801
    assert loop_size(7, 5764801) == 8
    assert transform(7, 11) == 17807724
    assert loop_size(7, 17807724) == 11
    assert first(EXAMPLE) == 14897079
    assert second(EXAMPLE) == None


def run() -> None:
    test_example()
    print("First step:")
    print(first(INPUT)) # 18862163
    print("\nSecond step:")
    print(second(INPUT)) # None