from abc import ABCMeta, abstractmethod
from enum import Enum
import functools
from io import TextIOWrapper
from itertools import groupby
import itertools
from typing import Any, Callable, Iterator, TypeVar

rank: dict[str, int] = {
    "A": 12,
    "K": 11,
    "Q": 10,
    "J": 9,
    "T": 8,
    "9": 7,
    "8": 6,
    "7": 5,
    "6": 4,
    "5": 3,
    "4": 2,
    "3": 1,
    "2": 0
}

rank2: dict[str, int] = {
    "A": 12,
    "K": 11,
    "Q": 10,
    "T": 9,
    "9": 8,
    "8": 7,
    "7": 6,
    "6": 5,
    "5": 4,
    "4": 3,
    "3": 2,
    "2": 1,
    "J": 0
}

class Comparable(metaclass=ABCMeta):
    @abstractmethod
    def __lt__(self, other: Any) -> bool: ...

class HandType(Enum):
    FiveOfAKind = 7
    FourOfAKind = 6
    FullHouse = 5
    ThreeOfAKind = 4
    TwoPair = 3
    Pair = 2
    Regular = 1

    def pp(self) -> str:
        name = str(self).split("HandType.")[1]
        return "{0:<14}".format(name)

def hand_type(hand: str) -> HandType:
    occs = [len(list(group)) for _, group in groupby(sorted(hand))]
    match sorted(occs, reverse=True):
        case [5]:			return HandType.FiveOfAKind
        case [4, *_]:		return HandType.FourOfAKind
        case [3, 2, *_]:	return HandType.FullHouse
        case [3, *_]:		return HandType.ThreeOfAKind
        case [2, 2, *_]:	return HandType.TwoPair
        case [2, *_]:		return HandType.Pair
        case _:				return HandType.Regular


T = TypeVar("T", bound=Comparable)
def maximum(xs: Iterator[T]) -> T:
    mx = None
    cmp: Callable[[T, T], bool] = lambda x,y: x > y

    for x in xs:
        if mx is None or cmp(x,mx):
            mx = x
    if mx is None:
        raise ValueError(f"Expected non-empty list, got {list(xs)}")
    return mx

T2 = TypeVar("T2")
def maximum_by(xs: Iterator[T2], cmp: Callable[[T2, T2], int]) -> T2:
    mx = None

    for x in xs:
        if mx is None or cmp(x,mx):
            mx = x
    if mx is None:
        raise ValueError(f"Expected non-empty list, got {list(xs)}")
    return mx


def substitute_joker(hand: str) -> list[str]:
    if not any([x == "J" for x in hand]):
        return [hand]

    xs = sorted(
        list(set([c for c in hand if c != "J"])),
        key=lambda x: rank[x])

    return sub_with("", hand, "J", xs)


def sub_with(prefix: str, curr: str, sub_ch: str, elements: list[str]) -> list[str]:
    match list(curr):
        case [] | [""]:
            return [prefix]
        case [ch, *_] if ch == sub_ch and len(elements) > 0:
            xs = [sub_with(prefix + x, curr[1:], sub_ch, elements) for x in elements]
            return list(itertools.chain.from_iterable(xs))
        case [ch, *_]:
            return sub_with(prefix + ch, curr[1:], sub_ch, elements)
        case xs:
            raise ValueError(f"Unhandled case in sub_with: {xs}")



def with_substitutions(hand: str) -> HandType:
    subs = substitute_joker(hand)
    try:
        return maximum_by(
            map(hand_type, subs),
            cmp=lambda x,y: x.value > y.value)
    except ValueError:
        raise ValueError(f"failed subbing! {hand} => subs: {subs}")

def parse_hands(file: TextIOWrapper) -> list[tuple[str, int]]:
    out: list[tuple[str, int]] = []
    while True:
        match file.readline().split(" "):
            case [""]:
                break
            case [hand, bet]:
                out.append((hand, int(bet)))
            case lexs:
                raise ValueError(f"Unhandled case: {lexs}")
    return out

Tcmp = TypeVar("Tcmp", bound=Comparable)
def cmp(a: Tcmp, b: Tcmp) -> int:
    if a > b: return 1
    elif b < a: return -1
    else: return 0

def cmp_cards(h1: str, h2: str, r: dict[str, int] = rank) -> int:
    for c1, c2 in zip(h1, h2):
        if r[c1] > r[c2]:     return 1
        elif r[c1] < r[c2]:   return -1

    return 0


def cmp_hands(h1: str, h2: str) -> int:
    match list(map(hand_type, [h1,h2])):
        case [ht1, ht2] if ht1.value > ht2.value:
            return 1
        case [ht1, ht2] if ht1.value < ht2.value:
            return -1
        case _:
            return cmp_cards(h1,h2, rank)

def cmp_hands_2(h1: str, h2: str) -> int:
    match list(map(with_substitutions, [h1,h2])):
        case [ht1, ht2] if ht1.value > ht2.value:
            return 1
        case [ht1, ht2] if ht1.value < ht2.value:
            return -1
        case _:
            return cmp_cards(h1,h2, r=rank2)
                # case _:
                #     print(f"{h1 if r > 0 else h2} won!")
                #     return r

def run(file: TextIOWrapper):
    hand_order = zip(
        sorted(
            parse_hands(file),
            key= functools.cmp_to_key(lambda x,y: cmp_hands_2(x[0], y[0]))),
        range(1, 1000000))

    acc: list[tuple[str, int, int]] = []
    for ((hand, bet), rank) in hand_order:
        acc.append((hand, bet, rank))

    s = 0
    for hand, bet, rank in acc:
        s += bet * rank

    print(f"Total winnings: {sum([bet * rank for _, bet, rank in acc])}")