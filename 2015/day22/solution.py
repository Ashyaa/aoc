#!/usr/bin/env python3

from copy import deepcopy
from sys import maxsize
from typing import Tuple
from AoC.util import show


class Character:
    def __init__(self, hp: int, atk: int=0, dfs: int=0, mana: int=500) -> None:
        self.hp = hp
        self.atk = atk
        self.dfs = dfs
        self.mana = mana
        self.spent = 0
        self.poison_timer = 0
        self.shield_timer = 0
        self.recharge_timer = 0


    def copy(self):
        return deepcopy(self)


    def poison(self):
        self.poison_timer -= 1
        self.hp -= 3


    def shield(self):
        self.shield_timer -= 1
        self.dfs = 7


    def recharge(self):
        self.recharge_timer -= 1
        self.mana += 101


    def run_effects(self) -> None:
        self.dfs = 0
        if self.poison_timer >0: self.poison()
        if self.recharge_timer >0: self.recharge()
        if self.shield_timer >0: self.shield()


def missile(caster: Character, target: Character) -> None:
    caster.spent += 53
    caster.mana -= 53
    target.hp -= 4


def drain(caster: Character, target: Character) -> None:
    caster.spent += 73
    caster.mana -= 73
    caster.hp += 2
    target.hp -= 2


def shield(caster: Character, target: Character) -> None:
    caster.spent += 113
    caster.mana -= 113
    caster.shield_timer = 6


def poison(caster: Character, target: Character) -> None:
    caster.spent += 173
    caster.mana -= 173
    target.poison_timer = 6


def recharge(caster: Character, target: Character) -> None:
    caster.spent += 229
    caster.mana -= 229
    caster.recharge_timer = 5


SPELLS = [
    (53, missile),
    (73, drain),
    (113, shield),
    (173, poison),
    (229, recharge),
]


def can_cast(player: Character, boss: Character, index: int) -> bool:
    cost, _ = SPELLS[index]
    if index == 2 and player.shield_timer > 0:
        return False
    if index == 3 and boss.poison_timer > 0:
        return False
    if index == 4 and player.recharge_timer > 0:
        return False
    return player.mana >= cost


def attack(atk: int, dfs: int) -> int:
    return atk - dfs if atk > dfs else 1


def fight(player: Character, boss: Character, p2: bool=False, α: int=maxsize) -> Tuple[bool, int]:
    if player.spent > α:
        return False, 0
    player.run_effects()
    boss.run_effects()
    if p2:
        player.hp -= 1
        if player.hp <= 0:
            return False, 0
    if boss.hp <= 0:
        return True, player.spent
    castable = [spell[1] for i, spell in enumerate(SPELLS) if can_cast(player, boss, i)]
    if len(castable) == 0:
        return False, 0
    res = α
    for spell in castable:
        p = player.copy()
        b = boss.copy()
        spell(p, b)
        if b.hp <= 0:
            res = p.spent if p.spent < res else res
            continue
        p.run_effects()
        b.run_effects()
        if b.hp <= 0:
            res = p.spent if p.spent < res else res
            continue
        p.hp -= attack(b.atk, p.dfs)
        if p.hp <= 0:
            continue
        ok, spent = fight(p, b, p2, res)
        if ok:
            res = spent if spent < res else res
    if res < α:
        return True, res
    return False, 0


@show
def first() -> int:
    _, res  = fight(Character(50), Character(58, 9))
    return res


@show
def second() -> int:
    _, res  = fight(Character(50), Character(58, 9), True)
    return res

first() # 1269
second() # 1309