import re

from pathlib import Path
from typing import Dict, List

CWD = Path(__file__).parent

# Expected fields:
# byr (Birth Year)
# iyr (Issue Year)
# eyr (Expiration Year)
# hgt (Height)
# hcl (Hair Color)
# ecl (Eye Color)
# pid (Passport ID)
# cid (Country ID)

MANDATORY_FIELDS: List[str] = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
OPTIONAL_FIELDS: List[str] = ["cid"]
HCL_REGEX = re.compile(r"^#[0-9a-f]{6}$")
PID_REGEX = re.compile(r"^[0-9]{9}$")
VALID_ECL = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]

class Passport:
    data: Dict[str, str]

    def __init__(self, raw: str):
        raw_fields = raw.strip().replace("\n", " ").split(" ")
        self.data = {}
        for element in raw_fields:
            key, value = element.split(":", maxsplit=1)
            if key in MANDATORY_FIELDS or key in OPTIONAL_FIELDS:
                self.data[key] = value
    

    def is_valid_1(self) -> bool:
        return all(field in self.data for field in MANDATORY_FIELDS)


    def byr_valid(self) -> bool:
        try:
            res = int(self.data["byr"])
            return 1920 <= res <= 2002
        except (KeyError, ValueError):
            return False
    

    def iyr_valid(self) -> bool:
        try:
            res = int(self.data["iyr"])
            return 2010 <= res <= 2020
        except (KeyError, ValueError):
            return False
   
   
    def eyr_valid(self) -> bool:
        try:
            res = int(self.data["eyr"])
            return 2020 <= res <= 2030
        except (KeyError, ValueError):
            return False


    def hgt_valid(self) -> bool:
        try:
            raw_hgt = self.data["hgt"]
            height = int(self.data["hgt"][:-2])
            if raw_hgt.endswith("cm"):
                return 150 <= height <= 193
            if raw_hgt.endswith("in"):
                return  59 <= height <= 76
            return False
        except (KeyError, ValueError):
            return False


    def hcl_valid(self) -> bool:
        try:
            return HCL_REGEX.match(self.data["hcl"])
        except (KeyError, ValueError):
            return False


    def ecl_valid(self) -> bool:
        try:
            return self.data["ecl"] in VALID_ECL
        except KeyError:
            return False

    
    def pid_valid(self) -> bool:
        try:
            return PID_REGEX.match(self.data["pid"])
        except KeyError:
            return False


    def is_valid_2(self) -> bool:
        if not self.is_valid_1():
            return False
        for field in MANDATORY_FIELDS:
            if not getattr(self, f"{field}_valid")():
                return False
        return True


def read_input() -> List[Passport]:
    input_file = CWD.joinpath("input.txt")
    res = []
    with open(input_file, "r") as reader:
        raw_passport = ""
        for l in reader.readlines():
            if l == "\n":
                res.append(Passport(raw_passport))
                raw_passport = ""
            else:
                raw_passport += l
        if raw_passport != "":
            res.append(Passport(raw_passport))
    return res


def first(passports: List[Passport]) -> int:
    return len([p for p in passports if p.is_valid_1()])
    

def second(passports: List[Passport]) -> int:
    return len([p for p in passports if p.is_valid_2()])


def run() -> None:
    passport_list = read_input()
    print("Passports found: %d" % len(passport_list))
    print(" ")
    print("First step:")
    nb_valid_1 = first(passport_list)
    print("%d passports are valid in the list!" % nb_valid_1)
    print("\nSecond step:")
    nb_valid_2 = second(passport_list)
    print("%d passports are valid in the list!" % nb_valid_2)
