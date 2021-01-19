#!/usr/bin/env python3

import contextlib
import math

from typing import List
from AoC.util import show


class Item:
    def __init__(self, price: int, damage: int, armor: int, name: str) -> None:
        self.price = price
        self.damage = damage
        self.armor = armor
        self.name = name

NO_ITEM = Item(0,0,0,"_")

WEAPON = [
    Item(8,4,0,"Dagger"),
    Item(10,5,0,"Shortsword"),
    Item(25,6,0,"Warhammer"),
    Item(40,7,0,"Longsword"),
    Item(74,8,0,"Greataxe"),
]

ARMOR = [
    NO_ITEM,
    Item(13,0,1,"Leather"),
    Item(31,0,2,"Chainmail"),
    Item(53,0,3,"Splintmail"),
    Item(75,0,4,"Bandedmail"),
    Item(102,0,5,"Platemail"),
]

RING = [
    NO_ITEM,
    NO_ITEM,
    Item(25,1,0,"Dmg+1"),
    Item(50,2,0,"Dmg+2"),
    Item(100,3,0,"Dmg+3"),
    Item(20,0,1,"Dfs+1"),
    Item(40,0,2,"Dfs+2"),
    Item(80,0,3,"Dfs+3"),
]


class Character:
    def __init__(self, hp: int,  damage: int=0, armor: int=0) -> None:
        self.hp = hp
        self.damage = damage
        self.armor = armor
        self.inventory = []


    def equip(self, items: List[Item]) -> None:
        self.inventory = items
        self.armor = self.damage = 0
        for i in items:
            self.armor += i.armor
            self.damage += i.damage


    def golds(self) -> int:
        return sum(i.price for i in self.inventory)


BOSS = Character(103, 9, 2)


def attack(atk: int, dfs: int) -> int:
    return atk - dfs if atk > dfs else 1


def fight(player: Character, boss: Character) -> bool:
    return math.ceil(boss.hp/attack(player.damage, boss.armor)) <= math.ceil(player.hp/attack(boss.damage, player.armor))


def simulate(win: bool) -> List[int]:
    player = Character(100)
    candidates = [ [wp, arm, r1, r2]
        for wp in WEAPON
        for arm in ARMOR
        for i, r1 in enumerate(RING)
        for j, r2 in enumerate(RING)
        if i < j
    ]
    golds = []
    for c in candidates:
        player.equip(c)
        if fight(player, BOSS) == win:
            golds.append(player.golds())
    return golds


@show
def first() -> int:
    return min(simulate(True))


@show
def second() -> int:
    return max(simulate(False))


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        p1 = Character(8,5,5)
        p2 = Character(12,7,2)
        assert fight(p1, p2)


test_example()
first() # 121
second() # 201