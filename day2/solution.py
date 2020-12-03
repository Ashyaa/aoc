from pathlib import Path
from typing import List

CWD = Path(__file__).parent

class Password:
    character: str
    example: str
    min: int
    max: int

    def __init__(self, raw: str):
        # raw format: "<min>-<max> <char>: <example>""
        elements = raw.split(" ")
        if len(elements) != 3:
            return
        self.character = elements[1][0] # first char of 2nd element
        self.example = elements[2]
        min_str, max_str = elements[0].split("-", maxsplit=1)
        self.min = int(min_str)
        self.max = int(max_str)
    
    def is_valid_1(self) -> bool:
        count = 0
        for c in self.example:
            if c == self.character:
                count += 1
        return self.min <= count <= self.max
    
    def is_valid_2(self) -> bool:
        first_index = self.min - 1
        second_index = self.max - 1
        char_1 = self.example[first_index]
        char_2 = self.example[second_index]
        return (char_1 != char_2) and (self.character == char_1 or self.character == char_2)


def read_input() -> List[Password]:
    input_file = CWD.joinpath("input.txt")
    with open(input_file, "r") as reader:
        return [Password(l) for l in reader.readlines()]


def first(passwords: List[Password]) -> None:
    valid_passwords = [1 for pwd in passwords if pwd.is_valid_1()]
    print(f"The list has {len(valid_passwords)} valid passwords.")


def second(passwords: List[Password]) -> None:
    valid_passwords = [1 for pwd in passwords if pwd.is_valid_2()]
    print(f"The list has {len(valid_passwords)} valid passwords.")


def run() -> None:
    passwords = read_input()
    print(f"Read {len(passwords)} passwords!")
    print("")
    print("First step:")
    first(passwords)
    print("\nSecond step:")
    second(passwords)
