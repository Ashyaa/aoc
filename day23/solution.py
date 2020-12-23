from pathlib import Path
from typing import List


CWD = Path(__file__).parent


class Node:
    def __init__(self, val: int):
        self.val = val
        self.next = None


    def __eq__(self, other):
        return self.val == other.val


    def __ne__(self, other):
        return not self == other


    def __repr__(self):
        return str(self.val)


class LinkedList:
    def __init__(self, nodes: List[int]=None):
        self.list = [Node(n) for n in range(len(nodes)+1)]
        for index, target in enumerate(nodes[1:]):
            self.list[nodes[index]].next = self.list[target]
        self.list[nodes[-1]].next = self.list[nodes[0]]
        self.current = self.list[nodes[0]]
        self.max = len(nodes)


    def play_once(self) -> None:
        popped = self.current.next
        self.current.next = popped.next.next.next
        popped_values = [popped.val, popped.next.val, popped.next.next.val]
        dest = self.current.val - 1 if self.current.val > 1 else self.max
        while dest in popped_values:
            dest = dest - 1 if dest > 1 else self.max
        popped.next.next.next = self.list[dest].next
        self.list[dest].next = popped
        self.current = self.current.next


    def __repr__(self):
        n = self.current
        res = []
        for _ in range(self.max+1):
            res.append(str(n.val))
            n = n.next
        return " -> ".join(res)


    def answer_1(self) -> str:
        node = self.list[1].next
        while node.val != 1:
            node = node.next
        res = []
        node = node.next
        while node.val != 1:
            res.append(str(node.val))
            node = node.next
        return "".join(res)


    def answer_2(self) -> int:
        m = self.list[1].next
        n = m.next
        return m.val * n.val


def read_input(filename: str="input.txt") -> List[int]:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        return [int(c) for c in reader.read().strip()]


def play(cups: List[int], turns: int) -> LinkedList:
    llist = LinkedList(cups)
    for _ in range(turns):
        llist.play_once()
    return llist


def first(cups: List[int], turns: int) -> str:
    return play(cups, turns).answer_1()


def second(cups: List[int]) -> None:
    cups_2 = cups + [i for i in range(max(cups)+1, 1000001)]
    return play(cups_2, 10000000).answer_2()


def test_example() -> None:
    cups = read_input("example.txt")
    assert first(cups, 10) == "92658374"
    assert first(cups, 100) == "67384529"
    assert second(cups) == 149245887792


def run() -> None:
    cups = read_input()
    test_example()
    print("First step:")
    print(first(cups, 100)) # 45798623
    print("\nSecond step:")
    print(second(cups)) # step2