from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Set

CWD = Path(__file__).parent

class Food:
    ingredients: Set[str]
    allergens: Set[str]

    def __init__(self, raw: str):
        ings, allergs = raw.split(" (", maxsplit=1)
        self.ingredients = set(ings.split(" "))
        self.allergens = set(allergs.strip()[9:-1].split(", "))


def read_input(filename: str="input.txt") -> List[Food]:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        return [Food(l) for l in reader.readlines()]


def get_allergen_sources(foods: List[Food]) -> Dict[str, str]:
    allergens_list = set()
    for f in foods:
        allergens_list = allergens_list.union(f.allergens)
    found_allergens = defaultdict(str)
    while len(found_allergens) != len(allergens_list):
        for i, f in enumerate(foods):
            unfound_allergens = f.allergens - set(found_allergens.keys())
            unfound_ingredients = f.ingredients - set(found_allergens.values())
            if len(unfound_allergens) == len(unfound_ingredients) == 1:
                found_allergens[unfound_allergens.pop()] = unfound_ingredients.pop()
                continue
            for a in unfound_allergens:
                common_ings = unfound_ingredients
                for j, g in enumerate(foods):
                    if i == j or a not in g.allergens:
                        continue
                    common_ings = common_ings.intersection(g.ingredients)
                    if len(common_ings) == 1:
                        found_allergens[a] = common_ings.pop()
                        break
    return found_allergens


def first(foods: List[Food], allergen_sources: Dict[str, str]) -> int:
    ingredients_list = set()
    for f in foods:
        ingredients_list = ingredients_list.union(f.ingredients)
    safe_ingredients = ingredients_list - set(allergen_sources.values())
    return len([i for f in foods for i in f.ingredients if i in safe_ingredients])


def second(foods: List[Food],allergen_sources: Dict[str, str]) -> str:
    allergens = list(allergen_sources.keys())
    allergens.sort()
    return ','.join([allergen_sources[a] for a in allergens])


def test_example() -> None:
    foods = read_input("example.txt")
    allergen_sources = get_allergen_sources(foods)
    assert first(foods, allergen_sources) == 5
    assert second(foods, allergen_sources) == "mxmxvkd,sqjhc,fvjkl"


def run() -> None:
    test_example()
    foods = read_input()
    allergen_sources = get_allergen_sources(foods)
    print("First step:")
    print(first(foods, allergen_sources)) # 2380
    print("\nSecond step:")
    print(second(foods, allergen_sources)) # ktpbgdn,pnpfjb,ndfb,rdhljms,xzfj,bfgcms,fkcmf,hdqkqhh